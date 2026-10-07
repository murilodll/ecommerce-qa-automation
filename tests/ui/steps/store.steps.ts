import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

import { StorePage } from '../pages/store.page.ts';
import { CarrinhoPage } from '../pages/carrinho.page.ts';

const { Given, When, Then } = createBdd();

// ======================================================= GIVEN ===================================================== #

Given('que acesso o site da store', async ({ page }) => {
	const storePage = new StorePage(page);

	await storePage.acessar();
});

Given(
	'que possuo {int} unidade(s) de {string} no carrinho',
	async ({ page }, quantidade: number, produto: string) => {
		const storePage = new StorePage(page);

		await storePage.adicionarProduto(produto, quantidade);
	},
);

// ======================================================= WHEN ===================================================== #

When('acesso o carrinho', async ({ page }) => {
	const storePage = new StorePage(page);

	await storePage.acessarCarrinho();
});

// ======================================================= THEN ===================================================== #

Then(
	'deve ser exibida a mensagem {string} para o produto {string} na store',
	async ({ page }, mensagem: string, produto: string) => {
		const storePage = new StorePage(page);

		await expect(storePage.mensagemProduto(produto)).toHaveText(mensagem);
	},
);

Then(
	'o botão de adicionar o produto {string} deve estar desabilitado',
	async ({ page }, produto: string) => {
		const storePage = new StorePage(page);

		await expect(storePage.botaoAdicionarProduto(produto)).toBeDisabled();
	},
);
