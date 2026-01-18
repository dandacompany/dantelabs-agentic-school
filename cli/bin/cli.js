#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync } from 'fs';

import installCommand from '../src/commands/install.js';
import listCommand from '../src/commands/list.js';
import infoCommand from '../src/commands/info.js';
import uninstallCommand from '../src/commands/uninstall.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Read version from package.json
const pkg = JSON.parse(
  readFileSync(join(__dirname, '../../package.json'), 'utf8')
);

const program = new Command();

program
  .name('dantelabs')
  .description('Dante Labs Agentic School - Claude Code Plugin Installer')
  .version(pkg.version)
  .addHelpText('after', `
${chalk.bold('Examples:')}
  ${chalk.gray('# Install all plugins')}
  $ npx dantelabs-agentic-school install

  ${chalk.gray('# Install specific plugin')}
  $ npx dantelabs-agentic-school install brand-analytics

  ${chalk.gray('# Install to custom path')}
  $ npx dantelabs-agentic-school install --path ./my-project

  ${chalk.gray('# List available plugins')}
  $ npx dantelabs-agentic-school list

  ${chalk.gray('# Show plugin info')}
  $ npx dantelabs-agentic-school info brand-analytics

${chalk.bold('More info:')} https://github.com/dandacompany/dantelabs-agentic-school
  `);

// Register commands
installCommand(program);
listCommand(program);
infoCommand(program);
uninstallCommand(program);

// Parse arguments
program.parse();

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
