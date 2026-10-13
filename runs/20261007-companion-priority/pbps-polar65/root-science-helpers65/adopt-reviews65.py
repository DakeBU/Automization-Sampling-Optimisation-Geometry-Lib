from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-polar65'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def new(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def logical(x):return sha(json.dumps({k:v for k,v in x.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def smallpin(p,x):
 b=p.read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'],p
 assert len(lf(b))==x['lf_bytes'] and sha(lf(b))==x['lf_sha256'],p
def largepin(p,x):
 b=p.read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'],p
 assert sha(lf(b))==x['LF_sha256'],p
 return b
d=r/'independent-math65';lease=load(d/'lease.final.json');run=load(d/'run.json')
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['final_owned_file_count']==40
assert sha((d/'lease.final.json').read_bytes())=='d73a560e8bd41f1da72b974d24714e5619820e5305fe24cb8268f32ccf533269'
assert logical(run)==run['run_sha256']==lease['whole_logical_run_sha256']=='2db94e72f30373264f39eec3e41e5e58d58f90c9655340013e2785ef1c3686f5'
assert sha((d/'mathematical-review.named.raw.json').read_bytes())==lease['complete_named_RAW_review_sha256']=='c45d5f8543270a64bc1fd26d475011eef4dc76e390f8b5c195acd6f94120900c'
listed={Path(x['path']).resolve().relative_to(d.resolve()).as_posix() for x in lease['all_owned_except_this_final_lease']}|{'lease.final.json'}
assert listed=={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} and len(listed)==40
for x in lease['all_owned_except_this_final_lease']:smallpin(Path(x['path']),x)
inputs=load(d/'inputs.manifest.json');assert len(inputs['inputs'])==191 and len(inputs['finite_historical_resolutions'])==1
for x in inputs['inputs']:smallpin(Path(x['resolved_path']),x)
fr=inputs['finite_historical_resolutions'][0]
assert fr['claimed_RAW_sha256']=='c9e6d896c543e0eaf7841db6852f1be3bae32886788221139923bf62b5e18763'
assert Path(fr['resolved_exact_RAW_snapshot']['path'])==r/'audit.0.before-decoder.exactraw.snapshot.json'
focused=load(d/'focused.result.json');checks=load(d/'checks.result.json');math=load(d/'mathematical-review.json')
assert focused['exit_code']==0 and focused['terminal_closed'] and focused['actual_foreground_lake_pid']==23980 and focused['jobs']==3945
assert focused['all_inputs_RAW_LF_unchanged'] and len(focused['standard3_declarations'])==2
assert checks['status']=='PASS' and checks['all5_literal_BODY_matches'] and len(checks['literal_BODY_steps'])==5
assert math['verdict']==run['verdict']=='ACCEPT_BOUNDED_PRECOMMIT_MATHEMATICS_AND_LITERAL_PRESENTATION'
for x in checks['literal_BODY_steps']:
 p=root/('AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean' if x['step']<=3 else 'Tests/ProximalBPSPolarIsometry.lean')
 b=p.read_bytes();span=b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']])
 assert sha(b)==x['whole_source_RAW_sha256'] and sha(span)==x['literal_BODY_span_RAW_sha256'] and len(span)==x['literal_BODY_bytes']
