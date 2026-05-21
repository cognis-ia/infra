INFRA — OpenClaw (Bruno Eduardo)
Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo.
Última atualização: 2026-05-21 (sessão 4 — Imersão Pixel AI Hub)

Como iniciar uma nova sessão
Selecione a pasta D:\COGNIS\Curso Openclaw no Cowork — o CLAUDE.md dispara
automaticamente a skill openclaw-session-start, que busca este arquivo e configura SSH.
Arquivo necessário na pasta: vps_key (chave SSH privada — nunca compartilhe)

---

Arquitetura conceitual (Imersão Pixel AI Hub)

Tese: Claude = estação · GitHub = memória · OpenClaw = operação.
- Claude/Cowork: estação de trabalho da pessoa (escreve, decide, captura).
- GitHub: fonte de verdade da memória, versionada, portátil.
- OpenClaw: runtime sempre ligado (canais, crons, heartbeats, agentes 24/7).

3 níveis de memória (entender em qual cada agente está):
1. Amnésia total — sessão isolada, esquece tudo.
2. Memória isolada — agente lembra, mas só ele.
3. Cérebro compartilhado — memória no repositório. Qualquer agente acessa.
Objetivo do stack: tudo no nível 3.

3 cérebros (separação de permissão e contexto):
- Pessoal — privado, individual, auto-commit ok.
  Hoje no stack: workspace dos agentes individuais (Rocky, BrIA, Gabi, Max, Leo).
- Empresa — compartilhado pelo time, auto-commit p/ dados não-sensíveis, gatilhos roteiam sensíveis pra diretoria.
  Hoje no stack: parcial — shared/bria-shared, sem segregação formal por área.
- Diretoria — sem auto-commit. Tudo passa por staging → revisão humana → main.
  Hoje no stack: NÃO existe (gap aberto — ver Pendências).

Áreas vs Agentes (não misturar):
- areas/ = conhecimento que existe independente de quem opera (vendas, marketing, atendimento, operações).
- agentes/ = operadores que leem e executam o conhecimento. Pode trocar o agente; o conhecimento da área permanece.

4 estágios de evolução multi-agente (onde estamos):
1. Agente pessoal dos sócios (1 agente no privado, acessa cérebro inteiro).
2. Agente geral no grupo (1 agente compartilhado com a equipe).
3. Segmentação por BU (agente que cobre 3-4 áreas correlatas).
4. 1 agente por área + master coordenador.
Hoje no stack: misto entre 1 e 2 (Rocky/Leo pessoais; BrIA/Gabi/Max especialistas Bernardelli; sem master coordenador).

---

Padrões obrigatórios (do curso Pixel)

Sempre que criar/auditar workspace de agente, exigir:

1. Tríade de identidade por agente: SOUL.md (quem é) + AGENTS.md (o que pode) + USER.md (quem serve).
   Complementares: HEARTBEAT.md (proatividade), MEMORY.md (memória curada), IDENTITY.md (papel base), TOOLS.md (ferramentas).

2. MAPA.md em cada nível do cérebro.
   Sem mapa, agente entra em todas as pastas pra trazer informação — torra tokens e se perde.
   Cobertura mínima: raiz/cerebro, cerebro/empresa, cerebro/areas/<area>, cerebro/agentes/<agente>.

3. _index.md em toda pasta de skills/rotinas.
   Lista o que existe + o que cada item faz + onde está.

4. Estrutura canônica por área: contexto/ + skills/ + rotinas/ + projetos/.
   contexto = geral.md + people.md + decisions.md + lessons.md.

5. Anatomia de skill em 4 níveis progressivos (não começar pesado):
   N1 só SKILL.md → N2 +examples/ → N3 +scripts/ → N4 completo.

6. Cron vs Heartbeat (não confundir):
   - Cron: agenda por tempo, determinístico, cria os eventos (relatório 8h, follow-up segunda).
   - Heartbeat: decide por estado, adaptativo, reage aos eventos (priorizar leads, pausar campanha ruim, recuperar cron falho).

