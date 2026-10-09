# E-commerce QA Automation

Projeto de Quality Assurance desenvolvido sobre a Verzel Store,
contemplando planejamento e execução de testes manuais, automação de interface,
testes de API, documentação de defeitos, evidências e acompanhamento dos resultados.

A solução contempla planejamento e execução de testes manuais, cenários
escritos em Gherkin, automação de testes de interface com Playwright e
validações de API com REST Assured.

Além da execução dos testes, o projeto inclui documentação dos defeitos
encontrados, evidências, relatórios automatizados e um dashboard para
acompanhamento dos resultados.

## Sumário

- [Escopo](#escopo)
- [Estratégia de Testes](#estratégia-de-testes)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
- [Execução via Linha de Comando (CLI)](#execução-via-linha-de-comando-cli)
- [Visualização dos Relatórios](#visualização-dos-relatórios)
- [Resultados dos Testes](#resultados-dos-testes)
- [Bugs Encontrados](#bugs-encontrados)
- [Relatórios e Evidências](#relatórios-e-evidências)
- [Decisões Técnicas](#decisões-técnicas)
- [Uso de Inteligência Artificial](#uso-de-inteligência-artificial)

## Escopo

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

Os testes foram elaborados a partir da documentação funcional
disponibilizada para a Verzel Store, com foco nas regras de negócio
relacionadas a:

- Aplicação e validação de cupons de desconto;
- Cálculo de subtotal, desconto, frete e total;
- Regra de frete grátis;
- Limite máximo de unidades por produto;
- Gerenciamento do carrinho;
- Validações e confirmação do checkout;
- Endpoints de produtos, carrinho e pedidos.

Foram utilizadas abordagens complementares de testes manuais e
automatizados para validar tanto a interface quanto a API.

## Estratégia de Testes

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
A estratégia adotada foi dividida em três frentes:

### Testes manuais e exploratórios

Cenários voltados principalmente para navegação, gerenciamento do
carrinho e fluxo de checkout.

Os cenários foram escritos em Gherkin e possuem identificadores
individuais para permitir o registro e acompanhamento de cada execução.

### Automação de interface

Os principais critérios de aceitação relacionados às regras de carrinho,
cupons, frete e limite de produtos foram automatizados utilizando
Playwright, TypeScript e Playwright-BDD.

A implementação utiliza Page Objects para separar a interação com as
páginas das definições dos passos dos cenários.

### Automação de API

A API foi validada utilizando REST Assured, Java, JUnit 5 e Maven.

Os testes cobrem os endpoints de produtos, cálculo do carrinho e criação
de pedidos, incluindo cenários positivos, validações de entrada e
respostas de erro.

Os testes que reproduzem defeitos conhecidos foram separados da suíte de
regressão através da tag `known-bug`, permitindo que a regressão
permaneça independente dos defeitos já identificados.

## Tecnologias Utilizadas

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

### Interface

- **Playwright** - automação dos testes de interface.
- **TypeScript** - implementação dos testes automatizados.
- **Playwright-BDD** - integração dos cenários Gherkin com Playwright.
- **Gherkin** - especificação dos cenários de teste em linguagem de
  negócio.

### API

- **Java 21** - linguagem utilizada na automação da API.
- **REST Assured** - execução e validação das requisições HTTP.
- **JUnit 5** - estrutura e execução dos testes de API.
- **Maven** - gerenciamento das dependências e execução das suítes.

### Execução e acompanhamento

- **Python** - implementação modular da ferramenta auxiliar para
  execução e acompanhamento dos testes.
- **Streamlit** - interface para execução manual, disparo das
  automações e visualização consolidada dos resultados.
- **CSV / JSON** - persistência dos resultados manuais e centralização
  dos dados utilizados pelos testes.

## Estrutura do Projeto

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

```text

e-commerce/
├── config/
│ └── playwright.config.ts
├── data/
│ ├── dados.json
│ ├── execucoes.csv
│ └── produtos.json
├── docs/
│ ├── bugs/
│ └── evidencias/
├── reports/
├── src/
│ ├── main.py
│ ├── manual_tests.py
│ ├── dashboard.py
│ ├── runners.py
│ ├── gherkin_loader.py
│ └── api_results_loader.py
├── tests/
│ ├── api/
│ └── ui/
├── utils/
│ └── dados.ts
├── package.json
├── package-lock.json
├── requirements.txt
├── tsconfig.json
└── README.md

```

## Pré-requisitos

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

Para executar todas as funcionalidades do projeto, é necessário ter
instalado:

- Node.js e npm;
- Java JDK 21;
- Maven;
- Python 3 e pip.

## Instalação

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
Clone o repositório e acesse a pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd e-commerce
```

### Dependências da automação de interface

Instale as dependências Node.js:

```bash
npm install
```

Instale o Chromium utilizado pelo Playwright:

```bash
npx playwright install chromium
```

### Dependências Python

Instale as dependências utilizadas pela aplicação Streamlit:

```bash
pip install -r requirements.txt
```

As versões utilizadas no desenvolvimento estão fixadas no arquivo
`requirements.txt`.

### Dependências da automação de API

As dependências dos testes de API são gerenciadas pelo Maven através do
arquivo `tests/api/pom.xml` e são baixadas automaticamente durante a
primeira execução.

## Execução

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

### Aplicação Auxiliar em Python / Streamlit

#### Auxiliar de Execução Manual, Triggers de Execuções dos Automáticos e Dashboard _(Lightweight Test Case Management Tool / TCMS)_

Para iniciar a aplicação Streamlit:

```bash
python -m streamlit run src/main.py
```

Foi desenvolvida uma aplicação em Streamlit como ferramenta auxiliar para centralizar:

- A visualização e o registro da execução dos cenários manuais;
- O acionamento e a execução das automações;
- O acompanhamento dos resultados das suítes de testes;
- A visualização consolidada do estado dos testes no dashboard.

A aplicação Python foi dividida por responsabilidade para manter o fluxo
principal simples e reduzir o acoplamento entre execução, persistência e
visualização:

```text
src/
├── main.py                 # Orquestração da aplicação Streamlit
├── manual_tests.py         # Execução e persistência dos testes manuais
├── dashboard.py            # Métricas e visualização dos resultados
├── runners.py              # Execução e leitura das automações
├── gherkin_loader.py       # Leitura dos cenários Gherkin
└── api_results_loader.py   # Leitura dos resultados REST Assured / JUnit
```

O `main.py` atua principalmente como orquestrador das abas. Os cenários
manuais são carregados a partir dos arquivos Gherkin e seu estado de
execução é persistido em `data/execucoes.csv`. O dashboard utiliza o
estado completo mantido pela aplicação, de forma independente dos
filtros aplicados na visualização dos testes manuais.

O dashboard não substitui os testes ou seus relatórios originais. Ele
funciona como uma camada adicional para facilitar o acompanhamento das
execuções.

## Execução via Linha de Comando (CLI)

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
Todos os comandos abaixo devem ser executados a partir da raiz do
projeto e servem como alternativa para acionar manualmente as automações via terminal.

### Automação de interface

Para gerar os testes BDD e executar a suíte Playwright:

```bash
npm test
```

Esse comando executa:

```bash
npx bddgen -c config/playwright.config.ts
npx playwright test -c config/playwright.config.ts
```

O `bddgen` gera os testes a partir dos cenários Gherkin e, em seguida, o
Playwright executa a suíte automatizada no Chromium.

### Automação de API

A suíte de regressão da API também pode ser executada através do npm:

```bash
npm run test:api
```

Esse script executa:

```bash
mvn test -f tests/api/pom.xml
```

Também é possível executar diretamente pelo Maven:

```bash
mvn -f tests/api/pom.xml test
```

A suíte de regressão exclui os cenários associados a defeitos
conhecidos.

Para executar exclusivamente os cenários que reproduzem os defeitos
conhecidos:

```bash
mvn -f tests/api/pom.xml -Pknown-bugs test
```

> **Nota:** enquanto os defeitos documentados permanecerem na aplicação,
> a execução do perfil `known-bugs` termina com `BUILD FAILURE`. Esse
> comportamento é esperado, pois os testes mantêm as asserções
> correspondentes ao comportamento definido nos requisitos e demonstram
> as divergências encontradas na aplicação.

## Visualização dos Relatórios

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

### Relatório Playwright

Após a execução dos testes de interface, o relatório HTML do Playwright
pode ser aberto com:

```bash
npm run playwright-report
```

O comando abre o relatório localizado em:

```text
reports/playwright-report/
```

### Relatório Cucumber

O relatório dos cenários BDD pode ser aberto com:

```bash
npm run cucumber-report
```

O comando abre o relatório localizado em:

```text
reports/cucumber-report/
```

### Relatórios da API

Os resultados JUnit/XML da suíte de regressão da API são gerados em:

```text
reports/api/
```

Os resultados dos testes destinados à reprodução dos bugs conhecidos são
armazenados separadamente em:

```text
reports/api/known-bugs/
```

Esses resultados também são processados pela aplicação Streamlit e
apresentados no dashboard.

## Resultados dos Testes

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
A execução final das suítes apresentou os seguintes resultados:

| Tipo                      | Total | Passou | Falhou | Observação                                           |
| ------------------------- | ----: | -----: | -----: | ---------------------------------------------------- |
| Testes manuais            |    18 |     18 |      0 | Todos os cenários manuais executados com sucesso     |
| Playwright - UI           |    27 |     25 |      2 | As duas falhas reproduzem o BUG-001                  |
| REST Assured - Regressão  |    28 |     28 |      0 | Suíte de regressão executada com sucesso             |
| REST Assured - Known Bugs |     3 |      0 |      3 | Três cenários reproduzem os dois defeitos conhecidos |

As falhas presentes nas suítes automatizadas não representam falhas da
infraestrutura de automação. Elas correspondem a divergências entre o
comportamento esperado, definido nos requisitos, e o comportamento atual
da aplicação.

### Execução manual

Foram realizadas **18 execuções manuais**, baseadas em cenários escritos em Gherkin, abrangendo navegação pela loja, manipulação do carrinho e validações do checkout.

Resultado:

```text
18 Passed
0 Failed
```

O estado de cada execução é registrado em `data/execucoes.csv` e pode
ser acompanhado através da aplicação Streamlit.

### Automação de interface

A execução final do Playwright apresentou:

```text
27 testes
25 Passed
2 Failed
```

As duas falhas estão relacionadas ao mesmo defeito de regra de negócio,
documentado como `BUG-001`, referente à cobrança de frete quando o
subtotal é exatamente R\$ 200,00.

Os testes mantêm a expectativa definida no requisito, permitindo que o
defeito continue sendo detectado até que o comportamento da aplicação
seja corrigido.

### Automação de API

A suíte principal de regressão apresentou:

```text
28 testes
28 Passed
0 Failed
```

Os cenários que reproduzem defeitos conhecidos são mantidos
separadamente através da tag `known-bug`.

A execução específica desses cenários apresentou:

```text
3 testes
3 Failed
```

Essas três falhas reproduzem **dois defeitos distintos**:

- um cenário reproduz o `BUG-001`;
- dois cenários reproduzem o `BUG-002`, validando o problema tanto no
  cálculo do carrinho quanto na criação do pedido.

## Bugs Encontrados

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
Durante a execução dos testes foram identificados dois defeitos
relacionados às regras de negócio.

### BUG-001 - Frete cobrado para subtotal de exatamente R\$ 200,00

Quando o subtotal do carrinho é exatamente R\$ 200,00, a aplicação cobra
R\$ 19,90 de frete.

De acordo com o critério de aceitação, compras com subtotal **maior ou
igual a R\$ 200,00** devem possuir frete grátis.

O problema foi reproduzido tanto pela interface quanto diretamente
através da API.

**Relatório:** [`docs/bugs/BUG-001.md`](docs/bugs/BUG-001.md)

### BUG-002 - API permite quantidade superior ao limite máximo de 5 unidades

A API permite utilizar uma quantidade superior a 5 unidades do mesmo
produto.

O comportamento foi identificado em dois pontos:

- o cálculo do carrinho aceita 6 unidades e retorna HTTP `200`;
- a criação do pedido aceita 6 unidades, retorna HTTP `201` e confirma
  o pedido.

De acordo com o critério de aceitação, a quantidade máxima permitida é
de 5 unidades por produto.

**Relatório:** [`docs/bugs/BUG-002.md`](docs/bugs/BUG-002.md)

## Relatórios e Evidências

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
Os artefatos gerados durante as execuções estão organizados no projeto
para facilitar a análise dos resultados.

### Evidências dos bugs

As evidências utilizadas nos relatórios estão disponíveis em:

```text
docs/evidencias/
├── BUG-001/
│   ├── BUG-001-ui.png
│   └── BUG-001-api.png
└── BUG-002/
    ├── BUG-002-carrinho-api.png
    └── BUG-002-pedido-api.png
```

Cada relatório de bug contém a descrição do problema, passos para
reprodução, resultado esperado, resultado obtido, impacto e referência
às respectivas evidências.

### Relatórios Playwright

Os relatórios da automação de interface são gerados no diretório
`reports/`.

O relatório HTML permite consultar individualmente os cenários
executados, resultados, erros e evidências geradas pelo Playwright e
Cucumber.

### Relatórios REST Assured / JUnit

Os resultados da suíte de regressão da API são gerados em:

```text
reports/api/
```

Os resultados dos cenários de reprodução dos defeitos conhecidos são
mantidos separadamente em:

```text
reports/api/known-bugs/
```

Essa separação permite acompanhar a saúde da regressão sem ocultar os
testes que demonstram problemas conhecidos da aplicação.

## Decisões Técnicas

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>
Algumas decisões foram adotadas para manter a solução organizada,
reproduzível e facilitar a análise dos resultados.

### Gherkin como especificação dos cenários

Os cenários de teste foram escritos em Gherkin para manter uma descrição
próxima às regras de negócio e facilitar a rastreabilidade entre
requisitos, cenários e automação.

Os cenários destinados à execução manual e à automação foram mantidos
separadamente:

```text
tests/ui/manual/
tests/ui/features/
```

Os cenários manuais são interpretados pela aplicação Streamlit para
permitir o registro das execuções, enquanto os cenários automatizados
são processados pelo Playwright-BDD.

### Page Object Model

A automação de interface utiliza Page Objects para centralizar seletores
e ações relacionadas às páginas da aplicação.

Essa abordagem reduz duplicação nos steps e separa a lógica de interação
com a interface da descrição dos cenários de teste.

### Centralização dos dados de teste

URLs, endpoints e demais dados compartilhados pelos testes foram
centralizados em:

```text
data/dados.json
```

O arquivo é utilizado pelas diferentes partes da solução, evitando a
duplicação de informações de configuração nos testes.

### Separação dos bugs conhecidos

Os testes de API que reproduzem defeitos identificados durante o desafio
utilizam a tag:

```text
known-bug
```

Esses cenários são excluídos da execução padrão da regressão e podem ser
executados separadamente através do perfil Maven:

```bash
mvn -f tests/api/pom.xml -Pknown-bugs test
```

A separação permite manter a suíte de regressão estável sem remover ou
alterar testes que demonstram comportamentos divergentes dos requisitos.

### API stateless

Os testes de API foram desenvolvidos de forma independente entre si, sem
depender da execução ou do estado produzido por outros testes.

Isso é compatível com o comportamento da API disponibilizada para o
desafio e reduz dependências entre cenários.

## Uso de Inteligência Artificial

<div align="right">
  <sup><a href="#sumário">🏠 Voltar ao topo</a></sup>
</div>

Ferramentas de Inteligência Artificial foram utilizadas como apoio assistido durante o desenvolvimento da solução. O uso ocorreu por meio de interações via chat e recursos de autocomplete inteligente na IDE. Não foram utilizados agentes autônomos, _Skills_, MCP (_Model Context Protocol_) ou outras ferramentas de execução autônoma.

O suporte abrangeu atividades como:

- Discussão e refinamento da estratégia de testes;
- Revisão e sugestões de implementação;
- Apoio na estruturação de cenários e validações;
- Análise e resolução de erros durante o desenvolvimento;
- Organização e documentação do projeto.

### Validação e autoria

As decisões relacionadas à estratégia de testes, implementação, escopo dos cenários, validação dos resultados e classificação dos defeitos foram revisadas e validadas pelo autor durante o desenvolvimento da solução.

Os testes foram executados contra o ambiente disponibilizado para o desafio. Os resultados, relatórios e evidências apresentados neste repositório correspondem às execuções realizadas na aplicação.
