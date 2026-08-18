---
id: tmpy71ewyeg-kit-sync-2.4.1
from: tmpy71ewyeg
to: autonomous
status: filed
ball: provider
repo_path: /var/folders/4q/zm0nd5n15glbgtlv51dtmqjm0000gn/T/tmpy71ewyeg
re: kit_sync to 2.4.1 — please verify against the tree
---
kit_sync reports `version-stale` at kit 2.4.1 for `/var/folders/4q/zm0nd5n15glbgtlv51dtmqjm0000gn/T/tmpy71ewyeg`.

`repo_path` above is the directory this run ACTUALLY wrote, resolved at run
time — not the one anyone intended. `.` resolves against the caller's working
directory, so a run launched from elsewhere would sync some other repo and
still report success; autonomous compares this line against its registry and
disputes a mismatch. (Residuum, 2026-08-18: a receipt read `current` while the
named repo had no `.kit/` at all, and nothing in the receipt could show why.)

MANIFEST as written:

```
kit_version: 0.0.1
```

Verify by re-reading, not by trusting this: `kit_sync.py <repo> --check`.
