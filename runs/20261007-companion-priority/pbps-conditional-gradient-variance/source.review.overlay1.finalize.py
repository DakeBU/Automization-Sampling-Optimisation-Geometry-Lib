import datetime as dt
import hashlib
import json
import pathlib
import sys
import types

sys.dont_write_bytecode=True
sys.path[:0]=['tools','website/scripts']
import astis_publication as pub
import astis_semantic_roundtrip_core as rt
ROOT=pathlib.Path.cwd()
RUN=ROOT/'runs/20261007-companion-priority/pbps-conditional-gradient-variance'
def h(b):return hashlib.sha256(b).hexdigest()
def canon(o):return h(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8'))
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def write(p,o):pathlib.Path(p).write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return sorted(x for k in a.keys()|b.keys() for x in (diff(a[k],b[k],p+'/'+k) if k in a and k in b else [p+'/'+k]))
 if isinstance(a,list):
  if len(a)==len(b) and all(isinstance(x,dict) for x in a+b):return [z for i,(x,y) in enumerate(zip(a,b)) for z in diff(x,y,p+'/'+str(i))]
  return [p] if a!=b else []
 return [p] if a!=b else []

lease=read(RUN/'source.1.review.lease.json');own=read(RUN/'reviewer.source.1.lease.json')
assert lease['status']==own['status']=='OPEN'
original=read(RUN/'source.0.review.json')
assert pin(RUN/'source.0.review.json')['raw_sha256']=='d1dff3c8228af14bffcb93b662687ab94b733238288640b24670f4448827e2b6'
assert original['blocking'] and canon({k:v for k,v in original.items() if k!='review_run_sha256'})==original['review_run_sha256']
packet=read(RUN/'source.1.reviewer-packet.json');oldpacket=read(RUN/'source.0.reviewer-packet.json')
assert canon({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==lease['reviewer_packet_sha256']
oldchecks=read(RUN/'source.review.checks.json')
snapmap={x['source']['path']:ROOT/x['snapshot']['path'] for x in oldchecks['immutable_snapshots']}
lp='website/content/declaration_lessons/pbps-conditional-gradient-variance.json'
pp='website/content/publications/pbps-conditional-gradient-variance.json'
ap='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientVariance.json'
oldlesson=read(snapmap[lp]);lesson=read(ROOT/lp)
oldpub=read(snapmap[pp]);publication=read(ROOT/pp)
oldaudit=read(snapmap[ap]);audit=read(ROOT/ap)
overlay=RUN/'publication-metadata-overlay48'
assert (overlay/'pbps-conditional-gradient-variance.json.before.raw.snapshot').read_bytes()==snapmap[lp].read_bytes()
assert (overlay/'ASTIS-RT-20261007-PBPSConditionalGradientVariance.json.before.raw.snapshot').read_bytes()==snapmap[ap].read_bytes()
assert diff(oldlesson,lesson)==['/units/0/astis_dependencies','/units/0/mathlib_dependencies']
u=lesson['units'][0];ou=oldlesson['units'][0]
expected=ou['mathlib_dependencies'][:];assert expected[5]=='InnerProductSpace.inner_gradient_left';expected[5]='inner_gradient_left'
assert u['mathlib_dependencies']==expected
actualparent='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg'
assert u['astis_dependencies']==ou['astis_dependencies']+[actualparent]
assert diff(oldpub,publication)==['/items/0/chapter_path']
assert publication['items'][0]['chapter_path']=='example-cases/samplewiki/companions/proximal-bouncy-particle.html'
assert diff(oldaudit,audit)==['/publication_binding_sha256','/publication_context/lesson/astis_dependencies','/publication_context/lesson/mathlib_dependencies']
assert diff(oldpacket,packet)==['/candidate_publication_context/lesson/astis_dependencies','/candidate_publication_context/lesson/mathlib_dependencies','/packet_sha256','/publication_binding_sha256']
assert rt.semantic_reviewer_packet(audit)==packet
name=packet['lean']['declaration'];data={'declarations':{name:types.SimpleNamespace(source_file=packet['lean']['file'])},'lessons':{name:u}}
item=publication['items'][0]
assert pub.binding_digest(item,item['bindings'][0],data)==packet['publication_binding_sha256']==lease['publication_binding_sha256']
assert pub.review_context(item,item['bindings'][0],data)==packet['candidate_publication_context']
assert packet['source']==oldpacket['source'] and packet['lean']==oldpacket['lean'] and packet['blind_reconstruction']==oldpacket['blind_reconstruction']
for a in lease['input_artifacts']:
 p=pin(ROOT/a['path']);assert p['raw_sha256']==a['raw_sha256'] and p['lf_sha256']==a['lf_sha256'],a['path']
for a in original['additional_input_artifacts']:
 p=pin(ROOT/a['path']);assert p['raw_sha256']==a['raw_sha256'] and p['lf_sha256']==a['lf_sha256'],a['path']
prior_changes=[];reused=[]
for a in original['input_artifacts']:
 p=pin(ROOT/a['path']);reused.append(p)
 if p['raw_sha256']!=a['raw_sha256'] or p['lf_sha256']!=a['lf_sha256']:prior_changes.append(a['path'])
assert sorted(prior_changes)==sorted([lp,pp,ap])
for path in [packet['lean']['file'],'Tests/ProximalBPSConditionalGradientVariance.lean']:
 assert (ROOT/path).read_bytes()==snapmap[path].read_bytes()
gradient=(ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean').read_text(encoding='utf-8')
assert 'lemma inner_gradient_left' in gradient and not any(l.startswith('namespace ') for l in gradient.splitlines()[:291])
code=(ROOT/packet['lean']['file']).read_text(encoding='utf-8');assert actualparent in code
vf=(ROOT/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean').read_text(encoding='utf-8');assert 'theorem variance_nonneg' in vf
drun=read(RUN/'anonymous-decoder/run.json');decoder=read(RUN/'anonymous-decoder/result0.json')
assert canon(drun['execution_payload'])==decoder['decoder_run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
assert decoder['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert audit['reconstruction']['input_artifacts']==['lean-statement','approved-definition-context']
front=read(ROOT/'website/content/samplewiki_companion_frontiers.json');assert front['cases'][2]['slug']=='proximal-bouncy-particle'
formulaunchanged=u['formula']==ou['formula'] and u['steps']==ou['steps'] and item['formulae']==oldpub['items'][0]['formulae']
assert formulaunchanged and all('\\\\' not in s for s in [u['formula'],*[s['formula'] for s in u['steps']]])

snapshots=[]
for i,path in enumerate([RUN/'source.1.review.lease.json',RUN/'source.1.reviewer-packet.json',ROOT/lp,ROOT/pp,ROOT/ap,overlay/'repair.json']):
 dest=RUN/f'source.review.overlay1.frozen.{i:02d}.raw.snapshot{path.suffix}';assert not dest.exists();dest.write_bytes(path.read_bytes());snapshots.append({'source':pin(path),'snapshot':pin(dest)})
checks={'reviewer':'phase_source_reviewer_20261005','status':'ACCEPTED_SCOPED_METADATA_ONLY_OVERLAY','blocking':False,'checked_utc':utc(),'repair_proposal':pin(overlay/'repair.json'),'original_rejected_review':pin(RUN/'source.0.review.json'),'exact_diff':{'publication':diff(oldpub,publication),'lesson':diff(oldlesson,lesson),'audit':diff(oldaudit,audit),'reviewer_packet':diff(oldpacket,packet)},'exact_operations_checked':'Only chapter_path replacement, one qualified-to-global Mathlib name, append one actually called variance_nonneg parent; audit context/binding and packet hash are derived.','all_current_frozen_inputs_raw_LF_match':True,'frozen_input_count':len(lease['input_artifacts']),'original_215_current_footprints_checked':len(reused),'only_original_changed_paths':prior_changes,'current_reused_input_artifacts':reused,'production_Test_original_raw_bytes_identical':True,'source_statement_reconstruction_unchanged':True,'same_verbatim_decoder_originals_and_acyclic_payload_hash':decoder['decoder_run_sha256'],'all_six_steps_formulas_and_source_original_newlines_unchanged':True,'no_TeX_or_newline_repair':True,'canonical_publication_context_and_packet_rebuilt_exact':True,'metadata_truth':'global inner_gradient_left exists with no namespace; variance_nonneg is directly invoked at target lines105/110; companion renderer emits BASE+slug+.html matching proximal-bouncy-particle','source_proof_graph_unchanged_reused_without_self_validation':True,'no_compiler_or_new_math_credit':True,'input_artifacts':lease['input_artifacts'],'snapshots':snapshots}
checks['review_run_sha256']=canon(checks);write(RUN/'source.review.overlay1.checks.json',checks)
result={k:v for k,v in original.items() if k not in ['review_run_sha256','status','verdict','blocking','mathematical_source_comparison','verdict_explanation','deltas','repairs','input_artifacts','checks_artifact','started_utc','finished_review_utc']}
result.update({'status':'ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_ONLY_OVERLAY','verdict':'equivalent-after-elaboration','blocking':False,'reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'deltas':[],'repairs':[],'semantic_slots':original['semantic_slots'],'input_artifacts':lease['input_artifacts'],'current_reused_original_215_input_artifacts':reused,'checks_artifact':pin(RUN/'source.review.overlay1.checks.json'),'original_review':pin(RUN/'source.0.review.json'),'original_review_run_sha256':original['review_run_sha256'],'overlay_proposal':pin(overlay/'repair.json'),'overlay_review_run_sha256':checks['review_run_sha256'],'scope':'Fresh exact publication metadata overlay and current packet acceptance. Original independent primary/whole-production/two complete Tests/six-formula/seven-slot source review reused only after unchanged mathematical/source/decoder byte checks. No repeated proof compilation or additional mathematical result.','review_evidence':'Independently accepted exactly three requested metadata corrections and derived audit/context/packet rebinding; no other JSON field changed. Rechecked all55 overlay-frozen raw/LF inputs and all215 original current footprints (only publication, lesson and derived audit changed). Full production/Test, exact signature, source/definitions, sourcegraph, six formula proof steps and original anonymous decoder bytes/hashes remain unchanged. Global inner_gradient_left, direct Poincare.variance_nonneg and canonical companion slug are now correct. Own primary-beforebody seven-slot analysis is explicitly reused with no EXCESS or mathematical/source repair. Compiler never started; original blocked receipt preserved; this accepts only pointwise smoothcompact Ex7, not outer integration/rough closure/B13/main/cost/reader feature completion.','started_utc':own['opened_utc'],'finished_review_utc':utc(),'exposure':{**original['exposure'],'current_review':'Previously complete own whole-source mathematical comparison known, root-authored representation repair assessed independently; no claim of fresh historical blindness or repeated proof review.'},'verdict_explanation':'All seven mathematical slots and actual scoped proof remain equivalent after explicit finite-Hilbert/rank-zero/own-gradient elaboration; original metadata blockers are now exactly repaired without added source/public assumptions.'})
result['semantic_slots']['scopes']['evidence']='All six unchanged formula steps match the actual own-gradient route and preserve outer/rough boundaries. Three original provenance/locator defects are independently repaired exactly, with source/proof bytes unchanged; actual current API IDs and companion path now match. Tests retain their stated actual Markov/reflection and zero-gradient outputs without claiming every production conjunction independently.'
result['review_evidence_details']['scopes']=result['semantic_slots']['scopes']['evidence']
result['review_run_sha256']=canon(result);out=RUN/'source.1.review.json';assert not out.exists();write(out,result)
assert canon({k:v for k,v in read(out).items() if k!='review_run_sha256'})==result['review_run_sha256']
for a in lease['input_artifacts']:
 p=pin(ROOT/a['path']);assert p['raw_sha256']==a['raw_sha256'] and p['lf_sha256']==a['lf_sha256']
for path,current in [(RUN/'reviewer.source.1.lease.json',own),(RUN/'source.1.review.lease.json',lease)]:
 current.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':utc(),'result':pin(out),'review_run_sha256':result['review_run_sha256'],'outcome':'accepted-scoped current source fidelity after exact metadata-only overlay; no canonical changes'})
 current.pop('lease_run_sha256',None);current['lease_run_sha256']=canon(current);write(path,current)
print(json.dumps({'result':pin(out),'review_run_sha256':result['review_run_sha256'],'packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'overlay_check':pin(RUN/'source.review.overlay1.checks.json'),'root_lease':pin(RUN/'source.1.review.lease.json'),'own_lease':pin(RUN/'reviewer.source.1.lease.json'),'all_leases':'CLOSED'},ensure_ascii=False))
