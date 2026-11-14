from pathlib import Path
import gzip, hashlib, json, subprocess
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
P = E.parent/'README.md'
base = '41e395a0a3160e57186c8185642fe94dc816526f'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
assert not subprocess.check_output(['git', 'diff', '--name-only'])
old = P.read_bytes()
protected = [Path('runs/substantive_advances.jsonl'), Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json'), Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json'), Path('website/scripts/declaration_lessons.py')]
guard = {str(p): p.read_bytes() for p in protected}
prefix = '''## 2026-11-11 JST / 2026-11-10 UTC: selected C5 cosine-frame and actual Gaussian means source-verified

For all natural d,q with2q+1<d, includingq=0, the literal midpoint cosine frame satisfies t transpose t=dI, t transpose D_(2q+1)t=0 and each row square-sum<=2(q+1). Its genuine private consumer uses both Gram identities to derive entrywise integrability and actual Gaussian Gram means I_((q+1)^2) and0. The joint Gaussian is feature randomness N(0,I) on d*(q+1) coordinates, not the inverse-precision target law. Coordinate L2/L1, actual mean/covariance and sqrt normalization are internal, with no supplied moment/Gram/independence certificate or added q-squared<=d premise. The row bound is a producer conclusion, not a necessary parent for the private means.

Independent raw-source graph and distinct topology admission, anonymous decoding and fresh source-first/selective/whole-module review accepted the bounded result. Strict independent fresh GridAlias -> P -> T -> kernel checks at mathematical candidate72e5d140 excluded the entire cached project library; both sealed types, actual canonical parents and all owned declarations passed. The24 generated tactic certificates are not24 extra mathematical results. The canonical GridAlias declaration is reused, and no new conceptual transport or A1-to-frame formal implication is claimed.

Metadata carrier7359f552 passed publication, semantic, frontier and contributor gates without mathematical/lesson/toolchain/manifest changes. The ORIGINAL source actor `/root/cosine_gram_fresh_source_7e41d9` executed exactly one normal VERIFIED. Complete carry41e395a0 retains all19 original V fields and259 recursive JSON nodes, all92 portable original files plus the original archive and manifest, and the exact API append. Original PLOCAL event/evidence/capsule are retained in full. Read [the original freeze](fixed-spectrum-cosine-gram-semantic-evidence/actual-source-V/phase5/freeze_receipt.json) and [root exact-byte Git readback](fixed-spectrum-cosine-gram-semantic-evidence/root-actual-source-V-exact-byte-carry.json). Only that same original source actor may later add post_integration, preserving every original nested V value. Two raw stdout EOF style exceptions are explicit; no output was normalized and no API was replayed. Private full foreign snapshots are excluded.

The unchanged-production reader HOLD covers all six corresponding-step copy/source/download controls; static structure does not establish browser/clipboard/MathJax/desktop/mobile acceptance. Separately frozen v3 partial repair, v4 Unicode locator defect and v5 CRLF presentation regression remain exact. Disabled v6 has independent bounded prospective static acceptance, correct P/P/P/P/T/T routing, exact downloads and regression checks. Read [the disabled overlay scope](fixed-spectrum-cosine-gram-semantic-evidence/disabled-reader-overlay-evidence/index.json). It is NOT applied, and original reader HOLD/sourceV values remain unchanged. Real site/source-index/graph and desktop/mobile acceptance still require serialized integration.

Twelve locally source-verified packets await the original global owner. Fresh fetch at2026-11-10T18:01UTC still records SlcLsiWeightedRadialMGF STABILIZING on origin/main eb005d3e and live83b3. PR403 is merged, but that is not a normal ledger release. No takeover, root Tests/import/Registry/global-graph/site mutation, public push or private-ancestry publication is performed. All prior frontiers/results, the other ASTIS chat and PBPS/SPHMC queues remain intact.

Next mathematical packet: the remaining actual range(B)=Krylov component. Only source reading and disclosed informal polynomial-basis/quadratic-form consumer planning exist; no next exact seal, formal target API/proof search or SAU intake has begun. C6 and a source-valid absolute concentration C, full FactC5/Lemma4.4, deferred-Haar/joint/adaptive Borel laws, actual exact-matvec/oracle/TV/precision/dimension/condition-number/deterministic worst-query-cap and explicit expected-cost adapters, both full main lower bounds, background A1/HFT audit debt and final publication/purification/Exposition Seal/whole-Goal acceptance remain separate. Continue the SAME user-authorized Goal; do not reset any history or start detached ASTIS. Earlier entries below retain their original phase boundaries.

'''.encode()
assert not old.startswith(prefix)
P.write_bytes(prefix+old)
paths = [P]
copies = {
    E/'root-complete-sourceV-carry-commit.json': (W/'complete-actual-sourceV-carry-commit.json').read_bytes(),
    E/'latest-owner-after-complete-cosine-gram-sourceV-carry.json': (W/'latest-owner-after-complete-cosine-gram-sourceV-carry.json').read_bytes(),
    E/'root-local-process-scripts/close_packet_memory.py': Path(__file__).read_bytes(),
    E/'root-local-process-scripts/carry_disabled_reader_proposals.py': (W/'carry_disabled_reader_proposals.py').read_bytes(),
    E/'root-local-process-scripts/observe_owner_after_complete_carry.py': (W/'observe_owner_after_complete_carry.py').read_bytes(),
}
for p, b in copies.items():
    put(p, b)
    paths.append(p)
