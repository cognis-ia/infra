INFRA — OpenClaw (Bruno Eduardo)
Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo.
Última atualização: 2026-07-08 (cutover Rocky OpenClaw -> Hermes concluído)

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
  Hoje no stack: existe em `~/.openclaw/cerebro-diretoria/` (repo privado cognis-ia/cerebro-diretoria).

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
  - Audit crons — auditoria automática dos agentes.                       [parcial: Rocky Auditor semanal ativo]
  - Logs completos — toda ação com timestamp.                             [validar]
  - Rotação de tokens — trocar chaves a cada 90 dias.                     [pendência aberta — OpenAI exposta]
  - Memória no GitHub — backup de decisões críticas.                      [parcial: backups por agente + governança + diretoria ok]

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

Agentes OpenClaw + runtimes Hermes

| Agente | ID | Emoji | Papel | Canal Telegram | Workspace | GitHub backup |
|--------|-----|-------|-------|---------------|-----------|---------------|
| Rocky | main (default) | Legado OpenClaw do Rocky; sem uso canônico após cutover para Hermes em 2026-07-08 | Telegram default desativado | ~/.openclaw/workspace | cognis-ia/clawdio-workspace-backup |
| Leo | leo | Agente profissional (COGNIS IA) | telegram:leo (@CG_Leo_Bot) | ~/.openclaw/workspace-leo | cognis-ia/leo-workspace-backup |
| BrIA | bria | Braço operacional Cognis na Bernardelli (tráfego, Hotmart, Astron, Nicochat, relatórios) | telegram:bria (@BE_BrIA_bot) | ~/.openclaw/workspace-bria | cognis-ia/bria-workspace-backup |
| Gabi | gabi | Criativa/estratégica da Jane — Bernardelli Ensino | telegram:gabi (@BE_Gabi_bot) | ~/.openclaw/workspace-gabi | cognis-ia/gabi-workspace-backup |
| Max | max | Operacional da Marilia — Bernardelli Ensino | telegram:max (@BE_Max_bot) | ~/.openclaw/workspace-max | cognis-ia/max-workspace-backup |
| Sofia | sofia | Legado knowledge-base Astron/Bernardelli | sem canal publico | ~/.openclaw/workspace-sofia | cognis-ia/sofia-workspace-backup |
| Atlas | atlas | Gestor institucional de agentes, auditoria e lifecycle | telegram:atlas (@Cognis_Atlas_bot) | ~/.openclaw/workspace-atlas | cognis-ia/atlas-workspace-backup |

Runtime Hermes ativo fora do OpenClaw:

| Agente | Runtime | Papel | Canal Telegram | Base |
|--------|---------|-------|----------------|------|
| Rocky | Hermes | Agente pessoal canônico do Bruno a partir de 2026-07-08 | @rocky_bruno_hermes_bot | ~/.hermes |
| Lia | Hermes | Suporte vivo Bernardelli | @BE_Lia_Suporte_bot | ~/.hermes |

GitHub org: cognis-ia — token no VPS em ~/.openclaw/workspace/.env

Perfis Bernardelli:
- BrIA: braço operacional da Cognis na Bernardelli — tráfego (Meta Ads), Hotmart, Astron Members, Nicochat, criação de relatórios. Reporta a Bruno; não atende aluna direto (essa é a Lia)
- Gabi: criativa, conteúdo, voz da marca Jane — mentora de arte
- Max: operacional, analítica, parceira da Marilia
- Sofia: legado de catalogo/knowledge base Astron/Bernardelli
- Lia: suporte vivo Bernardelli via Hermes/Telegram; substitui Sofia nas rotinas operacionais correntes e no fechamento diario

---

Segundos Cérebros

| Workspace | Quem usa | GitHub |
|-----------|----------|--------|
| ~/.openclaw/workspace-shared/ | Rocky + Leo | cognis-ia/shared-workspace-backup |
| ~/.openclaw/workspace-bria-shared/ | BrIA (isolado) | cognis-ia/bria-shared-backup |
| ~/.openclaw/cerebro-governanca/ | Constituição/padrões dos 6 agentes | cognis-ia/cerebro-governanca |
| ~/.openclaw/cerebro-cognis/ | **Cérebro empresa Cognis IA** (template-empresa Pixel; gestor: Atlas; áreas: infraestrutura, contas-atendidas, produtos) | cognis-ia/cerebro-cognis |
| ~/.openclaw/cerebro-diretoria/ | Sensível/diretoria (Bruno + Jane) | cognis-ia/cerebro-diretoria |
| ~/.openclaw/cerebro-bernardelli-areas/ | Operacional compartilhado Bernardelli (BrIA/Gabi/Max/Lia; Sofia legado) | cognis-ia/cerebro-bernardelli-areas |

BrIA, Gabi, Max e Lia usam `cerebro-bernardelli-areas` para conhecimento operacional compartilhado. Sofia permanece apenas como legado/knowledge-base enquanto existir no stack. Rocky e Leo não usam este cérebro no dia a dia.

`cerebro-cognis` é o cérebro empresa Cognis IA, criado em 2026-06-15 a partir do template-empresa-0.1.0 do Pixel AI Hub. Estrutura completa: `agentes/atlas/` (gestor) + `areas/{infraestrutura,contas-atendidas,produtos}/` + `empresa/contexto/` + `empresa/skills/` + `inbox/bruno/` + `onboarding/`. Branch padrão `main`; trabalho diário em `staging`.

---

Automações ativas (resumo atual)

OpenClaw cron nativo mantido:

| ID | Nome | Agente | Horário | Status |
|----|------|--------|---------|--------|
| 2afeecdc | atlas-auditoria-agentes-semanal | atlas | segunda 07h | ok |
| eb77d0d9 | atlas-auditoria-skills-mensal | atlas | dia 1, 08h15 | ok |

Systemd user timers ativos:

| Timer | Agente/uso | Horário |
|-------|------------|---------|
| heartbeat-runner-bria.timer | BrIA heartbeat por estado | 08h02, 12h02, 16h02, 20h02 |
| heartbeat-runner-leo.timer | Leo heartbeat por estado | 08h04, 12h04, 16h04, 20h04 |
| heartbeat-runner-gabi.timer | Gabi heartbeat por estado | 08h06, 12h06, 16h06, 20h06 |
| heartbeat-runner-max.timer | Max heartbeat por estado | 08h08, 12h08, 16h08, 20h08 |
| daily-handoff-leo.timer | handoff diario Leo para Atlas | 21h32 |
| daily-handoff-bria.timer | handoff diario BrIA para Atlas | 21h34 |
| daily-handoff-gabi.timer | handoff diario Gabi para Atlas | 21h36 |
| daily-handoff-max.timer | handoff diario Max para Atlas | 21h38 |
| daily-handoff-lia.timer | handoff diario Lia para Atlas | 21h40 |
| atlas-daily-consolidation.timer | consolidacao diaria dos handoffs | 22h10 |
| atlas-daily-distribution.timer | distribuicao diaria do staging | 22h12 |
| atlas-daily-promotion.timer | promocao canônica com commit/push | 22h14 |
| backup-workspace-rocky.timer | backup Git Rocky | 23h00 |
| backup-workspace-leo.timer | backup Git Leo | 23h05 |
| backup-workspace-bria.timer | backup Git BrIA | 23h10 |
| backup-workspace-gabi.timer | backup Git Gabi | 23h15 |
| backup-workspace-max.timer | backup Git Max | 23h20 |
| backup-workspace-sofia.timer | backup Git Sofia | 23h25 |
| cognis-consolidar.timer | **consolidação noturna MVP cerebro-cognis** (Atlas writes canônicos + sync staging→main + Telegram) | 02:00 BRT |
| vigiar-markdowns-gabi.timer | watcher Markdown Gabi | 20h00 |
| vigiar-markdowns-max.timer | watcher Markdown Max | 20h00 |

Timers desativados no cutover do Rocky para Hermes em 2026-07-08:

- `heartbeat-runner-rocky.timer`
- `daily-handoff-rocky.timer`
- `rocky-revisao-dia.timer`
- `rocky-focus-checkin.timer`

Permanece ativo por usar o mesmo workspace canônico, independentemente do runtime:

- `backup-workspace-rocky.timer`

Crons nativos antigos/desativados por arquitetura quebrada em sessão isolated: rocky-heartbeat, bria-heartbeat, vigiar-markdowns-gabi/max, rocky-backup-diario.

Cutover Rocky 2026-07-08:

- cron OpenClaw restante do `agent:main` removido (`custodia-filha-check-*`);
- Rocky-Hermes passa a ler `SOUL.md`, `HEARTBEAT.md`, `MEMORY.md` e `USER.md` canônicos do workspace antigo;
- workspace do Rocky ganhou pontes locais para:
  - `segundo-cerebro -> ~/.openclaw/workspace-shared`
  - `cerebro-cognis -> ~/.openclaw/cerebro-cognis`
  - `cerebro-governanca -> ~/.openclaw/cerebro-governanca`

Pipeline atual de fechamento diario:

1. agentes geram handoff diario por `systemd`;
2. Atlas consolida os handoffs em `reports/daily/master/`;
3. Atlas distribui memoria duravel para staging nos destinos canonicos;
4. Atlas promove o staging para memoria versionada com commit/push nos repos com upstream;
5. itens sensiveis continuam retidos fora do cerebro operacional, aguardando revisao humana.

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
  Agentes: BrIA, Gabi, Max, Sofia (legado)
  Club ID: 8194 (Pintando Telas) — 908 alunas
  Credenciais: ASTRON_AM_KEY, ASTRON_AM_SECRET, ASTRON_CLUB_ID=8194
  Base: https://api.astronmembers.com.br/v1.0/
  Auth: Basic HTTP (user=AM_KEY senha=AM_SECRET)
  Skill: workspace-max/skills/astron-members-api/SKILL.md
  Sofia: workspace-sofia/skills/astron-course-mapper/SKILL.md + scripts/astron_discover.py
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
Sofia: astron-course-mapper, course-knowledge-builder

---

Pendências

URGENTE
5. Renovar token OpenAI Codex — ate 22 maio 2026 (SSH com TTY)
6. Rotacionar chave OpenAI — exposta em historico Git
7. Rotacionar tokens Notion de Gabi/Max (valores foram encontrados em historico local antigo; repos novos foram sanitizados antes do primeiro push).
8. Endurecer Control UI do gateway: remover `allowInsecureAuth=true` e tirar `controlUi.token` do `openclaw.json` para fonte menos exposta.
9. Revisar credenciais injetadas por drop-ins do systemd (`openai.conf`, `gog-account.conf`, integrações Hermes/Lia) e consolidar fila de rotação.

Curso Openclaw (mini) — implementação pendente (ordem de prioridade)
A. TOOLS.md → MAPAs distribuídos — Rocky e Leo (A6)
   Migrar TOOLS.md monolítico para MAPA.md em cada pasta do workspace
   (memory/, content/, skills/, archive/). Gabi/Max/BrIA: verificar estado.
B. Heartbeat por estado (A9) — CONCLUIDO/PARCIAL.
   Rocky e BrIA concluídos via heartbeat-runner systemd em 2026-05-27.
   Leo, Gabi e Max concluídos/testados via heartbeat-runner systemd em 2026-06-02.
   Crons nativos antigos foram desativados porque ficavam funcionalmente blocked em sessão isolated.
   Sofia e Atlas seguem sem heartbeat-runner dedicado por desenho: Sofia é knowledge-base; Atlas tem auditoria semanal.
C. USER.md com 8 blocos — Rocky (A5)
   Verificar e completar: perfil, negócios, família, equipe, tom,
   restrições, valores, contexto operacional.
D. AGENTS.md atualizado em todos os workspaces (A5/A13) — CONCLUIDO.
   Adendo de governança aplicado aos 5 agentes originais em 2026-05-22.
   Sofia já nasceu em 2026-05-28 com marcador BEGIN_COGNIS_GOVERNANCA_ADENDO_v0.1.0 e Auto-Resolver.
E. Crons: Revisão do Dia (18h) e meta-cron de auditoria (7h) — CONCLUIDO.
   Meta-cron de auditoria criado em 2026-05-22:
   rocky-auditoria-agentes-semanal, segunda 07:00 America/Sao_Paulo, agente main, Telegram Bruno.
   Revisão do Dia criada em 2026-05-28 via systemd:
   rocky-revisao-dia.timer, diariamente 18:00 America/Sao_Paulo, envia resumo deterministico via Telegram.
