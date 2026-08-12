# Sistema de Empréstimo de Laboratório

Sistema desenvolvido em Python para gerenciamento de alunos, equipamentos e empréstimos de um laboratório.

## Requisitos

* Python 3.10 ou superior
* Git

O sistema não utiliza bibliotecas externas. Todas as bibliotecas utilizadas pertencem à biblioteca padrão do Python.

## Execução

### 1. Instalar o Python

Instale o Python 3.10 ou superior na máquina.

### 2. Clonar o projeto

```bash
git clone https://github.com/RoanFelipeVT/sistema-emprestimo-laboratorio.git
```

### 3. Entrar na pasta do projeto

```bash
cd sistema-emprestimo-laboratorio
```

### 4. Executar

Linux/macOS:

```bash
python3 -m src.main
```

Windows:

```bash
python -m src.main
```

O comando deve ser executado a partir da pasta raiz do projeto.

## Credenciais do administrador

O sistema possui um administrador padrão com as seguintes credenciais iniciais:

```text
Usuário: admin
Senha: admin
```

Ao inicializar o sistema pela primeira vez, o administrador deverá definir uma nova senha para substituir a senha padrão.

## Dependências

O projeto não possui dependências externas. O arquivo `requirements.txt` está vazio porque todas as funcionalidades utilizadas são fornecidas pela biblioteca padrão do Python.

## Arquivos de dados

Os arquivos necessários para a execução já estão incluídos no projeto:

```text
admin.json
data/alunos.json
data/equipamentos.json
data/emprestimos.json
```

Não é necessário instalar ou configurar um banco de dados.

## Estrutura do projeto

```text
sistema-emprestimo-laboratorio/
├── README.md
├── DECISOES.md
├── requirements.txt
├── admin.json
├── data/
│   ├── alunos.json
│   ├── equipamentos.json
│   └── emprestimos.json
└── src/
    ├── main.py
    ├── cli/
    ├── models/
    └── services/
```

## Execução em uma máquina diferente

Para executar o sistema em uma máquina diferente da utilizada durante o desenvolvimento, basta instalar o Python, clonar o repositório e executar os comandos apresentados acima.

Na primeira inicialização, utilize as credenciais padrão do administrador (`admin` / `admin`) e defina uma nova senha quando solicitado.

O projeto contém seus próprios arquivos de dados e não depende de configurações, caminhos absolutos ou arquivos existentes exclusivamente na máquina do desenvolvedor.
