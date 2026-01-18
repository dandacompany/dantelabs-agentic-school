/**
 * English translations (default)
 */
export default {
  // Common
  common: {
    plugins: 'plugins',
    agents: 'agents',
    commands: 'commands',
    skills: 'skills',
    version: 'version',
    install: 'Install',
    summary: 'Summary',
    location: 'Location',
    external: 'External',
    availablePlugins: 'Available plugins',
    yes: 'yes',
    no: 'no'
  },

  // CLI descriptions
  cli: {
    description: 'Dante Labs Agentic School - Claude Code Plugin Installer',
    examples: 'Examples',
    moreInfo: 'More info',
    installAllPlugins: '# Install all plugins',
    installSpecificPlugin: '# Install specific plugin',
    installCustomPath: '# Install to custom path',
    listPlugins: '# List available plugins',
    showPluginInfo: '# Show plugin info'
  },

  // Install command
  install: {
    description: 'Install plugins to your project',
    optionPath: 'Installation path (default: current directory)',
    optionForce: 'Force overwrite existing files',
    optionAll: 'Install all available plugins',
    optionNoCommon: 'Skip common utilities',
    optionDryRun: 'Show what would be installed without making changes',
    installTarget: 'Installation target',
    loadingRegistry: 'Loading plugin registry...',
    registryLoaded: 'Plugin registry loaded',
    confirmInstallAll: 'Install all {count} plugins?',
    installCancelled: 'Installation cancelled',
    pluginNotFound: "Plugin '{name}' not found",
    dryRunTitle: 'Dry run - would install:',
    dryRunFooter: 'Run without --dry-run to install.',
    installing: 'Installing {name}...',
    installingComponent: 'Installing {plugin}: {type} {name}',
    installed: 'Installed {name}',
    failedToInstall: 'Failed to install {name}: {error}',
    successMessage: 'Successfully installed {count} plugin(s)',
    componentSummary: '{agents} agents, {commands} commands, {skills} skills',
    nextSteps: 'Next steps',
    nextStep1: 'Run {command} to see available commands',
    nextStep2: 'Try {command}',
    externalSkillsRequired: 'External skills required'
  },

  // List command
  list: {
    description: 'List all available plugins',
    optionJson: 'Output as JSON',
    optionVerbose: 'Show detailed information',
    title: 'Dante Labs Agentic School - Available Plugins',
    summaryText: '{plugins} plugins, {agents} agents, {commands} commands, {skills} skills',
    installHint: 'Install: npx dantelabs-agentic-school install [plugin-name]'
  },

  // Info command
  info: {
    description: 'Show detailed information about a plugin',
    optionJson: 'Output as JSON',
    pluginNotFound: "Plugin '{name}' not found",
    agents: 'Agents',
    commands: 'Commands',
    skills: 'Skills',
    externalSkillsRequired: 'External Skills Required',
    installHint: 'Install'
  },

  // Uninstall command
  uninstall: {
    description: 'Uninstall a plugin from your project',
    optionPath: 'Project path (default: current directory)',
    optionYes: 'Skip confirmation prompt',
    noClaudeDir: 'No .claude directory found at {path}',
    loadingRegistry: 'Loading plugin registry...',
    pluginNotFound: "Plugin '{name}' not found in registry",
    willRemove: 'Will remove {name}:',
    confirmUninstall: 'Are you sure you want to uninstall {name}?',
    uninstallCancelled: 'Uninstall cancelled',
    uninstalling: 'Uninstalling {name}...',
    uninstalled: 'Uninstalled {name}',
    removedSummary: 'Removed: {agents} agents, {commands} commands, {skills} skills'
  },

  // Logger
  logger: {
    info: 'info',
    success: 'success',
    warn: 'warn',
    error: 'error',
    debug: 'debug'
  }
};
