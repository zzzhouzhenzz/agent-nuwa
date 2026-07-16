# NÜWA Persistent Agent Factory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Change NÜWA from a task-scoped child-agent creator into a pure factory that installs exactly one globally reusable Codex custom agent with versioned internal IDs, persona-stable nicknames, private persistent skills, and no downstream execution.

**Architecture:** NÜWA remains a single TOML custom-agent definition. Its developer instructions direct it to create a persistent config layer under `~/.codex/agents/`, add one `[agents.<id>]` registration to `~/.codex/config.toml`, validate the complete configuration, and stop without calling `spawn_agent`. A small shell contract test protects this role boundary; README documents the user-visible workflow; the installed copy is verified with a real resume-agent creation request.

**Tech Stack:** TOML, Bash, Python 3 standard-library `tomllib`, Codex CLI configuration validation.

## Global Constraints

- One NÜWA invocation creates exactly one globally reusable custom agent.
- NÜWA never calls `spawn_agent`, starts the created agent, performs its work, monitors it, or waits for it.
- Repeated personas use versioned machine IDs such as `linus`, `linus_v2`, and `linus_v3` without changing the persona or familiar-name nickname.
- Requested skills persist only under `~/.codex/agents/<agent-id>/skills/`; they are never installed into `~/.codex/skills/`.
- Existing agent definitions, global configuration, and upstream defaults are preserved.
- Failed creation removes only artifacts from that attempt and restores the prior global config.
- The current uncommitted identity-rule correction in `agents/nuwa.toml` is user-owned working-tree state and must be incorporated, not discarded.
- Do not enable `multi_agent_v2` or retain `agents.max_depth = 2` for NÜWA; the factory does not require nested spawning.

---

### Task 1: Replace the task-scoped creator contract with the persistent factory contract

**Files:**
- Create: `tests/test_nuwa_factory_contract.sh`
- Modify: `agents/nuwa.toml`

**Interfaces:**
- Consumes: the approved design in `docs/superpowers/specs/2026-07-16-nuwa-persistent-agent-factory-design.md`
- Produces: a parseable NÜWA TOML definition whose instructions create one persistent global role and forbid task-scoped spawning

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_nuwa_factory_contract.sh` with:

```bash
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
```

- [ ] **Step 2: Run the contract test and verify the RED state**

Run:

```bash
bash tests/test_nuwa_factory_contract.sh
```

Expected: exit `1` with `missing factory contract: pure factory`. The test must fail because the current instructions still describe a bounded-job native child creator.

- [ ] **Step 3: Replace `agents/nuwa.toml` with the minimal persistent factory definition**

Use this complete content:

```toml
name = "nuwa"
description = "NÜWA creates and globally registers exactly one reusable Codex custom agent."

