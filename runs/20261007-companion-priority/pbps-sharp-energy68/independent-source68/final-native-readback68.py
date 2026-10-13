from pathlib import Path
import json,hashlib,os,sys,re,datetime
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
run=read('review-run.json');logical=sha(canon({k:v for k,v in run.items() if k!='run_sha256'}));assert logical==run['run_sha256']
complete=read('complete-RAW-decision.json');assert complete['review_run_sha256']==logical
names=['source.0.decision.json','source.1.decision.json','source.consumer.decision.json'];audits=['ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound','ASTIS-RT-20261009-PBPSSharpCorrectorEnergy','ASTIS-RT-20261009-PBPSSharpModifiedEnergyConsumer']
slotnames={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
for i,n in enumerate(names):
 d=read(n);e=complete['decision_files'][i];assert e['path']==n and e['RAW_sha256']==sha((O/n).read_bytes()) and e['decision']==d;assert d['audit_id']==audits[i];assert d['review_run_sha256']==logical and d['verdict']=='equivalent-after-elaboration' and d['bounded_source_acceptance'];assert set(d['semantic_slots'])==slotnames;assert all(x['original'] and x['reconstructed'] and x['evidence'] and x['relation']!='not-audited' for x in d['semantic_slots'].values());assert not d['blocking_deltas'] and not d['repairs'];assert d['independent_from_formalizer'] and d['independent_from_decoder'];assert not any(d[k] for k in ['own_compiler_started','full_Exposition_Seal','PURIFIED','full_paper_or_Goal_complete','VERIFIED_transition_claim']);base=dict(d);base.pop('review_run_sha256');assert base==run['three_native_decisions_without_external_run_reference'][i]
inputs=read('complete-RAW-input-payload.json');assert len(inputs['entries'])==146
rows=[]
for e in inputs['entries']:
 b=(O/e['raw_snapshot']).read_bytes();lf=(O/e['lf_snapshot']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and len(lf)==e['LF_bytes'] and sha(lf)==e['LF_sha256'] and b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')==lf
 path=Path(e['source_path']);p=path if path.is_absolute() else R/path;current=p.read_bytes();assert current==b, f'CURRENT_INPUT_DRIFT:{p}';rows.append({'input_ordinal':len(rows),'source_path':e['source_path'],'RAW_sha256':sha(current),'current_equals_frozen_RAW':True})
primary=(O/'inputs/000.RAW.snapshot').read_bytes();coverage=read('primary344.readback.json');assert sha(primary)==coverage['source_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';assert len(coverage['items'])==344 and len(coverage['six_regions'])==6 and coverage['missing_items']==0
for e in coverage['items']:
 a,b=e['source_RAW_range_end_exclusive'];assert sha(primary[a:b])==e['RAW_sha256'] and e['classification'] and e['alt_annotation_exact']
for e in coverage['six_regions']:
 a,b=e['source_RAW_range_end_exclusive'];assert len(primary[a:b])==e['RAW_bytes'] and sha(primary[a:b])==e['RAW_sha256']
body=read('eleven-literal-BODY-spans.readback.json');assert len(body['steps'])==11
for s in body['steps']:
 e=s['region'];b=(R/e['path']).read_bytes();assert sha(b)==e['source_raw_sha256'];span=b''.join(b.splitlines(keepends=True)[e['start_line']-1:e['end_line']]);assert sha(span)==e['exact_code_raw_sha256']
limit=read('nonblocking-exposition-limitation-S-T.json');assert limit['missing_explicit_definitions']['S']=='‖u‖²+‖v‖²';assert limit['missing_explicit_definitions']['T']=='‖u−K v‖²+‖K u+v‖² = ‖D u‖²+‖D v‖²';assert not limit['source_or_Lean_mathematical_repair_needed'] and not limit['full_Exposition_Seal'] and not limit['PURIFIED']
compile=read('compile-evidence.scope-readback.json');assert compile['root_compiler_actual_pid']==38372 and compile['root_compiler_authoritative_exit']==0 and compile['matching_current_RAW_inputs']==9 and not compile['all11_compiler_input_current_RAW_pins_equal'] and compile['all3_final_Lean_plus_fixed_toolchain_manifest_RAW_pins_equal'];assert len(compile['exact_three_standard_axiom_outputs'])==3 and sum(e['all_targeted_occurrences'] for e in compile['exact_three_standard_axiom_outputs'])==5
for n,exitcode in [('author68.terminal.json',0),('author68.v2.terminal.json',0),('validation68.v2.terminal.json',1),('validation68.v3.terminal.json',0)]:
 a=read(n);assert a['actual_exit_code']==exitcode and a['foreground'] and not a['detached'];prefix=n.removesuffix('terminal.json');assert sha((O/(prefix+'stdout.RAW.txt')).read_bytes())==a['stdout_raw_sha256'] and sha((O/(prefix+'stderr.RAW.txt')).read_bytes())==a['stderr_raw_sha256']
report={'status':'FINAL_NATIVE_SOURCE_DECISIONS_INPUTS_BODY_AND_LOGICAL_RUN_READBACK_PASS','actual_pid':os.getpid(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'whole_logical_run_sha256':logical,'only_top_level_run_sha256_removed':True,'current_and_frozen_exact_RAW_entries':rows,'entry_count':146,'decisions':3,'semantic_slots':21,'source_items':344,'source_regions':6,'literal_BODY_spans':11,'actual_compiler_pid_reused':38372,'own_compiler_started':False,'full_Exposition_Seal':False,'PURIFIED':False,'no_canonical_writes':True}
write('final-native-readback.json',report);print('FINAL_NATIVE_READBACK_EXIT0',os.getpid(),logical,'146_CURRENT_RAW_MATCH','3_DECISIONS','21_SLOTS','344_ITEMS','11_BODY')
