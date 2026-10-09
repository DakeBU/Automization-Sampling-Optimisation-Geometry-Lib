from common import *
import gzip,re,html
openings=J(P/'opening.inputs.json');supp=J(P/'opening.assets.supplement.json');tree=J(P/'integration.tree.index.json')['files'];notes=J(R/'integration.notes.json');plan=J(R/'publication-plan.json');exact=R/'exact-science-verification';rows=[];seen=set()
def bind(q,resolved=None,label=''):
 expected=dict(q);expected['path']=path(q['path']).as_posix();dest=path(resolved or expected['path']).as_posix();key=(expected['path'],expected['raw_sha256'],expected.get('lf_sha256'))
 matches(expected,dest)
 if key not in seen:seen.add(key);rows.append(dict(expected=expected,resolved_path=dest,label=label))
 return dest
frozen={p['original']['path']:p['exact_raw_snapshot']['path'] for p in openings['snapshot_pairs']+supp['pairs']}
for pair in openings['snapshot_pairs']+supp['pairs']:bind(pair['original'],pair['exact_raw_snapshot']['path'],'exact opening snapshot');bind(pair['exact_raw_snapshot'])
def original_bytes(p):return path(frozen.get(path(p).as_posix(),path(p).as_posix())).read_bytes()
def gj(p):return json.loads(original_bytes(p))
for q in J(P/'integration.git.entries.json')['entries']:bind(q['opening_current'],frozen.get(q['opening_current']['path']),'exact integration1875 current originals frozen before63')
# Inspect exact existing science, never later63 files.
for q in J(exact/'inputs.before.json')['mathematical_freeze']:bind(q,label='unchanged math27')
prior=J(exact/'run.json');assert H(C({k:v for k,v in prior.items() if k!='run_sha256'}))==prior['run_sha256'];assert H((exact/'named-exact-verification.payload.json').read_bytes())==prior['named_payload_raw_sha256']
lease=J(exact/'lease.json');assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_terminal_readback']['exit_code']==0
for field in ['run','receipt','named_payload','inputs','outputs','readback_status','verified']:bind(lease[field],label='exact62 actual CLOSED lease output')
maps=[]
cellpaths=[ROOT/'research-wiki/frontier-cells'/f'{c}.json' for c in plan['active_cells']]
for i,p in enumerate(cellpaths):
 raw=subprocess.check_output(['git','show',SCI+':'+p.relative_to(ROOT).as_posix()],cwd=ROOT);dest=P/f'science-cell-{i}.qualified.exactraw.snapshot';dest.write_bytes(raw)
 maps.append(dict(qualified_original_path=p.as_posix(),exact_raw_snapshot=pin(dest),source='Exact SCI62 Git blob; current administrative cell differs explicitly.'))
ledger_before63=ROOT/'runs/20261007-companion-priority/pbps-macro-root63/ledger.before63.exactraw.snapshot'
for row in J(exact/'strict-inputs.json')['rows']:
 q=row['expected'];resolved=row['resolved_path']
 if path(q['path']) in cellpaths:
  m=next(m for m in maps if m['qualified_original_path']==path(q['path']).as_posix());resolved=m['exact_raw_snapshot']['path'];matches(q,resolved)
 elif path(q['path'])==ROOT/'runs/substantive_advances.jsonl' and resolved==q['path']:
  matches(q,ledger_before63);resolved=ledger_before63.as_posix();maps.append(dict(qualified_original_path=q['path'],expected=q,exact_raw_snapshot=pin(ledger_before63),source='Exact62 post-VERIFIED ledger before root63 claim, single fully qualified map.'))
 bind(q,resolved,'reused exact62 strict1162 input')
