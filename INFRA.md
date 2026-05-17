INFRA — OpenClaw (Bruno Eduardo)
Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo.
Última atualização: 2026-05-15

Como iniciar uma nova sessão
Selecione a pasta D:\COGNIS\Curso Openclaw no Cowork — o CLAUDE.md dispara
automaticamente a skill openclaw-session-start, que busca este arquivo e configura SSH.
Arquivo necessário na pasta: vps_key (chave SSH privada — nunca compartilhe)

---

Infraestrutura

VPS: 217.77.10.26 — usuário openclaw
SSH: ssh -i <caminho>/vps_key -o IdentitiesOnly=yes openclaw@217.77.10.26
OpenClaw versão: 2026.5.3-1
Binário: ~/.npm-global/bin/openclaw
Serviço: systemctl --user restart openclaw-gateway

---

Agentes ativos (5)

| Agente | ID | Emoji | Papel | Canal Telegram | Workspace | GitHub backup |
|--------|-----|-------|-------|---------------|-----------|---------------|
| Rocky | main (default) | | Agente pessoal do Bruno | telegram:default (@Rocky_Bruno_bot) | ~/.openclaw/workspace | cognis-ia/clawdio-workspace-backup |
| Leo | leo | 🦁 | Agente profissional (COGNIS IA) | telegram:leo (@CG_Leo_Bot) | ~/.openclaw/workspace-leo | cognis-ia/leo-workspace-backup |
| BrIA | bria | 🧡 | Suporte de alunas — Bernardelli Ensino | telegram:bria (@BE_BrIA_bot) | ~/.openclaw/workspace-bria | cognis-ia/bria-workspace-backup |
| Gabi | gabi | 💜 | Criativa/estratégica da Jane — Bernardelli Ensino | telegram:gabi (@BE_Gabi_bot) | ~/.openclaw/workspace-gabi | nao criado |
| Max | max | | Operacional da Marilia — Bernardelli Ensino | telegram:max (@BE_Max_bot) | ~/.openclaw/workspace-max | nao criado |

GitHub org: cognis-ia — token no VPS em ~/.openclaw/workspace/.env

Perfis Bernardelli:
- BrIA: suporte de alunas, Hotmart, Astron Members — persona Maria, 62 anos
- Gabi: criativa, conteúdo, voz da marca Jane — mentora de arte
- Max: operacional, analítica, parceira da Marilia

Usuários com acesso liberado:
- Bruno Eduardo: Telegram ID 1950767646 (todos os agentes)
- Jane Bernardelli: Telegram ID 938877898 (Gabi)

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

Voz dos agentes (TTS)

Configuração global (openclaw.json → messages.tts):
  auto: "inbound" — responde com áudio SOMENTE quando receber áudio
  provider: openai
  model: gpt-4o-mini-tts
  voice: "echo" (padrão global — masculino)

Overrides por agente (agents.list[].tts):
  Gabi: voice = "nova" (feminino, animado)

Para trocar voz da Gabi: editar agents.list onde id=gabi → tts.providers.openai.voice
Vozes femininas disponíveis: nova, coral, shimmer, sage, alloy

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

---

Skills instaladas (além do Starter Kit v2.5.6)

Rocky: remembering-conversations, openclaw-guardian, meta-ads-api
Leo: content-strategy, copywriting, social-content, email-sequence,
     analytics-tracking, openclaw-guardian, meta-ads-api, dispatching-parallel-agents
BrIA: copy-editing, email-sequence, marketing-psychology, openclaw-guardian,
      remembering-conversations, hotmart-api, astron-members-api, meta-ads-api,
      analytics-tracking, ab-test-setup, content-strategy, dispatching-parallel-agents
Gabi: copywriting, social-content, content-strategy, marketing-ideas,
      marketing-psychology, openclaw-guardian, remembering-conversations,
      hotmart-api, astron-members-api, meta-ads-api
Max: analytics-tracking, ab-test-setup, openclaw-guardian, remembering-conversations,
     dispatching-parallel-agents, astron-members-api, meta-ads-api

---

Segurança — Historico de incidentes

2026-05-15: Brave Search e DeepSeek API keys expostas no repo cognis-ia/infra (git history).
  - Keys antigas revogadas nas plataformas
  - Historico reescrito com git filter-branch + force push
  - Novas keys configuradas no VPS
  - Brave: openclaw.json → plugins.entries.brave.config.webSearch.apiKey
  - DeepSeek: ~/.config/systemd/user/openclaw-gateway.service.d/deepseek.conf

REGRA: NUNCA colocar valores de API keys no INFRA.md — apenas indicar onde estão armazenadas.

---

Pendências

1. GitHub backup Gabi e Max — cognis-ia/gabi-workspace-backup e max-workspace-backup
2. Crons com erro — rocky-backup-diario (sem route) e bria heartbeat+backup (sem chatId)
3. Heartbeat Rocky e Leo — não configurado
4. Segundo cérebro Gabi e Max
5. Renovar token OpenAI Codex — ate 22 maio 2026 (SSH com TTY) — URGENTE
6. Rotacionar chave OpenAI exposta em historico Git (diferente do incidente acima)
7. TOOLS.md legado — Rocky e Leo, migrar para MAPAs distribuídos
8. Deletar @Clawdio_Bruno_bot no BotFather — acao manual Bruno

---

Regra absoluta

NUNCA assinar, contratar ou comprar qualquer coisa sem o expresso consentimento do Bruno Eduardo.

---

Atualização deste arquivo

Ao final de cada sessão: "Atualize o INFRA.md com o que fizemos hoje."
Claude atualiza E faz push para cognis-ia/infra no GitHub.
Nunca criar um novo arquivo — sempre editar este.
