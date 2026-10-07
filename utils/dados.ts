import { readFile } from 'fs/promises';

// Classe para resolver as variáveis dentro do arquivo JSON config.json
// Ao utilizar a classe no lugar do arquivo os dados retornam já resolvidos.
// Função recursiva para resolver variáveis dentro de strings
const resolveVariables = (value: any, config: Record<string, any>): any => {
	if (typeof value === 'string') {
		return value.replace(/\${(.*?)}/g, (_, varName) => resolveVariables(config[varName] || '', config));
	} else if (Array.isArray(value)) {
		return value.map((item) => resolveVariables(item, config));
	} else if (typeof value === 'object' && value !== null) {
		return Object.fromEntries(
			Object.entries(value).map(([key, val]) => [key, resolveVariables(val, config)]),
		);
	}
	return value;
};

// Função para carregar e processar o JSON
async function loadConfig() {
	const rawConfig = await readFile(new URL('../data/dados.json', import.meta.url), 'utf8');
	const dados = JSON.parse(rawConfig);

	// Resolver as variáveis em todas as chaves do JSON
	return resolveVariables(dados, dados);
}

const dados = await loadConfig();
export default dados;
