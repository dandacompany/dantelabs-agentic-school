import { readFile, writeFile, readdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Package root directory
const PACKAGE_ROOT = join(__dirname, '../../..');

const CONFIG_CACHE_FILE = '.dantelabs-cache.json';
const CACHE_TTL = 1000 * 60 * 60; // 1 hour

// GitHub configuration
export const GITHUB_CONFIG = {
  owner: 'dandacompany',
  repo: 'dantelabs-agentic-school',
  branch: 'master',
  get rawBase() {
    return `https://raw.githubusercontent.com/${this.owner}/${this.repo}/${this.branch}`;
  },
  get apiBase() {
    return `https://api.github.com/repos/${this.owner}/${this.repo}`;
  }
};

/**
 * Get marketplace configuration
 * First tries local, then fetches from GitHub with caching
 */
export async function getMarketplaceConfig(options = {}) {
  const { useCache = true, forceRefresh = false, useLocal = true } = options;

  // Try local first (when installed via npm)
  if (useLocal) {
    const localConfig = await getLocalConfig();
    if (localConfig) {
      return localConfig;
    }
  }

  // Try cache
  if (useCache && !forceRefresh) {
    const cached = await getCachedConfig();
    if (cached) {
      return cached;
    }
  }

  // Fetch from GitHub
  const config = await fetchRemoteConfig();

  // Save to cache
  await saveCachedConfig(config);

  return config;
}

/**
 * Get local marketplace config (when package is installed)
 */
async function getLocalConfig() {
  try {
    // Go up from cli/src/lib to root, then to .claude-plugin
    const localPath = join(__dirname, '../../..', '.claude-plugin/marketplace.json');
    if (existsSync(localPath)) {
      const content = await readFile(localPath, 'utf8');
      return JSON.parse(content);
    }
  } catch {
    // Fall through to remote fetch
  }
  return null;
}

/**
 * Fetch config from GitHub
 */
async function fetchRemoteConfig() {
  const url = `${GITHUB_CONFIG.rawBase}/.claude-plugin/marketplace.json`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch marketplace config: ${response.status}`);
  }

  return response.json();
}

/**
 * Get cached config
 */
async function getCachedConfig() {
  try {
    const cacheFile = join(process.cwd(), CONFIG_CACHE_FILE);
    if (!existsSync(cacheFile)) {
      return null;
    }

    const cached = JSON.parse(await readFile(cacheFile, 'utf8'));

    // Check TTL
    if (Date.now() - cached.timestamp > CACHE_TTL) {
      return null;
    }

    return cached.data;
  } catch {
    return null;
  }
}

/**
 * Save config to cache
 */
async function saveCachedConfig(config) {
  try {
    const cacheFile = join(process.cwd(), CONFIG_CACHE_FILE);
    await writeFile(cacheFile, JSON.stringify({
      timestamp: Date.now(),
      data: config
    }, null, 2));
  } catch {
    // Ignore cache write errors
  }
}

/**
 * Normalize source path (handle both 'path' and 'source' fields)
 */
export function getSourcePath(plugin) {
  const source = plugin.source || plugin.path;
  if (!source) return `plugins/${plugin.name}`;
  return source.replace(/^\.\//, '');
}

/**
 * Discover components by scanning local plugin directory
 */
async function discoverLocalComponents(pluginPath) {
  const components = { agents: [], commands: [], skills: [] };

  // Scan agents directory
  const agentsDir = join(pluginPath, 'agents');
  if (existsSync(agentsDir)) {
    const files = await readdir(agentsDir);
    components.agents = files
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }

  // Scan commands directory
  const commandsDir = join(pluginPath, 'commands');
  if (existsSync(commandsDir)) {
    const files = await readdir(commandsDir);
    components.commands = files
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }

  // Scan skills directory
  const skillsDir = join(pluginPath, 'skills');
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
  const components = { agents: [], commands: [], skills: [] };

  const fetchDir = async (path) => {
    const url = `${GITHUB_CONFIG.apiBase}/contents/${path}?ref=${GITHUB_CONFIG.branch}`;
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'dantelabs-agentic-school-cli'
      }
    });
    if (!response.ok) return [];
    return response.json();
  };

  // Scan agents directory
  try {
    const agentsContents = await fetchDir(`${remotePath}/agents`);
    components.agents = agentsContents
      .filter(f => f.type === 'file' && f.name.endsWith('.md'))
      .map(f => f.name.replace('.md', ''));
  } catch (e) { /* no agents dir */ }

  // Scan commands directory
  try {
    const commandsContents = await fetchDir(`${remotePath}/commands`);
    components.commands = commandsContents
      .filter(f => f.type === 'file' && f.name.endsWith('.md'))
      .map(f => f.name.replace('.md', ''));
  } catch (e) { /* no commands dir */ }

  // Scan skills directory
  try {
    const skillsContents = await fetchDir(`${remotePath}/skills`);
    components.skills = skillsContents
      .filter(f => f.type === 'dir')
      .map(f => f.name);
  } catch (e) { /* no skills dir */ }

  return components;
}

/**
 * Enrich plugin with discovered components
 */
export async function enrichPluginWithComponents(plugin) {
  // If components already exist, return as is
  if (plugin.components && Object.keys(plugin.components).length > 0) {
    return plugin;
  }

  const sourcePath = getSourcePath(plugin);
  const localPath = join(PACKAGE_ROOT, sourcePath);

  let components;
  if (existsSync(localPath)) {
    components = await discoverLocalComponents(localPath);
  } else {
    components = await discoverRemoteComponents(sourcePath);
  }

  return { ...plugin, components };
}

/**
 * Validate plugin name
 */
export function validatePluginName(name, config) {
  const plugin = config.plugins.find(p => p.name === name);
  return plugin || null;
}

/**
 * Get plugin dependencies
 */
export function getPluginDependencies(pluginName, config) {
  const deps = [];

  // Common is always a dependency unless it's the plugin itself
  if (pluginName !== 'common') {
    const common = config.plugins.find(p => p.name === 'common');
    if (common) {
      deps.push(common);
    }
  }

  return deps;
}
