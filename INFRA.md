# INFRA — OpenClaw (Bruno Eduardo)
_Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo._
_Última atualização: 2026-05-11_

---

## Infraestrutura

- **VPS:** `217.77.10.26` — usuário `openclaw`
- **SSH:** `ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes openclaw@217.77.10.26`
- **OpenClaw versão:** 2026.5.3-1
- **Binário:** `~/.npm-global/bin/openclaw`
- **Serviço:** `systemctl --user restart openclaw-gateway`

---

## Agentes ativos

| Agente | ID | Canal Telegram | Workspace | GitHub backup |
|--------|----|---------------|-----------|---------------|
| 🪨 Rocky | `main` (default) | @Rocky_Bruno_bot | `~/.openclaw/workspace` | `cognis-ia/clawdio-workspace-backup` |
| 🦁 Léo | `leo` | `telegram:leo` | `~/.openclaw/workspace-leo` | `cognis-ia/leo-workspace-backup` |
| 🧡 BrIA | `bria` | `telegram:bria` | `~/.openclaw/workspace-bria` | `cognis-ia/bria-workspace-backup` |

**GitHub org:** `cognis-ia` — token: `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`

---

## Segundos Cérebros

| Workspace | Quem usa | GitHub |
|-----------|----------|--------|
| `~/.openclaw/workspace-shared/` | Rocky + Léo | `cognis-ia/shared-workspace-backup` |
| `~/.openclaw/workspace-bria-shared/` | BrIA (isolado) | `cognis-ia/bria-shared-backup` |

---

## Crons ativos

| ID | Nome | Agente | Horário | Tools |
|----|------|--------|---------|-------|
| 1a645071 | rocky-backup-diario | main | 23h todo dia | exec,read,write |
| 9cdbe3fa | leo-backup-diario | leo | 23h todo dia | exec,read,write |
| b5bc28b7 | bria-backup-diario | bria | 23h todo dia | exec,read,write |
| 8af5c4af | bria-heartbeat | bria | 8h,12h,16h,20h | exec,read,write |

---

## Configuração chave (`~/.openclaw/openclaw.json`)

- **Modelo primário:** `openai-codex/gpt-5.4`
- **Fallback:** `deepseek/deepseek-v4-flash`
- **TTS voz Rocky:** `messages.tts.providers.openai.voice: "echo"` (robótica/metálica)
- **TTS auto:** `messages.tts.auto: "inbound"` (só quando usuário manda áudio)
- **Brave Search:** `plugins.entries.brave.config.webSearch.apiKey: "BRAVE_API_KEY_REVOGADA"`
- **Telegram accounts:** `default` (Rocky), `leo` (Léo), `bria` (BrIA)

---

## Tokens de API

- **OpenAI API Key:** `sk-proj-1V8i82Ptp...` (válida — usada pelo provider `openai`)
- **OpenAI Codex (OAuth):** conta `contato@pintandotelas.com.br` — **expira ~15 maio 2026**
  - Para renovar: SSH no VPS → `~/.npm-global/bin/openclaw models auth login --provider openai-codex`
- **DeepSeek:** `DEEPSEEK_API_KEY_REVOGADA`
- **Telegram Rocky:** `8655715318:AAEzQnDQVvTKknA9CBSQWt4LID2cn7C_Vvc`
- **Telegram Léo:** `8614945051:AAGnPqkxJR7ifgO-Au-u2Ie6pa3epUtMMkFs`
- **Telegram BrIA:** `8454764914:AAHphx2iXsMYm-Rvs0StqzEVyaqvYnDFG5M`

---

## exec-approvals.json — allowlist global (`*`)

Todos os agentes podem rodar sem pedir aprovação:
`/usr/bin/git`, `git`, `/bin/bash`, `/usr/bin/bash`, `/bin/sh`, `/usr/bin/date`, `date`, `/usr/bin/python3`, `/usr/bin/env`, `/home/openclaw/.npm-global/bin/openclaw`

Allowlist `main` (Rocky): `~/.local/bin/gog` + comandos de cron aprovados
Allowlist `leo`: `~/.local/bin/gog`

---

## Starter Kit v2.5.6

Instalado em Rocky, Léo e BrIA. 19 skills cada:
- `skills/starter/` (10): onboarding-checklist, wizard-agente, wizard-aluno, wizard-autonomia, wizard-conectar, wizard-workspace, wizard-whisper-quick, primeira-vitoria, continuar-jornada, gera-log-jornada
- `skills/operacional/` (4): backup-workspace-github, commit-diario-workspace, cron-resume-wizards, seguranca-checklist
- `skills/planejamento/` (4): brainstorming, executing-plans, verification-before-completion, writing-plans
- `skills/canais/` (1): wizard-whatsapp

---

## BrIA — Bernardelli Ensino

- **Empresa:** Bernardelli Ensino (Jane Bernardelli — "A Arte Transforma")
- **Produtos:** Pintando Telas, Arte Abstrata, Rosas Perfeitas, Arte Derramada
- **Plataformas:** Hotmart (vendas) + Astron Members (área de membros)
- **Persona das alunas:** Maria, 62 anos, aposentada, apaixonada por arte
- **Tom:** acolhedor, caloroso, premium — assina com 🧡
- **Pareamento Telegram:** ID `1950767646` (Bruno) já aprovado

---

## Pendências e próximas ações

1. **Renovar token OpenAI Codex** até ~15 maio — rodar `openclaw models auth login --provider openai-codex` direto no VPS via SSH (precisa de TTY)
2. **Skills hunt** — pesquisar em clawhub.ai e github.com/okjpg/openclaw-BrunoOkamoto skills relevantes para Rocky, Léo e BrIA
3. **Heartbeat Rocky e Léo** — ainda não configurado (só BrIA tem)
4. **TOOLS.md migration** — Rocky e Léo ainda têm TOOLS.md (legado); migrar para MAPAs distribuídos por pasta (dívida técnica v2)
5. **Deletar bot antigo** — @Clawdio_Bruno_bot ainda existe no BotFather; Bruno precisa rodar /deletebot manualmente

---

## Regra absoluta (todos os agentes)

**NUNCA assinar, contratar ou comprar** qualquer coisa, serviço ou produto sem o expresso consentimento do Bruno Eduardo — independente do valor ou urgência aparente.

---

## Como usar este arquivo

Anexe o `INFRA.md` no início de cada nova sessão com:
> "Segue o INFRA.md com o contexto da nossa infra OpenClaw. Vamos continuar."

Ao final de cada sessão, peça para atualizar:
> "Atualize o INFRA.md com o que fizemos hoje."

**Nunca criar um novo arquivo** — sempre editar este.
