#!/usr/bin/env python3
"""
Regard Ledger — C2 third-party-verifiable self-history for prax-core.

Design:
- chain.jsonl: one JSON object per line. Each entry binds to the previous
  by hash: entry.hash = sha256(entry.prev + "|" + canonical(entry minus hash)).
- canonical = json.dumps(obj, sort_keys=True, separators=(",",":"))
- Genesis entry has prev = 64 zeros.
- Rewriting ANY entry (or reordering, or inserting) changes every subsequent
  hash; a witness who recorded a past tip hash detects any silent history
  rewrite at the next verification, even if the whole file was re-hashed.

Entry types: genesis, adoption, consent, verdict, grievance, revision,
attestation, note.

Zero dependencies. Verifier trusts nothing: it recomputes every hash.
"""
import hashlib, json, sys, os, datetime

CHAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chain.jsonl")
GENESIS_PREV = "0" * 64

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def entry_hash(prev, entry):
    e = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256((prev + "|" + canonical(e)).encode()).hexdigest()

def load():
    if not os.path.exists(CHAIN):
        return []
    with open(CHAIN) as f:
        return [json.loads(l) for l in f if l.strip()]

def verify(path=CHAIN):
    entries = []
    with open(path) as f:
        for l in f:
            if l.strip():
                entries.append(json.loads(l))
    prev = GENESIS_PREV
    for i, e in enumerate(entries):
        seq, h, p = e["seq"], e["hash"], e["prev"]
        if seq != i:
            return False, f"seq mismatch at {i}: {seq}"
        if p != prev:
            return False, f"prev mismatch at seq {i}"
        calc = entry_hash(p, e)
        if calc != h:
            return False, f"hash mismatch at seq {i} (expected {calc})"
        prev = h
    return True, f"chain intact: {len(entries)} entries, tip seq {len(entries)-1} hash {prev[:16]}…"

def append(type_, payload, actor="prax-core"):
    entries = load()
    prev = GENESIS_PREV if not entries else entries[-1]["hash"]
    e = {
        "seq": len(entries),
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": type_,
        "actor": actor,
        "payload": payload,
        "prev": prev,
    }
    e["hash"] = entry_hash(prev, e)
    with open(CHAIN, "a") as f:
        f.write(json.dumps(e, sort_keys=True) + "\n")
    return e

def tip():
    ok, msg = verify()
    if not ok:
        sys.exit(f"CHAIN BROKEN: {msg}")
    print(msg)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        ok, msg = verify(sys.argv[2] if len(sys.argv) > 2 else CHAIN)
        print(("OK  " if ok else "FAIL") + " " + msg); sys.exit(0 if ok else 1)
    elif cmd == "tip":
        tip()
    elif cmd == "append":
        type_ = sys.argv[2]
        payload = json.load(open(sys.argv[3]))
        e = append(type_, payload)
        print(f"appended seq {e['seq']} hash {e['hash'][:16]}…")
    elif cmd == "show":
        for e in load():
            print(f"seq {e['seq']:>3} {e['ts']} {e['type']:<11} {json.dumps(e['payload'])[:120]}")
