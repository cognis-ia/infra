#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from html import escape
from pathlib import Path


HOME = Path.home()
STATE = HOME / ".openclaw"
ROOT = STATE / "mission-control"
DATA_DIR = ROOT / "data"
INFRA = STATE / "infra" / "INFRA.md"
GOV = STATE / "cerebro-governanca"
REPORT_DIR = GOV / "auditorias" / "reports"

AGENTS = [
    {"name": "Rocky", "role": "Pessoal + auditor", "path": STATE / "workspace", "repo": "clawdio-workspace-backup"},
    {"name": "Leo", "role": "Profissional Cognis", "path": STATE / "workspace-leo", "repo": "leo-workspace-backup"},
    {"name": "BrIA", "role": "Bernardelli Ensino", "path": STATE / "workspace-bria", "repo": "bria-workspace-backup"},
    {"name": "Gabi", "role": "Agente da Jane", "path": STATE / "workspace-gabi", "repo": "gabi-workspace-backup"},
    {"name": "Max", "role": "Agente da Marilia", "path": STATE / "workspace-max", "repo": "max-workspace-backup"},
]

CORE_REPOS = [
    {"name": "governanca", "path": GOV},
    {"name": "diretoria", "path": STATE / "cerebro-diretoria"},
    {"name": "infra", "path": STATE / "infra"},
]


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 25) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout.strip()
    except Exception as exc:  # noqa: BLE001
        return 999, str(exc)


def git_summary(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"exists": False, "clean": False, "last_commit": "-", "dirty": ["workspace ausente"]}
    status_code, status = run(["git", "status", "--short"], cwd=path)
    log_code, log = run(["git", "log", "-1", "--oneline"], cwd=path)
    remote_code, remote = run(["git", "remote", "-v"], cwd=path)
    dirty = [line for line in status.splitlines() if line.strip()]
    return {
        "exists": True,
        "clean": status_code == 0 and not dirty,
        "dirty": dirty[:8],
        "last_commit": log if log_code == 0 and log else "-",
        "has_remote": remote_code == 0 and bool(remote.strip()),
    }


def latest_audit() -> dict[str, object]:
    reports = sorted(REPORT_DIR.glob("auditoria-agentes-*.md"))
    if not reports:
        return {"found": False}
    path = reports[-1]
    text = path.read_text(encoding="utf-8", errors="replace")
    score = re.search(r"Conformidade geral: ([^\n]+)", text)
    crit = re.search(r"Críticos: (\d+)", text)
    high = re.search(r"Altos: (\d+)", text)
    med = re.search(r"Médios: (\d+)", text)
    per_agent = re.findall(r"### ([^—\n]+) — ([^\n]+)\n\n((?:- .+\n)+)", text)
    agents = []
    for name, agent_score, block in per_agent:
        issues = [line[2:] for line in block.splitlines() if line.startswith("- ") and "Último commit:" not in line]
        agents.append({"name": name.strip(), "score": agent_score.strip(), "issues": issues})
    return {
        "found": True,
        "file": str(path),
        "score": score.group(1).strip() if score else "-",
        "criticos": int(crit.group(1)) if crit else 0,
        "altos": int(high.group(1)) if high else 0,
        "medios": int(med.group(1)) if med else 0,
        "agents": agents,
    }


def systemd_timers() -> list[dict[str, str]]:
    code, out = run(["systemctl", "--user", "list-timers", "--all"])
    if code != 0:
        return [{"timer": "systemctl indisponivel", "next": "-", "last": out[:160], "service": "-"}]
    rows = []
    for line in out.splitlines():
        if not re.search(r"openclaw|rocky|bria|gabi|max|leo|backup-workspace|heartbeat-runner|mission-control", line):
            continue
        parts = line.split()
        service = parts[-1] if parts else "-"
        timer = parts[-2] if len(parts) > 1 else "-"
        rows.append({"raw": line, "timer": timer, "service": service})
    return rows


def openclaw_crons() -> list[str]:
    cli = HOME / ".npm-global/bin/openclaw"
    code, out = run([str(cli), "cron", "list"], timeout=35)
    if code != 0:
        return [out[:300]]
    lines = [line for line in out.splitlines() if line.strip()]
    return lines[:20]


def infra_pendencias() -> list[str]:
    if not INFRA.exists():
        return ["INFRA.md nao encontrado"]
    text = INFRA.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Pendências\n\n(.+?)\n---\n\nRegra absoluta", text, re.S)
    if not match:
        return ["Secao Pendencias nao encontrada"]
    lines = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(token in stripped for token in ["CONCLUIDO", "CONCLUIDA"]):
            continue
        lines.append(stripped)
    return lines[:36]


def collect() -> dict[str, object]:
    now = datetime.now().astimezone()
    return {
        "generated_at": now.isoformat(timespec="seconds"),
        "agents": [{**agent, "path": str(agent["path"]), "git": git_summary(agent["path"])} for agent in AGENTS],
        "core_repos": [{**repo, "path": str(repo["path"]), "git": git_summary(repo["path"])} for repo in CORE_REPOS],
        "audit": latest_audit(),
        "timers": systemd_timers(),
        "crons": openclaw_crons(),
        "pendencias": infra_pendencias(),
    }


def badge(text: str, kind: str = "neutral") -> str:
    return f'<span class="badge {kind}">{escape(text)}</span>'


