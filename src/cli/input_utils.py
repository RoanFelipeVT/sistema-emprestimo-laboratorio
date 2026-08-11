def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("O valor não pode estar vazio.")


def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()

        try:
            return int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_data(mensagem):
    while True:
        valor = input(mensagem).strip()

        try:
            from datetime import datetime

            datetime.strptime(
                valor,
                "%Y-%m-%d"
            )

            return valor

        except ValueError:
            print(
                "Data inválida. Use o formato YYYY-MM-DD."
            )


def pausar():
    input("\nPressione ENTER para continuar...")