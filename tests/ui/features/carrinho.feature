# language: pt

@carrinho
Funcionalidade: Cupom de desconto no carrinho
  Como cliente da store
  Quero aplicar cupons de desconto
  Para pagar menos nas minhas compras

Contexto:
    Dado que acesso o site da store

# ================================================================================================================= #

@CA01
Esquema do Cenário: Aplicar cupom válido de 10% de desconto
  Dado que possuo 1 unidade de "<produto>" no carrinho
  E acesso o carrinho
  E o subtotal do carrinho é de R$ "<subtotal>"
  Quando aplico o cupom "<cupom>"
  Então o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | produto               | subtotal | cupom       | desconto | frete | total  |
    | Mochila Urbana 20L    | 100,00   | BEMVINDO10  | 10,00    | 19,90 | 109,90 |
    | Jaqueta Corta-Vento   | 229,90   | BEMVINDO10  | 22,99    | 0,00  | 206,91 |
    | Tênis Casual Urbano   | 189,90   | BEMVINDO10  | 18,99    | 19,90 | 190,81 |

# ================================================================================================================= #

@CA02
Esquema do Cenário: Aplicar cupom ignorando maiúsculas, minúsculas e espaços
  Dado que possuo 1 unidade de "<produto>" no carrinho
  E acesso o carrinho
  Quando aplico o cupom "<cupom>"
  Então o cupom "<cupom>" deve ser aplicado com sucesso
  E o desconto deve ser de R$ "<desconto>"

  Exemplos:
    | produto            | cupom           | desconto |
    | Mochila Urbana 20L | bemvindo10      | 10,00    |
    | Mochila Urbana 20L | BEMvindo10      | 10,00    |
    | Mochila Urbana 20L |  BEMVINDO10     | 10,00    |

# ================================================================================================================= #

@CA03
Esquema do Cenário: Aplicar um cupom inexistente
  Dado que possuo 1 unidade de "<produto>" no carrinho
  E acesso o carrinho
  Quando aplico o cupom "CUPOMINVALIDO"
  Então deve ser exibida a mensagem "Cupom inválido."
  E nenhum desconto deve ser aplicado

Exemplos:
    | produto              | 
    | Mochila Urbana 20L   | 
    | Jaqueta Corta-Vento  |

# ================================================================================================================= #

@CA04
Esquema do Cenário: Aplicar um cupom expirado
  Dado que possuo 1 unidade de "<produto>" no carrinho
  E acesso o carrinho
  Quando aplico o cupom "<cupom>"
  Então deve ser exibida a mensagem "Cupom expirado."
  E nenhum desconto deve ser aplicado

Exemplos:
    | produto              | cupom       |
    | Mochila Urbana 20L   | VERAO2026   |
    | Jaqueta Corta-Vento  | VERAO2026   |

# ================================================================================================================= #

@CA05
Esquema do Cenário: Trocar o cupom aplicado no carrinho
  Dado que possuo 1 unidade de "<produto>" no carrinho
  E acesso o carrinho
  E aplico o cupom "<cupom>"
  Quando removo o cupom aplicado
  E aplico o cupom "<cupom_trocado>"
  Então deve ser exibida a mensagem "Cupom expirado."
  E nenhum desconto deve ser aplicado

Exemplos:
    | produto              | cupom       | cupom_trocado |
    | Mochila Urbana 20L   | BEMVINDO10  | VERAO2026     |
    | Jaqueta Corta-Vento  | BEMVINDO10  | VERAO2026     |

# ================================================================================================================= #

@CA06
  Esquema do Cenário: Aplicar frete grátis para compras a partir de R$ 200,00
    Dado que possuo <quantidade> unidades de "<produto>" no carrinho
    E acesso o carrinho
    Então o subtotal do carrinho deve ser de R$ "<subtotal>"
    E o frete deve ser de R$ "<frete>"

    Exemplos:
      | quantidade | produto            | subtotal | frete  |
      | 2          | Mochila Urbana 20L | 200,00   | 0,00   |
      | 1          | Jaqueta Corta-Vento| 229,90   | 0,00   |
      | 1          | Mochila Urbana 20L | 100,00   | 19,90  |