F. Mission Control (A14) — CONCLUIDO/MVP em 2026-05-28.
   - VPS: ~/.openclaw/mission-control/
   - Local: D:\COGNIS\Curso Openclaw\mission-control\
   - Gera index.html + data/status.json read-only.
   - Timer systemd: mission-control-refresh.timer (a cada 30min).

Imersão Pixel AI Hub — gaps de arquitetura (ver seções conceituais no topo)
G. Cérebro de diretoria — CONCLUIDO em 2026-05-22.
   - Repo privado cognis-ia/cerebro-diretoria criado e clonado em ~/.openclaw/cerebro-diretoria.
   - Estrutura inicial: financeiro, rh, juridico, governanca, sociedade-bernardelli, inbox, staging.
   - CODEOWNERS e PR template criados; branch protection falhou via API (403), manter disciplina manual por enquanto.
H. MAPA.md inexistente nos workspaces atuais.
   - Auditar cada workspace (Rocky, Leo, BrIA, Gabi, Max, shared, bria-shared).
   - Garantir MAPA.md em raiz e em cada subárea quando houver áreas separadas.
   - Sobrepõe parcialmente com pendência A (TOOLS.md → MAPAs do mini-curso).
I. _index.md em skills.
   - Validar que cada pasta skills/ dos 6 agentes tem _index.md atualizado.
J. Heartbeat baseado em estado (não só cron) — CONCLUIDO/PARCIAL.
   - Rocky e BrIA: concluído via heartbeat-runner systemd + LLM one-shot.
   - Leo, Gabi e Max: concluído em 2026-06-02; services testados com HEARTBEAT_OK.
   - Sofia/Atlas: sem runner dedicado por enquanto; manter avaliação futura.
   - Sobrepõe com pendência B.
K. Audit crons (camada 3 de segurança) — PARCIAL.
   - Atlas Auditor semanal ativo via OpenClaw cron `atlas-auditoria-agentes-semanal`.
   - Skill auditoria-agentes criada no Rocky em 2026-05-22 e atualizada para v0.2.0 em 2026-05-25.
   - Atualizada em 2026-05-28 para incluir Sofia.
   - Roda semanalmente: arquivos canônicos, adendo de governança, memory recente,
     git limpo, commits recentes, upstream, possíveis segredos, scratch/backups e crons com erro.
   - Primeiro relatório salvo em ~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-agentes-2026-05-22.md.
   - Relatório mais recente: auditoria-agentes-2026-06-02.md com 7 agentes, 244/245 checks (99.6%).
   - Único médio atual: Atlas sem upstream GitHub, bloqueado até token rotation/criação do repo `atlas-workspace-backup`.
   - Evoluir depois para auditoria mensal mais profunda.
L. Gestor de agentes (master coordenador — estágio 4) — PARCIAL/EVOLUINDO.
   - Decisão 2026-06-02: não misturar Rocky pessoal com gestor institucional.
   - Atlas criado como agente separado para criar, gerenciar e auditar agentes/estruturas.
   - Auditoria semanal migrada de Rocky/main para Atlas/atlas.
   - Coordenação operacional corretiva ainda depende de autorização explícita do Bruno.
M. Permissionamento Telegram — CONCLUIDO em 2026-05-28.
   - Todos os 5 bots Telegram têm dmPolicy=allowlist, allowFrom explícito,
     groupAllowFrom explícito e groups.*.requireMention=true.
   - Rocky/default: Bruno (1950767646).
   - Leo: Bruno (1950767646).
   - BrIA: Bruno (1950767646).
   - Gabi: Bruno (1950767646) + Jane (938877898).
   - Max: Bruno (1950767646) + Marilia (8443736822).
   - WhatsApp já está read-only desde 2026-05-20.
N. Estrutura áreas/ canônica nos workspaces compartilhados — CONCLUIDO/PARCIAL em 2026-05-28.
   - Criado repo privado `cognis-ia/cerebro-bernardelli-areas`.
   - Clone no VPS: `~/.openclaw/cerebro-bernardelli-areas/`.
   - Estrutura criada no padrão Pixel:
     `areas/{atendimento,conteudo,marketing,operacoes,produtos,tecnologia}/{contexto,skills,rotinas,projetos}`.
   - BrIA, Gabi, Max e Sofia foram conectados ao novo cérebro via `AGENTS.md`/MAPA operacional.
   - `workspace-bria-shared` permanece como legado da BrIA e deve ser migrado com calma quando houver demanda real.
   - `workspace-shared` (Rocky+Leo) ainda não foi reorganizado; fazer apenas quando houver dor operacional.
O. Cérebro modelo do GitHub do curso.
   - imersao-openclaw-negocios-main.zip tem cérebro de exemplo populado com 4 agentes
     (assistente, marketing, bot-suporte) com SOUL+AGENTS+HEARTBEAT completos.
   - Vale ler para padronizar SOUL/AGENTS dos agentes atuais antes de criar novos.

Infraestrutura
1. GitHub backup Gabi e Max — CONCLUIDO em 2026-05-22 (snapshots sanitizados, sem historico com tokens Notion)
2. Cron bria heartbeat sem chatId — CONCLUIDO/substituido em 2026-05-27. Diagnostico real: crons agentTurn em sessão isolated ficavam blocked; solução atual é heartbeat-runner systemd para Rocky e BrIA. rocky-backup-diario também foi migrado para systemd em 2026-05-26 (sessao 9).
4. Segundo cérebro Gabi e Max — CONCLUIDO em 2026-05-28 via `cerebro-bernardelli-areas`.
8. Deletar @Clawdio_Bruno_bot no BotFather — acao manual Bruno
9. Verificar se allowFrom da Gabi devia ter ID da Jane (938877898) — CONCLUIDO em 2026-05-28.
10. Max allowlist — CONCLUIDO em 2026-06-02. `allowFrom` e `groupAllowFrom` da Max confirmados com Bruno + Marilia no `openclaw.json`.
11. PAT GitHub antigo do Rocky — CONCLUIDO em 2026-06-02. Token revogado manualmente por Bruno; validado localmente com `git ls-remote origin` ainda funcional no repo `cognis-ia/clawdio-workspace-backup`.

---

Regra absoluta

NUNCA assinar, contratar ou comprar qualquer coisa sem o expresso consentimento do Bruno Eduardo.

---

Atualização deste arquivo

Ao final de cada sessão: "Atualize o INFRA.md com o que fizemos hoje."
Claude atualiza E faz push para cognis-ia/infra no GitHub.
Nunca criar um novo arquivo — sempre editar este.

---

Historico da sessao - 2026-05-28 (sessao 21 — Sofia/Astron e auditoria 6 agentes)

- Criada Sofia, novo agente especialista em cursos da Bernardelli Ensino.
  - ID OpenClaw: `sofia`.
  - Workspace: `~/.openclaw/workspace-sofia`.
  - Agent dir: `~/.openclaw/agents/sofia/agent`.
  - Modelo: `openai/gpt-5.4`.
  - Canal publico: nenhum nesta fase.
- Repo privado criado e sincronizado:
  - `cognis-ia/sofia-workspace-backup`.
  - Commits principais:
    - `feat: bootstrap sofia curso specialist`
    - `feat: mapeia catalogo astron inicial`
    - `chore: alinha sofia a governanca`
- Estrutura Sofia criada seguindo o padrao Pixel:
  - `IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`, `MAPA.md`, `MEMORY.md`, `HEARTBEAT.md`, `TOOLS.md`.
  - `catalogo/`, `transcricoes/`, `knowledge/`, `pendencias/`, `skills/`, `memory/`.
  - Skills iniciais: `astron-course-mapper` e `course-knowledge-builder`.
- Sofia conectou na AstronMembers em modo read-only e gerou catalogo inicial.
  - Club ID: 8194.
  - Clubes encontrados: 1.
  - Planos encontrados: 92.
  - Aulas ativas encontradas: 491.
  - Cursos inferidos por `course_id`: 37.
  - Arquivos gerados: `catalogo/astron-discovery.*`, `catalogo/cursos.*`, `catalogo/curso-*.md`, `pendencias/astron-api.md`.
  - Limitacao: a API inicial trouxe IDs/metadados de aulas, mas ainda nao nomes humanos completos de cursos/modulos em todos os niveis.
- `cerebro-bernardelli-areas` atualizado para registrar Sofia:
  - `MAPA.md`.
  - `areas/operacoes/contexto/topologia-agentes.md`.
  - `areas/produtos/contexto/produtos-conhecidos.md`.
  - `areas/tecnologia/contexto/plataformas.md`.
  - Commit: `e1511a0 docs: registra sofia e catalogo astron inicial`.
- Sofia alinhada a governanca v0.2:
  - AGENTS com `BEGIN_COGNIS_GOVERNANCA_ADENDO_v0.1.0`.
  - Auto-Resolver.
  - SOUL com Tom especifico e Continuidade v0.2.
  - IDENTITY com Territories e Historico de versoes.
  - HEARTBEAT por estado.
  - `skills/_index.md` e `memory/2026-05-28.md`.
- Backup systemd da Sofia criado e testado:
  - `backup-workspace-sofia.service`.
  - `backup-workspace-sofia.timer`.
  - Schedule: diariamente 23:25 America/Sao_Paulo.
  - Teste manual: sucesso; tree clean e sincronizado com origin.
- Auditoria oficial atualizada para 6 agentes:
  - Rocky Auditor (`auditoria-agentes`) agora inclui Sofia.
  - Commit Rocky: `c4dbdf9 feat(auditoria): inclui sofia no relatorio`.
  - Alto pendente do BrIA resolvido com commit dos relatorios Arte Derramada:
    `e2d0e49 docs(reports): adiciona relatorio arte derramada 2026-05-28`.
  - Auditoria final: 210/210 checks (100.0%), 0 criticos, 0 altos, 0 medios, 0 baixos.
  - Commit governanca: `cb62d7e docs(auditoria): inclui sofia no relatorio 2026-05-28`.
- Tokens/credenciais Astron nao foram rotacionados nesta fase por decisao anterior:
  deixar tokens por ultimo. Credenciais continuam fora dos arquivos versionados e devem entrar na etapa de rotacao/migracao.

---

Historico da sessao - 2026-06-02 (sessao 25 — Rocky infra-manager)

- Diagnostico da Max fechado:
  - O bloqueio da Marilia era de permissionamento de entrada, nao de token ou bot offline.
  - `dmPolicy: allowlist` exige combinacao correta entre `allowFrom` / `groupAllowFrom` no `openclaw.json`.
  - Estado final confirmado da Max: Bruno (`1950767646`) + Marilia (`8443736822`) autorizados.
- `INFRA.md` revisado para refletir o estado real da infra:
  - Max marcada como concluida.
  - Lista de pendencias reorganizada por risco real.
  - `allowInsecureAuth` e credenciais em drop-ins promovidos a pendencias explicitas.
- Incidente operacional identificado durante a sessao:
  - Reiniciar `openclaw-gateway` no meio do turno derruba o app-server ativo da sessao Codex.
  - Log observado: `SIGTERM` seguido de `codex app-server client closed before turn completed`.
  - Regra pratica: evitar restart do gateway durante investigacao interativa, salvo necessidade real.
- Timer `rocky-revisao-dia.timer` corrigido sem restart do gateway:
  - Havia alerta de `Timezone` invalido.
  - Arquivo ajustado e `systemd` reloaded sem derrubar o runtime principal.
- Mapeamento de risco de credenciais concluido:
  - Risco estrutural mais serio encontrado no `openclaw.json`: `controlUi.token` em arquivo canônico + `allowInsecureAuth=true`.
  - OpenAI em uso cruzado entre `openclaw.json`, drop-ins do gateway e runtime Hermes/Lia.
  - Tokens Notion concentrados em Gabi/Max.
  - PAT GitHub antigo do Rocky parecia o item mais seguro para matar primeiro.
- Priorizacao de rotacao definida:
  1. PAT GitHub antigo do Rocky.
  2. Tokens Notion de Gabi/Max.
  3. Credenciais OpenAI com coordenacao entre OpenClaw e Hermes/Lia.
  4. `controlUi.token` do gateway por ultimo, porque impacta o acesso do operador.
