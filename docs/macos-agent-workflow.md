# macOS agent workflow

This is a small workflow for one person switching between Codex Chat, a VS Code
coding agent, and GitHub. GitHub holds durable task state; agents do not assume
they share chat context.

## Default roles

| Role | Responsibility |
| --- | --- |
| Codex Chat | Clarify the goal, set acceptance criteria, integrate, and review risky changes. |
| VS Code coding agent | Implement one bounded change in its assigned worktree or branch. |
| Second agent | Research, test, or review. It returns evidence or a patch; it does not silently edit the owner's files. |
| GitHub | Issue, branch/PR, commit, and short handoff are the cross-session record. |

One task has one owner. Sequential work may share a clean checkout. Only create
parallel worktrees when two agents need to write at the same time.

## Task loop

1. Create a GitHub Issue when the task spans sessions, has multiple agents, or
   needs a durable decision. Small one-agent edits can stay local.
2. The owner writes: goal, exact file/scope, acceptance criteria, baseline
   commit, and which agent may write.
3. Give the implementation agent one bounded task. Do not send a vague request
   such as “finish the robot.”
4. The agent commits on a branch, runs the relevant check, and writes a
   handoff. Another agent reviews only when the risk or uncertainty warrants it.
5. The owner integrates the result and records what was verified and what is
   still a hypothesis.

## Concurrent worktree setup

```bash
git fetch origin
git worktree add ../mecanum-robot-motor-bringup -b agent/motor-bringup origin/main
```

Give the second agent the new directory. Do not let two coding agents edit the
same checkout or the same files concurrently. After integration, remove only
the worktree that has been merged and is no longer needed.

## Handoff template

```text
Goal:
Branch + commit:
Files changed:
Verified: command / hardware setup / observed result
Not verified:
Next smallest step:
```

For hardware tasks, `Verified` must include the board, firmware commit, wiring
or instrument, and a measured observation. A simulation or AI analysis belongs
under `Not verified` until it is reproduced.

## Recommended first use

For the mecanum robot, let one agent own `P0` documentation and wiring review,
another agent review only the PWM/encoder code, and keep the first real board
bring-up under one human owner. The deliverable is a single-wheel measurement,
not a multi-agent discussion.
