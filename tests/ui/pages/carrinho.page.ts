import type { Locator, Page } from '@playwright/test';

export class CarrinhoPage {
	private readonly campoCupom: Locator;
	private readonly botaoAplicarCupom: Locator;
	private readonly subtotal: Locator;
	private readonly desconto: Locator;
	private readonly frete: Locator;
	private readonly total: Locator;

	constructor(private readonly page: Page) {
		this.campoCupom = page.getByLabel('Cupom de desconto');
		this.botaoAplicarCupom = page.getByRole('button', { name: 'Aplicar cupom' });
		this.subtotal = page.locator('[data-valor="subtotal"]');
		this.desconto = page.locator('[data-valor="desconto"]');
		this.frete = page.locator('[data-valor="frete"]');
		this.total = page.locator('[data-valor="total"]');
	}

	quantidadeProduto(produto: string): Locator {
		return this.page.locator(`output[aria-label="Quantidade de ${produto}"]`);
	}

	botaoAumentarQuantidade(produto: string): Locator {
		return this.page.getByRole('button', { name: `Aumentar quantidade de ${produto}` });
	}

	botaoDiminuirQuantidade(produto: string): Locator {
		return this.page.getByRole('button', { name: `Diminuir quantidade de ${produto}` });
	}

	botaoRemoverProduto(produto: string): Locator {
		return this.page.getByRole('button', { name: `Remover ${produto} do carrinho` });
	}

	mensagemLimite(produto: string): Locator {
		return this.page.locator('.item-carrinho').filter({ hasText: produto }).locator('.item-limite');
	}

	async aplicarCupom(cupom: string): Promise<void> {
		await this.campoCupom.fill(cupom);
		await this.botaoAplicarCupom.click();
	}

	mensagemCupomAplicado(cupom: string): Locator {
		return this.page.locator('.cupom-aplicado').getByText(`Cupom ${cupom} aplicado.`);
	}

	mensagemCupom(): Locator {
		return this.page.getByRole('alert');
	}

	async removerCupom(): Promise<void> {
		await this.page
			.getByRole('button', {
				name: 'Remover cupom',
			})
			.click();
	}

	obterSubtotal(): Locator {
		return this.subtotal;
	}

	obterDesconto(): Locator {
		return this.desconto;
	}

	obterFrete(): Locator {
		return this.frete;
	}

	obterAvisoFrete(): Locator {
		return this.page.locator('.aviso-frete');
	}

	obterTotal(): Locator {
		return this.total;
	}
}
