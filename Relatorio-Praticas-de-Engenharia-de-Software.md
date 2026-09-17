# Relatório de Práticas de Engenharia de Software

> Relatório consolidado e agnóstico de tecnologia, extraído da análise da base de conhecimento do repositório `athena`. O conteúdo foi generalizado para descrever práticas de engenharia de software aplicáveis a qualquer stack, sem vínculo com plataformas, linguagens ou ferramentas específicas.

---

## 1. Escopo e Método

A base documental foi analisada nas dimensões:

- **Regras de código** (convenções, formatação, nomenclatura, boas práticas de escrita);
- **Padrões de projeto e arquitetura** (fundamentos de design orientado a objetos e domínio);
- **Abordagens de desenvolvimento** (fluxo de implementação, rascunhos, validação local);
- **Práticas de revisão** (critérios, checklist, formação de revisores, responsabilidades);
- **Fluxos de versionamento e release** (ramificações, commits, publicação de correções);
- **Estratégia de testes** (o que testar, como testar, em quais plataformas);
- **Qualidade e monitoramento** (análise estática, desempenho, disponibilidade).

---

## 2. Regras de Código

### 2.1 Nomenclatura

- Nomes devem ser **de fácil compreensão**, **pronunciáveis** e com propósito claro.
- Evitar **siglas**, **tipos embutidos** e **sufixos desnecessários** no nome.
- Nomes devem ser **passíveis de busca** e **não economizar palavras**.
- Evitar **palavras reservadas** e **mistura de idiomas** no mesmo contexto.
- **Classes** → substantivos; **métodos** → verbos ou frases verbais.
- Métodos devem ser descritivos e autoexplicativos (ex.: `ListarColetas`, `ExisteColetaPorItemControle` — generalizando: sempre expressar *o que* a operação faz e o *resultado* que entrega).
- Nomes devem respeitar a **linguagem ubíqua do domínio**; nomes técnicos "arranjados" que não correspondem ao conceito de negócio devem ser questionados na revisão.
- **Consistência**: seguir um único padrão de caixa por contexto (constantes, atributos privados, protegidos, variáveis locais) e pelos tipos de identificadores (arquivos em um padrão, símbolos em outro).
- Métodos assíncronos devem ter sufixo padronizado (`Async`, `Sync`, etc.) no nome.

### 2.2 Formatação e legibilidade

- Indentação e formatação **sempre no mesmo padrão do projeto**; aplicar os formatadores/linters oficiais da linguagem.
- Código **legível acima de tudo**: se não é possível entender sem esforço, deve ser refatorado.
- **Classes e métodos pequenos**; funções com responsabilidade única e escopo curto.
- **Sem comentários desnecessários**; comentários são aceitos apenas para fins de documentação (contexto/justificativa de decisões).
- **Sem código comentado** — não deve subir para a aplicação.
- **Sem código morto**: linhas após `return`, condições inalcançáveis, variáveis não utilizadas.
- **Sem código duplicado ou redundante**: reduz capacidade de manutenção, infla o código e prejudica desempenho.
- **Loops sempre com fim alcançável** — revisar por laços infinitos.

### 2.3 Valores e estado

- **Sem constantes nem números mágicos**: strings e números repetidos devem ser extraídos para constantes/recursos nomeados.
- **Sem strings mágicas**: mensagens expostas ao usuário devem vir de camadas de recursos/mensagens (internacionalização), nunca hardcoded.
- **Evitar variáveis globais / estado mutável compartilhado**; preferir escopo restrito e imutabilidade.
- Usar **imutabilidade** por padrão em valores constantes; declarar mutáveis apenas quando houver necessidade real de alteração.
- Preferir **constantes/read-only** sobre variáveis mutáveis de propósito único.
- **Tipagem explícita**: evitar o tipo "genérico/indefinido" (`any`, etc.) a menos que não exista alternativa razoável.
- **Encapsulamento**: membros internos privados por padrão; propriedades com escrita controlada para validar mudanças.

### 2.4 Qualidade de código em revisão (resumo da checklist)