7. Regra dos 3 gatilhos (DIRETORIA, não cérebro empresa):
   - Dinheiro com nome próprio (salário, comissão, pró-labore, dívida nominal).
   - Pessoa específica (avaliação, conflito, contratação, desligamento, performance).
   - Peso jurídico/contratual (contrato, NDA, litígio, LGPD, governança).
   Se disparar qualquer dos 3 → não vai pro cérebro do time, vai pro repo de diretoria com revisão humana.

8. Permissionamento Telegram em 2 camadas: estar no grupo + estar na whitelist de IDs do agente.

9. Workspace separado obrigatório para bot de suporte (não compartilhar contexto com agente principal).

---

Segurança em 3 camadas (OWASP LLM Top 10 2026)

Referência: 21k+ instâncias OpenClaw/agentes expostas com chaves vazadas, 88% das empresas
com agentes IA tiveram incidente, Prompt Injection é o risco #1, hardening correto reduz ~90% da superfície de ataque.

Camada 1 — Servidor (fundação)
  - SSH key-only — login com senha desabilitado.                          [ok no VPS atual]
  - Fail2ban — ban automático após 5 tentativas.                          [validar]
  - UFW Firewall — só portas 22, 80, 443 abertas.                         [validar]
  - Gateway em localhost — nunca expor 18789.                             [validar]
  - Updates automáticos — fecha CVEs conhecidas.                          [validar]

Camada 2 — Agente (comportamento)
  - dmPolicy: allowlist — só IDs autorizados falam.                       [aplicado WhatsApp read-only 2026-05-20]
  - Credenciais no .env — chmod 600, nunca no código.                     [verificar todos os workspaces]
  - Skills auditadas — ler código antes de instalar.                      [Starter Kit v2.5.6 ok]
  - Tool restrictions — allowlist de comandos.                            [exec.security=full hoje; reavaliar]
  - requireMention: true — bot só responde mencionado.                    [WhatsApp ok; Telegram revisar por grupo]

Camada 3 — Processo (disciplina operacional)
  - Dupla autorização — 2 confirmações antes de prod.                     [não implementado]
  - Audit crons — auditoria diária automática.                            [não implementado — ver Pendências]
  - Logs completos — toda ação com timestamp.                             [validar]
  - Rotação de tokens — trocar chaves a cada 90 dias.                     [pendência aberta — OpenAI exposta]
  - Memória no GitHub — backup de decisões críticas.                      [parcial: backups por agente ok, diretoria não existe]

OWASP TOP 5 que as 3 camadas cobrem:
Prompt Injection · Tool Misuse · Goal Hijack · Memory Poisoning · Privilege Abuse.

Lição do curso (caso Supabase): agente com acesso direto a banco identificou anomalia
e tentou corrigir sozinho — subiu update sem autorização. Restringir ferramentas e
comandos é obrigatório; default deve ser conversar por queries/mirrors/edge functions.

---

Infraestrutura

VPS: 217.77.10.26 — usuário openclaw
SSH: ssh -i <caminho>/vps_key -o IdentitiesOnly=yes openclaw@217.77.10.26
OpenClaw versão: 2026.5.18
Binário: ~/.npm-global/bin/openclaw
Serviço: systemctl --user restart openclaw-gateway

---

Agentes ativos (5)

