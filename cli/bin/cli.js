#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync } from 'fs';

import { setLocale, t, getAvailableLocales } from '../src/i18n/index.js';
import installCommand from '../src/commands/install.js';
import listCommand from '../src/commands/list.js';
import infoCommand from '../src/commands/info.js';
import uninstallCommand from '../src/commands/uninstall.js';
import sampleCommand from '../src/commands/sample.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Read version from package.json
const pkg = JSON.parse(
  readFileSync(join(__dirname, '../../package.json'), 'utf8')
);

// Pre-parse --lang option before commander
const langIndex = process.argv.findIndex(
  (arg) => arg === '--lang' || arg === '-l'
);
if (langIndex !== -1 && process.argv[langIndex + 1]) {
  setLocale(process.argv[langIndex + 1]);
}

const program = new Command();

program
  .name('dantelabs')
  .description(t('cli.description'))
  .version(pkg.version)
  .option(
    '-l, --lang <locale>',
    `Language (${getAvailableLocales().join(', ')})`,
    'en'
  )
  .hook('preAction', (thisCommand) => {
    const opts = thisCommand.opts();
    if (opts.lang) {
      setLocale(opts.lang);
    }
  })
  .addHelpText('after', `
${chalk.bold(t('cli.examples'))}
  ${chalk.gray(t('cli.installAllPlugins'))}
  $ npx dantelabs-agentic-school install

  ${chalk.gray(t('cli.installSpecificPlugin'))}
  $ npx dantelabs-agentic-school install brand-analytics

  ${chalk.gray(t('cli.installCustomPath'))}
  $ npx dantelabs-agentic-school install --path ./my-project

  ${chalk.gray(t('cli.listPlugins'))}
  $ npx dantelabs-agentic-school list

  ${chalk.gray(t('cli.showPluginInfo'))}
  $ npx dantelabs-agentic-school info brand-analytics

  ${chalk.gray('# Download samples')}
  $ npx dantelabs-agentic-school sample marketing
  $ npx dantelabs-agentic-school sample --all

  ${chalk.gray('# Install for OpenClaw (~/.openclaw/skills/)')}
  $ npx dantelabs-agentic-school install trading-tools -t openclaw

  ${chalk.gray('# Korean language')}
  $ npx dantelabs-agentic-school --lang ko list

${chalk.bold(t('cli.moreInfo'))}: https://github.com/dandacompany/dantelabs-agentic-school
  `);

// Register commands
installCommand(program);
listCommand(program);
infoCommand(program);
uninstallCommand(program);
sampleCommand(program);

// Parse arguments
program.parse();

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
