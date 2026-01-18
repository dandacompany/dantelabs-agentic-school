import { mkdir, writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { existsSync } from 'fs';
import { GITHUB_CONFIG } from './config.js';

/**
 * Fetch file content from GitHub
 */
export async function fetchFile(path) {
  const url = `${GITHUB_CONFIG.rawBase}/${path}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status}`);
  }

  return response.text();
}

/**
 * Get directory contents from GitHub API
 */
export async function getDirectoryContents(path) {
  const url = `${GITHUB_CONFIG.apiBase}/contents/${path}?ref=${GITHUB_CONFIG.branch}`;
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'dantelabs-agentic-school-cli'
    }
  });

  if (!response.ok) {
    if (response.status === 404) {
      return [];
    }
    throw new Error(`GitHub API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Recursively download a directory
 */
export async function downloadDirectory(remotePath, localPath, options = {}) {
  const contents = await getDirectoryContents(remotePath);

  for (const item of contents) {
    const localItemPath = join(localPath, item.name);

    if (item.type === 'dir') {
      await mkdir(localItemPath, { recursive: true });
      await downloadDirectory(item.path, localItemPath, options);
    } else if (item.type === 'file') {
      const content = await fetchFile(item.path);
      const dir = dirname(localItemPath);

      if (!existsSync(dir)) {
        await mkdir(dir, { recursive: true });
      }

      await writeFile(localItemPath, content);

      if (options.onFile) {
        options.onFile(item.path, localItemPath);
      }
    }
  }
}

/**
 * Download a specific plugin from GitHub
 */
export async function downloadPlugin(pluginName, targetDir, options = {}) {
  const pluginPath = `plugins/${pluginName}`;

  // Download entire plugin directory
  await downloadDirectory(pluginPath, targetDir, options);

  return true;
}

/**
 * Download marketplace config
 */
export async function downloadMarketplaceConfig() {
  const content = await fetchFile('.claude-plugin/marketplace.json');
  return JSON.parse(content);
}
