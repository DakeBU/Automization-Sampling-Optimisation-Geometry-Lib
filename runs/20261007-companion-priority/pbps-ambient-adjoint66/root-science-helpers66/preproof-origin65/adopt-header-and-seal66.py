from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66';d=r/'independent-header66';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def new(p,x):assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease,run,manifest,index=[load(d/n) for n in ['lease.final.json','review-run.json','owned-manifest.json','closure-index.json']]
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count']==97
assert sha((d/'lease.final.json').read_bytes())=='d7a2611c9098217d357ff2062a4ad6f2f2e133f7d0da6df036b11e69c073630c'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='2d6f3b8fef81246756f21b94abc81edda346e2e091eaa93ef0fa3ccf6b61db9f'
assert set(manifest['all_owned_file_names'])=={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}
for x in manifest['files']:
 b=(d/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(lf(b))==x['LF_sha256']
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='b1ee0c043a044b493756e2f4c83286a3a6b5e046e5cf213f14dcc79717b65bec'
for k,expected in [('COMPLETE_RAW_DECISIONS','039b165334fd28382080ad2322e3abf06972013623ac443e8fe38da5ddafddba'),('COMPLETE_RAW_REVIEW','13f3157533f5323497bac7113e5330627d16b98628cf48b5b7acb6b1594fb01c'),('SEPARATE_COMPLETE_RAW_INPUT','39d4f6fedca83da35eeedb0d3808c388a6b2b7dcb8be1783e3f3356530e5b5fd')]:
 x=index[k];b=(d/x['name']).read_bytes();assert sha(b)==x['RAW_sha256']==expected and len(b)==x['RAW_bytes']
payload=load(d/'RAW-input-payload.json');assert len(payload['complete_finite_inputs'])==31
for x in payload['complete_finite_inputs']:
 b=(d/x['RAW_snapshot']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and b==x['utf8'].encode()
 assert (d/x['LF_snapshot']).read_bytes()==lf(b) and sha(lf(b))==x['LF_sha256']
decisions=[load(d/f'decision{i}.json') for i in range(2)];headers=[]
for i,decision in enumerate(decisions):
 p=r/f'header{i}.lean';b=p.read_bytes();assert sha(b)==decision['header_RAW_sha256']
 assert decision['status']=='HEADER_ACCEPTED_TYPE_ELABORATED_BODY_UNIMPLEMENTED' and decision['verdict']=='equivalent-after-elaboration'
 assert len(decision['semantic_slots'])==7 and not decision['deltas'] and not decision['repairs'] and not decision['source_mathematical_repair'] and not decision['proof_acceptance']
 assert decision['review_run_sha256']==logical
 headers.append(dict(path=p.relative_to(root).as_posix(),raw_sha256=sha(b),lf_sha256=sha(lf(b)),native_decision=(d/f'decision{i}.json').relative_to(root).as_posix(),source_header_accepted=True,type_elaborated_body_unimplemented=True))
overlay=load(d/'process-only-overlay.json');assert sha((d/'process-only-overlay.json').read_bytes())=='2d090e73aa2c0ecb834e3b8bceb5079a3d6510160836930c1a487776326e858d'
assert overlay['reviewed_process_only'] and not overlay['source_mathematical_repair'] and overlay['changed_metadata_field_count']==2
before=r/'type-only-process-overlay.before';before.mkdir(exist_ok=False)
for row in overlay['wrapper_syntax_overlays']:
 p=Path(row['source_path']);old=p.read_bytes();assert sha(old)==row['before_RAW_sha256'] and old==(d/row['before_RAW_snapshot']).read_bytes()
 after=(d/row['after_RAW_snapshot']).read_bytes();assert sha(after)==row['after_RAW_sha256'] and after==old.replace(b'  exact ASTIS_UNIMPLEMENTED_BODY66',b'  ASTIS_UNIMPLEMENTED_BODY66',1)
 (before/p.name).write_bytes(old);p.write_bytes(after)
p=Path(overlay['metadata_source_path']);old=p.read_bytes();after=(d/overlay['metadata_after_snapshot']).read_bytes();assert sha(old)==overlay['metadata_before_RAW_sha256'] and sha(after)==overlay['metadata_after_RAW_sha256']
oldj=json.loads(old);newj=json.loads(after);check=json.loads(after)
for i in range(2):
 assert newj['headers'][i]['header_RAW_sha256']==headers[i]['raw_sha256'];check['headers'][i]['header_RAW_sha256']=oldj['headers'][i]['header_RAW_sha256']
assert check==oldj;(before/p.name).write_bytes(old);p.write_bytes(after)
adoption=dict(status='CLOSED_HEADER66_TYPE_ONLY_AND_PROCESS_OVERLAY_ADOPTED',actual_root_pid=os.getpid(),native_owned_files=97,native_run_sha256=logical,native_complete_RAW_review_sha256=index['COMPLETE_RAW_REVIEW']['RAW_sha256'],native_complete_RAW_decisions_sha256=index['COMPLETE_RAW_DECISIONS']['RAW_sha256'],native_separate_RAW_input_sha256=index['SEPARATE_COMPLETE_RAW_INPUT']['RAW_sha256'],finite_inputs=31,headers=headers,reviewed_overlay_applied=True,header_statement_bytes_unchanged=True,actual_owned_typecheck_pids=[33108,41072],typecheck_EXIT1_only_intentional_BODY_unknown_tactic=True,source_mathematical_repair=False,proof_acceptance=False,SAU_claim=False)
new(r/'root.header66.adoption.json',adoption)
new(r/'root.statement-seal66.json',dict(status='STATEMENT66_SEALED_NOT_PROVED_NOT_CLAIMED',headers=headers,source_header_review=(r/'root.header66.adoption.json').relative_to(root).as_posix(),primary_first=(r/'root.primary66.adoption.json').relative_to(root).as_posix(),original_inputs_byte_equal65=True,extra_public_premises=[],rank_zero_and_alpha_eta_one_retained=True,truth_boundary='Actual ambient extension of intrinsic block adjoint and genuine globally centered first-corrector input/norm budget only; no full B20 bound,commutation/B21,halfturn,H1/dynamics/main/errors/expectedcost/composition.',proof_search=False,SAU_claim=False))
print('PASS66 sealed unchanged two v2 headers:97 native files,31 finite RAW inputs,seven slots each;exact reviewed BODY-probe/two-pin overlay applied. TYPE only,no proof/SAU credit.')
