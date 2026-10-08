import pathlib,json,hashlib,datetime
O=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-l2-macroscopic-mean-sourcegraph55')
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def desc(p):
 b=p.read_bytes();return {'path':str(p),'raw_bytes':len(b),'lf_bytes':len(lf(b)),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
def write(n,d):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
slots=json.loads((O/'public-provider-slots.draft.json').read_text(encoding='utf8'))
old=next(x for x in slots if x['id']=='P55.conditionalUnique');oldbefore=dict(old)
old.update({'qualified_id':"ProbabilityTheory.eq_condKernel_of_measure_eq_compProd'",'role':'Weaker per-measurable-set uniqueness, not sufficient alone for whole-kernel AE alignment'})
p=pathlib.Path(old['path']);data=p.read_bytes();lines=data.splitlines(keepends=True)
def newslot(pid,lo,hi,q,role):
 start=sum(map(len,lines[:lo-1]));end=sum(map(len,lines[:hi]));frag=data[start:end];k=frag.find(b':=');frag=frag[:k] if k>=0 else frag
 (O/'public-fragments'/(pid+'.raw.txt')).write_bytes(frag);(O/'public-fragments'/(pid+'.lf.txt')).write_bytes(lf(frag))
 return {'id':'P55.'+pid,'qualified_id':q,'role':role,'path':str(p),'physical_lines1':[lo,hi],'start_utf8_byte0':start,'end_utf8_byte0_exclusive':start+len(frag),'fragment_raw_sha256':sha(frag),'fragment_lf_sha256':sha(lf(frag)),'whole_raw_sha256':sha(data),'whole_lf_sha256':sha(lf(data)),'proof_expanded':False,'body_semantics_expanded':False}
strong=newslot('conditionalUniqueFull',82,84,'ProbabilityTheory.eq_condKernel_of_measure_eq_compProd','Actual finite-kernel whole-kernel AE uniqueness; chosen Markov kernels finite internally')
scope=newslot('conditionalUniqueScope',34,39,None,'Actual StandardBorelSpace/Nonempty and finite-measure inherited slots; E supplies these internally')
slots.extend([strong,scope])
# L2 instance and theorem definition scope were read; restrict successor inner-def fragment to theorem header.
inner=next(x for x in slots if x['id']=='P55.L2Inner');b=pathlib.Path(inner['path']).read_bytes();a=b.splitlines(keepends=True);start=sum(map(len,a[:136]));frag=a[136].split(b':=')[0]
(O/'public-fragments'/'L2Inner-header.raw.txt').write_bytes(frag);(O/'public-fragments'/'L2Inner-header.lf.txt').write_bytes(lf(frag))
innerbefore=dict(inner);inner.update({'physical_lines1':[137,137],'start_utf8_byte0':start,'end_utf8_byte0_exclusive':start+len(frag),'fragment_raw_sha256':sha(frag),'fragment_lf_sha256':sha(lf(frag)),'body_semantics_expanded':False,'role':'MeasureTheory.L2.inner_def actual public theorem header; old anonymous Inner instance and rfl prefix retained as incidental public-definition exposure'})
write('public-provider-slots.current.draft.json',slots)
write('provider-plan.errata.json',{'original_plan_preserved':True,'changes':[{'id':'P55.conditionalUnique','before':oldbefore,'after':old,'reason':'Historical55 selected51-53 actually prime weaker declaration; exact source full uniqueness82-84 now pinned separately'},{'id':'P55.L2Inner','before':innerbefore,'after':inner,'reason':'Narrow to actual theorem137 header; retain original draft fragment exposure without using rfl proof'}],'additional_slots':[strong,scope],'candidate_seen':False,'mathematical_target_changed':False,'no_admission':True})
for s in slots:
 b=pathlib.Path(s['path']).read_bytes();assert sha(b)==s['whole_raw_sha256'];frag=b[s['start_utf8_byte0']:s['end_utf8_byte0_exclusive']];assert sha(frag)==s['fragment_raw_sha256']
capsule='''Primary-first55 preparatory source reconstruction is frozen before any new root exact signature exists or is read. primary-before-signature.freeze.json binds the initial source draft and exact selected source units; all nine units have balanced p/table/tbody/tr/td wrappers. Actual lease remains OPEN by authorization; compiler NOT_STARTED_CLOSED.

Recommend the actual all-L2 same-law mean bridge: produce canonical pullback isometry M and bounded contraction T internally from original PBPS curvature/step regime, actual mu/J/nu/S/U/P, with forall u: PMu=Mu, MTu=A Mu, Tu equal AE-nu to the literal S integral, AE-nu fiber integrability of u and u², integral variance(S,u)=norm(BMu)^2=norm(u)^2-norm(Tu)^2. Keep every-y source density equality, but rough observer integrability/mean representatives only AE-nu. No centering, Nontrivial, caller operator/kernel/normalizer/coherence/closure/limit premises.

Shortest selected producer route uses actual50 probability/source-kernel/compact coherence, canonical Lp pullback, actual51 dense smoothcompact input core, closed isometric M range and continuity to extend A invariance, then inverse-range T. Actual all-L2 ReflectionL2 projection formula and whole-kernel AE uniqueness align kernel/operator representatives; actual GaussianReflection yields Lambda.snd=nu. L1/square L1/disintegration and genuine variance definition give B9 defect. This mean producer does not require54 proof, and claims no rough gradient/H1/Gamma/main/cost result.

public-provider-slots.current.draft.json pins 25 exact selected slots. Original historical55 snapshots remain immutable. Two explicit bounded provider-plan errata are retained: historical Unique51-53 is the weaker primed per-set theorem, so whole-kernel uniqueness82-84 and its StandardBorel/Nonempty/finite context are added; L2.inner_def is restricted to theorem137 header with the old instance/rfl prefix disclosed. Complete ambient lexical/caller/context inventory and exact fixed-target coverage remain preparatory work for the later signature-bound graph, not a topology admission.

Native checkpoint raw/LF inputs and output hashes use exact bytes and CRLF->LF only. Run logical hash uses sorted compact UTF8 JSON ensure_ascii=False, whole object excluding run_sha256. Historical CLOSED preread lease and current OPEN creator lease are distinguished. No55 compiler, typing, claim, SAU, proof, canonical edit or admission; no54 body/verdict/decoder or new55 candidate seen.
'''
(O/'capsule.checkpoint.md').write_bytes(capsule.encode('utf8'))
inputs=json.loads((O/'draft-input-bindings.json').read_text(encoding='utf8'))
for d in inputs:assert desc(pathlib.Path(d['path']))['raw_sha256']==d['raw_sha256']
outputs=[desc(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['run.checkpoint.json']]
run={'schema':'sourcegraph55-source-before-signature-checkpoint/v1','status':'OPEN_PREPARATORY_SOURCE_ONLY','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'actual_lease':desc(O/'lease.json'),'primary_freeze':desc(O/'primary-before-signature.freeze.json'),'current_public_slots':25,'primary_coverage_rows':208,'primary_formula_count':78,'candidate_seen':False,'implementation_seen':False,'proof54_seen':False,'compiler':'NOT_STARTED_CLOSED','topology_admitted':False,'hash_recipes':{'raw':'SHA256 exact bytes','LF':'CRLF -> LF only','logical':'SHA256 UTF8 sorted compact JSON ensure_ascii=False of whole run minus run_sha256'}}
run['run_sha256']=sha(json.dumps(run,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8'));write('run.checkpoint.json',run)
print(json.dumps({'run_raw':sha((O/'run.checkpoint.json').read_bytes()),'run_logical':run['run_sha256'],'primary_freeze':run['primary_freeze']['raw_sha256'],'lease_OPEN':run['actual_lease']['raw_sha256'],'public_slots':25,'outputs':len(outputs),'inputs':len(inputs)}))
