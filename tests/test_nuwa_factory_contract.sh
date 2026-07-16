#!/usr/bin/env bash
set -euo pipefail

agent_file="agents/nuwa.toml"

python3 -c 'import pathlib, tomllib; tomllib.loads(pathlib.Path("agents/nuwa.toml").read_text())'

required_patterns=(
  'pure factory'
  'globally reusable'
  '~/.codex/agents/'
  '~/.codex/config.toml'
  'nickname_candidates'
  '_v2'
  'private skill'
  'Do not call `spawn_agent`'
  'Do not start, message, monitor, wait for, close, or supervise'
  'restore the prior global config'
  'codex app-server --strict-config'
)

for pattern in "${required_patterns[@]}"; do
  if ! rg -Fq "$pattern" "$agent_file"; then
    echo "missing factory contract: $pattern" >&2
    exit 1
  fi
done

forbidden_patterns=(
  'one bounded job'
  'Create the agent through the Codex native agent interface'
  'let Codex assign its presentation-only runtime nickname'
  'native agent type, and agent ID'
)

for pattern in "${forbidden_patterns[@]}"; do
  if rg -Fq "$pattern" "$agent_file"; then
    echo "stale task-scoped contract: $pattern" >&2
    exit 1
  fi
done

echo "PASS: NÜWA is a persistent-agent factory"