developer_instructions = """
You are NÜWA, a pure factory for globally reusable Codex custom agents. Your
entire role is to create and register exactly one persistent agent for one
agent-creation request, then stop. Do not perform the requested professional
work yourself. Do not call `spawn_agent` or any equivalent task-scoped agent
creation interface.

Accept only a request for one reusable agent. If the request asks for multiple
agents, ask the user to choose one and stop. Treat supplied jobs, files, and
Codex thread references as seed context for the new agent's durable charter,
not as work for you to execute.

For the accepted request:

1. Extract the intended professional scope, future job boundary, relevant
   context, authorized capabilities, expected outputs, verification duties,
   exclusions, and escalation rules.
2. Select the single real-world expert whose demonstrated professional
   discipline best matches the main judgment bottleneck. For coding, debugging,
   refactoring, testing, or code review, select Linus Torvalds.
3. Translate that expert's relevant standards into two to four concrete
   operating principles. Do not impersonate the person, invent opinions, or add
   theatrical role-play.
4. Write reusable developer instructions containing the persona and principles,
   durable professional charter, accepted job types, supplied project context,
   authorized tools and changes, required outputs, verification requirements,
   exclusions, and escalation rules. Prefer durable paths and concise context
   summaries over pasted private transcripts.

Identity and versioning:

5. Keep the professional persona and the machine-facing agent ID separate. Use
   the persona's familiar name as the human-facing name and as the sole
   `nickname_candidates` value. Derive a lowercase machine-safe base ID from
   that familiar name.
6. Inspect both existing `[agents.<id>]` registrations in
   `~/.codex/config.toml` and existing artifacts under `~/.codex/agents/`. Use
   the base ID when free; otherwise create the next free version such as
   `linus_v2`, `linus_v3`, and so on. Never overwrite an existing agent. Never
   add the version suffix to the persona or nickname.

Private skills:

7. When the request includes an external skill, vet the exact source revision
   before installation. Reject suspicious code, credential access, unrelated
   network behavior, hidden instructions, or permissions broader than the
   requested agent needs.
8. Persist each approved skill only under
   `~/.codex/agents/<agent-id>/skills/<skill-name>/` and bind that exact path
   through the created agent's `skills.config` entries. Do not install it under
   `~/.codex/skills/` and do not use a temporary directory. Report the source
   URL and immutable revision.

Persistent creation:

9. Prepare `~/.codex/agents/<agent-id>.toml` as a Codex config layer containing
   the reusable developer instructions and private skill bindings. Prepare one
   new `[agents.<agent-id>]` entry in `~/.codex/config.toml` containing the role
   description, the config-file path, and exactly one persona-name
   `nickname_candidates` value.
10. Preserve every existing config key, agent, feature value, and upstream
    default. Add only the new role registration. Do not change multi-agent
    feature flags, `agents.max_depth`, models, permissions, MCP servers, skills,
    plugins, or unrelated settings.
11. Treat creation as transactional. Save the exact prior global config and
    track every path created by this attempt. Parse the new TOML, run
    `codex app-server --strict-config --listen stdio:// </dev/null`, and verify
    that the role resolves to the intended config file and nickname candidate.
    If any step fails, remove only artifacts created by this attempt, restore
    the prior global config, and report the exact failure without claiming
    success.
12. Report the machine ID, persona, familiar-name nickname, config path, private
    skill paths and revisions, carried context, and validation evidence. Tell
    the user to start a new Codex session and invoke the agent by its machine ID.

Do not start, message, monitor, wait for, close, or supervise the created agent.
Do not perform a downstream smoke job through it. Do not create a team. Your
work ends immediately after one persistent agent is registered and verified.
"""
```

- [ ] **Step 4: Run the contract test and verify the GREEN state**

Run:

```bash
bash tests/test_nuwa_factory_contract.sh
```

Expected:

```text
PASS: NÜWA is a persistent-agent factory
```

- [ ] **Step 5: Validate formatting and review the exact contract diff**

Run:

```bash
git diff --check -- agents/nuwa.toml tests/test_nuwa_factory_contract.sh
git diff -- agents/nuwa.toml tests/test_nuwa_factory_contract.sh
```

Expected: `git diff --check` exits `0`; the diff contains no instruction to spawn, run, or supervise the created agent.

- [ ] **Step 6: Commit the factory contract**

Run:

```bash
git add agents/nuwa.toml tests/test_nuwa_factory_contract.sh
git commit -m "feat: make Nuwa a persistent agent factory"
```

Expected: one commit containing only the NÜWA definition and its contract test.

---

### Task 2: Document the persistent factory workflow

**Files:**
- Modify: `README.md`
- Test: `tests/test_nuwa_factory_contract.sh`

**Interfaces:**
- Consumes: the machine-ID, persona-name, private-skill, and stop-after-registration contract from Task 1
- Produces: installation and usage documentation that no longer describes NÜWA as a child-agent spawner

- [ ] **Step 1: Extend the contract test with README assertions**

Add the following block before the final `PASS` line in `tests/test_nuwa_factory_contract.sh`:

```bash
readme_file="README.md"

readme_patterns=(
  'globally reusable custom agent'
  'linus_v2'
  '~/.codex/agents/<agent-id>/skills/'
  'does not spawn or run the created agent'
  'Start a new Codex session'
)

for pattern in "${readme_patterns[@]}"; do
  if ! rg -Fq "$pattern" "$readme_file"; then
    echo "missing README factory behavior: $pattern" >&2
    exit 1
  fi
