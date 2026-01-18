import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { join } from 'path';
import { existsSync } from 'fs';

import { getMarketplaceConfig } from '../lib/config.js';
import { uninstallPlugin } from '../lib/installer.js';
import logger from '../utils/logger.js';
import { resolvePath } from '../utils/fs-utils.js';
import { t } from '../i18n/index.js';

export default function uninstallCommand(program) {
  program
    .command('uninstall <plugin>')
    .alias('rm')
    .description(t('uninstall.description'))
    .option('-p, --path <path>', t('uninstall.optionPath'))
    .option('-y, --yes', t('uninstall.optionYes'))
    .action(async (pluginName, options) => {
      const spinner = ora();

      try {
        // Determine path
        const targetPath = options.path
          ? resolvePath(options.path)
          : process.cwd();
        const claudeDir = join(targetPath, '.claude');

        // Check if .claude directory exists
        if (!existsSync(claudeDir)) {
          logger.error(t('uninstall.noClaudeDir', { path: targetPath }));
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
          console.log(
            chalk.gray(`  ${t('common.agents')}: ${components.agents.join(', ')}`)
          );
        }
        if (components.commands?.length) {
          console.log(
            chalk.gray(`  ${t('common.commands')}: /${components.commands.join(', /')}`)
          );
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

        const results = await uninstallPlugin(plugin, claudeDir);

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
      } catch (error) {
        spinner.fail();
        logger.error(error.message);
        process.exit(1);
      }
    });
}
