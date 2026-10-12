from pathlib import Path
import json,hashlib,subprocess,datetime
pre=Path(__file__).parent;src=pre.parent/'pbps-actual-l2-flip-duality108/next-primary109'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();delivery=load(src.parent/'integration108/postpush-binding108.json');assert head==delivery['local_head']==delivery['remote_head']==delivery['pr']['headRefOid']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main',head]).returncode==0
header=ref(pre/'Header109.lean');assert header['raw_sha256']=='927043eaaace6083ec00c750037e4c69f21173595b85646bb9a5a1b63795e31b'
assert load(pre/'type-only1/receipt.json')['exit_code']==0
math=pre/'independent-header-math109/header-math-decision109.native.json';source=pre/'independent-header-source109/header-source-decision109.native.json';top=src/'independent-topology109/decision109.native.json'
assert load(math)['decision']=='ACCEPT_EXACT_HEADER109_FOR_SEAL_AND_PROOF'
assert load(source)['verdict']=='ACCEPT_EXACT_PROSPECTIVE_HEADER_SOURCE_BOUNDARY'
assert load(top)['decision']=='ACCEPT_EXACT_PROSPECTIVE109_GRAPH_AND_BOUNDED_ROUTE'
artifacts=[];bindings={}
def walk(v,context):
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
  for x in v.values():walk(x,context)
 elif isinstance(v,list):
  for x in v:walk(x,context)
for folder in [src,pre/'independent-header-math109',pre/'independent-header-source109']:
 for p in sorted(folder.rglob('*.json')):artifacts.append(ref(p));walk(load(p),p.parent)
rec=load(src/'recommendation109.native.json');graph=src/'source-proof-graph-delta109.native.json'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=header,
 expanded_literal_Prop=Path(header['path']).read_text(encoding='utf8').split('def candidate',1)[1].split('#check candidate',1)[0].strip(),
 proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging.actual_position_l2_averaging',
 source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1(iii) and final Gaussian momentum averaging lines3246-3259; A.2 lines3265-3287 is a future consumer only.',
 independent_math_header=ref(math),independent_source_header=ref(source),independent_topology=ref(top),source_graph=ref(graph),source_coverage=ref(src/'source-coverage109.native.json'),primary=load(src/'primary-first109.native.json')['primary'],all_review_artifacts_rehashed=artifacts,all_bound_RAW_inputs_rehashed=list(bindings.values()),
 binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING='Finite-dimensional real inner-product Borel space, including rank zero.',OBSERVABLE='Inherited Borel/bounded tests and arbitrary MemLp representatives and L2 classes.',EXCESS=[]),
 definition_audit='All37 actual global definitions retained. Same global Z and A/J retain every108 output. mu is literal position tilted law, B canonical fst pullback, M its adjoint, Kpos_T=M A_T B. All regularity and representative identities are outputs, never supplied providers.',
 core_delta='For the same actual108 global process Z and real L2 family A/J, construct canonical Gaussian averaging M=B.adjoint, identify its literal Gaussian integral for arbitrary MemLp representatives, and prove Kpos_T=M A_T B is selfadjoint, norm at most1, Kpos_0=id with its literal Gaussian-outer clock-inner expectation representative.',
 actual_producer_plan=load(graph)['actual_direct_producers_planned'],consumer=rec['actual_consumer'],truth_boundary='Fixed-reference real L2 Gaussian momentum averaging and actual position expectation. Markov positivity/constants, strong continuity, restart/semigroup/kernel-witness identity, reference averaging, complex L2, hypocoercivity, implementation errors, expected costs, actual-input composition and all four complete papers remain open.',
 upstream_reconciliation=dict(fetched_main=subprocess.check_output(['git','rev-parse','origin/main']).decode().strip(),pending=False),source_topology_counts=load(graph)['counts'],current_scheduling_capsule=ref(pre/'capsule109.stdout.log'),current_checkpoint=ref(pre/'companion-papers-handoff.md.current.exactraw'),proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal109.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('SEALED109',sha(p.read_bytes()),len(bindings))
