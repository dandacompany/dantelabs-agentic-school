import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { join } from 'path';
import { existsSync } from 'fs';

import { getMarketplaceConfig } from '../lib/config.js';
import { uninstallPlugin } from '../lib/installer.js';
import logger from '../utils/logger.js';
import { resolvePath } from '../utils/fs-utils.js';

export default function uninstallCommand(program) {
  program
    .command('uninstall <plugin>')
    .alias('rm')
    .description('Uninstall a plugin from your project')
    .option('-p, --path <path>', 'Project path (default: current directory)')
    .option('-y, --yes', 'Skip confirmation prompt')
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
          logger.error(`No .claude directory found at ${targetPath}`);
          process.exit(1);
        }

        // Load marketplace config to get plugin info
        spinner.start('Loading plugin registry...');
        const config = await getMarketplaceConfig();
        spinner.stop();

        // Find plugin
        const plugin = config.plugins.find((p) => p.name === pluginName);

        if (!plugin) {
          logger.error(`Plugin '${pluginName}' not found in registry`);
          console.log();
          console.log('Available plugins:');
          config.plugins.forEach((p) => {
            console.log(`  - ${chalk.cyan(p.name)}`);
          });
          process.exit(1);
        }

        // Show what will be removed
        console.log();
        console.log(chalk.bold(`Will remove ${chalk.cyan(plugin.name)}:`));
        const components = plugin.components || {};

        if (components.agents?.length) {
          console.log(
            chalk.gray(`  Agents: ${components.agents.join(', ')}`)
          );
        }
        if (components.commands?.length) {
          console.log(
            chalk.gray(`  Commands: /${components.commands.join(', /')}`)
          );
        }
        if (components.skills?.length) {
          console.log(
            chalk.gray(`  Skills: ${components.skills.join(', ')}`)
          );
        }
        console.log();

        // Confirm unless --yes
        if (!options.yes) {
          const { confirm } = await inquirer.prompt([
            {
              type: 'confirm',
              name: 'confirm',
              message: `Are you sure you want to uninstall ${plugin.name}?`,
              default: false
            }
          ]);

          if (!confirm) {
            logger.info('Uninstall cancelled');
            return;
          }
        }

        // Uninstall
        spinner.start(`Uninstalling ${chalk.cyan(plugin.name)}...`);

        const results = await uninstallPlugin(plugin, claudeDir);

        spinner.succeed(`Uninstalled ${chalk.cyan(plugin.name)}`);

        // Summary
        console.log();
        console.log(
          chalk.gray(
            `Removed: ${results.agents} agents, ${results.commands} commands, ${results.skills} skills`
          )
        );
      } catch (error) {
        spinner.fail();
        logger.error(error.message);
        process.exit(1);
      }
    });
}
