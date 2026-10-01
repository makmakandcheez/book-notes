import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
    rules: {
      // Flags the standard "fetch on mount" effect pattern (setState directly
      // in the effect body) as a smell, even though it's the pattern React's
      // own docs use for data fetching. Too aggressive for a hand-rolled data
      // layer without a fetching library.
      'react-hooks/set-state-in-effect': 'off',
    },
  },
])
