import config.DadosConfig;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import payload.PedidoPayload;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import java.util.List;
import java.util.Map;

class PedidosTest {

  @Test
  void deveCriarPedidoValido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "P005",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(201)
        .body("numero", matchesPattern("VZ-\\d{6}"))
        .body("criadoEm", notNullValue())
        .body("cliente.nome", equalTo("Maria Silva"))
        .body("cliente.email", equalTo("maria@exemplo.com"))
        .body("cliente.cep", equalTo("01310100"))
        .body("subtotal", equalTo(100))
        .body("desconto", equalTo(10))
        .body("frete", equalTo(19.9F))
        .body("freteGratis", equalTo(false))
        .body("valorFaltanteFreteGratis", equalTo(100))
        .body("total", equalTo(109.9F))
        .body("cupom.codigo", equalTo("BEMVINDO10"))
        .body("cupom.aplicado", equalTo(true));
  }

  @Test
  void deveRetornarErroQuandoNomeNaoPossuirSobrenome() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.comCliente(
        "Maria",
        "maria@exemplo.com",
        "01310-100",
        "P001",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("DADOS_INVALIDOS"))
        .body("erro.mensagem", notNullValue())
        .body("erro.campos[0].campo", equalTo("cliente.nome"))
        .body("erro.campos[0].mensagem", equalTo("Informe nome e sobrenome."));
  }

  @Test
  void deveRetornarErroQuandoEmailForInvalido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.comCliente(
        "Maria Silva",
        "email-invalido",
        "01310-100",
        "P001",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("DADOS_INVALIDOS"))
        .body("erro.mensagem", notNullValue())
        .body("erro.campos[0].campo", equalTo("cliente.email"))
        .body("erro.campos[0].mensagem", equalTo("Informe um e-mail válido."));
  }

  @Test
  void deveRetornarErroQuandoCepForInvalido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.comCliente(
        "Maria Silva",
        "maria@exemplo.com",
        "12345",
        "P001",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("DADOS_INVALIDOS"))
        .body("erro.mensagem", notNullValue())
        .body("erro.campos[0].campo", equalTo("cliente.cep"))
        .body("erro.campos[0].mensagem", equalTo("Informe um CEP com 8 dígitos."));
  }

  @Test
  void deveRetornarErroQuandoCupomForInvalido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "P001",
        1,
        "CUPOMINVALIDO");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("CUPOM_INVALIDO"))
        .body("erro.mensagem", equalTo("Cupom inválido."))
        .body("erro.campo", equalTo("cupom"));
  }

  @Test
  void deveRetornarErroQuandoCupomEstiverExpirado() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "P001",
        1,
        "VERAO2026");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("CUPOM_EXPIRADO"))
        .body("erro.mensagem", equalTo("Cupom expirado."))
        .body("erro.campo", equalTo("cupom"));
  }

  @Test
  @Tag("known-bug")
  void deveRetornarErroQuandoQuantidadeExcederMaximo() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "P001",
        6,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body(
            "erro.codigo",
            equalTo("QUANTIDADE_MAXIMA_EXCEDIDA"))
        .body(
            "erro.campo",
            equalTo("itens[0].quantidade"));
  }

  @Test
  void deveRetornarErroQuandoQuantidadeForZero() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "P001",
        0,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("QUANTIDADE_INVALIDA"))
        .body(
            "erro.mensagem",
            equalTo("A quantidade deve ser um número inteiro maior ou igual a 1."))
        .body(
            "erro.campo",
            equalTo("itens[0].quantidade"));
  }

  @Test
  void deveRetornarErroQuandoProdutoNaoExistir() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.pedidoValido(
        "PRODUTO-INEXISTENTE",
        1,
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("PRODUTO_NAO_ENCONTRADO"))
        .body(
            "erro.mensagem",
            equalTo("Produto PRODUTO-INEXISTENTE não encontrado."))
        .body(
            "erro.campo",
            equalTo("itens[0].produtoId"));
  }

  @Test
  void deveRetornarErroQuandoProdutoEstiverDuplicado() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = PedidoPayload.comItens(
        List.of(
            Map.of(
                "produtoId", "P001",
                "quantidade", 1),
            Map.of(
                "produtoId", "P001",
                "quantidade", 1)),
        "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("ITEM_DUPLICADO"))
        .body(
            "erro.mensagem",
            equalTo("O produto P001 aparece mais de uma vez."))
        .body(
            "erro.campo",
            equalTo("itens[1].produtoId"));
  }

  @Test
  void deveRetornarErroQuandoJsonForInvalido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    String jsonInvalido = """
        {
            "cliente": {
                "nome": "Maria Silva"
        """;

    given()
        .contentType("application/json")
        .body(jsonInvalido)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(400)
        .body("erro.codigo", equalTo("JSON_INVALIDO"))
        .body(
            "erro.mensagem",
            equalTo("O corpo da requisição deve ser um objeto JSON válido."));
  }

  @Test
  void deveRetornarErroQuandoMetodoNaoForPermitido() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    given()
        .when()
        .get(apiPedidos)
        .then()
        .statusCode(405)
        .body("erro.codigo", equalTo("METODO_NAO_PERMITIDO"))
        .body(
            "erro.mensagem",
            equalTo("O método GET não é permitido nesta rota."));
  }

  @Test
  void deveRetornarErroQuandoRotaNaoExistir() {

    String baseUrl = DadosConfig.get("BASE_URL");

    given()
        .when()
        .get(baseUrl + "/api/rota-inexistente")
        .then()
        .statusCode(404)
        .body("erro.codigo", equalTo("ROTA_NAO_ENCONTRADA"))
        .body("erro.mensagem", equalTo("Rota não encontrada."));
  }

  @Test
  void deveRetornarErroQuandoItensNaoForemInformados() {

    String apiPedidos = DadosConfig.get("API_PEDIDOS");

    var body = Map.of(
        "cliente", Map.of(
            "nome", "Maria Silva",
            "email", "maria@exemplo.com",
            "cep", "01310-100"),
        "cupom", "BEMVINDO10");

    given()
        .contentType("application/json")
        .body(body)
        .when()
        .post(apiPedidos)
        .then()
        .statusCode(422)
        .body("erro.codigo", equalTo("ITENS_OBRIGATORIOS"))
        .body("erro.mensagem", equalTo("Informe ao menos um item."))
        .body("erro.campo", equalTo("itens"));
  }

}