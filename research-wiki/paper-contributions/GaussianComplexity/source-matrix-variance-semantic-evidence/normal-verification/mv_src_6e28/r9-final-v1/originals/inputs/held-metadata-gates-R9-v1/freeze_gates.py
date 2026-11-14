from pathlib import Path
import json,hashlib,datetime,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
# Importing run_gates would rerun checks; it is intentionally never imported here.
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');HELD='02fb93c64e4222f112e57c97ced2a548235cd0f6'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((HERE/'gate-summary.json').read_text());assert s['all_four_actual_zero'] and len(s['gates'])==4
assert s['before']['head']==s['after']['head']==HELD and s['before']['index_sha256']==s['after']['index_sha256']
report='''# Held R9 metadata gates — independent execution

PASS for exactly four real read-only metadata gates, each invoked once on held HEAD02fb93c64e4222f112e57c97ced2a548235cd0f6, using base6819e686116e6f18df3ef0e638c6ca24bde7dd8d where required. Actual command argv/cwd/effective environment/start/end/exit/stdout/stderr hashes and unmodified outputs are in commands/. No build, kernel recheck, browser repetition, global site gate, other acceptance gate, V or normalV was run.

1. python3 tools/astis_publication.py check --base6819e686116e6f18df3ef0e638c6ca24bde7dd8d: exit0, empty stderr. Actual output reports Publication PASS for386 source items, with legacy debt explicit.
2. python3 tools/astis_semantic_roundtrip.py check: exit0, empty stderr. Actual output reports registry valid,468 audits and8 repair proposals. This is schema/link validation, not a new source/decoder judgment.
3. python3 tools/astis_contributor_contract.py check --base6819e686116e6f18df3ef0e638c6ca24bde7dd8d: exit0, empty stderr. Actual output resolves exactly that base/held HEAD, two affected declarations (public uncentered R9 producer and prior shared real PSD-integral S) and two changed cells. Its own output limits the result to affected metadata, keeping publication/semantic/Lean requirements separate. It reports working-tree/untracked inclusion; no no-op scope was substituted.
4. python3 tools/astis_frontier_cells.py check: exit0, empty stderr;466 registered cells.

Each gate was followed by a real git rev-parse HEAD snapshot and direct index byte hash. Before, after each gate, and final HEAD all equal the held02fb commit. The exact .git/index is25,039,709 bytes/SHA2562f9f667a54d7dcfd9337a26e9c1d3d4c2c398965ca32cb88719b0d9c90f8f978 throughout. GIT_OPTIONAL_LOCKS=0 prevented optional refresh writes. The runner wrote only its new owned evidence directory and performed no C/ledger/audit/index/shared tracked-file mutation or state transition. Stable index is not presented as proof of every possible external concurrent worktree property.

The mathematical compile boundary remains e654e98642350a615c473bc8190fbc1d47fe52bd; no recompilation of02fb is claimed. Reader authors remain1d0dedf3aac3c2ff72ee96566461e29e38a2eeae. Original native PASS and original bounded reader FAIL are still separately sealed/carried; the later conditional UNAPPLIED production CSS prototype PASS does not replace that FAIL or certify canonical integration/full-site delivery. Existing source review is not rejudged by this native metadata execution. Final V/normalV admissibility remains the separately assigned verifier's decision, not this report's.

All four actual outputs, bootstrap/index-path and HEAD command receipts, direct index snapshots, runner source/version and this report are portable originals. No full proof dump, foreign private/control data or source/decoder verdict was loaded/exported in this metadata task. The outer tool's launch/completion envelope remains in the conversation transcript; inner subprocess records are original dedicated captures, not reconstructed historical logs. No missing capture is represented as an invented receipt.
'''
(HERE/'REPORT.md').write_text(report)
dest='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/native-review/variance_native_61d0/held-metadata-gates-R9-v1/originals/'
rows=[]
for p in sorted(HERE.rglob('*')):
 if not p.is_file() or p.name in {'SEAL.json','portable-manifest.json','postseal-envelope.json'} or '__pycache__' in p.parts:continue
 rel=p.relative_to(HERE).as_posix()
 rows.append({'source':str(p),'destination':dest+rel,'relative_source':rel,'bytes':p.stat().st_size,'sha256':sha(p)})
(HERE/'portable-manifest.json').write_text(json.dumps({'schema':1,'files':rows,'destination_root':dest,'postseal_index':'separate postseal-envelope.json avoids self-hash recursion'},indent=2))
seal={'schema':1,'assessor':'variance_native_61d0','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'outcome':'FOUR_HELD_METADATA_GATES_PASS','held_metadata_HEAD':HELD,'base':s['base'],'actual_math_compiled_commit':s['actual_math_compiled_commit'],'reader_author_commit':s['reader_author_commit'],'gates':[{'label':g['label'],'actual_exit':g['exit'],'HEAD_index_stable':g['HEAD_index_stable']} for g in s['gates']],'index_sha256_before_and_after':s['before']['index_sha256'],'index_bytes':s['before']['index_bytes'],'report_sha256':sha(HERE/'REPORT.md'),'summary_sha256':sha(HERE/'gate-summary.json'),'portable_manifest_sha256':sha(HERE/'portable-manifest.json'),'original_reader_disposition':'FAIL remains explicit; conditional UNAPPLIED prototype PASS is separate','normalV':'not run or decided','new_math_build_browser_or_other_gates':'none'}
(HERE/'SEAL.json').write_text(json.dumps(seal,indent=2));print(json.dumps({'seal_sha256':sha(HERE/'SEAL.json'),'manifest_sha256':sha(HERE/'portable-manifest.json'),'report_sha256':sha(HERE/'REPORT.md'),'files':len(rows),'portable_bytes':sum(x['bytes'] for x in rows)},indent=2))