- Acao executada e validada:
  - Bruno revogou manualmente o PAT GitHub antigo do Rocky.
  - Validacao local apos a revogacao:
    - `git ls-remote origin` continuou funcionando no repo `cognis-ia/clawdio-workspace-backup`.
    - `openclaw-gateway.service` permaneceu ativo e estavel.
  - Conclusao: o token deletado era o antigo/exposto, nao o token ativo do backup.
- Observacao lateral:
  - Nesta VPS nao existe a unit `backup-workspace-github.timer`; os backups ativos sao os timers individuais `backup-workspace-*.timer` por agente.

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

---

Historico da sessao - 2026-05-22

- Retomada da sessao iniciada no Claude Opus 4.7 apos criacao do cerebro-governanca e cerebro-diretoria.
- Auditoria as-is dos 5 agentes feita antes pelo Claude:
  AGENTS.md dos 5 era basicamente Starter Kit; Rocky mais completo; Gabi/Max sem heartbeat ativo;
  MEMORY.md da Max fraco; nenhum agente conhecia regra dos 3 gatilhos.
- Repo privado cognis-ia/cerebro-governanca criado:
  clone VPS em ~/.openclaw/cerebro-governanca/; copia local em D:\COGNIS\Curso Openclaw\cerebro-governanca\.
  Conteudo v0.1.0: CONSTITUICAO.md, padroes SOUL/USER/AGENTS/HEARTBEAT/MAPA/MEMORY/TOOLS,
  regra dos 3 gatilhos, seguranca 3 camadas, checklist de auditoria e mapa dos agentes.
- Repo privado cognis-ia/cerebro-diretoria criado:
  clone VPS em ~/.openclaw/cerebro-diretoria/.
  Areas: financeiro, rh, juridico, governanca, sociedade-bernardelli.
  Fluxo: inbox -> staging -> revisao humana -> main. Sem auto-commit para dados sensiveis.
  Branch protection via API falhou com 403; manter revisao manual enquanto Jane nao estiver como collaborator.
- Housekeeping antes do adendo:
  remote do Rocky corrigido para remover PAT GitHub da URL; token ainda deve ser revogado/rotacionado.
  repos cognis-ia/gabi-workspace-backup e cognis-ia/max-workspace-backup criados.
  Léo confirmado com origin e backup apontando para cognis-ia/leo-workspace-backup.
  Lixo regeneravel removido: tmp/wa_* do Rocky, reports/__pycache__ da BrIA, backups .bak antigos de Gabi/Max.
  .gitignore atualizado em Rocky e BrIA para evitar retorno de scratch/cache.
- Backups dos workspaces:
  Rocky: commit c55232b backup-2026-05-22 + 2bc53b2 governanca-agents-adendo-2026-05-22.
  Leo: commit b1c6e7b backup-2026-05-22 + 2f9a1db governanca-agents-adendo-2026-05-22.
  BrIA: commit 85aefef backup-2026-05-22 + c14cddc governanca-agents-adendo-2026-05-22.
  Gabi: snapshot inicial sanitizado 8d002cc + adendo d5bf95e.
  Max: snapshot inicial sanitizado 18ee053 + adendo 4610b2a.
- Tokens Notion reais foram encontrados em skills/notion-api/SKILL.md de Gabi/Max antes do primeiro push.
  Arquivos atuais foram sanitizados com [REDACTED_NOTION_TOKEN].
  Historico local de Gabi/Max foi substituido por branch orphan sanitizada antes do primeiro push.
  Pendencia urgente: rotacionar os tokens Notion mesmo assim.
- AGENTS-adendo.md da governanca aplicado nos 5 workspaces com marcador:
  BEGIN_COGNIS_GOVERNANCA_ADENDO_v0.1.0.
  Validado: cada AGENTS.md contem exatamente 1 marcador e working trees ficaram limpas.

- Rocky Auditor implementado conforme estrutura da Imersão Pixel (gestor dos agentes read-only):
  skill auditoria-agentes v0.1.0 criada em ~/.openclaw/workspace/skills/operacional/auditoria-agentes/.
  Commits Rocky: 22cea70 feat: cria skill auditoria-agentes; 2cfd2b9 chore: ignora cache python da auditoria.
- Primeiro relatório de auditoria salvo em cerebro-governanca:
  ~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-agentes-2026-05-22.md.
  Resultado: 139/150 checks (92.7%), 0 críticos, 2 altos, 7 médios, 2 baixos.
  Altos atuais: cron Monitorar jogos do Corinthians em erro; cron vigiar-markdowns-gabi em erro.
- Cron semanal criado para o Rocky Auditor:
  id 2afeecdc-c292-4521-8a3b-1bcd8f51d0af, nome rocky-auditoria-agentes-semanal, segunda 07:00 America/Sao_Paulo, agente main, session isolated, Telegram Bruno.
- Governança atualizada com checklist apontando para auditoria-agentes e relatório versionado.
  Commits governança: 53b0108 feat: registra primeira auditoria dos agentes; 1355dc4 chore: atualiza primeira auditoria apos instalacao.

- Altos da primeira auditoria atacados:
  cron Monitorar jogos do Corinthians e cron vigiar-markdowns-gabi editados com toolsAllow explicito e failureAlert.
  Corinthians migrado para session isolated; execucao manual passou a status ok.
  Gabi passou de error para ok no scheduler, mas a rotina ainda relata bloqueio funcional por indisponibilidade de exec/read/write no runtime; tratar como refinamento estrutural futuro (script deterministico ou runner externo), nao como alerta alto do auditor.
- Auditoria rerodada apos correcoes:
  Resultado atualizado: 141/150 checks (94.0%), 0 criticos, 0 altos, 7 medios, 2 baixos.
  Commit governanca: ee1f5a6 chore: atualiza auditoria sem alertas altos.

- Watchers Markdown de Gabi e Max migrados para rotina deterministica fora do agente:
  skills criadas em skills/operacional/vigiar-markdowns/ nos workspaces Gabi e Max.
  O script roda via systemd --user, le git/status diretamente e envia Telegram via openclaw message send somente quando houver novidade.
  Timers ativos: vigiar-markdowns-gabi.timer e vigiar-markdowns-max.timer, ambos diarios as 20:00 America/Sao_Paulo.
  Crons antigos OpenClaw desativados: c8341652-9185-4a38-a4b5-7d200bb8c6ba (Gabi) e eb52f8fe-cd22-4601-846f-b152c77dc207 (Max).
  Estado operacional memory/md-watch-state.json removido do Git e mantido local/ignorado para nao sujar worktree a cada execucao.
  Commits Gabi: b9d0df4 feat watcher, ebf7300 sync state, 87bd8b0 estado local.
  Commits Max: a620872 feat watcher, 67cb32f sync state, 4e421e6 estado local.
  Unit files versionados em cognis-ia/infra: systemd/user/vigiar-markdowns-{gabi,max}.{service,timer}.
- Auditoria rerodada apos migracao deterministica:
  Resultado: 141/150 checks (94.0%), 0 criticos, 0 altos, 7 medios, 2 baixos.
  Commit governanca: 8eee16b chore: atualiza auditoria apos watchers deterministos.

- Heartbeats de Gabi e Max ativados conforme padrao Pixel/governanca:
  Gabi: HEARTBEAT.md substituido por checks de estado para demandas criativas, agenda/email Jane, Notion, watcher markdown e regra dos 3 gatilhos.
  Commit Gabi: af22570 feat: heartbeat por estado da Gabi.
  Max: HEARTBEAT.md substituido por checks de estado operacional; MEMORY.md expandido com contexto Bernardelli, pessoas, ferramentas, autoridade, decisoes e licoes aprendidas.
  Commit Max: 3537ce3 feat: heartbeat e memoria operacional da Max.
- Auditoria rerodada apos heartbeats:
  Resultado: 144/150 checks (96.0%), 0 criticos, 0 altos, 4 medios, 2 baixos.
  Gabi e Max ficaram 30/30 (100%) no Rocky Auditor.
  Commit governanca: 5e951ae chore: atualiza auditoria apos heartbeat gabi max.

- Auditoria dos 5 agentes fechada em 100%:
  Leo: USER.md expandido para contexto profissional COGNIS IA e memory/2026-05-22.md criada.
  Commit Leo: 0ed66d2 feat: completa user e memoria recente do leo.
  Rocky: skills/documentos/SKILL.md criado como indice da area de documentos; backup antigo de TOOLS arquivado fora da raiz.
  Commits Rocky: fe9d179 feat: indice de skills documentos; 309324a chore: arquiva backup antigo de tools.
  BrIA: skills/design/SKILL.md criado como indice da area de design; relatorios Arte Derramada movidos da raiz para reports/arte-derramada/.
  Commits BrIA: 1396eb8 feat: indice de skills design; a426b18 chore: organiza relatorios arte derramada.
  Resultado final do Rocky Auditor: 150/150 checks (100.0%), 0 criticos, 0 altos, 0 medios, 0 baixos.
  Commit governanca: 0b19f01 chore: auditoria agentes 100 por c
Historico da sessao - 2026-05-22 (continuacao via Cowork)

- Skill alternativa criada em paralelo via Cowork: skills/operacional/auditor-integridade-agentes/ (Bash, 540 linhas).
  Foi desenvolvida sem conhecimento da skill auditoria-agentes do codex (que e em Python e mais robusta).
  Decisao Bruno: deixar as 2 skills coexistirem por enquanto. A do codex e o caminho de producao
  (referenciada pelo cron rocky-auditoria-agentes-semanal). A em Bash fica como alternativa standalone.
  Commit Rocky: 6d60e8e chore: fecha gaps da auditoria + instala skill auditor-integridade-agentes.
- Cron rocky-auditoria-agentes-semanal validado end-to-end via execucao manual:
  Comando: openclaw cron run 2afeecdc-c292-4521-8a3b-1bcd8f51d0af
  Duracao: 63s
  Status: ok, delivered=true
  Resultado: 150/150 checks (100%), Telegram do Bruno (1950767646) recebeu o resumo conforme esperado.
  Proxima execucao automatica: segunda-feira 25/05/2026 07:00 BRT.
- Higiene adicional fechada nesta sessao:
  IDENTITY.md de Rocky/Leo/Gabi/Max ganhou linha 'Agent ID: <slug>' (formato dossie do BrIA generalizado).
  skills/_index.md gerado automaticamente em todos os 5 workspaces (34/31/37/34/31 skills indexadas).
  chmod 600 nos .env de Gabi e Max (permissao estava 664).
  Working tree de todos os 5 workspaces limpo + push sincronizado com origin/main.
- Pendencias urgentes seguem em aberto (item de seguranca):
  Rotacionar PAT GitHub antigo do Rocky (exposto em URL antes da correcao).
  Rotacionar NOTION_TOKEN_TRABALHO de Gabi e Max (apareceram em logs antes da sanitizacao).
  Rotacionar NOTION_TOKEN reserva da Marilia.
  Renovar token OpenAI Codex (prazo 22/05/2026 = hoje).

Historico da sessao - 2026-05-25 (sessao 7 — Cowork + codex em paralelo)

- Bruno enviou Downloads.rar (75MB) com material consolidado da Pixel AI Hub:
  Mod 2 (Mini-curso v2 Managed — 17 aulas + Starter Kit v2.5.7 + Templates + Cases + Refs + Transcricoes),
  Mod 3 (Imersao — ja tinhamos da sessao 5),
  Mod 4 e Mod 6 (Da teoria pra pratica — versoes 22/05 e 25/05, identicas entre si e ao que ja tinhamos),
  Mod 5 (Pixel AI Hub HQ — so meta-orientacao geral).
- Conteudo realmente novo identificado: Mini-curso v2 inteiro + Templates da Amora (referencia madura mes 6+).
- Conteudo duplicado: Imersao Mod 3, Da teoria pra pratica Mod 4/6 (templates 0.1.0 idem ao que tinhamos).

- Frente A executada: Benchmark qualitativo Amora 4.0 vs os 5 agentes do Bruno.
  Documento gerado: D:\COGNIS\Curso Openclaw\BENCHMARK-AMORA-2026-05-25.md
  17 padroes da Amora analisados; 5 quick wins priorizados (Tom especifico, Continuidade,
  IDENTITY dossie expandido, Regra de Prioridade explicita pra Rocky, Protocolo Repeticao->Skill).

