"""Freeze the exact independently reviewed candidate only after98 remote delivery."""
from pathlib import Path
import datetime,hashlib,json,subprocess
root=Path.cwd().resolve();pre=Path(__file__).resolve().parent.relative_to(root)
source=pre.parent/'pbps-actual-prescribed-gibbs-survival98/next-primary99-source-completion'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
push=load(pre.parent/'pbps-actual-prescribed-gibbs-survival98/integration98/postpush-binding98.json')
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
assert push['local_head']==push['remote_head']==head==push['pr']['headRefOid']
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedStateReversal.lean').exists()
checked={}
def visit(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   q=pin(v['path']);assert q['raw_sha256']==v['raw_sha256'],v['path'];checked[q['path']]=q
  for x in v.values():visit(x)
 elif isinstance(v,list):
  for x in v:visit(x)
manifests=[pre/'independent-header-math99/closed-RAW-header99.native.json',pre/'independent-header-math99/topology99/closed-RAW-topology99.native.json',pre/'independent-header-math99/minimal-import99/closed-RAW-minimal-import99.native.json',pre/'independent-header-source99/closed-RAW-header-source99.native.json',pre/'independent-header-source99/minimal-import-transfer/closed-RAW-transfer99.native.json',source/'closed-raw-manifest99.native.json']
for p in manifests:visit(load(p));checked[p.as_posix()]=pin(p)
math=pre/'independent-header-math99/header-math-decision99.native.json'
topology=pre/'independent-header-math99/topology99/source-topology-decision99.native.json'
src=pre/'independent-header-source99/header-source-decision99.native.json'
mt=pre/'independent-header-math99/minimal-import99/minimal-import-transfer99.native.json'
st=pre/'independent-header-source99/minimal-import-transfer/source-transfer99.native.json'
assert load(topology)['decision']=='ACCEPT_SOURCE_TOPOLOGY_AND_COVERAGE'
assert load(src)['verdict']=='accept-prospective-header-source-boundary'
assert load(mt)['decision']=='ACCEPT_EXACT_IMPORT_ONLY_HEADER_TRANSFER'
assert load(st)['verdict']=='accept-unchanged-mathematical-header'
for p in [math,topology,src,mt,st]:visit(load(p));checked[p.as_posix()]=pin(p)
header=pre/'Header99.minimal-import.lean'
assert pin(header)['raw_sha256']=='ee79c6079b533ff9bb374aae08a09dee7ea2efc5b7abb3cd1bb0c3fe131060e7'
for p in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json']:checked[p]=pin(p)
text=header.read_text(encoding='utf8')
d=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=pin(header),expanded_literal_Prop=text.split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 actual prescribed trajectories, A5 incoming-rate match and A8 reversed event substitution',independent_math_header=pin(math),independent_source_header=pin(src),independent_topology=pin(topology),minimal_import_transfers=[pin(mt),pin(st)],source_graph=pin(source/'source-proof-graph99.native.json'),source_coverage=pin(source/'source-coverage99.native.json'),primary=pin(pre.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),all_review_bound_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['finite-dimensional real Hilbert E with Borel measurable structure'],EXCESS=[]),definition_audit='Original actual c/Phi/S/zAt/K/Psi/Gamma, strict Prefix and unused exact comap measure; R and rate literal. A=Gamma(T); both grids include0 andT; post/arrive arrays use Fin(n+1), rate product Fin n. rho is produced with exact coordinates, never assumed.',core_delta='Actual reversed post and incoming states equal momentum reversals of original incoming and post states at reversed arc indices; all incoming real-rate products agree.',export_alignment='Two state identities and product equality are public. EVENT99/per-event rate equality is an internal source proof node, not a fourth public conclusion.',actual_producer_plan=['ActualPhaseReversalVolume.actual_phase_reversal_volume_laws','ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws'],consumer='Actual94 incoming-density factors, later open-arc/AE reversal with actual flow group law, then98 Gibbs/survival and97 weighted sector substitution.',truth_boundary='No pointwise reversal of right-continuous path values at genuine jumps; no survival time substitution, weighted density equality, invariant probability, Markovness, hypocoercivity, implementation error, expected cost, main result or composition.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal99.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(seal=pin(p),bound_inputs=len(checked),proved=False)))
