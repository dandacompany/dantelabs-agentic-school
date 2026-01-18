/**
 * Internationalization (i18n) module
 * Default language: English (en)
 * Supported languages: en, ko
 */

import en from './locales/en.js';
import ko from './locales/ko.js';

const locales = { en, ko };

// Default language
let currentLocale = 'en';

/**
 * Set the current locale
 * @param {string} locale - Locale code (en, ko)
 */
export function setLocale(locale) {
  if (locales[locale]) {
    currentLocale = locale;
  } else {
    console.warn(`Locale '${locale}' not supported. Using 'en' as default.`);
    currentLocale = 'en';
  }
}

/**
 * Get the current locale
 * @returns {string} Current locale code
 */
export function getLocale() {
  return currentLocale;
}

/**
 * Get available locales
 * @returns {string[]} Array of locale codes
 */
export function getAvailableLocales() {
  return Object.keys(locales);
}

/**
 * Get translation for a key path
 * @param {string} keyPath - Dot-separated key path (e.g., 'install.description')
 * @param {object} params - Parameters to interpolate
 * @returns {string} Translated string
 */
export function t(keyPath, params = {}) {
  const keys = keyPath.split('.');
  let value = locales[currentLocale];

  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key];
    } else {
      // Fallback to English
      value = locales.en;
      for (const k of keys) {
        if (value && typeof value === 'object' && k in value) {
          value = value[k];
        } else {
          return keyPath; // Return key if not found
        }
      }
      break;
    }
  }

  if (typeof value !== 'string') {
    return keyPath;
  }

  // Interpolate parameters: {name} -> value
  return value.replace(/\{(\w+)\}/g, (_, key) => {
    return params[key] !== undefined ? params[key] : `{${key}}`;
  });
}

/**
 * Get all translations for a section
 * @param {string} section - Section name (e.g., 'install', 'list')
 * @returns {object} Section translations
 */
export function getSection(section) {
  return locales[currentLocale][section] || locales.en[section] || {};
}

export default {
  setLocale,
  getLocale,
  getAvailableLocales,
  t,
  getSection
};
