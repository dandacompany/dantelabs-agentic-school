import { mkdir, writeFile, rm, readFile, readdir, stat, cp } from 'fs/promises';
import { join, dirname } from 'path';
import { existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { fetchFile, downloadDirectory } from './downloader.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Get root directory of the package
const PACKAGE_ROOT = join(__dirname, '../../..');

/**
 * Ensure directory exists
 */
async function ensureDir(dir) {
  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }
}

/**
 * Check if local plugin source exists
 */
function hasLocalSource(sourcePath) {
  const localPath = join(PACKAGE_ROOT, sourcePath);
  return existsSync(localPath);
}

/**
 * Copy directory recursively
 */
async function copyDirectory(src, dest) {
  await ensureDir(dest);
  const entries = await readdir(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);

    if (entry.isDirectory()) {
      await copyDirectory(srcPath, destPath);
    } else {
      await cp(srcPath, destPath);
    }
  }
}

/**
 * Discover components by scanning plugin directory
 */
async function discoverComponents(localPath) {
  const components = { agents: [], commands: [], skills: [] };

  // Scan agents directory
  const agentsDir = join(localPath, 'agents');
  if (existsSync(agentsDir)) {
    const files = await readdir(agentsDir);
    components.agents = files
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }

  // Scan commands directory
  const commandsDir = join(localPath, 'commands');
  if (existsSync(commandsDir)) {
    const files = await readdir(commandsDir);
    components.commands = files
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }

  // Scan skills directory
  const skillsDir = join(localPath, 'skills');
  if (existsSync(skillsDir)) {
    const entries = await readdir(skillsDir, { withFileTypes: true });
    components.skills = entries
      .filter(e => e.isDirectory())
      .map(e => e.name);
  }

  return components;
}

/**
 * Discover components from remote GitHub directory
 */
async function discoverRemoteComponents(remotePath) {
  const { getDirectoryContents } = await import('./downloader.js');
  const components = { agents: [], commands: [], skills: [] };

  // Scan agents directory
  try {
    const agentsContents = await getDirectoryContents(`${remotePath}/agents`);
    components.agents = agentsContents
      .filter(f => f.type === 'file' && f.name.endsWith('.md'))
      .map(f => f.name.replace('.md', ''));
  } catch (e) { /* no agents dir */ }

  // Scan commands directory
  try {
    const commandsContents = await getDirectoryContents(`${remotePath}/commands`);
    components.commands = commandsContents
      .filter(f => f.type === 'file' && f.name.endsWith('.md'))
      .map(f => f.name.replace('.md', ''));
  } catch (e) { /* no commands dir */ }

  // Scan skills directory
  try {
    const skillsContents = await getDirectoryContents(`${remotePath}/skills`);
    components.skills = skillsContents
      .filter(f => f.type === 'dir')
      .map(f => f.name);
  } catch (e) { /* no skills dir */ }

  return components;
}

/**
 * Normalize source path (handle both 'path' and 'source' fields)
 */
