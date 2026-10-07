import { defineConfig, devices } from '@playwright/test';
import { defineBddConfig, cucumberReporter } from 'playwright-bdd';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import dados from '../utils/dados.ts'; // Importando o arquivo de dados resolvidos

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = resolve(__dirname, '..');

// Obtenha o diretório do arquivo atual
const testDir = defineBddConfig({
	features: resolve(rootDir, 'tests/ui/features/**/*.feature'),
	steps: resolve(rootDir, 'tests/ui/steps/**/*.ts'),
	featuresRoot: resolve(__dirname, '../tests/ui/features'),
	language: 'pt',
	verbose: true,
	missingSteps: 'skip-scenario',
	tags: '(@carrinho or @store) and not @ignore',
});

export default defineConfig({
	testDir,
	timeout: 180 * 1000,
	reporter: [
		['list'],
		['json', { outputFile: resolve(rootDir, 'reports/playwright-results.json') }],
		['html', { outputFolder: resolve(rootDir, 'reports/playwright-report'), open: 'never' }], // Relatório HTML Playwright
		cucumberReporter('html', {
			outputFile: resolve(rootDir, 'reports/cucumber-report/index.html'), // Relatório Cucumber
			externalAttachments: true,
		}),
	],
	outputDir: resolve(rootDir, 'reports/test-results'), // Relatórios

	use: {
		trace: 'on-first-retry',
		headless: true,
		baseURL: dados.BASE_URL,
		screenshot: 'only-on-failure',
		//video: 'on',
		locale: 'pt-BR',
		launchOptions: {
			slowMo: 400,
		},
		actionTimeout: 6 * 1000,
	},

	/* Configure projects for major browsers */
	projects: [
		{
			name: 'chromium',
			use: { ...devices['Desktop Chrome'] },
		},
	],

	/* Run your local dev server before starting the tests */
	// webServer: {
	//   command: 'npm run start',
	//   url: 'http://127.0.0.1:3000',
	//   reuseExistingServer: !process.env.CI,
	// },
});
