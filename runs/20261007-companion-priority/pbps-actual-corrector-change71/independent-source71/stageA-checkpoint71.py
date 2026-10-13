import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,datetime,os
O=pathlib.Path(__file__).resolve().parent; B=pathlib.Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def write(n,x):
 with (O/n).open('xb') as f:f.write((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
bundle=json.loads((O/'stageA.complete-named-expectations-input-payload71.json').read_bytes())
for q in bundle['frozen_RAW_pins']:
 p=B/q['path']; assert sha(p.read_bytes())==q['RAW_sha256']
inventory=json.loads((O/'stageA.primary255.reparsed-inventory.json').read_bytes())['items']
coverage=json.loads((O/'stageA.primary255-NODE-EXCLUDED71.before-current-BODY.frozen.json').read_bytes())
assert len(coverage['entries'])==len(inventory)==255 and coverage['counts']=={'NODE':144,'EXCLUDED':111}
g=json.loads((O/'stageA.source-proof-graph71.before-current-BODY.frozen.json').read_bytes());ids={n['id'] for n in g['nodes']}
assert len(ids)==22 and len(g['edges'])==49
assert all(e['parent'] in ids and e['child'] in ids for e in g['edges'])
assert all(e['reason'] and e['classification'] in ['NODE','EXCLUDED'] and all(n in ids for n in e['source_nodes']) for e in coverage['entries'])
lookup={x['math_id']:x for x in inventory}
for x in coverage['entries']:
 assert all(x[k]==lookup[x['math_id']][k] for k in ['RAW_full_start','RAW_full_end_exclusive','math_RAW_sha256','formula_latex'])
for n in g['nodes']:
 for x in n['current_four_region_RAW_anchors']:assert x==lookup[x['math_id']]
for x in inventory:
 b=(O/('stageA.source.'+x['region']+'.RAW.html')).read_bytes()[x['RAW_region_start']:x['RAW_region_end_exclusive']]
 assert len(b)==x['math_RAW_bytes'] and sha(b)==x['math_RAW_sha256']
terminal=[]
for p in sorted(O.glob('*.terminal-receipt.json')):
 r=json.loads(p.read_bytes())
 for k in ['stdout','stderr']:
  q=r[k];b=(O/q['name']).read_bytes();assert sha(b)==q['RAW_sha256'] and len(b)==q['RAW_bytes']
 terminal.append({'receipt':pin(p),'actual_pid':r['actual_pid'],'exit_code':r['exit_code']})
old=[]
for name,expect in [('independent-repository-reader70','44e6685c07f449a5f5a3ee8f697187394775ab507b707992735a105c4653e0c6'),('independent-generated-whitespace70','d920055d33f4b70bec5aed916cdf9ca14a90cad13d115f8c6a086c1eb3a8045e')]:
 d=B/'runs/20261007-companion-priority/pbps-actual-projected-rotation70'/name
 assert sha((d/'lease.final.json').read_bytes())==expect
 old.extend([pin(d/'lease.final.json'),pin(d/'owned-manifest.json')])
run={'schema':'source71-stageA-expectation-freeze-run-v1','actor':'/root/independent_primary69','stage':'A_SOURCE_ONLY','status':'STAGE_A_FROZEN_STAGE_B_OPEN','primary_RAW_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','expectations':pin(O/'stageA.source-expectations71.before-current-BODY.frozen.json'),'graph':pin(O/'stageA.source-proof-graph71.before-current-BODY.frozen.json'),'coverage':pin(O/'stageA.primary255-NODE-EXCLUDED71.before-current-BODY.frozen.json'),'named_payload':pin(O/'stageA.complete-named-expectations-input-payload71.json'),'source_math_count':255,'NODE':144,'EXCLUDED':111,'nodes':22,'edges':49,'target_formulas':18,'obligations':24,'exposure':pin(O/'stageA.anti-anchoring-exposure71.frozen.json'),'terminal_receipts':terminal,'old213_32_lease_manifest_pins_only_no_recursive_payload':old,'whole_logical_recipe':'Canonical sorted compact UTF8 JSON deleting ONLY top-level run_sha256.','current71_BODY_or_new_publication_or_decoder_or_verdict_read':False,'final_source_review_or_SAU_credit':False}
run['run_sha256']=sha(canon(run));write('stageA.freeze.run71.json',run)
manifest=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
write('stageA.owned-finite-manifest71.json',{'schema':'source71-stageA-finite-OPEN-checkpoint-manifest-v1','owned_count_before_this_manifest':len(manifest),'files':manifest,'entries_canonical_sha256':sha(canon(manifest)),'LF_recipe':'ONLY CRLF byte pairs to LF.','scope':'All owned files at StageA snapshot, including helpers, failed terminals and complete named expectation payload; StageB may add new files, frozen StageA files cannot change.','self_policy':'This manifest and following OPEN checkpoint are separate finite binding layers. Not a final CLOSED lease.'})
write('stageA.OPEN-checkpoint71.json',{'schema':'source71-stageA-OPEN-checkpoint-v1','status':'OPEN_STAGE_B_NOT_AUTHORIZED_YET','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':pin(O/'stageA.freeze.run71.json'),'manifest':pin(O/'stageA.owned-finite-manifest71.json'),'owned_count_including_manifest_and_this_checkpoint':len(manifest)+2,'frozen_StageA_immutable':True,'current71_BODY_unread':True,'final_CLOSED_LAST_lease':'Deferred until authorized StageB whole review concludes.','no_canonical_Git_ledger_Goal_or_old_closed_writes':True})
print(json.dumps({'actual_pid':os.getpid(),'status':'PASS_STAGE_A_OPEN_CHECKPOINT','run_whole_logical':run['run_sha256'],'run':pin(O/'stageA.freeze.run71.json'),'manifest':pin(O/'stageA.owned-finite-manifest71.json'),'checkpoint':pin(O/'stageA.OPEN-checkpoint71.json'),'terminal_history':[(x['actual_pid'],x['exit_code']) for x in terminal]},ensure_ascii=False,indent=2))
