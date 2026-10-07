# language: pt

@carrinho
Funcionalidade: Cupom de desconto no carrinho
  Como cliente da store
  Quero aplicar cupons de desconto
  Para pagar menos nas minhas compras

Contexto:
    Dado que acesso o site da store

# ================================================================================================================= #

@CA01 @ignore
Esquema do Cenário: Aplicar cupom válido de 10% de desconto
  Dado que possuo 1 unidade de "<produto>" no carrinho
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

@CA02 @ignore
Esquema do Cenário: Aplicar cupom ignorando maiúsculas, minúsculas e espaços
  Dado que possuo 1 unidade de "<produto>" no carrinho
  Quando aplico o cupom "<cupom>"
  Então o cupom "<cupom>" deve ser aplicado com sucesso
  E o desconto deve ser de R$ "<desconto>"

  Exemplos:
    | produto            | cupom           | desconto |
    | Mochila Urbana 20L | bemvindo10      | 10,00    |
    | Mochila Urbana 20L | BEMvindo10      | 10,00    |
    | Mochila Urbana 20L |  BEMVINDO10     | 10,00    |

# ================================================================================================================= #

@CA03 @ignore
Esquema do Cenário: Aplicar um cupom inexistente
  Dado que possuo 1 unidade de "<produto>" no carrinho
  Quando aplico o cupom "CUPOMINVALIDO"
  Então deve ser exibida a mensagem "Cupom inválido."
  E nenhum desconto deve ser aplicado

Exemplos:
    | produto              | 
    | Mochila Urbana 20L   | 
    | Jaqueta Corta-Vento  |

# ================================================================================================================= #

@CA04 @ignore
Esquema do Cenário: Aplicar um cupom expirado
  Dado que possuo 1 unidade de "<produto>" no carrinho
  Quando aplico o cupom "<cupom>"
  Então deve ser exibida a mensagem "Cupom expirado."
  E nenhum desconto deve ser aplicado

Exemplos:
    | produto              | cupom       |
    | Mochila Urbana 20L   | VERAO2026   |
    | Jaqueta Corta-Vento  | VERAO2026   |

# ================================================================================================================= #

@CA05 @ignore
Esquema do Cenário: Trocar o cupom aplicado no carrinho
  Dado que possuo 1 unidade de "<produto>" no carrinho
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

@CA06 @ignore
  Esquema do Cenário: Aplicar frete grátis para compras a partir de R$ 200,00
    Dado que possuo <quantidade> unidades de "<produto>" no carrinho
    Então o subtotal do carrinho deve ser de R$ "<subtotal>"
    E o frete deve ser de R$ "<frete>"

    Exemplos:
      | quantidade | produto            | subtotal | frete  |
      | 2          | Mochila Urbana 20L | 200,00   | 0,00   |
      | 1          | Jaqueta Corta-Vento| 229,90   | 0,00   |
      | 1          | Mochila Urbana 20L | 100,00   | 19,90  |

# ================================================================================================================= #

@CA07 @ignore
Esquema do Cenário: Cobrar frete para compras abaixo de R$ 200,00
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Então o subtotal do carrinho deve ser de R$ "<subtotal>"
  E o frete deve ser de R$ "<frete>"
  E deve ser informado que faltam R$ "<faltante>" para obter frete grátis

  Exemplos:
    | quantidade | produto             | subtotal | faltante | frete  |
    | 1          | Mochila Urbana 20L  | 100,00   | 100,00   | 19,90  |
    | 1          | Tênis Casual Urbano | 189,90   | 10,10    | 19,90  |
    | 2          | Mochila Urbana 20L  | 200,00   | 0,00     | 0,00 |

# ================================================================================================================= #

@CA08 @ignore
Esquema do Cenário: Manter frete grátis quando o desconto reduz o valor abaixo de R$ 200,00
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  E o subtotal do carrinho é de R$ "<subtotal>"
  Quando aplico o cupom "<cupom>"
  Então o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | quantidade | produto            | subtotal | cupom       | desconto | frete | total  |
    | 2          | Mochila Urbana 20L | 200,00   | BEMVINDO10  | 20,00    | 0,00  | 180,00 |

# ================================================================================================================= #

@CA09 @ignore
Esquema do Cenário: Aplicar desconto somente sobre o subtotal dos produtos
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
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

@CA10 @ignore
Esquema do Cenário: Permitir até 5 unidades do mesmo produto
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Então a quantidade do produto deve ser "<quantidade>"
  E deve ser exibida a mensagem "<mensagem>"
  E o botão de adicionar ao carrinho deve ser desabilitado
  E o subtotal do carrinho deve ser de R$ "<subtotal>"

  Exemplos:
    | quantidade | produto             | mensagem                           | subtotal |
    | 5          | Mochila Urbana 20L  | Limite de 5 unidades por produto.  | 500,00   |
    | 5          | Tênis Casual Urbano | Limite de 5 unidades por produto.  | 949,50   |

# ================================================================================================================= #

@CA11 @ignore
Esquema do Cenário: Exibir valores arredondados com duas casas decimais
  Dado que possuo <quantidade> unidades de "<produto>" no carrinho
  Quando aplico o cupom "<cupom>"
  Então o subtotal do carrinho deve ser de R$ "<subtotal>"
  E o desconto deve ser de R$ "<desconto>"
  E o frete deve ser de R$ "<frete>"
  E o total do pedido deve ser de R$ "<total>"

  Exemplos:
    | quantidade | produto             | cupom       | subtotal | desconto | frete | total  |
    | 1          | Camiseta Essencial  | BEMVINDO10  | 59,90    | 5,99     | 19,90 | 73,81  |
    | 1          | Tênis Casual Urbano | BEMVINDO10  | 189,90   | 18,99    | 19,90 | 190,81 |