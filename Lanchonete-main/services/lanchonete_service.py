from domain.cliente import Cliente
from domain.pedido import Pedido
from domain.produto import Produto
from repositories.memory import db


class LanchoneteService:
    """Serviço principal com as regras de negócio da lanchonete.

    Coordena operações sobre clientes, produtos e pedidos,
    delegando a persistência ao repositório em memória.
    """

    def criar_cliente(self, cpf: str, nome: str = "") -> Cliente:
        """Cria um novo cliente ou retorna o existente com o mesmo CPF."""

        if not cpf.strip():
            raise ValueError("CPF não pode ser vazio")

        if cpf in db.clientes_por_cpf:
            return db.clientes_por_cpf[cpf]

        cliente = Cliente(cpf=cpf, nome=nome)

        db.clientes_por_cpf[cpf] = cliente

        return cliente

    def obter_cliente(self, cpf: str) -> Cliente | None:
        """Busca um cliente pelo CPF."""

        return db.clientes_por_cpf.get(cpf)

    def criar_produto(
        self,
        codigo: int,
        valor: float,
        tipo: int,
        desconto_percentual: float = 0.0
    ) -> Produto:
        """Cria e persiste um novo produto."""

        produto = Produto(
            codigo=codigo,
            valor=valor,
            tipo=tipo,
            desconto_percentual=desconto_percentual
        )

        db.produtos_por_id[codigo] = produto

        return produto

    def obter_produto(self, codigo: int) -> Produto | None:
        """Busca um produto pelo código."""

        return db.produtos_por_id.get(codigo)

    def alterar_valor_produto(
        self,
        codigo: int,
        novo_valor: float
    ) -> bool:
        """Atualiza o preço base de um produto existente."""

        produto = self.obter_produto(codigo)

        if not produto:
            return False

        produto.valor = novo_valor

        return True

    def criar_pedido(
        self,
        cpf: str,
        cod_produto: int,
        qtd_max_produtos: int
    ) -> Pedido | None:
        """Cria um pedido com o primeiro produto já adicionado."""

        cliente = self.obter_cliente(cpf)

        produto = self.obter_produto(cod_produto)

        if not cliente or not produto:
            return None

        pedido = Pedido(
            cliente=cliente,
            qtd_max_produtos=qtd_max_produtos
        )

        if not pedido.adicionar_produto(produto):
            return None

        db.pedidos_por_codigo[pedido.codigo] = pedido

        return pedido

    def alterar_pedido(
        self,
        cod_pedido: int,
        cod_produto: int
    ) -> bool:
        """Adiciona um produto a um pedido existente."""

        pedido = db.pedidos_por_codigo.get(cod_pedido)

        produto = self.obter_produto(cod_produto)

        if not pedido or not produto:
            return False

        return pedido.adicionar_produto(produto)

    def finalizar_pedido(
        self,
        cod_pedido: int
    ) -> float | None:
        """Finaliza um pedido e retorna o total calculado."""

        pedido = db.pedidos_por_codigo.get(cod_pedido)

        if not pedido:
            return None

        return pedido.finalizar()

    def obter_pedido(
        self,
        cod_pedido: int
    ) -> Pedido | None:
        """Busca um pedido pelo código."""

        return db.pedidos_por_codigo.get(cod_pedido)

    def adicionar_observacao(
        self,
        cod_pedido: int,
        observacao: str
    ) -> bool:

        pedido = self.obter_pedido(cod_pedido)

        if pedido is None:
            return False

        return pedido.adicionar_observacao(
            observacao
        )

    def buscar_observacao_pedido(
        self,
        cod_pedido: int
    ):

        pedido = self.obter_pedido(cod_pedido)

        if pedido is None:
            return None

        return pedido


service = LanchoneteService()