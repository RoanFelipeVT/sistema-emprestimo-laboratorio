import json
import os
from datetime import datetime, timedelta

from src.models.equipamento import Equipamento


class EquipamentoService:

    def __init__(self, data_file="data/equipamentos.json"):
        self.data_file = data_file
        self.equipamentos = []
        self._carregar()

    def _carregar(self):
        if not os.path.exists(self.data_file):
            self._salvar()
            return

        with open(self.data_file, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.equipamentos = [
            Equipamento.from_dict(equipamento)
            for equipamento in dados
        ]

    def _salvar(self):
        with open(self.data_file, "w", encoding="utf-8") as arquivo:
            json.dump(
                [
                    equipamento.to_dict()
                    for equipamento in self.equipamentos
                ],
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def cadastrar(self, equipamento):
        if equipamento.quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        if equipamento.prazo_devolucao <= 0:
            raise ValueError(
                "O prazo de devolução deve ser maior que zero."
            )

        if equipamento.prazo_resolicitacao < 0:
            raise ValueError(
                "O prazo de nova solicitação não pode ser negativo."
            )

        if self.buscar_por_id(equipamento.id):
            raise ValueError(
                "Já existe um equipamento com esse ID."
            )

        self.equipamentos.append(equipamento)
        self._salvar()

    def listar(self):
        return self.equipamentos

    def buscar_por_id(self, id_equipamento):
        for equipamento in self.equipamentos:
            if equipamento.id == id_equipamento:
                return equipamento

        return None

    def alterar(
        self,
        id_equipamento,
        nome,
        categoria,
        quantidade,
        prazo_devolucao,
        prazo_resolicitacao
    ):
        equipamento = self.buscar_por_id(id_equipamento)

        if equipamento is None:
            raise ValueError("Equipamento não encontrado.")

        if quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        if prazo_devolucao <= 0:
            raise ValueError(
                "O prazo de devolução deve ser maior que zero."
            )

        if prazo_resolicitacao < 0:
            raise ValueError(
                "O prazo de nova solicitação não pode ser negativo."
            )

        equipamento.nome = nome
        equipamento.categoria = categoria
        equipamento.quantidade = quantidade
        equipamento.prazo_devolucao = prazo_devolucao
        equipamento.prazo_resolicitacao = prazo_resolicitacao

        self._salvar()

    def remover(self, id_equipamento, emprestimos):
        equipamento = self.buscar_por_id(id_equipamento)

        if equipamento is None:
            raise ValueError("Equipamento não encontrado.")

        for emprestimo in emprestimos:
            if (
                emprestimo.id_equipamento == id_equipamento
                and emprestimo.status
                in (
                    emprestimo.STATUS_SOLICITADO,
                    emprestimo.STATUS_EMPRESTADO
                )
            ):
                raise ValueError(
                    "Não é possível remover um equipamento "
                    "com empréstimo ou solicitação ativa."
                )

        self.equipamentos.remove(equipamento)
        self._salvar()

    def esta_disponivel(self, equipamento):
        if equipamento.quantidade <= 0:
            return False

        if equipamento.ultima_devolucao is None:
            return True

        data_devolucao = datetime.fromisoformat(
            equipamento.ultima_devolucao
        )

        liberacao = data_devolucao + timedelta(
            days=equipamento.prazo_resolicitacao
        )

        return datetime.now() >= liberacao

    def quantidade_disponivel(
        self,
        equipamento,
        emprestimos
    ):
        ativos = sum(
            1
            for emprestimo in emprestimos
            if (
                emprestimo.id_equipamento == equipamento.id
                and emprestimo.status
                in (
                    emprestimo.STATUS_SOLICITADO,
                    emprestimo.STATUS_EMPRESTADO
                )
            )
        )

        quantidade = equipamento.quantidade - ativos

        if not self.esta_disponivel(equipamento):
            return 0

        return max(quantidade, 0)