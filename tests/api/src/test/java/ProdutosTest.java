import config.DadosConfig;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class ProdutosTest {

    @Test
    void deveListarProdutos() {

        String apiProdutos = DadosConfig.get("API_PRODUTOS");

        given()
        .when()
            .get(apiProdutos)
        .then()
            .statusCode(200)
            .body("$", not(empty()))
            .body("[0].id", notNullValue())
            .body("[0].nome", notNullValue())
            .body("[0].preco", notNullValue());
    }

    @Test
    void deveConsultarProdutoExistente() {

        String apiProduto = DadosConfig.get("API_PRODUTO");

        given()
            .pathParam("id", "P001")
        .when()
            .get(apiProduto)
        .then()
            .statusCode(200)
            .body("id", equalTo("P001"))
            .body("nome", notNullValue())
            .body("preco", notNullValue());
    }

    @Test
    void deveRetornarErroAoConsultarProdutoInexistente() {

    String apiProduto = DadosConfig.get("API_PRODUTO");

    given()
        .pathParam("id", "PRODUTO-INEXISTENTE")
    .when()
        .get(apiProduto)
    .then()
        .statusCode(404)
        .body(
            "erro.codigo",
            equalTo("PRODUTO_NAO_ENCONTRADO")
        )
        .body(
            "erro.mensagem",
            notNullValue()
        );
    }


}