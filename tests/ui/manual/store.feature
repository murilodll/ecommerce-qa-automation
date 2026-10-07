# language: pt

@manual @store
Funcionalidade: Interação na Store
  Como cliente da Store
  Quero navegar pelas opções disponíveis
  Para acessar os produtos, a documentação e o carrinho

  @MANUAL-STORE-001
  Cenário: Navegar para a seção de produtos
    Dado que acesso a página da Store
    Quando clico na opção "Produtos"
    Então devo ser direcionado para a seção de produtos

  @MANUAL-STORE-002
  Cenário: Navegar para a documentação
    Dado que acesso a página da Store
    Quando clico na opção "Documentação"
    Então devo ser direcionado para a página de documentação

  @MANUAL-STORE-003
  Cenário: Navegar para o carrinho
    Dado que acesso a página da Store
    Quando clico na opção "Carrinho"
    Então devo ser direcionado para a página do carrinho

  @MANUAL-STORE-004
  Cenário: Atualizar a quantidade de itens exibida no acesso ao carrinho
    Dado que acesso a página da Store
    E o carrinho está vazio
    Quando adiciono 1 unidade de um produto ao carrinho
    Então o acesso ao carrinho deve indicar 1 item no carrinho
    Quando adiciono mais 1 unidade do mesmo produto
    Então o acesso ao carrinho deve indicar 2 itens no carrinho