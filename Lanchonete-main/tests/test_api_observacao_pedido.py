def test_deve_adicionar_observacao(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem cebola"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # TODO: validar retorno

def test_nao_deve_aceitar_observacao_vazia(client):
    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": ""
        }
    )

    # TODO: validar erro


def test_nao_deve_adicionar_observacao_em_pedido_finalizado(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: finalizar pedido

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem molho"
        }
    )

    # TODO: validar erro

def test_deve_buscar_observacao_pedido(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: adicionar observação

    response = client.get(
        "/lanchonete/pedidos/1/observacao"
    )

    assert response.status_code == 200

    data = response.json()

    # TODO: validar observação