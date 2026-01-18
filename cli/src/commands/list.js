import chalk from 'chalk';
import { getMarketplaceConfig } from '../lib/config.js';
import logger from '../utils/logger.js';
import { t } from '../i18n/index.js';

export default function listCommand(program) {
  program
    .command('list')
    .alias('ls')
    .description(t('list.description'))
    .option('--json', t('list.optionJson'))
    .option('-v, --verbose', t('list.optionVerbose'))
    .action(async (options) => {
      try {
        const config = await getMarketplaceConfig();

        if (options.json) {
          console.log(JSON.stringify(config.plugins, null, 2));
          return;
        }

        console.log();
        console.log(chalk.bold.blue(t('list.title')));
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
            if (plugin.externalSkills?.length) {
              console.log(
                chalk.yellow(`  ${t('common.external')}: ${plugin.externalSkills.join(', ')}`)
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
          chalk.bold(`${t('common.summary')}:`),
          t('list.summaryText', {
            plugins: config.plugins.length,
            agents: totalAgents,
            commands: totalCommands,
            skills: totalSkills
          })
        );
        console.log();
        console.log(chalk.gray(t('list.installHint')));
      } catch (error) {
        logger.error(error.message);
        process.exit(1);
      }
    });
}