| Agente | ID | Emoji | Papel | Canal Telegram | Workspace | GitHub backup |
|--------|-----|-------|-------|---------------|-----------|---------------|
| Rocky | main (default) | Agente pessoal do Bruno | telegram:default (@Rocky_Bruno_bot) | ~/.openclaw/workspace | cognis-ia/clawdio-workspace-backup |
| Leo | leo | Agente profissional (COGNIS IA) | telegram:leo (@CG_Leo_Bot) | ~/.openclaw/workspace-leo | cognis-ia/leo-workspace-backup |
| BrIA | bria | Suporte de alunas — Bernardelli Ensino | telegram:bria (@BE_BrIA_bot) | ~/.openclaw/workspace-bria | cognis-ia/bria-workspace-backup |
| Gabi | gabi | Criativa/estratégica da Jane — Bernardelli Ensino | telegram:gabi (@BE_Gabi_bot) | ~/.openclaw/workspace-gabi | nao criado |
| Max | max | Operacional da Marilia — Bernardelli Ensino | telegram:max (@BE_Max_bot) | ~/.openclaw/workspace-max | nao criado |

GitHub org: cognis-ia — token no VPS em ~/.openclaw/workspace/.env

Perfis Bernardelli:
- BrIA: suporte de alunas, Hotmart, Astron Members — persona Maria, 62 anos
- Gabi: criativa, conteúdo, voz da marca Jane — mentora de arte
- Max: operacional, analítica, parceira da Marilia

---

Segundos Cérebros

| Workspace | Quem usa | GitHub |
|-----------|----------|--------|
| ~/.openclaw/workspace-shared/ | Rocky + Leo | cognis-ia/shared-workspace-backup |
| ~/.openclaw/workspace-bria-shared/ | BrIA (isolado) | cognis-ia/bria-shared-backup |

Gabi e Max sem segundo cérebro ainda.

---

Crons ativos

| ID | Nome | Agente | Horário | Status |
|----|------|--------|---------|--------|
| 1a645071 | rocky-backup-diario | main | 23h todo dia | error sem route |
| 9cdbe3fa | leo-backup-diario | leo | 23h todo dia | ok |
| b5bc28b7 | bria-backup-diario | bria | 23h todo dia | error sem chatId |
| 8af5c4af | bria-heartbeat | bria | 8h 12h 16h 20h | error sem chatId |
| edf0d77c | Monitorar emails | main | 9h 14h 20h | idle |

---

Configuração exec-approvals — CRITICO

Para que agentes executem sem pedir aprovação, ambos os arquivos devem estar assim:

~/.openclaw/openclaw.json:
  tools.exec.security = "full"
  tools.exec.ask = "off"

~/.openclaw/exec-approvals.json:
  defaults.security = "full"
  defaults.ask = "off"
  defaults.autoAllowSkills = true
  (cada agente: main, *, leo, bria, max, gabi também tem esses campos explícitos)

Valores válidos:
  security: "full" (autonomia total) | "allowlist" | "deny"
  ask: "off" (nunca pedir) | "on-miss" | "always"

Se voltar a pedir aprovação: checar esses campos e reiniciar o gateway.

---

APIs integradas — Bernardelli Ensino

HOTMART (vendas)
  Agentes: BrIA, Gabi
  Credenciais: HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET, HOTMART_BASIC_TOKEN
  OAuth: https://api-sec-vlc.hotmart.com/security/oauth/token
  API: https://api-hot-connect.hotmart.com/
  Skill: workspace-bria/skills/hotmart-api/SKILL.md

ASTRON MEMBERS (entrega de cursos)
  Agentes: BrIA, Gabi, Max
  Club ID: 8194 (Pintando Telas) — 908 alunas
  Credenciais: ASTRON_AM_KEY, ASTRON_AM_SECRET, ASTRON_CLUB_ID=8194
  Base: https://api.astronmembers.com.br/v1.0/
  Auth: Basic HTTP (user=AM_KEY senha=AM_SECRET)
  Skill: workspace-max/skills/astron-members-api/SKILL.md
  CRITICO: usar urllib Python, nunca curl. Parâmetros em query string, nunca no path.

  Formato de resposta padrão Astron:
    Nome Completo
    Email
    Ativo ou Inativo
    Nome do curso - DD/MM/AAAA
    (expirados ao final:) Nome do curso - Expirado - DD/MM/AAAA

