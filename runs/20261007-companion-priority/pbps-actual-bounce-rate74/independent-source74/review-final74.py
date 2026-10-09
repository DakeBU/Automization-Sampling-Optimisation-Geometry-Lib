from pathlib import Path
from types import SimpleNamespace
import json,hashlib,os,sys,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
RUN=R/'runs/20261007-companion-priority/pbps-actual-bounce-rate74'
PRE=R/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/independent-header-source74'
sys.path.insert(0,str(R/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def check(z):
 p=Path(z['path']);p=p if p.is_absolute() else R/p;b=p.read_bytes()
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
def write(n,x):
 p=O/n;assert not p.exists(),n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def snaps(p,folder,n):
 b=p.read_bytes();base=f'{folder}/{n:02d}'
 raw=O/(base+'.exactraw.snapshot');lf=O/(base+'.CRLF-only-LF.snapshot')
 raw.parent.mkdir(parents=True,exist_ok=True);assert not raw.exists() and not lf.exists()
 raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'))
 return {'path':pin(p)['path'],**{k:v for k,v in pin(p).items() if k!='path'},'RAW_snapshot':raw.relative_to(O).as_posix(),'LF_snapshot':lf.relative_to(O).as_posix()}
packet_path=RUN/'source-review.packet.json';freeze_path=RUN/'source-review.freeze74.json'
packet=load(packet_path);freeze=load(freeze_path)
assert packet['packet_sha256']=='649b468a636925f4644cda84268990c868a37fe1e036bace641594318034a30e'
assert sha(can({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
assert len(freeze['inputs'])==8
for z in freeze['inputs']:check(z)
recon_path=R/freeze['native_reconstruction']['path'];check(freeze['native_reconstruction']);recon=load(recon_path)
assert recon['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert recon['reconstructed_text_sha256']==sha(recon['reconstructed_theorem_text'].encode('utf-8'))==packet['blind_reconstruction']['text_sha256']
assert recon['source_text_visible'] is False and recon['source_identity_visible'] is False and recon['proof_visible'] is False
module=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'
lesson_path=R/'website/content/declaration_lessons/pbps-actual-bounce-rate.json'
pubpath=R/'website/content/publications/pbps-actual-bounce-rate.json'
auditpath=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBounceRate.json'
cellpath=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounce-rate.json'
audit=load(auditpath);cell=load(cellpath);item=load(pubpath)['items'][0];lesson=load(lesson_path)['units'][0]
assert audit['state']=='blind-reconstructed' and audit['source_review']=={'state':'pending'}
assert 'semantic_slots' not in audit and 'verdict' not in audit and 'deltas' not in audit
assert rt.semantic_reviewer_packet(audit)==packet
raw=module.read_bytes();lines=raw.splitlines(keepends=True)
assert len(lines)==211 and sha(raw)=='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c'
assert b''.join(lines[:70])==(PRE/'header74.proposed.exactraw.snapshot.lean').read_bytes()
prep=load(O/'prepacket.whole211line-coverage74.json');oldinputs=load(O/'prepacket.inputs.v0.json')
assert prep['module']['RAW_sha256']==sha(raw)
assert len(lesson['steps'])==7
for s in lesson['steps']:
 z=s['lean_source_region'];b=b''.join(lines[z['start_line']-1:z['end_line']]);assert sha(b)==z['exact_code_raw_sha256'] and b.decode('utf-8')==s['lean']
assert item['statement']==lesson['statement']==lesson['lean_statement']
name=packet['lean']['declaration'];binding=item['bindings'][0]
data={'declarations':{name:SimpleNamespace(source_file=module.relative_to(R).as_posix())},'lessons':{name:lesson}}
binding_sha=pub.binding_digest(item,binding,data);context=pub.review_context(item,binding,data)
assert binding_sha==packet['publication_binding_sha256']==audit['publication_binding_sha256']=='599d4550f863962f6ef74dd0821ef433ebe7c8f5ead8d907d8a5f409fb0feeca'
assert context==packet['candidate_publication_context']==audit['publication_context']

# Distinct approved reader-process repair authority; no other mathematical review.
repair=RUN/'independent-reader-metadata-repair74';adoption_path=RUN/'root.reader-metadata-overlay74.adoption.json'
adopt=load(adoption_path);rd=load(repair/'decision.json');rr=load(repair/'run.json');rl=load(repair/'lease.final.json')
assert rd['actor']=='/root/exact_science63' and rd['accepted'] and rd['independent_of_root_proposal_and_source_observer']
assert rd['new_theorem_or_source_review_verdict'] is False and rd['applied_by_reviewer'] is False
assert rl['status']=='CLOSED_LAST' and rl['owned_count']==25 and rr['run_sha256']==adopt['native_whole_logical_run_sha256']
assert sha(can({k:v for k,v in rr.items() if k!='run_sha256'}))==rr['run_sha256']
assert pin(repair/'lease.final.json')['RAW_sha256']==adopt['native_lease']['RAW_sha256']
for z in rl['all_owned_outputs_except_only_self']:check(z)
assert len(list(repair.rglob('*')))>0 and len([p for p in repair.rglob('*') if p.is_file()])==25
assert adopt['actual_root_PID']==32304 and len(rd['approved_rows'])==2 and adopt['old_binding_sha256']==adopt['new_binding_sha256']==binding_sha
def differences(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  if set(a)!=set(b):return [path]
  return [v for k in a for v in differences(a[k],b[k],path+'/'+str(k))]
 if isinstance(a,list):
  if len(a)!=len(b):return [path]
  return [v for i in range(len(a)) for v in differences(a[i],b[i],path+'/'+str(i))]
 return [] if a==b else [path]
repair_rows=[];repair_paths=[adoption_path,repair/'decision.json',repair/'run.json',repair/'lease.final.json',RUN/'reader-metadata-overlay74/proposal.json']
for z in rd['approved_rows']:
 before=check(z['before']);proposed=check(z['proposed']);current=R/z['path']
 assert current.read_bytes()==proposed
 assert differences(json.loads(before),json.loads(proposed))==[z['json_pointer']]
 repair_rows.append({'path':z['path'],'json_pointer':z['json_pointer'],'old':z['old'],'new':z['new'],'before':pin(R/z['before']['path']),'after':pin(current),'approved_proposed':pin(R/z['proposed']['path']),'authority':pin(repair/'decision.json'),'mathematical_change':False})
 repair_paths.extend([R/z['before']['path'],R/z['proposed']['path']])
assert len(repair_paths)==9
oldpub=load(O/'prepacket-inputs.v0/02.exactraw.snapshot')['items'][0]
assert pub.binding_digest(oldpub,oldpub['bindings'][0],data)==binding_sha
assert pub.review_context(oldpub,oldpub['bindings'][0],data)==context

# Preserve historical v0 artifacts and separate the8 final frozen current inputs.
final_current=[]
for i,z in enumerate(freeze['inputs']):final_current.append(snaps(R/z['path'],'final-current-inputs',i))
hist=[]
for q in oldinputs['inputs']:
 z={**q['input'],'RAW_snapshot':Path(q['RAW_snapshot']['path']).relative_to(O.relative_to(R)).as_posix(),'LF_snapshot':Path(q['LF_snapshot']['path']).relative_to(O.relative_to(R)).as_posix()}
 b=(O/z['RAW_snapshot']).read_bytes();assert sha(b)==z['RAW_sha256'] and (O/z['LF_snapshot']).read_bytes()==b.replace(b'\r\n',b'\n')
 current=pin(R/z['path']);z['final_current']=current
 if current['RAW_sha256']==z['RAW_sha256']:z['version_relation']='unchanged'
 else:
  match=[m for m in repair_rows if m['path']==z['path']];assert len(match)==1 and sha(b)==match[0]['before']['RAW_sha256'];z['version_relation']='approved_exact_metadata_only_replacement';z['approved_mapping']=match[0]
 hist.append(z)
cell_before=next(z for z in rd['approved_rows'] if z['path']==cellpath.relative_to(R).as_posix())
cb=R/cell_before['before']['path'];cz=snaps(cb,'historical-cell-before-overlay',0)
cz['path']=cellpath.relative_to(R).as_posix();cz['version_relation']='approved_exact_metadata_only_replacement';cz['final_current']=pin(cellpath);cz['approved_mapping']=next(q for q in repair_rows if q['path']==cz['path']);hist.append(cz)
assert len(hist)==7 and sum(z['version_relation']=='approved_exact_metadata_only_replacement' for z in hist)==2
source_names=['lease.final.json','manifest.final.json','stageA.freeze74.json','stageA.manifest74.json','source-expectations.before-header74.json','source95-item-classification74.json','source-inputs74.json','source-formulas21.exact74.json','source-proof-graph74.json','source-obligations26.before-header74.json','header74.coverage-projection.json','header74.binders-definitions-clauses.review.json','source-header.0.decision.json','source-header.0.review.md','source-header.0.run.json','header74.proposed.exactraw.snapshot.lean','root.statement-seal74.exactraw.snapshot.json','stageA.complete-named-source-payload74.json']
source_pins=[pin(PRE/n) for n in source_names]
for z in load(PRE/'manifest.final.json')['members']:check(z)
source_input=load(PRE/'source-inputs74.json');primary_pin=source_input['primary'];check(primary_pin)
protocol_paths=[freeze_path,RUN/'mathematics-freeze74.json',RUN/'expanded74.frozen.header.lean',R/'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean',R/'lean-toolchain',R/'lake-manifest.json',R/'tools/astis_semantic_roundtrip_core.py',R/'tools/astis_semantic_roundtrip.py',R/'tools/astis_publication.py',recon_path]
inputs={'LF_recipe':'Replace CRLF byte pairs with LF only; preserve bare CR and every other byte','current_input_count':len(final_current),'final_current_inputs':final_current,'source_contract_input_count':len(source_pins),'immutable_source_contract_inputs':source_pins,'protocol_and_freeze_inputs':[pin(p) for p in protocol_paths],'repair_authority_inputs':[pin(p) for p in repair_paths],'primary_reference':primary_pin,'historical_versions':hist,'historical_version_count':len(hist),'approved_historical_to_current_replacements':repair_rows,'repair_authority_count':len(repair_paths),'only_reader_metadata_two_fields_changed':True,'no_recursive_old_native_copies':True,'earlier_source_first_reaffirmation':pin(O/'source-baseline-reaffirmation74.json')}
write('source.0.input-manifest.json',inputs)

coverage=copy.deepcopy(prep);coverage['phase']='FINAL_INDEPENDENT_SOURCE_IMPLEMENTATION_AND_LOCAL_EXPOSITION_REVIEW'
coverage.update({'counts':dict(module_lines=211,source_regions=15,source_blocks=53,source_items=95,NODE=38,EXCLUDED=57,source_nodes=28,source_edges=52,internal_bridges_produced=13,source_callers=6,conclusions=10,lesson_steps=7),'unclassified':0,'all_source_classifications_unchanged':True,'local_source_math_exposition_accepted':True,'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':pin(packet_path)['RAW_sha256'],'publication_binding_sha256':binding_sha,'source_graph_not_Lean_dependency_graph':True,'current_source_nodes_N01_through_N24_produced_or_defined':True,'retained_source_context_N25_not_formal_parent':True,'N26_N27_N28_consumers_open':True,'reader_runtime_and_Exposition_Seal_accepted':False})
for q in coverage['95_source_item_projection']:q['final_semantic_admission']=True
for q in coverage['13_bridges']:
 q['final_admission_pending']=False;q['produced_internally']=True
 if q['node_id']=='N11':q['precision']='General total-division measurability is applied inside fun_prop for the actual S composition; no separately named public theorem for generic R measurability is claimed.'
for q in coverage['26_obligations']:
 q['final_decision']='satisfied within implemented deterministic source boundary; listed stochastic/reader/full-paper exclusions remain open'
write('source.0.coverage.json',coverage)

evidence_base='runs/20261007-companion-priority/pbps-actual-bounce-rate74/independent-source74'
slot_original={
 'objects':'Fixed PBPSv1 primary defines V on real Euclidean state, actual c=y-eta*gradV(xRef), h=gradV(x)-gradV(xRef), R_h with R0=I, actual S, sqrteta positive-part rate and SAME centered weighted SUM H. These are deterministic objects, not supplied kernels or certificates.',
 'domains':'Finite real Euclidean state and phase pairs; all y/reference/position/momentum and all normals including zero. eta>0 under original eta<=1/beta; zero energy and rank0 are not excluded. Standard Borel structures for joint state/reference maps.',
 'quantifiers':'Original global C2/Hessian conditions; arbitrary fixed y,xRef and arbitrary phase states. Reflection laws for every n,p; actual bounce/rate laws for every xRef,z. Same-H energy layer quantifies y,xRef,z0 first and z subject only to H(z)=H(z0). No actual stochastic path is quantified.',
 'assumptions':'Original0<alpha<=beta, V C2, both global Hessian bounds, eta>0,betaeta<=1. Gradient continuity and beta-Lipschitz/Borel/energy inequalities are internal proof ingredients; no nonzero-normal/positive-energy/extra-regularity/integrability premise.',
 'conclusion':'Selected bounded leaf: actual joint-Borel S; continuous/Borel nonnegative rate; exact R0/involution/norm/negative pairing; actual S fixes x/is involutive and preserves SAME H; exact flipped rate/rate difference and zero-residual laws; same-energy-layer radii and exact Lambda envelope. Full Proposition3.1 stochastic conclusions remain excluded.',
 'scopes':'Same V,eta and reference are used by c,h,S,rate,H in each clause. Position stays fixed at bounce. The same y,xRef determine both H(z0) and H(z) in the cap. Zero antecedent applies only to identity/zero-rate conclusion; no hidden provider or algorithm law.',
 'constant_dependencies':'Exact factor2/norm-normal-squared reflection; sqrteta positive-part rate; one-half weighted SUM H; radii sqrt(2E),sqrt(2etaE); Lambda=sqrteta*beta*sqrt(2E)*(sqrt(2etaE)+norm(c-xRef)). No existential or unspecified constants; alpha only in retained source hypotheses.'}
slot_evidence={
 'objects':'Source exact formulas21 and N06--N18; module25--34/72--79; decoder definitions exactly agree. Total real division realizes R0=I; complete private Prop is specification, not provider.',
 'domains':'Source S1.p1, eta S2.SS2.p1.1 and A1.SS1.p1; module17--24/62--69; finite-dimensional real Hilbert/Borel typing is an isometric elaboration of R^d, including rank0. No global continuity of S asserted.',
 'quantifiers':'Module35--59 and proof167--169 retain every input, same reference and branch. Decoder grouping of ten top-level conjuncts into seven prose items changes no quantifier or conjunction. The energy equality is a local conditional conclusion, not a new global analytic caller.',
 'assumptions':'Six caller prefix exact source-reviewed header, module106--111 uses QuadReg r=0 with original hV/hH and internal completeness. Strict alpha positivity, alpha<=beta,betaeta<=1 retained even though not needed by this bounded BODY. No certificate premise.',
 'conclusion':'Whole211-line review and all7 literal BODY/formula spans in source.0.coverage.json; source95 classification unchanged. Positive-part identity a_+-(-a)_+=a is an internal algebraic consequence of source normal-sign law. Paper path cap/nonexplosion is not claimed.',
 'scopes':'Actual S keeps its position, so h uses unchanged x/reference; H norm conservation lines141--143; same-H equality branch170--208. Decoder a renames xRef consistently. No arbitrary normal/rate/center substitutes for actual definitions.',
 'constant_dependencies':'Module28/32/34/55--59 and proof170--208; exact source A1.Ex4--6. QuadReg zero precision yields beta, not beta+eta^-1. No division by H0/cap, so zero energy and alphaeta1 remain legal.'}
slots={k:{'original':slot_original[k],'reconstructed':recon[k],'relation':'explicit-elaboration' if k in ['objects','domains','assumptions','conclusion'] else 'equivalent','evidence':slot_evidence[k]+' Evidence: '+evidence_base+'/source.0.coverage.json; primary:'+primary_pin['RAW_sha256']} for k in rt.SEMANTIC_SLOTS}
delta_specs=[
 ('domains','Finite-dimensional real Hilbert/Borel typing elaborates paper R^d and retains rank0.','S1.p1; module17--24/62--69; decoder domains. No dimension positivity caller.'),
 ('objects','Total real division gives the exact source R0=I extension.','S2.E4/A1.Ex3; module112 and zero-normal branch125--130/159--161.'),
 ('assumptions','Gradient continuity and beta-Lipschitz are produced internally, never assumed.','A1.SS1.p3.3/A1.SS2.p3; actual QuadReg specialization r=0 at106--111 with hV/hH.'),
 ('assumptions','All six standing callers persist; strict alpha positivity/order and betaeta cap are retained beyond the deterministic BODY needs.','Same sealed prefix; BODY uses hV,hH,h_eta. NNReal alpha/beta remain nonnegative; no source hypothesis is deleted.'),
 ('conclusion','Normal reflection and positive-part algebra supply exact flipped-rate/rate-difference auxiliary identities.','Source negative normal pairing and lambda definition; module144--158; a_+-(-a)_+=a for all real a.'),
 ('quantifiers','The cap is a deterministic SAME-H equality-layer statement, not a producer of actual initial-energy path conservation.','Source A1.Ex4--6 plus excluded recurrence rows; module52--59/167--208; decoder final quantifier order matches.'),
 ('conclusion','Only joint Borel bounce is required at zero residual; actual rate is continuous and hence Borel.','Source A1.SS1.p1.3/A1.SS2.p3; module131--136/165--166; no joint S-continuity assertion.'),
 ('scopes','Actual residual, center, reflection, rate and energy use the same potential/reference/scale within each clause.','Module25--34/72--79 and same-reference substitutions137--161; decoder consistently renames xRef to a.'),
 ('constant_dependencies','The cap preserves every exact source coefficient and uses beta from r=0.','A1.Ex4--6; module170--208; sqrteta*beta*sqrt(2E)*(sqrt(2etaE)+norm(c-xRef)), no unspecified constants or division by E.'),
 ('objects','Complete private literal Prop is a statement record, not a provider or certificate.','Module16--59 and public return70; named adjacent helper in unchanged lesson; actual proof follows full target.'),
 ('scopes','73 is a sibling deterministic edge, while clocks/path/nonexplosion/invariance/terminal/main/cost remain excluded real consumers.','Moduleimports1--3; independent source graph N25--N28 and57 EXCLUDED rows. Checkout INT73 is provenance, not formal parent.'),
 ('scopes','A stale process-reader sentence was corrected only under distinct exact two-field repair authority.','Independent exact_science63 CLOSED25 decision/run/lease, root32304 adoption. Two dead_code_audit values changed; module,lesson,source,assumptions,binding/context unchanged. Not a theorem repair.'),
 ('conclusion','All211 implementation lines,95 source items,13 internal bridges and7 formula/BODY spans are exhaustively source-reviewed without conflating source and Lean graphs.','source.0.coverage.json; source graph28/52 unchanged, N25 retained context and N26--N28 open. Browser/runtime/Exposition Seal remain outside this local exposition review.')]
deltas=[{'slot':a,'severity':'informational','description':b,'evidence':c+'; '+evidence_base+'/source.0.coverage.json'} for a,b,c in delta_specs]
assert len(slots)==7 and len(deltas)==13
analysis=(O/'prepacket.body-source-analysis74.md').read_text(encoding='utf-8')
final_analysis=analysis+'\nFinal packet qualification: the official frozen packet and native strict-blind reconstruction have now been compared in all seven slots. No blocking semantic difference or mathematical/source statement repair was found. Historical v0 and current publication/cell are related by exactly the two separately reviewed dead_code_audit substitutions; their binding and mathematical review_context are unchanged. Independent source implementation and local formula exposition are accepted for this bounded deterministic leaf only. This is not fresh mathematical compile, exact-SCI, repository/reader-runtime acceptance, Exposition Seal, PURIFIED, full-paper or VERIFIED credit.\n'
review={'reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'verdict':'equivalent-after-elaboration','blocking_semantic_deltas':0,'semantic_slots':slots,'deltas':deltas,'repairs':[],'whole_body_source_analysis':final_analysis,'source_before_candidate_and_BODY_reaffirmation':pin(O/'source-baseline-reaffirmation74.json'),'source_coverage':pin(O/'source.0.coverage.json'),'current_packet':pin(packet_path),'official_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':binding_sha,'publication_review_context_sha256':sha(can(context)),'approved_reader_metadata_only_mapping':repair_rows,'current_inputs_are_final_not_v0':True,'fresh_math_compile_or_other_verdict_used':False,'reader_boundary':'Complete private helper and exact7 adjacent BODY snippets/attributed formulas accepted locally. DOM/initial folds/browser/copy/download, serialized aggregate and Exposition Seal/PURIFIED remain separate.','truth_boundary':'Only actual deterministic zero-safe Borel bounce/rate, ten conclusions and same-H layer envelope. No actual random path/hazard/clocks/nonexplosion/Markov/invariance/terminal kernel/main/errors/cost/wholepaper/Goal completion.'}
write('source.0.review.json',review)
core={'schema':'ASTIS_NATIVE_INDEPENDENT_SOURCE_REVIEW74_V1','reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'fresh_math_compile_or_other_verdict_used':False,'input_manifest':pin(O/'source.0.input-manifest.json'),'coverage':pin(O/'source.0.coverage.json'),'review':pin(O/'source.0.review.json'),'complete_review':review,'source_baseline':pin(O/'source-baseline-reaffirmation74.json'),'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':pin(packet_path)['RAW_sha256'],'publication_binding_sha256':binding_sha,'counts':coverage['counts'],'local_source_math_exposition_accepted':True,'no_canonical_Git_ledger_or_old_CLOSED_writes':True,'VERIFIED_or_full_paper_credit':False}
core['run_sha256']=sha(can(core));write('source.0.run.json',core);h=core['run_sha256']
decision={'verdict':'equivalent-after-elaboration','blocking_semantic_deltas':0,'repairs':[],'semantic_slots':slots,'deltas':deltas,'reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'review_evidence':evidence_base+'/source.0.review.json','review_run_sha256':h,'reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':binding_sha,'source_review_scope':'whole211-line current implementation, source95 items/28node52edge/13bridges and7 exact local exposition BODY/formula steps; deterministic boundary only','approved_reader_metadata_repair_authority':pin(repair/'decision.json'),'mathematical_repairs':False,'VERIFIED_or_full_paper_credit':False}
write('source.0.decision.json',decision)
fields={'state':'source-reviewed','verdict':decision['verdict'],'semantic_slots':slots,'deltas':deltas,'source_review':{'state':'accepted','reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':packet['packet_sha256'],'evidence':evidence_base+'/source.0.review.json','review_run_sha256':h,'run_artifact':evidence_base+'/source.0.decision.json'},'repairs':[]}
accepted=copy.deepcopy(audit);accepted.update(fields)
assert rt.semantic_reviewer_packet(accepted)==packet
reg=rt.load_registry();reg['audits']=[accepted if a['id']==accepted['id'] else a for a in reg['audits']]
errors=rt.validate_registry(reg);assert not errors,errors
coverage_fields={'source_graph':(PRE/'source-proof-graph74.json').relative_to(R).as_posix(),'source_inventory':(PRE/'source95-item-classification74.json').relative_to(R).as_posix(),'coverage_report':pin(O/'source.0.coverage.json'),'coverage_status':'Independently source-reviewed current211-line actual deterministic bounce/rate implementation and7 exact BODY/formula steps;95 items classified38NODE57EXCLUDED,15regions53blocks21formulas,28nodes52edges unchanged,13 internal bridges produced,6 original callers10conclusions. N25 retained source context is not a formal74 parent; N26--N28 stochastic/path/kernel/main/cost consumers remain open. This is source/local-exposition admission only, not Exposition Seal/PURIFIED/whole-paper/VERIFIED.'}
newitem=copy.deepcopy(item);newitem['source_proof_coverage']=coverage_fields
assert pub.binding_digest(newitem,newitem['bindings'][0],data)==binding_sha and pub.review_context(newitem,newitem['bindings'][0],data)==context
admission={'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':pin(packet_path)['RAW_sha256'],'publication_binding_sha256':binding_sha,'audit_fields':fields,'cell_source_proof_coverage':coverage_fields,'publication_source_proof_coverage':coverage_fields,'semantic_reviewer_packet_before_after_admission_equal':True,'binding_and_review_context_unchanged_by_coverage_fields':True,'native_source_verdict_only':True,'no_canonical_changes_applied':True}
write('source.0.admission-fields.json',admission)
write('terminal.final-source74.receipt.json',{'actual_PID':os.getpid(),'EXIT':0,'argv':sys.argv,'current_frozen_inputs_verified':8,'historical_versions':7,'source_contract_inputs':18,'protocol_and_freeze_inputs':10,'repair_authority_inputs':9,'two_approved_metadata_replacements':True,'registry_validation_errors':0,'semantic_reviewer_packet_before_after_equal':True,'binding_context_equal':True,'canonical_Git_ledger_old_CLOSED_writes':False,'no_fresh_Lean_compile_or_other_math_verdict':True})
names=['source.0.run.json','source.0.decision.json','source.0.review.json','source.0.input-manifest.json','source.0.admission-fields.json']
named={'whole_logical_run_sha256':h,'named_payload_count':5,'named_payloads':[{'name':n,'pin':pin(O/n),'complete_RAW_UTF8':(O/n).read_bytes().decode('utf-8')} for n in names],'all_exact_input_snapshots_and_coverage_are_separately_bound_by_whole_owned_manifest':True,'no_recursive_historical_base64':True}
write('complete-named-review-decision-input-payload.json',named)
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'whole_logical_run_sha256':h,'decision':pin(O/'source.0.decision.json'),'admission':pin(O/'source.0.admission-fields.json'),'named_payload':pin(O/'complete-named-review-decision-input-payload.json'),'current_historical_source_protocol_repair_counts':[8,7,18,10,9],'registry_errors':0,'not_closed_yet':True},ensure_ascii=True))
