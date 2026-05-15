def test_deve_adicionar_observacao(client):

    # cria cliente
    client.post(
        "/clientes",
        json={
            "cpf": "11122233344",
            "nome": "Cliente Teste"
        }
    )

    # cria produto
    client.post(
        "/produtos",
        json={
            "codigo": 1,
            "valor": 20,
            "tipo": 1,
            "desconto_percentual": 0
        }
    )

    # cria pedido
    client.post(
        "/lanchonete/pedidos",
        json={
            "cpf": "11122233344",
            "cod_produto": 1,
            "qtd_max_produtos": 10
        }
    )

    # adiciona observação
    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem cebola"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True
    assert data["mensagem"] == "Observação adicionada com sucesso"
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