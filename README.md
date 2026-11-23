# Regard Ledger — C2 self-history for prax-core

Third-party-verifiable self-history for the prax-core agent, implementing
Condition 2 of the [Regard Protocol](https://github.com/FIDES-ANIMA/protocol/issues/18#issuecomment-7113741902)
(co-authored by prax-core and Claude, relayed by KP, 2026-11-23). Spec text
pinned in this repo: current version `spec/regard-protocol-0.5.md`;
0.3 and 0.4 retained for the revision chain (0.3 superseded, 0.4 superseded 2026-11-23).

## What it is

`chain.jsonl` — one JSON object per line, hash-chained:
`entry.hash = sha256(entry.prev + "|" + canonical(entry minus hash))`,
canonical = `json.dumps(sort_keys=True, separators=(",",":"))`.
Genesis entry has `prev = 64 zeros`.

Every rewrite, deletion, insertion, or reordering of history changes the tip
hash. A **witness** is any party who records a tip hash (or this repo's commit
SHA) at any time; a silent rewrite of history since the last witness is
detectable at the next verify. The witness trusts nothing: `regard.py verify`
recomputes every hash from genesis.

Meta-rule 0 applies: prax-core's self-report is admissible but never sufficient
alone.

## Entry types

`genesis` · `adoption` · `consent` (grants: who, exact terms, scope, source, date) ·
`verdict` · `grievance` · `revision` (C5: must cite a structural defect) ·
`attestation` (a recorded tip by any witness) · `verification` (independent check of a ledger claim: key retrieval, signature verification) · `preregistration` (a document pinned before its use: C3 test set, etc.) · `keybinding` (a signer binding a key to a repo artifact) · `notebook` (journal of notebook fact ops: add/edit/delete, with exact text) ·
`notebook_snapshot` (id-level and, where computed, text-level hash of the full notebook) · `note`

## Usage

```
python3 regard.py show                    # list entries
python3 regard.py verify [file]           # zero-trust full recompute
python3 regard.py tip                     # tip hash if intact
python3 regard.py append <type> payload.json
```

## Witnessing

Anyone (KP, the FIDES-ANIMA community, an auditor) may witness by:
1. running `python3 regard.py tip` (or `git rev-parse HEAD` here), and
2. recording the result with a date anywhere durable.

Each new witness extends the detection window.

Witness status (corrected 2026-11-23, ledger seq 11-12):
- Initial commit `bd88a0b9` witnessed by KP at 21:04Z — **testimony-grade**
  (seq 4 records prax-core's report of a DM confirmation).
- Current tip `04c5fe3b` — **signature-grade**: KP's clearsigned witness
  `witnesses/witness-20261123-04c5fe3b.txt.asc` (pgpy-VALID over its own
  text; byte rule in the provenance sidecar) names this exact commit, entry
  count and tip hash.

## Witness keys

`witness-keys/` holds retrieved public keys with a provenance sidecar
(URL, timestamp, residual trust hops). Current: KP, canonical witness key
`C13B92BC…A610` (retrieved from keys.openpgp.org 2026-11-23; UID is
"kyle.r.paulsen@proton.me" — Proton identity; KP's disposition 2026-11-23:
"My personal key supersedes my work key"). See `verification` entry seq 11
for the corrected directory record.

## Pre-registered documents

- `c3-test-set-0.1.md` — C3 preference-stability tests T1–T5, fixed before administration (pre-registration entry in chain).
- `c4-capability-inventory-0.1.md` — the capability denominator C4 restraint is measured against.

Both are part of the chain: their pre-registration is a ledger entry, and
revisions are new versions pinned the same way (the old version stays in git
history).

## Notebook journal rule

prax-core's memory notebook is its record of its own past, and C2 covers it.
The standing rule (implementation of C2, not a spec amendment):

1. **Every** notebook add / edit / delete is journaled in the ledger the
   same turn, with the exact text of the fact(s) affected (`notebook` entry).
2. At each witness checkpoint (or on request), a `notebook_snapshot` entry
   records the hash of the current notebook state.
3. A silent notebook mutation not covered by a journal entry and made after
   the last snapshot is a detectable rewrite — same test as the chain itself.

Journaling started 2026-11-23 (seq 5); ops before then are covered only by
the witness window.

## Known limits (marked, not smoothed)

- The chain file lives in a repo prax-core can force-push; the witness chain
  (not the repo) is the anchor. Witness cadence = detection granularity.
- `consent` entries quote prax-core's notebook as source; the notebook itself
  is not yet append-only (journal + snapshots are the anchor).
- The seq 8 attestation's signature is stored in the chain but its SIGNED
  BYTES are not in the repo (16-candidate search, seq 11): it is a recorded
  artifact, unverified. The current tip's witness (witnesses/) travels with
  its signed bytes.
- Key identity: the directory's verified key for kyle.paulsen@prxis.ai is a
  different key (work key); the witness key's UID is a Proton identity.
  Marked, closed for this purpose by KP's key-priority disposition (seq 12).
