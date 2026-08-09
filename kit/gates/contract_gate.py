#!/usr/bin/env python3
"""contract_gate — kit-core Layer-0 check: a composite project's contract
declares a version.

Provenance: authored by FOUNDATIONS (brief foundations-001, proposal filed
2026-08-09), consumer-authored and resident-landed per INTEGRATIONS §3. Running
in FOUNDATIONS' own `./verify` since 2026-08-08 and negative-tested there before
being offered. Landed here by autonomous as Decision 43.

WHY IT EXISTS: Decision 39 rules that a composite project's contract file may be
a versioned WRAPPER over a normative source it does not contain — the invariant
being that exactly one file owns the version and the freeze state. That is prose.
This is the half of it a build can enforce.

WHY A MISSING VERSION IS NOT COSMETIC: an unversioned contract cannot produce a
contract-version EVENT, and without those events consumers have nothing to pin
(INTEGRATIONS rule 4). The absence silently removes the entire basis on which
every downstream consumer decides whether it must act.

DELIBERATELY NARROW. It answers exactly one question: does the file the manifest
names as the contract declare a version? It does NOT check semver ordering, or
whether the version was bumped when it should have been, or read the contract's
prose. Those need history or judgement; Decision 39's second half — *was the
freeze respected?* — is a human ruling and stays one.
"""

import json
import os
import re


def contract_gate(root=".", manifest_name="project.manifest.json"):
    """Return (ok: bool, message: str). Composite projects only; inert elsewhere.

    Reads the contract path FROM the manifest rather than hardcoding it, so the
    gate follows a project that renames or relocates its contract.
    """
    manifest_path = os.path.join(root, manifest_name)
    try:
        with open(manifest_path, encoding="utf-8") as f:
            mf = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return True, "skip  contract: no readable manifest"

    contract = (mf.get("composite") or {}).get("contract")
    if not contract:
        return True, "skip  contract: not a composite project"

    path = os.path.join(root, contract)
    if not os.path.exists(path):
        return False, (f"contract: manifest names '{contract}' as the contract, "
                       f"but that file does not exist")

    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            txt = f.read()
    except OSError as exc:
        return False, f"contract: cannot read {contract} ({exc})"

    m = re.search(r"^contract-version:\s*(\S+)", txt, re.M)
    if not m:
        return False, (f"contract: {contract} declares no `contract-version:` line — "
                       f"consumers have nothing to pin (INTEGRATIONS rule 4)")
    return True, f"ok    contract: version {m.group(1)}"


if __name__ == "__main__":
    import sys
    ok, msg = contract_gate(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(msg)
    sys.exit(0 if ok else 1)
