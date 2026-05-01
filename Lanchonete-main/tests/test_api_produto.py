def test_put_produto_altera_valor(client):
    client.post("/produtos", json={
        "codigo": 1,
        "valor": 10,
        "tipo": 1,
        "desconto_percentual": 0
    })

    r = client.put("/produtos/1/valor", json={"novo_valor": 50})

    assert r.status_code == 200
    assert r.json() == {"alterou": True}