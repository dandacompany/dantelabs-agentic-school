import chalk from 'chalk';

export class Logger {
  constructor(options = {}) {
    this.silent = options.silent || false;
  }

  info(message) {
    if (!this.silent) {
      console.log(chalk.blue('info'), message);
    }
  }

  success(message) {
    if (!this.silent) {
      console.log(chalk.green('success'), message);
    }
  }

  warn(message) {
    if (!this.silent) {
      console.log(chalk.yellow('warn'), message);
    }
  }

  error(message) {
    console.error(chalk.red('error'), message);
  }

  debug(message) {
    if (process.env.DEBUG) {
      console.log(chalk.gray('debug'), message);
    }
  }
}

export default new Logger();
