import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { existsSync } from 'fs';
import { mkdir } from 'fs/promises';
import { homedir } from 'os';
import { resolve } from 'path';

import { PLATFORMS, PLATFORM_NAMES, getPlatformConfig } from './platforms.js';
import { enrichPluginWithComponents } from './config.js';
import { detectInstalledPlugins } from './install-detector.js';
import { t } from '../i18n/index.js';

/**
 * Run the interactive installation wizard.
 *
 * @param {object} config - Marketplace config with plugins array
 * @returns {object|null} Installation plan or null if cancelled
 *   { platform, targetPath, pluginsToInstall, componentSelections, force }
 */
export async function runInteractiveInstall(config) {
  // ─── Step 1: Platform Selection ───
  const platform = await selectPlatform();
  const platformConfig = getPlatformConfig(platform);

  // ─── Step 2: Scope Selection ───
  const targetPath = await selectScope(platform, platformConfig);

  // ─── Step 3: Plugin Selection (with component enrichment) ───
  const spinner = ora();
  spinner.start(t('interactive.loadingComponents'));

  const enrichedPlugins = [];
  for (const plugin of config.plugins) {
    enrichedPlugins.push(await enrichPluginWithComponents(plugin));
  }
  spinner.succeed(t('interactive.componentsLoaded'));

  // Detect already-installed plugins
  const baseDir = resolve(targetPath, platformConfig.dir);
  let installStatus = new Map();
  if (existsSync(baseDir)) {
    installStatus = detectInstalledPlugins(enrichedPlugins, baseDir, platformConfig);
  }

  const selectedPlugins = await selectPlugins(enrichedPlugins, installStatus, config.categories);
  if (!selectedPlugins.length) return null;

  // ─── Step 4: Component Selection (optional) ───
  const componentSelections = await selectComponents(selectedPlugins, platformConfig);

  // ─── Step 5: Already-Installed Detection ───
  const installedSelected = selectedPlugins.filter(
    p => installStatus.get(p.name)?.installed
  );

  let force = false;
  let finalPlugins = [...selectedPlugins];

  if (installedSelected.length > 0) {
    const action = await handleInstalledPlugins(installedSelected);
    if (action === 'cancel') return null;
    if (action === 'skip') {
      finalPlugins = finalPlugins.filter(p => !installStatus.get(p.name)?.installed);
      if (finalPlugins.length === 0) {
        console.log(chalk.yellow(t('interactive.nothingToInstall')));
        return null;
      }
    }
    if (action === 'update') {
      force = true;
    }
  }

  // ─── Step 6: Common Dependency ───
  const hasCommon = finalPlugins.some(p => p.name === 'common');
  if (!hasCommon && finalPlugins.length > 0) {
    const commonInstalled = installStatus.get('common')?.installed;
    const commonPlugin = enrichedPlugins.find(p => p.name === 'common');

    if (commonPlugin) {
      const includeCommon = await askIncludeCommon(commonInstalled);
      if (includeCommon) {
        finalPlugins.unshift(commonPlugin);
      }
    }
  }

  // ─── Step 7: Summary + Confirm ───
  const confirmed = await showSummaryAndConfirm(
    platform, platformConfig, targetPath, finalPlugins, componentSelections, installStatus
  );

  if (!confirmed) return null;

  return {
    platform,
    targetPath,
    pluginsToInstall: finalPlugins,
    componentSelections,
    force
  };
}

// ─────────────────────────────────────────────
// Step 1: Platform Selection
// ─────────────────────────────────────────────

async function selectPlatform() {
  const choices = PLATFORM_NAMES.map(key => {
    const p = PLATFORMS[key];
    const components = [
      p.skills ? 'skills' : null,
      p.agents ? 'agents' : null,
      p.commands ? 'commands' : null
    ].filter(Boolean).join(', ');
    const globalTag = p.global ? ` ${chalk.yellow(t('interactive.global'))}` : '';
    return {
      name: `${p.name}${globalTag} ${chalk.gray(`(${components})`)}`,
      value: key,
      short: p.name
    };
  });

  const { platform } = await inquirer.prompt([{
    type: 'list',
    name: 'platform',
    message: t('interactive.selectPlatform'),
    choices,
    default: 'claude'
  }]);

  return platform;
}

// ─────────────────────────────────────────────
// Step 2: Scope Selection
// ─────────────────────────────────────────────

