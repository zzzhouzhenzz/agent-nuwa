# NÜWA Persistent Agent Factory Design

## Purpose

NÜWA is a factory for reusable Codex custom agents. One invocation creates and
registers exactly one persistent agent, then stops. NÜWA never starts the new
agent, performs its work, supervises it, or waits for it.

The input is one agent-creation request, not one downstream job. NÜWA derives a
durable professional charter for the new agent and may carry relevant project or
task context into that charter as seed context. The resulting agent can accept
future jobs within its charter from new Codex sessions.

## Chosen Approach

Use direct global registration. NÜWA creates the agent definition and any
agent-private skills under `~/.codex/agents/`, adds a narrowly scoped role entry
to `~/.codex/config.toml`, validates the resulting Codex configuration, reports
the result, and stops.

This keeps NÜWA config-only and avoids a separate scaffolding CLI. Draft-only
generation was rejected because it would make NÜWA a template generator rather
than a factory. Spawn-then-promote was rejected because spawning is task-scoped,
creates lifecycle ambiguity, and is unnecessary for persistent registration.

## Persistent Artifacts

For an internal agent ID `<agent-id>`, NÜWA creates:

- `~/.codex/agents/<agent-id>.toml`: the reusable agent configuration layer;
- `~/.codex/agents/<agent-id>/skills/<skill-name>/`: private persistent skill
  content when the request includes a skill; and
- `[agents.<agent-id>]` in `~/.codex/config.toml`: the global role registration,
  including its description, config file, and persona nickname candidate.

NÜWA does not install requested skills into the global shared skill catalog.
Each created agent enables only its own private skill paths through its config
layer.

## Naming

The unique machine-facing ID and the human-facing persona name are separate:

- The first Linus agent uses ID `linus`.
- Later Linus agents use `linus_v2`, `linus_v3`, and so on.
- The created agent's persona remains `Linus Torvalds` in its instructions.
- Its sole nickname candidate is the persona's familiar name, `Linus`.

NÜWA determines the next suffix by inspecting both registered agent IDs and
existing agent artifacts. It never overwrites an existing reusable agent.
Versioning the ID must not add a version suffix to the persona or nickname.

## Creation Flow

1. Confirm the request asks for exactly one reusable agent.
2. Extract the desired professional scope, future job boundary, relevant
   context, authorized capabilities, expected outputs, and verification duties.
3. Select the real-world expert whose demonstrated professional discipline best
   matches the main judgment bottleneck. Coding, debugging, refactoring,
   testing, and code review use Linus Torvalds.
4. Convert the expert's relevant standards into two to four concrete operating
   principles without impersonation or invented opinions.
5. Derive the unique agent ID while keeping the persona and nickname unchanged.
6. Vet every requested external skill before persisting it. Copy approved skill
   content into the new agent's private skill directory and bind that exact path
   in the agent configuration.
7. Write the agent configuration with a reusable charter, persona, principles,
   durable scope, supplied project context, tools and permissions boundaries,
   output expectations, verification requirements, and escalation rules.
8. Add only the new `[agents.<agent-id>]` registration to the global config.
   Preserve all existing settings and upstream defaults.
9. Validate the agent TOML and the complete Codex configuration. Confirm that
   the new role resolves to the expected config file and nickname candidate.
10. Report the agent ID, persona, nickname, config path, private skills, carried
    context, validation result, and the identifier to use from a new session.
11. Stop without invoking the new agent.

## Failure Handling

Creation is transactional from the user's perspective. NÜWA prepares new
artifacts before registration. If skill vetting, file creation, registration, or
validation fails, it removes only artifacts created by the failed attempt and
restores the prior config content. Existing agents and unrelated configuration
must remain unchanged.

Writing under `~/.codex/` may require an explicit sandbox approval. NÜWA asks
for that approval as part of creation; it does not redirect output to a temporary
task-scoped agent or claim success without persistent installation.

## Explicit Non-Goals

NÜWA does not:

- call `spawn_agent` or any equivalent task-scoped creation interface;
- execute or test the downstream professional work;
- monitor, wait for, message, close, or supervise the created agent;
- synthesize results from agents or create teams;
- install requested skills into the global shared skill catalog; or
- overwrite an existing agent when an ID collision occurs.

## Acceptance Criteria

- One invocation creates exactly one globally reusable custom agent.
- The agent is available to new Codex sessions through a unique role ID.
- Repeated personas produce IDs such as `linus`, `linus_v2`, and `linus_v3`.
- Every version retains the persona nickname `Linus`, not `Linus v2` or an
  unrelated generated nickname.
- Requested skills persist only inside that agent's private directory and load
  through its configuration.
- Relevant supplied task or thread context appears in the reusable charter.
- Existing Codex configuration and upstream defaults remain unchanged except
  for adding the new agent registration.
- A failed creation leaves no partial registration or private skill directory.
- NÜWA reports the persistent artifacts and validation evidence, then stops
  without invoking the created agent.