- Fase 1 do plano executada: constituicao bumpada para v0.2.0.
  Commit cerebro-governanca: c11b663 feat: bumpa constituicao para v0.2.0 - quick wins da Amora
  Mudancas (8 arquivos, +463 / -32 linhas):
  - SOUL-template.md: +2 blocos obrigatorios (Tom especifico proibindo bajulacao + Continuidade)
  - IDENTITY-template.md: formato dossie expandido (Territories, cerebros compartilhados, historico, ponteiros).
    Tamanho-alvo bumpa de 15-25 linhas para 1200-1800 bytes.
  - AGENTS-adendo.md: matriz Auto-Resolver (Age sem perguntar | Pede antes | Nunca faz) com tabelas por situacao.
  - USER-template.md: +3 blocos OPCIONAIS Modo A (Vocabulario/Expressoes, Rotina detalhada, Tom por plataforma).
  - CONSTITUICAO.md: versao 0.1.0 -> 0.2.0, capitulos 2/3/5/7 atualizados.
  - CHANGELOG.md: NOVO. Historico de versoes do repo.

- Auditoria mais recente disponivel em cerebro-governanca/auditorias/reports/auditoria-agentes-2026-05-25.md
  (gerada antes do bump v0.2.0).

- PENDENTE — Fase 2: aplicar v0.2.0 nos 5 agentes
  1. Editar SOUL.md de cada (adicionar Tom especifico + Continuidade)
  2. Editar IDENTITY.md de cada (formato dossie expandido com Territories)
  3. Anexar matriz Auto-Resolver no AGENTS.md de cada (substituindo/complementando v0.1.0 do adendo)
  4. Opcional: editar USER.md de Rocky e Leo (blocos 9-11)
  5. Commit + push nos 5 backups
  6. Re-rodar auditoria; esperado retornar a 100% conformidade com checklist atualizado

- PENDENTE — Skill auditoria-agentes (codex) precisa de atualizacao pra v0.2.0:
  - Checar string "BEGIN_COGNIS_GOVERNANCA_ADENDO_v0.2.0" no AGENTS.md (em vez de v0.1.0)
  - Checar presenca de "Tom especifico" e "Continuidade" no SOUL
  - Checar presenca de "Territories" e "Historico" no IDENTITY
  - Caso contrario, auditoria continua passando 150/150 mas nao reflete profundidade nova

- Demais Frentes do benchmark (B/C/D) — estado atualizado:
  Frente B — CONCLUIDA em 2026-05-28.
    10 adendos tematicos do Mini-curso v2 criados em cerebro-governanca/referencias/mini-curso-v2/
    Commit cerebro-governanca: de38206 docs: adiciona referencias mini-curso v2
  Frente C — CONCLUIDA em 2026-05-28.
    Skill `prompts-library` criada no Rocky em `skills/operacional/prompts-library/`.
    Material encontrado no curso: 12 arquivos `.md` em 6 categorias (business, community, content,
    productivity, research, support). Commit Rocky: f9e5570 feat(skills): adiciona prompts-library pixel
  Frente D — CONCLUIDA/MVP em 2026-05-28.
    Mission Control read-only criado em ~/.openclaw/mission-control/ e copia local em
    D:\COGNIS\Curso Openclaw\mission-control\. Timer systemd atualiza a cada 30min.
  Frente bonus — CONCLUIDA em 2026-05-28.
    Rocky atualizado com `wizard-conectar` v2.1 do Starter Kit v2.5.7.
    Commit Rocky: 09289b9 fix(starter): atualiza wizard-conectar para v2.5.7

- Documentos gerados nesta sessao salvos no D:\COGNIS\Curso Openclaw\:
  BENCHMARK-AMORA-2026-05-25.md (analise qualitativa Amora vs 5 agentes)
  cerebro-governanca/ (atualizado in-place com v0.2.0)

- Conteudo da Pixel extraido em /tmp/pixel_unzipped no VPS (95MB) para referencia futura.
  Material da Amora (6 arquivos canonicos) em:
  /tmp/pixel_unzipped/Modulo 2/Construindo seus primeiros agentes (Mini-curso Openclaw v2)/🧰 Templates (soul, user, identity, tools, etc)/📂 Exemplos da Amora (Agente Bruno Okamoto)/

Historico da sessao - 2026-05-25 (sessao 8 — Cowork, Fase 2 v0.2.0)

- Fase 2 do plano benchmark-amora-2026-05-25.md executada completa nos 3 arquivos canonicos principais:

  Item 1 — SOUL.md dos 5 agentes (+2 blocos obrigatorios v0.2.0):
    Tom especifico (proibe bajulacao: "Otima pergunta!", "Espero ter ajudado", etc) +
    Continuidade (lista dos 8 arquivos canonicos que sao o agente).
    Para BrIA/Gabi/Max foi aplicada versao com excecao autorizada "tom acolhedor com clientes/alunas".
    Tamanhos: Rocky 4946→6654, Leo 6574→8282, BrIA 2937→5467, Gabi 2924→5454, Max 2916→5446.
    Commits: dc78403, 01928d8, 60b49cd, 6116cb7, 2a8cf85.

  Item 2 — IDENTITY.md dos 5 agentes expandido para formato dossie v0.2.0:
    Adicionado: Versao semantica, Workspace path, Reportagem (operador tecnico/funcional),
    Territories (canais + topics + cerebros compartilhados com permissoes), Empresa que sirvo,
    Ponteiros para os 7 outros arquivos canonicos, Historico de versoes.
    Tamanhos: Rocky 303→2148, Leo 285→2109, BrIA 452→2630 (v2.0 — ja era dossie parcial),
    Gabi 630→2594, Max 527→2683.
    Commits: 565841a, c503c55, 56d79c5, 4b5beae, d417c22.
    Backups .bak-v010-* mantidos localmente no VPS, nao no git.

  Item 3 — AGENTS.md dos 5 agentes com matriz Auto-Resolver:
    Inserida entre "## Auditoria semanal" e "## Versao deste adendo" do bloco governanca.
    3 categorias: "Age sem perguntar" (leitura, organizacao interna), "Pede antes" (externo, custos,
    config), "Nunca faz" (gatilhos sensiveis, push direto main, WhatsApp send, etc).
    Inclui anti-pattern "terceirizacao excessiva".
    Entrada v0.2.0 adicionada ao historico do adendo.
    Tamanhos: Rocky/Leo/BrIA 364→436 linhas, Gabi/Max 347→419 linhas (+72 cada).
    Commits: 4064fcd, 224ca11, 65ecd98, b51c46b, 6dae721.
    Marcador BEGIN_COGNIS_GOVERNANCA_ADENDO_v0.1.0 mantido (formato literal "\\n" do codex em 22/05).

  Item 5 — Skill auditoria-agentes bumpada para v0.2.0:
    audit_agents.py: 5 patches.
      ADENDO_MARKER_V01 mantido + 5 marcadores novos
        (V02_AUTO_RESOLVER, SOUL_MARKER_TOM, SOUL_MARKER_CONTINUIDADE,
        IDENTITY_MARKER_TERRITORIES, IDENTITY_MARKER_HISTORICO).
      5 checks novos no audit_agent() — severidade MEDIO.
      REQUIRED_FILES bumpa: IDENTITY.md 250→1200 bytes, SOUL.md 800→4500 bytes.
      Header do relatorio: v0.1.0 → v0.2.0.
    SKILL.md: version frontmatter 0.1.0 → 0.2.0; lista de checks reflete os 5 novos.
    Commit Rocky: de2f4ad feat(auditoria-agentes): bumpa skill para v0.2.0.

  Item 4 — USER blocos 9-11 (Vocabulario, Rotina, Tom por plataforma) — PENDENTE.
    Depende de entrevistar Bruno para extrair vocabulario proprio + rotina + tom de comunicacao.
    Pode entrar em proxima sessao via conversa estruturada.

- Auditoria pos-Fase 2 (rodada manual via python3 audit_agents.py):
  Resultado: 170/175 checks (97.1%), 0 criticos, 3 altos, 2 medios, 0 baixos.
  TODOS os 5 agentes passaram nos 5 checks v0.2.0 novos (Tom, Continuidade, Auto-Resolver, Territories, Historico).
  Leo: 35/35 (100%).
  Issues restantes sao operacionais reais (nao da migracao):
    Rocky: working tree dirty (skill recem-modificada, resolvido pelo commit de2f4ad) + cron rocky-backup-diario em erro (pendencia conhecida).
    BrIA: working tree dirty (memory/2026-05-25.md untracked do agente em uso ativo).
    Gabi e Max: sem nota memory recente — agentes nao usados nos ultimos 7 dias (Jane/Marilia inativas).

- Constituicao cerebro-governanca v0.2.0 publicada na sessao 7 ja estava no remote — Fase 2 desta sessao consumiu os templates atualizados.

- Pendencia urgente que continua: rotacionar tokens (PAT GitHub antigo do Rocky + Notion Gabi/Max + OpenAI Codex se ainda nao renovado).

- Relatorio final da auditoria 2026-05-25 atualizado em:
  /home/openclaw/.openclaw/cerebro-governanca/auditorias/reports/auditoria-agentes-2026-05-25.md

Historico da sessao - 2026-05-26 (sessao 9 — Cowork, backup-workspace systemd)

- Pendencia operacional fechada: cron OpenClaw rocky-backup-diario (1a645071-e3b0-4494-b266-73eb5e587636) deletado.
  Estava disabled + quebrado por arquitetura ruim: pedia para LLM (gpt-5.4) em sessao isolated rodar git commit/push.
  LLM nao tem acesso real ao filesystem em sessao isolated → todo run terminava como "[blocked] Nao consegui executar".
  Padrao errado do cron (heartbeat de LLM) substituido pelo padrao correto do curso Pixel Mod1 Aula 08: cron deterministico via systemd.

- Nova infra de backup deterministica (sem LLM):
  Script bash unico reusavel: ~/.openclaw/workspace/skills/operacional/backup-workspace/scripts/run_backup.sh
    Le env WORKSPACE + AGENT_NAME. Idempotente: tree clean → loga e sai OK; dirty → git add + commit + push.
    Mensagem de commit padrao: "chore: automated backup YYYY-MM-DD HH:MM ZZZ".
    Faz alerta de seguranca se detectar .env/secrets/.key/.pem nos arquivos a commitar (defesa em profundidade alem do .gitignore).
  SKILL.md documentando o padrao em ~/.openclaw/workspace/skills/operacional/backup-workspace/SKILL.md
  
  5 systemd user services + 5 timers (escalonados a cada 5min a partir das 23h BRT):
    backup-workspace-rocky.{service,timer} → 23:00 → cognis-ia/clawdio-workspace-backup
    backup-workspace-leo.{service,timer}   → 23:05 → cognis-ia/leo-workspace-backup
    backup-workspace-bria.{service,timer}  → 23:10 → cognis-ia/bria-workspace-backup
    backup-workspace-gabi.{service,timer}  → 23:15 → cognis-ia/gabi-workspace-backup
    backup-workspace-max.{service,timer}   → 23:20 → cognis-ia/max-workspace-backup
  
  Habilitados via: systemctl --user daemon-reload + enable --now backup-workspace-{agent}.timer
  Persistent=true em todos (recupera se VPS estiver fora do ar na hora).
  Logam via journalctl --user -u backup-workspace-{agent}.service

- Validacao end-to-end (run manual dos 5 services):
  Rocky: commit + push (5c21226 - skill backup-workspace adicionada)
  Leo: tree clean, nada a fazer
  BrIA: commit + push (38d3fb2 - memory/2026-05-25.md)
  Gabi: tree clean
  Max: tree clean
  Duracao tipica: ~2s por agente.

- Tudo versionado em cognis-ia/infra:
  systemd/user/backup-workspace-*.service (5 arquivos)
  systemd/user/backup-workspace-*.timer (5 arquivos)
  Commit: 0188fc4 feat(systemd): backup-workspace timers determinísticos para os 5 agentes
  Segue padrao identico ao vigiar-markdowns-{gabi,max} criado pelo codex na sessao 7.

- Commit de migracao do Rocky para backup deterministico:
  Commit Rocky (workspace): 5c21226 chore: automated backup 2026-05-26 16:45 -03

