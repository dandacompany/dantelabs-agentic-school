import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { join } from 'path';
import { existsSync } from 'fs';

import { getMarketplaceConfig } from '../lib/config.js';
import { uninstallPlugin } from '../lib/installer.js';
import { getPlatformConfig, PLATFORM_NAMES, DEFAULT_PLATFORM } from '../lib/platforms.js';
import logger from '../utils/logger.js';
import { resolvePath } from '../utils/fs-utils.js';
import { t } from '../i18n/index.js';

export default function uninstallCommand(program) {
  program
    .command('uninstall <plugin>')
    .alias('rm')
    .description(t('uninstall.description'))
    .option('-p, --path <path>', t('uninstall.optionPath'))
    .option('-t, --target <platform>', t('uninstall.optionTarget'), DEFAULT_PLATFORM)
    .option('-y, --yes', t('uninstall.optionYes'))
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

        // Determine path
        const targetPath = options.path
          ? resolvePath(options.path)
          : process.cwd();
        const baseDir = join(targetPath, platformConfig.dir);

        // Check if target directory exists
        if (!existsSync(baseDir)) {
          logger.error(
            t('uninstall.noTargetDir', { dir: platformConfig.dir, path: targetPath })
          );
          process.exit(1);
        }

        // Load marketplace config to get plugin info
        spinner.start(t('uninstall.loadingRegistry'));
        const config = await getMarketplaceConfig();
        spinner.stop();

        // Find plugin
        const plugin = config.plugins.find((p) => p.name === pluginName);

        if (!plugin) {
          logger.error(t('uninstall.pluginNotFound', { name: pluginName }));
          console.log();
          console.log(`${t('common.availablePlugins')}:`);
          config.plugins.forEach((p) => {
            console.log(`  - ${chalk.cyan(p.name)}`);
          });
          process.exit(1);
        }

        // Show what will be removed
        console.log();
        console.log(
          chalk.bold(t('uninstall.willRemove', { name: chalk.cyan(plugin.name) }))
        );
        const components = plugin.components || {};

        if (components.agents?.length) {
          if (platformConfig.agents) {
            console.log(
              chalk.gray(`  ${t('common.agents')}: ${components.agents.join(', ')}`)
            );
          } else {
            console.log(
              chalk.yellow(
                `  ${t('common.agents')}: ${t('install.platformNotSupported', { platform: platformConfig.name, component: t('common.agents') })}`
              )
            );
          }
        }
        if (components.commands?.length) {
          if (platformConfig.commands) {
            console.log(
              chalk.gray(`  ${t('common.commands')}: /${components.commands.join(', /')}`)
            );
          } else {
            console.log(
              chalk.yellow(
                `  ${t('common.commands')}: ${t('install.platformNotSupported', { platform: platformConfig.name, component: t('common.commands') })}`
              )
            );
          }
        }
        if (components.skills?.length) {
          console.log(
            chalk.gray(`  ${t('common.skills')}: ${components.skills.join(', ')}`)
          );
        }
        console.log();

        // Confirm unless --yes
        if (!options.yes) {
          const { confirm } = await inquirer.prompt([
            {
              type: 'confirm',
              name: 'confirm',
              message: t('uninstall.confirmUninstall', { name: plugin.name }),
              default: false
            }
          ]);

          if (!confirm) {
            logger.info(t('uninstall.uninstallCancelled'));
            return;
          }
        }

        // Uninstall
        spinner.start(t('uninstall.uninstalling', { name: chalk.cyan(plugin.name) }));

        const results = await uninstallPlugin(plugin, baseDir, { platform });

        spinner.succeed(t('uninstall.uninstalled', { name: chalk.cyan(plugin.name) }));

        // Summary
        console.log();
        console.log(
          chalk.gray(
            t('uninstall.removedSummary', {
              agents: results.agents,
              commands: results.commands,
              skills: results.skills
            })
          )
        );

        // Show skipped info
        if (results.skippedAgents > 0 || results.skippedCommands > 0) {
          console.log(
            chalk.yellow(
              `  ${t('install.skippedComponents', {
                agents: results.skippedAgents,
                commands: results.skippedCommands,
                platform: platformConfig.name
              })}`
            )
          );
        }
      } catch (error) {
        spinner.fail();
        logger.error(error.message);
        process.exit(1);
      }
    });
}
