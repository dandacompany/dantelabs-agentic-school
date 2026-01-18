import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { resolve, join } from 'path';
import { existsSync } from 'fs';
import { mkdir } from 'fs/promises';

import { getMarketplaceConfig, getPluginDependencies } from '../lib/config.js';
import { installPlugin } from '../lib/installer.js';
import logger from '../utils/logger.js';
import { resolvePath } from '../utils/fs-utils.js';
import { t } from '../i18n/index.js';

export default function installCommand(program) {
  program
    .command('install [plugin]')
    .alias('i')
    .description(t('install.description'))
    .option('-p, --path <path>', t('install.optionPath'))
    .option('-f, --force', t('install.optionForce'))
    .option('--all', t('install.optionAll'))
    .option('--no-common', t('install.optionNoCommon'))
    .option('--dry-run', t('install.optionDryRun'))
    .action(async (pluginName, options) => {
      const spinner = ora();

      try {
        // Determine installation path
        const targetPath = options.path
          ? resolvePath(options.path)
          : process.cwd();
        const claudeDir = join(targetPath, '.claude');

        logger.info(`${t('install.installTarget')}: ${chalk.cyan(claudeDir)}`);

        // Load marketplace config
        spinner.start(t('install.loadingRegistry'));
        const config = await getMarketplaceConfig();
        spinner.succeed(t('install.registryLoaded'));

        // Determine which plugins to install
        let pluginsToInstall = [];

        if (options.all || !pluginName) {
          // Install all plugins
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

          // Add common dependency if needed
          if (options.common !== false && pluginName !== 'common') {
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
              console.log(
                chalk.gray(
                  `    ${t('common.agents')}: ${components.agents.join(', ')}`
                )
              );
            }
            if (components.commands?.length) {
              console.log(
                chalk.gray(
                  `    ${t('common.commands')}: /${components.commands.join(', /')}`
                )
              );
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

        // Create .claude directory
        if (!existsSync(claudeDir)) {
          await mkdir(claudeDir, { recursive: true });
        }

        // Install each plugin
        let totalAgents = 0;
        let totalCommands = 0;
        let totalSkills = 0;

        for (const plugin of pluginsToInstall) {
          spinner.start(t('install.installing', { name: chalk.cyan(plugin.name) }));

          try {
            const results = await installPlugin(plugin, claudeDir, {
              force: options.force,
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
        console.log();
        console.log(`${t('common.location')}: ${chalk.cyan(claudeDir)}`);

        // Show next steps
        console.log();
        console.log(chalk.bold(`${t('install.nextSteps')}:`));
        console.log(
          `  1. ${t('install.nextStep1', { command: chalk.cyan('claude --help') })}`
        );

        // Show example command based on installed plugins
        const hasAnalyzeBrand = pluginsToInstall.some(
          (p) => p.components?.commands?.includes('analyze-brand')
        );
        if (hasAnalyzeBrand) {
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
