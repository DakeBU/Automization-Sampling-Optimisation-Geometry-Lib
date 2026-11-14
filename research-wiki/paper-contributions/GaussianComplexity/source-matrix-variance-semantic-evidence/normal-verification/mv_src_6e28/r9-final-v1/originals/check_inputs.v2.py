from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil,re
sys.dont_write_bytecode=True
os.environ['GIT_OPTIONAL_LOCKS']='0'
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=Path(__file__).resolve().parent
E=R/'research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence';N=E/'native-review/variance_native_61d0/originals';C=N.parent/'conditional-proposal-v3/originals';G=R/'.astis/semantic-neutral-20261113/variance_native_61d0/held-metadata-gates-R9-v1';S=R/'.astis/semantic-neutral-20261112/mv_src_6e28/incremental-reader-v3c'
HELD='02fb93c64e4222f112e57c97ced2a548235cd0f6';MATH='e654e98642350a615c473bc8190fbc1d47fe52bd';READER='1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
ADV='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def wr(n,x):
 with (B/n).open('x') as f:f.write(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
refs=[]
def ref(p,kind):
 b=p.read_bytes();d={'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b),'qualification':kind};refs.append(d);return d
assert git('rev-parse','HEAD').decode().strip()==HELD
assert git('status','--porcelain','-uno')==b''
idx=(R/'.git/index').read_bytes();assert len(idx)==25039709 and sha(idx)=='2f9f667a54d7dcfd9337a26e9c1d3d4c2c398965ca32cb88719b0d9c90f8f978'
checks={}
for label,root,want in [('native',N,'1379b67fc72814e6a12d04317b3780c56c4ba8b312720663bc8e39928121a72e'),('conditional',C,None),('gates',G,'c4df12ce12a96f467eeef687c063f5c97fbfcab246698e399c25158680b45058')]:
 p=root/'portable-manifest.json';m=read(p)
 if want:assert sha(p.read_bytes())==want
 total=0
 for x in m['files']:
  f=(R/x['destination']) if label=='conditional' else root/x['relative_source'];b=f.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],str(f);total+=len(b)
 ref(p,'manifest semantic contract parsed; every listed file independently byte/hash checked, not every file semantically read')
 checks[label+'_manifest']={'listed_files':len(m['files']),'listed_bytes':total,'manifest_sha256':sha(p.read_bytes()),'all_listed_bytes_match':True}
 for name in ['SEAL.json','postseal-envelope.json']:
  if (root/name).exists():ref(root/name,'full JSON parsed/read for custody/boundary, not compilation credit from metadata alone')
# Gate execution, exact arguments/outputs and once-only originals.
gs=read(G/'gate-summary.json');assert gs['all_four_actual_zero'] and gs['held_metadata_HEAD']==HELD and len(gs['gates'])==4
for i,x in enumerate(gs['gates']):
 d=G/'commands'/x['label'];r=read(d/'result.json');assert r['exit']==0 and r['held_metadata_HEAD']==HELD
 assert r['argv']==x['argv'] and x['HEAD_index_stable']
 for stream in ['stdout','stderr']:
  b=(d/stream).read_bytes();assert len(b)==r[stream]['bytes'] and sha(b)==r[stream]['sha256']
  if stream=='stderr':assert b==b''
  ref(d/stream,'actual raw metadata-gate output fully read/checked')
 ref(d/'result.json','complete receipt parsed incl argv, cwd, exact exit and output hashes')
 assert r['argv'][1] in ['tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_contributor_contract.py','tools/astis_frontier_cells.py']
 if i in [0,2]:assert r['argv'][-2:]==['--base','6819e686116e6f18df3ef0e638c6ca24bde7dd8d']
assert sha((G/'REPORT.md').read_bytes())=='2589fb4d904d3fb54a39a1c74d61531dec7ad5573aa60dd5c0f2cca0934eb74c'
assert sha((G/'SEAL.json').read_bytes())=='b976e6ccbaf73be21b332a3ab7eff0c9638efd3d08e4c97c4ae3f3afcfb1ec8a'
# Native exact fresh closure, dependency environment and actual kernel command.
p=read(N/'preparation.json');assert p['commit']==MATH and p['empty_output_initially'] and p['no_project_olean_read_or_copied'];assert len(p['sources'])==12
assert sha(Path(p['lean']).read_bytes())==p['toolchain']['sha256']
for x in p['toolchain']['pins']:
 q=R/'.lake/packages'/x['name'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=q).decode().strip()==x['pin']==x['head'];assert subprocess.check_output(['git','status','--porcelain','-uno'],cwd=q)==b''
for x in p['sources']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];assert git('show',MATH+':'+x['path'])==b;assert (N/'candidate'/x['path']).read_bytes()==b
for name in ['lean-toolchain','lake-manifest.json','lakefile.lean']:
 assert (R/name).read_bytes()==git('show',MATH+':'+name)==(N/'inputs'/name).read_bytes()
