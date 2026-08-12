# src/services/emprestimo_service.py

import json
import os
from datetime import datetime, timedelta

from src.models.emprestimo import Emprestimo


class EmprestimoService:

    LIMITE_PADRAO = 5

    def __init__(
        self,
        aluno_service,
        equipamento_service,
        data_file="data/emprestimos.json"
    ):
        self.aluno_service = aluno_service
        self.equipamento_service = equipamento_service
        self.data_file = data_file

        self.emprestimos = []
        self.limite_emprestimos = self.LIMITE_PADRAO

        self._carregar()

    # =========================
    # PERSISTÊNCIA
    # =========================

    def _carregar(self):
        if not os.path.exists(self.data_file):
            self._salvar()
            return

        with open(
            self.data_file,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        self.emprestimos = [
            Emprestimo.from_dict(emprestimo)
            for emprestimo in dados
        ]

    def _salvar(self):
        diretorio = os.path.dirname(self.data_file)

        if diretorio:
            os.makedirs(
                diretorio,
                exist_ok=True
            )

        with open(
            self.data_file,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                [
                    emprestimo.to_dict()
                    for emprestimo in self.emprestimos
                ],
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    # =========================
    # UTILITÁRIOS
    # =========================

    def _proximo_id(self):
        if not self.emprestimos:
            return 1

        return max(
            emprestimo.id
            for emprestimo in self.emprestimos
        ) + 1

    def buscar_por_id(self, id_emprestimo):
        for emprestimo in self.emprestimos:
            if emprestimo.id == id_emprestimo:
                return emprestimo

        return None

    def listar(self):
        return self.emprestimos

    # =========================
    # PENDÊNCIAS
    # =========================

    def possui_pendencia(self, matricula):
        hoje = datetime.now().date()

        for emprestimo in self.emprestimos:

            if (
                emprestimo.matricula_aluno == matricula
                and emprestimo.status
                == Emprestimo.STATUS_EMPRESTADO
                and emprestimo.data_prevista_devolucao
            ):
                data_prevista = datetime.fromisoformat(
                    emprestimo.data_prevista_devolucao
                ).date()

                if data_prevista < hoje:
                    return True

        return False

    def emprestimos_atrasados_do_aluno(self, matricula):
        hoje = datetime.now().date()
        atrasados = []

        for emprestimo in self.emprestimos:

            if (
                emprestimo.matricula_aluno == matricula
                and emprestimo.status
                == Emprestimo.STATUS_EMPRESTADO
                and emprestimo.data_prevista_devolucao
            ):
                data_prevista = datetime.fromisoformat(
                    emprestimo.data_prevista_devolucao
                ).date()

                if data_prevista < hoje:
                    atrasados.append(emprestimo)

        return atrasados

    # =========================
    # EMPRÉSTIMOS ATIVOS
    # =========================

    def quantidade_ativos(self, matricula):
        return sum(
            1
            for emprestimo in self.emprestimos
            if (
                emprestimo.matricula_aluno == matricula
                and emprestimo.status
                == Emprestimo.STATUS_EMPRESTADO
            )
        )

    def emprestimos_ativos_do_aluno(self, matricula):
        return [
            emprestimo
            for emprestimo in self.emprestimos
            if (
                emprestimo.matricula_aluno == matricula
                and emprestimo.status
                == Emprestimo.STATUS_EMPRESTADO
            )
        ]

    def possui_emprestimo_ativo_para_equipamento(
        self,
        id_equipamento
    ):
        return any(
            emprestimo.id_equipamento == id_equipamento
            and emprestimo.status
            == Emprestimo.STATUS_EMPRESTADO
            for emprestimo in self.emprestimos
        )

    # =========================
    # SOLICITAÇÃO DE EQUIPAMENTO
    # =========================

    def solicitar(
        self,
        matricula,
        id_equipamento
    ):
        aluno = (
            self.aluno_service
            .buscar_por_matricula(matricula)
        )

        if aluno is None:
            raise ValueError(
                "Aluno não encontrado."
            )

        if self.possui_pendencia(matricula):
            raise ValueError(
                "Aluno possui empréstimo em atraso."
            )

        if (
            self.quantidade_ativos(matricula)
            >= self.limite_emprestimos
        ):
            raise ValueError(
                f"O aluno já atingiu o limite de "
                f"{self.limite_emprestimos} equipamentos."
            )

        equipamento = (
            self.equipamento_service
            .buscar_por_id(id_equipamento)
        )

        if equipamento is None:
            raise ValueError(
                "Equipamento não encontrado."
            )

        quantidade_disponivel = (
            self.equipamento_service
            .quantidade_disponivel(
                equipamento,
                self.emprestimos
            )
        )

        if quantidade_disponivel <= 0:
            raise ValueError(
                "Equipamento indisponível."
            )

        if equipamento.ultima_devolucao:

            ultima_devolucao = datetime.fromisoformat(
                equipamento.ultima_devolucao
            )

            agora = datetime.now()

            prazo_requisicao = timedelta(
                days=equipamento.prazo_resolicitacao
            )

            limite_requisicao = (
                ultima_devolucao
                + prazo_requisicao
            )

            if agora < limite_requisicao:
                raise ValueError(
                    "O equipamento ainda está dentro "
                    "do prazo para nova solicitação."
                )

        agora = datetime.now()

        data_prevista = (
            agora
            + timedelta(
                days=equipamento.prazo_devolucao
            )
        )

        emprestimo = Emprestimo(
            id=self._proximo_id(),
            matricula_aluno=matricula,
            id_equipamento=id_equipamento,
            data_emprestimo=agora.isoformat(),
            data_prevista_devolucao=(
                data_prevista.isoformat()
            ),
            status=Emprestimo.STATUS_EMPRESTADO
        )

        self.emprestimos.append(
            emprestimo
        )

        self._salvar()

        return emprestimo

    # =========================
    # DEVOLUÇÕES
    # =========================

    def registrar_devolucao(
        self,
        id_emprestimo,
        data_devolucao=None
    ):
        emprestimo = self.buscar_por_id(
            id_emprestimo
        )

        if emprestimo is None:
            raise ValueError(
                "Empréstimo não encontrado."
            )

        if (
            emprestimo.status
            != Emprestimo.STATUS_EMPRESTADO
        ):
            raise ValueError(
                "Esse empréstimo não está ativo."
            )

        if data_devolucao is None:
            data_devolucao = datetime.now()

        emprestimo.data_devolucao = (
            data_devolucao.isoformat()
        )

        emprestimo.status = (
            Emprestimo.STATUS_DEVOLVIDO
        )

        equipamento = (
            self.equipamento_service
            .buscar_por_id(
                emprestimo.id_equipamento
            )
        )

        if equipamento:

            equipamento.ultima_devolucao = (
                data_devolucao.isoformat()
            )

            self.equipamento_service._salvar()

        self._salvar()

        return emprestimo

    def alterar_devolucao(
        self,
        id_emprestimo,
        nova_data
    ):
        emprestimo = self.buscar_por_id(
            id_emprestimo
        )

        if emprestimo is None:
            raise ValueError(
                "Empréstimo não encontrado."
            )

        if (
            emprestimo.status
            != Emprestimo.STATUS_DEVOLVIDO
        ):
            raise ValueError(
                "O empréstimo ainda não foi devolvido."
            )

        try:
            data = datetime.fromisoformat(
                nova_data
            )

        except ValueError:
            raise ValueError(
                "Data inválida. Use o formato YYYY-MM-DD."
            )

        emprestimo.data_devolucao = (
            data.isoformat()
        )

        equipamento = (
            self.equipamento_service
            .buscar_por_id(
                emprestimo.id_equipamento
            )
        )

        if equipamento:

            equipamento.ultima_devolucao = (
                data.isoformat()
            )

            self.equipamento_service._salvar()

        self._salvar()

    # =========================
    # CONSULTAS
    # =========================

    def devolucoes_do_aluno(self, matricula):
        return [
            emprestimo
            for emprestimo in self.emprestimos
            if (
                emprestimo.matricula_aluno == matricula
                and emprestimo.status
                == Emprestimo.STATUS_DEVOLVIDO
            )
        ]

    # =========================
    # CONFIGURAÇÕES
    # =========================

    def configurar_limite(self, limite):
        if limite <= 0:
            raise ValueError(
                "O limite deve ser maior que zero."
            )

        self.limite_emprestimos = limite