- O código **testa o que se propõe a testar** (quantidade e criticidade suficientes, valores corretos).
- **Debug** removido antes da entrega.
- Trocar variáveis globais por alternativas que reduzam estados inconsistentes.
- Remover `[Ignore]`/exclusões de cobertura em testes/símbolos; quando extremamente necessárias, exigir **débito técnico registrado e priorizado**.

---

## 3. Padrões de Projeto, Design e Arquitetura

- **SOLID** como princípio-base de design.
- **Tell, Don't Ask** — pedir a um objeto que realize a operação em vez de extrair dados para decidir fora.
- **YAGNI** — não construir o que não é necessário agora.
- **DDD (Domain-Driven Design)**:
  - **Regras de negócio e validações vivem na camada de domínio** (e não na camada de dados/interface).
  - Entidades de domínio devem ser **consistentes por construção** (não existir em estado inválido); construtores exigem as informações mínimas para a entidade ser funcional.
  - Encapsulamento: alteração de propriedades passa por métodos/validações, não por escrita direta.
  - **Linguagem ubíqua** padronizada e coerente entre requisito, código e telas.
- **Camadas com responsabilidades bem definidas**:
  - **Domínio**: regras, contratos, validações.
  - **Aplicação/serviços**: operações de caso de uso (consultas, orquestração), sem conhecer a persistência.
  - **Dados/Repositórios**: acesso a dados isolado do negócio.
  - **Interface/Controllers**: entrada HTTP e contrato de resposta; mensagens amigáveis em vez de exceções não tratadas.
- **Injeção de dependência**: manter a composição em um único ponto por fronteira; não criar/construir contêineres no meio do código de produção.
- **Composição sobre herança**: evitar classes-base "faz-tudo" muito acopladas; preferir unidades pequenas e focadas (handlers/operações dedicadas).
- **Padrões de mensageria**: tratativas de erro explícitas, filas de não entregáveis (dead letter) com reprocessamento, planos de contingência para mensagens falhas.
- **Padrão de resposta/contrato único** para as APIs, reduzindo surpresas no consumidor.
- **Tratamento de erros centralizado**: exceções não tratadas não devem vazar; converter em notificações/mensagens amigáveis ao usuário, registrando a causa.
- **Cuidado com os "gotchas" de cada framework**: conhecer comportamentos implícitos (ex.: ciclo de vida de componentes, eventos assíncronos, lazy loading) para evitar bugs silenciosos.

---

## 4. Abordagens de Desenvolvimento

### 4.1 Fluxo de implementação

1. Criar uma **ramificação de feature a partir da ramificação de desenvolvimento** (jamais de produção);
2. **Codificar + escrever os testes** de forma incremental;
3. Realizar **validação local (desk check)** do comportamento com as partes interessadas (negócio + QA) *antes* de abrir o PR;
4. Abrir o **PR para a ramificação de origem** com título/descrição padronizados e vínculo com o work item;
5. Propagar correções entre ambientes por **cherry-pick** (dev → release → produção), mantendo os três ambientes coerentes;
6. Correções de produção (hotfix/bugfix) devem ser **propagadas de volta** para dev para não se perderem.

### 4.2 Regras de ramificação e publicação

- Features e correções saem da **dev**; releases nascem de dev e seguem para aceite e produção.
- Hotfix: ramificação a partir da **release/produção corrente**; após publicar, **replicar para aceite e dev**.
- Bugfix durante release a partir de **aceite**, com propagação para dev.
- **Atividades longas (+2 semanas) não devem ser tratadas como fix prioritário** — aguardam a próxima release a partir de dev. Fixes relevantes devem passar por todos os ambientes de forma rastreável.
- Após o deploy, **validar a versão no ambiente** (status do serviço/versão publicada).

### 4.3 Commits e histórico