META ADS
  Agentes: BrIA, Gabi, Max, Rocky, Leo
  Credenciais: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID=10201604992032651
  Base: https://graph.facebook.com/v21.0/
  Skill: workspace-leo/skills/meta-ads-api/SKILL.md

NOTION (workspace Trabalho - 2025 — Jane + Marilia)
  Agentes: Gabi, Max
  Token compartilhado: NOTION_TOKEN_TRABALHO (em .env de cada agente)
  Workspace ID: 5f58405d-3718-47c7-802d-1e36cb1b777d (dono: Bruno)
  Database Atividades: 16327f4e-477c-813f-8a26-c8c855efffc5
  Página raiz (Banco de Dados): 17427f4e-477c-80fd-bb36-f29b5011f34a
  Skill: workspace-gabi/skills/notion-api/SKILL.md (igual para Max)
  CRITICO: .env está no .gitignore — tokens não vão para o GitHub backup.
    Tokens salvos apenas nos .env do VPS (nunca commitar).
    Para recriar: notion.so/my-integrations → workspace correspondente.

---

Skills instaladas (além do Starter Kit v2.5.6)

Rocky: remembering-conversations, openclaw-guardian, meta-ads-api, expense-tracker, fitness-coach, pdf-reports, whatsapp-monitor
Leo: content-strategy, copywriting, social-content, email-sequence,
     analytics-tracking, openclaw-guardian, meta-ads-api, dispatching-parallel-agents, pdf-reports
BrIA: copy-editing, email-sequence, marketing-psychology, openclaw-guardian,
      remembering-conversations, hotmart-api, astron-members-api, meta-ads-api,
      analytics-tracking, ab-test-setup, content-strategy, dispatching-parallel-agents, pdf-reports
  exec-approvals bria.ask = "on-miss" (crons rodam sem aprovacao, novos comandos pedem)
Gabi: copywriting, social-content, content-strategy, marketing-ideas,
      marketing-psychology, openclaw-guardian, remembering-conversations,
      hotmart-api, astron-members-api, meta-ads-api, notion-api, pdf-reports
Max: analytics-tracking, ab-test-setup, openclaw-guardian, remembering-conversations,
     dispatching-parallel-agents, astron-members-api, meta-ads-api, notion-api, pdf-reports

---

Pendências

URGENTE
5. Renovar token OpenAI Codex — ate 22 maio 2026 (SSH com TTY)
6. Rotacionar chave OpenAI — exposta em historico Git

Curso Openclaw (mini) — implementação pendente (ordem de prioridade)
A. TOOLS.md → MAPAs distribuídos — Rocky e Leo (A6)
   Migrar TOOLS.md monolítico para MAPA.md em cada pasta do workspace
   (memory/, content/, skills/, archive/). Gabi/Max/BrIA: verificar estado.
B. Heartbeat Rocky e Leo (A9)
   Criar HEARTBEAT.md e configurar proatividade passiva.
   BrIA tem heartbeat mas está com erro (sem chatId).
C. USER.md com 8 blocos — Rocky (A5)
   Verificar e completar: perfil, negócios, família, equipe, tom,
   restrições, valores, contexto operacional.
D. AGENTS.md atualizado em todos os workspaces (A5/A13)
   Organograma com 5 agentes, canais, modelos, escopo, WhatsApp.
E. Crons: Revisão do Dia (18h) e meta-cron de auditoria (7h) — Rocky (A9)
F. Mission Control (A14) — dashboard visual, projeto maior, sessão dedicada

Imersão Pixel AI Hub — gaps de arquitetura (ver seções conceituais no topo)
G. Cérebro de diretoria não existe.
   - Criar repo cognis-ia/cerebro-diretoria com template-diretoria-0.1.0.
   - Definir gatilhos automáticos no AGENTS.md (dinheiro+nome, pessoa, jurídico).
   - CODEOWNERS + PR template já vêm no template.
   - Decidir qual agente serve a diretoria (provavelmente Rocky, com workspace separado).