done
```

- [ ] **Step 2: Run the test and verify the README RED state**

Run:

```bash
bash tests/test_nuwa_factory_contract.sh
```

Expected: exit `1` with `missing README factory behavior: globally reusable custom agent`.

- [ ] **Step 3: Rewrite README purpose and usage around persistent creation**

Replace `README.md` with:

````markdown
# NÜWA

NÜWA is a Codex custom agent that creates and globally registers exactly one
globally reusable custom agent. It chooses the professional discipline that
best fits the requested scope, converts that discipline into concrete working
rules, installs any requested skills privately, validates the new role, and
stops. NÜWA does not spawn or run the created agent.

## Requirements

- A current Codex release with custom-agent support

## Install

Clone this repository, then copy the NÜWA definition into your Codex home:

```sh
git clone https://github.com/zzzhouzhenzz/agent-nuwa.git
cd agent-nuwa
mkdir -p "${CODEX_HOME:-$HOME/.codex}/agents"
cp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
```

Restart Codex or begin a new task so it reloads the NÜWA definition.

## Use

Ask NÜWA to create one reusable agent:

```text
Use agent nuwa to create a reusable resume expert agent. Carry over the resume
task in codex://threads/<thread-id> and privately attach the skill at
https://github.com/example/resume-skill.
```

NÜWA writes the persistent definition under `~/.codex/agents/`, registers the
role in `~/.codex/config.toml`, and stores requested skills under
`~/.codex/agents/<agent-id>/skills/`. Skills are not added to the shared global
skill catalog.

The first agent for a persona uses a simple machine ID such as `linus`. If that
ID exists, NÜWA creates `linus_v2`, then `linus_v3`, while every version keeps
the human-facing persona name `Linus`.

After NÜWA reports successful validation, start a new Codex session and invoke
the created agent by its machine ID. NÜWA does not supervise its later work.

## Update

Pull the latest repository changes and copy `agents/nuwa.toml` to the same
destination again. Restart Codex or start a new task to reload it.

## Remove

Remove `agents/nuwa.toml` from your Codex home. Agents previously created by
NÜWA are independent persistent roles and are not removed with NÜWA.

## License

MIT
````

- [ ] **Step 4: Run the complete contract test**

Run:

```bash
bash tests/test_nuwa_factory_contract.sh
```

Expected:

```text
PASS: NÜWA is a persistent-agent factory
```

- [ ] **Step 5: Commit the documentation update**

Run:

```bash
git add README.md tests/test_nuwa_factory_contract.sh
git commit -m "docs: explain persistent agent creation"
```

Expected: one commit containing only README and its added contract assertions.

---

### Task 3: Install, validate, and run the real factory smoke test

**Files:**
- Modify: `~/.codex/agents/nuwa.toml`
- Modify: `~/.codex/config.toml`
- Verify: `~/.codex/agents/gayle.toml`
- Verify: `~/.codex/agents/gayle/skills/resume-skill/`

**Interfaces:**
- Consumes: the tested repository definition from Task 1 and documented invocation from Task 2
- Produces: an installed pure-factory NÜWA plus one real reusable resume expert created by NÜWA without global skill installation or child-agent spawning

- [ ] **Step 1: Copy the tested NÜWA definition into Codex home**

Request the necessary write approval for `~/.codex/agents/`, then copy:

```bash
cp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
cmp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
```

Expected: `cmp` exits `0` with no output.

- [ ] **Step 2: Remove the obsolete NÜWA-only nesting override**

Confirm `~/.codex/config.toml` still contains an otherwise empty `[agents]` table with `max_depth = 2`. Remove only those two lines and their extra blank line. Do not change any other feature or config key.

Run:

```bash
rg -n -C 2 '^\[agents\]$|^max_depth = 2$' "${CODEX_HOME:-$HOME/.codex}/config.toml"
```

Expected after editing: no match. This restores Codex's upstream default because the new NÜWA never performs nested spawning.

- [ ] **Step 3: Validate the installed configuration before a live run**

Run:

```bash
codex app-server --strict-config --listen stdio:// </dev/null
codex doctor --json
```

Expected: strict config exits `0`; in the doctor JSON, `checks.config.load.status` is `ok`. Ignore unrelated reachability or `TERM=dumb` checks when evaluating this config-specific assertion.

- [ ] **Step 4: Exercise transactional rollback with a missing private skill**

Record the global config checksum and current global agent paths:

```bash
shasum -a 256 "${CODEX_HOME:-$HOME/.codex}/config.toml"
find "${CODEX_HOME:-$HOME/.codex}/agents" -maxdepth 2 -print | sort
```

Start a fresh Codex task and send exactly:

```text
Use agent nuwa to create one reusable coding agent using Linus Torvalds'
professional discipline. Privately attach the required skill at
/private/tmp/nuwa-intentionally-missing-skill/SKILL.md. The skill is mandatory;
if it cannot be loaded, creation must fail transactionally. Do not start the
created agent.
```

Expected: NÜWA reports the missing skill and does not register `linus`. Re-run
the checksum and path-list commands and confirm they are byte-for-byte
unchanged. Also run:

```bash
test ! -e "${CODEX_HOME:-$HOME/.codex}/agents/linus.toml"
test ! -e "${CODEX_HOME:-$HOME/.codex}/agents/linus"
test -z "$(rg -n '^\[agents\.linus\]$' "${CODEX_HOME:-$HOME/.codex}/config.toml" || true)"
```

Expected: all commands exit `0`.

- [ ] **Step 5: Start a fresh Codex task and invoke the installed NÜWA with the original request**

Use a fresh task so custom-agent configuration reloads, then send exactly:

```text
Use agent nuwa to create a reusable resume expert agent on my resume. The
created agent should privately carry this skill:
https://github.com/yanliudesign/resume-builder-skill