- Padrão de mensagem de commit: **`tipo/identificador - o que a atividade executou`**, com `feature`, `bugfix` e `hotfix` como tipos.
- Título do PR deve ser **texto simples** (sem markdown e sem caracteres especiais), pois será usado como mensagem de commit no merge da base.
- **Histórico saudável**: reduzir a feature a um **único commit** (squash) para o merge; *squash* preserva a rastreabilidade sem poluir o histórico.
- Durante o desenvolvimento, cobrar ao menos **um commit por dia decorrido** no PR (evidencia progresso e diffs menores para revisão).
- Reverter PRs mergeados com **revert explícito** (e revert múltiplo na ordem do mais recente para o mais antigo).

### 4.4 Validação local (Desk Check)

- O desenvolvedor valida localmente a entrega **antes da subida para ambientes oficiais**;
- Após finalizar, **aciona negócio e qualidade** para demonstrar a correção/evidência no ambiente local;
- Somente **após a aprovação local** abre-se o PR.

### 4.5 PR em modo rascunho (Draft)

- Abrir o PR em modo **draft/rascunho** enquanto não está pronto para merge;
- Benefícios: não dispara pipelines de integração a cada commit intermediário; permite ao próprio autor **revisar o próprio código**; reduz carga na infraestrutura de CI.

---

## 5. Práticas de Revisão de Código

### 5.1 Responsabilidade do revisor

- "Tu te tornas eternamente responsável por aquilo que revisas" — a revisão é uma **responsabilidade de qualidade**, não uma formalidade.
- Cobrar padrões (título/descrição do PR, vínculo com work item, quantidade de commits).
- Na **ausência de padrão definido**, questionar os demais revisores e **registrar a decisão na base de conhecimento** para o futuro (fonte de verdade viva).

### 5.2 O que revisar (checklist de código-fonte)

**Nomenclatura e legibilidade**
- Nomes claros, pronunciáveis, buscáveis, sem siglas/tipos/sufixos ambíguos;
- Classes substantivos, métodos verbos;
- Não misturar idiomas; respeito à linguagem ubíqua.

**Correção e manutenção**
- Comentários desnecessários removidos; sem código comentado;
- Sem código morto, redundante ou duplicado;
- Loops com fim alcançável; sem comandos de debug;
- Variáveis globais evitadas;
- Convenções do time respeitadas (formatação, padrões de arquivo, sufixos de tipos).

**Testes**
- Testes testam exatamente o que se propõem (cenário nomeado de forma clara);
- Cobertura suficiente para os **pontos críticos e de maior complexidade** (não apenas o que a análise automática exige);
- Cenários descritos no work item cobertos;
- Preferir testes **descritivos e expressivos (DAMP)** sobre reaproveitamento excessivo (DRY em testes); registrar a discussão para não virar dogma;
- **Isolamento garantido** (sem depender de ElasticSearch, rede ou dados voláteis);
- Nomes significativos em casos de teste e fontes de casos.

**Backend/domínio**
- Validações/regras na camada de domínio;
- Consulta a dados **somente via repositório** (não vazar fonte de dados/consulta para fora);
- Não expor consultas que executem no banco de forma tardia como se fossem dados prontos (não propagar *queries* não materializadas; executar de forma consciente);
- **Evidência da consulta gerada** por ORM para qualquer acesso a banco (profiling) — obrigatório;
- Respeito às boas práticas do framework de persistência (performance), avaliação no banco vs. em memória;
- Atenção a mudanças no registro de dependências (não quebrar a configuração de injeção anterior).

**Frontend/interface**
- Lint de formatação aplicado;
- Tipagem explícita; evitar tipo genérico;
- Imutabilidade e encapsulamento (membros privados; constantes read-only);
- Consciência das peculiaridades do framework (ciclos de vida, assíncronismo, detecção de mudanças) para evitar bugs silenciosos.

### 5.3 Revisão de testes automatizados de interface (E2E/UI)

- Sem comandos de debug; sem `.only`/`.skip` deixados no código;
- **Sem esperas de tempo fixo** (`wait/ sleep` fixos) — usar esperas explícitas/inteligentes (último recurso);
- Evitar **condicionais** no teste sempre que possível (avisar sobre fragilidade);
- **Estressar o teste em modo headless** para detectar **intermitência**, principalmente com condicionais;
- Mapear elementos com **seletores estáveis dedicados** (atributos do tipo `data-`), não por hierarquia de classe/css;
- Abstrair **ações comuns nos hooks** (setup/teardown);
- Usar **aliases/contexto compartilhado** no lugar de variáveis mutáveis para encadear estado entre passos;
- Uso correto dos localizadores encadeados (buscar no escopo certo do elemento).