H. MAPA.md inexistente nos workspaces atuais.
   - Auditar cada workspace (Rocky, Leo, BrIA, Gabi, Max, shared, bria-shared).
   - Garantir MAPA.md em raiz e em cada subárea quando houver áreas separadas.
   - Sobrepõe parcialmente com pendência A (TOOLS.md → MAPAs do mini-curso).
I. _index.md em skills.
   - Validar que cada pasta skills/ dos 5 agentes tem _index.md atualizado.
J. Heartbeat baseado em estado (não só cron).
   - Adotar conceito Pixel: heartbeat = decisão por estado (priorizar leads, pausar campanha,
     recuperar cron falho). Reescrever bria-heartbeat após corrigir chatId.
   - Sobrepõe com pendência B.
K. Audit crons (camada 3 de segurança).
   - Skill que roda diariamente: SOUL.md válido? Skills referenciadas existem? Permissões consistentes?
     Commits recentes? Cron com erro há mais de 24h?
   - Sobrepõe com pendência E (meta-cron de auditoria).
L. Gestor de agentes (master coordenador — estágio 4).
   - Relatório semanal de evolução (skills criadas, crons rodando, contexto atualizado).
   - Auditoria mensal de integridade.
   - Bom candidato: Rocky como master (já é o agente pessoal default).
M. Permissionamento Telegram — auditar whitelist de IDs.
   - Confirmar que cada @bot tem dmPolicy: allowlist com IDs explícitos.
   - WhatsApp já está read-only desde 2026-05-20.
N. Estrutura áreas/ canônica nos workspaces compartilhados.
   - workspace-shared (Rocky+Leo) e workspace-bria-shared não seguem padrão
     areas/{nome}/{contexto,skills,rotinas,projetos}.
   - Reorganizar conforme casos forem aparecendo (não refazer do zero).
O. Cérebro modelo do GitHub do curso.
   - imersao-openclaw-negocios-main.zip tem cérebro de exemplo populado com 4 agentes
     (assistente, marketing, bot-suporte) com SOUL+AGENTS+HEARTBEAT completos.
   - Vale ler para padronizar SOUL/AGENTS dos agentes atuais antes de criar novos.

Infraestrutura
1. GitHub backup Gabi e Max — cognis-ia/gabi-workspace-backup e max-workspace-backup
2. Crons com erro — rocky-backup-diario (sem route) e bria heartbeat+backup (sem chatId)
4. Segundo cérebro Gabi e Max
8. Deletar @Clawdio_Bruno_bot no BotFather — acao manual Bruno
9. Verificar se allowFrom da Gabi devia ter ID da Jane (938877898) — se sim, adicionar de volta

---

Regra absoluta

NUNCA assinar, contratar ou comprar qualquer coisa sem o expresso consentimento do Bruno Eduardo.

---

Atualização deste arquivo

Ao final de cada sessão: "Atualize o INFRA.md com o que fizemos hoje."
Claude atualiza E faz push para cognis-ia/infra no GitHub.
Nunca criar um novo arquivo — sempre editar este.

---

Historico da sessao - 2026-05-14

- INFRA.md buscado de https://raw.githubusercontent.com/cognis-ia/infra/main/INFRA.md.
- Chave SSH privada localizada em D:\COGNIS\Curso Openclaw\vps_key (conteudo nao registrado).
- SSH validado no VPS 217.77.10.26 como usuario openclaw; host respondeu vmi3214243.
- Aliases SSH configurados no Windows em ~/.ssh/config:
  ssh openclaw
  ssh openclaw-vps
- OpenClaw confirmado no VPS: OpenClaw 2026.5.3-1 (2eae30e).
- Gmail/gog do cron da Digi reautorizado para brneduardobot@gmail.com apos erro invalid_grant.
- Cron "Monitorar emails da Digi e baixar guias" migrado do Rocky para a BrIA:
  agente bria, Telegram accountId bria, mesma configuracao gog/Gmail do gateway.
