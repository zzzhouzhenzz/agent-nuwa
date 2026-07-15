# NÜWA

NÜWA is a Codex custom agent that creates one purpose-built, expert-guided
agent for one bounded job. It selects the professional discipline that best fits
the job, turns that discipline into concrete working rules, and registers one
focused agent through Codex's native agent interface.

## Requirements

- A current Codex release with custom-agent support
- Python 3.10 or newer for the installer

The package has no runtime dependencies.

## Install

Install directly from the public repository, then place the agent in your Codex
home:

```sh
python3 -m pip install "git+https://github.com/zzzhouzhenzz/project-nuwa.git"
python3 -m project_nuwa install
```

The installer writes only `agents/nuwa.toml` beneath the resolved Codex home.
Resolution order is:

1. `--codex-home PATH`
2. the `CODEX_HOME` environment variable
3. `.codex` beneath the current user's home directory

If a different `nuwa.toml` already exists, installation stops without changing
it. Review your local file, then use `--force` only when replacement is intended:

```sh
python3 -m project_nuwa install --force
```

Check the installed file at any time:

```sh
python3 -m project_nuwa check
```

After installation, restart Codex or begin a new task so it reloads custom-agent
configuration.

## Use

Give NÜWA exactly one job:

```text
Use the custom agent nuwa to create a coding agent for this one job:

Add bounded retries to the upload client and verify timeout behavior.
```

NÜWA creates the agent; it does not run or supervise the resulting job. Coding,
debugging, refactoring, and code-review jobs use Linus Torvalds' relevant
engineering standards without impersonation.

## Local development

```sh
python3 -m unittest discover -v
python3 -m pip wheel . --no-deps
```

For an editable local install:

```sh
python3 -m pip install -e .
python3 -m project_nuwa install --codex-home /path/to/a/test-codex-home
```

## Remove

Remove `agents/nuwa.toml` from the same Codex home selected during installation.
The Python package can then be removed with:

```sh
python3 -m pip uninstall project-nuwa
```

## License

MIT. See [LICENSE](LICENSE).
