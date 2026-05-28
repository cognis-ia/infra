#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path


HOME = Path.home()
STATE = HOME / ".openclaw"
STATUS = STATE / "mission-control/data/status.json"
INFRA = STATE / "infra/INFRA.md"
OPENCLAW = HOME / ".npm-global/bin/openclaw"
TARGET = "1950767646"


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def recent_history(text: str) -> list[str]:
    blocks = re.findall(r"Historico da sessao - 2026-05-28[^\n]*\n\n(.+?)(?=\nHistorico da sessao|\Z)", text, re.S)
    lines: list[str] = []
    for block in blocks[-4:]:
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("- ") and "Tokens" not in stripped:
                lines.append(stripped[2:])
    return lines[-5:]


def pending_focus(text: str) -> list[str]:
    match = re.search(r"Pendências\n\n(.+?)\n---\n\nRegra absoluta", text, re.S)
    if not match:
        return []
    focus = []
    for line in match.group(1).splitlines():
        s = line.strip()
        if not s or "CONCLUIDO" in s or "CONCLUIDA" in s:
            continue
        if s.startswith(("A.", "B.", "C.", "E.", "H.", "I.", "J.", "M.", "N.", "O.", "4.", "8.", "9.")):
            focus.append(s)
    return focus[:5]


def build_message() -> str:
    status = read_json(STATUS)
    infra = read_text(INFRA)
    audit = status.get("audit", {})
    agents = status.get("agents", [])
    dirty = [a["name"] for a in agents if not a.get("git", {}).get("clean")]
    generated = status.get("generated_at", "-")
    wins = recent_history(infra)
    pending = pending_focus(infra)

    audit_line = f"{audit.get('score', '-')} | criticos {audit.get('criticos', '-')}, altos {audit.get('altos', '-')}, medios {audit.get('medios', '-')}"
    clean_line = "todos os workspaces limpos" if not dirty else "workspaces dirty: " + ", ".join(dirty)

    msg = [
        "Revisao do Dia - Rocky",
        "",
        f"Mission Control: {generated}",
        f"Auditoria: {audit_line}",
        f"Git: {clean_line}",
        "",
        "Vitorias recentes:",
    ]
    msg.extend(f"- {w}" for w in (wins or ["sem novas vitorias registradas no INFRA hoje"]))
    msg.extend(["", "Pendencias sem token para atacar:"])
    msg.extend(f"- {p}" for p in (pending or ["nenhuma pendencia operacional sem token encontrada"]))
    msg.extend([
        "",
        "Proximo passo recomendado: escolher entre USER blocos 9-11 (depende de entrevista) ou segundo cerebro operacional Gabi/Max.",
        "Tokens seguem para a ultima etapa.",
    ])
    return "\n".join(msg)


def main() -> int:
    subprocess.run([str(OPENCLAW), "message", "send", "--channel", "telegram", "--target", TARGET, "--message", build_message()], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