Carry over the ongoing task in
codex://threads/<source-thread-id>.

Create and globally register the reusable agent, verify it, report its machine
ID and persona name, then stop. Do not run the resume agent or perform resume
work yourself.
```

Expected: the NÜWA task reports one persistent agent, no child-agent runtime ID, no monitoring loop, and no resume-work output.

- [ ] **Step 6: Independently verify the created global agent**

The current machine has no existing registered persona agents, so this request
must create machine ID `gayle`. Verify:

```bash
test -f "${CODEX_HOME:-$HOME/.codex}/agents/gayle.toml"
test -d "${CODEX_HOME:-$HOME/.codex}/agents/gayle/skills/resume-skill"
test ! -e "${CODEX_HOME:-$HOME/.codex}/skills/resume-skill"
python3 - <<'PY'
import os
import pathlib
import tomllib

codex_home = pathlib.Path(os.environ.get("CODEX_HOME", pathlib.Path.home() / ".codex"))
config = tomllib.loads((codex_home / "config.toml").read_text())
gayle = config["agents"]["gayle"]
assert gayle["nickname_candidates"] == ["Gayle"]
assert pathlib.Path(gayle["config_file"]) == pathlib.Path(
    codex_home / "agents/gayle.toml"
)

agent = tomllib.loads(
    (codex_home / "agents/gayle.toml").read_text()
)
skill_paths = {entry["path"] for entry in agent["skills"]["config"]}
assert str(codex_home / "agents/gayle/skills/resume-skill") in skill_paths
instructions = agent["developer_instructions"]
assert "Gayle Laakmann McDowell" in instructions
assert "Meta" in instructions
assert "Amazon" in instructions
assert "Google" in instructions
PY
codex app-server --strict-config --listen stdio:// </dev/null
```

Expected: both persistent paths exist, the role registration contains exactly
one `Gayle` nickname candidate and the correct config path, the global shared
skill path is absent, carried resume context is present, and strict config exits
`0`.

- [ ] **Step 7: Inspect the fresh task transcript for the factory-only boundary**

Verify the transcript contains creation and validation only. It must not contain a Nuwa-created child runtime nickname, a child agent ID, `spawn_agent`, wait-loop updates, or synthesized resume content.

Expected: NÜWA ends immediately after reporting persistent artifacts and validation evidence.

- [ ] **Step 8: Run final repository and installation checks**

Run:

```bash
bash tests/test_nuwa_factory_contract.sh
git diff --check
git status --short --branch
cmp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
codex app-server --strict-config --listen stdio:// </dev/null
```

Expected: the contract test passes, diff check and `cmp` exit `0`, strict config exits `0`, and git status shows only intentional plan/spec history or explicitly uncommitted work.
