import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
run=json.loads((O/'stageA.freeze.run72.json').read_bytes());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
for q in run['records']:
 b=(B/q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
primary=json.loads((O/'stageA.primary-input-manifest72.json').read_bytes());raw=(B/primary['primary']['path']).read_bytes();assert sha(raw)==primary['primary']['RAW_sha256']
for x in primary['regions']:
 b=raw[x['RAW_start']:x['RAW_end_exclusive']];assert b==(O/x['snapshot']).read_bytes() and b.replace(b'\r\n',b'\n')==(O/x['LF_snapshot']).read_bytes() and sha(b)==x['RAW_sha256']
prior=json.loads((O/'stageA.prior71-readonly-pins72.json').read_bytes())
for q in prior['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
cov=json.loads((O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json').read_bytes());assert cov['primary_four_region_count']==len(cov['primary_entries'])==255 and cov['supplemental_unique_count']==len(cov['supplemental_entries'])==106 and cov['unclassified']==0
for x in cov['primary_entries']+cov['supplemental_entries']:assert x['classification'] in {'NODE','EXCLUDED'} and x['reason'] and sha(raw[x['RAW_start']:x['RAW_end_exclusive']])==x['RAW_sha256']
graph=json.loads((O/'stageA.source-proof-graph72.before-header.frozen.json').read_bytes());assert len(graph['nodes'])==24 and len(graph['edges'])==53 and not graph['generic_leaf_has_B21_dependency']
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()];manifest={'schema':'source72-StageA-OPEN-finite-checkpoint-manifest-v1','owned_count_before_this_manifest':len(files),'files':files,'entries_canonical_sha256':sha(canon(files)),'closure_status':'OPEN; StageA source expectations frozen,72 header unread; current wrapper writes its3 receipt/log files after this checkpoint,all must join eventual complete CLOSED manifest.'};write('stageA.owned-finite-manifest72.json',manifest)
record={'schema':'source72-StageA-OPEN-checkpoint-v1','actual_pid':os.getpid(),'status':'OPEN_STAGEA_SOURCE_EXPECTATIONS_FROZEN_AWAITING_ROOT_HEADER','run_whole_logical_sha256':run['run_sha256'],'expectations':pin(O/'stageA.source-expectations72.before-header.frozen.json'),'graph':pin(O/'stageA.source-proof-graph72.before-header.frozen.json'),'coverage':pin(O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json'),'named_payload':pin(O/'stageA.complete-named-expectations-input-payload72.json'),'manifest':pin(O/'stageA.owned-finite-manifest72.json'),'manifest_file_count':len(files),'all_exact_RAW_LF_and_old71pins_verified':True,'future72header_proposal_otheragent_sourceplan_unread':True,'sourceblind':False,'no_proof_compile_claim_source_admission_orVERIFIED':True,'no_canonical_Git_ledger_Goal_oldCLOSEDwrites':True};write('stageA.OPEN-checkpoint72.json',record);print(json.dumps(record,indent=2))
