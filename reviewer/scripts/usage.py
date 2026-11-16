"""Token and tool usage of the current review, as a markdown section to append to the findings file.

Usage: usage.py [<session-id>]
Transcripts: ${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<encoded root>/<session>.jsonl (+ <session>/subagents/).
Without a session id, the most recently modified transcript of this repo is used.
"""
import datetime
import glob
import json
import os
import re
import sys
from collections import OrderedDict

from gitutil import toplevel

COMMAND = re.compile(r"<command-name>/reviewer<")
PREVIOUS_RUN = re.compile(r"usage\.py\s+[0-9a-f]{8}-")
SHELL_CATEGORIES = [("walkthrough", r"walkthrough\.py"), ("rules", r"rules/"),
              ("git", r"\bgit (diff|show|log|fetch|merge-base|rev-parse|grep)"), ("github cli", r"\bgh\b"),
              ("sed / cat (reading code)", r"\b(sed -n|cat|head)\b"), ("grep / find", r"\b(grep|rg|find)\b")]
FIELDS = ["cache_read_input_tokens", "cache_creation_input_tokens", "input_tokens", "output_tokens"]


def transcript(session):
    projects = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
    if session:
        hits = glob.glob(os.path.join(projects, "*", session + ".jsonl"))
        return hits[0] if hits else sys.exit(f"no transcript for session {session} under {projects}")
    folder = os.path.join(projects, re.sub(r"[^A-Za-z0-9]", "-", toplevel() or os.getcwd()))
    files = glob.glob(os.path.join(folder, "*.jsonl"))
    return max(files, key=os.path.getmtime) if files else sys.exit(f"no transcripts in {folder}")


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except ValueError:
                continue
    return rows


def blocks(row):
    content = (row.get("message") or {}).get("content")
    return [{"type": "text", "text": content}] if isinstance(content, str) else [b for b in content or [] if isinstance(b, dict)]


def text_of(content):
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content or [] if isinstance(b, dict))


def window_start(rows, results):
    start = 0
    for i, row in enumerate(rows):
        if row.get("type") == "user" and COMMAND.search(text_of((row.get("message") or {}).get("content"))):
            start = i
    for i, row in enumerate(rows):
        for b in blocks(row) if row.get("type") == "assistant" else []:
            ok = b.get("type") == "tool_use" and b.get("id") in results and not results[b["id"]][1]
            if ok and PREVIOUS_RUN.search(json.dumps(b.get("input"))):
                start = max(start, i + 1)
    return start


def kind(name, data):
    if name == "Bash":
        command = data.get("command", "")
        return "bash: " + next((k for k, p in SHELL_CATEGORIES if re.search(p, command)), "other")
    if name == "Read":
        path = data.get("file_path", "")
        return "read: walkthrough" if "/walkthrough/" in path else "read: spilled output" if "tool-results" in path else "read: file"
    return name


def subagent_line(path, since, seen):
    agents, calls, totals = 0, 0, dict.fromkeys(FIELDS, 0)
    for sub in sorted(glob.glob(os.path.join(path[:-len(".jsonl")], "subagents", "agent-*.jsonl"))):
        counted = 0
        for row in load(sub):
            msg = row.get("message") or {}
            if row.get("type") != "assistant" or not msg.get("usage") or (row.get("timestamp") or "") < since:
                continue
            if msg.get("id") in seen:
                continue
            seen.add(msg.get("id"))
            counted += 1
            for k in FIELDS:
                value = msg["usage"].get(k)
                totals[k] += value if isinstance(value, int) else 0
        agents += counted > 0
        calls += counted
    if not agents:
        return None
    return (f"Subagents: {agents} · {calls} API calls · cache read {totals[FIELDS[0]]:,} · cache write "
            f"{totals[FIELDS[1]]:,} · input {totals[FIELDS[2]]:,} · output {totals[FIELDS[3]]:,}")


def main(argv):
    path = transcript(argv[0] if argv else None)
    rows = load(path)
    results = {}
    for row in rows:
        for b in blocks(row) if row.get("type") == "user" else []:
            if b.get("type") == "tool_result":
                results[b.get("tool_use_id")] = (len(text_of(b.get("content"))), bool(b.get("is_error")))
    rows = rows[window_start(rows, results):]
    calls = OrderedDict()
    for row in rows:
        msg = row.get("message") or {}
        if row.get("type") == "assistant" and msg.get("usage"):
            call = calls.setdefault(msg.get("id"), {"usage": msg["usage"], "tools": []})
            call["usage"] = msg["usage"]
            call["tools"] += [b for b in blocks(row) if b.get("type") == "tool_use"]
    if not calls:
        sys.exit("no API calls since the review started")
    calls = list(calls.values())
    times = [r["timestamp"] for r in rows if r.get("timestamp")]
    parse = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    minutes = (parse(times[-1]) - parse(times[0])).total_seconds() / 60 if times else 0.0
    ctx = lambda u: sum(u.get(k) or 0 for k in FIELDS[:3])
    sums = [sum(c["usage"].get(k) or 0 for c in calls) for k in FIELDS]
    tools = {}
    for i, call in enumerate(calls):
        for b in call["tools"]:
            tokens = results.get(b.get("id"), (0, False))[0] / 3.5
            row = tools.setdefault(kind(b.get("name"), b.get("input") or {}), [0, 0.0, 0.0])
            row[0] += 1
            row[1] += tokens
            row[2] += tokens * (len(calls) - 1 - i)
    out = ["", "## Token usage", "",
           f"Session `{os.path.basename(path)[:8]}` · {minutes:.1f} min · {len(calls)} API calls · "
           f"context {ctx(calls[0]['usage']):,} → {ctx(calls[-1]['usage']):,}", "",
           "| cache read tokens | cache write tokens | input tokens | output tokens |", "|---:|---:|---:|---:|",
           "| " + " | ".join(f"{s:,}" for s in sums) + " |", "",
           "| tool kind | calls | ~tokens it added | ~tokens re-read later |", "|---|---:|---:|---:|"]
    for name, (count, added, reread) in sorted(tools.items(), key=lambda t: -t[1][2]):
        out.append(f"| {name} | {count} | {int(added):,} | {int(reread):,} |")
    seen = {m.get("id") for r in rows for m in [r.get("message") or {}] if r.get("type") == "assistant"}
    line = subagent_line(path, times[0] if times else "", seen)
    if line:
        out += ["", line]
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
