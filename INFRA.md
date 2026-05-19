INFRA — OpenClaw (Bruno Eduardo)
Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo.
Última atualização: 2026-05-19 (sessão 3)

Como iniciar uma nova sessão
Selecione a pasta D:\COGNIS\Curso Openclaw no Cowork — o CLAUDE.md dispara
automaticamente a skill openclaw-session-start, que busca este arquivo e configura SSH.
Arquivo necessário na pasta: vps_key (chave SSH privada — nunca compartilhe)

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

Curso Openclaw — implementação pendente (ordem de prioridade)
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
- Limpeza de config pó