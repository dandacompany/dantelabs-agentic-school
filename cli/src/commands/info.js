import chalk from 'chalk';
import { getMarketplaceConfig } from '../lib/config.js';
import logger from '../utils/logger.js';
import { t } from '../i18n/index.js';

export default function infoCommand(program) {
  program
    .command('info <plugin>')
    .description(t('info.description'))
    .option('--json', t('info.optionJson'))
    .action(async (pluginName, options) => {
      try {
        const config = await getMarketplaceConfig();
        const plugin = config.plugins.find((p) => p.name === pluginName);

        if (!plugin) {
          logger.error(t('info.pluginNotFound', { name: pluginName }));
          console.log();
          console.log(`${t('common.availablePlugins')}:`);
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
          console.log(chalk.bold(`${t('info.agents')}:`));
          components.agents.forEach((a) => console.log(`  - ${a}`));
          console.log();
        }

        if (components.commands?.length) {
          console.log(chalk.bold(`${t('info.commands')}:`));
          components.commands.forEach((c) => console.log(`  - /${c}`));
          console.log();
        }

        if (components.skills?.length) {
          console.log(chalk.bold(`${t('info.skills')}:`));
          components.skills.forEach((s) => console.log(`  - ${s}`));
          console.log();
        }

        if (plugin.externalSkills?.length) {
          console.log(chalk.bold.yellow(`${t('info.externalSkillsRequired')}:`));
          plugin.externalSkills.forEach((s) => console.log(`  - ${s}`));
          console.log();
        }

        console.log(
          chalk.gray(`${t('info.installHint')}:`),
          `npx dantelabs-agentic-school install ${pluginName}`
        );
      } catch (error) {
        logger.error(error.message);
        process.exit(1);
      }
    });
}
