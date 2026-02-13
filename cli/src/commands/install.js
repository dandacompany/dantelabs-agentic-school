import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { resolve, join } from 'path';
import { existsSync } from 'fs';
import { mkdir } from 'fs/promises';

import { getMarketplaceConfig, getPluginDependencies } from '../lib/config.js';
import { installPlugin } from '../lib/installer.js';
import { getPlatformConfig, getDefaultTargetPath, PLATFORM_NAMES, DEFAULT_PLATFORM } from '../lib/platforms.js';
import { runInteractiveInstall } from '../lib/interactive-installer.js';
import logger from '../utils/logger.js';
import { resolvePath } from '../utils/fs-utils.js';
import { t } from '../i18n/index.js';

export default function installCommand(program) {
  program
    .command('install [plugin]')
    .alias('i')
    .description(t('install.description'))
    .option('-p, --path <path>', t('install.optionPath'))
    .option('-t, --target <platform>', t('install.optionTarget'), DEFAULT_PLATFORM)
    .option('-f, --force', t('install.optionForce'))
    .option('--all', t('install.optionAll'))
    .option('--common', t('install.optionCommon'))
    .option('--dry-run', t('install.optionDryRun'))
    .action(async (pluginName, options) => {
      const spinner = ora();

      try {
        // Validate platform
        const platform = options.target;
        if (!PLATFORM_NAMES.includes(platform)) {
          logger.error(
            t('install.invalidPlatform', {
              name: platform,
              valid: PLATFORM_NAMES.join(', ')
            })
          );
          process.exit(1);
        }

        const platformConfig = getPlatformConfig(platform);

        // Determine installation path (global platforms default to $HOME)
        const targetPath = options.path
          ? resolvePath(options.path)
          : getDefaultTargetPath(platform);
        const baseDir = join(targetPath, platformConfig.dir);

        // Show platform info for non-default platforms
        if (platform !== DEFAULT_PLATFORM) {
          logger.info(
            t('install.platformInfo', {
              name: platformConfig.name,
              description: platformConfig.description
            })
          );
        }
        logger.info(`${t('install.installTarget')}: ${chalk.cyan(baseDir)}`);

        // Load marketplace config
        spinner.start(t('install.loadingRegistry'));
        const config = await getMarketplaceConfig();
        spinner.succeed(t('install.registryLoaded'));

        // Determine which plugins to install
        let pluginsToInstall = [];
        let interactiveResult = null;

        if (!pluginName && !options.all) {
          // ─── Interactive mode: no plugin name, no --all flag ───
          interactiveResult = await runInteractiveInstall(config);

          if (!interactiveResult) {
            logger.info(t('install.installCancelled'));
            return;
          }

          pluginsToInstall = interactiveResult.pluginsToInstall;

          // Override platform and path from interactive selections
          const effectivePlatform = interactiveResult.platform;
          const effectivePlatformConfig = getPlatformConfig(effectivePlatform);
          const effectiveBaseDir = join(interactiveResult.targetPath, effectivePlatformConfig.dir);

          if (interactiveResult.force) {
            options.force = true;
          }

          // Create base directory
          if (!existsSync(effectiveBaseDir)) {
            await mkdir(effectiveBaseDir, { recursive: true });
          }

          // Install each plugin with interactive selections
          let totalAgents = 0;
          let totalCommands = 0;
          let totalSkills = 0;
          let totalSkippedAgents = 0;
          let totalSkippedCommands = 0;

          for (const plugin of pluginsToInstall) {
            spinner.start(t('install.installing', { name: chalk.cyan(plugin.name) }));

            try {
              const componentFilter = interactiveResult.componentSelections[plugin.name] || null;

              const results = await installPlugin(plugin, effectiveBaseDir, {
                force: options.force,
                platform: effectivePlatform,
                componentFilter,
                onProgress: (type, name) => {
                  spinner.text = t('install.installingComponent', {
                    plugin: chalk.cyan(plugin.name),
                    type,
                    name
                  });
                }
              });

              totalAgents += results.agents;
              totalCommands += results.commands;
              totalSkills += results.skills;
              totalSkippedAgents += results.skippedAgents;
              totalSkippedCommands += results.skippedCommands;

              spinner.succeed(t('install.installed', { name: chalk.cyan(plugin.name) }));
            } catch (err) {
              spinner.fail(
                t('install.failedToInstall', {
                  name: plugin.name,
                  error: err.message
                })
              );
              if (!options.force) throw err;
            }
          }

          // Summary
          console.log();
          logger.success(
            t('install.successMessage', { count: pluginsToInstall.length })
          );
          console.log(
            chalk.gray(
              `  ${t('install.componentSummary', {
                agents: totalAgents,
                commands: totalCommands,
                skills: totalSkills
              })}`
            )
          );

          if (totalSkippedAgents > 0 || totalSkippedCommands > 0) {
            console.log(
              chalk.yellow(
                `  ${t('install.skippedComponents', {
                  agents: totalSkippedAgents,
                  commands: totalSkippedCommands,
                  platform: effectivePlatformConfig.name
                })}`
              )
            );
          }

          console.log();
          console.log(`${t('common.location')}: ${chalk.cyan(effectiveBaseDir)}`);
          return;
        } else if (options.all) {
          // Install all plugins (existing behavior)
          const { confirm } = await inquirer.prompt([
            {
              type: 'confirm',
              name: 'confirm',
              message: t('install.confirmInstallAll', {
                count: config.plugins.length
              }),
              default: true
            }
          ]);

          if (!confirm) {
            logger.info(t('install.installCancelled'));
            return;
          }

          pluginsToInstall = [...config.plugins];
        } else {
          // Find specific plugin
          const plugin = config.plugins.find((p) => p.name === pluginName);

          if (!plugin) {
            logger.error(t('install.pluginNotFound', { name: pluginName }));
            console.log();
            console.log(`${t('common.availablePlugins')}:`);
            config.plugins.forEach((p) => {
              console.log(`  - ${chalk.cyan(p.name)}: ${p.description}`);
            });
            process.exit(1);
          }

          pluginsToInstall = [plugin];

          // Add common dependency only when explicitly requested with --common
          if (options.common === true && pluginName !== 'common') {
            const deps = getPluginDependencies(pluginName, config);
            pluginsToInstall = [...deps, ...pluginsToInstall];
          }
        }

        // Remove duplicates
        pluginsToInstall = pluginsToInstall.filter(
          (plugin, index, self) =>
            index === self.findIndex((p) => p.name === plugin.name)
        );

        // Dry run mode
        if (options.dryRun) {
          console.log();
          logger.info(t('install.dryRunTitle'));
          console.log();

          for (const plugin of pluginsToInstall) {
            console.log(chalk.bold.cyan(`  ${plugin.name}`));
            const components = plugin.components || {};

            if (components.agents?.length) {
              if (platformConfig.agents) {
                console.log(
                  chalk.gray(
                    `    ${t('common.agents')}: ${components.agents.join(', ')}`
                  )
                );
              } else {
                console.log(
                  chalk.yellow(
                    `    ${t('common.agents')}: ${t('install.platformNotSupported', { platform: platformConfig.name, component: t('common.agents') })}`
                  )
                );
              }
            }
            if (components.commands?.length) {
              if (platformConfig.commands) {
                console.log(
                  chalk.gray(
                    `    ${t('common.commands')}: /${components.commands.join(', /')}`
                  )
                );
              } else {
                console.log(
                  chalk.yellow(
                    `    ${t('common.commands')}: ${t('install.platformNotSupported', { platform: platformConfig.name, component: t('common.commands') })}`
                  )
                );
              }
            }
            if (components.skills?.length) {
              console.log(
                chalk.gray(
                  `    ${t('common.skills')}: ${components.skills.join(', ')}`
                )
              );
            }
            console.log();
          }

          console.log(chalk.gray(t('install.dryRunFooter')));
          return;
        }

        // Create base directory
        if (!existsSync(baseDir)) {
          await mkdir(baseDir, { recursive: true });
        }

        // Install each plugin
        let totalAgents = 0;
        let totalCommands = 0;
        let totalSkills = 0;
        let totalSkippedAgents = 0;
        let totalSkippedCommands = 0;

        for (const plugin of pluginsToInstall) {
          spinner.start(t('install.installing', { name: chalk.cyan(plugin.name) }));

          try {
            const results = await installPlugin(plugin, baseDir, {
              force: options.force,
              platform,
              onProgress: (type, name) => {
                spinner.text = t('install.installingComponent', {
                  plugin: chalk.cyan(plugin.name),
                  type,
                  name
                });
              }
            });

            totalAgents += results.agents;
            totalCommands += results.commands;
            totalSkills += results.skills;
            totalSkippedAgents += results.skippedAgents;
            totalSkippedCommands += results.skippedCommands;

            spinner.succeed(t('install.installed', { name: chalk.cyan(plugin.name) }));
          } catch (err) {
            spinner.fail(
              t('install.failedToInstall', {
                name: plugin.name,
                error: err.message
              })
            );
            if (!options.force) {
              throw err;
            }
          }
        }

        // Summary
        console.log();
        logger.success(
          t('install.successMessage', { count: pluginsToInstall.length })
        );
        console.log(
          chalk.gray(
            `  ${t('install.componentSummary', {
              agents: totalAgents,
              commands: totalCommands,
              skills: totalSkills
            })}`
          )
        );

        // Show skipped components warning
        if (totalSkippedAgents > 0 || totalSkippedCommands > 0) {
          console.log(
            chalk.yellow(
              `  ${t('install.skippedComponents', {
                agents: totalSkippedAgents,
                commands: totalSkippedCommands,
                platform: platformConfig.name
              })}`
            )
          );
        }

        console.log();
        console.log(`${t('common.location')}: ${chalk.cyan(baseDir)}`);

        // Show next steps
        console.log();
        console.log(chalk.bold(`${t('install.nextSteps')}:`));

        // Platform-specific next step hint
        const cliCommands = {
          claude: 'claude --help',
          gemini: 'gemini',
          antigravity: 'antigravity',
          codex: 'codex --help',
          opencode: 'opencode --help',
          openclaw: 'openclaw --help',
          agents: 'claude --help',
        };
        const hintCmd = cliCommands[platform] || 'claude --help';
        console.log(
          `  1. ${t('install.nextStep1', { command: chalk.cyan(hintCmd) })}`
        );

        // Show example command based on installed plugins
        const hasAnalyzeBrand = pluginsToInstall.some(
          (p) => p.components?.commands?.includes('analyze-brand')
        );
        if (hasAnalyzeBrand && platformConfig.commands) {
          console.log(
            `  2. ${t('install.nextStep2', {
              command: chalk.cyan('/analyze-brand --brand-doc ./your-brand.md')
            })}`
          );
        }

        // Show external skill requirements
        const externalSkills = pluginsToInstall
          .filter((p) => p.externalSkills?.length)
          .flatMap((p) => p.externalSkills);

        if (externalSkills.length > 0) {
          console.log();
          console.log(chalk.yellow(`${t('install.externalSkillsRequired')}:`));
          [...new Set(externalSkills)].forEach((skill) => {
            console.log(`  - ${skill}`);
          });
        }
      } catch (error) {
        spinner.fail();
        logger.error(error.message);
        process.exit(1);
      }
    });
}
