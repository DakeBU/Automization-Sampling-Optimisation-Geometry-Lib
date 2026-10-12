from pathlib import Path
import json,hashlib,datetime,subprocess
pre=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
src=pre.parent/'pbps-actual-normalized-endpoint104/next-primary105'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
delivery=load(src.parent/'integration104/postpush-binding104.json')
assert head==delivery['local_head']==delivery['remote_head']==delivery['pr']['headRefOid']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
assert load(pre/'fetch-status105.json')['exit_code']==0
header=ref(pre/'Header105.lean')
assert header['raw_sha256']=='209ca04935d0dc953d86d334db4e62129642b57b04d18dc4354bbad5e1f0f89d'
assert load(pre/'header105.receipt.json')['exit_code']==0
# Actual reviewer decisions and topology counts are filled only after native outputs arrive.
config=load(pre/'review-admission-config105.json')
for key in ['math','source','topology']:
 p=Path(config[key]['path']);assert sha(p.read_bytes())==config[key]['raw_sha256']
 d=load(p);assert d[config[key]['decision_field']]==config[key]['expected_decision']
artifacts=[];bindings={}
def walk(v):
 if isinstance(v,dict):
  name,digest=v.get('path'),v.get('raw_sha256')
  if isinstance(name,str) and isinstance(digest,str) and len(digest)==64:
   raw=Path(name).read_bytes();row=dict(path=name,raw_sha256=digest)
   if sha(raw)!=digest and 'line_start' in v and 'line_end' in v:
    raw=b''.join(raw.splitlines(keepends=True)[v['line_start']-1:v['line_end']]);row.update(line_start=v['line_start'],line_end=v['line_end'])
   elif sha(raw)!=digest and 'byte_start' in v and 'byte_end_exclusive' in v:
    raw=raw[v['byte_start']:v['byte_end_exclusive']];row.update(byte_start=v['byte_start'],byte_end_exclusive=v['byte_end_exclusive'])
   assert sha(raw)==digest,('RAW_BINDING_MISMATCH',name,digest,sha(raw));bindings[(name,digest)]=row
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for folder in [src,pre/'independent-header-math105',pre/'independent-header-source105',pre/'source-graph-repair105']:
 for p in sorted(folder.rglob('*.json')):
  artifacts.append(ref(p));walk(load(p))
r=load(src/'recommendation105.native.json')
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=header,
 expanded_literal_Prop=Path(header['path']).read_text(encoding='utf8').split('def candidate',1)[1].split('#check candidate',1)[0].strip(),
 proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw.actual_countable_endpoint_law',
 source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',
 source_anchor='Appendix A.1 A7, initial Gibbs averaging and nonnegative Tonelli before A8: actual normalized countable endpoint-pair law assembly and reversal.',
 independent_math_header=ref(config['math']['path']),independent_source_header=ref(config['source']['path']),independent_topology=ref(config['topology']['path']),
 source_graph=ref(config['source_graph']),source_coverage=ref(config['source_coverage']),primary=ref(load(src/'primary-first-reconstruction105.native.json')['primary']['path']),
 all_review_artifacts_rehashed=artifacts,all_bound_RAW_inputs_rehashed=list(bindings.values()),
 binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING='Finite-dimensional real Hilbert Borel space, including rank zero.',EXCESS=[]),
 definition_audit='Literal actual93 harmonic flow, reflection, hazard, exponential clocks, stopped recursion, event sectors, prescribed Gamma and rho; one global actual Z with joint measurability, arc/fallback/zero characterization. Exact tilted position times standard Gaussian initial phase. Actual endpoint pushforward Q, all-Nat sector sum and same flipped swap J.',
 core_delta=r['statement'],actual_producer_plan=[x['declaration'] for x in load(src/'retrieval105.native.json')['selected_actual_public_producers']],consumer=r['real_consumer'],
 truth_boundary='Actual normalized countable endpoint law, probability and endpoint reversal only. Signed bilinear averaging, phase marginal invariance, restart/Markovness, hypocoercivity, implementation errors, expected costs, full composition and four full papers remain open.',
 upstream_reconciliation=dict(fetched_main=load(pre/'fetch-status105.json')['origin_main'],pending=True,reason='Sphere-gradient upstream changes do not alter the exact four sealed producer files or pinned toolchain; reconcile shared integration surfaces before next publication.'),
 source_topology_counts=config['counts'],proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal105.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('SEALED105',sha(p.read_bytes()),len(bindings))
