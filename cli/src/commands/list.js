import chalk from 'chalk';
import { getMarketplaceConfig } from '../lib/config.js';
import logger from '../utils/logger.js';

export default function listCommand(program) {
  program
    .command('list')
    .alias('ls')
    .description('List all available plugins')
    .option('--json', 'Output as JSON')
    .option('-v, --verbose', 'Show detailed information')
    .action(async (options) => {
      try {
        const config = await getMarketplaceConfig();

        if (options.json) {
          console.log(JSON.stringify(config.plugins, null, 2));
          return;
        }

        console.log();
        console.log(chalk.bold.blue('Dante Labs Agentic School - Available Plugins'));
        console.log(chalk.gray('━'.repeat(60)));
        console.log();

        for (const plugin of config.plugins) {
          console.log(
            chalk.bold.cyan(`${plugin.name}`),
            chalk.gray(`v${plugin.version}`)
          );
          console.log(`  ${plugin.description}`);

          if (options.verbose) {
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
            if (plugin.externalSkills?.length) {
              console.log(
                chalk.yellow(`  External: ${plugin.externalSkills.join(', ')}`)
              );
            }
          }

          console.log();
        }

        // Summary
        const totalAgents = config.plugins.reduce(
          (sum, p) => sum + (p.components?.agents?.length || 0),
          0
        );
        const totalCommands = config.plugins.reduce(
          (sum, p) => sum + (p.components?.commands?.length || 0),
          0
        );
        const totalSkills = config.plugins.reduce(
          (sum, p) => sum + (p.components?.skills?.length || 0),
          0
        );

        console.log(chalk.gray('━'.repeat(60)));
        console.log(
          chalk.bold('Summary:'),
          `${config.plugins.length} plugins,`,
          `${totalAgents} agents,`,
          `${totalCommands} commands,`,
          `${totalSkills} skills`
        );
        console.log();
        console.log(
          chalk.gray(`Install: npx dantelabs-agentic-school install [plugin-name]`)
        );
      } catch (error) {
        logger.error(error.message);
        process.exit(1);
      }
    });
}
