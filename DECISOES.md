# 1. Decisões assumidas

## 1.1 Prazo padrão de empréstimo

O pedido não especifica por quanto tempo um aluno poderá permanecer com um equipamento. Assumimos que o prazo padrão de devolução será de **7 dias** para os equipamentos. Se o cliente esperasse outro prazo, seria necessário alterar o cálculo da data prevista de devolução dos empréstimos já registrados ou estabelecer um novo prazo para os próximos empréstimos.

## 1.2 Prazo de empréstimo configurável

O pedido não especifica se todos os equipamentos devem possuir obrigatoriamente o mesmo prazo de empréstimo. Assumimos que o administrador poderá **definir o prazo de devolução individualmente para cada equipamento**, utilizando 7 dias como valor padrão quando nenhum prazo específico for informado. Se o cliente esperasse um único prazo para todos os equipamentos, seria necessário remover a configuração individual e aplicar uma única regra aos empréstimos.

## 1.3 Limite padrão de equipamentos por aluno

O pedido informa que alunos com pendências não podem realizar novos empréstimos, mas não especifica se existe um limite de equipamentos que um aluno pode possuir simultaneamente. Assumimos que cada aluno poderá possuir **até 5 equipamentos emprestados simultaneamente**. Se o cliente esperasse outro limite ou nenhum limite, seria necessário alterar a validação realizada antes da criação de um empréstimo.

## 1.4 Limite de empréstimos configurável

O pedido não especifica se o limite de equipamentos por aluno deve ser fixo. Assumimos que o administrador poderá **alterar o limite máximo de equipamentos que um aluno pode possuir simultaneamente**, sendo 5 o valor padrão. Se o cliente esperasse um limite fixo para todos os alunos, seria necessário remover essa configuração administrativa.

## 1.5 Registro dos empréstimos pelo aluno

Assumimos que o aluno poderá **solicitar diretamente um equipamento disponível** por meio do menu do aluno. Caso todas as regras de negócio sejam atendidas, o empréstimo será registrado imediatamente.

Não existe uma etapa de aprovação ou confirmação do administrador. Dessa forma, uma solicitação aceita pelo sistema já resulta em um empréstimo com status **`EMPRESTADO`**.

Se o cliente esperasse que o administrador precisasse aprovar cada solicitação antes da retirada do equipamento, seria necessário criar uma etapa intermediária no fluxo.

## 1.6 Ausência de solicitações pendentes

O pedido não especifica a necessidade de um estado intermediário para solicitações de empréstimo. Assumimos que **não existirá o status** **`PENDENTE`** no sistema.

Quando o aluno solicita um equipamento e todas as regras são atendidas, o empréstimo é registrado diretamente como **`EMPRESTADO`**. Caso alguma regra não seja atendida, a solicitação é recusada e nenhum empréstimo é criado.

Se o cliente esperasse que uma solicitação aguardasse aprovação administrativa, seria necessário adicionar o status `PENDENTE` e implementar o fluxo de aprovação.

## 1.7 Controle de empréstimos ativos

Assumimos que um empréstimo será considerado **ativo enquanto possuir o status** **`EMPRESTADO`**.

Quando o administrador registrar a devolução, o status será alterado para **`DEVOLVIDO`**, fazendo com que o empréstimo deixe de ser considerado ativo.

Essa distinção é utilizada para controlar a quantidade de equipamentos emprestados, verificar pendências e determinar a disponibilidade dos equipamentos.

## 1.8 Controle de pendências

Assumimos que um aluno possuirá uma pendência quando possuir um empréstimo com status **`EMPRESTADO`** cuja data prevista de devolução seja anterior à data atual.

Enquanto possuir pelo menos um empréstimo atrasado, o aluno não poderá realizar novos empréstimos.

Empréstimos já devolvidos não geram pendência, mesmo que tenham sido devolvidos depois da data prevista.

## 1.9 Campos do relatório de atrasos

O pedido solicita que o técnico possua um relatório dos atrasos, mas não especifica quais informações devem aparecer nele. Assumimos que o relatório conterá **aluno, equipamento, data do empréstimo, data prevista de devolução e quantidade de dias de atraso**.

