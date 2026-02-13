import { existsSync } from 'fs';
import { join } from 'path';

/**
 * Detect which plugins are already installed in the target directory.
 *
 * Checks for:
 * - agents/{pluginName}/ directory
 * - commands/{pluginName}/ directory
 * - skills/{skillName}/ directory (per skill)
 *
 * @param {Array} plugins - Enriched plugins with components
 * @param {string} baseDir - Base installation directory (e.g. /project/.claude)
 * @param {object} platformConfig - Platform configuration from platforms.js
 * @returns {Map<string, { installed: boolean, installedComponents: { agents: string[], commands: string[], skills: string[] } }>}
 */
export function detectInstalledPlugins(plugins, baseDir, platformConfig) {
  const result = new Map();

  for (const plugin of plugins) {
    const components = plugin.components || {};
    const installedComponents = { agents: [], commands: [], skills: [] };

    // Check agents
    if (platformConfig.agents && components.agents?.length) {
      const agentsDir = join(baseDir, platformConfig.agents, plugin.name);
      if (existsSync(agentsDir)) {
        for (const agent of components.agents) {
          const agentFile = join(agentsDir, `${agent}.md`);
          if (existsSync(agentFile)) {
            installedComponents.agents.push(agent);
          }
        }
      }
    }

    // Check commands
    if (platformConfig.commands && components.commands?.length) {
      const commandsDir = join(baseDir, platformConfig.commands, plugin.name);
      if (existsSync(commandsDir)) {
        for (const cmd of components.commands) {
          const cmdFile = join(commandsDir, `${cmd}.md`);
          if (existsSync(cmdFile)) {
            installedComponents.commands.push(cmd);
          }
        }
      }
    }

    // Check skills (skills use skill name directly, not plugin name)
    if (components.skills?.length) {
      for (const skill of components.skills) {
        const skillDir = join(baseDir, platformConfig.skills, skill);
        if (existsSync(skillDir)) {
          installedComponents.skills.push(skill);
        }
      }
    }

    const hasAny =
      installedComponents.agents.length > 0 ||
      installedComponents.commands.length > 0 ||
      installedComponents.skills.length > 0;

    result.set(plugin.name, {
      installed: hasAny,
      installedComponents
    });
  }

  return result;
}
