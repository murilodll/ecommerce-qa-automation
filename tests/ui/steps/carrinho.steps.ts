import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

import { StorePage } from '../pages/store.page.ts';
import { CarrinhoPage } from '../pages/carrinho.page.ts';

const { Given, When, Then } = createBdd();

async function validarSubtotal(page: Page, subtotal: string): Promise<void> {
	const carrinhoPage = new CarrinhoPage(page);

	await expect(carrinhoPage.obterSubtotal()).toHaveText(`R$ ${subtotal}`);
}

// ======================================================= GIVEN ===================================================== #

Given('o subtotal do carrinho é de R$ {string}', async ({ page }, subtotal: string) => {
	await validarSubtotal(page, subtotal);
});

// ======================================================= WHEN ===================================================== #

When('aplico o cupom {string}', async ({ page }, cupom: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	await carrinhoPage.aplicarCupom(cupom);
});

When('removo o cupom aplicado', async ({ page }) => {
	const carrinhoPage = new CarrinhoPage(page);

	await carrinhoPage.removerCupom();
});

// ======================================================= THEN ===================================================== #

Then('o desconto deve ser de R$ {string}', async ({ page }, desconto: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	const descontoEsperado = desconto === '0,00' ? 'R$ 0,00' : `- R$ ${desconto}`;

	await expect(carrinhoPage.obterDesconto()).toHaveText(descontoEsperado);
});

Then('o frete deve ser de R$ {string}', async ({ page }, frete: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	if (frete === '0,00') {
		await expect(carrinhoPage.obterFrete()).toHaveText('Grátis');
	} else {
		await expect(carrinhoPage.obterFrete()).toHaveText(`R$ ${frete}`);
	}
});

Then('o total do pedido deve ser de R$ {string}', async ({ page }, total: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	await expect(carrinhoPage.obterTotal()).toHaveText(`R$ ${total}`);
});

Then('o cupom {string} deve ser aplicado com sucesso', async ({ page }, cupom: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	const cupomEsperado = cupom.trim().toUpperCase();

	await expect(carrinhoPage.mensagemCupomAplicado(cupomEsperado)).toBeVisible();
});

Then('deve ser exibida a mensagem {string}', async ({ page }, mensagem: string) => {
	const carrinhoPage = new CarrinhoPage(page);

	await expect(carrinhoPage.mensagemCupom()).toHaveText(mensagem);
});

Then('nenhum desconto deve ser aplicado', async ({ page }) => {
	const carrinhoPage = new CarrinhoPage(page);

	await expect(carrinhoPage.obterDesconto()).toHaveText('R$ 0,00');
});

Then('o subtotal do carrinho deve ser de R$ {string}', async ({ page }, subtotal: string) => {
	await validarSubtotal(page, subtotal);
});

Then(
	'deve ser informado que faltam R$ {string} para obter frete grátis',
	async ({ page }, faltante: string) => {
		const carrinhoPage = new CarrinhoPage(page);

		if (faltante === '0,00') {
			await expect(carrinhoPage.obterAvisoFrete()).not.toBeVisible();
			return;
		}

		await expect(carrinhoPage.obterAvisoFrete()).toHaveText(
			`Faltam R$ ${faltante} para o frete grátis.`,
		);
	},
);

Then(
	'a quantidade do produto {string} deve ser {string}',
	async ({ page }, produto: string, quantidade: string) => {
		const carrinhoPage = new CarrinhoPage(page);

		await expect(carrinhoPage.quantidadeProduto(produto)).toHaveText(quantidade);
	},
);

Then(
	'deve ser exibida a mensagem de limite {string} para o produto {string}',
	async ({ page }, mensagem: string, produto: string) => {
		const carrinhoPage = new CarrinhoPage(page);

		await expect(carrinhoPage.mensagemLimite(produto)).toHaveText(mensagem);
	},
);

Then(
	'o botão de aumentar a quantidade do produto {string} deve estar desabilitado',
	async ({ page }, produto: string) => {
		const carrinhoPage = new CarrinhoPage(page);

		await expect(carrinhoPage.botaoAumentarQuantidade(produto)).toBeDisabled();
	},
);
