import json
import os
import re

from src.models.aluno import Aluno


class AlunoService:

    def __init__(self, data_file="data/alunos.json"):
        self.data_file = data_file
        self.alunos = []
        self._carregar()

    def _carregar(self):
        if not os.path.exists(self.data_file):
            self._salvar()
            return

        with open(self.data_file, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.alunos = [
            Aluno.from_dict(aluno)
            for aluno in dados
        ]

    def _salvar(self):
        with open(self.data_file, "w", encoding="utf-8") as arquivo:
            json.dump(
                [aluno.to_dict() for aluno in self.alunos],
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def cadastrar(self, aluno):
        if not aluno.matricula.isdigit():
            raise ValueError(
                "A matrícula deve conter somente números."
            )

        if not re.fullmatch(
            r"[A-Za-zÀ-ÖØ-öø-ÿ ]+",
            aluno.nome
        ):
            raise ValueError(
                "O nome deve conter somente letras e espaços."
            )

        if self.buscar_por_matricula(aluno.matricula):
            raise ValueError(
                "Já existe um aluno com essa matrícula."
            )

        self.alunos.append(aluno)
        self._salvar()

    def autenticar(self, matricula, senha):
        aluno = self.buscar_por_matricula(matricula)

        if aluno and aluno.senha == senha:
            return aluno

        return None

    def buscar_por_matricula(self, matricula):
        for aluno in self.alunos:
            if aluno.matricula == matricula:
                return aluno

        return None

    def listar(self):
        return self.alunos