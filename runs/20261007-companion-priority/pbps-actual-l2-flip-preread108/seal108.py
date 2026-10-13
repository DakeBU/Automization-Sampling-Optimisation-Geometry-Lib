from pathlib import Path
import json,hashlib,subprocess,datetime
pre=Path(__file__).parent;src=pre.parent/'pbps-actual-l2-expectation107/next-primary108'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();delivery=load(src.parent/'integration107/postpush-binding107.json');assert head==delivery['local_head']==delivery['remote_head']==delivery['pr']['headRefOid']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main',head]).returncode==0
header=ref(pre/'Header108.lean');assert header['raw_sha256']=='72b87d59ed60dbe26c4174c949289d07b8328b72224ce3fb3a8fd21b5f0775ae'
assert load(pre/'type-only1/receipt.json')['exit_code']==0
math=pre/'independent-header-math108/header-math-decision108.native.json';source=pre/'independent-header-source108/header-source-decision108.native.json';top=src/'independent-topology108/v2-admission/admission108.v2.native.json'
assert load(math)['decision']=='ACCEPT_EXACT_HEADER108_FOR_SEAL_AND_PROOF'
assert load(source)['verdict']=='ACCEPT_EXACT_PROSPECTIVE_HEADER_SOURCE_BOUNDARY_ONLY'
assert load(top)['decision']=='ACCEPT_EXACT_PROSPECTIVE108_GRAPH_V2'
artifacts=[];bindings={}
def walk(v, context):
 if isinstance(v,dict):
  name,digest=v.get('path'),v.get('raw_sha256')
  if isinstance(name,str) and isinstance(digest,str) and len(digest)==64:
   q=Path(name)
   if not q.exists():q=context/name
   raw=q.read_bytes();row=dict(path=q.as_posix(),raw_sha256=digest)
   if sha(raw)!=digest and 'line_start' in v and 'line_end' in v:
    raw=b''.join(raw.splitlines(keepends=True)[v['line_start']-1:v['line_end']]);row.update(line_start=v['line_start'],line_end=v['line_end'])
   elif sha(raw)!=digest and 'byte_start' in v and 'byte_end_exclusive' in v:
    raw=raw[v['byte_start']:v['byte_end_exclusive']];row.update(byte_start=v['byte_start'],byte_end_exclusive=v['byte_end_exclusive'])
   assert sha(raw)==digest,('RAW_BINDING_MISMATCH',name,digest,sha(raw));bindings[(name,digest)]=row
  for x in v.values():walk(x, context)
 elif isinstance(v,list):
  for x in v:walk(x, context)
for folder in [src,pre/'independent-header-math108',pre/'independent-header-source108']:
 for p in sorted(folder.rglob('*.json')):artifacts.append(ref(p));walk(load(p), p.parent)
rec=load(src/'recommendation108.native.json');graph=src/'route-policy-repair108/source-proof-graph-delta108.v2.native.json'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=header,
 expanded_literal_Prop=Path(header['path']).read_text(encoding='utf8').split('def candidate',1)[1].split('#check candidate',1)[0].strip(),
 proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality.actual_l2_flip_duality',
 source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 Eq A.3 (A1.E3 lines3000-3014), density extension (A1.Ex21 lines3210-3227), phase law Eq3.1 lines1411-1422.',
 independent_math_header=ref(math),independent_source_header=ref(source),independent_topology=ref(top),source_graph=ref(graph),source_coverage=ref(src/'route-policy-repair108/source-coverage108.v2-overlay.native.json'),primary=rec['source'],all_review_artifacts_rehashed=artifacts,all_bound_RAW_inputs_rehashed=list(bindings.values()),
 binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING='Finite-dimensional real inner-product Borel space, including rank zero.',OBSERVABLE='Inherited Borel/bounded tests and arbitrary MemLp real representatives; new universally quantified L2 classes.',EXCESS=[]),
 definition_audit='37 literal global actual algorithm/clock/path/phase definitions retained, inherited op/endpoint/opG lets and canonical J pullback (41 total). Same global Z and same A family retain all107 conclusions. Measure preservation of R is an output; no supplied process/operator/duality premise.',
 core_delta='For the same actual global Z and real L2 expectation family A from107, prove the canonical momentum-flip pullback J is an involutive L2 isometry and every fixed-time adjoint satisfies A_T.adjoint = J composed A_T composed J, by bounded simple representatives and continuous two-variable density extension.',
 actual_producer_plan=load(graph)['actual_direct_producers_planned'],consumer='Actual momentum-averaged position self-adjointness; future hypocoercive operator analysis also requires separately proved domain, continuity and semigroup facts.',
 truth_boundary='Full fixed-time real L2 flip adjoint identity with all107 conclusions. Strong continuity, restart/Markov/semigroup, separate kernel-witness identification, momentum-averaged position operator, hypocoercivity, implementation errors, actual expected costs, composition and all four full papers remain open.',
 upstream_reconciliation=dict(fetched_main=subprocess.check_output(['git','rev-parse','origin/main']).decode().strip(),pending=False),source_topology_counts=load(graph)['counts'],current_scheduling_capsule=ref(pre/'capsule108.stdout.log'),current_checkpoint=ref(pre/'companion-papers-handoff.md.current.exactraw'),proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal108.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('SEALED108',sha(p.read_bytes()),len(bindings))
