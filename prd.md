---

# Product Requirements Document (PRD): Acionamento de Entregas (MVP)

## 1. Visão Geral e Objetivo

Atualmente, o processo logístico permite que fiscais de obras reservem materiais informando uma data de necessidade. Para fechar o ciclo de atendimento com o armazém, este produto introduzirá o fluxo de **Acionamento de Entrega**.

O objetivo da solução é permitir que as reservas sejam convertidas em ordens de saída logísticas precisas, garantindo flexibilidade para entregas parciais e registrando de forma definitiva o agendamento logístico para consumo posterior do sistema WMS.

## 2. Perfis de Usuário

* **Fiscal de Obras (Agência):** Usuário principal. Consulta as reservas, decide o que precisa ser entregue no momento e confirma o agendamento logístico da entrega.
* **Operador de Armazém / WMS:** Usuário indireto. Consumirá os dados deste acionamento no sistema WMS para iniciar o *picking* (separação) e expedição.

## 3. Requisitos Funcionais e Fluxo do Usuário

O sistema deve suportar o seguinte fluxo principal:

1. **Acesso e Contexto:** Ao acessar o sistema, o fiscal de obras seleciona sua agência. A tela carregará as reservas pendentes vinculadas a esta agência (consumindo as rotas atuais `GET /pedidos`).
2. **Seleção Flexível:** O fiscal de obras seleciona quais itens da reserva deseja acionar. O sistema deve permitir o **acionamento parcial** (seleção de parte dos itens do pedido original).
3. **Gestão de Datas:**
* O sistema sugere, por padrão, a *data de necessidade* original definida no momento da reserva.
* O fiscal de obras pode aceitar a data sugerida ou editá-la (antecipar ou postergar).


4. **Confirmação:** A ação de confirmação finaliza o acionamento de forma autônoma, sem necessidade de fluxos paralelos de aprovação.
5. **Pendências:** Itens da reserva que não forem selecionados permanecerão atrelados ao `id_pedido_origem` para acionamentos futuros.

## 4. Diretrizes de Interface e Experiência (UX/UI)

A interface deve priorizar a eficiência operacional, com as seguintes premissas visuais e de interação:

* **Estética Clean e Minimalista:** Uso consciente de espaços em branco (white space), remoção de textos redundantes e foco absoluto na legibilidade dos dados logísticos.
* **Identidade Visual:** Aplicação das cores institucionais para alinhamento com o ecossistema atual, garantindo familiaridade aos usuários.
* **Componentes:** Utilização de bordas arredondadas (rounded borders) para botões, modais e *cards* de informação.
* **Telas Necessárias:**
* Listagem de histórico de acionamentos da agência (com paginação).
* Tela/Modal de seleção de itens e confirmação de data.
* Tela/Modal de visualização dos detalhes de um acionamento específico.



## 5. Especificações Técnicas e Arquitetura

### 5.1. Stack Tecnológico

* **Backend:** Microsserviços rodando em **AWS Lambda** utilizando **FastAPI** (Python).
* **Banco de Dados:** **Amazon DynamoDB** (NoSQL), modelado com padrão "Agrupado" (1 registro = 1 acionamento completo).
* **Mensageria:** **Amazon SNS** para desacoplamento e envio das ordens logísticas ao WMS.
* **Padrão de Integração:** Arquitetura BFF (Backend For Frontend) para orquestração das requisições e isolamento de regras de negócio da camada de UI.

### 5.2. Modelagem de Dados (DynamoDB)

O registro no banco de dados deve consolidar o cabeçalho do acionamento e a lista de itens despachados.

**Chaves de Acesso:**

* **Partition Key (PK):** `id_acionamento`
* **Global Secondary Index (GSI):** `hash_destino-index` (para consultas por agência).

**Estrutura do Payload (Atributos):**

* `id_acionamento` (String/UUID)
* `hash_destino` (String)
* `destino` (String)
* `solicitante` (String)
* `numero_projeto` (String)
* `data_entrega` (String/Date)
* `id_pedido_origem` (String)
* `itens` (Array de Objetos)
* `id_item` (String)
* `sku` (String)
* `descricao` (String)
* `quantidade` (Number)



### 5.3. Contrato de APIs (BFF + FastAPI)

| Rota | Método | Objetivo e Parâmetros | Retorno |
| --- | --- | --- | --- |
| `/acionamentos` | **POST** | **Gravar Acionamento.**<br>

<br>Recebe payload agrupado. Grava registro no DynamoDB gerando o ID único e dispara mensagem para o tópico SNS correspondente. | `201 Created` + `id_acionamento` gerado |
| `/acionamentos` | **GET** | **Listagem Histórica.**<br>

<br>**Query Params:** `hash_destino` (Obrigatório), `next_token` (Opcional).<br>

<br>Consulta via GSI ordenada por data de criação. | `200 OK` + Array de acionamentos resumidos + `next_token` |
| `/acionamentos/{id}` | **GET** | **Detalhes do Acionamento.**<br>

<br>**Path Params:** `id_acionamento` (Obrigatório).<br>

<br>Busca direta via Partition Key (`GetItem`). | `200 OK` + Objeto JSON agrupado completo. |

*Nota: As rotas de listagem e detalhamento de reservas disponíveis no momento da solicitação continuam utilizando as rotas vigentes (`GET /pedidos` e `GET /pedidos/{id_pedido}`).*

## 6. Fora de Escopo (Não contemplado no MVP)

* Controle de validade ou expiração sistêmica de reservas não acionadas ao longo do tempo.
* Integração bidirecional (via API REST/Webhook) com o WMS de forma síncrona. O acoplamento será feito via disparo de evento no SNS.
* Modificação das quantidades unitárias no momento do acionamento (a fração ocorre apenas por seleção de itens inteiros na lista).

## 7. Critérios de Aceitação

* O sistema permite acionar parcial ou totalmente os itens listados no pedido de origem.
* O fiscal de obras consegue sobrepor a data sugerida por uma nova data (antecipando ou postergando).
* A requisição via `POST /acionamentos` persiste o dado corretamente agrupado no DynamoDB.
* Uma mensagem SNS contendo o payload agrupado é publicada com sucesso para consumo do WMS.
* A listagem de acionamentos por agência funciona via GSI com suporte nativo a paginação.