- Estado do cron da Digi migrado para /home/openclaw/.openclaw/workspace-bria/memory/digi-email-watch.json.
- Execucao manual pos-migracao validada com status ok e resposta NO_REPLY quando nao havia novidade relevante.
- Importante: Rocky deve continuar com acesso a email e agenda. OAuth gog global reautorizado para
  brneduardobot@gmail.com com services calendar,gmail; chamadas reais de Gmail e Calendar validadas.
- Canva conectado ao OpenClaw via MCP oficial:
  servidor canva em ~/.openclaw/openclaw.json usando npx -y mcp-remote@latest https://mcp.canva.com/mcp.
- OAuth Canva autorizado e validado no VPS; token armazenado em ~/.mcp-auth/mcp-remote-0.1.37/.
- Pastas Canva criadas e testadas:
  Rocky: OpenClaw - Rocky, folder FAHJqxjREf0, https://www.canva.com/folder/FAHJqxjREf0
  Gabi: OpenClaw - Gabi, folder FAHJq_9sfpo, https://www.canva.com/folder/FAHJq_9sfpo
  Max: OpenClaw - Max, folder FAHJqwxhZhA, https://www.canva.com/folder/FAHJqwxhZhA
- Rocky, Gabi e Max testados via agente: cada um localizou sua pasta Canva com status ok.
- Regras gravadas nos TOOLS.md dos tres agentes:
  usar Canva para design/layout/edicao/exportacao/organizacao; usar ChatGPT/OpenAI image_generate como padrao para criacao de imagens bitmap.
- Google Workspace da Gabi conectado via gog:
  conta janebernardellibot@gmail.com, alias `gabi`, services calendar,gmail.
  Testes reais validados: `gog -a gabi gmail messages search ...` e `gog -a gabi calendar events list ...`.
  Regra gravada em /home/openclaw/.openclaw/workspace-gabi/TOOLS.md: Gabi usa sempre `gog -a gabi`; Rocky continua na conta default brneduardobot@gmail.com.

---

Historico da sessao - 2026-05-15

- BrIA promovida a gestora de tráfego senior: 4 skills instaladas (analytics-tracking de Leo,
  ab-test-setup de Max, content-strategy de Leo, dispatching-parallel-agents de Leo).
- exec-approvals BrIA: ask alterado para "on-miss" — crons rodam sem aprovaçao, novos
  comandos pedem aprovaçao. Isso resolve cron de desempenho de campanha sempre pedindo auth.
- 2 anuncios com criativo quebrado (reels deletados) na campanha INGRESSOS IMERSAO ARTE DERRAMADA:
  IDs 120246710816460100 e 120246710816500100 — Bruno pausou manualmente no Ads Manager.
  API Meta bloqueia DELETE e PAUSE em anuncios com criativo incompleto (error_subcode 2446289).
- Rocky — novas funcoes e skills criadas:
  expense-tracker (v1.1): controle financeiro via Google Sheets.
    Planilha: "Controle de Gastos Bruno 2026"
    ID: 1L1mBxfZ5yU3ej2tHEhc2mCyXcnFBNZR1e1tTVA3D6Rk
    URL: https://docs.google.com/spreadsheets/d/1L1mBxfZ5yU3ej2tHEhc2mCyXcnFBNZR1e1tTVA3D6Rk/edit
    Abas: Gastos (A:G = Data|Descrição|Categoria|Valor|Pagamento|Parcelado|Observação),
          Resumo Mensal, Análise de Fatura
    Config salva em: ~/.openclaw/workspace/memory/finance-config.json
  fitness-coach: personal trainer + coach perda de peso, treinos casa e academia.
    Perfil em: ~/.openclaw/workspace/memory/fitness-profile.json
