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

export default function installCommand(program) {
  program
    .command('install [plugin]')
    .alias('i')
    .description('Install plugins to your project')
    .option('-p, --path <path>', 'Installation path (default: current directory)')
    .option('-f, --force', 'Force overwrite existing files')
    .option('--all', 'Install all available plugins')
    .option('--no-common', 'Skip common utilities')
    .option('--dry-run', 'Show what would be installed without making changes')
    .action(async (pluginName, options) => {
      const spinner = ora();

      try {
        // Determine installation path
        const targetPath = options.path
          ? resolvePath(options.path)
          : process.cwd();
        const claudeDir = join(targetPath, '.claude');

        logger.info(`Installation target: ${chalk.cyan(claudeDir)}`);

        // Load marketplace config
        spinner.start('Loading plugin registry...');
        const config = await getMarketplaceConfig();
        spinner.succeed('Plugin registry loaded');

        // Determine which plugins to install
        let pluginsToInstall = [];

        if (options.all || !pluginName) {
          // Install all plugins
          const { confirm } = await inquirer.prompt([
            {
              type: 'confirm',
              name: 'confirm',
              message: `Install all ${config.plugins.length} plugins?`,
              default: true
            }
          ]);

          if (!confirm) {
            logger.info('Installation cancelled');
            return;
          }

          pluginsToInstall = [...config.plugins];
        } else {
          // Find specific plugin
          const plugin = config.plugins.find((p) => p.name === pluginName);

          if (!plugin) {
            logger.error(`Plugin '${pluginName}' not found`);
            console.log();
            console.log('Available plugins:');
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
          logger.info('Dry run - would install:');
          console.log();

          for (const plugin of pluginsToInstall) {
            console.log(chalk.bold.cyan(`  ${plugin.name}`));
            const components = plugin.components || {};

            if (components.agents?.length) {
              console.log(
                chalk.gray(`    Agents: ${components.agents.join(', ')}`)
              );
            }
            if (components.commands?.length) {
              console.log(
                chalk.gray(`    Commands: /${components.commands.join(', /')}`)
              );
            }
            if (components.skills?.length) {
              console.log(
                chalk.gray(`    Skills: ${components.skills.join(', ')}`)
              );
            }
            console.log();
          }

          console.log(chalk.gray('Run without --dry-run to install.'));
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
          spinner.start(`Installing ${chalk.cyan(plugin.name)}...`);

          try {
            const results = await installPlugin(plugin, claudeDir, {
              force: options.force,
              onProgress: (type, name) => {
                spinner.text = `Installing ${chalk.cyan(plugin.name)}: ${type} ${name}`;
              }
            });

            totalAgents += results.agents;
            totalCommands += results.commands;
            totalSkills += results.skills;

            spinner.succeed(`Installed ${chalk.cyan(plugin.name)}`);
          } catch (err) {
            spinner.fail(`Failed to install ${plugin.name}: ${err.message}`);
            if (!options.force) {
              throw err;
            }
          }
        }

        // Summary
        console.log();
        logger.success(
          `Successfully installed ${pluginsToInstall.length} plugin(s)`
        );
        console.log(
          chalk.gray(
            `  ${totalAgents} agents, ${totalCommands} commands, ${totalSkills} skills`
          )
        );
        console.log();
        console.log(`Location: ${chalk.cyan(claudeDir)}`);

        // Show next steps
        console.log();
        console.log(chalk.bold('Next steps:'));
        console.log(
          `  1. Run ${chalk.cyan('claude --help')} to see available commands`
        );

        // Show example command based on installed plugins
        const hasAnalyzeBrand = pluginsToInstall.some(
          (p) => p.components?.commands?.includes('analyze-brand')
        );
        if (hasAnalyzeBrand) {
          console.log(
            `  2. Try ${chalk.cyan('/analyze-brand --brand-doc ./your-brand.md')}`
          );
        }

        // Show external skill requirements
        const externalSkills = pluginsToInstall
          .filter((p) => p.externalSkills?.length)
          .flatMap((p) => p.externalSkills);

        if (externalSkills.length > 0) {
          console.log();
          console.log(chalk.yellow('External skills required:'));
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
