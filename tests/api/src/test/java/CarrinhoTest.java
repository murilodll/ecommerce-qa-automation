import config.DadosConfig;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import payload.CarrinhoPayload;
import payload.PedidoPayload;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import java.util.List;
import java.util.Map;

class CarrinhoTest {

  @Test
  void deveCalcularCarrinhoComItemValido() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("P001", 1);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(59.9F))
        .body("desconto", equalTo(0))
        .body("frete", equalTo(19.9F))
        .body("freteGratis", equalTo(false))
        .body("valorFaltanteFreteGratis", equalTo(140.1F))
        .body("total", equalTo(79.8F));
  }

  @Test
  @Tag("known-bug")
  void deveRetornarErroQuandoQuantidadeExcederMaximo() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("P001", 6);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(422)
        .body(
            "erro.codigo",
            equalTo("QUANTIDADE_MAXIMA_EXCEDIDA"))
        .body(
            "erro.mensagem",
            notNullValue());
  }

  @Test
  void deveRetornarErroQuandoQuantidadeForZero() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("P001", 0);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(422)
        .body(
            "erro.codigo",
            equalTo("QUANTIDADE_INVALIDA"))
        .body(
            "erro.mensagem",
            notNullValue());
  }

  @Test
  void deveRetornarErroQuandoProdutoNaoExistir() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("PRODUTO-INEXISTENTE", 1);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(422)
        .body(
            "erro.codigo",
            equalTo("PRODUTO_NAO_ENCONTRADO"))
        .body(
            "erro.mensagem",
            notNullValue());
  }

  @Test
  void deveRetornarErroQuandoProdutoEstiverDuplicado() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItens(
        List.of(
            Map.of(
                "produtoId", "P001",
                "quantidade", 1),
            Map.of(
                "produtoId", "P001",
                "quantidade", 1)));

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(422)
        .body(
            "erro.codigo",
            equalTo("ITEM_DUPLICADO"))
        .body(
            "erro.mensagem",
            notNullValue());
  }

  @Test
  void deveAplicarFreteGratisQuandoSubtotalForMaiorQueDuzentos() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("P001", 4);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(239.6F))
        .body("desconto", equalTo(0))
        .body("frete", equalTo(0))
        .body("freteGratis", equalTo(true))
        .body("valorFaltanteFreteGratis", equalTo(0))
        .body("total", equalTo(239.6F));
  }

  @Test
  @Tag("known-bug")
  void deveAplicarFreteGratisQuandoSubtotalForExatamenteDuzentos() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItem("P005", 2);

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(200))
        .body("desconto", equalTo(0))
        .body("frete", equalTo(0))
        .body("freteGratis", equalTo(true))
        .body("valorFaltanteFreteGratis", equalTo(0))
        .body("total", equalTo(200));
  }

  @Test
  void deveAplicarDezPorCentoDeDescontoComCupomBemVindo10() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItemECupom(
        "P001",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(59.9F))
        .body("desconto", equalTo(5.99F))
        .body("frete", equalTo(19.9F))
        .body("freteGratis", equalTo(false))
        .body("total", equalTo(73.81F))
        .body("cupom.codigo", equalTo("BEMVINDO10"))
        .body("cupom.aplicado", equalTo(true))
        .body("cupom.mensagem", notNullValue());
  }

  @Test
  void deveAceitarCupomIgnorandoMaiusculasMinusculasEEspacos() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItemECupom(
        "P001",
        1,
        "  bemvindo10  ");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(59.9F))
        .body("desconto", equalTo(5.99F))
        .body("frete", equalTo(19.9F))
        .body("total", equalTo(73.81F))
        .body("cupom.codigo", equalTo("BEMVINDO10"))
        .body("cupom.aplicado", equalTo(true));
  }

  @Test
  void naoDeveAplicarDescontoComCupomInvalido() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItemECupom(
        "P001",
        1,
        "CUPOMINVALIDO");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(59.9F))
        .body("desconto", equalTo(0))
        .body("frete", equalTo(19.9F))
        .body("total", equalTo(79.8F))
        .body("cupom.aplicado", equalTo(false))
        .body("cupom.mensagem", notNullValue());
  }

  @Test
  void naoDeveAplicarDescontoComCupomExpirado() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItemECupom(
        "P001",
        1,
        "VERAO2026");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(59.9F))
        .body("desconto", equalTo(0))
        .body("frete", equalTo(19.9F))
        .body("total", equalTo(79.8F))
        .body("cupom.codigo", equalTo("VERAO2026"))
        .body("cupom.aplicado", equalTo(false))
        .body("cupom.mensagem", equalTo("Cupom expirado."));
  }

  @Test
  void deveCalcularFreteGratisComBaseNoSubtotalAntesDoDesconto() {

    String apiCarrinho = DadosConfig.get("API_CARRINHO");

    var body = CarrinhoPayload.comItensECupom(
        List.of(
            Map.of(
                "produtoId", "P003",
                "quantidade", 1),
            Map.of(
                "produtoId", "P006",
                "quantidade", 1)),
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiCarrinho)
        .then()
        .statusCode(200)
        .body("subtotal", equalTo(219.8F))
        .body("desconto", equalTo(21.98F))
        .body("frete", equalTo(0))
        .body("freteGratis", equalTo(true))
        .body("total", equalTo(197.82F))
        .body("cupom.aplicado", equalTo(true));
  }

  @Test
  void deveRetornarErroQuandoItemForInvalido() {
    Map<String, Object> body = Map.of(
        "itens", List.of("item-invalido"));

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(DadosConfig.get("API_CARRINHO"))
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("ITEM_INVALIDO"));
  }

  @Test
  void deveCriarPedidoComCepSemHifen() {
    Map<String, Object> body = PedidoPayload.comCliente(
        "Maria Silva",
        "maria@exemplo.com",
        "01310100",
        "P005",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(DadosConfig.get("API_PEDIDOS"))
        .then()
        .statusCode(201)
        .body("cliente.cep", equalTo("01310100"));
  }

}