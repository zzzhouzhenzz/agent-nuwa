# Agent NÜWA config-only rename design

## Objective

Rename the active project identity from `project-nuwa` to `agent-nuwa` and
reduce the repository to a portable Codex custom-agent definition with manual
installation instructions. The Codex agent itself remains named `nuwa`.

## Final repository contents

The active tree will contain only:

- `.gitignore`
- `LICENSE`
- `README.md`
- `agents/nuwa.toml`

The existing agent definition at `src/project_nuwa/agents/nuwa.toml` will move
unchanged to `agents/nuwa.toml`.

The retained `.gitignore` will ignore only general local OS noise such as
`.DS_Store`; Python-specific ignore rules will be removed with the wrapper.

## Removed Python wrapper

Remove `pyproject.toml`, the complete `src/project_nuwa/` package, the complete
`tests/` package, and any ignored Python build artifacts such as `build/`,
`dist/`, and `*.egg-info`. There will be no Python distribution, import module,
installer module, generated wheel, or project CLI.

## Naming changes

- GitHub repository: `zzzhouzhenzz/agent-nuwa`
- Local directory: `/Users/zhouzhen24/ml-workspace/agent-nuwa`
- Git remote: `https://github.com/zzzhouzhenzz/agent-nuwa.git`
- Project references in current tracked files: `agent-nuwa`
- Codex runtime name and installed filename: `nuwa` and `agents/nuwa.toml`
- Product heading and prose branding: `NÜWA`

The earlier clean public commit remains in repository history. This is a normal
rename commit, not another history rewrite.

## Installation documentation

The README will document cloning the repository and copying
`agents/nuwa.toml` to the selected Codex home. `CODEX_HOME` is used when set;
otherwise the documented default is `~/.codex`. Installation must not imply
that Python, pip, or a package registry is required.

## Safety boundaries

Do not delete or modify the installed `/Users/zhouzhen24/.codex/agents/nuwa.toml`.
Do not delete the public repository or rewrite its clean history. Do not change
the behavior or identity encoded by the NÜWA agent definition. Do not touch
files outside the project directory except for renaming that directory.

## Verification

Before completion:

1. Parse `agents/nuwa.toml` with Python's standard `tomllib` as a verification
   tool only; Python is not a project dependency.
2. Confirm the current tracked tree contains exactly the four intended files.
3. Confirm no current tracked file contains `project-nuwa`, `project_nuwa`, a
   machine-specific user-home path, or private credential material.
4. Confirm the local directory and `origin` use `agent-nuwa`.
5. Confirm GitHub reports the public repository as
   `zzzhouzhenzz/agent-nuwa`, with `main` at the pushed local commit.
6. Confirm the old GitHub URL redirects to the renamed repository rather than
   exposing a separate repository.
