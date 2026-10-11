"""Freeze the type-only target after independent prospective math/source audits."""
from pathlib import Path
import datetime, hashlib, json, subprocess
root=Path.cwd().resolve()
pre=Path(__file__).resolve().parent.relative_to(root)
next_source=pre.parent/'pbps-actual-bounded-path-expansion95/next-primary96'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
checked={}
def visit(v):
    if isinstance(v,dict):
        if 'path' in v and 'raw_sha256' in v:
            q=pin(v['path']);assert q['raw_sha256']==v['raw_sha256'],v['path']
            checked[q['path']]=q
        for x in v.values():visit(x)
    elif isinstance(v,list):
        for x in v:visit(x)
for p in [pre/'independent-header-math96/closed-RAW-manifest96.native.json',pre/'independent-header-source96/closed-raw-manifest96.native.json',next_source/'closed-raw-manifest96.native.json',next_source/'scope96/closed-raw-manifest-scope96.v3.native.json']:
    visit(load(p));checked[p.as_posix()]=pin(p)
math=pre/'independent-header-math96/header-math-decision96.native.json'
source=pre/'independent-header-source96/header-source-review96.native.json'
assert load(math)['decision']=='ACCEPT_EXACT_HEADER_NO_REQUIRED_MATHEMATICAL_REPAIR'
assert load(source)['verdict']=='ACCEPTABLE_FOR_STATEMENT_SEAL_FROM_SOURCE_SCOPE_ONLY'
assert not load(source)['required_changes'] and not load(source)['blocking_findings']
header=pre/'Header96.lean'
assert pin(header)['raw_sha256']=='7a3d1929ccc6f1ae01ac3187040ad032515df7af0d627636d646d7f4df382a91'
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean').exists()
for p in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json',pre/'reuse-search96/receipt.json']:
    checked[str(p).replace('\\','/')]=pin(p)
text=header.read_text(encoding='utf8')
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_MATH_AND_SOURCE_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),header=pin(header),expanded_literal_Prop=text.split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 actual flow, reflection A5/A6, direct elementary dependency of A8 finite prescribed endpoint/time reversal',independent_math_header=pin(math),independent_source_header=pin(source),source_graph=pin(next_source/'source-proof-graph-delta96.native.json'),source_coverage=pin(next_source/'source-coverage-delta96.native.json'),primary=load(source)['primary'],all_review_bound_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['finite-dimensional real Hilbert E with Borel measurable structure'],test_scope='Integrable real F is local to A6 integral conclusion over infinite phase Lebesgue measure.',EXCESS=[]),definition_audit='Eight literal definitions: c,h,B,S,R,Phi,rate,ell. ell explicitly equals volume(E).prod(volume(E)); zero division is Lean totalized zero, matching identity reflection at zero normal.',core_delta='Actual harmonic flow, state-dependent bounce and momentum reversal preserve phase product volume; their joint Borel laws and exact reversal/rate identities are proved conclusions. Existing inversion/measurability producers are reused.',consumer='Finite prescribed endpoint/time reversal involution for A8, then weighted A7 stationary averaging. Restart/Markovness is a separate obligation, not an invented prerequisite.',truth_boundary='No false unscaled harmonic isometry; no naive pointwise time reversal at right-continuous jump values; no stationary law, semigroup, hypocoercivity, unbounded cost or main/composition result.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
out=pre/'root.statement-seal96.json';assert not out.exists()
out.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(seal=pin(out),rehashed_inputs=len(checked),proved=False)))
