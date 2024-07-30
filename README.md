# fiap-tech-challenge-1

Tech Challenge da primeira fase do curso Pós-Tech - Software Architecture | FIAP

1.  Configuração

    1.1. Instale [poetry](https://python-poetry.org/docs/).

    1.2. Crie e ative um ambiente virtual

    ```shell
    $ poetry shell
    ```

    1.3. Instale as dependências

    ```shell
    $ poetry install
    ```

    A flag `--no-dev` pode ser adiconada para não instalar dependências de desenvolvimento.

    ```bash
     $ poetry install --no-dev
    ```

2.  Variaveis de ambiente

        2.1. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

    Tech Challenge da primeira fase do curso Pós-Tech - Software Architecture | FIAP

    | Variável               | Descrição                          |
    | ---------------------- | ---------------------------------- |
    | API_PORT               | Porta de acesso a API              |
    | MONGO_USERNAME         | Usuário de acesso ao Mongodb       |
    | MONGO_PASSWORD         | Senha de acesso ao Mongodb         |
    | MONGO_PORT             | Porta de acesso ao MongoDB         |
    | MONGO_EXPRESS_USERNAME | Usuário de acesso ao Mongo Express |
    | MONGO_EXPRESS_USERNAME | Senha de acesso ao Mongo Express   |

3.  Execução

    Para executar o projeto, você pode utilizar o Makefile fornecido. Certifique-se de ter o Make instalado em seu sistema.

    3.1. Build e execução do projeto

    ```shell
    $ make start-up
    ```

    Este comando irá compilar e executar o projeto.

    3.2. Limpeza do projeto

    ```shell
    $ make clean-up
    ```

    Este comando irá limpar os arquivos gerados durante a compilação.

    Certifique-se de ter as variáveis de ambiente definidas corretamente no arquivo `.env` antes de executar o projeto.
