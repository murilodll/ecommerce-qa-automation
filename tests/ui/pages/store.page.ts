import type { Page } from '@playwright/test';

export class StorePage {
	constructor(private readonly page: Page) {}

	async acessar(): Promise<void> {
		await this.page.goto('/');
	}

	async adicionarProduto(produto: string, quantidade: number = 1): Promise<void> {
		const cardProduto = this.page.getByRole('article', { name: produto });
		const botaoAdicionar = cardProduto.getByRole('button', { name: 'Adicionar ao carrinho' });
		for (let i = 0; i < quantidade; i++) {
			await botaoAdicionar.click();
		}
	}

	async acessarCarrinho(): Promise<void> {
		await this.page.getByRole('link', { name: /^Carrinho/ }).click();
	}
}
