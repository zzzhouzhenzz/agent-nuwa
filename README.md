# NÜWA

NÜWA is a Codex custom agent that creates one purpose-built, expert-guided
agent for one bounded job. It chooses the professional discipline that best
fits the job, converts that discipline into concrete working rules, and
registers one focused agent through Codex's native agent interface.

## Requirements

- A current Codex release with custom-agent support

## Install

Clone this repository, then copy the agent definition into your Codex home:

```sh
git clone https://github.com/zzzhouzhenzz/agent-nuwa.git
cd agent-nuwa
mkdir -p "${CODEX_HOME:-$HOME/.codex}/agents"
cp agents/nuwa.toml "${CODEX_HOME:-$HOME/.codex}/agents/nuwa.toml"
```

Restart Codex or begin a new task so it reloads custom-agent configuration.

## Use

Give NÜWA exactly one job:

```text
Use the custom agent nuwa to create a coding agent for this one job:

Add bounded retries to the upload client and verify timeout behavior.
```

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