- Comandos uteis pos-instalacao:
  systemctl --user list-timers backup-workspace-\*       # ver proximos disparos
  systemctl --user start backup-workspace-rocky.service  # disparar manual
  journalctl --user -u backup-workspace-rocky -n 20      # logs
  systemctl --user disable --now backup-workspace-rocky.timer  # desligar se precisar

- Pendencia BrIA heartbeat (sem chatId) substituida por diagnostico mais amplo na sessao 10:
  rocky-heartbeat e bria-heartbeat estavam "ok" no scheduler, mas funcionalmente blocked.

Historico da sessao - 2026-05-27 (sessao 10 — Codex, heartbeat-runner systemd + LLM por estado)

- Diagnostico real dos heartbeats:
  rocky-heartbeat (6d910b5b-ad84-4ad3-8411-b0b428e40116) e bria-heartbeat
  (8af5c4af-a776-45bd-9aa4-7c90911b5428) apareciam com lastRunStatus="ok" e delivery=true,
  mas os summaries dos ultimos runs eram "[blocked] Nao consegui ler HEARTBEAT.md/memory/hot.md".
  O problema nao era so chatId da BrIA: o runner agentTurn do OpenClaw 2026.5.18 nao expoe
  filesystem tools em cron, mesmo com lightContext=true e toolsAllow read/write/exec.

- Testes executados:
  1. bria-heartbeat com sessionTarget=session:agent:bria:telegram:direct:1950767646 -> ainda HEARTBEAT_BLOCKED.
  2. bria-heartbeat isolated com toolsAllow=["exec"] -> EXEC_BLOCKED.
  3. openclaw agent --agent bria --json -> funciona, injeta arquivos canonicos, mas custo/contexto alto.
  4. openclaw infer model run --model openai-codex/gpt-5.4 --thinking low -> funciona para decisao LLM one-shot.

- Solucao instalada: skill operacional heartbeat-runner.
  Caminho: ~/.openclaw/workspace/skills/operacional/heartbeat-runner/
  Ideia: systemd acorda e coleta contexto local; LLM decide por estado; HEARTBEAT_OK fica silencioso;
  apenas HEARTBEAT_ALERT vai para Bruno via Telegram.
  Isso preserva o principio Pixel: timer/cron = tempo; heartbeat = estado.

- Arquivos instalados:
  ~/.config/systemd/user/heartbeat-runner-rocky.service
  ~/.config/systemd/user/heartbeat-runner-rocky.timer
  ~/.config/systemd/user/heartbeat-runner-bria.service
  ~/.config/systemd/user/heartbeat-runner-bria.timer

- Agenda ativa:
  Rocky: 08:00, 12:00, 16:00, 20:00 America/Sao_Paulo
  BrIA: 08:02, 12:02, 16:02, 20:02 America/Sao_Paulo

- Crons nativos quebrados desativados:
  rocky-heartbeat -> enabled=false
  bria-heartbeat -> enabled=false

- Validacao:
  systemctl --user start heartbeat-runner-bria.service -> Silencioso: HEARTBEAT_OK
  systemctl --user start heartbeat-runner-rocky.service -> Silencioso: HEARTBEAT_OK
  Estado temporario do runner fica em /tmp/openclaw-heartbeat-runner/{agent}.json para nao sujar git.

- Versionamento:
  Commit Rocky: 3a8f693 feat(operacional): adiciona heartbeat-runner systemd
  Commit infra: 35409d8 feat(systemd): heartbeat-runner para Rocky e BrIA

- Comandos uteis:
  systemctl --user list-timers heartbeat-runner-\*
  systemctl --user start heartbeat-runner-bria.service
  systemctl --user start heartbeat-runner-rocky.service
  journalctl --user -u heartbeat-runner-bria.service -n 40 --no-pager
  journalctl --user -u heartbeat-runner-rocky.service -n 40 --no-pager

- Extensao da sessao 10: focus-guard do Rocky.
  Objetivo: Rocky mandar check-ins surpresa entre 09h e 20h e usar contexto local
  sanitizado do Chrome para cobrar foco sem ler dados sensiveis.

  Privacidade do Chrome:
  - Windows Task Scheduler roda D:\COGNIS\Curso Openclaw\tools\focus-guard\run_chrome_focus_monitor.ps1
    a cada 10 minutos.
  - O script ignora fora da janela 09h-20h.
  - Le copia local do SQLite History do Chrome, agrega somente dominios.
  - Nao envia URL completa, titulo da pagina, cookies, formularios, senhas ou conteudo.
  - Dominios sensiveis de auth/banco/governo/pagamento/senhas sao mascarados.
  - Upload privado para:
    ~/.openclaw/workspace/memory/local-private/focus-monitor/latest.json
  - .gitignore do Rocky inclui memory/local-private/ para nao versionar historico local.

  Check-ins surpresa:
  - Skill: ~/.openclaw/workspace/skills/operacional/focus-guard/
  - Timer VPS: rocky-focus-checkin.timer
  - Agenda: oportunidades a cada hora de 09h a 19h com RandomizedDelaySec=55m.
  - Script aplica sorteio interno, limite maximo 4 mensagens/dia e gap minimo 75 min.
  - Se houver dominios de distracao recentes, chance de mensagem aumenta.
  - Mensagem manual validada em 2026-05-27 16h22 BRT.

  Versionamento:
  - Commit Rocky: 34a61cf feat(rocky): adiciona focus-guard com check-ins surpresa
  - Commit infra: 089c36d feat(systemd): check-ins surpresa do Rocky

  Comandos uteis:
  - Windows: Get-ScheduledTask -TaskName 'OpenClaw Chrome Focus Monitor'
  - Windows: Start-ScheduledTask -TaskName 'OpenClaw Chrome Focus Monitor'
  - VPS: systemctl --user list-timers rocky-focus-checkin\*
  - VPS: journalctl --user -u rocky-focus-checkin.service -n 40 --no-pager

Historico da sessao - 2026-05-28 (sessao 11 — limpeza de pendencias no INFRA)

- INFRA.md auditado contra o estado real do VPS/GitHub.
- Confirmado: copia local D:\COGNIS\Curso Openclaw\INFRA.md e repo cognis-ia/infra estavam sincronizados antes da edicao.
- Limpas inconsistencias antigas no resumo operacional:
  - secao de crons antigos substituida por resumo atual de OpenClaw cron + systemd timers;
  - BrIA heartbeat deixou de constar como erro sem chatId e passou a constar como substituido pelo heartbeat-runner;
  - pendencias B/J atualizadas para refletir que Rocky e BrIA ja rodam heartbeat por estado via systemd;
  - diretoria e audit crons ajustados para refletir repos/rotinas ja criados.
- Pendencias reais remanescentes naquele momento: rotacao de tokens, USER blocos 9-11, Frentes B/C/D do benchmark Pixel, Mission Control e segundo cerebro operacional Gabi/Max.

Historico da sessao - 2026-05-28 (sessao 12 — Frente B referencias mini-curso v2)

- Diretriz da sessao: continuar a preparacao dos agentes seguindo o conteudo Pixel, deixando rotacao de tokens por ultimo.
- Auditoria atual dos 5 agentes regenerada com `auditoria-agentes` v0.2.0:
  - Relatorio: ~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-agentes-2026-05-28.md
  - Resultado: 172/175 checks (98.3%), 0 criticos, 0 altos, 3 medios.
  - Medios restantes: Rocky, Gabi e Max sem nota `memory/YYYY-MM-DD.md` recente.
  - Commit cerebro-governanca: 2c937f9 docs: registra auditoria agentes 2026-05-28
- Frente B do benchmark Pixel/Amora concluida no `cerebro-governanca`:
  - Criada pasta `referencias/mini-curso-v2/`.
  - Criados 10 adendos operacionais adaptados ao ecossistema Cognis IA:
    onboarding, identidade, workspace, memoria, skills, crons/heartbeats,
    outros canais, integracoes, multi-agente e mission-control.
  - `README.md` e `CHANGELOG.md` atualizados para v0.3.0.
  - Commit cerebro-governanca: de38206 docs: adiciona referencias mini-curso v2
- Tokens NAO foram rotacionados nesta sessao por decisao operacional do Bruno; permanecem para a ultima etapa de seguranca.

Historico da sessao - 2026-05-28 (sessao 13 — Frente C prompts-library)

- Frente C do benchmark Pixel/Amora concluida no workspace do Rocky:
  - Criada skill `skills/operacional/prompts-library/`.
  - Skill segue o principio de disclosure progressivo: `SKILL.md` pequeno, prompts em `references/prompts/`,
    script de listagem em `scripts/list_prompts.py`.
  - Fonte: `/tmp/pixel_unzipped/.../Templates de prompts/`.
  - Material efetivamente encontrado: 12 arquivos `.md` em 6 categorias:
    business, community, content, productivity, research e support.
  - Validado:
    `python3 skills/operacional/prompts-library/scripts/list_prompts.py`
    `python3 skills/operacional/prompts-library/scripts/list_prompts.py --category content`
    `python3 skills/operacional/prompts-library/scripts/list_prompts.py --search suporte`
  - Atualizados `skills/MAPA.md` e `skills/operacional/_registry.md`.
  - Commit Rocky: f9e5570 feat(skills): adiciona prompts-library pixel
- Observacao: INFRA antigo citava "38 prompts"; na pasta recebida do curso havia 12 arquivos `.md`.
  Se aparecer outro pacote de prompts, adicionar como nova fonte na mesma skill.

Historico da sessao - 2026-05-28 (sessao 14 — Frente D Mission Control)

- Frente D do benchmark Pixel/Amora concluida como MVP read-only.
- Criado `~/.openclaw/mission-control/` no VPS com:
  - `README.md`
  - `scripts/generate_status.py`
  - `systemd/mission-control-refresh.service`
  - `systemd/mission-control-refresh.timer`
  - `index.html`
  - `data/status.json`
- O gerador coleta sem usar tokens novos:
  - estado Git dos 5 agentes;
  - estado Git dos repos centrais governanca, diretoria e infra;
  - auditoria mais recente;
  - timers systemd relevantes;
  - crons OpenClaw;
  - pendencias do INFRA.md.
- Instalado timer systemd user:
  - `mission-control-refresh.timer`
  - frequencia: a cada 30 minutos via `OnUnitActiveSec=30min`;
  - ultimo teste: service executou com `status=0/SUCCESS`.
