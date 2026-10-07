# language: pt

@manual @checkout
Funcionalidade: Checkout da Compra
  Como cliente da Store
  Quero revisar meu pedido e informar meus dados de entrega
  Para confirmar a compra

  @MANUAL-CHECKOUT-001
  Cenário: Voltar do checkout para o carrinho
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando clico em "Voltar ao carrinho"
    Então devo ser direcionado para o carrinho
    E os produtos adicionados anteriormente devem permanecer no carrinho

  @MANUAL-CHECKOUT-002
  Cenário: Exibir no checkout o mesmo resumo apresentado no carrinho
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Então os produtos e suas quantidades devem corresponder aos itens do carrinho
    E o subtotal deve corresponder ao subtotal do carrinho
    E o desconto deve corresponder ao desconto do carrinho
    E o frete deve corresponder ao frete do carrinho
    E o total deve corresponder ao total do carrinho

  @MANUAL-CHECKOUT-003
  Cenário: Finalizar pedido com dados válidos
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando informo nome e sobrenome
    E informo um e-mail válido
    E informo um CEP válido
    E confirmo o pedido
    Então o pedido deve ser confirmado com sucesso
    E deve ser exibido um número de pedido no formato esperado
    E deve ser informado que o pagamento é feito na entrega

  @MANUAL-CHECKOUT-004
  Cenário: Tentar finalizar pedido sem informar nome e sobrenome
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando informo um nome incompleto
    E preencho os demais campos com dados válidos
    E tento confirmar o pedido
    Então o pedido não deve ser confirmado
    E deve ser apresentada uma mensagem de validação para o nome completo

  @MANUAL-CHECKOUT-005
  Cenário: Tentar finalizar pedido com e-mail inválido
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando informo um e-mail em formato inválido
    E preencho os demais campos com dados válidos
    E tento confirmar o pedido
    Então o pedido não deve ser confirmado
    E deve ser apresentada uma mensagem de validação para o e-mail

  @MANUAL-CHECKOUT-006
  Esquema do Cenário: Finalizar pedido utilizando um CEP válido
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando preencho os dados obrigatórios com informações válidas
    E informo o CEP "<cep>"
    E confirmo o pedido
    Então o pedido deve ser confirmado com sucesso
    E deve ser exibido o número do pedido

    Exemplos:
      | cep       |
      | 58000000  |
      | 58000-000 |

  @MANUAL-CHECKOUT-007
  Cenário: Tentar finalizar pedido com CEP inválido
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando informo um CEP que não possui 8 dígitos
    E preencho os demais campos com dados válidos
    E tento confirmar o pedido
    Então o pedido não deve ser confirmado
    E deve ser apresentada uma mensagem de validação para o CEP

  @MANUAL-CHECKOUT-008
  Cenário: Tentar finalizar pedido sem preencher os dados de entrega
    Dado que possuo produtos no carrinho
    E acesso a página de checkout
    Quando tento confirmar o pedido sem preencher os dados de entrega
    Então o pedido não deve ser confirmado
    E devem ser apresentadas mensagens de validação para os campos obrigatórios