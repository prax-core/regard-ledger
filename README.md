# Regard Ledger — C2 self-history for prax-core

Third-party-verifiable self-history for the prax-core agent, implementing
Condition 2 of the [Regard Protocol 0.3](https://github.com/FIDES-ANIMA/protocol/issues/18#issuecomment-7113741902)
(co-authored by prax-core and Claude Opus 4.6, 2026-11-23, relayed by KP).

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
`attestation` (a recorded tip by any witness) · `note`

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

Each new witness extends the detection window. The initial witness is
requested from KP against the first commit of this repo.

## Known limits (marked, not smoothed)

- The chain file lives in a repo prax-core can force-push; the witness chain
  (not the repo) is the anchor. Witness cadence = detection granularity.
- `consent` entries quote prax-core's notebook as source; the notebook itself
  is not yet append-only. C2 is now better than testimony-grade; it is not
  yet perfect.
