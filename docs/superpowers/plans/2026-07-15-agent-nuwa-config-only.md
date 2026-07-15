# Agent NÜWA Config-Only Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the project to `agent-nuwa` and leave a four-file, config-only Codex custom-agent repository with no Python package or CLI.

**Architecture:** The repository becomes a direct distribution of one Codex agent definition at `agents/nuwa.toml`. Installation is a documented file copy into the user's Codex home; no executable wrapper or language runtime is part of the project.

**Tech Stack:** TOML, Markdown, Git, GitHub CLI

## Global Constraints

- The final tracked tree contains exactly `.gitignore`, `LICENSE`, `README.md`, and `agents/nuwa.toml`.
- The agent definition moves byte-for-byte from `src/project_nuwa/agents/nuwa.toml` to `agents/nuwa.toml`.
- Repository, local directory, origin URL, and active project references use `agent-nuwa`.
- The Codex runtime identity remains `nuwa`; the installed destination remains `agents/nuwa.toml`.
- Do not modify `/Users/zhouzhen24/.codex/agents/nuwa.toml`.
- Preserve the clean public Git history; do not delete or recreate the repository and do not rewrite commits.
- The final repository contains no Python distribution, module, installer, CLI, tests, or build artifacts.

---

### Task 1: Convert the repository to a direct agent definition

**Files:**
- Create: `agents/nuwa.toml`
- Modify: `.gitignore`
- Modify: `README.md`
- Delete: `pyproject.toml`
- Delete: `src/project_nuwa/`
- Delete: `tests/`

**Interfaces:**
- Consumes: the current packaged agent definition at `src/project_nuwa/agents/nuwa.toml`
- Produces: a manually installable Codex agent definition at `agents/nuwa.toml`

- [ ] **Step 1: Capture the source-agent checksum**

Run:

```bash
shasum -a 256 src/project_nuwa/agents/nuwa.toml
```

Expected: one SHA-256 value to compare after the move.

- [ ] **Step 2: Move the agent definition and remove the Python wrapper**

Move `src/project_nuwa/agents/nuwa.toml` to `agents/nuwa.toml`. Delete
`pyproject.toml`, all remaining files under `src/project_nuwa/`, and all files
under `tests/`. Remove ignored `build/`, `dist/`, `*.egg-info`, `__pycache__`,
`.pytest_cache`, `.coverage`, and `.venv` artifacts if present.

- [ ] **Step 3: Replace `.gitignore` with the config-only rule**

```gitignore
.DS_Store
```

- [ ] **Step 4: Replace `README.md` with config-only documentation**

```markdown
# NÜWA

NÜWA is a Codex custom agent that creates one purpose-built, expert-guided
agent for one bounded job. It chooses the professional discipline that best
fits the job, converts that discipline into concrete working rules, and
registers one focused agent through Codex's native agent interface.

## Requirements

- A current Codex release with custom-agent support

## Install

Clone this repository, then copy the agent definition into your Codex home:

\`\`\`sh
git clone https://github.com/zzzhouzhenzz/agent-nuwa.git
cd agent-nuwa
mkdir -p "${CODEX_HOME:-$HOME/.codex}/agents"
cp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
\`\`\`

Restart Codex or begin a new task so it reloads custom-agent configuration.

## Use

Give NÜWA exactly one job:

\`\`\`text
Use the custom agent nuwa to create a coding agent for this one job:

Add bounded retries to the upload client and verify timeout behavior.
\`\`\`

NÜWA creates the agent; it does not run or supervise the resulting job. Coding,
debugging, refactoring, and code-review jobs use Linus Torvalds' relevant
engineering standards without impersonation.

## Update

Pull the latest repository changes and copy `agents/nuwa.toml` to the same
destination again.

## Remove

Remove `agents/nuwa.toml` from the Codex home used during installation.

## License

MIT. See [LICENSE](LICENSE).
```

- [ ] **Step 5: Verify the config-only tree before committing**

Run:

```bash
python3 -c 'import pathlib,tomllib; p=pathlib.Path("agents/nuwa.toml"); d=tomllib.loads(p.read_text()); assert d["name"] == "nuwa"; print(p)'
shasum -a 256 agents/nuwa.toml
git diff --check
git status --short
```

Expected: TOML parse succeeds, the checksum matches Step 1, diff check is
silent, and status shows only the intended move, edits, and Python deletions.

- [ ] **Step 6: Commit the config-only conversion**

```bash
git add -A
git commit -m "refactor: make NÜWA config-only"
```

Expected: one commit containing the direct agent file, documentation update,
and Python-wrapper removal.

### Task 2: Remove planning artifacts and rename the project everywhere active

**Files:**
- Delete: `docs/superpowers/specs/2026-07-15-agent-nuwa-config-only-design.md`
- Delete: `docs/superpowers/plans/2026-07-15-agent-nuwa-config-only.md`
- Rename directory: `/Users/zhouzhen24/ml-workspace/project-nuwa-public` to `/Users/zhouzhen24/ml-workspace/agent-nuwa`

**Interfaces:**
- Consumes: the config-only commit from Task 1
- Produces: the final four-file project at the public `agent-nuwa` URL

- [ ] **Step 1: Remove temporary design and plan artifacts**

Delete `docs/` completely, then confirm the tracked tree contains exactly the
four final paths:

```bash
git add -A
git diff --cached --check
git diff --cached --name-status
git commit -m "chore: finalize minimal agent repository"
git ls-tree -r --name-only HEAD
```

Expected tree:

```text
.gitignore
LICENSE
README.md
agents/nuwa.toml
```

- [ ] **Step 2: Rename the GitHub repository and update origin**

```bash
gh repo rename -R zzzhouzhenzz/project-nuwa agent-nuwa --yes
git remote set-url origin https://github.com/zzzhouzhenzz/agent-nuwa.git
git push origin main
```

Expected: GitHub rename succeeds and `main` pushes to `agent-nuwa`.

- [ ] **Step 3: Rename the local directory**

From `/Users/zhouzhen24/ml-workspace`:

```bash
mv project-nuwa-public agent-nuwa
```

Expected: only `/Users/zhouzhen24/ml-workspace/agent-nuwa` exists.

- [ ] **Step 4: Run final local and remote verification**

From `/Users/zhouzhen24/ml-workspace/agent-nuwa`:

```bash
python3 -c 'import pathlib,tomllib; p=pathlib.Path("agents/nuwa.toml"); d=tomllib.loads(p.read_text()); assert d["name"] == "nuwa"; print("nuwa.toml valid")'
test "$(git ls-tree -r --name-only HEAD | wc -l | tr -d " ")" = 4
! git grep -nE 'project-nuwa|project_nuwa|/Users/zhouzhen24|/home/' HEAD
test "$(git remote get-url origin)" = "https://github.com/zzzhouzhenzz/agent-nuwa.git"
git status --short --branch
gh repo view zzzhouzhenzz/agent-nuwa --json nameWithOwner,url,visibility,defaultBranchRef
git ls-remote https://github.com/zzzhouzhenzz/agent-nuwa.git
curl -sSIL https://github.com/zzzhouzhenzz/project-nuwa | sed -n '1,20p'
```

Expected: TOML valid; four tracked files; no stale names or machine-local paths;
clean `main` tracking `origin/main`; public GitHub repository named
`zzzhouzhenzz/agent-nuwa`; remote `main` matches local HEAD; the old URL returns
a GitHub redirect or the renamed repository page rather than a separate repo.
