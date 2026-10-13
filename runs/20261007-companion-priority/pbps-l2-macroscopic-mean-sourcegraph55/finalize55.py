import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-sourcegraph55'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def lf(b):
    b = b.replace(b'\r\n', b'\n')
    assert b'\r' not in b, 'lone CR: LF recipe cannot silently normalize it'
    return b
def encode(d):
    return (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def descriptor(p, b=None):
    if b is None:
        b = p.read_bytes()
    normalized = lf(b)
    return dict(path=str(p), raw_bytes=len(b), lf_bytes=len(normalized),
                raw_sha256=sha(b), lf_sha256=sha(normalized))
def write(name, d):
    (OUT / name).write_bytes(encode(d))

inputs = json.loads((OUT / 'input-bindings.json').read_text(encoding='utf-8-sig'))
for item in inputs:
    current = descriptor(Path(item['path']))
    for k in ['raw_bytes', 'lf_bytes', 'raw_sha256', 'lf_sha256']:
        assert current[k] == item[k], (item['path'], k)
counts = json.loads((OUT / 'counts.json').read_text(encoding='utf-8-sig'))
assert counts == dict(nodes=181, edges=668, providers=146, coverage=590, callers=593,
                     lexemes=2891, unresolved=0, external_deep_boundaries=77,
                     coverage_NODE=466, coverage_EXCLUDED=124)
graph = json.loads((OUT / 'source-proof-graph.json').read_text(encoding='utf-8-sig'))
assert graph['topology_admitted'] is False
assert graph['compiled_graph_created'] is False
assert graph['candidate_LF_sha256'] == '0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
assert len(graph['nodes']) == counts['nodes'] and len(graph['edges']) == counts['edges']
lease = json.loads((OUT / 'lease.json').read_text(encoding='utf-8-sig'))
assert all(lease[k] == 'OPEN' for k in ['read', 'write', 'python'])
assert lease['compiler'] == 'NOT_STARTED_CLOSED'

capsule = '''The bounded source-only graph55 is complete and ready for distinct independent topology review. It is not a compiled theorem or a creator admission.

The exact root-adopted statement remains 2526 LF bytes, SHA256 0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f. Primary reconstruction and its freeze preceded candidate exposure; the original primary draft, checkpoint, two API corrections, and rejected representation drafts remain immutable. Root's anonymous Prop typecheck/StatementSeal is provenance only, not proof55.

Scope: one SAME-law all-L2 mean bridge, with actual mu/J/nu probability, literal EVERY-y source-density S, Lambda both marginals equal nu, true reflection U, canonical snd pullback M, bounded contraction T, PM=M, MT=AM, AE fiber L1 and square-L1, and actual integrated variance/norm defect. All source alpha/beta/C2/Hessian/eta-cap binders remain. Finite-Hilbert/rank0 and explicit Lp bookkeeping are authored extensions; noncentered constants are permitted. Rough observers have AE-nu fiber integrability and mean agreement; no EVERY-y rough C1 or derivative transfer is asserted.

Five opaque existing producer contracts: MacroscopicEnergy50, GaussianMarginalGradient51 (dense compact input core only), ReflectionL2, GaussianReflection, and GaussianConditionalKernel.exists_tilted_isCondKernel. The last is a necessary genuine internal posterior/disintegration producer even though R is not returned. No caller kernel/operator/coherence/normalizer/desired-bound/closure certificate is added. No54 proof or verdict was read or used.

Chosen source route has seven obligations in source-contract.json: actual law/block producers; canonical M and complete closed range; compact density/continuity giving PM=M and invariant range; bounded inverse-range T and contraction; real posterior/disintegration/AE uniqueness identifying literal mean; actual L2/squared-moment/Fubini variance; exact block norm defect. Ingredient edges are prospective mathematical dependencies, never claimed compiled55 calls.

Active schema bounded-source-proof-graph55/v1: 181 nodes, 668 edges, 146 selected providers, 590 physical rows (466 NODE,124 EXCLUDED), 593 named caller occurrences, 2891 lexical entries, zero unresolved active lexemes, and 77 deep external-boundary records. Selected primary scope has 208 physical rows and 78 formula records within nine balanced units: 351-361,614-648,3551-3579,3582-3596,3602-3635,3705-3735,3762-3786,4573-4587,4653-4665. Formula(C.2) is within C.1, not subsection C.2. B13/fullrough and C1 density/closedness are genuine downstream mathematical boundaries, not layout exclusions.

Provider headers retain let assignments/default-slot syntax and all needed ambient scopes. Global Module, actual condKernel/eLp primitives, generated compact-support carrier, UniformSpace class, and LinearPMap ambient context are explicit. Generated field/declaration names are distinguished from mathematical calls. Physical lines are one-based; inventory rows and UTF8 byte/column half-open offsets are zero-based. Every selected row is NODE or EXCLUDED; coverage is exhaustive within selected slices, not the whole library.

Native input-bindings.json binds 87 current whole/control inputs. Whole source and selected fragment hashes are distinct. Raw hashes use exact bytes; LF replaces CRLF only and rejects lone CR. Native logical run SHA256 is canonical UTF8 JSON of the whole run object minus run_sha256, sorted keys, compact separators, ensure_ascii=False. Outputs include the original preparatory artifacts and retained failed attempts; current closed lease is separately bound, and its write is the final filesystem operation.

Historical49/50 proof/sourcegraph exposure and own54 source-only primitive metadata are disclosed; no freshblind claim. Accidental GaussianConditionalKernel proof prefix43-57 and prior overwide/public locator snippets remain pinned EXCLUDED exposure, not copied proof ingredients. Failed guessed locators and representation attempts are retained. Final console printing encountered a GBK encoding failure after successful byte rechecks; it was corrected by UTF8 stdout, without any source change.

Remaining boundaries: independent topology review; subsequent root proof and independent exact verification; allrough B13 gradient/H1 closure limit; Gamma/halfturn/main/mixing/cost/composition. Compiler NOT_STARTED_CLOSED. No theorem55 implementation, claim, SAU, self-admission, or canonical mutation.
'''
(OUT / 'capsule.md').write_bytes(capsule.encode('utf-8'))
write('creation-dependencies.json', {
    'schema': 'sourcegraph55-creation-dependencies/v1',
    'actual_current_open_snapshot': descriptor(OUT / 'lease.open.snapshot.json'),
    'historical_preread_CLOSED': [i for i in inputs if i.get('role', '').startswith('historical immutable CLOSED')],
    'source_before_candidate_freeze': descriptor(OUT / 'primary-before-signature.freeze.json'),
    'root_typed_StatementSeal_status_only': descriptor(ROOT / 'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-preproof55/statement-seals.accepted.json'),
    'compiler': 'NOT_STARTED_CLOSED',
    'original_scopes_reopened': False,
    'future_independent_topology': 'required; creator cannot admit',
    'LF_recipe': 'replace CRLF only; reject remaining lone CR'
})
write('final-byte-readback.json', {
    'status': 'creator mechanical byte recheck only', 'inputs_rechecked': len(inputs),
    'sourcegraph_counts': counts, 'unresolved_active_lexemes': 0,
    'inherited_mechanical_detail': descriptor(OUT / 'creator-byte-bookkeeping.json'),
    'self_topology_admission': False, 'compiler_started': False,
    'console_failure': 'GBK UnicodeEncodeError while printing source-contract after successful input checks; retained here; UTF8 print retry succeeded without source edits'
})

# All filesystem enumeration and reads occur before writing the final CLOSED lease.
outputs = [descriptor(p) for p in sorted(OUT.rglob('*')) if p.is_file()
           and p.name not in ['run.json', 'lease.json']]
for item in outputs:
    assert descriptor(Path(item['path'])) == item
closed = dict(lease)
closed.update(read='CLOSED', write='CLOSED', python='CLOSED', compiler='NOT_STARTED_CLOSED',
              stage='SOURCE_GRAPH_COMPLETE_PENDING_INDEPENDENT_TOPOLOGY', candidate_read=True,
              implementation_read=False, closed_utc=datetime.now(timezone.utc).isoformat(),
              closure_rule='All native outputs and readbacks completed before this final filesystem write',
              creator_admission=False, proof_or_claim_created=False)
closed_bytes = encode(closed)
closed_desc = descriptor(OUT / 'lease.json', closed_bytes)
run = dict(schema='sourcegraph55-native-run/v1', status='CLOSED_SOURCE_ONLY_PENDING_INDEPENDENT_TOPOLOGY',
           inputs=inputs, outputs=outputs, counts=counts, actual_closed_lease=closed_desc,
           created_utc=datetime.now(timezone.utc).isoformat(),
           LF_recipe='CRLF -> LF only; reject remaining lone CR; exact UTF8 byte fragment offsets',
           logical_hash_recipe='SHA256 UTF8 JSON whole object minus run_sha256, sort_keys=True, separators=(comma,colon), ensure_ascii=False',
           compiler='NOT_STARTED_CLOSED', implementation55_seen=False,
           source_or_topology_admitted_by_creator=False, canonical_mutation=False)
run['run_sha256'] = sha(json.dumps(run, ensure_ascii=False, sort_keys=True,
                                 separators=(',', ':')).encode('utf-8'))
run_bytes = encode(run)
(OUT / 'run.json').write_bytes(run_bytes)
assert (OUT / 'run.json').read_bytes() == run_bytes
summary = dict(run_raw_LF=descriptor(OUT / 'run.json', run_bytes),
               run_logical=run['run_sha256'], lease_raw_LF=closed_desc,
               graph=descriptor(OUT / 'source-proof-graph.json'),
               capsule=descriptor(OUT / 'capsule.md'), counts=counts,
               output_count=len(outputs), input_count=len(inputs))
# LAST FILESYSTEM OPERATION. No reads/stats/enumerations/subprocesses after it.
(OUT / 'lease.json').write_bytes(closed_bytes)
print(json.dumps(summary, ensure_ascii=False, indent=2))