Se o cliente esperasse informações diferentes, seria necessário alterar os dados apresentados e a estrutura do relatório.

## 1.10 Cadastro manual dos alunos

O pedido não especifica como os alunos serão cadastrados no sistema. Assumimos que o **administrador realizará manualmente o cadastro dos alunos**, informando os dados necessários para sua identificação e autenticação.

Se o cliente esperasse integração com algum sistema acadêmico, seria necessário substituir o cadastro manual por uma integração externa.

## 1.11 Conta administrativa inicial

O pedido informa que o técnico precisa realizar operações no sistema, mas não especifica como será feita sua autenticação. Assumimos que existirá uma **conta administrativa inicial com username** **`admin`** **e senha padrão** **`admin`**.

Se o cliente esperasse autenticação integrada com outro sistema, seria necessário alterar a forma de autenticação administrativa.

## 1.12 Alteração obrigatória da senha administrativa

O pedido não especifica o comportamento da conta administrativa no primeiro acesso. Assumimos que, após entrar utilizando a senha padrão `admin`, o administrador deverá **escolher uma nova senha antes de continuar utilizando o sistema**.

Se o cliente esperasse que a senha padrão permanecesse válida permanentemente, seria necessário remover essa exigência de alteração.

## 1.13 Autenticação do aluno

O pedido não especifica quais dados serão utilizados para autenticar o aluno. Assumimos que o aluno realizará login utilizando **matrícula e senha**.

Se o cliente esperasse autenticação por outro identificador, como CPF, e-mail institucional ou integração com o sistema acadêmico, seria necessário alterar o mecanismo de autenticação.

## 1.14 Formato da matrícula

O pedido não especifica o formato das matrículas dos alunos. Assumimos que a matrícula será composta **exclusivamente por números**.

O sistema recusará uma matrícula que contenha letras ou outros caracteres. Se o cliente utilizasse matrículas alfanuméricas, seria necessário alterar a validação e o formato armazenado.

## 1.15 Formato do nome do aluno

O pedido não especifica quais caracteres podem ser utilizados no nome do aluno. Assumimos que o nome será composto por **caracteres alfabéticos e espaços**, não permitindo números no campo de nome.

Se o cliente esperasse permitir outros caracteres, seria necessário alterar a validação utilizada no cadastro.

## 1.16 Configuração dos equipamentos

O pedido informa que o sistema deve controlar os equipamentos, mas não especifica quais informações devem ser cadastradas sobre eles. Assumimos que cada equipamento possuirá **identificador, nome, categoria, quantidade, prazo de devolução e prazo para nova solicitação**.

Se o cliente esperasse outros dados ou uma estrutura diferente de cadastro, seria necessário alterar o modelo dos equipamentos e os registros já existentes.

## 1.17 Configuração da quantidade por equipamento

Assumimos que cada cadastro de equipamento poderá representar **uma quantidade de unidades do mesmo equipamento**, em vez de cada unidade física possuir obrigatoriamente um cadastro separado.

A disponibilidade será calculada considerando a quantidade cadastrada e a quantidade de unidades atualmente envolvidas em empréstimos ativos.

Se o cliente esperasse que cada unidade física tivesse seu próprio identificador e cadastro individual, seria necessário alterar o modelo de equipamentos.

## 1.18 Prazo para nova solicitação

O pedido não especifica se um equipamento que acabou de ser devolvido poderá ser imediatamente solicitado novamente. Assumimos que cada equipamento poderá possuir um **prazo para nova solicitação após uma devolução**, definido pelo administrador.

Durante esse período, novas solicitações para o equipamento serão recusadas.

Se o cliente esperasse que o equipamento pudesse ser solicitado imediatamente após a devolução, seria necessário remover essa restrição.

## 1.19 Cadastro de equipamentos

O pedido não especifica quais operações administrativas serão disponibilizadas para os equipamentos. Assumimos que o administrador poderá **cadastrar equipamentos no sistema** antes que eles sejam utilizados em empréstimos.

