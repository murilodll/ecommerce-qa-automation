package config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;

public class DadosConfig {

    private static final JsonNode DADOS;

    static {
        try {
            ObjectMapper mapper = new ObjectMapper();

            DADOS = mapper.readTree(
                new File("../../data/dados.json")
            );

        } catch (IOException e) {
            throw new RuntimeException(
                "Erro ao carregar data/dados.json",
                e
            );
        }
    }

    public static String get(String chave) {

        JsonNode node = DADOS.get(chave);

        if (node == null) {
            throw new IllegalArgumentException(
                "Chave não encontrada no dados.json: " + chave
            );
        }

        if (!node.isTextual()) {
            throw new IllegalArgumentException(
                "A chave não contém um valor textual: " + chave
            );
        }

        return resolverVariaveis(node.asText());
    }

    private static String resolverVariaveis(String valor) {

        while (valor.contains("${")) {

            int inicio = valor.indexOf("${");
            int fim = valor.indexOf("}", inicio);

            if (fim == -1) {
                throw new IllegalArgumentException(
                    "Variável não fechada corretamente: " + valor
                );
            }

            String variavel = valor.substring(
                inicio + 2,
                fim
            );

            JsonNode nodeVariavel = DADOS.get(variavel);

            if (nodeVariavel == null) {
                throw new IllegalArgumentException(
                    "Variável não encontrada no dados.json: "
                    + variavel
                );
            }

            String valorVariavel = resolverVariaveis(
                nodeVariavel.asText()
            );

            valor = valor.replace(
                "${" + variavel + "}",
                valorVariavel
            );
        }

        return valor;
    }
}