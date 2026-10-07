from pathlib import Path
import json,hashlib,subprocess,sys,datetime
sys.path.insert(0,'tools')
import astis_publication as pub
R=Path('runs/20261007-companion-priority/gaussian-flip-energy');O=R/'dependency-metadata-overlay1';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def pin(r,p=None):
 x=d(p or r['path']);assert x['raw_sha256']==r['raw_sha256'] and x['lf_sha256']==r['lf_sha256'],(x,r);return x
def put(p,x):assert not p.exists(),p;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
def dif(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else dif(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in dif(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
repair=j(O/'repair.json');assert not repair['mathematical_repair'] and len(repair['changes'])==2
inputs=[d(O/'repair.json')]
for row,name in zip(repair['changes'],['lesson.before.raw.snapshot.json','audit.before.raw.snapshot.json']):
 pin(row['before'],O/name);pin(row['after']);inputs += [d(O/name),d(row['path'])]
lessonpath=Path(repair['changes'][0]['path']);auditpath=Path(repair['changes'][1]['path']);before_l=j(O/'lesson.before.raw.snapshot.json');current_l=j(lessonpath);before_a=j(O/'audit.before.raw.snapshot.json');current_a=j(auditpath)
assert dif(before_l,current_l)==['/units/0/mathlib_dependencies/13']
assert before_l['units'][0]['mathlib_dependencies'][13]=='Filter.tendsto_inv_atTop_zero' and current_l['units'][0]['mathlib_dependencies'][13]=='tendsto_inv_atTop_zero'
assert lessonpath.read_bytes()==(O/'lesson.before.raw.snapshot.json').read_bytes().replace(b'Filter.tendsto_inv_atTop_zero',b'tendsto_inv_atTop_zero',1)
assert dif(before_a,current_a)==['/publication_binding_sha256','/publication_context/lesson/mathlib_dependencies/13']
packetpath=R/'source.0.reviewer-packet.overlay1.json';oldpacketpath=R/'source.0.reviewer-packet.json';packet=j(packetpath);oldpacket=j(oldpacketpath)
packetdiff=dif(oldpacket,packet);assert packetdiff==['/candidate_publication_context/lesson/mathlib_dependencies/13','/packet_sha256','/publication_binding_sha256']
for p in [packet,oldpacket]:assert pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert packet['lean']==oldpacket['lean'] and packet['source']==oldpacket['source'] and packet['blind_reconstruction']==oldpacket['blind_reconstruction']
data=pub.inputs();item=next(i for i in pub.load() if i['id']=='gaussian-compact-full-flip-energy');decl=packet['lean']['declaration'];b=next(x for x in item['bindings'] if x['declaration']==decl)
assert pub.binding_digest(item,b,data)==packet['publication_binding_sha256']==current_a['publication_binding_sha256'] and pub.review_context(item,b,data)==packet['candidate_publication_context']==current_a['publication_context']
api=Path('.lake/packages/mathlib/Mathlib/Topology/Algebra/Order/Field.lean');lines=api.read_bytes().splitlines(keepends=True);assert lines[73].decode().startswith('theorem tendsto_inv_atTop_zero :')
assert not any(x.decode().strip().startswith('namespace ') for x in lines[:74])
assert b'theorem Filter.tendsto_inv_atTop_zero' not in api.read_bytes()
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
apiregion=O/'reviewer.overlay1.api.Field.55-78.raw.snapshot';assert not apiregion.exists();apiregion.write_bytes(b''.join(lines[54:78]));inputs += [d(api),d(apiregion)]
sourcepath=R/'source.0.review.json';s=j(sourcepath);assert d(sourcepath)['raw_sha256']=='4da60ac71132deed2da980e3beafb86a8293205f623053ced7d205b7d4fdeaba'
assert s['status']=='BLOCKED_METADATA_ONLY_PUBLICATION_PROVENANCE' and s['blocking'] and s['mathematical_semantic_verdict']=='equivalent-after-elaboration'
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']
drifts=[]
for row in s['input_artifacts']:
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  assert row['path'] in {lessonpath.as_posix(),auditpath.as_posix()};drifts.append(row['path'])
 else:pin(row)
assert len(s['input_artifacts'])==83 and len(drifts)==2
for row in s['supporting_input_artifacts']:
 pin(row);pin(row,R/row['raw_snapshot']);assert (R/row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
math=j(R/'whole-proof-review/math.review.json');mathbinding=j(math['input_bindings']['path']);assert len(mathbinding['inputs'])==42
for row in mathbinding['inputs']:pin(row)
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==27
for row in freeze['inputs']:pin(row)
publication=Path('website/content/publications/gaussian-compact-full-flip-energy.json');assert publication.as_posix() in [x['path'] for x in s['input_artifacts']]
assert pub.digest(current_l['units'][0].get('steps',[]))==pub.digest(before_l['units'][0].get('steps',[]))
inputs += [d(packetpath),d(oldpacketpath),d(sourcepath),d(publication),d(R/'whole-proof-review/math.review.json'),d(math['input_bindings']['path'])]
snapshotrows=[]
for i,row in enumerate(inputs):
 p=Path(row['path']);a=O/f'reviewer.overlay1.input.{i:03}.raw.snapshot';b=O/f'reviewer.overlay1.input.{i:03}.lf.snapshot';assert not a.exists();a.write_bytes(p.read_bytes());b.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'));snapshotrows.append(dict(row,reviewer_raw_snapshot=a.as_posix(),reviewer_lf_snapshot=b.as_posix()))
binding=put(O/'reviewer.overlay1.bindings.json',{'actor':V,'inputs':snapshotrows,'original_source83_stable_except_exact2metadata_files':True,'source_support3_rawLF_unchanged':True,'original_math27_unchanged':True,'wholemath42_unchanged':True,'source_packet_exact_pointers':packetdiff,'current_review_context_sha256':pub.digest(packet['candidate_publication_context'])})
review={'schema_version':1,'status':'ACCEPTED_SCOPED_METADATA_ONLY_REPAIR_OVERLAY','verdict':'accepted-scoped-metadata-only','blocking':False,'reviewer':V,'independent_from_root_repair_creator':True,'scope':'Exact one declaration-name provenance fix only. No mathematical/source-premise repair, no source admission or VERIFIED.','proposal':d(O/'repair.json'),'exact_lesson_delta':['/units/0/mathlib_dependencies/13'],'old':'Filter.tendsto_inv_atTop_zero','new':'tendsto_inv_atTop_zero','actual_pinned_API':{'path':d(api),'line':74,'region':d(apiregion),'namespace':'global; open Filter imports names but does not introduce namespace','assumptions':'Ordered semifield/order topology; actual Real instantiates these. Function reciprocal tends0 at positive infinity.','actual_production_call':'Unqualified tendsto_inv_atTop_zero.comp (Real.tendsto_sqrt_atTop.comp successor_natCast_limit), unchanged and already independently compiled.'},'exact_audit_delta':['/publication_binding_sha256','/publication_context/lesson/mathlib_dependencies/13'],'exact_packet_delta':packetdiff,'packet':d(packetpath),'packet_sha256':packet['packet_sha256'],'current_publication_binding_sha256':packet['publication_binding_sha256'],'current_context_sha256':pub.digest(packet['candidate_publication_context']),'original_blocked_source_review':{'receipt':d(sourcepath),'status':s['status'],'review_run_sha256':s['review_run_sha256'],'mathematical_semantic_verdict':s['mathematical_semantic_verdict'],'remains_BLOCKED_original':True},'all_statement_proof_Test_source_assumptions_formula_steps_decoder_unchanged':True,'raw_lesson_exact7byte_namespace_prefix_removal':True,'original_math_freeze27_and_wholemath42_unchanged':True,'83_source_inputs_81_unchanged_2exactmetadata_projection':True,'input_bindings':binding,'EXCESS':[],'deltas':[],'mathematical_repairs':[],'source_acceptance':False,'VERIFIED_transition':False,'compiler_started':False,'no_new_mathematical_credit':True,'remaining_boundary':['Distinct source reviewer must independently admit the rebound current packet; original BLOCKED receipt is not overwritten or made accepted by this overlay.','Exact commit verification/shared integration/GaussianLSI/noncompact/Hilbert/T2/main/cost remain separate.'],'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
review['review_run_sha256']=pub.digest(review)
saved=put(O/'overlay1.review.json',review)
put(O/'reviewer.overlay1.lease.json',{'status':'CLOSED','actor':V,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','compiler_started':False,'Python':'CLOSED','review':saved,'review_run_sha256':review['review_run_sha256'],'canonical_mutations':False})
print(json.dumps({'status':review['status'],'receipt':saved,'review_run_sha256':review['review_run_sha256'],'all_leases':'CLOSED'},ensure_ascii=False))
