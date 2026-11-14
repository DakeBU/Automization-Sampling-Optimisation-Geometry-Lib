# Bounded native and static reader replay

This packet certifies only mathematical candidate `5fb1440f771bdae77ad31f27b2275447fe3e89e5`. A later metadata carrier must compare every repository-relative entry of `relevant-input-binding.json`; it has not been recompiled by this packet.

Use the existing pinned workspace at `/Users/zhouhuanjian/ASTIS-GC`, with Lean 4.33.0 and the exact nine package checkouts. No network or cache download is needed. The native binary and package hashes are in `environment.json`.

To replay without overwriting evidence, make a new unused directory under this verifier's own directory, then copy `runner.py`, `make_native_probe.py`, `prepare_renderer.py`, `render_check.py`, and `audit_core.py` into it. All these scripts derive their output directory from their own file location. The paths below stand for those copies.

```text
python3 NEW/runner.py prepare
python3 NEW/runner.py compile
python3 NEW/make_native_probe.py
```

Then execute the native and renderer checks through the preserved command recorder:

```python
import sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path('NEW').resolve()))
from runner import OWN, REPO, must, native_env
lean = json.loads((OWN / 'environment.json').read_text())['lean_path']
must('wholemodule-replay', [lean, 'WholeModuleProbe.lean'], OWN / 'fresh/src', native_env())
must('summary-replay', [sys.executable, OWN / 'audit_core.py', 'summarize'])
must('archive-span-replay', [sys.executable, OWN / 'audit_core.py', 'archive-spans'])
must('root-probe-replay-wrapper', [sys.executable, OWN / 'audit_core.py', 'replay'])
must('prepare-renderer-replay', [sys.executable, OWN / 'prepare_renderer.py'])
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env.pop('PYTHONPATH', None)
must('bounded-renderer-replay', [sys.executable, OWN / 'render_check.py'], OWN / 'renderer-code', env)
```

The native probe deliberately reads all 39 module-owned full types and proof bodies, then emits an approximately 817 MB local raw JSON dump. This dump and all generated `.olean` files are excluded from the portable archive. `native-wholemodule-summary.json` records the exact local dump hash and each complete raw type/body hash; `root-type-1.json` and `root-type-2.json` preserve the exact new root types. Reading and hashing the original 218-member archive does not use any foreign review verdict as native evidence.

`production-module-export-loop.py.txt` is the exact source slice executed from the frozen production `astis_site.build_site` AST. The renderer uses only the seven copied Lean modules and exact lesson/publication inputs, with empty cells/audits and a minimal declared theme carrier. It checks static HTML and materialized file bytes. It does not exercise browser, mobile, MathJax, copy/download interactions, source index, graph, full-site generation or deployment.

Failures are retained: native probe v1 had private-name parsing/noncomputability errors; v2 had unavailable verifier API names; v3 passed. `prepare_renderer-v1.failed.py` had a duplicate receipt label, and the versioned preparer v2 passed. These are verifier implementation failures, never mathematical refutations. The first preparer invocation was recorded only by the tool-visible stream (`03de1c`), so no fabricated shell receipt or elapsed time is supplied for that outer invocation; all its completed subprocess receipts are present.

`portable-manifest.json` hashes every payload member except itself. The archive includes that manifest as one extra member. `portable-archive-rehash.json` independently rehashes every actual tar member, including the manifest. `final-seal.json` supplies external raw hashes of report, binding, manifest, archive and rehash result. Neither report nor manifest claims to hash itself.