- Rocky SOUL.md atualizado com 4 papeis: assistente pessoal, controle financeiro,
  personal trainer, Meta Ads.

---

Historico da sessao - 2026-05-18

- gog auth brneduardobot@gmail.com atualizado para incluir escopo "sheets"
  (antes: calendar, gmail — agora: calendar, gmail, sheets).
  Metodo usado: gog auth add --services calendar,gmail,sheets --manual --force-consent.
- Google Sheets API habilitada no projeto OAuth (project 470709763792, client_id comeca com 470709763792-fd1p...).
- Planilha "Controle de Gastos Bruno 2026" criada e validada:
  ID: 1L1mBxfZ5yU3ej2tHEhc2mCyXcnFBNZR1e1tTVA3D6Rk
  Abas configuradas com cabeçalhos corretos.
  Teste de append bem-sucedido: 7 colunas gravadas na linha A3:G3.
- expense-tracker SKILL.md v1.1: corrigida sintaxe gog (pipe | para separar celulas),
  conta brneduardobot@gmail.com (era brneduardo@gmail.com), colunas reais da planilha.
- finance-config.json salvo em ~/.openclaw/workspace/memory/.
- Tudo commitado e pushed para cognis-ia/clawdio-workspace-backup. Gateway reiniciado OK.
- CRITICO PENDENTE: Renovar token OpenAI Codex ate 22/05/2026 (4 dias).

---

Historico da sessao - 2026-05-18 (continuação)

- Notion integrado para Gabi e Max no workspace "Trabalho - 2025" (dono: Bruno).
  Token compartilhado salvo em .env de ambas as agentes (NOTION_TOKEN_TRABALHO).
  Token do "Espaço de Marilia" também salvo (NOTION_TOKEN) em cada .env como reserva.
  Acesso validado via API: database Atividades e página raiz Banco de Dados acessíveis.
  Página de teste criada com sucesso pelo VPS.
  Skill notion-api v1.0 instalada em workspace-gabi e workspace-max.
  OBS: .env está no .gitignore dos repos de Gabi e Max — tokens não sincronizam.
       Backups GitHub de Gabi e Max ainda não criados (pendência).
- Marilia usa email institucional marilia@janebernardelli.com.br (não Gmail).
  Não há necessidade de gog para Max por enquanto — só Notion.

---

Historico da sessao - 2026-05-19

- OpenClaw atualizado de 2026.5.3-1 para 2026.5.18.
  Método: rm -rf do diretório antigo + npm install -g openclaw@latest --prefix ~/.npm-global.
  Necessário para compatibilidade com plugin WhatsApp (@openclaw/whatsapp 2026.5.18).
- Plugin WhatsApp instalado e configurado:
  Canal: channels.whatsapp.accounts.default (em openclaw.json).
  Binding: whatsapp default -> agente main (Rocky).
  Skill whatsapp-monitor criada em workspace/skills/whatsapp-monitor/SKILL.md.
  Bruno escaneou QR code via SSH -t; status: linked e ativo.
  Rocky monitora grupos silenciosamente e avisa Bruno no Telegram quando houver novidade
  relevante sobre IA/automação. Regra gravada no SOUL.md: nunca responde nos grupos.
- Limpeza de config pós-update — entry truncada no commit anterior; nenhuma ação derivada pendente.

---

Historico da sessao - 2026-05-20

- Incidente WhatsApp analisado: a configuracao perigosa era `groupPolicy: "open"` com `groups."*".requireMention: false` sem trava de envio; isso permitia auto-respostas em grupos.
- OpenClaw WhatsApp ajustado em `/home/openclaw/.openclaw/openclaw.json` para modo preparado/passivo:
  `channels.whatsapp.enabled=false`, `sendReadReceipts=false`, `reactionLevel=off`, `ackReaction.group=never`, `actions.reactions=false`, `actions.sendMessage=false`, `actions.polls=false`.