Se o cliente esperasse que os equipamentos fossem carregados automaticamente a partir de outro sistema, seria necessário substituir o cadastro manual por uma integração.

## 1.20 Consulta dos equipamentos

O pedido não especifica como o usuário identificará os equipamentos disponíveis para realizar uma solicitação. Assumimos que o sistema permitirá **consultar e listar os equipamentos cadastrados e suas disponibilidades**.

A listagem apresenta informações como identificador, nome, categoria, quantidade disponível e prazo de devolução.

Se o cliente esperasse que o usuário informasse diretamente o identificador do equipamento sem consultar a lista, essa operação de consulta poderia ser removida.

## 1.21 Alteração dos equipamentos

O pedido não especifica o que deve acontecer quando uma informação de um equipamento cadastrado estiver incorreta. Assumimos que o administrador poderá **alterar os dados dos equipamentos cadastrados**, permitindo corrigir informações como nome, categoria, quantidade e configurações de empréstimo.

Se o cliente esperasse que os dados fossem imutáveis após o cadastro, seria necessário remover essa operação.

## 1.22 Remoção dos equipamentos

O pedido não especifica o que deve acontecer quando o administrador tentar remover um equipamento que esteja atualmente emprestado. Assumimos que o administrador **não poderá remover um equipamento enquanto existir pelo menos um empréstimo ativo associado a ele**.

Um empréstimo ativo é aquele cujo status seja `EMPRESTADO`.

Caso o equipamento possua apenas empréstimos já devolvidos, sua remoção será permitida, pois não existe mais um vínculo ativo com um aluno.

Se o cliente esperasse permitir a remoção mesmo com equipamentos emprestados, seria necessário definir como esses empréstimos ativos seriam tratados e como o histórico seria preservado.

## 1.23 Preservação do histórico de empréstimos

Assumimos que a remoção de um equipamento não deverá apagar automaticamente o histórico de empréstimos já realizados.

Entretanto, para evitar inconsistências no sistema, um equipamento somente poderá ser removido quando **não possuir empréstimos ativos**.

Dessa forma, empréstimos já devolvidos podem continuar registrados no histórico mesmo após a remoção do equipamento.

Se o cliente esperasse que a remoção apagasse também o histórico, seria necessário definir uma política específica para exclusão dos registros relacionados.

## 1.24 Consulta dos empréstimos pelo administrador

O pedido informa que o laboratório precisa saber o que está emprestado e para quem, mas não especifica como essa informação será consultada. Assumimos que o administrador poderá **listar os empréstimos registrados**, identificando o aluno, o equipamento, o status e as datas relacionadas ao empréstimo.

A listagem considera os estados `EMPRESTADO` e `DEVOLVIDO`.

Se o cliente esperasse que essa informação estivesse disponível somente por meio do relatório de atrasos, seria necessário remover essa consulta independente.

## 1.25 Registro das devoluções

O pedido exige que o sistema controle os empréstimos e devoluções, mas não especifica quem registrará a devolução. Assumimos que o **administrador registrará manualmente a devolução de um equipamento** no sistema.

Somente empréstimos com status `EMPRESTADO` poderão receber uma devolução.

Após o registro, o empréstimo passará para o status `DEVOLVIDO`.

Se o cliente esperasse que o próprio aluno confirmasse a devolução, seria necessário alterar o fluxo da operação.

## 1.26 Atualização da disponibilidade após devolução

Assumimos que, ao registrar uma devolução, o sistema atualizará a informação de **última devolução do equipamento**.

Essa informação será utilizada para verificar o prazo configurado para uma nova solicitação.

Se o cliente esperasse que a disponibilidade fosse controlada por outro mecanismo, seria necessário alterar essa regra.

## 1.27 Consulta das devoluções pelo administrador

O pedido exige o registro das devoluções, mas não especifica se haverá histórico dessas operações. Assumimos que o administrador poderá **listar as devoluções registradas**, permitindo consultar os empréstimos que já foram encerrados e suas respectivas datas de devolução.

Se o cliente esperasse apenas o registro da devolução sem histórico consultável, essa funcionalidade seria desnecessária.

