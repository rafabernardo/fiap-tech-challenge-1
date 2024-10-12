# fiap-tech-challenge

# Tech Challenge do curso Pós-Tech - Software Architecture | FIAP

## Sobre o Projeto

Este projeto é uma API RESTful desenvolvida em Python utilizando o framework FastAPI e banco de dados MongoDB. Criado utilizando os principais conceitos de arquitetura de software, como SOLID, DDD e Clean Architecture.

## Event Storming

Para visualizar o diagrama criado a partir dos eventos, consulte o [board no Miro](https://shorturl.at/3xRZ9).

## Requisitos Funcionais do Projeto

### 1. Identificação do Cliente

- **RF1.1**: O sistema deve oferecer a opção de cadastro com nome e e-mail.
- **RF1.2**: O sistema deve permitir que o cliente se identifique através do CPF.
- **RF1.3**: O sistema deve permitir que o cliente faça pedidos sem se identificar.

### 2. Seleção de Produtos

- **RF2.1**: O sistema deve apresentar os produtos disponíveis, categorizados em Lanche, Acompanhamento, Bebida e Sobremesa.
- **RF2.2**: Para cada produto, o sistema deve exibir nome, descrição e preço.
- **RF2.3**: O sistema deve adicionar os produtos seguindo a seguinte sequência de categorias: Lanche > Acompanhamento > Bebida > Sobremesa.
- **RF2.4**: O sistema deve permitir que o cliente pule a sequência acima, sendo todas elas opcionais.

### 3. Finalização do Pedido

- **RF3.1**: O sistema deve confirmar o recebimento do pagamento antes de processar o pedido.
- **RF3.2**: O sistema deve notificar a cozinha após a confirmação de pagamento.

### 4. Acompanhamento do Pedido

- **RF4.1**: O sistema deve exibir o status atual do pedido (Recebido, Em preparação, Pronto, Finalizado).
- **RF4.2**: O sistema deve atualizar o status do pedido em tempo real.
- **RF4.3**: O sistema deve notificar o cliente quando o pedido estiver pronto para retirada.

### 5. Gerenciamento de Produtos

- **RF5.1**: O sistema deve permitir cadastrar novos produtos, especificando nome, descrição, preço, categoria e imagem.
- **RF5.2**: O sistema deve permitir editar informações de produtos existentes.

### 6. Gerenciamento de Pedidos

- **RF6.1**: O sistema deve exibir uma lista de pedidos em andamento, ordenados por Recebido, Em preparação, Pronto e em ordem decrescente de criação.
- **RF6.2**: O sistema deve permitir atualizar o status de cada pedido.
- **RF6.3**: O sistema deve fornecer tempo de espera do pedido.

## Configuração

1. Instale [Poetry](https://python-poetry.org/docs/).
2. Crie e ative um ambiente virtual:

   ```shell
   poetry shell
   ```

3. Instale as dependências:

   ```shell
   poetry install
   ```

   A flag `--no-dev` pode ser adicionada para não instalar dependências de desenvolvimento:

   ```shell
   poetry install --no-dev
   ```

## Variáveis de Ambiente

1. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

   | Variável               | Descrição                          | Exemplo       |
   | ---------------------- | ---------------------------------- | ------------- |
   | API_PORT               | Porta de acesso à API              | 8000          |
   | MONGO_URL              | URL de acesso ao MongoDB           | localhost     |
   | MONGO_PORT             | Porta de acesso ao MongoDB         | 27017         |
   | MONGO_DATABASE         | Database utilizada no MongoDB      | database_test |
   | MONGO_USERNAME         | Usuário de acesso ao MongoDB       | user          |
   | MONGO_PASSWORD         | Senha de acesso ao MongoDB         | pass          |
   | MONGO_EXPRESS_USERNAME | Usuário de acesso ao Mongo Express | user          |
   | MONGO_EXPRESS_PASSWORD | Senha de acesso ao Mongo Express   | pass          |

## Execução

Para executar o projeto, utilize o Makefile fornecido. Certifique-se de ter o Make instalado em seu sistema.

1. Build e execução do projeto:

   ```shell
   make start-up
   ```

   Este comando irá compilar e executar o projeto.

2. Limpeza do projeto:

   ```shell
   make clean-up
   ```

   Este comando irá limpar os arquivos gerados durante a compilação.

Certifique-se de ter as variáveis de ambiente definidas corretamente no arquivo `.env` antes de executar o projeto.

## Documentação da API

A documentação da API pode ser acessada quando o projeto estiver em execução em `/docs` no navegador.

## Endpoints

### Users

- **[GET] /v1/users**: Lista todos os usuários.
- **[GET] /v1/users/{id}**: Obtém um usuário pelo ID.
- **[GET] /v1/users/cpf/{cpf}**: Obtém um usuário pelo CPF.
- **[POST] /v1/users/register**: Registra um novo usuário.
- **[DELETE] /v1/users/delete/{id}**: Deleta um usuário pelo ID.
- **[PATCH] /v1/users/identify/{id}**: Identifica um usuário pelo CPF usando seu ID.

### Products

- **[GET] /v1/products/**: Lista paginada de todos os produtos.
- **[GET] /v1/products/{id}**: Obtém um produto pelo ID.
- **[DELETE] /v1/products/{id}**: Deleta um produto pelo ID.
- **[PATCH] /v1/products/{id}**: Atualiza um produto pelo ID.
- **[POST] /v1/products**: Registra um novo produto.

### Orders

- **[GET] /v1/order/queue**: Lista paginada de itens na fila de pedidos.
- **[GET] /v1/order**: Lista paginada de todos os pedidos.
- **[POST] /v1/order**: Registra um novo pedido.
- **[GET] /v1/order/{id}**: Obtém um pedido pelo ID.
- **[DELETE] /v1/order/{id}**: Deleta um pedido pelo ID.
- **[PATCH] /v1/order/{id}**: Atualiza um pedido pelo ID.
- **[PATCH] /v1/order/fake-checkout/{order_id}**: Define o status de pagamento de um pedido. (Fake Checkout que simula o pagamento)
- **[GET] /v1/order/get_payment_status/{order_id}**: Obtém o status de pagamento de um pedido.
- **[GET] /v1/order/display-orders/**: Lista paginada de todos os pedidos ordenados pelo status (ready > being_prepared > received) e data descendente de criacao.
