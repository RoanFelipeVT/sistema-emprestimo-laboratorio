from datetime import datetime


class RelatorioService:

    def __init__(
        self,
        emprestimo_service,
        aluno_service,
        equipamento_service
    ):
        self.emprestimo_service = emprestimo_service
        self.aluno_service = aluno_service
        self.equipamento_service = equipamento_service

    def gerar_relatorio_atrasos(self):
        hoje = datetime.now().date()
        relatorio = []

        for emprestimo in self.emprestimo_service.listar():

            if emprestimo.status != "EMPRESTADO":
                continue

            data_prevista = datetime.fromisoformat(
                emprestimo.data_prevista_devolucao
            ).date()

            if data_prevista >= hoje:
                continue

            aluno = self.aluno_service.buscar_por_matricula(
                emprestimo.matricula_aluno
            )

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    emprestimo.id_equipamento
                )
            )

            dias_atraso = (
                hoje - data_prevista
            ).days

            relatorio.append({
                "aluno": aluno.nome if aluno else "Desconhecido",
                "equipamento": (
                    equipamento.nome
                    if equipamento
                    else "Desconhecido"
                ),
                "data_emprestimo": (
                    emprestimo.data_emprestimo
                ),
                "data_prevista_devolucao": (
                    emprestimo.data_prevista_devolucao
                ),
                "dias_atraso": dias_atraso
            })

        return relatorio