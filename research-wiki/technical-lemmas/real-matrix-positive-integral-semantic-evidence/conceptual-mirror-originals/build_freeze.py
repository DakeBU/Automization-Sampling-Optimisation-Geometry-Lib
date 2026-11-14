from pathlib import Path
import json,hashlib,datetime,re
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261112/mp_sg_52ad/conceptual-v1';PACKET=ROOT/'.astis/huanjian-real-matrix-positive-integral-20261112/bounded-conceptual-mirror-input.json'
def sha(b):return hashlib.sha256(b).hexdigest()
pb=PACKET.read_bytes();assert sha(pb)=='3dca2559371bb1f502d31c83448e1acaee33b9598853d10f3dbf8a99a3ece6f6';s=pb.decode();p=json.loads(s)
assert not (OUT/'freeze-manifest.json').exists(),'Do not overwrite a conceptual freeze.'
(OUT/'inputs').mkdir(exist_ok=True)
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def write(n,t):(OUT/n).write_text(t,encoding='utf-8')
(OUT/'inputs/bounded-conceptual-mirror-input.json').write_bytes(pb)
dec=json.JSONDecoder()
def object_fields(text):
 i=0
 while text[i].isspace():i+=1
 assert text[i]=='{';i+=1;out={}
 while True:
  while text[i].isspace() or text[i]==',':i+=1
  if text[i]=='}':break
  key,end=dec.raw_decode(text,i);i=end
  while text[i].isspace():i+=1
  assert text[i]==':';i+=1
  while text[i].isspace():i+=1
  start=i;val,end=dec.raw_decode(text,i);out[key]=(start,end,val);i=end
 return out
fields=object_fields(s);a,z,_=fields['existing'];i=a+1;record_slices=[]
while True:
 while s[i].isspace() or s[i]==',':i+=1
 if s[i]==']':break
 start=i;obj,end=dec.raw_decode(s,i);record_slices.append((start,end,obj));i=end
assert [o for _,_,o in record_slices]==p['existing']
pres=[]
for index,(a,z,obj) in enumerate(record_slices):
 text=s[a:z];raw=text.encode();name=f'inputs/existing-record-{index}.raw.json';(OUT/name).write_bytes(raw)
 fs=object_fields(text);ma,mz,metadata=fs['metadata'];sa,sz,status=fs['status']
 assert metadata==obj['metadata'] and status==obj['status']
 pres.append({'discovery_id':obj['discovery_id'],'bridge_id':metadata['bridge_id'],'family_id':metadata['family_id'],
  'historical_status_preserved':status,'action':'PRESERVE_IDENTITY_METADATA_AND_STATUS_UNCHANGED','revalidation_or_recertification':False,
  'record_raw_snapshot':name,'record_exact_raw_sha256':sha(raw),'metadata_exact_raw_sha256':sha(text[ma:mz].encode()),'status_exact_raw_sha256':sha(text[sa:sz].encode()),
  'source_packet_char_start':a,'source_packet_char_end_exclusive':z,'source_packet_utf8_start':len(s[:a].encode()),'source_packet_utf8_end_exclusive':len(s[:z].encode()),
  'new_compiled_edges':[],'new_formal_credit':False,
  'current_ledger_check':'Packet/parent reports metadata and status just checked against current discovery ledger. This actor does not reread ledger or independently recertify that check.',
  'historical_meaning':'Preserved historical conceptual status only; no source or new-target proof acceptance follows.'})
assert [(x['discovery_id'],x['historical_status_preserved']) for x in pres]==[
 ('ASTIS-DISC-20261007-GaussianSymmetryPushforwardRepaired','merged'),
 ('ASTIS-DISC-20261111-GaussianRadialWeightedMatrixSymmetry','validated')]
