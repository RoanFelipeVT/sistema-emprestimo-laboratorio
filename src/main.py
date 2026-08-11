from src.services.aluno_service import AlunoService
from src.services.equipamento_service import EquipamentoService
from src.services.emprestimo_service import EmprestimoService
from src.services.relatorio_service import RelatorioService

from src.cli.menu import Menu


def main():
    aluno_service = AlunoService()

    equipamento_service = EquipamentoService()

    emprestimo_service = EmprestimoService(
        aluno_service=aluno_service,
        equipamento_service=equipamento_service
    )

    relatorio_service = RelatorioService(
        emprestimo_service=emprestimo_service,
        aluno_service=aluno_service,
        equipamento_service=equipamento_service
    )

    menu = Menu(
        aluno_service=aluno_service,
        equipamento_service=equipamento_service,
        emprestimo_service=emprestimo_service,
        relatorio_service=relatorio_service
    )

    menu.iniciar()


if __name__ == "__main__":
    main()