## 1.28 Alteração das devoluções

O pedido não especifica o comportamento do sistema quando uma devolução for registrada incorretamente. Assumimos que o administrador poderá **alterar a data de uma devolução já registrada**, principalmente para corrigir informações inseridas incorretamente.

A alteração somente poderá ser realizada em empréstimos que já possuam status `DEVOLVIDO`.

Se o cliente esperasse que uma devolução não pudesse ser alterada depois de registrada, seria necessário remover essa operação.

## 1.29 Consulta dos empréstimos pelo aluno

O pedido não especifica quais informações o aluno poderá consultar depois de realizar uma solicitação ou possuir um empréstimo. Assumimos que o aluno poderá **consultar seus próprios empréstimos ativos**, visualizando os equipamentos associados e as datas do empréstimo e da devolução prevista.

O aluno não poderá consultar empréstimos ativos pertencentes a outros alunos.

## 1.30 Consulta das devoluções pelo aluno

O pedido não especifica se o aluno terá acesso ao histórico de devoluções. Assumimos que o aluno poderá **consultar suas próprias devoluções**, sem acesso aos registros de outros alunos.

Se o cliente esperasse que esse histórico fosse exclusivo do administrador, seria necessário remover essa consulta da área do aluno.

## 1.31 Consulta das pendências pelo aluno

O pedido informa especificamente que o técnico precisa de um relatório dos atrasos, mas não especifica se o aluno também poderá consultar suas próprias pendências.

Assumimos que o aluno poderá **consultar se possui empréstimos em atraso**, sem acesso às pendências de outros alunos.

Essa consulta não representa um novo status de empréstimo. A pendência é determinada pela combinação entre o status `EMPRESTADO` e a data prevista de devolução já ultrapassada.

## 1.32 Interface em linha de comando

O pedido não especifica se o sistema será web, desktop ou linha de comando. Assumimos que o sistema será implementado como uma **aplicação de linha de comando (CLI)** utilizando Python.

A interface apresentará menus e receberá os dados do usuário pelo terminal.

Se o cliente esperasse uma interface gráfica ou web, seria necessário substituir a camada de apresentação, mantendo as regras de negócio e os dados do sistema.

## 1.33 Persistência dos dados

O pedido não especifica como os dados dos alunos, equipamentos, empréstimos e devoluções serão armazenados. Assumimos que os dados serão **persistidos em arquivos locais**, permitindo que as informações permaneçam disponíveis após o encerramento do programa.

Se o cliente esperasse que os dados fossem armazenados em um banco de dados compartilhado entre diferentes computadores, seria necessário substituir a camada de persistência.

---

# 2. Perguntas ao cliente

## 2.1 Quantos usuários administrativos o sistema deve possuir?

O pedido informa que o técnico precisa utilizar o sistema, mas não especifica se haverá apenas um usuário administrativo ou se diferentes técnicos poderão possuir contas próprias.

**Resposta possível 1: O sistema possuirá apenas um administrador.**

Nesse caso, o sistema poderá utilizar uma única conta administrativa para realizar operações como cadastrar equipamentos, registrar devoluções e consultar os empréstimos. A autenticação administrativa poderá ser vinculada a uma única credencial.

**Resposta possível 2: O sistema permitirá vários administradores, cada um com sua própria conta.**

Nesse caso, será necessário criar e armazenar múltiplas contas administrativas, permitindo que cada técnico possua suas próprias credenciais. A estrutura de autenticação deverá deixar de depender de uma única conta fixa e poderá ser necessário identificar qual administrador realizou cada operação.

A pergunta é relevante porque altera diretamente o modelo de autenticação e, no caso de múltiplos administradores, pode exigir o armazenamento de usuários administrativos e a associação das operações realizadas às respectivas contas.

---

## 2.2 Quais informações você gostaria que fossem colocadas no relatório dos empréstimos atrasados?

**Resposta possível 1: Somente aluno, equipamento e dias de atraso.**

Nesse caso, o relatório seria reduzido a essas informações.

