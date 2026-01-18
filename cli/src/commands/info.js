import chalk from 'chalk';
import { getMarketplaceConfig } from '../lib/config.js';
import logger from '../utils/logger.js';

export default function infoCommand(program) {
  program
    .command('info <plugin>')
    .description('Show detailed information about a plugin')
    .option('--json', 'Output as JSON')
    .action(async (pluginName, options) => {
      try {
        const config = await getMarketplaceConfig();
        const plugin = config.plugins.find((p) => p.name === pluginName);

        if (!plugin) {
          logger.error(`Plugin '${pluginName}' not found`);
          console.log();
          console.log('Available plugins:');
          config.plugins.forEach((p) => {
            console.log(`  - ${chalk.cyan(p.name)}`);
          });
          process.exit(1);
        }

        if (options.json) {
          console.log(JSON.stringify(plugin, null, 2));
          return;
        }

        console.log();
        console.log(
          chalk.bold.blue(plugin.name),
          chalk.gray(`v${plugin.version}`)
        );
        console.log(chalk.gray('━'.repeat(50)));
        console.log();
        console.log(plugin.description);
        console.log();

        const components = plugin.components || {};

        if (components.agents?.length) {
          console.log(chalk.bold('Agents:'));
          components.agents.forEach((a) => console.log(`  - ${a}`));
          console.log();
        }

        if (components.commands?.length) {
          console.log(chalk.bold('Commands:'));
          components.commands.forEach((c) => console.log(`  - /${c}`));
          console.log();
        }

        if (components.skills?.length) {
          console.log(chalk.bold('Skills:'));
          components.skills.forEach((s) => console.log(`  - ${s}`));
          console.log();
        }

        if (plugin.externalSkills?.length) {
          console.log(chalk.bold.yellow('External Skills Required:'));
          plugin.externalSkills.forEach((s) => console.log(`  - ${s}`));
          console.log();
        }

        console.log(
          chalk.gray('Install:'),
          `npx dantelabs-agentic-school install ${pluginName}`
        );
      } catch (error) {
        logger.error(error.message);
        process.exit(1);
      }
    });
}
