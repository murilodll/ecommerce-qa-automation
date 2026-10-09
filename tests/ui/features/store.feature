# language: pt

@store
Funcionalidade: Adicionar itens ao carrinho
  Como cliente da store
  Quero adicionar produtos ao carrinho

Contexto:
    Dado que acesso o site da store

# ================================================================================================================= #

@CA10
Esquema do Cenário: Impedir adição de produtos acima do limite máximo na Store
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Então deve ser exibida a mensagem "<mensagem_store>" para o produto "<produto>" na store
  E o botão de adicionar o produto "<produto>" deve estar desabilitado
  Quando acesso o carrinho
  Então a quantidade do produto "<produto>" deve ser "<quantidade>"
  E deve ser exibida a mensagem de limite "<mensagem_carrinho>" para o produto "<produto>"
  E o botão de aumentar a quantidade do produto "<produto>" deve estar desabilitado
  E o subtotal do carrinho deve ser de R$ "<subtotal>"

  Exemplos:
    | quantidade | produto             | mensagem_store                  | mensagem_carrinho                 | subtotal |
    | 5          | Mochila Urbana 20L  | Limite de 5 unidades atingido. | Limite de 5 unidades por produto. | 500,00   |
    | 5          | Tênis Casual Urbano | Limite de 5 unidades atingido. | Limite de 5 unidades por produto. | 949,50   |