def test_deve_adicionar_observacao(client):

    client.post(
        "/lanchonete/clientes",
        json={
            "nome": "Lucas"
        }
    )

    client.post(
        "/lanchonete/produtos",
        json={
            "nome": "X-Burger",
            "preco": 20
        }
    )

    client.post(
        "/lanchonete/pedidos",
        json={
            "cod_cliente": 1,
            "itens": [
                {
                    "cod_produto": 1,
                    "quantidade": 1
                }
            ]
        }
    )

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem cebola"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True
    assert data["mensagem"] == (
        "Observação adicionada com sucesso"
    )
def test_nao_deve_aceitar_observacao_vazia(client):

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": ""
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "Pedido não encontrado ou inválido"
    )