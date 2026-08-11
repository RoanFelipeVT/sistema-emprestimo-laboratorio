class Emprestimo:
    STATUS_SOLICITADO = "SOLICITADO"
    STATUS_EMPRESTADO = "EMPRESTADO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"

    def __init__(
        self,
        id,
        matricula_aluno,
        id_equipamento,
        data_emprestimo,
        data_prevista_devolucao,
        status=STATUS_SOLICITADO,
        data_devolucao=None
    ):
        self.id = id
        self.matricula_aluno = matricula_aluno
        self.id_equipamento = id_equipamento
        self.data_emprestimo = data_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao
        self.status = status
        self.data_devolucao = data_devolucao

    def to_dict(self):
        return {
            "id": self.id,
            "matricula_aluno": self.matricula_aluno,
            "id_equipamento": self.id_equipamento,
            "data_emprestimo": self.data_emprestimo,
            "data_prevista_devolucao": self.data_prevista_devolucao,
            "status": self.status,
            "data_devolucao": self.data_devolucao
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            matricula_aluno=data["matricula_aluno"],
            id_equipamento=data["id_equipamento"],
            data_emprestimo=data["data_emprestimo"],
            data_prevista_devolucao=data["data_prevista_devolucao"],
            status=data.get("status", cls.STATUS_EMPRESTADO),
            data_devolucao=data.get("data_devolucao")
        )