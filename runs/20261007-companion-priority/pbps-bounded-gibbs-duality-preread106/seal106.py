from pathlib import Path
import json,hashlib,subprocess,datetime
pre=Path(__file__).parent;src=pre.parent/'pbps-actual-countable-endpoint105/next-primary106'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();delivery=load(src.parent/'integration105/postpush-binding105.json');assert head==delivery['local_head']==delivery['remote_head']==delivery['pr']['headRefOid']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
header=ref(pre/'Header106.lean');assert header['raw_sha256']=='6e995eb9308bf5c6d09fcd15b6ebb0e120b3fced62202572a4041cbfe19e7b9d'
assert load(pre/'typecheck106/receipt.json')['exit_code']==0
math=pre/'independent-header-math106/header-math-decision106.native.json';source=pre/'independent-header-source106/header-source-decision106.native.json';top=src/'independent-topology106/topology-admission106.native.json'
assert load(math)['decision']=='ACCEPT_PROSPECTIVE_EXACT_HEADER_MATHEMATICS_AND_TYPE'
assert load(source)['verdict']=='ACCEPT_PROSPECTIVE_HEADER_SOURCE_BOUNDARY_ONLY'
assert load(top)['decision']=='ACCEPT_INHERITED105_PLUS_PROPOSED106_TOPOLOGY_AND_COVERAGE'
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
for folder in [src,pre/'independent-header-math106',pre/'independent-header-source106']:
 for p in sorted(folder.rglob('*.json')):artifacts.append(ref(p));walk(load(p))
graph=load(src/'source-proof-graph-delta106.native.json')
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=header,
 expanded_literal_Prop=Path(header['path']).read_text(encoding='utf8').split('def candidate',1)[1].split('#check candidate',1)[0].strip(),
 proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality.actual_bounded_gibbs_duality',
 source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 final bounded signed bilinear identity (A8 averaging) and F=1 fixed-time Gibbs stationarity.',
 independent_math_header=ref(math),independent_source_header=ref(source),independent_topology=ref(top),source_graph=ref(src/'source-proof-graph-delta106.native.json'),source_coverage=ref(src/'source-coverage-delta106.native.json'),primary=load(src/'recommendation106.native.json')['source'],all_review_artifacts_rehashed=artifacts,all_bound_RAW_inputs_rehashed=list(bindings.values()),
 binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING='Finite-dimensional real inner-product Borel space, including rank zero.',OBSERVABLE='Measurable bounded real F,G and finite nonnegative bounds within universal conclusion.',EXCESS=[]),
 definition_audit='37 literal actual algorithm/clock/path/phase definitions of105, exactly the same global Z arc/fallback/zero contract; two new internal let definitions op and endpoint. No arbitrary process/kernel provider, signed-integrability, mass or momentum-symmetry premise.',
 core_delta='Under the original six assumptions, one global actual jointly measurable Z satisfies the inherited arc/fallback/zero-time contract. Every y,r,T endpoint pushes nu_y times P to nu_y; every pair of bounded Borel real F,G yields both outer integrability conclusions and integral F*(op G) = integral (G composed R)*(op(F composed R)).',
 actual_producer_plan=[x['declarations'][0] for x in graph['actual_direct_producers_proposed']],consumer='Printed Appendix A.1 bounded duality and fixed-time Gibbs stationarity; future actual L2 and kernel-invariance consumers require their separate representation and same-witness adapters.',
 truth_boundary='Bounded signed Gibbs duality and fixed-time actual phase invariance only. L2 operator/domain identity, restart/Markovness, kernel-witness identification, hypocoercivity, simulation errors, actual expected costs, composition and all four full papers remain open.',
 upstream_reconciliation=dict(fetched_main=subprocess.check_output(['git','rev-parse','origin/main']).decode().strip(),pending=True,reason='New sphere-Rayleigh upstream changes do not alter three selected producers or toolchain; preserve shared changes in next serialized integration.'),source_topology_counts=load(top)['effective_counts'],proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal106.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('SEALED106',sha(p.read_bytes()),len(bindings))
