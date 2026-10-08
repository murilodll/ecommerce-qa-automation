package payload;

import java.util.List;
import java.util.Map;

public class CarrinhoPayload {

  public static Map<String, Object> comItem(
      String produtoId,
      int quantidade) {
    return Map.of(
        "itens", List.of(
            Map.of(
                "produtoId", produtoId,
                "quantidade", quantidade)));
  }

  public static Map<String, Object> comItens(
      List<Map<String, Object>> itens) {

    return Map.of(
        "itens", itens);
  }

  public static Map<String, Object> comItemECupom(
      String produtoId,
      int quantidade,
      String cupom) {

    return Map.of(
        "itens", List.of(
            Map.of(
                "produtoId", produtoId,
                "quantidade", quantidade)),
        "cupom", cupom);
  }

  public static Map<String, Object> comItensECupom(
      List<Map<String, Object>> itens,
      String cupom) {

    return Map.of(
        "itens", itens,
        "cupom", cupom);
  }

}