# Mission Control Cognis IA

Dashboard read-only para acompanhar o estado dos agentes OpenClaw do Bruno.

## O que mostra

- status dos 5 agentes;
- ultimo commit e working tree;
- auditoria mais recente;
- timers systemd relevantes;
- crons OpenClaw;
- pendencias do `INFRA.md`;
- links/paths operacionais.

## Como gerar

No VPS:

```bash
python3 ~/.openclaw/mission-control/scripts/generate_status.py
```

Saidas:

- `~/.openclaw/mission-control/index.html`
- `~/.openclaw/mission-control/data/status.json`

## Regras

- Read-only.
- Nao acessa `cerebro-diretoria`.
- Nao usa tokens.
- Nao abre porta publica.
- Nao corrige nada automaticamente.