### 5.4 Formação e escala de revisores

- Novos revisores passam por **período supervisionado** com um padrinho avaliando a qualidade das revisões;
- Feedback semanal baseado em **checklist** (apontar o tópico perdido é responsabilidade do aprendiz estudá-lo);
- Promoção a revisor após **mínimo de período e média objetiva em revisões** (notas por gravação de checklist mais avaliação do padrinho);
- Revisão de **testes de automação exige o time de qualidade** — alterações na camada de testes de UI passam por revisão dedicada.

---

## 6. Estratégia de Testes

### 6.1 Como identificar o que testar

**Com base no requisito (caixa-preta):**
- **Partição de equivalência** — agrupar entradas equivalentes para reduzir casos;
- **Análise de valor limite** — testar nos limites das partições;
- **Tabela de decisão** — combinações de condições e ações;
- **Transição de estado** — eventos e mudanças de estado permitidos/negados.

**Com base no código (caixa-branca):**
- **Cobertura de sentença** — todo comando executado ao menos uma vez;
- **Cobertura de decisão** — todas as decisões verdadeiras/falsas exercitadas.

**Com base na experiência:**
- **Testes exploratórios** — missões guiadas (SBT/session based testing), navegação orientada por risco e conhecimento empírico;
- **Heurísticas** — guias mnemônicos por tipo de contexto (sessão/cookies, campos obrigatórios e estouro, paginação, regras de negócio, acesso direto a URLs, listagens de 0/1/muitos, máscaras e tipagem, fuso horário, soft delete e chaves estrangeiras, ortografia, idiomas/perfis, acessibilidade/ALT, indicação de obrigatoriedade);
- **Histórico de falhas** — priorizar regressões com base no dashboard de defeitos registrados.

**Com base nos riscos:**
- Priorização por **probabilidade × impacto** (abordagem do tipo PRISMA), votada por equipe técnica e de negócio;
- Vulnerabilidades típicas: fraude, segurança/ataques, queda de conexão/serviço, abandono de processo, gravação incorreta.

### 6.2 Níveis e formatos de teste

- **Testes unitários**:
  - Nome significativo no modelo `Deve_Realizar_Ação` (idioma do time);
  - Operações assíncronas testadas de forma assíncrona (sem bloquear thread);
  - Validadores/regras unitárias com mocks (sem infraestrutura);
  - **Um tema por arquivo**: testes de validação separados dos testes de serviço/operação.
- **Testes de integração**:
  - Composição de dependências via container real com sobrescrita de infra (não depender de serviços externos);
  - **Cargas de dados compartilhadas** (datasets reutilizáveis) para evitar setups gigantes;
  - **Não adicionar novas entidades a cargas existentes** — novo cenário = nova carga, para evitar intermitência/efeito cascata;
  - Cargas com hooks idempotentes (`antes de carregar`, `já carregado?`) evitando duplicação;
  - Em fontes de dados não transacionais (busca/índices), não depender de consulta prévia para decidir carregar (retornar pronto, pois o estado pode mudar/versione).
- **Testes de interface (E2E)**: dados estáveis por seletores dedicados, sem sleeps, sem condicionais frágeis, tolerância a intermitência.
- **Testes de API REST**:
  - Regras de negócio (limites, obrigatórios, payloads variados);
  - Continuidade de fluxos (retorno faz sentido para a próxima etapa);
  - Tipagem de dados de entrada/saída;
  - Parâmetros corretos por método e local (body vs. URL vs. query);
  - Permissões com **perfis de usuário diferentes** (o que cada perfil pode/pode achar);
  - Semântica HTTP correta (`201` criar, `200` consultar/alterar, `204` excluir);
  - Estrutura estável das respostas; **documentação do contrato** (ex.: spec/Swagger) coerente com o implementado.
