from pathlib import Path
import copy, datetime, hashlib, json
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86'
OUT=BASE/'independent-source86'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def desc(p,kind):return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(p),'sha256':sha(p),'bytes':p.stat().st_size,'kind':kind}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(name,data):
 p=OUT/name
 assert not p.exists()
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return p
oldpacket=BASE/'source-review86.packet.json'
packet=BASE/'source-review86.eof-successor.packet.json'
old,new=read(oldpacket),read(packet)
canonical=hashlib.sha256(json.dumps({k:v for k,v in new.items() if k!='packet_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert canonical==new['packet_sha256']=='05d5060a5a0bbf369040a91cfbb30fe44362bbb439fb2c3132b5cc93e161404a'
assert sha(packet)=='f2d16dff9329694d1ee080c09af6eaa14782bb27c0d4e3b381b26109f417a09e'
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
lesson=ROOT/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
publication=ROOT/'website/content/publications/pbps-actual-finite-first-event-law.json'
oldmodule=BASE/'eof-whitespace-repair86/module.before.exactraw.lean'
oldlesson=BASE/'eof-whitespace-repair86/lesson.before.exactraw.json'
expected=BASE/'eof-source-review86/eof-lesson-metadata.expected-structure.json'
oldhash='cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5'
newhash='d6667ccbb917d6463e96b2082a5a26089950889fd20af4859052cd7a9a1db776'
assert sha(module)==newhash and module.read_bytes()==oldmodule.read_bytes()[:-1]
assert oldlesson.read_bytes().count(oldhash.encode())==11
assert lesson.read_bytes()==oldlesson.read_bytes().replace(oldhash.encode(),newhash.encode())
assert read(lesson)==read(expected)
assert sha(lesson)=='9cb0da1316872b2484404316211a9378310656b61ceb02b455793d055e5fb033'
assert sha(publication)=='f1408d45a5bfe5aa5875b73786460296e451da94074a40335aad2d75a5392bb1'
for field in ['lean','source','blind_reconstruction','anti_anchoring']:assert new[field]==old[field]
assert new['candidate_publication_context']['file']==newhash
assert new['candidate_publication_context']['current_lean_module'].encode()==module.read_bytes()
unit=read(lesson)['units'][0]
for key,value in new['candidate_publication_context']['lesson'].items():assert value==unit[key]
# Hash-only permission. Never decode, parse, print or expose these bytes.
anonymous_old=BASE/'anonymous.decoder86.json'
anonymous_new=BASE/'eof-whitespace-repair86/anonymous.eof-successor.packet.json'
assert anonymous_old.read_bytes()==anonymous_new.read_bytes()
assert sha(anonymous_old)==sha(anonymous_new)=='5b44cec13222776d49e7aac7337b2b76a538d487b47a2a1e791925b305ddf995'
previous=OUT/'source-review86.final-successor.decision.json'
previous_run=OUT/'source-review86.final-successor.run.json'
d=copy.deepcopy(read(previous))
lines=module.read_text(encoding='utf-8').splitlines(keepends=True)
for i,step in enumerate(unit['steps']):
 region=step['lean_source_region']
 assert region['source_raw_sha256']==newhash
 code=''.join(lines[region['start_line']-1:region['end_line']])
 assert code==step['lean']
 assert hashlib.sha256(code.encode()).hexdigest()==region['exact_code_raw_sha256']
 d['lesson_review']['steps'][i]['region']=region
 d['authored_step_coverage']['steps'][i]['region']=region
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
d.update(status='SOURCE_LOCAL_AND_EFFECTIVE_TOPOLOGY_ACCEPTED_EOF_REBOUND_CANDIDATE_LAYOUT_ACCEPTED_APPLICATION_PENDING',reviewer_packet_sha256=canonical,reviewer_packet_raw_sha256=sha(packet),publication_binding_sha256=new['publication_binding_sha256'],full_module_sha256=newhash,current_lesson_raw_sha256=sha(lesson),current_publication_raw_sha256=sha(publication),completed_utc=now)
d.pop('review_run_sha256',None)
d['reason']='Exact current module is the reviewed module minus its final empty LF line. Current lesson differs byte-for-byte only in11 containing-module provenance hashes; all exact region hashes, lines, prose/formulas and assumptions are unchanged. The fresh anti-anchored packet changes only current-module/lesson provenance and packet/publication bindings. Authorized anonymous original/successor packets are independently byte-identical by hash-only comparison, so prior independent blind reconstruction and all seven-slot/source/topology/full-statement/11step/V4candidate analyses remain valid and are explicitly reused under a fresh exact binding. Applied site generation, browser validation and live publication remain pending.'
d['review_evidence']=d['reason']
anonymous_check={'method':'RAW-byte equality and SHA256 only; anonymous content was never decoded/parsed/printed','original':desc(anonymous_old,'anonymous-hash-only-original'),'successor':desc(anonymous_new,'anonymous-hash-only-successor'),'byte_identical':True,'no_new_blind_run_required':True}
d['nonmathematical_rebinding']={'historical_review':desc(previous,'immutable-previous-final-source-decision'),'old_module':desc(oldmodule,'immutable-old-module-snapshot'),'old_lesson':desc(oldlesson,'immutable-old-lesson-snapshot'),'current_module':desc(module,'current-module'),'current_lesson':desc(lesson,'current-lesson'),'exact_EOF_review':desc(BASE/'eof-source-review86/eof-source-review86.decision.json','independent-EOF-delta-review'),'exact11_metadata_review':desc(BASE/'eof-source-review86/eof-source-review86.metadata-supplement.decision.json','independent11metadata-review'),'root_delta_provenance':desc(BASE/'root.eof86.adoption.json','delta-application-provenance-only'),'allowed_changes':['Delete final LF only, retaining namespace terminal newline','Change exactly11 per-step source_raw_sha256 fields oldmodule->newmodule; every other lesson byte identical'],'anonymous_packet_check':anonymous_check,'unchanged_analyses':['All seven primary-first independently assessed semantic slots','All72 explicit source anchors and independently composed38node76relation source topology','All14 literal definitions and six analytic source binders','All11 exact proof regions and explanations','Exact V4 candidate reader layout'],'mathematical_or_source_statement_change':False}
d['pending_actions']=['Apply exact separately reviewed V4 renderer in sole integration lane if still unapplied.','Run actual aggregate/publication/site checks and browser validation on applied output.','No VERIFIED/stabilization/main/PURIFIED/live/fullpaper/wholeGoal conclusion supplied by this reviewer.']
paths=[(packet,'canonical-current-reviewer-packet'),(oldpacket,'immutable-original-reviewer-packet'),(module,'current-lean-module'),(lesson,'current-authored-lesson'),(publication,'current-publication'),(ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html','primary-source'),(OUT/'primary-first-freeze.json','original-primary-first-freeze'),(previous,'historical-immutable-source-decision'),(previous_run,'historical-immutable-source-run'),(oldmodule,'immutable-old-module-snapshot'),(oldlesson,'immutable-old-lesson-snapshot'),(expected,'exact11field-expected-lesson-structure'),(BASE/'eof-source-review86/eof-source-review86.decision.json','independent-EOF-delta-review'),(BASE/'eof-source-review86/eof-source-review86.metadata-supplement.decision.json','independent11metadata-review'),(BASE/'root.eof86.adoption.json','delta-application-provenance-only'),(anonymous_old,'anonymous-hash-only-original'),(anonymous_new,'anonymous-hash-only-successor'),(BASE/'topology-repair-review86/source-proof-graph86.single-edge-proposed-successor.json','effective-source-graph'),(OUT/'source-inventory86.exhaustive-successor.json','exhaustive-source-inventory'),(OUT/'renderer-v4-candidate-inspection86.json','unchanged-independent-V4-candidate-inspection'),(BASE/'reader-adjacency-repair86/proposal.v4.json','exact-V4-renderer-proposal'),(BASE/'reader-adjacency-repair86/renderer.proposed.v4.exactraw.snapshot','exact-V4-renderer-candidate')]
inputs=[desc(p,k) for p,k in paths];inputs[0]['canonical_sha256']=canonical
chronology={'previous_independent_chronology':desc(OUT/'source-review86.final-successor.chronology.json','immutable-full-review-chronology'),'new_events':['Root proposed oneLF cleanup; reviewer independently checked prefix identity and11 exact source regions.','Root specified exact11 metadata changes; reviewer froze expected parsed structure and provenance-only assessment.','Root applied reviewed changes and supplied canonical fresh source-review packet.','Reviewer checked current module/lesson byte delta, fresh packet canonical/RAW hash and context projection, unchanged source/statement/reconstruction fields.','Explicit narrow anonymous authorization: independently byte-compared and hashed old/new files without exposing/parsing content.','Rebinding receipt frozen with unchanged seven-slot/72anchor/11step/V4candidate analyses and new input descriptors; no canonical writes or completion claim.'],'anonymous_contents_exposed':False,'completed_utc':now}
run={'schema_version':1,'task':'independent-semantic-source-review-exact-nonmathematical-rebinding','reviewer':d['reviewer'],'independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':canonical,'reviewer_packet_raw_sha256':sha(packet),'publication_binding_sha256':d['publication_binding_sha256'],'reconstructed_theorem_sha256':d['reconstructed_theorem_sha256'],'full_module_sha256':newhash,'inputs':inputs,'input_artifacts':inputs,'review':d,'independent_chronology':chronology,'diagnostics':['Initial comparison incorrectly required full lesson object equality; canonical packet intentionally omits lesson.boundary. All14 included lesson keys and all11 source descriptors match current authored lesson exactly. No semantic/input drift.'],'completed_utc':now}
r=write('source-review86.eof-rebound.final.run.json',run)
d['review_run_sha256']=sha(r)
decision=write('source-review86.eof-rebound.final.decision.json',d)
ch=write('source-review86.eof-rebound.final.chronology.json',chronology)
m=write('source-review86.eof-rebound.final.native-RAW-manifest.json',{'schema':'astis.independent-source86.EOF-rebound.native-RAW-manifest.v1','inputs':inputs,'outputs':[desc(r,'immutable-native-final-run'),desc(decision,'immutable-native-final-decision'),desc(ch,'independent-chronology'),desc(Path(__file__).resolve(),'receipt-script')],'historical_analysis_manifest':desc(OUT/'source-review86.final-successor.native-RAW-manifest.json','immutable-historical-analysis-manifest'),'historical_mutable_paths':'Historical manifests retain their original canonical-path descriptors as history; current receipt binds accepted old contents through the preserved oldmodule/oldlesson snapshots. No old RAW is required at current mutable canonical paths.','source_private_exclusions':['primary-A1.SS1-extraction.private.json','primary-standing-source-context.private.json','primary-A1.SS1-raw.private.html','primary-atomic-items.private.json'],'anonymous_contents_copied':False,'canonical_writes':False,'original_review_files_changed':False,'completed_utc':now})
print(json.dumps({'decision':desc(decision,'native-final-decision'),'run':desc(r,'native-final-run'),'manifest':desc(m,'native-RAW-manifest'),'chronology':desc(ch,'independent-chronology'),'reviewer_packet_sha256':canonical,'publication_binding_sha256':d['publication_binding_sha256'],'full_module_sha256':newhash,'current_lesson_raw_sha256':sha(lesson),'reconstructed_theorem_sha256':d['reconstructed_theorem_sha256'],'source_text_sha256':d['source_text_sha256'],'verdict':d['verdict']},indent=2))
