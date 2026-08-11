class Aluno:
    def __init__(self, matricula, senha, nome):
        self.matricula = matricula
        self.senha = senha
        self.nome = nome

    def to_dict(self):
        return {
            "matricula": self.matricula,
            "senha": self.senha,
            "nome": self.nome
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            matricula=data["matricula"],
            senha=data["senha"],
            nome=data["nome"]
        )