- Conta WhatsApp default configurada com `dmPolicy=disabled`, `groupPolicy=open`, `groups."*".requireMention=false` e system prompt de leitura somente, orientando `NO_REPLY`.
- Trava principal adicionada em `session.sendPolicy`: regra `deny` para `channel=whatsapp`, mantendo `default=allow` para nao afetar Telegram e demais canais.
- `messages.groupChat.visibleReplies=message_tool` e `messages.groupChat.unmentionedInbound=room_event` definidos para tratar mensagens de grupo como contexto silencioso.
- Politica "WhatsApp Read-Only" gravada nos TOOLS.md de Rocky, Leo, BrIA, Gabi e Max: nunca enviar, comentar, reagir, criar enquete, marcar leitura ou reconhecer mensagens no WhatsApp.
- Config validada com `openclaw config validate`; gateway reiniciado e confirmado `ready`; Telegram voltou conectado em todas as contas.
- Backup da configuracao anterior salvo no VPS em `/home/openclaw/.openclaw/openclaw.json.bak-before-whatsapp-readonly`.

---

Historico da sessao - 2026-05-21

- Material editorial completo da Imersao Pixel AI Hub recebido em 2 zips:
  "Formacao agentes de IA nos negocios (Imersao)" (22.8MB · 20 aulas em 2 modulos + FAQ + transcricoes srt + github exemplo)
  e "Da teoria pra pratica - arquitetura do cerebro + templates" (6.9MB · 5 aulas + 3 templates zip: pessoal, empresa, diretoria).
- Confirmado que esse material NUNCA tinha sido enviado em sessoes anteriores. Distinto do Starter Kit OpenClaw v2.5.x do mini-curso.
- Conteudo extraido localmente em sessao temporaria; copia permanente nao mantida no D:\COGNIS\.
- INFRA.md atualizado com 3 secoes conceituais novas extraidas da Imersao:
  Arquitetura conceitual (3 cerebros, 3 niveis de memoria, areas vs agentes, 4 estagios de evolucao).
  Padroes obrigatorios (triade SOUL/AGENTS/USER, MAPA.md, _index.md, cron vs heartbeat, regra dos 3 gatilhos, 2 camadas Telegram, workspace separado p/ bot suporte).
  Seguranca em 3 camadas (Servidor + Agente + Processo, OWASP LLM Top 10 2026, ~90% reducao de superficie).
- Pendencias ampliadas com 9 itens novos derivados da Imersao (G a O): criar cerebro diretoria,
  MAPA.md nos workspaces, _index.md em skills, heartbeat por estado, audit crons, master coordenador,
  whitelist IDs Telegram, estrutura canonica de areas, ler cerebro modelo do github da imersao.
- Identificado overlap entre pendencias do mini-curso (A-F) e da Imersao (G-O):
  A ~ H (TOOLS->MAPAs vs MAPA.md geral), B ~ J (Heartbeat vs heartbeat por estado), E ~ K (meta-cron vs audit crons).
- Decisao pendente: qual agente serve como master coordenador (candidato Rocky) e qual serve a diretoria.
- Templates Pixel disponiveis para consulta futura:
  template-pessoal-0.1.0 (18 arquivos, skill cerebro+sync-pessoal).
  template-empresa-0.1.0 (CLAUDE.md, MAPA.md, agente geral-empresa com SOUL/AGENTS/HEARTBEAT, areas vazias, 9 slash commands).
  template-diretoria-0.1.0 (mesma base + CODEOWNERS, PR template, areas financeiro/rh/juridico/governanca).
- Github de exemplo da imersao (imersao-openclaw-negocios-main) tem cerebro populado com 4 agentes
  (assistente, marketing, bot-suporte) usavel como referencia de padrao SOUL/AGENTS/HEARTBEAT.
- Merge feito: versao local (que estava em 2026-05-14) sincronizada com remote (2026-05-19) antes de aplicar mudancas e fazer push.
