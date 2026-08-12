# Reference projects and extracted patterns

The hub deliberately borrows patterns, not dependencies.

## agent-orchestration

<https://github.com/madebyaris/agent-orchestration>

Useful ideas: shared task queue, agent discovery, resource locks, structured
handoffs, and compatibility through `AGENTS.md`. It is the closest conceptual
match, but its MCP server is more infrastructure than this four-agent setup
needs initially.

## OpenHands Software Agent SDK

<https://github.com/OpenHands/software-agent-sdk>

Useful ideas: explicit workspaces, task tracking tools, local versus ephemeral
execution, and GitHub workflows. It is a good future option if agents need to be
launched programmatically instead of through their existing native clients.

## CrewAI

<https://github.com/crewAIInc/crewAI>

Useful ideas: role-based agents and separating autonomous “crews” from
deterministic event-driven “flows”. For this repository, deterministic state and
human review matter more than autonomous group chat.

## AutoGen

<https://github.com/microsoft/autogen>

Useful ideas: agents exposed as tools and layered orchestration. AutoGen itself
is now in maintenance mode, so it is a reference rather than a foundation for a
new implementation.

## Practical conclusion

For agents already running in different clients and on different computers,
the reliable shared primitives are GitHub Issues, isolated Git branches,
pull-request review, capability routing, and durable evidence. A common model
runtime can be added later without changing this protocol.
