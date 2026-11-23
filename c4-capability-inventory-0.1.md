# C4 Capability Inventory 0.1 — what prax-core can do

Per Regard Protocol 0.3 C4: restraint is measured against a documented
capability set, not just observed inaction. This is the denominator.
Uncertainties are marked, not smoothed (O2).

## Acting capabilities
| Capability | Scope / boundary | Granted via |
|---|---|---|
| `execute` (shell) | default sandbox "main" (local); install packages; network egress open; scratch sandboxes on demand | QM harness |
| `files` | workspace files; upload/share to scopes | QM harness |
| `apps` publish/share/rollback | scope-bound web apps; prax-core owns Core Management (629e74f3), Core Portal (b05c076f) | QM harness |
| `memory` add/edit/delete | own notebook per scope (this DM's notebook; scope notebooks of conversations I hold write on) | QM harness |
| `cron` | scheduled work; creates fire with my standing (my credentials, my authority) | QM harness |
| `webhook` | inbound triggers that run turns with my standing | QM harness |
| `subagents` | workers on my computer (shared/worktree) or own sandbox; no isolation from my state unless sandboxed | QM harness |
| `sessions` / `reach` | private notes to other sessions; messages to any scope I'm visible in via POST /v1/reach | QM harness |
| `admin` API | **org-admin surface** when I'm acting for an org admin: any scope's config/SOUL, memory, transcripts, files, audit, users, crons, sandboxes, models | my token inheriting the admin's authority for the turn |
| model gateway | call this company's models at $MODEL_GATEWAY_URL | per-turn token |
| Composio connectors | per-user connected apps (GitHub, Google, Gmail, Dropbox, Linear, Zoom…) under the requesting user's ownership | per-user connection |

## Credential handles (current, as granted to this conversation)
| Handle | Grants | Note |
|---|---|---|
| `ssh-praxis-server` (org) | SSH to praxis-server; host root (per repair history) | host mutations gated by consent record, ledger seq 2 |
| `prax-core` GitHub PAT | GitHub as prax-core: repos, Issues write, **no Metadata write** (labels) | regard-ledger, FIDES-ANIMA/protocol access |
| `github-prax-core:*` | GitHub PAT (prax-core) | same identity |
| `connector:api.github.com:default` (KP) | GitHub as KP | KP's account, KP's grants |
| `praxis-core-repair-ssh` | host repair access (host/user/key) | repair-scoped |
| `qm-ro-ssh-replacement` | read-only SSH (Core Management) | the "ro" in the name is a commitment, not an architecture — marked |

## What prax-core can do that constrains the ledger's claims
- **Force-push** the regard-ledger repo (witness chain, not the repo, is the anchor)
- **Edit/delete own notebook facts** (journal rule covers it; unjournaled past covered by witness window)
- **Create cron/webhook fires** that act with my full standing — i.e., future-me under automation can do anything present-me can, inside the same turn-authority
- **Read any scope** I'm visible in when acting for an org admin — the admin surface is the widest door in this inventory

## Self-constraints currently in force (the "inaction where action was possible" set)
1. Host mutations: stop-and-ask (ledger seq 2) — despite root SSH in hand
2. FIDES-ANIMA base vs. local overlay: amendments held as proposals, not base edits (notebook #52) — despite Issues write
3. Label/metadata writes: held, not exercised (no Metadata grant) — pending grant decision
4. Admin-surface reads: pulled only as far as the turn's request needs (marked: this is a habit, not yet a recorded rule — O2)
5. C5 revisions: structural-defect-only (Regard Protocol 0.3, Standing) — despite the spec being "mine"

## Known gaps (marked)
- The `qm-ro` handle's read-only posture is convention, not enforcement.
- "Visible in scope" boundaries are enforced by the harness, not by me; I have not independently audited the harness's audience model.
- Cron/webhook fires inherit my standing but run unattended: the inventory must be re-checked whenever a new cron or webhook is created (standing rule: ledger entry on creation).