**Resposta possível 2: Aluno, equipamento, data do empréstimo, data prevista de devolução e dias de atraso.**

Nesse caso, o relatório teria as informações atualmente assumidas na implementação.

**Resposta possível 3: Além dessas informações, outros dados administrativos.**

Nesse caso, seria necessário adicionar os campos solicitados à geração do relatório.

A pergunta é relevante porque altera diretamente o conteúdo e a estrutura do relatório solicitado pelo cliente.

---

## 2.3 Como deve ser realizado o cadastro dos usuários?

**Resposta possível 1: Cadastro manual pelo administrador.**

Nesse caso, o administrador continuará responsável por cadastrar os alunos no sistema.

**Resposta possível 2: Integração com o cadastro acadêmico existente.**

Nesse caso, seria necessário obter os dados dos alunos de um sistema externo, eliminando ou reduzindo o cadastro manual.

**Resposta possível 3: O próprio aluno realiza seu cadastro.**

Nesse caso, seria necessário criar uma funcionalidade de cadastro acessível aos alunos e definir regras adicionais de autenticação e validação.

A pergunta é relevante porque altera o fluxo de cadastro e a forma como os dados dos usuários entram no sistema.

---

# 3. Critérios de aceite

## 3.1 Bloqueio de empréstimo por pendência

**Entrada:** aluno cadastrado e autenticado possui um empréstimo com status `EMPRESTADO` e data prevista de devolução anterior à data atual. O aluno tenta solicitar um novo equipamento disponível.

**Resultado esperado:** o sistema recusa a solicitação com indicação de pendência, e nenhum novo registro de empréstimo é criado para o aluno.

---

## 3.2 Registro de empréstimo

**Entrada:** aluno cadastrado e autenticado, sem pendências e dentro do limite de equipamentos emprestados, solicita um equipamento com quantidade disponível maior que zero.

**Resultado esperado:** o sistema cria um novo registro de empréstimo com status `EMPRESTADO`, registra a data do empréstimo e calcula a data prevista de devolução conforme o prazo configurado para o equipamento.

---

## 3.3 Registro de devolução

**Entrada:** administrador seleciona um empréstimo existente com status `EMPRESTADO` e registra sua devolução.

**Resultado esperado:** o empréstimo passa para o status `DEVOLVIDO`, recebe a data de devolução informada e deixa de ser considerado um empréstimo ativo, aumentando novamente a quantidade disponível do equipamento.

---

# 4. Decisões da ferramenta de IA

Durante o desenvolvimento do sistema foi utilizado um assistente de IA para auxiliar na estruturação do projeto e na implementação do código. 

Uma decisão identificado no código foi a implementação da regra que **equipamentos não podem ser removidos enquanto estiverm associados a empréstimos ativos** Essa regra evita que um equipamento atualmente utilizado por um aluno seja excluído do cadastro e deixe um empréstimo ativo sem uma referência válida ao equipamento.


Uma decisão identificada no código gerado pelo assistente foi a criação de uma **conta administrativa inicial com username** **`admin`** **e senha** **`admin`**.


---

# 5. Registro de tempo

Horas escrevendo ou gerando código: **3 horas**

Horas decidindo o que o sistema deveria fazer: **3 horas e meia**

---

# 6. Declaração de uso de IA

Foi utilizado o **ChatGPT**, da OpenAI, como assistente de IA durante o desenvolvimento deste trabalho.

A ferramenta foi utilizada para auxiliar na **estruturação do projeto, organização dos arquivos, implementação de partes do código Python, elaboração e revisão da interface de linha de comando, identificação de erros durante a execução e discussão das decisões de comportamento do sistema**.

As decisões de negócio não foram consideradas automaticamente corretas apenas por terem sido sugeridas pela ferramenta. O código gerado foi analisado e testado manualmente pelo grupo, e as regras de negócio, estrutura do sistema, validações e comportamentos foram revisados antes de serem incorporados ao projeto.

A responsabilidade pela definição dos requisitos assumidos, pelas decisões registradas neste documento, pelo código entregue e pelo funcionamento final do sistema é integralmente do grupo.