- **Isolamento de interface**: testes de interface independentes do estado da base/ambiente.

### 6.3 Reporte de inconsistências/Bug

- **Título auto-descritivo com o impacto** ao usuário (permite dimensionar urgência);
- **Entrada + passos + comportamento atual em Gherkin**; comportamento esperado;
- **Ambiente e versão**;
- **Prioridade** (quando entregar — definida com o negócio) **≠ severidade** (gravidade funcional);
- **Evidências**: logs, screenshots, trecho de código;
- Boas práticas: reproduzir mais de uma vez; checar duplicados; investigar **causa raiz** (logs, front vs. back, regras); verificar status dos serviços antes de reportar; descrever impacto em outras áreas; ser claro e objetivo.

### 6.4 Combate à intermitência

- Intermitência é tratada com **seriedade** (é causa de retrabalho e desconfiança);
- Cargas de dados estáveis e específicas por cenário;
- Tests E2E estressados em headless para detectar flakiness;
- Melhorias de teste com impacto na estabilidade (ex.: remover indeterminância) tornam-se objetivo explícito de PR.

---

## 7. Qualidade Automatizada, Desempenho e Observabilidade

- **Lint/estilo** obrigatório desde o editável até o CI;
- **Análise estática** como camada de qualidade (*deve* passar), mas **não é suficiente**: revisão humana deve ir além (criticidade da regra de negócio, caminhos não cobertos);
- **Cobertura** orientada por **complexidade** (ciclomática) e pontos críticos; não apenas percentual global;
- **Banir no código de teste**: exclusões de cobertura e ignores — só com débito técnico registrado/priorizado;
- **Desempenho de acesso a dados**:
  - Monitorar a **query realmente gerada** pelo ORM (profiler) e seu **plano de execução**;
  - Evitar idas repetidas ao banco em laços (N+1); preferir carregamento antecipado/único quando adequado;
  - **Projetar/retornar apenas os dados necessários**;
  - **Deixar o banco fazer o trabalho** (filtro/agregação no banco e não em memória);
  - Conhecer a diferença entre "consulta ainda não executada" vs. "dados materializados" e entre predicado executável por expressão vs. chamada de função no servidor;
  - Consultas somente-leitura sem rastreamento de entidades (quando faz sentido).
- **Versionamento de esquema de dados**:
  - Migrations versionadas com **`Up` e `Down` simétricos** (rollback sempre fornecido);
  - **Sem manipular entidades dentro de migrations**; usar as APIs de manipulação de esquema/dados da ferramenta;
  - Data seeding declarativo em vez de inserts manuais;
  - Alterações de desempenho crítico: **zero downtime** — quebrar a evolução em fases (expand → preencher → contratar), cada deploy compatível com o anterior e reversível.
- **Observabilidade e SLOs**:
  - Monitorar disponibilidade com **testes sintéticos** periódicos (endpoints e fluxos de tela);
  - Definir **SLOs explícitos** (janelas de disponibilidade) e medir **MTTR** (tempo médio de reparo);
  - Logs centralizados como evidência para investigação de incidências.

---

## 8. Definições de Pronto (DoR/DoD)

### Definition of Ready (tarefa pronta para iniciar)
- **Descrição do problema** que a atividade resolve;
- **Ao menos um critério de aceite**;
- **Ao menos um cenário de teste**;
- Front: **wireframe/conceito visual** validado com UX e aderente aos padrões de UI;
- **Não iniciar fora do escopo** sem notificar analista/tech lead;
- **Não assumir atividades com dependências externas** (outras atividades, técnicas, pendências de negócio) não resolvidas;
- **Grandes funcionalidades / novos módulos** apresentados à arquitetura com antecedência (antes de escrever as tarefas).

### Definition of Done (entrega concluída)
- Front **fiel ao wireframe** acordado;
- **100% dos cenários de teste** atendidos;
- **100% dos critérios de aceite** atendidos;
- **Pré-validações** executadas quando realmente necessárias;
- **Evidência** apresentada cobrindo todos os critérios.

