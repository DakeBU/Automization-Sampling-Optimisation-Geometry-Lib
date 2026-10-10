import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,copy
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent;S=R/'reader-status-overlay71'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
proposal=json.loads((S/'proposal.json').read_bytes());approval=json.loads((O/'stageB.reader-status-overlay71.decision.json').read_bytes());packetpath=R/'source-review.packet.1.json'
packet=json.loads(packetpath.read_bytes());packet0=json.loads((R/'source-review.packet.0.json').read_bytes())
assert packetpath.read_bytes()==(S/'source-review.packet.1.proposed.json').read_bytes()
assert packet['packet_sha256']==approval['official_packet_proposed'] and packet['publication_binding_sha256']==approval['binding_proposed']
assert sha(canon({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
for i,row in enumerate(proposal['rows']):assert (B/row['path']).read_bytes()==(S/f'{i}.proposed.json').read_bytes()
auditpath=B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json'
assert auditpath.read_bytes()==(S/'audit.1.proposed.json').read_bytes()
paths=[packetpath,R/'source-review.freeze71.v1.json',auditpath,*[B/row['path'] for row in proposal['rows']]]
# Finite root overlay receipts/adoptions are pinned without interpreting any mathematical verdict.
for p in sorted(S.iterdir()):
 if p.is_file() and p.name not in {'proposal.json','packet-mapping.json','source-review.packet.1.proposed.json','audit.1.proposed.json','0.before.exactraw.json','1.before.exactraw.json','2.before.exactraw.json','0.proposed.json','1.proposed.json','2.proposed.json'}:paths.append(p)
for p in sorted(R.glob('*reader*overlay*')):
 if p.is_file():paths.append(p)
inputs=[]
for i,p in enumerate(dict.fromkeys(paths)):
 b=p.read_bytes();raw=f'stageB.final-current.input.{i:02}.exactraw.snapshot';lf=f'stageB.final-current.input.{i:02}.LF.snapshot';(O/raw).write_bytes(b);(O/lf).write_bytes(b.replace(b'\r\n',b'\n'));inputs.append({**pin(p),'snapshot':raw,'LF_snapshot':lf,'version_role':'final current after independently approved reader-status-only overlay'})
write('stageB.final-current-inputs71.json',{'schema':'source71-final-current-exact-inputs-v1','actual_pid':os.getpid(),'LF_recipe':'ONLY byte CRLF to LF; no other normalization','inputs':inputs})
sys.path.insert(0,str(B/'tools'));sys.path.insert(0,str(B/'website/scripts'))
import astis_site as base
import astis_publication as publication
import astis_semantic_roundtrip_core as core
module=B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'
assert sha(module.read_bytes())=='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a'
base.project_lean_paths=lambda:[module]
_,ds=base.scan_project_sources();declarations={d.full_name:d for d in ds};name=packet['lean']['declaration']
pub=json.loads((B/proposal['rows'][0]['path']).read_bytes())['items'][0];lesson=json.loads((B/proposal['rows'][1]['path']).read_bytes())['units'][0];data={'declarations':declarations,'lessons':{name:lesson}};binding=pub['bindings'][0]
assert publication.review_context(pub,binding,data)==packet['candidate_publication_context']==packet0['candidate_publication_context']
assert publication.binding_digest(pub,binding,data)==packet['publication_binding_sha256']
assert core.semantic_reviewer_packet(json.loads(auditpath.read_bytes()))==packet
pubcoverage=copy.deepcopy(pub);pubcoverage['source_proof_coverage']={'source_graph':'independent-current-final','coverage_status':'bounded-source-only'}
assert publication.binding_digest(pubcoverage,binding,data)==packet['publication_binding_sha256'] and publication.review_context(pubcoverage,binding,data)==packet['candidate_publication_context']
allowed={row['path']:row['proposed_RAW_sha256'] for row in proposal['rows']};allowed[auditpath.relative_to(B).as_posix()]=sha((S/'audit.1.proposed.json').read_bytes())
historical=[]
for fn,key in [('stageB.exact-input-manifest71.json','original_path'),('stageB.additional-exact-inputs71.json','path')]:
 for q in json.loads((O/fn).read_bytes())['inputs']:
  p=B/q[key];current=p.read_bytes();snapshot=(O/q['snapshot']).read_bytes();assert sha(snapshot)==q['RAW_sha256'] and len(snapshot)==q['RAW_bytes'];assert (O/q['LF_snapshot']).read_bytes()==snapshot.replace(b'\r\n',b'\n')
  changed=sha(current)!=q['RAW_sha256']
  if changed:assert q[key] in allowed and sha(current)==allowed[q[key]]
  historical.append({'input_path':q[key],'historical_RAW_sha256':q['RAW_sha256'],'current_RAW_sha256':sha(current),'exact_approved_reader_overlay_or_derived_audit':changed,'historical_exact_snapshot_retained':True})
write('stageB.all-input-current-attribution71.json',{'schema':'source71-historical-versus-final-finite-attribution-v1','actual_pid':os.getpid(),'rows':historical,'allowed_changed_paths':allowed,'unmapped_current_drift':0,'StageA_math_source_inputs_and_current_Lean_decoder_unchanged':True})
record={'schema':'source71-final-packet-reader-overlay-binding-v1','actual_pid':os.getpid(),'final_official_packet':pin(packetpath),'final_official_omit_top_packet_sha256':packet['packet_sha256'],'final_official_whole_canonical_packet_sha256':sha(canon(packet)),'final_publication_binding_sha256':packet['publication_binding_sha256'],'old_official0_packet':pin(R/'source-review.packet.0.json'),'old_official0_omit_top_sha256':packet0['packet_sha256'],'exact_independent_overlay_approval':pin(O/'stageB.reader-status-overlay71.decision.json'),'all_three_current_files_match_approved_RAW_proposals':True,'current_audit_exact_approved_proposed_bytes':True,'packet_and_review_context_math_identical_except_binding_hash_self_hash':True,'source_coverage_outside_binding_context_reconfirmed':True,'whole_module_literal_BODIES_formulas_decoder_unchanged':True,'no_canonical_writes':True}
write('stageB.final-packet-and-overlay-binding71.json',record)
print(json.dumps({'actual_pid':os.getpid(),'status':'FINAL_CURRENT_PACKET_AND_EXACT_READER_OVERLAY_BOUND','current_inputs':len(inputs),'old_manifest_inputs':len(historical),'unmapped_drift':0,'official_packet_sha256':packet['packet_sha256'],'packet_RAW_sha256':record['final_official_packet']['RAW_sha256'],'publication_binding_sha256':packet['publication_binding_sha256']},indent=2))
