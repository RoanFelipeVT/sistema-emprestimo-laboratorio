class Equipamento:
    def __init__(
        self,
        id,
        nome,
        categoria,
        quantidade,
        prazo_devolucao=7,
        prazo_resolicitacao=0
    ):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.prazo_devolucao = prazo_devolucao
        self.prazo_resolicitacao = prazo_resolicitacao
        self.ultima_devolucao = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "quantidade": self.quantidade,
            "prazo_devolucao": self.prazo_devolucao,
            "prazo_resolicitacao": self.prazo_resolicitacao,
            "ultima_devolucao": self.ultima_devolucao
        }

    @classmethod
    def from_dict(cls, data):
        equipamento = cls(
            id=data["id"],
            nome=data["nome"],
            categoria=data["categoria"],
            quantidade=data["quantidade"],
            prazo_devolucao=data.get("prazo_devolucao", 7),
            prazo_resolicitacao=data.get("prazo_resolicitacao", 0)
        )

        equipamento.ultima_devolucao = data.get("ultima_devolucao")

        return equipamento