dump('existing-identities-preservation.json',{'input_packet_sha256':sha(pb),'records':pres,'all_metadata_values_preserved_verbatim_in_raw_snapshots':True,'no_ledger_writes':True,'no_historical_status_revalidation':True})
sealbindings=[]
for target in p['sealed_targets']:
 signatures=[]
 for key in ['producer','actual_consumer','actual_private_consumer']:
  if key in target:
   b=target[key]['signature'].encode();assert sha(b)==target[key]['signature_sha256']
   signatures.append({'role':key,'name':target[key]['name'],'signature_sha256':sha(b)})
 sealbindings.append({'seal_id':target['seal_id'],'state_preserved_from_packet':target['state'],'signatures':signatures,'compiled_new_target_credit':False})

shared={
 'sau_id':'ASTIS-SA-20261112-RealMatrixPositiveIntegral','conceptual_mirror_audit':{'status':'none-found','new_candidate_count':0,'new_discovery_ids':[]},
 'judgment':'No new conceptual correspondence is supported by this bounded input. The advance selects a canonical real-matrix PSD specialization and centralizes repeated uses of the same closed-convex integral provider.',
 'canonical_Lean_node_rule':{'upstream_same_API':'Convex.integral_mem','planned_canonical_node':'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef',
  'meaning':'Exact reuse of one theorem/specialization across residuals and centered-square integrals belongs to one canonical Lean node with concrete application obligations; it does not create a pair of conceptual source mechanisms.',
  'new_node_state':'Sealed and unproved in the bounded input. No call or compiled edge is observed or awarded.'},
 'hypothesis_key_estimate_conclusion_review':{
  'hypotheses':'Arbitrary probability mu; actual integrable matrix-valued f; AE full Hermitian/quadratic PSD. PSD-cone closedness/convexity and actual norm/Bochner applicability remain internal.',
  'key_step':'Closed-convex expectation membership specialized to the PSD cone, equivalently preserving an AE nonnegative matrix residual under expectation.',
  'conclusion':'Full PSD of the actual Bochner integral. No Gaussian coefficient, second-moment sum, variance norm or concentration follows from this bridge alone.',
  'failure_boundary':'Missing integrability, AE full PSD or correct topology prevents the proposed application. Generic hf/hpos cannot become caller premises in the unchanged Gaussian theorem. A scalar/entrywise-positive observation alone is not full matrix PSD.'},
 'comparisons_considered':[
  {'comparison':'Repeated PSD integral uses in older private R4/R5 and actual R9 residual/square expectations','disposition':'canonical-reuse','reason':'The same Convex.integral_mem mechanism/API is being centralized. These are not independently sourced domain transports and no new compiled application is observed.'},
  {'comparison':'Generic closed-convex barycenter statement versus finite real PSD specialization','disposition':'canonical-specialization','reason':'A literal specialization of one provider with geometry applicability obligations is not a new conceptual pair. Paper p14 supplies application need, not a second printed generic theorem.'},
  {'comparison':'Existing Gaussian symmetry-pushforward or radial-weighted matrix records','disposition':'not-a-new-correspondence','reason':'The generic PSD-integral contract needs no Gaussian law symmetry, sign/permutation invariance, radial weight or moment evaluation. Formula-level expectation similarity does not supply a valid new hypothesis/conclusion transport.'}],
 'existing_records_considered':[x['discovery_id'] for x in p['existing']],
 'new_candidate_payloads':[],'failure_class':'NONE','mathematical_route_retired':False,'proof_or_status_authority':False}