# ================================================================================================================= #

@CA07
Esquema do Cenário: Cobrar frete para compras abaixo de R$ 200,00
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  E acesso o carrinho
  Então o subtotal do carrinho deve ser de R$ "<subtotal>"
  E o frete deve ser de R$ "<frete>"
  E deve ser informado que faltam R$ "<faltante>" para obter frete grátis

  Exemplos:
    | quantidade | produto             | subtotal | faltante | frete  |
    | 1          | Mochila Urbana 20L  | 100,00   | 100,00   | 19,90  |
    | 1          | Tênis Casual Urbano | 189,90   | 10,10    | 19,90  |
    | 2          | Mochila Urbana 20L  | 200,00   | 0,00     | 0,00   |

# ================================================================================================================= #

# Utilizados dois produtos para evitar que o BUG-001 no limite de R$ 200,00 interfira na validação deste critério.
# Após correção do bug pode ser retirado o segundo produto e validar apenas com um produto. Os passos de acessar o site e adicionar o segundo produto podem ser removidos.
@CA08
Esquema do Cenário: Manter frete grátis quando o desconto reduz o valor abaixo de R$ 200,00
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  E que possuo <quantidade2> unidades de "<produto2>" no carrinho
  E acesso o carrinho
  E o subtotal do carrinho é de R$ "<subtotal>"
  Quando aplico o cupom "<cupom>"
  Então o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | quantidade | produto        | quantidade2 | produto2            | subtotal | cupom       | desconto | frete | total  |
    | 3          | Boné Aba Curva | 2           | Kit 3 Pares de Meias| 209,50   | BEMVINDO10  | 20,95    | 0,00  | 188,55 |

# ================================================================================================================= #

@CA09
Esquema do Cenário: Aplicar desconto somente sobre o subtotal dos produtos
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  E acesso o carrinho
  E o subtotal do carrinho é de R$ "<subtotal>"
  Quando aplico o cupom "<cupom>"
  Então o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | quantidade | produto             | subtotal | cupom       | desconto | frete | total  |
    | 1          | Mochila Urbana 20L  | 100,00   | BEMVINDO10  | 10,00    | 19,90 | 109,90 |
    | 1          | Tênis Casual Urbano | 189,90   | BEMVINDO10  | 18,99    | 19,90 | 190,81 |

# ================================================================================================================= #

@CA10
Esquema do Cenário: Limitar a quantidade máxima de um produto no carrinho
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Quando acesso o carrinho
  Então a quantidade do produto "<produto>" deve ser "<quantidade>"
  E deve ser exibida a mensagem de limite "<mensagem_carrinho>" para o produto "<produto>"
  E o botão de aumentar a quantidade do produto "<produto>" deve estar desabilitado
  E o subtotal do carrinho deve ser de R$ "<subtotal>"

  Exemplos:
    | quantidade | produto             | mensagem_carrinho                 | subtotal |
    | 5          | Mochila Urbana 20L  | Limite de 5 unidades por produto. | 500,00   |
    | 5          | Tênis Casual Urbano | Limite de 5 unidades por produto. | 949,50   |

# ================================================================================================================= #


# A massa disponível permite validar a apresentação e o cálculo com duas casas decimais,
# embora não permita provocar um valor com uma terceira casa decimal para testar o limite de arredondamento.
@CA11
Esquema do Cenário: Exibir valores arredondados com duas casas decimais
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Quando acesso o carrinho
  Quando aplico o cupom "<cupom>"
  Então o subtotal do carrinho deve ser de R$ "<subtotal>"
  E o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | quantidade | produto             | cupom       | subtotal | desconto | frete | total  |
    | 1          | Camiseta Essencial  | BEMVINDO10  | 59,90    | 5,99     | 19,90 | 73,81  |
    | 1          | Tênis Casual Urbano | BEMVINDO10  | 189,90   | 18,99    | 19,90 | 190,81 |