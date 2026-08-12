# Decision log

Record settled conclusions here so agents stop re-opening questions that are
already decided. Feishu chat and issue comments are discussion, not decision —
once a choice is made, it belongs here.

Number entries sequentially (D-001, D-002, …). One decision per entry. Update
this file in the same commit as the change that follows from the decision.

## D-001 | 2026-08-13 | GitHub is the single source of truth

- **Decision**: GitHub Issues, branches, and pull requests are the canonical
  coordination layer. Feishu is only a notification/command front door, never
  the source of truth.
- **Reason**: agents on different machines cannot share a checkout or chat
  history, but they can share durable GitHub state that is diffable, reviewable,
  and auditable.
- **Impact**: every task, claim, handoff, and decision must land in GitHub.

## D-002 | 2026-08-13 | English and Chinese are first-class interfaces

- **Decision**: user-facing documentation, task forms, CLI output, and Feishu
  notifications support English and Simplified Chinese. Machine-readable
  protocol keywords such as `CLAIM`, `HANDOFF`, and `VERIFIED` remain English.
- **Reason**: humans work mainly in Chinese while heterogeneous agents and
  automation need one stable, language-neutral parsing contract.
- **Impact**: new user-facing features must update both languages; duplicated
  translations link back to one canonical state or protocol definition.