new(r/'root.math65.adoption.json',dict(status='INDEPENDENT_PRECOMMIT_MATHEMATICS65_ACCEPTED',actual_root_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_review_sha256=lease['complete_named_RAW_review_sha256'],native_owned_files=40,finite_inputs=191,literal_BODY_steps=5,fresh_foreground_lake_pid=23980,focused_exit=0,source_verdict_consumed=False,exact_commit_verification=False,remaining='Separate source admission, exact SCI65 verification, serialized integration and reader acceptance; no ambient B* extraction, onto or whole-paper credit.'))
d=r/'independent-source65';lease=load(d/'lease.final.json');run=load(d/'review-run.json');decision=load(d/'semantic-decision.json');manifest=load(d/'owned-manifest.json');index=load(d/'closure-index.json')
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count']==117
assert sha((d/'lease.final.json').read_bytes())=='3072596febc801ac0a25c016ff9750c62dc6ac1703219839dd6dfe1813efb057'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='ec13793f60dd53d3939b73142003d2c806b2469328b10b7da43ed491d17a65f5'
assert logical(run)==run['run_sha256']==lease['whole_logical_run_sha256']=='0953d659a767b3ff2cd9651906820e3301f7718bbd0833e97423523e84aa05cc'
assert set(manifest['all_owned_file_names'])=={p.name for p in d.iterdir()} and len(manifest['files'])==115
for x in manifest['files']:largepin(d/x['name'],x)
for k,expected in [('COMPLETE_RAW_DECISION','9eef9b5d2eea4e8d9bf174d8db7477639815193483a6c83c2cee693bb4a2ef5d'),('COMPLETE_RAW_REVIEW','bf80df665f6fe9f18b169e3d314dc61fdd08e4f75ce79a786679ec3fcd4769cc'),('SEPARATE_COMPLETE_RAW_INPUT','bb1fd7022c21a63b19d490076a5d7adb39562d4b39b26d7bc51d54f7547f9c25')]:
 x=index[k];largepin(d/x['name'],x);assert x['RAW_sha256']==expected
payload=load(d/'RAW-input-payload.json');assert len(payload['finite_exact_RAW_inputs'])==32
for x in payload['finite_exact_RAW_inputs']:
 b=largepin(d/x['name'],x);assert b==x['utf8'].encode('utf-8')
for block in payload['RAW_LF_maps']:
 for x in block['inputs']:
  b=largepin(d/x['RAW_snapshot'],x);assert (d/x['LF_snapshot']).read_bytes()==lf(b)
coverage=load(d/'source-coverage-audit.json');body=load(d/'literal-BODY-excerpts-audit.json')
assert coverage['math_items']==coverage['classified']==280 and coverage['missing']==coverage['annotation_mismatch']==0
assert body['all_five'] and len(body['spans'])==5
for x in body['spans']:
 b=(root/x['path']).read_bytes();lo,hi=x['raw_byte_range_end_exclusive'];assert sha(b)==x['source_RAW_sha256'] and sha(b[lo:hi])==x['RAW_sha256']
assert decision['review_run_sha256']==run['run_sha256'] and decision['verdict']=='equivalent-after-elaboration'
assert not decision['deltas'] and not decision['repairs'] and not decision['source_mathematical_repair']
assert decision['independent_from_decoder'] and decision['independent_from_formalizer']
assert len(decision['semantic_slots'])==7 and all(x['relation']!='not-audited' and x['evidence'] for x in decision['semantic_slots'].values())
assert decision['publication_binding_sha256']=='8df52ffc1447a016899dba2efc92163940a8e0048aa1a44215257d674e449319'
assert decision['current_publication_context_sha256']=='0cbc76b50d7a0d574a146b8d4136c537c5e940e218d1e53fc68244b1b3dc8fd8'
for k in ['actual_finalizer_exit','actual_readback_exit','actual_close_validator_exit']:assert lease[k]==0
new(r/'root.source65.adoption.json',dict(status='INDEPENDENT_SOURCE65_ACCEPTED_SELECTED_B16_AND_TYPED_CONSUMER',actual_root_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_review_sha256=index['COMPLETE_RAW_REVIEW']['RAW_sha256'],native_complete_RAW_decision_sha256=index['COMPLETE_RAW_DECISION']['RAW_sha256'],separate_complete_RAW_input_sha256=index['SEPARATE_COMPLETE_RAW_INPUT']['RAW_sha256'],native_owned_files=117,finite_inputs=32,source_items=280,literal_BODY_steps=5,publication_binding_sha256=decision['publication_binding_sha256'],current_publication_context_sha256=decision['current_publication_context_sha256'],source_mathematical_repair=False,accepted_scope=decision['source_admission'],full_Exposition=False,PURIFIED=False,Goal_complete=False))
print('PASS CLOSED math65:40 owned/191 inputs/3945/5 BODY; source65:117 owned/32 exact RAW inputs/280 items/5 BODY/seven slots. Native bytes unchanged.')