for q in J(exact/'outputs.manifest.json')['artifacts']:bind(q,label='exact62 own immutable outputs65')
native=J(exact/'native.review.json')
for folder,payload,key in [('independent-math62','named-mathematics.payload.json','whole_math_run_sha256'),('source-review62','named-source-review.payload.json','source_run_sha256')]:
 run=J(R/folder/'run.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==native[key];l=J(R/folder/'lease.json');assert l['status']=='CLOSED' and l['closed_last'];bind(pin(R/folder/'run.json'));bind(pin(R/folder/'lease.json'));bind(pin(R/folder/payload))
# Actual native gates: consume terminal receipts and their exact input snapshots.
gates=[]
for v in notes['checks']+notes['final_administration_checks']:
 rp=v['receipt']['path'] if isinstance(v['receipt'],dict) else v['receipt'];q=J(rp);assert q['exit_code']==0 and q['terminal_closed'];bind(pin(rp))
 if isinstance(v['receipt'],dict):bind(v['receipt'])
 else:assert pin(rp)['raw_sha256']==v['receipt_raw_sha256']
 bind(q['stdout']);bind(q['stderr'])
 for pair in q['input_snapshots']:
  bind(pair['original'],pair['exact_raw_snapshot']['path'],'root native pre-child exact input');bind(pair['exact_raw_snapshot']);bind(pair['LF_snapshot'])
 gates.append(dict(label=v['label'],actual_PID=q['actual_foreground_pid'],exit_code=0,receipt=pin(rp),stdout=q['stdout'],stderr=q['stderr']))
assert len(gates)==19
mandatory=path(gates[0]['stdout']['path']).read_text(encoding='utf8');assert '9169' in mandatory and '9463' in mandatory and ('507' in mandatory)
for slug,decl in zip(plan['slugs'],plan['mathematical_declarations']):
 ap=ROOT/'research-wiki/semantic-roundtrip/audits'/f"{plan['audit_ids'][plan['slugs'].index(slug)]}.json";a=J(ap);assert a['state']=='accepted' and a['source_review']['state']=='accepted';bind(pin(ap))
 p=ROOT/'website/content/publications'/f'{slug}.json';bind(pin(p));bind(pin(ROOT/'website/content/declaration_lessons'/f'{slug}.json'))
for v in notes['cell_administration_updates']:
 bind(v['before']);bind(v['after'],frozen.get(path(v['after']['path']).as_posix()))
 before=J(v['before']['path']);after=gj(v['after']['path']);assert after['status']=='independently_verified';assert after['evidence']['serialized_shared_gate']=='PASS'
 def diff(a,b,p=''):
  if isinstance(a,dict) and isinstance(b,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))],[])
  return [] if a==b else [dict(pointer=p,before=a,after=b)]
 v['reviewed_exact_diffs']=diff(before,after)
shared={p:original_bytes(p).decode() for p in ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean']}
assert 'import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique' in shared['AutoSamplingTheory/TechnicalLemmas.lean'];assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique' in shared['AutoSamplingTheory/ExampleCases.lean'];assert 'import Tests.ProximalBPSRealDefectRootUnique' in shared['Tests.lean'];assert 'formalizedTechnicalLemmaCount = 507' in shared['Tests/Basic.lean']
for name in ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean']:assert not re.search(r'^\s*(theorem|def|axiom|lemma)\s',shared[name],re.M)
for d in plan['mathematical_declarations']:assert shared['AutoSamplingTheory/TechnicalLemmas/Registry.lean'].count('localDecl := "'+d+'"')==1
for q in J(exact/'inputs.before.json')['mathematical_freeze'][:3]:
 b=path(q['path']).read_bytes();assert b==subprocess.check_output(['git','show',SCI+':'+path(q['path']).relative_to(ROOT).as_posix()],cwd=ROOT);assert b==subprocess.check_output(['git','show',INT+':'+path(q['path']).relative_to(ROOT).as_posix()],cwd=ROOT)
 for word in ['sorry','admit','axiom']:assert not re.search(r'\b'+word+r'\b',re.sub(r'--[^\n]*','',b.decode()))
 assert not (path(q['path']).as_posix().startswith((ROOT/'AutoSamplingTheory').as_posix()) and re.search(r'^import Tests',b.decode(),re.M))
diagnosis=J(R/'integration62/staging-whitespace/diagnosis.json');assert len(diagnosis['findings'])==374 and len(diagnosis['exact_immutable_raw_paths'])==38 and diagnosis['full_staged_exit']==2 and diagnosis['authored_complement_exit']==0 and not diagnosis['full_staged_called_PASS']
gz=R/'integration62/staging-whitespace/full-staged-immutable-negative.raw.gz';assert H(gzip.decompress(gz.read_bytes()))==diagnosis['negative_raw_sha256'];bind(pin(gz));bind(pin(R/'integration62/staging-whitespace/diagnosis.json'))
for q in diagnosis['exact_immutable_raw_paths']:bind(pin(q),'','exact native whitespace debt')
W(P/'history.maps.json',dict(status='PASS',maps=maps,source_audit_maps='Native source original31 excludes canonical audits; exact62 four administrative-stage snapshots retained separately. No new source input fallback.',root_cell_admin_diffs=notes['cell_administration_updates']))
W(P/'repository.checks.json',dict(status='PASS',science=SCI,integration=INT,gates=gates,gates_count=19,root_jobs=9169,Test_jobs=9463,Registry=507,production_inventory=J(P/'integration.tree.index.json')['production_module_count'],unchanged_exact62_science=True,exact_review_run=prior['run_sha256'],native_source_run=native['source_run_sha256'],decoder_whole_raw=native['decoder_whole_raw_sha256'],source_identity_separation=native['source_identity_separation'],shared_imports_declaration_free=True,production_Test_imports=False,whitespace=dict(findings=374,exact_paths=38,lossless_raw_negative=diagnosis['negative_raw_sha256'],authored_complement_PASS=True,full_staged_PASS=False),claimed63='Tracked source-first preproof/claim only. No63 production in exact integration tree; later private/new files excluded. No63 proof credit.',preserved_cards=67,restored_unrelated_paths=84,remaining=notes['remaining']))
W(P/'review.inputs.json',dict(count=len(rows),rows=rows,finite_exact_maps=pin(P/'history.maps.json')))
print('REPOSITORY62_PASS',len(rows),'unique qualified pins',len(gates),'native terminal gates')
