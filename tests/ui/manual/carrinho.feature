# language: pt

@manual @carrinho
Funcionalidade: Gerenciamento do Carrinho
  Como cliente da Store
  Quero gerenciar os produtos adicionados ao carrinho
  Para ajustar minha compra antes de finalizar o pedido

  @MANUAL-CARRINHO-001
  Cenário: Aumentar a quantidade de um produto no carrinho
    Dado que possuo 1 unidade de um produto no carrinho
    Quando aumento a quantidade do produto
    Então a quantidade do produto deve ser 2
    E o valor total do item deve ser atualizado
    E o resumo do pedido deve ser recalculado

  @MANUAL-CARRINHO-002
  Cenário: Diminuir a quantidade de um produto no carrinho
    Dado que possuo 2 unidades de um produto no carrinho
    Quando diminuo a quantidade do produto
    Então a quantidade do produto deve ser 1
    E o valor total do item deve ser atualizado
    E o resumo do pedido deve ser recalculado

  @MANUAL-CARRINHO-003
  Cenário: Remover um produto do carrinho com outros produtos adicionados
    Dado que possuo mais de um produto diferente no carrinho
    Quando removo um dos produtos
    Então o produto removido não deve mais ser exibido no carrinho
    E os demais produtos devem permanecer no carrinho
    E o resumo do pedido deve ser recalculado

  @MANUAL-CARRINHO-004
  Cenário: Remover o último produto do carrinho
    Dado que possuo apenas um produto no carrinho
    Quando removo o produto
    Então o carrinho deve ficar vazio
    E deve ser apresentada a indicação de carrinho vazio

  @MANUAL-CARRINHO-005
  Cenário: Esvaziar o carrinho
      Dado que possuo produtos no carrinho
      Quando clico em esvaziar carrinho
      Então o carrinho deve ficar vazio
      E deve ser apresentada a indicação de carrinho vazio