variance={
 'sau_id':'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance','conceptual_mirror_audit':{'status':'none-found','new_candidate_count':0,'new_discovery_ids':[]},
 'judgment':'The bounded packet exposes exact source composition and canonical reuse, while the radial-weighted symmetry correspondence is already recorded. No additional source-backed conceptual pair with distinct hypothesis/key-estimate/conclusion/failure maps is established here.',
 'hypothesis_key_estimate_conclusion_review':{
  'hypotheses':'Actual original-column standard Gaussian experiment; literal source half-grid, closed truncation and ordinary matrix products; only natural d,q and2q+1<d as public source inputs. Law/moment/PSD/integrability/frame/mean/norm proofs remain internal.',
  'key_estimates':['Actual radial fourth matrix moment gives r+2, followed by positive cutoff dropping and literal ||t_i||^2<=2r/unweighted frame aggregation.','Centering subtracts the PSD actual mean square; deterministic cosine weighting contributes w_i^2<=1.','Full PSD upper/lower bounds must be converted to both actual Euclidean operator-norm variance conclusions.'],
  'conclusion':'Actual uncentered square mean sum PSD bound and actual centered/weighted squared-mean norm bounds with2r(r+2)/d; all new targets remain unproved in this input.',
  'failure_boundary':'Finite first radial moment alone cannot supply unbounded fourth-moment integrability; wrong weight/law destroys the radial cancellation. Generic PSD integration alone supplies neither coefficient nor norm variance. Wrong product/norm/measure or guessed actual means invalidate the application; no source concentration or main lower bound is licensed.'},
 'comparisons_considered':[
  {'comparison':'Ex108 truncated radial moment versus Ex113 radial fourth matrix moment','disposition':'already-recorded','existing_id':'ASTIS-DISC-20261111-GaussianRadialWeightedMatrixSymmetry','reason':'The existing validated record already maps sign/permutation/trace mechanism, distinct retained versus fourth-moment integrability estimates, coefficient evaluations and failure boundary. Reusing it for an actual-source consumer does not create a new mirror or upgrade its historical compiled claims.'},
  {'comparison':'Cutoff residual, centered-square positivity and cosine-square domination','disposition':'canonical-reuse-and-source-composition','reason':'These use the same planned PSD-integral node and standard actual matrix order/algebra. Distinct residual functions are applications of that generic contract, not two source mechanisms requiring a new functor record.'},
  {'comparison':'Physical Gaussian-row law transport versus prior Gaussian symmetry-pushforward record','disposition':'canonical-law-reuse','existing_id':'ASTIS-DISC-20261007-GaussianSymmetryPushforwardRepaired','reason':'No new linear symmetry/generative-map correspondence, covariance calibration or independently sourced domain transport is furnished. Exact reuse of existing Gaussian law APIs remains canonical, while the merged historical record stays unchanged.'},
  {'comparison':'Matrix centering versus an abstract scalar/Hilbert covariance or positive-map theory','disposition':'outside-bounded-evidence','reason':'No second independent source/result with a complete hypothesis/key-estimate/conclusion/failure map is supplied. Inventing that source to manufacture a new candidate is unwarranted; this does not mathematically refute such a future correspondence.'}],
 'existing_records_considered':[x['discovery_id'] for x in p['existing']],
 'canonical_Lean_node_rule':'Same actually invoked row-law/radial-moment/frame/mean/Convex.integral_mem APIs should remain shared canonical nodes. Packet names and imports do not certify their new target applications.',
 'new_candidate_payloads':[],'failure_class':'NONE','mathematical_route_retired':False,'proof_or_status_authority':False}
dump('RealMatrixPositiveIntegral.audit.json',shared);dump('GaussianComplexitySourceMatrixVariance.audit.json',variance)
dump('per-sau-results.json',{'input_packet_sha256':sha(pb),'sealed_target_bindings':sealbindings,'audits':[shared,variance],
 'new_conceptual_candidates':[],'discovery_creation_requested':p['discovery_creation_requested'],'discovery_created':False,
 'no_second_source_fabricated':True,'no_equivalence_functor_or_Lean_implication_claim':True,'new_compiled_credit':False,
 'existing_identities_and_statuses':[{'discovery_id':x['discovery_id'],'status':x['historical_status_preserved'],'action':'preserve without revalidation'} for x in pres]})