async function selectScope(platform, platformConfig) {
  const isGlobal = platformConfig.global;

  const choices = [
    {
      name: t('interactive.scopeProject') + ` ${chalk.gray(process.cwd())}`,
      value: 'project',
      short: 'Project'
    },
    {
      name: t('interactive.scopeGlobal') + ` ${chalk.gray(homedir())}`,
      value: 'global',
      short: 'Global'
    },
    {
      name: t('interactive.scopeCustom'),
      value: 'custom',
      short: 'Custom'
    }
  ];

  const defaultScope = isGlobal ? 'global' : 'project';

  const { scope } = await inquirer.prompt([{
    type: 'list',
    name: 'scope',
    message: t('interactive.selectScope'),
    choices,
    default: defaultScope
  }]);

  if (scope === 'project') return process.cwd();
  if (scope === 'global') return homedir();

  // Custom path
  const { customPath } = await inquirer.prompt([{
    type: 'input',
    name: 'customPath',
    message: t('interactive.enterCustomPath'),
    validate: (input) => {
      if (!input.trim()) return t('interactive.enterCustomPath');
      return true;
    }
  }]);

  const resolved = resolve(customPath);

  if (!existsSync(resolved)) {
    const { create } = await inquirer.prompt([{
      type: 'confirm',
      name: 'create',
      message: t('interactive.pathNotFound', { path: resolved }),
      default: true
    }]);
    if (create) {
      await mkdir(resolved, { recursive: true });
    }
  }

  return resolved;
}

// ─────────────────────────────────────────────
// Step 3: Plugin Selection
// ─────────────────────────────────────────────

async function selectPlugins(plugins, installStatus, categories) {
  const choices = [];

  for (const category of categories) {
    choices.push(new inquirer.Separator(`── ${category.toUpperCase()} ──`));

    const categoryPlugins = plugins.filter(p => p.category === category);
    for (const plugin of categoryPlugins) {
      const components = plugin.components || {};
      const counts = [];
      if (components.agents?.length) counts.push(`${components.agents.length} agents`);
      if (components.commands?.length) counts.push(`${components.commands.length} commands`);
      if (components.skills?.length) counts.push(`${components.skills.length} skills`);
      const countHint = counts.length ? chalk.gray(` (${counts.join(', ')})`) : '';

      const status = installStatus.get(plugin.name);
      const installedTag = status?.installed
        ? chalk.green(` [${t('interactive.installed')}]`)
        : '';

      choices.push({
        name: `${plugin.name}${installedTag}${countHint} - ${chalk.gray(plugin.description)}`,
        value: plugin.name,
        short: plugin.name
      });
    }
  }

  const { selected } = await inquirer.prompt([{
    type: 'checkbox',
    name: 'selected',
    message: t('interactive.selectPlugins'),
    choices,
    pageSize: 20,
    validate: (answer) => {
      if (answer.length === 0) return t('interactive.selectAtLeastOne');
      return true;
    }
  }]);

  return plugins.filter(p => selected.includes(p.name));
}

// ─────────────────────────────────────────────
// Step 4: Component Selection
// ─────────────────────────────────────────────

async function selectComponents(plugins, platformConfig) {
  const selections = {};

  // Check if any plugin has multiple component types
  const multiComponentPlugins = plugins.filter(p => {
    const c = p.components || {};
    let typeCount = 0;
    if (c.agents?.length && platformConfig.agents) typeCount++;
    if (c.commands?.length && platformConfig.commands) typeCount++;
    if (c.skills?.length) typeCount++;
    return typeCount > 1;
  });

  if (multiComponentPlugins.length === 0) {
    // All plugins have single component type, no need for selection
    return selections;
  }

  const { wantSelection } = await inquirer.prompt([{
    type: 'confirm',
    name: 'wantSelection',
    message: t('interactive.wantComponentSelection'),
    default: false
  }]);

  if (!wantSelection) return selections;

  for (const plugin of multiComponentPlugins) {
    const components = plugin.components || {};
    const choices = [];

    if (components.agents?.length && platformConfig.agents) {
      choices.push(new inquirer.Separator(`── Agents ──`));
      for (const agent of components.agents) {
        choices.push({
          name: `agent: ${agent}`,
          value: `agent:${agent}`,
          checked: true
        });
      }
    }

    if (components.commands?.length && platformConfig.commands) {
      choices.push(new inquirer.Separator(`── Commands ──`));
      for (const cmd of components.commands) {
        choices.push({
          name: `command: /${cmd}`,
          value: `command:${cmd}`,
          checked: true
        });
      }
    }

    if (components.skills?.length) {
      choices.push(new inquirer.Separator(`── Skills ──`));
      for (const skill of components.skills) {
        choices.push({
          name: `skill: ${skill}`,
          value: `skill:${skill}`,
          checked: true
        });
      }
    }

    const { selected } = await inquirer.prompt([{
      type: 'checkbox',
      name: 'selected',
      message: t('interactive.selectComponents', { plugin: chalk.cyan(plugin.name) }),
      choices,
      pageSize: 20
    }]);

    // Parse selections into componentFilter format
    const filter = { agents: [], commands: [], skills: [] };
    for (const item of selected) {
      const [type, name] = item.split(':');
      if (type === 'agent') filter.agents.push(name);
      if (type === 'command') filter.commands.push(name);
      if (type === 'skill') filter.skills.push(name);
    }

    selections[plugin.name] = filter;
  }

  return selections;
}