- Copia local sincronizada em `D:\COGNIS\Curso Openclaw\mission-control\`.

Historico da sessao - 2026-05-28 (sessao 19 — cerebro Bernardelli Areas)

- Criado o cerebro operacional compartilhado da Bernardelli Ensino:
  - Repo privado: `cognis-ia/cerebro-bernardelli-areas`
  - Clone VPS: `~/.openclaw/cerebro-bernardelli-areas/`
  - Copia local: `D:\COGNIS\Curso Openclaw\cerebro-bernardelli-areas\`
- Estrutura criada seguindo o padrao Pixel de areas vs agentes:
  - `areas/atendimento/`
  - `areas/produtos/`
  - `areas/operacoes/`
  - `areas/conteudo/`
  - `areas/marketing/`
  - `areas/tecnologia/`
  - cada area com `contexto/`, `skills/`, `rotinas/`, `projetos/` e indices.
- Regra de fronteira registrada:
  - este cerebro e operacional;
  - informacao com dinheiro nominal, pessoa especifica, contrato, juridico ou sociedade vai para `cerebro-diretoria`;
  - Rocky e Leo nao usam este cerebro no dia a dia.
- BrIA, Gabi e Max conectados via `AGENTS.md` com escopos:
  - BrIA: atendimento, produtos, operacoes e `inbox/bria`;
  - Gabi: conteudo, marketing e `inbox/gabi`;
  - Max: operacoes, tecnologia e `inbox/max`.
- Tambem foi normalizado o marcador quebrado do adendo de governanca nos 5 agentes:
  - Rocky: `fix(agents): normaliza adendo governanca`
  - Leo: `fix(agents): normaliza adendo governanca`
  - BrIA/Gabi/Max: `docs(agents): conecta cerebro bernardelli areas`
- Auditoria `auditoria-agentes` rerodada apos a mudanca:
  - Resultado mantido: 175/175 checks (100.0%), 0 criticos, 0 altos, 0 medios.
  - Commit cerebro-governanca: bb55379 docs: atualiza auditoria apos cerebro bernardelli areas

Historico da sessao - 2026-05-28 (sessao 20 — populacao inicial Bernardelli Areas)

- Primeira populacao do `cerebro-bernardelli-areas` concluida.
- Fonte usada:
  - `workspace-bria-shared/MAPA.md` (confirmado como praticamente vazio, apenas mapa legado);
  - `TOOLS.md`, `MAPA.md` e `skills/_index.md` de BrIA, Gabi e Max.
- Nao foram migradas memorias pessoais, casos de alunas, dados financeiros, contratos ou informacoes sensiveis.
- Documentos criados:
  - `areas/operacoes/contexto/topologia-agentes.md`
  - `areas/operacoes/rotinas/uso-do-cerebro-areas.md`
  - `areas/atendimento/contexto/politica-canais.md`
  - `areas/tecnologia/contexto/plataformas.md`
  - `areas/tecnologia/skills/apis-e-integracoes.md`
  - `areas/marketing/contexto/capacidades-marketing.md`
  - `areas/conteudo/contexto/capacidades-conteudo.md`
  - `areas/produtos/contexto/produtos-conhecidos.md`
- `_index.md` das subpastas correspondentes atualizado.
- Varredura simples por segredos executada antes do commit; achados foram apenas textos preventivos como "nao salvar tokens".
- Commit `cerebro-bernardelli-areas`:
  - ed4b2f1 docs: popula base operacional inicial
- Auditoria `auditoria-agentes` rerodada:
  - Resultado mantido: 175/175 checks (100.0%), 0 criticos, 0 altos, 0 medios.
  - Relatorio nao mudou em relacao ao commit anterior da governanca; sem novo commit em `cerebro-governanca`.

Historico da sessao - 2026-05-28 (sessao 18 — permissionamento Telegram)

- Pendencia M da Imersao Pixel concluida.
- Backup da config criado antes da mudanca:
  - `/home/openclaw/.openclaw/openclaw.json.bak-before-telegram-allowlist-20260528`
- `openclaw.json` atualizado para todos os bots Telegram:
  - `dmPolicy=allowlist`
  - `allowFrom` explicito
  - `groupAllowFrom` explicito
  - `groups.*.requireMention=true`
- Politica final:
  - default/Rocky: Bruno (`1950767646`)
  - Leo: Bruno (`1950767646`)
  - BrIA: Bruno (`1950767646`)
  - Gabi: Bruno (`1950767646`) + Jane (`938877898`)
  - Max: Bruno (`1950767646`) ate confirmacao do ID Telegram da Marilia
- `openclaw config validate` executado com sucesso.
- `openclaw-gateway` reiniciado e confirmado ativo.
- Tokens nao foram rotacionados nesta etapa.
- Codigo do Mission Control versionado no repo `cognis-ia/infra`:
  - `mission-control/README.md`
  - `mission-control/scripts/generate_status.py`
  - `mission-control/scripts/send_daily_review.py`
  - `mission-control/systemd/*.service`
  - `mission-control/systemd/*.timer`
  - Commit infra: ee384b5 feat: versiona mission control
- O painel nao abre porta publica e nao acessa `cerebro-diretoria`; ele apenas mostra status e caminhos.

Historico da sessao - 2026-05-28 (sessao 15 — auditoria 100/100)

- Fechados os 3 medios restantes da auditoria:
  - Rocky recebeu `memory/2026-05-28.md` com manutencao de governanca.
  - Gabi recebeu `memory/2026-05-28.md` com manutencao de governanca.
  - Max recebeu `memory/2026-05-28.md` com manutencao de governanca.
- Commits:
  - Rocky: 3d68755 docs(memory): registra manutencao governanca 2026-05-28
  - Gabi: aa4ae6a docs(memory): registra manutencao governanca 2026-05-28
  - Max: 6c0ea55 docs(memory): registra manutencao governanca 2026-05-28
- Auditoria `auditoria-agentes` v0.2.0 rerodada:
  - Resultado final: 175/175 checks (100.0%)
  - Criticos: 0
  - Altos: 0
  - Medios: 0
  - Baixos/higiene: 0
- Relatorio final salvo e commitado no `cerebro-governanca`:
  - 68003bd docs: atualiza auditoria 100 porcento 2026-05-28
- Mission Control regenerado apos auditoria 100%.

Historico da sessao - 2026-05-28 (sessao 16 — Starter Kit v2.5.7)

- Frente bonus do benchmark Pixel/Amora concluida.
- Comparados os zips:
  - `starter-kit-openclaw-v2.5.6.zip`
  - `starter-kit-openclaw-v2.5.7.zip`
- Mudanca operacional relevante do v2.5.7:
  - `skills/starter/wizard-conectar/SKILL.md` v2.0 -> v2.1.
  - Corrige fluxo Tavily removendo comando inexistente `openclaw secrets set`.
  - Remove workaround incorreto via SDK Python.
  - Documenta fluxo oficial: `.env` + `openclaw configure --section web` + `secrets apply` + `secrets reload` + `secrets audit`.
  - Documenta workaround correto para `pairing required`: aluno executar manualmente no terminal Managed.
- Aplicado no Rocky:
  - `skills/starter/wizard-conectar/SKILL.md`
  - `skills/_registry.md` atualizado para marcar `wizard-conectar` v2.1.
- Validado:
  - Nenhuma linha executavel `openclaw secrets set` permaneceu.
  - Nenhuma linha executavel `pip install tavily-python` permaneceu.
  - Linhas `openclaw secrets apply --dry-run` e `openclaw secrets apply` presentes.
- Commit Rocky:
  - 09289b9 fix(starter): atualiza wizard-conectar para v2.5.7
- Auditoria rerodada apos o upgrade:
  - Resultado mantido: 175/175 checks (100.0%), 0 criticos, 0 altos, 0 medios.
  - Relatorio `auditoria-agentes-2026-05-28.md` atualizado com ultimo commit do Rocky `09289b9`.
  - Commit cerebro-governanca: e99d2e1 docs: atualiza auditoria apos starter v2.5.7
- Mission Control regenerado apos a auditoria.

Historico da sessao - 2026-05-28 (sessao 17 — Revisao do Dia 18h)

- Pendencia E do mini-curso concluida.
- Tentativa inicial via OpenClaw cron criada:
  - `rocky-revisao-do-dia-18h`
  - ID: 60a642d4-ece9-4d24-a4a1-2de8e4a04519
  - Resultado do teste: entregou mensagem no Telegram, mas sem acesso real aos arquivos por `sessionTarget=isolated`.
  - Acao: cron OpenClaw desativado.
- Solucao final via systemd deterministico:
  - Script: `~/.openclaw/mission-control/scripts/send_daily_review.py`
  - Service: `rocky-revisao-dia.service`
  - Timer: `rocky-revisao-dia.timer`
  - Schedule: diariamente as 18:00 America/Sao_Paulo
  - Fonte dos dados: `mission-control/data/status.json` + `infra/INFRA.md`
  - Envio: `openclaw message send --channel telegram --target 1950767646`
- Teste manual executado com sucesso:
  - Telegram Message ID: 645
- Copia local sincronizada em `D:\COGNIS\Curso Openclaw\mission-control\`.

---

Historico da sessao - 2026-05-28 (sessao 22 — Catalogo completo Astron)

- Identificados dois endpoints novos da API AstronMembers:
  - `listClubCourses?club_id=8194` — retorna 40 cursos com nomes reais (4 paginas).
  - `listCourseModules?club_id=8194&course_id=X` — retorna modulos com nomes (instavel em bulk, ok em probe individual).
- Script `astron_full_catalog.py` criado em `workspace-sofia/scripts/`:
  - Coleta cursos via `listClubCourses` (paginado).
  - Tenta modulos via `listCourseModules` (best-effort; 404 em bulk por rate-limit).
  - Coleta aulas por curso via `listClubClasses?course_id=X` (paginado).
  - Gera `catalogo_completo.json`, `cursos.md` e 40 fichas `curso-<nome>.md`.
- Resultado da coleta:
  - 40 cursos com nomes reais (ex: "Modulo 2 - Paisagem", "Bonus Lives de Mentoria").
  - 491 aulas ativas mapeadas com nome, ID, URL de video e modulo.
  - 0 modulos via API em bulk (endpoint instavel; modulos inferidos por course_module_id).
- Commit Sofia: `59cd5b9 feat(catalogo): catalogo completo com nomes reais — 40 cursos, 491 aulas`
- Copia local: `D:\COGNIS\Curso Openclaw\sofia-workspace\catalogo\`
- Pendencia de modulos: `listCourseModules` funciona individualmente (confirmado em probe);
  solucao futura: chamar um curso por vez com delay maior, ou usar module_id das aulas como referencia.
- Tokens/credenciais Astron continuam intocados (decisao: deixar rotacao por ultimo).

---

## Sessão 23 — 2026-05-29

### Sofia: pipeline de transcrição completo

**Problema resolvido:** ffmpeg estático segfaulta neste kernel. Solução definitiva: PyAV v17 (embute ffmpeg próprio) + download HLS puro Python.

**Fix crítico PyAV v17:** `resampler.resample()` retorna lista — necessário iterar antes de `.to_ndarray()`.

**Resultados:**
- 42 aulas do curso "Explorando a Arte Abstrata" transcritas (0 erros)
- Scripts: `transcribe_pipeline.py`, `build_knowledge.py`
- Knowledge base gerado em `knowledge/explorando-arte-abstrata/` (5 arquivos, ~470 KB)
- Commit: `d7ec7ff` em `cognis-ia/sofia-workspace-backup`

**Pendente:**
- Lives Bônus Arte Abstrata (99109, 60 aulas) — aguardando aprovação
- Demais cursos Astron — próximas sessões
- Token rotation (pendência de segurança em aberto)

---

## Sessão 24 — 2026-06-02

### Hermes Agent instalado no VPS

- Versão: v0.15.1 (successor do OpenClaw)
- Instalado em: `~/.hermes/hermes-agent/`
- CLI: `~/.hermes/hermes-agent/venv/bin/hermes`
- Auth: OAuth openai-codex (conta contato@pintandotelas.com.br) ✅
- Modelo padrão: `gpt-5.4` via `openai-codex`
- Serviço: `hermes-lia.service` (systemd user)

### Agente Lia criada (Hermes)

- Bot Telegram: `@BE_Lia_Suporte_bot` (token em `~/.hermes/.env`)
- SOUL.md: `~/.hermes/SOUL.md` — tutora empática, escalada automática para humano
- Knowledge base: `~/.hermes/skills/cursos-bernardelli/SKILL.md` (226 aulas, 4.1 MB)
- Config: `~/.hermes/config.yaml` (provider: openai-codex, model: gpt-5.4)
- Gateway: `hermes-lia.service` — sobe automaticamente no boot
- Status: online ✅

### Sofia — transcricoes e knowledge base completos

Cursos transcritos (Whisper base + PyAV, sem ffmpeg):
- Arte Abstrata: 49 aulas (módulo extra incluído)
- Arte Derramada: 15 aulas
- Pintando Telas (core): 88 aulas
- Rosas Perfeitas: 73 aulas
- Bônus Precificação: 1 aula
- **Total: 226 aulas**

Knowledge base em: `~/.openclaw/workspace-sofia/knowledge/`
Arquivo consolidado: `~/.openclaw/workspace-sofia/cursos_BE.md` (4.1 MB)
Pendente: Bônus Aulas Gratuitas (38784), Lives (38785, 99109), Mini Curso, cursos menores

### Rocky — skill infra-manager

Rocky (`@Rocky_Bruno_bot`) agora é o super agente de infraestrutura.
Skill: `~/.openclaw/workspace/skills/infra-manager/SKILL.md`
Capacidades: gerenciar todos os agentes, reiniciar serviços, aprovar pareamentos, atualizar Lia, ler/editar workspaces. Sob demanda apenas.

### Pendências abertas

- Lia: testar resposta completa com aluno real (serviço online; pairing desabilitado; `HUMAN_CONTACT=Bruno` já definido)
- Token rotation (segurança — em aberto desde sessão anterior)
- OpenClaw Control UI: revisar e endurecer `gateway.controlUi.allowInsecureAuth=true` antes de expor/usar dashboard fora do caso local compatível
- OpenClaw gateway: migrar credenciais injetadas via systemd drop-ins para um arranjo mais limpo/rotacionável

### Rocky — saneamento inicial da infra

- Diagnóstico da Max revisitado em 2026-06-02: a config atual em disco já está correta.
  `allowFrom` e `groupAllowFrom` incluem Bruno (`1950767646`) e Marilia (`8443736822`).
- Problema operacional identificado durante o saneamento:
  reiniciar `openclaw-gateway` no meio de uma sessão ativa mata o próprio turno em andamento
  (`codex app-server client closed before turn completed`). Tratar restart/reload como operação controlada.
- `rocky-revisao-dia.timer` corrigido:
  removida chave inválida `Timezone`; timer segue ativo para 18:00 America/Sao_Paulo.
- Inventário local confirmou superfície de credenciais em:
  workspaces (`.env`), Hermes (`~/.hermes/.env`) e drop-ins do systemd do gateway.
- Risco estrutural confirmado:
  `gateway.controlUi.allowInsecureAuth=true` e `gateway.controlUi.token` seguem presentes no `openclaw.json`.
- Ordem segura de rotação/reforço validada:
  1. revogar o PAT GitHub antigo do Rocky (histórico; remote atual já está limpo)
  2. rotacionar `NOTION_TOKEN_TRABALHO` e `NOTION_TOKEN` de Gabi/Max
  3. alinhar credenciais OpenAI entre `openclaw.json`, drop-ins do gateway e Hermes/Lia
  4. por último revisar/rotacionar `gateway.controlUi.token`
- Mapeamento de uso crítico:
  - Notion: concentrado em Gabi/Max via skills `notion-api` e `.env`
  - GitHub: `GITHUB_TOKEN` atual em Rocky/Leo/BrIA; PAT antigo do Rocky citado apenas como exposição histórica
- OpenAI: espalhado entre `openclaw.json`, drop-ins do `openclaw-gateway` e `~/.hermes/.env`

---

## Sessão 26 — 2026-06-02

### Atlas — agente gestor institucional criado

- Decisão arquitetural: Rocky permanece agente pessoal do Bruno; função de criar, gerenciar e auditar agentes/estruturas passa para Atlas.
- Agente OpenClaw criado:
  - ID: `atlas`
  - Workspace: `~/.openclaw/workspace-atlas`
  - Agent dir: `~/.openclaw/agents/atlas/agent`
  - Modelo: `openai/gpt-5.4`
  - Canal publico: nenhum por enquanto
- Arquivos canônicos criados no padrão Pixel/Governança:
  `IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`, `MAPA.md`, `MEMORY.md`, `HEARTBEAT.md`, `TOOLS.md`, `memory/2026-06-02.md`.
- Skills do Atlas:
  - `skills/operacional/agent-lifecycle/` — criar, gerenciar e auditar agentes.
  - `skills/operacional/auditoria-agentes/` — migrada/copiada do Rocky e atualizada para Atlas Auditor.
  - `skills/infra-manager/` — migrada/copiada do Rocky como função institucional.
- Commits locais Atlas:
  - `9357286 feat: bootstrap atlas agent`
  - `cd5481f feat: atlas assume auditoria agentes`
  - `d126f95 docs(identity): define emoji atlas`
  - `7693509 docs: adiciona indice operacional`
- GitHub backup do Atlas pendente: tentativa de criar `cognis-ia/atlas-workspace-backup` falhou com `GITHUB_TOKEN` 401. Manter para etapa de token rotation.

### Auditoria migrada de Rocky para Atlas

- Cron OpenClaw existente `2afeecdc-c292-4521-8a3b-1bcd8f51d0af` foi editado:
  - Nome: `atlas-auditoria-agentes-semanal`
  - Agente: `atlas`
  - Agenda: segunda 07:00 America/Sao_Paulo
  - Entrega: Telegram Bruno
- Auditoria manual pós-migração:
  - Relatório: `~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-agentes-2026-06-02.md`
  - Resultado: 7 agentes, 244/245 checks (99.6%), 0 críticos, 0 altos, 1 médio.
  - Médio único: Atlas sem upstream GitHub por causa da etapa de tokens.
- Commit governança:
  - `5560660 docs: auditoria atlas 2026-06-02`
- Observação: `auditoria-agentes-2026-06-01.md` apareceu untracked em `cerebro-governanca`; não foi alterado nesta sessão.

### MAPA.md e _index.md

- Gerados/commits de índices de categorias em `skills/{canais,operacional,planejamento,starter}/_index.md` para Rocky, Leo, BrIA, Gabi e Max.
- Gabi e Max receberam `content/MAPA.md` e `archive/MAPA.md`.
- Atlas recebeu `skills/operacional/_index.md`.
- Commits:
  - Rocky: `729b39e docs: adiciona indices de skills e mapas`
  - Leo: `c1dba20 docs: adiciona indices de skills e mapas`
  - BrIA: `4ea033d docs: adiciona indices de skills e mapas`
  - Gabi: `05c0332 docs: adiciona indices de skills e mapas`
  - Max: `cdf2d76 docs: adiciona indices de skills e mapas`

### Heartbeats por estado ampliados

- Criados e habilitados timers systemd:
  - `heartbeat-runner-leo.{service,timer}` — 08:04, 12:04, 16:04, 20:04
  - `heartbeat-runner-gabi.{service,timer}` — 08:06, 12:06, 16:06, 20:06
  - `heartbeat-runner-max.{service,timer}` — 08:08, 12:08, 16:08, 20:08
- Testes manuais:
  - Leo: `status=0/SUCCESS`, resposta `HEARTBEAT_OK`
  - Gabi: `status=0/SUCCESS`, resposta `HEARTBEAT_OK`
  - Max: `status=0/SUCCESS`, resposta `HEARTBEAT_OK`
- Commit infra:
  - `68670d4 feat(systemd): heartbeat-runner para leo gabi max`

### Lia, Max e hardening validado

- Lia:
  - `hermes-lia.service` ativo e rodando.
  - `HUMAN_CONTACT=Bruno` já definido em `~/.hermes/.env`.
  - Pairing desabilitado/allow-all ainda precisa teste com aluno real.
  - Validado: Lia não tem registro em openclaw agents list; operação canônica é Hermes em ~/.hermes/. Pasta legada ~/.openclaw/workspace-lia preservada, sem ligação com agente/canal/binding OpenClaw.
- Max:
  - Não há pending Telegram pairing requests.
  - `allowFrom`/`groupAllowFrom` já incluem Bruno e Marilia no `openclaw.json`.
- Hardening validado:
  - `fail2ban`: active.
  - `ufw`: active, somente SSH liberado.
  - Gateway OpenClaw `18789`: escutando apenas em `127.0.0.1` e `::1`.
  - `unattended-upgrades`: active.
  - Logs `openclaw-gateway` e `hermes-lia`: disponíveis via journalctl.

### Pendências reais após sessão 26

- Token rotation segue propositalmente por último:
  - OpenAI/OpenClaw/Hermes
  - Notion Gabi/Max
  - GitHub token atual 401 para criação de repo Atlas
  - Control UI token/insecure auth
- Criar/pushar `cognis-ia/atlas-workspace-backup` depois da rotação/credencial GitHub nova.
- Testar Lia com aluno real.
- Avaliar auditoria mensal profunda do Atlas.

## Sessão 27 — 2026-06-03

### Telegram Atlas configurado

- Bot do Atlas configurado no OpenClaw como `telegram:atlas` (`@Cognis_Atlas_bot`).
- Binding confirmado: agente `atlas` roteia mensagens do accountId `atlas`.
- `openclaw.json` validado com `openclaw config validate`.
- Gateway reiniciado e confirmado `active`.
- Status do canal: `Telegram atlas: enabled, configured, running, disconnected, mode:polling, token:config`.
- Permissionamento inicial: DM allowlist para Bruno (`1950767646`), mantendo a regra de duas camadas.
- Observação operacional: em polling, o bot pode aparecer `disconnected` até haver conversa ativa; Bruno precisa abrir o chat do bot no Telegram e enviar `/start` ou primeira mensagem.

## Sessão 28 — 2026-06-03

### Atlas preparado como gestor institucional completo

- Atlas recebeu a base de conhecimento Pixel AI Hub:
  - `~/.openclaw/workspace-atlas/knowledge/pixel-ai-hub/curso-pixel-ai-hub-compilado.md`
  - `~/.openclaw/workspace-atlas/knowledge/pixel-ai-hub/inventario-arquivos.md`
  - `~/.openclaw/workspace-atlas/knowledge/pixel-ai-hub/README.md`
- Atlas recebeu acesso documentado ao estado Cognis/OpenClaw:
  - copia de referencia: `knowledge/infra/INFRA.md`
  - fonte viva obrigatoria: `~/.openclaw/infra/INFRA.md`
  - mapa operacional: `knowledge/estrutura/MAPA-COGNIS-OPENCLAW.md`
- Atlas recebeu pesquisa curada de repos/skills externos em `knowledge/research/github-skills-2026-06-03.md`.
  - Decisao: nao instalar third-party skills automaticamente; ler/auditar antes.
- Codex CLI instalado no VPS para o usuario `openclaw`:
  - versao validada: `codex-cli 0.136.0`
  - uso documentado na skill `skills/operacional/codex-cli/`.
- Skills internas novas:
  - `skills/operacional/codex-cli/`
  - `skills/operacional/ssh-workspace-operator/`
  - `skills/operacional/estrutura-cognis/`
- Skills Pixel curadas copiadas para `skills/pixel-ai-hub/`:
  - auditoria-integridade
  - relatorio-evolucao-agentes
  - consolidacao-memoria
  - criar-skill
  - relatorio-rotinas
  - backup-workspace-github
  - commit-diario-workspace
  - cron-resume-wizards
  - seguranca-checklist
  - writing-plans
  - executing-plans
  - verification-before-completion
  - setup-agente-openclaw
  - sync-empresa
  - sync-diretoria
- `openclaw skills check --agent atlas` validado:
  - Total: 74
  - Eligible: 31
  - Visible to model: 31
  - Missing requirements: 0
- Commit Atlas:
  - `3529d1a feat: prepara atlas com base pixel e codex cli`

## Sessão 29 — 2026-06-03

### Auditoria das skills Pixel do Atlas

- Escopo auditado: `~/.openclaw/workspace-atlas/skills/pixel-ai-hub/`.
- Relatório criado:
  - `~/.openclaw/workspace-atlas/reports/auditoria-skills-pixel-2026-06-03.md`
- Resultado:
  - 15 skills Pixel avaliadas.
  - 7 skills aprovadas e mantidas ativas:
    - `auditoria-integridade`
    - `relatorio-evolucao-agentes`
    - `relatorio-rotinas`
    - `seguranca-checklist`
    - `writing-plans`
    - `executing-plans`
    - `verification-before-completion`
  - 7 skills movidas para referencia:
    - `knowledge/pixel-ai-hub/skills-reference/reference-only/`
  - 1 skill movida para quarentena:
    - `knowledge/pixel-ai-hub/skills-reference/quarantine/criar-skill/`
- Motivo da quarentena/referencia:
  - skills com `git push`, tokens, `.env`, symlinks, dados sensiveis, Telegram HTTP ou instalacao remota nao devem ficar ativas para Atlas sem adaptacao Cognis.
- Correcoes aplicadas:
  - frontmatter valido em `auditoria-integridade`, `relatorio-evolucao-agentes` e `relatorio-rotinas`.
  - `_index.md` criado em `skills/pixel-ai-hub/`.
- Validacao:
  - `openclaw skills check --agent atlas` passou com 0 missing requirements.
  - As 7 skills Pixel aprovadas aparecem como visiveis ao modelo.
- Commit Atlas:
  - `c9d8508 chore: audita skills pixel atlas`

## Sessão 30 — 2026-06-03

### Rotina mensal de auditoria de skills criada

- Skill nova no Atlas:
  - `~/.openclaw/workspace-atlas/skills/operacional/auditoria-skills/`
- Script principal:
  - `~/.openclaw/workspace-atlas/skills/operacional/auditoria-skills/scripts/audit_skills.py`
- Escopo:
  - Rocky, Leo, BrIA, Gabi, Max, Sofia e Atlas.
  - Lia/Hermes fica fora do escopo de agente OpenClaw, exceto observacao quando houver skills proprias.
- Comportamento:
  - read-only nos workspaces auditados.
  - nao le `.env`.
  - nao corrige automaticamente.
  - gera relatorios em Atlas e `cerebro-governanca`.
- Cron OpenClaw criado:
  - ID: `eb77d0d9-9939-41f3-bb67-2953be50350e`
  - Nome: `atlas-auditoria-skills-mensal`
  - Agente: `atlas`
  - Agenda: `15 8 1 * *` em `America/Sao_Paulo`
  - Entrega: Telegram Bruno
  - Proxima execucao: em 28 dias a partir de 2026-06-03
- Execucao manual validada:
  - Agentes avaliados: 7/7
  - Skills avaliadas: 190
  - Resultado inicial:
    - APROVADA: 67
    - APROVADA_COM_AJUSTES: 7
    - SOMENTE_REFERENCIA: 88
    - QUARENTENA: 28
    - REMOVER: 0
- Relatorios:
  - `~/.openclaw/workspace-atlas/reports/auditoria-skills-2026-06-03.md`
  - `~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-skills-2026-06-03.md`
- Commits:
  - Atlas: `1712dd7 feat: adiciona auditoria mensal de skills`
  - Governanca: `87294e6 docs: adiciona auditoria mensal de skills`

## Sessão 31 — 2026-06-03

### Skills compartilhadas Pixel instaladas nos agentes

- Fonte local recebida:
  - `C:\Users\brned\Downloads\voice.zip`
  - `C:\Users\brned\Downloads\youtube-watcher.zip`
- Distribuição aplicada:
  - `voice`: instalada em todos os agentes OpenClaw formais:
    - Rocky/main (`~/.openclaw/workspace/skills/voice`)
    - Leo (`~/.openclaw/workspace-leo/skills/voice`)
    - BrIA (`~/.openclaw/workspace-bria/skills/voice`)
    - Gabi (`~/.openclaw/workspace-gabi/skills/voice`)
    - Max (`~/.openclaw/workspace-max/skills/voice`)
    - Sofia (`~/.openclaw/workspace-sofia/skills/voice`)
    - Atlas (`~/.openclaw/workspace-atlas/skills/voice`)
  - `youtube-watcher`: instalada somente em Rocky/main, Leo, Gabi e Max:
    - `~/.openclaw/workspace/skills/youtube-watcher`
    - `~/.openclaw/workspace-leo/skills/youtube-watcher`
    - `~/.openclaw/workspace-gabi/skills/youtube-watcher`
    - `~/.openclaw/workspace-max/skills/youtube-watcher`
- Índices atualizados:
  - `skills/_index.md` de cada workspace recebeu a entrada da skill correspondente.
- Dependências instaladas no VPS para o usuário `openclaw`:
  - `edge-tts 7.2.8`
  - `yt-dlp 2026.03.17`
  - Fallback operacional para `~/.local/bin`, porque serviços systemd/OpenClaw podem não carregar PATH interativo.
- Hardening antes da distribuição:
  - `voice/index.js` reescrito para usar chamada por argumentos, não comando em string.
  - saída da voice limitada a arquivo `.mp3` simples dentro do diretório temporário.
  - bloqueio básico de padrões de segredo em texto falado (`sk-`, `ghp_`, `github_pat_`, chave privada).
  - texto limitado a 5000 caracteres.
  - `youtube-watcher/scripts/get_transcript.py` ajustado para localizar `yt-dlp` em PATH ou `~/.local/bin`.
- Validação:
  - `openclaw skills check --agent` passou com `Missing requirements: 0` em Rocky/main, Leo, BrIA, Gabi, Max, Sofia e Atlas.
  - `youtube-watcher` confirmado como visível e pronto em Rocky/main, Leo, Gabi e Max.
  - geração de arquivo TTS por `edge-tts` validada em `/tmp/openclaw-voice-test.mp3`.
  - reprodução de áudio não validada no VPS headless; geração do MP3 está operacional.
- Auditoria mensal de skills reexecutada após instalação:
  - Agentes avaliados: 7
  - Skills avaliadas: 201
  - Resultado:
    - APROVADA: 67
    - APROVADA_COM_AJUSTES: 7
    - SOMENTE_REFERENCIA: 88
    - QUARENTENA: 39
  - Relatórios atualizados:
    - `~/.openclaw/workspace-atlas/reports/auditoria-skills-2026-06-03.md`
    - `~/.openclaw/cerebro-governanca/auditorias/reports/auditoria-skills-2026-06-03.md`
- Commits dos workspaces:
  - Rocky/main: `89d7483 feat(skills): adiciona voice e youtube watcher`
  - Leo: `15c9802 feat(skills): adiciona voice e youtube watcher`
  - BrIA: `bd192b3 feat(skills): adiciona voice`
  - Gabi: `ec792ef feat(skills): adiciona voice e youtube watcher`
  - Max: `410b219 feat(skills): adiciona voice e youtube watcher`
  - Sofia: `881bbea feat(skills): adiciona voice`
  - Atlas: `90ba82f feat(skills): adiciona voice`
  - Atlas auditoria atualizada: `79ca635 chore: atualiza auditoria skills apos voice youtube`
  - Governança auditoria atualizada: `3aefe52 docs: atualiza auditoria skills apos voice youtube`
- Observações:
  - Atlas continua sem upstream GitHub até rotação/correção do token GitHub.
  - Arquivos locais/untracked não relacionados em Rocky, BrIA e governança foram preservados sem alteração.

## Sessão 32 — 2026-06-08

### LLM primária OAuth e fallback DeepSeek corrigido

- Arquitetura-alvo confirmada:
  - Primário: OpenAI via OAuth (`openai-codex`)
  - Backup: DeepSeek
- Estado OpenClaw verificado:
  - Modelo primário dos agentes: `openai/gpt-5.4`
  - Runtime efetivo: `openai via codex uses openai-codex`
  - Conta OAuth: `contato@pintandotelas.com.br`
  - Fallback configurado: `deepseek/deepseek-v4-flash`
- Problema encontrado:
  - `DEEPSEEK_API_KEY` existia em `~/.config/systemd/user/openclaw-gateway.service.d/deepseek.conf`.
  - Porém `openclaw models status` mostrava `Missing auth - deepseek`, porque o auth de modelos usa `~/.openclaw/agents/main/agent/auth-profiles.json` e `Shell env: off`.
- Correção aplicada:
  - Backup criado antes da alteração:
    - `~/.openclaw/agents/main/agent/auth-profiles.json.bak-20260608151158`
  - Perfil adicionado ao auth store:
    - `deepseek:default`
    - `provider=deepseek`
    - `type=api_key`
  - `openclaw models status` deixou de reportar `Missing auth - deepseek`.
- Validação:
  - Chamada direta validada:
    - `openclaw infer model run --model deepseek/deepseek-v4-flash --prompt 'Responda apenas: OK_DEEPSEEK' --thinking low`
    - retorno: `OK_DEEPSEEK`
- OpenAI API key ainda presente, mas não removida nesta sessão:
  - `~/.openclaw/openclaw.json`
  - `~/.openclaw/agents/main/agent/auth-profiles.json` (`openai:default`)
  - `~/.openclaw/agents/main/agent/codex-home/auth.json`
  - `~/.openclaw/agents/leo/agent/codex-home/auth.json`
  - `~/.openclaw/agents/gabi/agent/codex-home/auth.json`
  - `~/.config/systemd/user/openclaw-gateway.service.d/openai.conf`
  - `~/.config/systemd/user/openclaw-lia.service.d/openai.conf`
  - `~/.hermes/.env`
  - `~/.hermes/auth.json`
- Decisão operacional:
  - Não revogar/remover OpenAI API key ainda.
  - Motivo: ela ainda aparece em consumidores paralelos, incluindo Hermes/Lia, TTS/Whisper/imagem e codex-home legado.
  - Próxima etapa segura: migrar/remover cada consumidor explicitamente, validando serviço por serviço, e só então revogar a key no painel OpenAI.
- Hermes/Lia:
  - `~/.hermes/config.yaml` já aponta `provider: "openai-codex"`.
  - `~/.hermes/auth.json` contém OAuth `openai-codex` e também credencial `openai-api`; manter até validação completa da Lia sem `OPENAI_API_KEY`.
- Token Telegram Atlas:
  - Rotação continua recomendada porque o token foi colado em conversa.
  - Ação pendente depende de novo token gerado no BotFather.



---

Skills compartilhadas via `skills.load.extraDirs`

A partir de 2026-06-15, skills transversais (usadas por 2+ agentes) vivem no `cerebro-cognis` e são descobertas por todos os agentes via configuração `skills.load.extraDirs` no `openclaw.json`:

```
"skills": {
  "load": {
    "extraDirs": [
      "~/.openclaw/cerebro-cognis/empresa/skills",
      "~/.openclaw/cerebro-cognis/areas/infraestrutura/skills",
      "~/.openclaw/cerebro-cognis/areas/contas-atendidas/skills",
      "~/.openclaw/cerebro-cognis/areas/produtos/skills"
    ]
  }
}
```

Vantagem: zero cópias, zero symlinks, fonte de verdade única. OpenClaw já bloqueia symlinks por segurança (`reason=symlink-escape`); `extraDirs` é o caminho oficial.

Migração realizada em 2026-06-15 (25 skills no total):

Lote 1 (piloto): voice (7 agentes), youtube-watcher (4 agentes) → `cerebro-cognis/empresa/skills/`

Lote 2 (5 blocos, 23 skills):
- Planejamento (5 skills × 5 agentes): brainstorming, writing-plans, executing-plans, verification-before-completion, llm-council → `empresa/skills/planejamento/`
- Qualidade (4 skills × 4-5 agentes): impeccable, openclaw-guardian, pdf-reports, remembering-conversations → `empresa/skills/`
- Operacionais infra (4 skills × 5 agentes): cron-resume-wizards, commit-diario-workspace, backup-workspace-github, seguranca-checklist → `areas/infraestrutura/skills/operacional/`
- Atlas institucional (6 skills): auditoria-agentes, auditoria-skills, agent-lifecycle, codex-cli, ssh-workspace-operator, estrutura-cognis → `areas/infraestrutura/skills/operacional/`
- APIs cliente Bernardelli (4 skills): astron-members-api, hotmart-api, meta-ads-api, notion-api → `areas/contas-atendidas/skills/`

Lote 3 (2026-06-16, 16 skills extras):
- Pixel Starter Kit (10 wizards × 5 agentes): primeira-vitoria, wizard-aluno, wizard-agente, wizard-workspace, wizard-autonomia, wizard-conectar, wizard-whisper-quick, gera-log-jornada, continuar-jornada, onboarding-checklist → `empresa/skills/starter/`
- Canais (1 skill × 5 agentes): canais/wizard-whatsapp → `empresa/skills/canais/`
- Multi-agent (1 skill × 3 agentes): dispatching-parallel-agents → `empresa/skills/`
- Atlas único (3 skills): relatorio-evolucao-agentes, relatorio-rotinas, auditoria-integridade → `areas/infraestrutura/skills/operacional/`
- Atlas duplicado removido (4 skills): writing-plans, executing-plans, verification-before-completion, seguranca-checklist (já em outros paths)

Lote 4 - flow Cowork captura (2026-06-16):
- Skills cognis-capture + cognis-sync em `empresa/skills/`
- inbox/bruno/ adaptado (README, CLAUDE, _template) para Windows + Cowork
- sync_via_ssh.sh: roteia git operations via SSH no VPS (zero auth GitHub Windows)
- .gitattributes para line endings cross-platform

Total migrado: 41 skills consolidadas em cerebro-cognis (de ~190 inventariadas).

Pendente: skills agente-específicas que ainda fazem sentido onde estão (Leo: copywriting/content-strategy/email-sequence/social-content/analytics-tracking/lia-manager; BrIA: ab-test-setup/copy-editing/marketing-psychology; Gabi: marketing-ideas; Rocky pessoal: expense-tracker/fitness-coach/focus-guard/corinthians-jogos/whatsapp-monitor; Sofia legado: astron-course-mapper/course-knowledge-builder).

Atenção: cron OpenClaw `atlas-auditoria-agentes-semanal` (cron `2afeecdc`) continua usando `auditoria-agentes` — agora descoberta via `extraDirs` em `cerebro-cognis/areas/infraestrutura/skills/operacional/auditoria-agentes/`. Validado pós-migração.