function getSourcePath(plugin) {
  // Support both old 'path' format and new 'source' format
  const source = plugin.source || plugin.path;
  if (!source) return `plugins/${plugin.name}`;
  // Remove leading './' if present
  return source.replace(/^\.\//, '');
}

/**
 * Install a single plugin to .claude directory
 *
 * Source structure (plugins/):
 *   plugins/{plugin-name}/
 *   ├── agents/{agent}.md
 *   ├── commands/{command}.md
 *   └── skills/{skill-name}/
 *
 * Target structure (.claude/):
 *   .claude/
 *   ├── agents/{plugin-name}/{agent}.md
 *   ├── commands/{plugin-name}/{command}.md
 *   └── skills/{skill-name}/
 */
export async function installPlugin(plugin, claudeDir, options = {}) {
  const { force = false, onProgress } = options;
  const pluginName = plugin.name;
  const sourcePath = getSourcePath(plugin); // e.g., "plugins/brand-analytics"

  // Determine if we should use local or remote source
  const useLocalSource = hasLocalSource(sourcePath);
  const localSourcePath = join(PACKAGE_ROOT, sourcePath);

  // Discover components dynamically (or use provided components for backward compatibility)
  let components = plugin.components;
  if (!components || Object.keys(components).length === 0) {
    if (useLocalSource) {
      components = await discoverComponents(localSourcePath);
    } else {
      components = await discoverRemoteComponents(sourcePath);
    }
  }

  // Create base directories
  await ensureDir(join(claudeDir, 'agents'));
  await ensureDir(join(claudeDir, 'commands'));
  await ensureDir(join(claudeDir, 'skills'));

  const results = {
    plugin: pluginName,
    agents: 0,
    commands: 0,
    skills: 0
  };

  // Install agents
  if (components.agents?.length) {
    const agentsTargetDir = join(claudeDir, 'agents', pluginName);
    await ensureDir(agentsTargetDir);

    for (const agentName of components.agents) {
      const targetPath = join(agentsTargetDir, `${agentName}.md`);

      if (!force && existsSync(targetPath)) {
        throw new Error(`File exists: ${targetPath}. Use --force to overwrite.`);
      }

      try {
        let content;
        if (useLocalSource) {
          const localFilePath = join(localSourcePath, 'agents', `${agentName}.md`);
          content = await readFile(localFilePath, 'utf8');
        } else {
          const remotePath = `${sourcePath}/agents/${agentName}.md`;
          content = await fetchFile(remotePath);
        }

        await writeFile(targetPath, content);
        results.agents++;

        if (onProgress) {
          onProgress('agent', agentName);
        }
      } catch (err) {
        throw new Error(`Failed to install agent ${agentName}: ${err.message}`);
      }
    }
  }

  // Install commands
  if (components.commands?.length) {
    const commandsTargetDir = join(claudeDir, 'commands', pluginName);
    await ensureDir(commandsTargetDir);

    for (const commandName of components.commands) {
      const targetPath = join(commandsTargetDir, `${commandName}.md`);

      if (!force && existsSync(targetPath)) {
        throw new Error(`File exists: ${targetPath}. Use --force to overwrite.`);
      }

      try {
        let content;
        if (useLocalSource) {
          const localFilePath = join(localSourcePath, 'commands', `${commandName}.md`);
          content = await readFile(localFilePath, 'utf8');
        } else {
          const remotePath = `${sourcePath}/commands/${commandName}.md`;
          content = await fetchFile(remotePath);
        }

        await writeFile(targetPath, content);
        results.commands++;

        if (onProgress) {
          onProgress('command', commandName);
        }
      } catch (err) {
        throw new Error(`Failed to install command ${commandName}: ${err.message}`);
      }
    }
  }

  // Install skills (preserve full directory structure)
  if (components.skills?.length) {
    for (const skillName of components.skills) {
      const skillTargetDir = join(claudeDir, 'skills', skillName);

      if (!force && existsSync(skillTargetDir)) {
        throw new Error(`Directory exists: ${skillTargetDir}. Use --force to overwrite.`);
      }

      // Remove existing if force
      if (force && existsSync(skillTargetDir)) {
        await rm(skillTargetDir, { recursive: true });
      }

      await ensureDir(skillTargetDir);

      try {
        if (useLocalSource) {
          const localSkillPath = join(localSourcePath, 'skills', skillName);
          await copyDirectory(localSkillPath, skillTargetDir);
        } else {
          const remotePath = `${sourcePath}/skills/${skillName}`;
          await downloadDirectory(remotePath, skillTargetDir);
        }
        results.skills++;

        if (onProgress) {
          onProgress('skill', skillName);
        }
      } catch (err) {
        throw new Error(`Failed to install skill ${skillName}: ${err.message}`);
      }
    }
  }

  return results;
}

/**
 * Uninstall a plugin from .claude directory
 */
export async function uninstallPlugin(plugin, claudeDir) {
  const pluginName = plugin.name;
  const sourcePath = getSourcePath(plugin);

  // Discover components dynamically (or use provided components for backward compatibility)
  let components = plugin.components;
  if (!components || Object.keys(components).length === 0) {
    const useLocalSource = hasLocalSource(sourcePath);
    const localSourcePath = join(PACKAGE_ROOT, sourcePath);

    if (useLocalSource) {
      components = await discoverComponents(localSourcePath);
    } else {
      components = await discoverRemoteComponents(sourcePath);
    }
  }

  const results = {
    plugin: pluginName,
    agents: 0,
    commands: 0,
    skills: 0
  };

  // Remove agents
  if (components.agents?.length) {
    const agentsDir = join(claudeDir, 'agents', pluginName);
    if (existsSync(agentsDir)) {
      await rm(agentsDir, { recursive: true });
      results.agents = components.agents.length;
    }
  }

  // Remove commands
  if (components.commands?.length) {
    const commandsDir = join(claudeDir, 'commands', pluginName);
    if (existsSync(commandsDir)) {
      await rm(commandsDir, { recursive: true });
      results.commands = components.commands.length;
    }
  }

  // Remove skills
  if (components.skills?.length) {
    for (const skillName of components.skills) {
      const skillDir = join(claudeDir, 'skills', skillName);
      if (existsSync(skillDir)) {
        await rm(skillDir, { recursive: true });
        results.skills++;
      }
    }
  }

  return results;
}
