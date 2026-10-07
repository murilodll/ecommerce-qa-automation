import type { Page, Locator } from '@playwright/test';

export class StorePage {
	constructor(private readonly page: Page) {}

	async acessar(): Promise<void> {
		await this.page.goto('/');
	}

	private cardProduto(produto: string): Locator {
		return this.page.getByRole('article', { name: produto });
	}

	mensagemProduto(produto: string): Locator {
		return this.cardProduto(produto).locator('.produto-aviso');
	}

	botaoAdicionarProduto(produto: string): Locator {
		return this.cardProduto(produto).getByRole('button', {
			name: 'Adicionar ao carrinho',
		});
	}

	async adicionarProduto(produto: string, quantidade: number = 1): Promise<void> {
		const botaoAdicionar = this.botaoAdicionarProduto(produto);
		for (let i = 0; i < quantidade; i++) {
			await botaoAdicionar.click();
		}
	}

	async acessarCarrinho(): Promise<void> {
		await this.page.getByRole('link', { name: /^Carrinho/ }).click();
	}
}