for i,x in enumerate(p['sources']):
 for label in [f'compile-{i:02d}',f'deps-{i:02d}']:
  d=N/'commands'/label;r=read(d/'result.json');assert r['exit']==0 and r['compiled_commit']==MATH
  assert r['effective_env']['LEAN_PATH'].split(':')[0]==str(Path(p['candidate'])/'empty-astis-output')
  assert str(R/'.lake/build/lib/lean') not in r['effective_env']['LEAN_PATH']
  for stream in ['stdout','stderr']:
   b=(d/stream).read_bytes();assert len(b)==r[stream]['bytes'] and sha(b)==r[stream]['sha256']
   if stream=='stderr':assert b==b''
  ref(d/'result.json','full original Lean dependency/compile receipt parsed; original streams checked, no rerun')
inv=read(N/'declaration-inventory.json');assert len(inv)==54 and all(x['closed'] and x['kernel_actual_typed_let_checked'] for x in inv)
assert all(set(x['axioms'])<=set(['propext','Classical.choice','Quot.sound']) for x in inv)
n=read(N/'native-summary.json');assert n['kernel_exit']==0 and n['actual_typed_let_kernel_checked_count']==54 and n['module_count']==12 and n['standard_axioms_only'];assert n['exact_parent_sets_verified'];assert n['fake_closure_scan']['findings']==[]
assert len(n['root_checks'])==2 and all(x['universal'] and x['q0'] for x in n['root_checks'])
assert all(x['root_reachable'] for key in ['P','T'] for x in n['owned'][key])
kr=read(N/'commands/inventory-kernel-v4/result.json');assert kr['exit']==0 and kr['compiled_commit']==MATH and kr['stderr']['bytes']==0
assert (N/'commands/inventory-kernel-v4/stderr').read_bytes()==b''
assert kr['stdout']['bytes']==2986990023 and kr['stdout']['sha256']=='13cbe6119ac7329e8a6568d487f85b5ae3f1fd9450f4d8793e273311b49dc65e'
md=[json.loads(l) for l in (N/'inventory-metadata.raw.jsonl').read_bytes().splitlines() if l.strip()];assert len([x for x in md if x['record']=='declaration'])==54
assert len([x for x in md if x['record']=='literal-root-value-check' and x['universal'] and x['q0']])==2
seal=read(R/'research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
script=(N/'IndependentInventory.v4.lean').read_text()
for tag,key in [('P','producer'),('T','actual_private_consumer')]:
 params,prop=seal[key]['signature'].split(':\n',1)
 expected=f'def {tag}Literal : Prop := ∀ {params.strip()},\n{prop}\n'
 assert expected in script
 assert f'def {tag}ZeroLiteral : Prop := ∀ {{d : ℕ}} (hq : 2 * 0 + 1 < d),\n'+prop.replace('q','0')+'\n' in script
for text in ['ci.value? (allowOpaque := true)','Expr.letE `actual_value ci.type value (.bvar 0) false','value := actualValue','value := zeroValue']:
 assert text in script
for f in ['native-stage-seal.json','native-summary.json','native-REPORT.md','IndependentInventory.v4.lean','inventory-metadata.raw.jsonl','declaration-inventory.json','expression-token-hashes.json','compile.py','preparation.json','commands/inventory-kernel-v4/result.json']:
 ref(N/f,'complete semantic/machine read of native contract/checker/metadata; full 2.99GB proof dump not semantically read')
assert sha((N/'native-stage-seal.json').read_bytes())=='8fcdfb3cfe37033dd30acebdb3e098a3b55970f6b9b6a60ac3a53fdc66f4c3ef'
# Keep original reader failure separate from conditional prototype.
a=read(N/'reader-assessment.json');assert a['browser_actual_exit']==1 and a['disposition']=='NATIVE_PASS_READER_FAIL';assert a['four_contexts_completed'] and a['source_download_checks_completed']==8 and a['blocker']['wrapper_scrollLeft_after_set100']==0
ca=read(C/'assessment.json');assert ca['outcome']=='CONDITIONAL_PROPOSAL_PASS' and ca['canonical_integration_status']=='UNAPPLIED' and ca['actual_browser_exit']==0;assert ca['original_reader_outcome']=='FAIL, unchanged'
assert sha((R/'website/static/proof-readers.css').read_bytes())=='4509e56205aa4bb94c3fa32c7b2b0bd98a9b44a71c23e09f18d5affe038512ad'
for f in [N/'REPORT.md',N/'reader-assessment.json',N/'browser-report-1d0-v2.json',N/'visual-inspection.json',C/'REPORT.md',C/'assessment.json',C/'input-delta.json']:
 ref(f,'complete report/diagnostic parsed/read; original FAIL preserved, conditional prototype not canonical delivery')
# Reuse own immutable source decisions and exact current binding, not native compiler as source fidelity.
sys.path.insert(0,str(R/'tools'));import astis_publication as ap
po=read(S/'P/canonical-audit-overlay.portable.json');td=read(S/'T/private-consumer-source-decision.portable.json')
reg=read(R/'research-wiki/semantic-roundtrip/registry.json')['audits'];audit=next(x for x in reg if x['id']==po['id'])
for k in ['state','semantic_slots','deltas','verdict','source_review','repairs']:
 assert audit[k]==po[k],k
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
name=po['lean']['declaration'];item=next(x for x in ap.load() if any(y['declaration']==name for y in x['bindings']));binding=next(y for y in item['bindings'] if y['declaration']==name)
assert ap.binding_digest(item,binding)=='00bdeee242bd0c09802bbe1d7497da5da80c58d77f4ddb54df8196b5db27f1cf'
assert ap.binding_payload(item,binding)==read(S/'full-publication-binding-payload.checked.json')
for f in [S/'P/canonical-audit-overlay.portable.json',S/'P/reviewer-run.json',S/'T/private-consumer-source-decision.portable.json',S/'T/reviewer-run.json',S/'INCREMENTAL-SOURCE-FROZEN.json']:
 ref(f,'own prior independent frozen source decision reused unchanged; no fresh source self-certification')
for f in ['website/content/declaration_lessons/huanjian-gaussian-source-matrix-variance.json','website/content/publications/huanjian-gaussian-source-matrix-variance.json']:
 assert (R/f).read_bytes()==git('show',READER+':'+f)
# PL and own/foreign status.
plraw=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();assert sha(plraw)=='6d33efc87376f754034dcf4acf6f9acc6d6995a748f80d43a6a1302412d6e3e1';pl=json.loads(plraw);assert len(pl)==21
rows=[json.loads(x) for x in (R/'runs/substantive_advances.jsonl').read_bytes().splitlines() if x.strip()]
assert not any(x.get('advance_id')==ADV and x.get('to_state')=='VERIFIED' for x in rows)
assert [x for x in rows if x.get('advance_id')==ADV and x.get('to_state')=='PROVED_LOCAL'][-1]['evidence']==pl
assert sha((R/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json').read_bytes())=='5918990bf0a5fc8c1da2522bf8d02d456dbe443fa0d4eaf9bd56322900533138'
ref(E/'actual-PROVED_LOCAL-evidence.full.json','all 21 original PL values complete inline source')
(B/'inputs/actual-PROVED_LOCAL-evidence.full.json').write_bytes(plraw)
# Capture 54 gate originals locally, native and conditional remain exact tracked portable original references.
shutil.copytree(G,B/'inputs/held-metadata-gates-R9-v1')
checks.update({'all_pass':True,'held_HEAD':HELD,'actual_math_commit':MATH,'reader_commit':READER,'four_gates_actual_zero':True,'12_exact_sources_equal_current_and_math_commit':True,'54_complete_kernel_body_checks_standard_axioms':True,'four_actual_root_proof_value_literal_applications':True,'all_7_owned_declarations_reachable':True,'current_source_audit_equals_own_frozen_decision':True,'current_publication_binding':'00bdeee242bd0c09802bbe1d7497da5da80c58d77f4ddb54df8196b5db27f1cf','original_reader':'FAIL_MOBILE_TABLE_CLIPPING_UNCHANGED','conditional_prototype':'PASS_UNAPPLIED_NOT_CANONICAL_DELIVERY','PL_original_field_count':21,'R9_historical_V_count':0,'API_calls':0,'new_builds_browser_or_four_gates_run':0,'full_proof_dump_read':False})
wr('input-original-references.json',refs);wr('independent-input-checks.json',checks)
print(json.dumps(checks,indent=2))
