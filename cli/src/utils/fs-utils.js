import { access, constants } from 'fs/promises';
import { existsSync } from 'fs';
import { homedir } from 'os';
import { join, resolve } from 'path';

/**
 * Check if path exists and is writable
 */
export async function isWritable(path) {
  try {
    await access(path, constants.W_OK);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get default .claude directory
 */
export function getDefaultClaudeDir() {
  return join(homedir(), '.claude');
}

/**
 * Resolve path with ~ expansion
 */
export function resolvePath(inputPath) {
  if (inputPath.startsWith('~')) {
    return join(homedir(), inputPath.slice(1));
  }
  return resolve(inputPath);
}

/**
 * Check if directory is a claude project
 */
export function isClaudeProject(dir) {
  return existsSync(join(dir, '.claude')) ||
         existsSync(join(dir, 'CLAUDE.md'));
}