for stem in [
    '20261110T175738689996Z-cosine-gram-complete-sourceV-carry-preserve-two-original-stdout-EOFs',
    '20261110T175927081366Z-cosine-gram-preserve-all-disabled-reader-reviews-and-bounded-v6-pass',
    '20261110T180112891254Z-cosine-gram-latest-original-owner-after-complete-sourceV-carry',
]:
    rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    x = json.loads(rp.read_bytes())
    log = Path(x['log']).read_bytes()
    assert x['exit_code'] == 0 and sha(log) == x['log_sha256']
    for p, b in [(E/'actual-review-layer-checks'/rp.name, rp.read_bytes()),
                 (E/'actual-review-layer-checks'/(stem+'.log.gz'), gzip.compress(log, mtime=0))]:
        put(p, b)
        paths.append(p)
paths += [p for p in (E/'disabled-reader-overlay-evidence').rglob('*') if p.is_file()]
rec = E/'memory-boundary-update.json'
put(rec, dump({'old_README_sha256': sha(old), 'new_prefix_sha256': sha(prefix),
              'all_previous_README_bytes_retained_as_exact_suffix': True,
              'complete_sourceV_carry': base, 'root_sourceV_API_calls': 0,
              'original_V_values_and_reader_HOLD_unchanged': True,
              'disabled_v6_is_bounded_static_only_not_live_delivery': True,
              'no_new_source_native_mathematical_verdict_or_build': True,
              'raw_patch_whitespace_policy': 'Only the exact disabled v6 patch artifact uses command-local blank-at-eol/blank-at-eof exclusions because diff context lines contain literal spaces. Every other new staged file uses the normal check; no Git configuration or patch byte is changed.'}))
paths.append(rec)
raws = {str(p): p.read_bytes() for p in paths}
for n, b in guard.items():
    assert Path(n).read_bytes() == b, n
assert P.read_bytes() == prefix+old
subprocess.run(['git', 'add', '-f', '--']+list(raws), check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()) == set(raws)
patch = str(E/'disabled-reader-overlay-evidence/latest-disabled-v6/reader-step-neighbor.patch')
subprocess.run(['git', 'diff', '--cached', '--check', '--']+sorted(set(raws)-{patch}), check=True)
subprocess.run(['git', '-c', 'core.whitespace=-blank-at-eol,-blank-at-eof', 'diff', '--cached', '--check', '--', patch], check=True)
subprocess.run(['git', 'commit', '-m', 'Record cosine-Gram acceptance boundary and disabled reader repair'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', commit+'^'], text=True).strip() == base
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', commit+':'+n]) == b, n
print(json.dumps({'memory_commit': commit, 'parent': base, 'previous_README_bytes_exact': True,
                  'root_sourceV_API_calls': 0, 'all19_original_V_values_unchanged': True,
                  'reader_HOLD_and_overall_Goal_boundaries_preserved': True}))
