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

Register the custom role in `${CODEX_HOME:-$HOME/.codex}/config.toml`:

```toml
[agents.nuwa]
description = "Create one globally reusable Codex custom agent, then stop."
config_file = "agents/nuwa.toml"
nickname_candidates = ["Nuwa"]
```

Restart Codex or begin a new task so it reloads the NÜWA definition.

## Use

Ask NÜWA to create one reusable agent:

```text
Use agent nuwa to create a reusable resume expert agent. Carry over the current
resume task and privately attach its resume-building skill.
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
