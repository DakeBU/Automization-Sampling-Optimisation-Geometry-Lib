from pathlib import Path
import json,hashlib,subprocess,datetime
pre=Path(__file__).parent;src=pre.parent/'pbps-actual-bounded-gibbs-duality106/next-primary107'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();delivery=load(src.parent/'integration106/postpush-binding106.json');assert head==delivery['local_head']==delivery['remote_head']==delivery['pr']['headRefOid']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main',head]).returncode==0
header=ref(pre/'Header107.lean');assert header['raw_sha256']=='cd447dcfc7bbff5045c9fd99d190b72a154f1443d4793c82c728dc4313612352'
assert load(pre/'type-only1/receipt.json')['exit_code']==0
math=pre/'independent-header-math107/header-math-decision107.native.json';source=pre/'independent-header-source107/header-source-decision107.native.json';top=src/'independent-topology107/v2-admission/admission107.v2.native.json'
assert load(math)['decision']=='ACCEPT_EXACT_HEADER_FOR_STATEMENT_SEAL_AND_SUBSEQUENT_PROOF'
assert load(source)['decision']=='ACCEPT_PROSPECTIVE_EXACT_HEADER_SOURCE_BOUNDARY'
assert load(top)['decision']=='ACCEPT_EXACT_V2_PROPOSAL_FOR_PROSPECTIVE_STATEMENT_SEAL'
artifacts=[];bindings={}
historical_index=src.parent/'integration106/affected-graph/3.before.exactraw.snapshot'
def walk(v):
 if isinstance(v,dict):
  name,digest=v.get('path'),v.get('raw_sha256')
  if isinstance(name,str) and isinstance(digest,str) and len(digest)==64:
   raw=Path(name).read_bytes();row=dict(path=name,raw_sha256=digest)
   if sha(raw)!=digest and 'line_start' in v and 'line_end' in v:
    raw=b''.join(raw.splitlines(keepends=True)[v['line_start']-1:v['line_end']]);row.update(line_start=v['line_start'],line_end=v['line_end'])
   elif sha(raw)!=digest and 'byte_start' in v and 'byte_end_exclusive' in v:
    raw=raw[v['byte_start']:v['byte_end_exclusive']];row.update(byte_start=v['byte_start'],byte_end_exclusive=v['byte_end_exclusive'])
   elif name=='research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json' and digest=='7e57337b2f1bcc63c50aba1e5c11714b9a42e5b35a491c3691e6a0b0c4abe7a3':
    raw=historical_index.read_bytes();row.update(exact_historical_recovery=historical_index.as_posix(),role='Historical retrieval index, regenerated during106. Scheduling uses fresh107 capsule/checkpoint; not proof evidence.')
   assert sha(raw)==digest,('RAW_BINDING_MISMATCH',name,digest,sha(raw));bindings[(name,digest)]=row
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for folder in [src,pre/'independent-header-math107',pre/'independent-header-source107']:
 for p in sorted(folder.rglob('*.json')):artifacts.append(ref(p));walk(load(p))
rec=load(src/'recommendation107.native.json');graph=src/'graph-expansion107/source-proof-graph-delta107.v2.native.json'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=header,
 expanded_literal_Prop=Path(header['path']).read_text(encoding='utf8').split('def candidate',1)[1].split('#check candidate',1)[0].strip(),
 proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation.actual_l2_expectation_contraction',
 source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 bounded signed duality toward Eq A.3: actual fixed-time L2 operator construction and contraction, before density extension.',
 independent_math_header=ref(math),independent_source_header=ref(source),independent_topology=ref(top),source_graph=ref(graph),source_coverage=ref(src/'graph-expansion107/source-coverage107.v2-overlay.native.json'),primary=rec['source'],all_review_artifacts_rehashed=artifacts,all_bound_RAW_inputs_rehashed=list(bindings.values()),
 binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING='Finite-dimensional real inner-product Borel space, including rank zero.',OBSERVABLE='Borel test functions and bounded tests; arbitrary MemLp real representatives within universal conclusion.',EXCESS=[]),
 definition_audit='37 literal global actual algorithm/clock/path/phase definitions, two inherited op/endpoint lets and one opG let (40total). Same global Z retains all106 conclusions. No supplied process/kernel/operator or integrability/contraction premise.',
 core_delta='For the same actual global Z from106, prove joint Borel clock expectation for Borel tests, bounded section integrability, and internally construct a family of real L2 continuous linear contractions with norm at most1. For every arbitrary MemLp input prove almost-everywhere clock-section integrability, actual expectation MemLp and quotient identification, square-integral bound, and zero-time identity.',
 actual_producer_plan=rec['actual_direct_producers'],consumer='Actual Appendix A.3 L2 density extension needs this same-process bounded operator and representative identification; restart/semigroup and separate existential kernels are distinct consumers requiring separate adapters.',
 truth_boundary='Fixed-time real L2 expectation contraction with inherited106 bounded duality/invariance. Full A.3 identity, strong continuity, restart/Markov/semigroup, separate kernel-witness identification, hypocoercivity, implementation errors, actual expected costs, composition and all four full papers remain open.',
 upstream_reconciliation=dict(fetched_main=subprocess.check_output(['git','rev-parse','origin/main']).decode().strip(),pending=False),source_topology_counts=load(graph)['counts'],current_scheduling_capsule=ref(pre/'capsule107.stdout.log'),current_checkpoint=ref(pre/'companion-papers-handoff.md.current.exactraw'),proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal107.json';assert not p.exists();p.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('SEALED107',sha(p.read_bytes()),len(bindings))
