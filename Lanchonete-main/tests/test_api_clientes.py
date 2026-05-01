# =============================================================================
# test_api_clientes.py — Testes de integração dos endpoints de clientes
# =============================================================================


def test_post_e_get_cliente(client):
    response = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert response.status_code == 200
    assert response.json()["cpf"] == "11122233344"

    response2 = client.get("/clientes/11122233344")
    assert response2.status_code == 200
    assert response2.json()["nome"] == "Cliente X"


def test_get_cliente_inexistente(client):
    response = client.get("/clientes/000")
    assert response.status_code == 404

def test_post_cliente_cpf_vazio(client):
   
    response = client.post("/clientes", json={"cpf": "", "nome": "Teste"})

    assert response.status_code == 400