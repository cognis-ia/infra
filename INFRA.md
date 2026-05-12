# INFRA — OpenClaw (Bruno Eduardo)
_Arquivo único e canônico. Atualizar ao final de cada sessão — nunca criar um novo._
_Última atualização: 2026-05-12 (sessão 4)_

---

## Como iniciar uma nova sessão

**Passo 1 — Selecione a pasta** `D:\COGNIS\Curso Openclaw` no Cowork ao iniciar.

**Passo 2 — Cole na primeira mensagem:**

> Leia meu INFRA em https://raw.githubusercontent.com/cognis-ia/infra/main/INFRA.md e configure o acesso SSH ao VPS com a chave em `vps_key` na pasta conectada. Usuário: `openclaw`, host: `217.77.10.26`.

Claude vai: 1) buscar o INFRA.md pela URL, 2) ler a chave `vps_key` da pasta, 3) configurar o SSH no sandbox, 4) testar a conexão — tudo automaticamente.

**Arquivo necessário na pasta:** `vps_key` (chave SSH privada — nunca compartilhe ou envie para ninguém)

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
| 💜 Gabi | `gabi` | @BE_Gabi_bot | `~/.openclaw/workspace-gabi` | _(backup pendente)_ |
| 💚 Max | `max` | @BE_Max_bot | `~/.openclaw/workspace-max` | _(backup pendente)_ |

**GitHub org:** `cognis-ia` — token no VPS em `~/.openclaw/workspace/.env`

### Bernardelli Ensino — estrutura de agentes

| Agente | Serve | Foco | Supervisão |
|--------|-------|------|------------|
| 💜 Gabi | Jane Bernardelli | Criação de conteúdo, edição visual (Canva), vendas, lançamentos | BrIA monitora |
| 💚 Max | Marilia | Planejamento, copy, mapeamento de cursos, YouTube, dados de lançamentos | BrIA monitora |

- **BrIA supervisiona Gabi e Max** — cron ativo a cada 30min (`*/30 * * * *`); script em `~/supervisao-bernardelli.sh`; log em `~/.openclaw/supervisao-bernardelli.log`; alerta para Bruno (ID `1950767646`) via Telegram da BrIA se gateway cair ou canal Gabi/Max sair do ar
- Personas salvas em `IDENTITY.md`, `SOUL.md` e `USER.md` nos respectivos workspaces
- Tokens Telegram de Gabi (@BE_Gabi_bot) e Max (@BE_Max_bot) configurados e ativos

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
- **Brave Search:** ativo — chave no VPS em `~/.openclaw/openclaw.json`
- **Telegram accounts:** `default` (Rocky), `leo` (Léo), `bria` (BrIA)

---

## Credenciais

Todas as credenciais ficam no VPS — nunca neste arquivo.
Para acessá-las quando necessário, usar SSH e ler os arquivos de config do VPS.

- **OpenAI Codex OAuth:** conta `contato@pintandotelas.com.br` — **expira ~22 maio 2026** (tem refresh_token; deve renovar automaticamente)
  - Para renovar manualmente se necessário: SSH no VPS → `~/.npm-global/bin/openclaw models auth login --provider openai-codex` (precisa de TTY, fazer direto no terminal)
- Tokens de API: `~/.config/systemd/user/openclaw-gateway.service.d/`
- GitHub token: `~/.openclaw/workspace/.env`

---

## exec-approvals — allowlist global (`*`)

Todos os agentes executam sem pedir aprovação:
`git`, `/usr/bin/git`, `/bin/bash`, `/usr/bin/bash`, `/bin/sh`, `date`, `/usr/bin/date`, `/usr/bin/python3`, `/usr/bin/env`, `/home/openclaw/.npm-global/bin/openclaw`

Allowlist `main` (Rocky): adicional `~/.local/bin/gog`
Allowlist `leo`: adicional `~/.local/bin/gog`

---

## Starter Kit v2.5.6

Instalado em Rocky, Léo e BrIA. 19 skills cada:
- `starter/` (10): onboarding-checklist, wizard-agente, wizard-aluno, wizard-autonomia, wizard-conectar, wizard-workspace, wizard-whisper-quick, primeira-vitoria, continuar-jornada, gera-log-jornada
- `operacional/` (4): backup-workspace-github, commit-diario-workspace, cron-resume-wizards, seguranca-checklist
- `planejamento/` (4): brainstorming, executing-plans, verification-before-completion, writing-plans
- `canais/` (1): wizard-whatsapp

---

## BrIA — Bernardelli Ensino

- **Empresa:** Bernardelli Ensino (