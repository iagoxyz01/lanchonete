# =============================================================================
# test_api_pedidos.py — Teste de integração do fluxo completo de pedidos
# =============================================================================

def test_fluxo_completo_pedido(client):
    """Simula o ciclo de vida completo de um pedido via API."""

    # 1. Cria o cliente
    r_cliente = client.post("/clientes", json={
        "cpf": "11122233344",
        "nome": "Cliente X"
    })
    assert r_cliente.status_code == 200

    # 2. Cria os produtos
    r_prod1 = client.post("/produtos", json={
        "codigo": 1,
        "valor": 10,
        "tipo": 1,
        "desconto_percentual": 10
    })
    assert r_prod1.status_code == 200

    r_prod2 = client.post("/produtos", json={
        "codigo": 2,
        "valor": 20,
        "tipo": 2,
        "desconto_percentual": 10
    })
    assert r_prod2.status_code == 200

    # 3. Cria o pedido
    r = client.post("/lanchonete/pedidos", json={
        "cpf": "11122233344",
        "cod_produto": 1,
        "qtd_max_produtos": 10
    })
    assert r.status_code == 200

    cod_pedido = r.json()["codigo"]

    # valida estrutura básica da resposta
    assert "codigo" in r.json()
    assert isinstance(cod_pedido, int)

    # 4. Adiciona mais um item
    r2 = client.put(
        f"/lanchonete/pedidos/{cod_pedido}/itens",
        json={"cod_produto": 2}
    )
    assert r2.status_code == 200

    # 5. Busca o pedido antes de finalizar (extra - deixa o teste mais completo)
    r_get = client.get(f"/lanchonete/pedidos/{cod_pedido}")
    assert r_get.status_code == 200
    assert r_get.json()["codigo"] == cod_pedido
    assert len(r_get.json()["produtos"]) == 2

    # 6. Finaliza o pedido
    r3 = client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")
    assert r3.status_code == 200

    # valida o total
    assert r3.json()["total"] == 29.0

    # 7. Busca novamente após finalizar (garante consistência)
    r_final = client.get(f"/lanchonete/pedidos/{cod_pedido}")
    assert r_final.status_code == 200
    assert r_final.json()["codigo"] == cod_pedido
    assert len(r_final.json()["produtos"]) == 2
    #iago