---

## 9. Colaboração e Cerimônias (apoio à engenharia)

- **Reuniões com contrato**: pauta enviada antes; foco nos pontos de pauta; questionamento ativo dos participantes; **ata consolidando decisões** (documento resultante) — decisões de reunião não se perdem em e-mails.
- **Conhecimento como fonte de verdade**: padrões acordados são registrados na base de conhecimento e consultados; quando não há padrão, decide-se em conjunto e **registra-se**.
- **Treinamento e competências**: mapeamento de competências e trilhas técnicas/negócio para nivelar o time; aprendizagem contínua é parte do processo de qualidade (inclusive para revisores).

---

## 10. Recomendações e Melhorias

Com base na análise, seguem recomendações práticas e agnósticas:

1. **Consolidar uma única fonte de verdade** dos padrões (checklist único de revisão, regras de código, DoR/DoD) em um *handbook* versionado e consultável — a base atual está rica porém distribuída em vários documentos com estados distintos (inclui itens "em desenvolvimento" e "deprecated").
2. **Fixar um template de PR obrigatório** (por quê / como / efeitos colaterais) versionado no próprio repositório e validado por automação (checagem de campos preenchidos e vínculo com work item).
3. **Automatizar os critérios verificáveis da checklist**: lint, formato de mensagem de commit, banimento de `sleep`/`.only`/`.skip`/exclusões de cobertura, metas de cobertura por complexidade — reduzindo a carga humana para o que exige julgamento.
4. **Transformar intermitência em débito priorizado**: qualquer teste flaky identificado deve virar item explícito de trabalho (com evidência) e não ser apenas "rodado de novo".
5. **Escalar revisão por pares com mentoria**, mantendo métricas objetivas (checklist + avaliação) e feedback semanal — modelo que funciona e deve ser documentado como guia formal.
6. **Reforçar o desk check local como gate** antes do PR: transformar em checklist versionada (evidência, tela/branch, cenário, condições), evitando que se torne etapa informal.
7. **Publicar guias de zero downtime e migrações em etapas** como padrão-padrão do pipeline de release, com checklists (expandir, preencher, contratar, reverter) e exemplos por tipo de mudança (campo obrigatório, renomeação, partição).
8. **Tratar decoração de PRs com comportamento**: revisores devem questionar nomes e desenhos que não correspondem à linguagem ubíqua e registrar o racional/ADR quando a classificação (facade vs. mapper vs. aggregate) for ambígua.
9. **Priorizar testes baseados em risco (PRISMA)** nas liberações recorrentes, atrelando critérios de aceite e cenários ao nível de risco calculado.
10. **Manter SLOs/MTTR** como métricas de engenharia — publicar painel acessível e usar incidentes para alimentar o ciclo de melhoria (causa raiz → ação → validação).
11. **Padronizar o reporte de bugs** (título com impacto, Gherkin, ambiente/versão, prioridade ≠ severidade, evidências) com template/formulário único para reduzir retrabalho de triagem.
12. **Cuidado com "boas práticas" copiadas sem contexto** (ex.: DAMP vs. DRY em testes): registrar o **racional** de cada decisão e sinalizar quando é "discutir" vs. "regra".

---

## 11. Glossário de Práticas Referenciadas

| Termo | Significado |
|---|---|
| **DoR / DoD** | Definition of Ready / Definition of Done — entradas e saídas de uma atividade. |
| **DAMP / DRY** | DAMP: testes descritivos e expressivos; DRY: não repetir a si mesmo. |
| **SBT** | Session-Based Testing — testes exploratórios estruturados em sessões/missões. |
| **PRISMA / RBT** | Testes baseados em risco — priorização por probabilidade × impacto. |
| **SLO / MTTR** | Nível de serviço desejado / tempo médio de reparo. |
| **Gherkin** | Formato de descrição de cenários (dado/quando/então). |
| **Zero downtime** | Mudança aplicável sem indisponibilidade e com rollback imediato. |
| **Linguagem ubíqua** | Vocabulário único e consistente entre negócio e código. |