exposure={'input_path':str(PACKET.relative_to(ROOT)),'input_exact_bytes':len(pb),'input_sha256':sha(pb),
 'allowed_scope':'Only this bounded packet was opened for the conceptual-v1 audit. No source/raw/type/graph original, implementation/API, ledger/advance/registry/C/Git file was read or changed by this conceptual task.',
 'input_contents':'Two existing conceptual metadata/status records and full new exact seals/environment/exposure metadata. This is conceptual/source-facing context, NOT a blind-decoder packet and NOT a new independent source verdict.',
 'historical_verification_boundary':'existing_metadata_and_status_checked_current=true is a packet/parent report. Current discovery ledger was not queried by this actor; historical merged/validated statuses are preserved, not recertified.',
 'prior_actor_exposure':'Earlier independent source/type/background graph tasks are known to this actor. Those exposures cannot be erased; this conceptual audit does not claim source/API blindness. Their artifacts were not reopened or altered in this task.',
 'formalizer_API_pristine':False,'new_target_proof_implementation_seen':False,
 'unproved_boundaries':'Both new targets are UNPROVED according to the bounded seals. No existing mirror status, receipt name, API name or metadata grants them compiled/source-complete credit.',
 'independence_of_judgment':'Each SAU is assessed separately. none-found reflects exact canonical reuse, existing correspondence coverage and bounded source support, not a requested/expected verdict.',
 'writes':'New conceptual-v1 directory only. No discovery/advance/C/registry/Git mutation, no permission/status/compiled credit grant.'}
dump('inputs-and-exposure.json',exposure)
write('decision.md','Both SAUs receive conceptual_mirror_audit.status=none-found. The shared real-matrix bridge centralizes one canonical PSD expectation specialization; repeated residual/square applications of the same API are not a new conceptual pair. The variance packet uses the already-recorded Gaussian radial-weighted symmetry correspondence plus exact source order/centering/frame/norm composition. No additional bounded source supports a new complete mechanism correspondence. Existing transport:gaussian-symmetry-pushforward remains historical merged and transport:gaussian-radial-weighted-matrix-symmetry remains historical validated, with exact raw metadata preserved and no revalidation. Both new targets remain unproved, and no compiled edge, equivalence, functor or Lean implication is awarded.\n')
write('README.md','Independent per-SAU conceptual audit from the sole bounded packet. Read per-sau-results.json, both SAU audit files, existing-identities-preservation.json and inputs-and-exposure.json. Existing metadata/status records are preserved in exact raw input snapshots. No discovery/advance or other shared state is changed. No source/type/graph originals are altered.\n')
manifest={'format':'astis-bounded-per-sau-conceptual-freeze-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actor':'/root/row_indep_source_graph_78c2','input_packet_sha256':sha(pb),'scope':'Two independent per-SAU conceptual audits; no proof/status/API authority.','files':[]}
for f in sorted(OUT.rglob('*')):
 if f.is_file():b=f.read_bytes();manifest['files'].append({'path':str(f.relative_to(OUT)),'bytes':len(b),'sha256':sha(b)})
dump('freeze-manifest.json',manifest);dig=sha((OUT/'freeze-manifest.json').read_bytes());write('freeze-manifest.sha256',dig+'  freeze-manifest.json\n')
for f in OUT.rglob('*'):
 if f.is_file():f.chmod(0o444)
for d in sorted([d for d in OUT.rglob('*') if d.is_dir()],key=lambda d:len(d.parts),reverse=True):d.chmod(0o555)
OUT.chmod(0o555)
print(json.dumps({'conceptual_path':str(OUT),'shared_status':'none-found','variance_status':'none-found','shared_audit_sha256':sha((OUT/'RealMatrixPositiveIntegral.audit.json').read_bytes()),'variance_audit_sha256':sha((OUT/'GaussianComplexitySourceMatrixVariance.audit.json').read_bytes()),'per_sau_results_sha256':sha((OUT/'per-sau-results.json').read_bytes()),'preservation_sha256':sha((OUT/'existing-identities-preservation.json').read_bytes()),'exposure_sha256':sha((OUT/'inputs-and-exposure.json').read_bytes()),'freeze_manifest_sha256':dig,'existing_statuses':[(x['discovery_id'],x['historical_status_preserved']) for x in pres],'new_compiled_credit':False},indent=2))
