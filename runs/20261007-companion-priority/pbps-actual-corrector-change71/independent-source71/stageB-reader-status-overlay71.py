import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,copy,ast,itertools
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent;S=R/'reader-status-overlay71'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def diffs(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  assert set(a)==set(b)
  return [q for k in a for q in diffs(a[k],b[k],path+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b)
  return [q for k,(x,y) in enumerate(zip(a,b)) for q in diffs(x,y,path+'/'+str(k))]
 return [] if a==b else [path]
proposal=json.loads((S/'proposal.json').read_bytes());mapping=json.loads((S/'packet-mapping.json').read_bytes())
old='Independent review, integration, full Exposition and PURIFIED remain pending.'
new='B21 alone establishes no full Exposition, PURIFIED, main/live, whole-paper or Goal completion.'
assert proposal['before']==old and proposal['after']==new
expected=[['/items/0/bindings/0/boundary','/items/0/purification/scope'],['/units/0/boundary'],['/purification/scope']]
inputs=[];rows=[]
files=[S/'proposal.json',S/'packet-mapping.json']
for i,row in enumerate(proposal['rows']):
 bp=S/f'{i}.before.exactraw.json';ap=S/f'{i}.proposed.json';before=bp.read_bytes();after=ap.read_bytes();current=(B/row['path']).read_bytes()
 assert before==current and sha(before)==row['before_RAW_sha256'] and sha(after)==row['proposed_RAW_sha256']
 bj=json.loads(before);aj=json.loads(after)
 assert diffs(bj,aj)==expected[i]
 for path in expected[i]:
  x=bj;y=aj
  for key in path.lstrip('/').split('/'):
   x=x[int(key)] if isinstance(x,list) else x[key];y=y[int(key)] if isinstance(y,list) else y[key]
  assert x.count(old)==1 and y==x.replace(old,new)
 # Other exact occurrences are historical source_history_boundary strings and stay unchanged.
 parts=before.split(old.encode());matched=[]
 for selected in itertools.combinations(range(len(parts)-1),len(expected[i])):
  candidate=parts[0]
  for k,part in enumerate(parts[1:]):candidate+=(new.encode() if k in selected else old.encode())+part
  if candidate==after:matched.append(selected)
 assert len(matched)==1
 files.extend([bp,ap]);rows.append({'current_path':row['path'],'before':pin(bp),'proposed':pin(ap),'JSON_changed_paths':expected[i],'only_exact_sentence_bytes_replaced':True,'occurrences':len(expected[i]),'replaced_RAW_occurrence_indices':matched[0],'other_historical_occurrences_preserved':len(parts)-1-len(expected[i])})
packet0=json.loads((R/'source-review.packet.0.json').read_bytes());packet1=json.loads((S/'source-review.packet.1.proposed.json').read_bytes())
assert sorted(diffs(packet0,packet1))==['/packet_sha256','/publication_binding_sha256']
for p in [packet0,packet1]:assert sha(canon({k:v for k,v in p.items() if k!='packet_sha256'}))==p['packet_sha256']
assert packet1['packet_sha256']==mapping['proposed_official_packet_sha256']
assert mapping['proposal_RAW_sha256']==sha((S/'proposal.json').read_bytes())
module=B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'
assert sha(module.read_bytes())=='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a'
sys.path.insert(0,str(B/'tools'));sys.path.insert(0,str(B/'website/scripts'))
import astis_site as base
import astis_publication as publication
import astis_semantic_roundtrip_core as core
base.project_lean_paths=lambda:[module]
_,ds=base.scan_project_sources();declarations={d.full_name:d for d in ds}
name=packet0['lean']['declaration'];pub0=json.loads((S/'0.before.exactraw.json').read_bytes())['items'][0];pub1=json.loads((S/'0.proposed.json').read_bytes())['items'][0]
lesson0=json.loads((S/'1.before.exactraw.json').read_bytes())['units'][0];lesson1=json.loads((S/'1.proposed.json').read_bytes())['units'][0]
data0={'declarations':declarations,'lessons':{name:lesson0}};data1={'declarations':declarations,'lessons':{name:lesson1}}
context0=publication.review_context(pub0,pub0['bindings'][0],data0);context1=publication.review_context(pub1,pub1['bindings'][0],data1)
assert context0==context1==packet0['candidate_publication_context']==packet1['candidate_publication_context']
binding0=publication.binding_digest(pub0,pub0['bindings'][0],data0);binding1=publication.binding_digest(pub1,pub1['bindings'][0],data1)
assert binding0==packet0['publication_binding_sha256']==proposal['old_publication_binding_sha256']
assert binding1==packet1['publication_binding_sha256']==proposal['proposed_publication_binding_sha256']
audit0path=B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json';audit0=json.loads(audit0path.read_bytes());audit1path=S/'audit.1.proposed.json';audit1=json.loads(audit1path.read_bytes())
assert core.semantic_reviewer_packet(audit0)==packet0 and core.semantic_reviewer_packet(audit1)==packet1
files.extend([S/'source-review.packet.1.proposed.json',audit1path,R/'source-review.packet.0.json',audit0path,module])
for i,p in enumerate(files):
 b=p.read_bytes();raw=f'stageB.reader-overlay.input.{i:02}.exactraw.snapshot';lf=f'stageB.reader-overlay.input.{i:02}.LF.snapshot';(O/raw).write_bytes(b);(O/lf).write_bytes(b.replace(b'\r\n',b'\n'));inputs.append({**pin(p),'snapshot':raw,'LF_snapshot':lf})
write('stageB.reader-status-overlay71.input-manifest.json',{'schema':'source71-reader-status-proposal-exact-inputs-v1','LF_recipe':'ONLY byte CRLF to LF; no other normalization','inputs':inputs})
decision={'schema':'source71-independent-exact-reader-status-overlay-decision-v1','actual_pid':os.getpid(),'decision':'accept_exact_reader_status_overlay_only','proposal':pin(S/'proposal.json'),'packet_mapping':pin(S/'packet-mapping.json'),'three_exact_proposed_files':rows,'changed_fields':4,'sentence_replacements':4,'binding_before':binding0,'binding_proposed':binding1,'official_packet_before':packet0['packet_sha256'],'official_packet_proposed':packet1['packet_sha256'],'changed_packet_fields':['publication_binding_sha256','packet_sha256'],'all_other_packet_fields_identical':True,'review_context_canonical_bytes_identical':canon(context0)==canon(context1),'proposed_audit_packet_exact':True,'audit_changed_JSON_paths':diffs(audit0,audit1),'math_statement_formula_BODY_Lean_decoder_unchanged':True,'private_literal_helper_is_not_provider':True,'reason':'Replaces a temporal draft status with a stable strict truth boundary. B21 alone grants no full Exposition/PURIFIED/main/live/whole-paper/Goal completion. This is reader metadata, not mathematical repair or additional source/SCI acceptance.','canonical_changes_by_reviewer':False,'application_authorized_only_for_exact_three_proposed_RAW_hashes_and_derived_exact_audit_packet':True,'root_must_apply_and_freeze_official1_before_final_source_binding':True}
write('stageB.reader-status-overlay71.decision.json',decision)
ast.parse((O/'source.0.author-native71.py').read_text(encoding='utf-8'))
print(json.dumps({'actual_pid':os.getpid(),'status':'ACCEPT_EXACT_READER_STATUS_OVERLAY_ONLY','decision':pin(O/'stageB.reader-status-overlay71.decision.json'),'proposal_RAW_sha256':decision['proposal']['RAW_sha256'],'new_binding':binding1,'new_official_packet_sha256':packet1['packet_sha256'],'author_script_AST_parse':'PASS; not executed pending final official packet'},indent=2))