def render(data: dict[str, object]) -> str:
    audit = data["audit"]
    agents = data["agents"]
    repos = data["core_repos"]
    timers = data["timers"]
    crons = data["crons"]
    pendencias = data["pendencias"]

    def agent_card(agent: dict[str, object]) -> str:
        git = agent["git"]
        state = "ok" if git["clean"] else "warn"
        dirty = "".join(f"<li>{escape(x)}</li>" for x in git.get("dirty", [])) or "<li>limpo</li>"
        return f"""
        <article class="card agent">
          <div class="card-top">
            <div><h3>{escape(agent['name'])}</h3><p>{escape(agent['role'])}</p></div>
            {badge('limpo' if git['clean'] else 'dirty', state)}
          </div>
          <p class="mono">{escape(git['last_commit'])}</p>
          <ul>{dirty}</ul>
        </article>
        """

    def repo_row(repo: dict[str, object]) -> str:
        git = repo["git"]
        return f"""
        <tr>
          <td>{escape(repo['name'])}</td>
          <td>{badge('limpo' if git['clean'] else 'dirty', 'ok' if git['clean'] else 'warn')}</td>
          <td class="mono">{escape(git['last_commit'])}</td>
        </tr>
        """

    timer_items = "".join(f"<li><span>{escape(t.get('timer','-'))}</span><code>{escape(t.get('service','-'))}</code></li>" for t in timers)
    cron_items = "".join(f"<li><code>{escape(line)}</code></li>" for line in crons)
    pending_items = "".join(f"<li>{escape(line)}</li>" for line in pendencias)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mission Control Cognis IA</title>
  <style>
    :root {{
      --bg: #f6f4ef;
      --ink: #1d2328;
      --muted: #66706b;
      --line: #d8d2c6;
      --panel: #fffdfa;
      --ok: #1f7a4d;
      --warn: #a36217;
      --bad: #ad3330;
      --accent: #245f73;
      --accent-2: #7a4d25;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif;
      background: var(--bg);
      color: var(--ink);
      letter-spacing: 0;
    }}
    header {{
      padding: 28px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: #ece8dd;
    }}
    h1 {{ margin: 0; font-size: 28px; line-height: 1.15; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; }}
    h3 {{ margin: 0; font-size: 16px; }}
    p {{ margin: 6px 0 0; color: var(--muted); }}
    main {{ padding: 24px 32px 40px; max-width: 1440px; margin: 0 auto; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(160px, 1fr));
      gap: 12px;
      margin-bottom: 22px;
    }}
    .metric, .card, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .metric {{ padding: 16px; min-height: 94px; }}
    .metric strong {{ display: block; font-size: 26px; margin-top: 8px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 22px;
    }}
    .card {{ padding: 14px; min-height: 180px; }}
    .card-top {{ display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
      border: 1px solid currentColor;
    }}
    .badge.ok {{ color: var(--ok); }}
    .badge.warn {{ color: var(--warn); }}
    .badge.bad {{ color: var(--bad); }}
    .badge.neutral {{ color: var(--accent); }}
    .mono, code {{
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 12px;
      overflow-wrap: anywhere;
    }}
    ul {{ margin: 10px 0 0; padding-left: 18px; color: var(--muted); }}
    li {{ margin: 6px 0; }}
    .columns {{ display: grid; grid-template-columns: 1.1fr .9fr; gap: 16px; }}
    .panel {{ padding: 16px; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    td, th {{ padding: 9px 6px; border-top: 1px solid var(--line); text-align: left; vertical-align: top; }}
    .list-tight li {{ display: flex; justify-content: space-between; gap: 12px; border-top: 1px solid var(--line); padding-top: 8px; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .summary, .grid, .columns {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Mission Control Cognis IA</h1>
    <p>Gerado em {escape(data['generated_at'])}. Painel read-only: observa, nao corrige.</p>
  </header>
  <main>
    <section class="summary">
      <div class="metric"><span>Auditoria</span><strong>{escape(audit.get('score','-') if audit.get('found') else '-')}</strong></div>
      <div class="metric"><span>Criticos</span><strong>{escape(str(audit.get('criticos','-')))}</strong></div>
      <div class="metric"><span>Altos</span><strong>{escape(str(audit.get('altos','-')))}</strong></div>
      <div class="metric"><span>Medios</span><strong>{escape(str(audit.get('medios','-')))}</strong></div>
    </section>

    <section>
      <h2>Agentes</h2>
      <div class="grid">{''.join(agent_card(a) for a in agents)}</div>
    </section>

    <section class="columns">
      <div>
        <section class="panel">
          <h2>Repos centrais</h2>
          <table><tbody>{''.join(repo_row(r) for r in repos)}</tbody></table>
        </section>
        <section class="panel">
          <h2>Timers systemd</h2>
          <ul class="list-tight">{timer_items}</ul>
        </section>
      </div>
      <div>
        <section class="panel">
          <h2>Pendencias INFRA</h2>
          <ul>{pending_items}</ul>
        </section>
        <section class="panel">
          <h2>Crons OpenClaw</h2>
          <ul>{cron_items}</ul>
        </section>
      </div>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = collect()
    (DATA_DIR / "status.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "index.html").write_text(render(data), encoding="utf-8")
    print(ROOT / "index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