// ─────────────────────────────────────────────
// Step 5: Already-Installed Handling
// ─────────────────────────────────────────────

async function handleInstalledPlugins(installedPlugins) {
  console.log();
  console.log(chalk.yellow(t('interactive.alreadyInstalledWarning')));
  for (const p of installedPlugins) {
    console.log(`  - ${chalk.cyan(p.name)}`);
  }
  console.log();

  const { action } = await inquirer.prompt([{
    type: 'list',
    name: 'action',
    message: t('interactive.updateAction'),
    choices: [
      { name: t('interactive.updateAll'), value: 'update' },
      { name: t('interactive.skipInstalled'), value: 'skip' },
      { name: t('interactive.cancelInstall'), value: 'cancel' }
    ]
  }]);

  return action;
}

// ─────────────────────────────────────────────
// Step 6: Common Dependency
// ─────────────────────────────────────────────

async function askIncludeCommon(commonAlreadyInstalled) {
  const hint = commonAlreadyInstalled
    ? chalk.gray(` (${t('interactive.commonAlreadyInstalled')})`)
    : '';

  const { include } = await inquirer.prompt([{
    type: 'confirm',
    name: 'include',
    message: t('interactive.includeCommon') + hint,
    default: !commonAlreadyInstalled
  }]);

  return include;
}

// ─────────────────────────────────────────────
// Step 7: Summary + Confirm
// ─────────────────────────────────────────────

async function showSummaryAndConfirm(
  platform, platformConfig, targetPath, plugins, componentSelections, installStatus
) {
  const baseDir = resolve(targetPath, platformConfig.dir);

  console.log();
  console.log(chalk.bold(`━━━ ${t('interactive.summaryTitle')} ━━━`));
  console.log(`  ${t('interactive.summaryPlatform')}: ${chalk.cyan(platformConfig.name)}`);
  console.log(`  ${t('interactive.summaryTarget')}: ${chalk.cyan(baseDir)}`);
  console.log(`  ${t('interactive.summaryPluginCount', { count: plugins.length })}`);
  console.log();

  for (const plugin of plugins) {
    const status = installStatus.get(plugin.name);
    const updateTag = status?.installed
      ? chalk.yellow(` [${t('interactive.update')}]`)
      : '';

    console.log(`  ${chalk.bold.cyan(plugin.name)}${updateTag}`);

    const components = plugin.components || {};
    const filter = componentSelections[plugin.name];

    // Show agents
    if (components.agents?.length && platformConfig.agents) {
      const agentList = filter ? filter.agents : components.agents;
      if (agentList.length > 0) {
        console.log(chalk.gray(`    agents: ${agentList.join(', ')}`));
      }
    }

    // Show commands
    if (components.commands?.length && platformConfig.commands) {
      const cmdList = filter ? filter.commands : components.commands;
      if (cmdList.length > 0) {
        console.log(chalk.gray(`    commands: /${cmdList.join(', /')}`));
      }
    }

    // Show skills
    if (components.skills?.length) {
      const skillList = filter ? filter.skills : components.skills;
      if (skillList.length > 0) {
        console.log(chalk.gray(`    skills: ${skillList.join(', ')}`));
      }
    }
  }

  console.log(chalk.bold(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`));
  console.log();

  const { confirm } = await inquirer.prompt([{
    type: 'confirm',
    name: 'confirm',
    message: t('interactive.confirmProceed'),
    default: true
  }]);

  return confirm;
}
