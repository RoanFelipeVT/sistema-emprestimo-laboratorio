import json
from pathlib import Path

from src.cli.input_utils import (
    ler_texto,
    ler_inteiro,
    ler_data,
    pausar
)

from src.models.aluno import Aluno
from src.models.equipamento import Equipamento


class Menu:

    def __init__(
        self,
        aluno_service,
        equipamento_service,
        emprestimo_service,
        relatorio_service
    ):
        self.aluno_service = aluno_service
        self.equipamento_service = equipamento_service
        self.emprestimo_service = emprestimo_service
        self.relatorio_service = relatorio_service

        self.admin_file = Path("admin.json")
        self.carregar_admin()

    def carregar_admin(self):
        if not self.admin_file.exists():
            dados = {
                "username": "admin",
                "password": "admin",
                "primeiro_acesso": True
            }

            with open(
                self.admin_file,
                "w",
                encoding="utf-8"
            ) as arquivo:
                json.dump(
                    dados,
                    arquivo,
                    indent=4,
                    ensure_ascii=False
                )

        with open(
            self.admin_file,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        self.admin_username = dados["username"]
        self.admin_password = dados["password"]
        self.primeiro_acesso_admin = dados["primeiro_acesso"]

    def salvar_admin(self):
        dados = {
            "username": self.admin_username,
            "password": self.admin_password,
            "primeiro_acesso": self.primeiro_acesso_admin
        }

        with open(
            self.admin_file,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    # =========================================================
    # MENU PRINCIPAL
    # =========================================================

    def iniciar(self):
        while True:
            print("\n================================")
            print("     SISTEMA DE EMPRÉSTIMO")
            print("================================")
            print("1 - Login do aluno")
            print("2 - Login do administrador")
            print("0 - Sair")

            opcao = ler_inteiro("Opção: ")

            if opcao == 1:
                self.login_aluno()

            elif opcao == 2:
                self.login_admin()

            elif opcao == 0:
                print("Sistema encerrado.")
                break

            else:
                print("Opção inválida.")

    # =========================================================
    # LOGIN
    # =========================================================

    def login_aluno(self):
        print("\n========== LOGIN ALUNO ==========")

        matricula = ler_texto("Matrícula: ")
        senha = ler_texto("Senha: ")

        aluno = self.aluno_service.autenticar(
            matricula,
            senha
        )

        if aluno is None:
            print("Matrícula ou senha inválida.")
            pausar()
            return

        print(f"\nBem-vindo, {aluno.nome}!")

        self.menu_aluno(aluno)

    def login_admin(self):
        print("\n======= LOGIN ADMINISTRADOR =======")

        username = ler_texto("Username: ")
        senha = ler_texto("Senha: ")

        if (
            username != self.admin_username
            or senha != self.admin_password
        ):
            print("Username ou senha inválidos.")
            pausar()
            return

        if self.primeiro_acesso_admin:
            print("\nPrimeiro acesso detectado.")
            print("Você precisa definir uma nova senha.")

            while True:
                nova_senha = ler_texto("Nova senha: ")

                confirmacao = ler_texto(
                    "Confirme a nova senha: "
                )

                if nova_senha != confirmacao:
                    print("As senhas não coincidem.")
                    continue

                if not nova_senha:
                    print("A senha não pode ser vazia.")
                    continue

                if nova_senha == "admin":
                    print(
                        "A nova senha deve ser diferente "
                        "de 'admin'."
                    )
                    continue

                self.admin_password = nova_senha
                self.primeiro_acesso_admin = False

                self.salvar_admin()

                print("Senha alterada com sucesso.")
                break

        self.menu_admin()

    # =========================================================
    # MENU DO ALUNO
    # =========================================================

    def menu_aluno(self, aluno):
        while True:
            print("\n================================")
            print("          MENU DO ALUNO")
            print("================================")
            print("1 - Listar equipamentos disponíveis")
            print("2 - Solicitar equipamento")
            print("3 - Meus empréstimos")
            print("4 - Minhas devoluções")
            print("5 - Minhas pendências")
            print("0 - Sair")

            opcao = ler_inteiro("Opção: ")

            if opcao == 1:
                self.listar_equipamentos()

            elif opcao == 2:
                self.solicitar_equipamento(aluno)

            elif opcao == 3:
                self.listar_meus_emprestimos(aluno)

            elif opcao == 4:
                self.listar_minhas_devolucoes(aluno)

            elif opcao == 5:
                self.mostrar_pendencias(aluno)

            elif opcao == 0:
                break

            else:
                print("Opção inválida.")

    # =========================================================
    # MENU DO ADMINISTRADOR
    # =========================================================

    def menu_admin(self):
        while True:
            print("\n================================")
            print("    MENU DO ADMINISTRADOR")
            print("================================")
            print("1 - Cadastrar aluno")
            print("2 - Listar alunos")
            print("3 - Cadastrar equipamento")
            print("4 - Listar equipamentos")
            print("5 - Alterar equipamento")
            print("6 - Remover equipamento")
            print("7 - Listar empréstimos")
            print("8 - Registrar devolução")
            print("9 - Listar devoluções")
            print("10 - Alterar devolução")
            print("11 - Configurar limite de empréstimos")
            print("12 - Gerar relatório de atrasos")
            print("0 - Sair")

            opcao = ler_inteiro("Opção: ")

            if opcao == 1:
                self.cadastrar_aluno()

            elif opcao == 2:
                self.listar_alunos()

            elif opcao == 3:
                self.cadastrar_equipamento()

            elif opcao == 4:
                self.listar_equipamentos()

            elif opcao == 5:
                self.alterar_equipamento()

            elif opcao == 6:
                self.remover_equipamento()

            elif opcao == 7:
                self.listar_emprestimos()

            elif opcao == 8:
                self.registrar_devolucao()

            elif opcao == 9:
                self.listar_devolucoes()

            elif opcao == 10:
                self.alterar_devolucao()

            elif opcao == 11:
                self.configurar_limite()

            elif opcao == 12:
                self.gerar_relatorio()

            elif opcao == 0:
                break

            else:
                print("Opção inválida.")

    # =========================================================
    # ALUNOS
    # =========================================================

    def cadastrar_aluno(self):
        print("\n========== CADASTRO DE ALUNO ==========")

        matricula = ler_texto("Matrícula: ")
        nome = ler_texto("Nome: ")
        senha = ler_texto("Senha: ")

        aluno = Aluno(
            matricula=matricula,
            senha=senha,
            nome=nome
        )

        try:
            self.aluno_service.cadastrar(aluno)
            print("Aluno cadastrado com sucesso.")

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    def listar_alunos(self):
        alunos = self.aluno_service.listar()

        print("\n========== ALUNOS ==========")

        if not alunos:
            print("Nenhum aluno cadastrado.")
            pausar()
            return

        for aluno in alunos:
            print(
                f"Matrícula: {aluno.matricula} | "
                f"Nome: {aluno.nome}"
            )

        pausar()

    # =========================================================
    # EQUIPAMENTOS
    # =========================================================

    def listar_equipamentos(self):
        equipamentos = self.equipamento_service.listar()

        print("\n========== EQUIPAMENTOS ==========")

        if not equipamentos:
            print("Nenhum equipamento cadastrado.")
            pausar()
            return

        for equipamento in equipamentos:

            quantidade = (
                self.equipamento_service
                .quantidade_disponivel(
                    equipamento,
                    self.emprestimo_service.listar()
                )
            )

            print(
                f"ID: {equipamento.id} | "
                f"Nome: {equipamento.nome} | "
                f"Categoria: {equipamento.categoria} | "
                f"Disponíveis: "
                f"{quantidade}/{equipamento.quantidade} | "
                f"Prazo padrão de devolução: "
                f"{equipamento.prazo_devolucao} dias | "
                f"Prazo padrão para novo empréstimo: "
                f"{equipamento.prazo_resolicitacao} dias"
            )

        pausar()

    def cadastrar_equipamento(self):
        print("\n======= CADASTRO DE EQUIPAMENTO =======")

        id_equipamento = ler_inteiro("ID: ")
        nome = ler_texto("Nome: ")
        categoria = ler_texto("Categoria: ")

        while True:
            entrada_prazo = ler_texto(
                "Prazo padrão de devolução "
                "[7 dias]: "
            )

            if entrada_prazo == "":
                prazo = 7
                break

            try:
                prazo = int(entrada_prazo)

                if prazo <= 0:
                    print(
                        "O prazo deve ser maior que zero."
                    )
                    continue

                break

            except ValueError:
                print(
                    "Digite um número inteiro válido."
                )

        quantidade = ler_inteiro(
            "Quantidade: "
        )

        while True:
            entrada_requisicao = ler_texto(
                "Prazo padrão para novo empréstimo "
                "após devolução [0 dias]: "
            )

            if entrada_requisicao == "":
                prazo_resolicitacao = 0
                break

            try:
                prazo_resolicitacao = int(
                    entrada_requisicao
                )

                if prazo_resolicitacao < 0:
                    print(
                        "O prazo não pode ser negativo."
                    )
                    continue

                break

            except ValueError:
                print(
                    "Digite um número inteiro válido."
                )

        try:
            equipamento = Equipamento(
                id=id_equipamento,
                nome=nome,
                categoria=categoria,
                quantidade=quantidade,
                prazo_devolucao=prazo,
                prazo_resolicitacao=prazo_resolicitacao
            )

            self.equipamento_service.cadastrar(
                equipamento
            )

            print(
                "Equipamento cadastrado com sucesso."
            )

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    def alterar_equipamento(self):
        print("\n======= ALTERAR EQUIPAMENTO =======")

        id_equipamento = ler_inteiro(
            "ID do equipamento: "
        )

        equipamento = (
            self.equipamento_service
            .buscar_por_id(id_equipamento)
        )

        if equipamento is None:
            print("Equipamento não encontrado.")
            pausar()
            return

        nome = ler_texto(
            f"Nome [{equipamento.nome}]: "
        )

        categoria = ler_texto(
            f"Categoria [{equipamento.categoria}]: "
        )

        quantidade = ler_inteiro(
            f"Quantidade [{equipamento.quantidade}]: "
        )

        while True:
            entrada_prazo = ler_texto(
                f"Prazo padrão de devolução "
                f"[atual: {equipamento.prazo_devolucao} dias]: "
            )

            if entrada_prazo == "":
                prazo = equipamento.prazo_devolucao
                break

            try:
                prazo = int(entrada_prazo)

                if prazo <= 0:
                    print(
                        "O prazo deve ser maior que zero."
                    )
                    continue

                break

            except ValueError:
                print(
                    "Digite um número inteiro válido."
                )

        while True:
            entrada_requisicao = ler_texto(
                f"Prazo padrão para novo empréstimo "
                f"[atual: "
                f"{equipamento.prazo_resolicitacao} dias]: "
            )

            if entrada_requisicao == "":
                prazo_resolicitacao = (
                    equipamento.prazo_resolicitacao
                )
                break

            try:
                prazo_resolicitacao = int(
                    entrada_requisicao
                )

                if prazo_resolicitacao < 0:
                    print(
                        "O prazo não pode ser negativo."
                    )
                    continue

                break

            except ValueError:
                print(
                    "Digite um número inteiro válido."
                )

        try:
            self.equipamento_service.alterar(
                id_equipamento,
                nome,
                categoria,
                quantidade,
                prazo,
                prazo_resolicitacao
            )

            print("Equipamento alterado com sucesso.")

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    def remover_equipamento(self):
        print("\n======= REMOVER EQUIPAMENTO =======")

        id_equipamento = ler_inteiro(
            "ID do equipamento: "
        )

        equipamento = (
            self.equipamento_service
            .buscar_por_id(id_equipamento)
        )

        if equipamento is None:
            print("Equipamento não encontrado.")
            pausar()
            return

        print(
            f"\nEquipamento selecionado:"
            f"\nID: {equipamento.id}"
            f"\nNome: {equipamento.nome}"
            f"\nCategoria: {equipamento.categoria}"
        )

        confirmacao = ler_texto(
            "Deseja realmente remover? (s/n): "
        ).lower()

        if confirmacao != "s":
            print("Operação cancelada.")
            pausar()
            return

        try:
            self.equipamento_service.remover(
                id_equipamento,
                self.emprestimo_service.listar()
            )

            print("Equipamento removido com sucesso.")

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    # =========================================================
    # EMPRÉSTIMOS
    # =========================================================

    def solicitar_equipamento(self, aluno):
        print("\n======= SOLICITAR EQUIPAMENTO =======")

        self.listar_equipamentos()

        id_equipamento = ler_inteiro(
            "ID do equipamento: "
        )

        try:
            emprestimo = (
                self.emprestimo_service
                .solicitar(
                    aluno.matricula,
                    id_equipamento
                )
            )

            print(
                "\nEmpréstimo registrado com sucesso!"
            )

            print(
                f"ID do empréstimo: "
                f"{emprestimo.id}"
            )

            print(
                f"Data do empréstimo: "
                f"{emprestimo.data_emprestimo}"
            )

            print(
                f"Data prevista de devolução: "
                f"{emprestimo.data_prevista_devolucao}"
            )

        except ValueError as erro:
            print(
                f"\nSolicitação recusada: {erro}"
            )

        pausar()

    def listar_emprestimos(self):
        emprestimos = (
            self.emprestimo_service.listar()
        )

        print("\n======= EMPRÉSTIMOS =======")

        encontrados = False

        for emprestimo in emprestimos:

            if emprestimo.status not in (
                "EMPRESTADO",
                "DEVOLVIDO"
            ):
                continue

            encontrados = True

            aluno = (
                self.aluno_service
                .buscar_por_matricula(
                    emprestimo.matricula_aluno
                )
            )

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    emprestimo.id_equipamento
                )
            )

            print(
                f"\nID: {emprestimo.id}"
            )

            print(
                f"Aluno: {aluno.nome}"
            )

            print(
                f"Equipamento: {equipamento.nome}"
            )

            print(
                f"Status: {emprestimo.status}"
            )

            print(
                f"Data do empréstimo: "
                f"{emprestimo.data_emprestimo}"
            )

            print(
                f"Devolução prevista: "
                f"{emprestimo.data_prevista_devolucao}"
            )

            if emprestimo.data_devolucao:
                print(
                    f"Devolução: "
                    f"{emprestimo.data_devolucao}"
                )

        if not encontrados:
            print("Nenhum empréstimo registrado.")

        pausar()

    # =========================================================
    # DEVOLUÇÕES
    # =========================================================

    def registrar_devolucao(self):
        print("\n======= REGISTRAR DEVOLUÇÃO =======")

        emprestimos = [
            e
            for e in self.emprestimo_service.listar()
            if e.status == "EMPRESTADO"
        ]

        if not emprestimos:
            print("Nenhum empréstimo ativo.")
            pausar()
            return

        for emprestimo in emprestimos:

            aluno = (
                self.aluno_service
                .buscar_por_matricula(
                    emprestimo.matricula_aluno
                )
            )

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    emprestimo.id_equipamento
                )
            )

            print(
                f"ID: {emprestimo.id} | "
                f"Aluno: {aluno.nome} | "
                f"Equipamento: {equipamento.nome}"
            )

        id_emprestimo = ler_inteiro(
            "ID do empréstimo: "
        )

        try:
            self.emprestimo_service.registrar_devolucao(
                id_emprestimo
            )

            print(
                "Devolução registrada com sucesso."
            )

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    def listar_devolucoes(self):
        devolucoes = [
            e
            for e in self.emprestimo_service.listar()
            if e.status == "DEVOLVIDO"
        ]

        print("\n======= DEVOLUÇÕES =======")

        if not devolucoes:
            print("Nenhuma devolução registrada.")
            pausar()
            return

        for devolucao in devolucoes:

            aluno = (
                self.aluno_service
                .buscar_por_matricula(
                    devolucao.matricula_aluno
                )
            )

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    devolucao.id_equipamento
                )
            )

            print(
                f"\nID: {devolucao.id}"
            )

            print(
                f"Aluno: {aluno.nome}"
            )

            print(
                f"Equipamento: {equipamento.nome}"
            )

            print(
                f"Data da devolução: "
                f"{devolucao.data_devolucao}"
            )

        pausar()

    def alterar_devolucao(self):
        print("\n======= ALTERAR DEVOLUÇÃO =======")

        devolucoes = [
            e
            for e in self.emprestimo_service.listar()
            if e.status == "DEVOLVIDO"
        ]

        if not devolucoes:
            print("Nenhuma devolução registrada.")
            pausar()
            return

        for devolucao in devolucoes:
            print(
                f"ID: {devolucao.id} | "
                f"Data: {devolucao.data_devolucao}"
            )

        id_emprestimo = ler_inteiro(
            "ID da devolução: "
        )

        nova_data = ler_data(
            "Nova data de devolução (YYYY-MM-DD): "
        )

        try:
            self.emprestimo_service.alterar_devolucao(
                id_emprestimo,
                nova_data
            )

            print(
                "Devolução alterada com sucesso."
            )

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    # =========================================================
    # CONSULTAS DO ALUNO
    # =========================================================

    def listar_meus_emprestimos(self, aluno):
        emprestimos = (
            self.emprestimo_service
            .emprestimos_ativos_do_aluno(
                aluno.matricula
            )
        )

        print("\n======= MEUS EMPRÉSTIMOS =======")

        if not emprestimos:
            print(
                "Você não possui empréstimos ativos."
            )
            pausar()
            return

        for emprestimo in emprestimos:

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    emprestimo.id_equipamento
                )
            )

            print(
                f"\nID do empréstimo: "
                f"{emprestimo.id}"
            )

            print(
                f"Equipamento: "
                f"{equipamento.nome}"
            )

            print(
                f"Data do empréstimo: "
                f"{emprestimo.data_emprestimo}"
            )

            print(
                f"Devolução prevista: "
                f"{emprestimo.data_prevista_devolucao}"
            )

        pausar()

    def listar_minhas_devolucoes(self, aluno):
        devolucoes = (
            self.emprestimo_service
            .devolucoes_do_aluno(
                aluno.matricula
            )
        )

        print("\n======= MINHAS DEVOLUÇÕES =======")

        if not devolucoes:
            print(
                "Você não possui devoluções registradas."
            )
            pausar()
            return

        for devolucao in devolucoes:

            equipamento = (
                self.equipamento_service
                .buscar_por_id(
                    devolucao.id_equipamento
                )
            )

            print(
                f"\nID do empréstimo: "
                f"{devolucao.id}"
            )

            print(
                f"Equipamento: "
                f"{equipamento.nome}"
            )

            print(
                f"Data da devolução: "
                f"{devolucao.data_devolucao}"
            )

        pausar()

    def mostrar_pendencias(self, aluno):
        possui = (
            self.emprestimo_service
            .possui_pendencia(
                aluno.matricula
            )
        )

        print("\n======= MINHAS PENDÊNCIAS =======")

        if possui:
            print(
                "Você possui empréstimos em atraso."
            )
        else:
            print(
                "Você não possui empréstimos em atraso."
            )

        pausar()

    # =========================================================
    # CONFIGURAÇÃO
    # =========================================================

    def configurar_limite(self):
        print("\n======= LIMITE DE EMPRÉSTIMOS =======")

        print(
            f"Limite atual: "
            f"{self.emprestimo_service.limite_emprestimos}"
        )

        novo_limite = ler_inteiro(
            "Novo limite: "
        )

        try:
            self.emprestimo_service.configurar_limite(
                novo_limite
            )

            print("Limite atualizado.")

        except ValueError as erro:
            print(f"Erro: {erro}")

        pausar()

    # =========================================================
    # RELATÓRIO
    # =========================================================

    def gerar_relatorio(self):
        print("\n======= RELATÓRIO DE ATRASOS =======")

        relatorio = (
            self.relatorio_service
            .gerar_relatorio_atrasos()
        )

        if not relatorio:
            print(
                "Não existem empréstimos atrasados."
            )
            pausar()
            return

        for item in relatorio:

            print(
                "\n--------------------------------"
            )

            print(
                f"Aluno: {item['aluno']}"
            )

            print(
                f"Equipamento: {item['equipamento']}"
            )

            print(
                f"Data do empréstimo: "
                f"{item['data_emprestimo']}"
            )

            print(
                f"Data prevista de devolução: "
                f"{item['data_prevista_devolucao']}"
            )

            print(
                f"Dias de atraso: "
                f"{item['dias_atraso']}"
            )

        pausar()