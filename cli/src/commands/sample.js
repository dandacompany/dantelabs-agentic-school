import chalk from 'chalk';
import ora from 'ora';
import { mkdir, writeFile, readFile, readdir, cp } from 'fs/promises';
import { join, dirname } from 'path';
import { existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { GITHUB_CONFIG } from '../lib/config.js';
import { fetchFile, getDirectoryContents } from '../lib/downloader.js';
import logger from '../utils/logger.js';
import { t } from '../i18n/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PACKAGE_ROOT = join(__dirname, '../../..');

/**
 * Check if local samples directory exists
 */
function hasLocalSamples() {
  return existsSync(join(PACKAGE_ROOT, 'samples'));
}

/**
 * Get list of available samples (local or remote)
 */
async function getAvailableSamples() {
  if (hasLocalSamples()) {
    const samplesDir = join(PACKAGE_ROOT, 'samples');
    const entries = await readdir(samplesDir, { withFileTypes: true });
    return entries.filter(e => e.isDirectory()).map(e => e.name);
  }

  // Fallback to remote
  const contents = await getDirectoryContents('samples');
  return contents
    .filter(item => item.type === 'dir')
    .map(item => item.name);
}

/**
 * Copy local sample folder recursively
 */
async function copyLocalSampleFolder(sampleName, targetDir, options = {}) {
  const { onFile } = options;
  const localPath = join(PACKAGE_ROOT, 'samples', sampleName);

  if (!existsSync(localPath)) {
    throw new Error(t('sample.notFound', { name: sampleName }));
  }

  // Create target directory
  await mkdir(targetDir, { recursive: true });

  let fileCount = 0;

  async function copyRecursive(srcDir, destDir) {
    const entries = await readdir(srcDir, { withFileTypes: true });

    for (const entry of entries) {
      const srcPath = join(srcDir, entry.name);
      const destPath = join(destDir, entry.name);

      if (entry.isDirectory()) {
        await mkdir(destPath, { recursive: true });
        await copyRecursive(srcPath, destPath);
      } else {
        const content = await readFile(srcPath);
        await writeFile(destPath, content);
        fileCount++;

        if (onFile) {
          onFile(entry.name);
        }
      }
    }
  }

  await copyRecursive(localPath, targetDir);
  return fileCount;
}

/**
 * Download a sample folder from remote
 */
async function downloadRemoteSampleFolder(sampleName, targetDir, options = {}) {
  const { onFile } = options;
  const remotePath = `samples/${sampleName}`;
  const contents = await getDirectoryContents(remotePath);

  if (contents.length === 0) {
    throw new Error(t('sample.notFound', { name: sampleName }));
  }

  // Create target directory
  await mkdir(targetDir, { recursive: true });

  let fileCount = 0;

  for (const item of contents) {
    if (item.type === 'file') {
      const content = await fetchFile(item.path);
      const filePath = join(targetDir, item.name);
      await writeFile(filePath, content);
      fileCount++;

      if (onFile) {
        onFile(item.name);
      }
    } else if (item.type === 'dir') {
      // Recursively download subdirectories
      const subDir = join(targetDir, item.name);
      const subResult = await downloadRemoteSampleFolder(
        `${sampleName}/${item.name}`,
        subDir,
        options
      );
      fileCount += subResult;
    }
  }

  return fileCount;
}

/**
 * Download or copy a sample folder (local or remote)
 */
async function downloadSampleFolder(sampleName, targetDir, options = {}) {
  if (hasLocalSamples()) {
    return copyLocalSampleFolder(sampleName, targetDir, options);
  }
  return downloadRemoteSampleFolder(sampleName, targetDir, options);
}

export default function sampleCommand(program) {
  program
    .command('sample [name]')
    .description(t('sample.description'))
    .option('-a, --all', t('sample.optionAll'))
    .option('-l, --list', t('sample.optionList'))
    .option('-p, --path <path>', t('sample.optionPath'), '.')
    .option('-f, --force', t('sample.optionForce'))
    .action(async (name, options) => {
      try {
        const targetBase = options.path;

        // List available samples
        if (options.list || (!name && !options.all)) {
          const spinner = ora(t('sample.fetchingList')).start();

          try {
            const samples = await getAvailableSamples();
            spinner.stop();

            console.log();
            console.log(chalk.bold.blue(t('sample.availableTitle')));
            console.log(chalk.gray('━'.repeat(50)));
            console.log();

            if (samples.length === 0) {
              console.log(chalk.yellow(t('sample.noSamples')));
            } else {
              for (const sample of samples) {
                console.log(`  ${chalk.cyan('•')} ${sample}`);
              }
              console.log();
              console.log(chalk.gray(t('sample.downloadHint')));
              console.log(chalk.gray(t('sample.downloadAllHint')));
            }
            console.log();
          } catch (error) {
            spinner.fail(t('sample.fetchError'));
            throw error;
          }
          return;
        }

        // Download all samples
        if (options.all) {
          const spinner = ora(t('sample.fetchingList')).start();
          const samples = await getAvailableSamples();
          spinner.stop();

          if (samples.length === 0) {
            logger.warn(t('sample.noSamples'));
            return;
          }

          console.log();
          console.log(chalk.bold.blue(t('sample.downloadingAll', { count: samples.length })));
          console.log();

          let totalFiles = 0;

          for (const sampleName of samples) {
            const targetDir = join(targetBase, 'samples', sampleName);

            if (!options.force && existsSync(targetDir)) {
              logger.warn(t('sample.alreadyExists', { name: sampleName }));
              continue;
            }

            const downloadSpinner = ora(t('sample.downloading', { name: sampleName })).start();

            try {
              const fileCount = await downloadSampleFolder(sampleName, targetDir, {
                onFile: (fileName) => {
                  downloadSpinner.text = t('sample.downloadingFile', { name: sampleName, file: fileName });
                }
              });

              downloadSpinner.succeed(
                t('sample.downloadedFiles', { name: sampleName, count: fileCount })
              );
              totalFiles += fileCount;
            } catch (error) {
              downloadSpinner.fail(t('sample.downloadFailed', { name: sampleName }));
              logger.error(error.message);
            }
          }

          console.log();
          console.log(chalk.green(t('sample.allComplete', { count: totalFiles })));
          console.log(chalk.gray(t('sample.savedTo', { path: join(targetBase, 'samples') })));
          console.log();
          return;
        }

        // Download specific sample
        const targetDir = join(targetBase, 'samples', name);

        if (!options.force && existsSync(targetDir)) {
          logger.error(t('sample.alreadyExistsError', { path: targetDir }));
          console.log(chalk.gray(t('sample.useForceHint')));
          process.exit(1);
        }

        const spinner = ora(t('sample.downloading', { name })).start();

        try {
          const fileCount = await downloadSampleFolder(name, targetDir, {
            onFile: (fileName) => {
              spinner.text = t('sample.downloadingFile', { name, file: fileName });
            }
          });

          spinner.succeed(t('sample.downloadedFiles', { name, count: fileCount }));
          console.log();
          console.log(chalk.gray(t('sample.savedTo', { path: targetDir })));
          console.log();
        } catch (error) {
          spinner.fail(t('sample.downloadFailed', { name }));
          throw error;
        }
      } catch (error) {
        logger.error(error.message);
        process.exit(1);
      }
    });
}
