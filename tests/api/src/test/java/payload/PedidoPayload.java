package payload;

import java.util.List;
import java.util.Map;

public class PedidoPayload {

  public static Map<String, Object> pedidoValido(
      String produtoId,
      int quantidade,
      String cupom) {

    return Map.of(
        "cliente", Map.of(
            "nome", "Maria Silva",
            "email", "maria@exemplo.com",
            "cep", "01310-100"),
        "itens", List.of(
            Map.of(
                "produtoId", produtoId,
                "quantidade", quantidade)),
        "cupom", cupom);
  }

  public static Map<String, Object> comCliente(
      String nome,
      String email,
      String cep,
      String produtoId,
      int quantidade,
      String cupom) {

    return Map.of(
        "cliente", Map.of(
            "nome", nome,
            "email", email,
            "cep", cep),
        "itens", List.of(
            Map.of(
                "produtoId", produtoId,
                "quantidade", quantidade)),
        "cupom", cupom);
  }

  public static Map<String, Object> comItens(
      List<Map<String, Object>> itens,
      String cupom) {

    return Map.of(
        "cliente", Map.of(
            "nome", "Maria Silva",
            "email", "maria@exemplo.com",
            "cep", "01310-100"),
        "itens", itens,
        "cupom", cupom);
  }

}