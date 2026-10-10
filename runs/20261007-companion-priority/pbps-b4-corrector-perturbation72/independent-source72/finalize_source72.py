from pathlib import Path
import json,hashlib,os,sys,traceback,copy
sys.dont_write_bytecode=True
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72';OWN=RUN/'independent-source72';REL=OWN.relative_to(ROOT).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def write(n,x):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(ROOT).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'bytewise CRLF-to-LF only'}
def ptrdiff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):
  assert set(a)==set(b);return [q for k in a for q in ptrdiff(a[k],b[k],p+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b);return [q for i,(x,y) in enumerate(zip(a,b)) for q in ptrdiff(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
code=0
try:
 assert not (OWN/'lease.final.json').exists()
 # Finite overlay history is small; preserve precise RAW/LF versions rather than
 # recursively embedding any old native audit tree or source packet.
 historypaths=[];hist=[]
 for folder in ['reader-status-overlay72','reader-status-overlay72.v2','reader-status-overlay72.v3']:
  d=RUN/folder;p=load(d/'proposal.json');historypaths.append(d/'proposal.json')
  for r in p['rows']:historypaths.extend([ROOT/r['before'],ROOT/r['proposed']])
  for r in p['bindings']:historypaths.append(ROOT/r['proposed_packet'])
  for n in [0,1]:
   for suffix in ['before.exactraw','proposed']:
    f=d/f'audit.{n}.{suffix}.json'
    if f.exists():historypaths.append(f)
  hist.append({'proposal':pin(d/'proposal.json'),'status':'approved-and-applied-exact' if folder.endswith('.v3') else 'incomplete-unapplied-retained','changed_field_count':p['status_fields'],'rows':p['rows'],'mathematical_change':False})
 unique=[];seen=set()
 for p in historypaths:
  if str(p) not in seen:seen.add(str(p));unique.append(p)
 pins=[]
 for i,p in enumerate(unique):
  b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');rd=OWN/f'overlay-inputs/{i:02d}.exactraw.snapshot';ld=OWN/f'overlay-inputs/{i:02d}.LF.snapshot';rd.parent.mkdir(exist_ok=True);rd.write_bytes(b);ld.write_bytes(lf)
  q=pin(p);q.update(raw_snapshot=rd.relative_to(OWN).as_posix(),lf_snapshot=ld.relative_to(OWN).as_posix(),semantic_read='opaque/diff pointer identity only; no prior verdict read' if '/audit.' in p.as_posix() else 'finite exact metadata mapping');pins.append(q)
 write('StageB.overlay-history.inputs.json',{'input_count':len(pins),'inputs':pins,'history':hist,'canonical_edit_by_reviewer':False})
 maps=[]
 for n in [0,1]:
  before=load(RUN/f'source-review.packet.{n}.json');after=load(RUN/f'source-review.packet.{n+2}.json');expected={'/publication_binding_sha256','/packet_sha256','/candidate_publication_context/lesson/sources/0/scope','/candidate_publication_context/candidate_assumptions/1/lean'}
  assert set(ptrdiff(before,after))==expected
  assert (RUN/f'source-review.packet.{n+2}.json').read_bytes()==(RUN/f'reader-status-overlay72.v3/source-review.packet.{n+2}.proposed.json').read_bytes()
  maps.append({'unit':n,'before':pin(RUN/f'source-review.packet.{n}.json'),'after':pin(RUN/f'source-review.packet.{n+2}.json'),'exact_leaf_diff_pointers':sorted(expected),'source_Lean_statement_decoder_formulas_BODY_unchanged':True,'whole_context_identical':False,'context_change':'Only same status suffix in lesson.sources[0].scope and candidate_assumptions[1].lean','before_context_sha256':sha(canon(before['candidate_publication_context'])),'after_context_sha256':sha(canon(after['candidate_publication_context']))})
 write('StageB.official-packet-version-map.json',{'units':maps,'canonical_objects_changed':8,'candidate_JSON_files_changed':6,'audits_changed':2,'authored_status_fields_changed':16,'mathematical_repair':False,'v3_independent_decision':pin(OWN/'reader-status-overlay72.v3.independent-decision.json')})
 write('StageB.observer-and-negative-history.json',{'failures':[{'actual_pid':38936,'exit_code':1,'receipt':'reader-status-overlay72.proposal0.terminal.json','helper':'review_overlay0.py','classification':'observer residual-count assertion; incomplete metadata v1 correctly not applied','exact_output_available':'original tool event / original helper and terminal receipt retained'},{'actual_pid':30276,'exit_code':0,'receipt':'reader-status-overlay72.v2.terminal.json','decision':'needs-revision','classification':'12-field v2 leaves four cell pending suffixes; no math failure'},{'actual_pid':33468,'exit_code':1,'receipt':'StageB.coverage.terminal.json','helper':'complete_coverage72.py','classification':'observer conflated twelve global and two local existentials; no candidate modification'},{'exit_code':1,'tool_chunk':'994f47','actual_pid':'not reported by tool; not invented','classification':'rg query named nonexistent astis_publication_core.py; corrected to actual astis_publication.py'}],'subsequent_successes':[{'actual_pid':45320,'exit_code':0,'receipt':'reader-status-overlay72.v3.terminal.json'},{'actual_pid':8608,'exit_code':0,'receipt':'StageB.coverage.v2.terminal.json'},{'actual_pid':47444,'exit_code':0,'receipt':'StageB.author-reviews.terminal.json'}],'correction_without_math_change':True,'early_approved_context_null':'inspect_semantics.py looked at wrong JSON level. Actual authorized neutral lean.approved_definition_context read subsequently; no missing context interpreted as theorem semantics.'})
 covnames=['StageB.source361.coverage.json','StageB.source-graph24-node-dispositions.json','StageB.source20-formula-coverage.json','StageB.all27-obligations.decisions.json','StageB.whole494-line-coverage.json','StageB.exact10-BODY-formula-coverage.json','StageB.parent-retention.exact-check.json','StageB.final-binding-checks.json','StageB.official-packet-version-map.json']
 reviews=[(OWN/f'source.{n}.review.RAW.md').read_text(encoding='utf-8') for n in [0,1]];cores=[load(OWN/f'source.{n}.decision.core.json') for n in [0,1]]
 run={'schema':'independent-source72-two-unit-native-run-v1','reviewer':'independent_primary69','source_blind':False,'anti_anchoring':'StageA pre-header/pre-BODY immutable; current72 BODY/publication/reconstruction first after official dispatch. Prior70/71/header72 exposure disclosed. Other math/source/header-math verdicts not read.','truth_scope':'Independent source/whole-module/formula/BODY/roundtrip review only; no proof ownership or SCI/VERIFIED/PURIFIED/fullpaper/Goal admission.','units':[{'unit':n,'official_packet':pin(RUN/f'source-review.packet.{n+2}.json'),'official_packet_sha256':load(RUN/f'source-review.packet.{n+2}.json')['packet_sha256'],'semantic_decision_before_run_binding':cores[n],'complete_RAW_review':reviews[n]} for n in [0,1]],'input_manifests':[pin(OWN/name) for name in ['preparation.inputs.json','StageB.current-inputs.manifest.json','StageB.final-current-inputs.manifest.json','StageB.overlay-history.inputs.json']],'coverage_artifacts':[pin(OWN/name) for name in covnames],'coverage':{'source_items':361,'NODE':239,'EXCLUDED':122,'source_nodes':24,'source_edges':53,'source_formulas':20,'source_obligations':27,'module_lines':494,'BODY_spans':[6,4],'blocking_deltas':[0,0]},'run_hash_recipe':'SHA256 of canonical UTF-8 JSON sorted keys ensure_ascii=False separators comma/colon after deleting ONLY top-level run_sha256. Derived decisions/admission reference this exact completed review run; no circular self-inclusion.','canonical_or_old_closed_writes':False,'actual_authoring_pid':os.getpid()}
 run['run_sha256']=sha(canon(run));write('source72.run.json',run)
 sys.path.insert(0,str(ROOT/'tools'));import astis_semantic_roundtrip_core as core
 audits=[];identity=[]
 slug=['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation'];an=['ASTIS-RT-20261010-PBPSHilbertCorrectorPerturbation','ASTIS-RT-20261010-PBPSActualCorrectorPerturbation']
 for n in [0,1]:
  p=load(RUN/f'source-review.packet.{n+2}.json');d=copy.deepcopy(cores[n]);d['review_run_sha256']=run['run_sha256'];d['state']='source-reviewed'
  source_review={'state':'accepted','reviewer':'independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'evidence':f'{REL}/source.{n}.review.RAW.md','review_run_sha256':run['run_sha256'],'reviewer_packet_sha256':p['packet_sha256'],'run_artifact':f'{REL}/source.{n}.decision.json'}
  d['source_review']=source_review;write(f'source.{n}.decision.json',d)
  fields={k:d[k] for k in ['state','verdict','semantic_slots','deltas','source_review','repairs']}
  coverage={'source_graph':f'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72/stageA.source-proof-graph72.before-header.frozen.json','source_inventory':f'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72/stageA.finite-source255-plus-supplemental-coverage72.frozen.json','coverage_report':f'{REL}/source.{n}.decision.json','coverage_status':f'Independent bounded whole-implementation/source review72 unit{n}:361 exact source items=255primary+106supplemental (239NODE/122EXCLUDED),24 source nodes53 edges,20 formulas27 obligations,494 combined module lines and6+4 exact BODY spans. Source graph/classes unchanged; per-node current dispositions recorded. NODE is source relevance, not a proof badge. Actual H/K/r_rho/B27/B28/fullB4/main/errors/cost/composition remain OPEN; no Exposition Seal/PURIFIED/VERIFIED/wholepaper/Goal credit.'}
  admission={'schema':'source72-portable-canonical-admission-fields-v1','unit':n,'audit_fields':fields,'cell_source_proof_coverage':coverage,'publication_source_proof_coverage':coverage,'official_packet_sha256':p['packet_sha256'],'official_packet_RAW_sha256':sha((RUN/f'source-review.packet.{n+2}.json').read_bytes()),'publication_binding_sha256':p['publication_binding_sha256'],'candidate_publication_context_sha256':sha(canon(p['candidate_publication_context'])),'native_review_run_sha256':run['run_sha256'],'native_run_artifact':f'{REL}/source72.run.json','preserve_reviewer_packet_before_after_admission':True,'apply_only_authored_fields':True}
  write(f'source.{n}.admission-fields.json',admission)
  # Select identity/provenance fields only. Do not observe prior semantic verdicts,
  # slots, deltas or repair conclusions while validating native protocol structure.
  raw_audit=load(ROOT/f'research-wiki/semantic-roundtrip/audits/{an[n]}.json')
  audit={k:raw_audit[k] for k in ['id','source','lean','reconstruction','publication_binding_sha256','publication_context']}
  before=core.semantic_reviewer_packet(audit);assert before==p
  audit.update(fields);after=core.semantic_reviewer_packet(audit);assert before==after
  assert canon(before)==canon(after)
  audits.append(audit);identity.append({'unit':n,'official_packet_sha256':p['packet_sha256'],'semantic_reviewer_packet_before_after_byte_equivalent':True,'canonical_packet_bytes_sha256':sha(canon(before)),'previous_verdict_fields_used':False})
 protocol={k:'required' for k in ['decoder_blindness','decoder_context_content_scan','independent_source_review','source_review_packet_binding','independent_repair_review','repair_review_packet_binding']};protocol['semantic_slots']=list(core.SEMANTIC_SLOTS);protocol['decoder_allowed_inputs']=list(core.DECODER_INPUT_ARTIFACTS)
 registry={'schema_version':1,'protocol':protocol,'audits':audits};errors=core.validate_registry(registry);assert not errors,errors
 # Coverage metadata is outside binding/review_context. Verify exact packet
 # stability under proposed portable coverage admissions without canonical writes.
 import astis_site as site;import astis_publication as pub
 paths=[ROOT/p['lean']['file'] for p in [load(RUN/'source-review.packet.2.json'),load(RUN/'source-review.packet.3.json')]];site.project_lean_paths=lambda:paths
 decls={d.full_name:d for d in site.scan_project_sources()[1]}
 for n in [0,1]:
  item=load(ROOT/f'website/content/publications/{slug[n]}.json')['items'][0];lesson=load(ROOT/f'website/content/declaration_lessons/{slug[n]}.json')['units'][0];b=item['bindings'][0];data={'declarations':decls,'lessons':{lesson['declaration']:lesson}};ad=load(OWN/f'source.{n}.admission-fields.json')
  orig=pub.binding_digest(item,b,data);ctx=pub.review_context(item,b,data);item['source_proof_coverage']=ad['publication_source_proof_coverage']
  assert pub.binding_digest(item,b,data)==orig==ad['publication_binding_sha256'];assert pub.review_context(item,b,data)==ctx
  identity[n]['coverage_update_preserves_binding_and_context']=True
 write('StageB.native-schema-and-admission-checks.json',{'actual_pid':os.getpid(),'exit_code':0,'schema_errors':errors,'bounded_audit_count':2,'identity_checks':identity,'canonical_writes':False,'protocol_check':'current tools/astis_semantic_roundtrip_core.py validate_registry on only the two synthesized admitted audits; no whole-registry/site/build check','run_sha256':run['run_sha256']})
 write('StageB.finalize.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False,'own_run_sha256':run['run_sha256']})
 # Complete named reviews, decisions and finite input manifests are included as
 # exact UTF8 strings. Large prior/native source inputs remain pinned references.
 names=['bounded-synthesis72.md','source72.run.json','source.0.review.RAW.md','source.1.review.RAW.md','source.0.decision.json','source.1.decision.json','source.0.admission-fields.json','source.1.admission-fields.json','preparation.inputs.json','StageB.current-inputs.manifest.json','StageB.final-current-inputs.manifest.json','StageB.overlay-history.inputs.json','StageB.official-packet-version-map.json','StageB.all27-obligations.decisions.json','StageB.source20-formula-coverage.json','StageB.final-binding-checks.json','StageB.native-schema-and-admission-checks.json','StageB.observer-and-negative-history.json','reader-status-overlay72.v3.independent-decision.json']
 manifest={'schema':'source72-complete-named-small-payload-manifest-v1','files':[pin(OWN/n) for n in names],'includes_complete_named_review_decision_run_inputs':True,'large_finite_coverage_and_RAW_snapshots':'Exact owned files pinned by native whole manifest; no historical recursive base64 or old254 copies.'};write('named-payload.manifest.json',manifest)
 payload={'schema':'source72-complete-named-review-decision-input-payload-v1','named_manifest':pin(OWN/'named-payload.manifest.json'),'manifest':manifest,'named_files':{n:{'RAW_utf8':(OWN/n).read_bytes().decode('utf-8'),'RAW_sha256':sha((OWN/n).read_bytes()),'RAW_bytes':(OWN/n).stat().st_size} for n in names},'finite_coverage_pins':[pin(OWN/n) for n in covnames],'RAW_snapshot_manifests':['StageB.current-inputs.manifest.json','StageB.final-current-inputs.manifest.json','StageB.overlay-history.inputs.json'],'native_whole_logical_run_sha256':run['run_sha256'],'not_claimed':'No Git RAW representation, historical close replay, old native changes, proof/SCI/VERIFIED/fullpaper completion.'};write('complete-named-review-decision-input-payload.json',payload)
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'run_RAW_sha256':sha((OWN/'source72.run.json').read_bytes()),'whole_logical_run_sha256':run['run_sha256'],'decision_RAW_sha256':[sha((OWN/f'source.{n}.decision.json').read_bytes()) for n in [0,1]],'admission_RAW_sha256':[sha((OWN/f'source.{n}.admission-fields.json').read_bytes()) for n in [0,1]],'named_manifest_RAW_sha256':sha((OWN/'named-payload.manifest.json').read_bytes()),'complete_named_payload_RAW_sha256':sha((OWN/'complete-named-review-decision-input-payload.json').read_bytes()),'complete_named_payload_bytes':(OWN/'complete-named-review-decision-input-payload.json').stat().st_size,'schema_errors':errors},indent=2))
except BaseException:
 code=1;traceback.print_exc();write('StageB.finalize.failure.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
