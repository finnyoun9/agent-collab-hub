# Local archive note — 2026-08-13

Local coordination work was preserved before any clone cleanup:

- `agent-collab-hub-coordinator`: local orchestration update committed as
  `40c0b85` (`feat: add local agent orchestration roles`).
- `agent-collab-hub`: contains an untracked `coordinator/` directory and a
  local branch with one commit not present in its configured upstream.
- `agent-collab-hub-recovery`: contains two commits not present in its
  configured upstream.
- `agent-collab-hub-pr14-review`: detached review checkout.
- `agent-collab-hub-codex` and `agent-collab-hub-workbuddy`: clean tracked
  checkouts at their configured upstreams.

The external archive directory contains Git bundles for every clone, a ZIP of
the untracked coordinator directory, a manifest, and SHA-256 checksums. No clone
was deleted or moved during archival.
