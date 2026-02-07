/**
 * Platform definitions for multi-platform skill installation.
 *
 * Each platform maps to a specific directory structure and
 * declares which component types (skills, agents, commands) it supports.
 * A `null` value means the platform does not support that component type.
 */

export const PLATFORMS = {
  claude: {
    name: 'Claude Code',
    dir: '.claude',
    skills: 'skills',
    agents: 'agents',
    commands: 'commands',
    description: 'Anthropic Claude Code',
  },
  gemini: {
    name: 'Gemini CLI',
    dir: '.gemini',
    skills: 'skills',
    agents: 'agents',
    commands: null,
    description: 'Google Gemini CLI',
  },
  antigravity: {
    name: 'Antigravity',
    dir: '.agent',
    skills: 'skills',
    agents: null,
    commands: null,
    description: 'Google Antigravity IDE',
  },
  codex: {
    name: 'Codex CLI',
    dir: '.agents',
    skills: 'skills',
    agents: null,
    commands: null,
    description: 'OpenAI Codex CLI',
  },
  opencode: {
    name: 'OpenCode',
    dir: '.opencode',
    skills: 'skills',
    agents: 'agents',
    commands: 'commands',
    description: 'OpenCode AI',
  },
  agents: {
    name: 'Universal (.agents)',
    dir: '.agents',
    skills: 'skills',
    agents: null,
    commands: null,
    description: 'Cross-platform .agents standard',
  },
};

/** Valid platform name array */
export const PLATFORM_NAMES = Object.keys(PLATFORMS);

/** Default platform */
export const DEFAULT_PLATFORM = 'claude';

/**
 * Get platform configuration by name.
 * @param {string} name - Platform key (e.g. 'claude', 'gemini')
 * @returns {object} Platform config object
 * @throws {Error} If the platform name is invalid
 */
export function getPlatformConfig(name) {
  const config = PLATFORMS[name];
  if (!config) {
    throw new Error(
      `Unknown platform '${name}'. Valid platforms: ${PLATFORM_NAMES.join(', ')}`
    );
  }
  return config;
}

/**
 * Compute the base installation directory for a given platform.
 * @param {string} targetPath - Project root or custom path
 * @param {string} platform  - Platform key
 * @returns {string} Absolute path to the platform directory (e.g. /project/.gemini)
 */
export function getTargetDir(targetPath, platform) {
  const config = getPlatformConfig(platform);
  return `${targetPath}/${config.dir}`;
}
