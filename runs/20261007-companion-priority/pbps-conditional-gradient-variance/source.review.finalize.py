import datetime as dt
import hashlib
import json
import pathlib
import sys
import types

sys.dont_write_bytecode = True
sys.path[:0] = ['tools', 'website/scripts']
import astis_semantic_roundtrip_core as rt
import astis_publication as pub

ROOT = pathlib.Path.cwd()
RUN = ROOT / 'runs/20261007-companion-priority/pbps-conditional-gradient-variance'
def h(b): return hashlib.sha256(b).hexdigest()
def canon(o): return h(json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8'))
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def write(p, o): pathlib.Path(p).write_bytes((json.dumps(o, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
def pin(p):
    p = pathlib.Path(p); b=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(), 'raw_sha256':h(b), 'lf_sha256':h(b.replace(b'\r\n',b'\n')), 'bytes':len(b)}
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()

lease = read(RUN/'source.review.lease.json')
own = read(RUN/'reviewer.source.lease.json')
assert lease['status']=='OPEN' and own['status']=='OPEN'
packet = read(RUN/'source.0.reviewer-packet.json')
audit = read(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientVariance.json')
item = read(ROOT/'website/content/publications/pbps-conditional-gradient-variance.json')['items'][0]
unit = read(ROOT/'website/content/declaration_lessons/pbps-conditional-gradient-variance.json')['units'][0]
name = packet['lean']['declaration']
data = {'declarations':{name:types.SimpleNamespace(source_file=packet['lean']['file'])},'lessons':{name:unit}}
assert rt.semantic_reviewer_packet(audit)==packet
assert pub.binding_digest(item,item['bindings'][0],data)==packet['publication_binding_sha256']
assert pub.review_context(item,item['bindings'][0],data)==packet['candidate_publication_context']
for a in lease['input_artifacts']:
    q=pin(ROOT/a['path'])
    assert q['raw_sha256']==a['raw_sha256'] and q['lf_sha256']==a['lf_sha256'],a['path']
decoder=read(RUN/'anonymous-decoder/result0.json')
drun=read(RUN/'anonymous-decoder/run.json')
assert canon(drun['execution_payload'])==decoder['decoder_run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
assert decoder['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert h(decoder['reconstructed_theorem_text'].encode())==packet['blind_reconstruction']['text_sha256']
assert audit['reconstruction']['input_artifacts']==['lean-statement','approved-definition-context']
initial=RUN/'anonymous-decoder/initial-lease.raw.snapshot.json'
assert pin(initial)['raw_sha256']==drun['input_artifacts'][1]['raw_sha256']
assert canon({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']
assert h(packet['source']['original_text'].encode())==packet['source']['text_sha256']
assert h(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']

prod=ROOT/packet['lean']['file']; code=prod.read_text(encoding='utf-8')
assert code==packet['candidate_publication_context']['current_lean_module']
assert 'InnerProductSpace.inner_gradient_left' in unit['mathlib_dependencies']
assert 'inner_gradient_left' in code
missing='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg'
assert missing in code and missing not in unit['astis_dependencies']
assert item['chapter_path']=='example-cases/samplewiki/companions/proximal-bouncy-particle-sampler.html'
front=read(ROOT/'website/content/samplewiki_companion_frontiers.json')
assert any(c['slug']=='proximal-bouncy-particle' for c in front['cases'])
g=(ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean').read_text(encoding='utf-8')
assert 'lemma inner_gradient_left' in g and not any(x.startswith('namespace ') for x in g.splitlines()[:291])
vf=(ROOT/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean').read_text(encoding='utf-8')
assert 'theorem variance_nonneg' in vf

formula_checks=[]
formulas=[('publication formulae/0/tex',item['formulae'][0]['tex']),('lesson formula',unit['formula'])]+[(f'lesson steps/{i}/formula',s['formula']) for i,s in enumerate(unit['steps'])]
for label,s in formulas:
    formula_checks.append({'field':label,'actual_double_backslash_count':s.count('\\\\'),'actual_backslash_count':s.count('\\'),'encoding_correct':s.count('\\\\')==0})
assert all(x['encoding_correct'] for x in formula_checks)
assert '\\n' not in packet['source']['original_text']

extras=[ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'website/scripts/samplewiki_companions.py',ROOT/'website/scripts/declaration_lessons.py',ROOT/'website/scripts/samplewiki_reader_contract.py',ROOT/'tools/astis_publication.py',ROOT/'tools/astis_semantic_roundtrip_core.py',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean']
additional=[pin(x) for x in extras]
snapshot_paths=[RUN/'source.0.reviewer-packet.json',RUN/'source.review.lease.json',prod,ROOT/'Tests/ProximalBPSConditionalGradientVariance.lean',ROOT/'website/content/declaration_lessons/pbps-conditional-gradient-variance.json',ROOT/'website/content/publications/pbps-conditional-gradient-variance.json',ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientVariance.json',RUN/'anonymous-decoder/result0.json',RUN/'anonymous-decoder/run.json',RUN/'anonymous-decoder/packet0.json',initial,ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread48/primary.contract.json',ROOT/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html',*extras]
snaps=[]
for i,p in enumerate(snapshot_paths):
    target=RUN/f'source.review.frozen.{i:02d}.raw.snapshot{p.suffix}'
    assert not target.exists()
    target.write_bytes(p.read_bytes());snaps.append({'source':pin(p),'snapshot':pin(target)})

orig={
 'objects':'Source mu=normalized exp(-V) volume; J law(X,X+sqrt(eta)Z); R true conditional of X|Y, S reflected x->2x-y; Tf expectation under S, actual Riesz gradient and centered-square variance. Parameter-y unnormalized score is centered by covariance.',
 'domains':'Printed finite Euclidean source with real smooth compact f. Explicit authored finite real Hilbert/Borel representation includes dimension zero. No extra CompleteSpace, Nontrivial or supplied domain hypotheses.',
 'quantifiers':'Source standing data precede one pair R/S; exact every-y reflected density; same S precedes every smoothcompact f and every y; true differentiability and inequality are pointwise. No joint domain selector or operator-choice equality.',
 'assumptions':'V globally C2, 0<alpha<=beta, actual evaluated Hessian bounds everywhere, eta>0 and beta*eta<=1. Only f carries globally smooth+compact support. Kernels, moments, derivative, covariance and variance estimates are derived outputs.',
 'conclusion':'Literal Ex7 norm(gradient Tf(y))^2 <= (eta^-1-alpha)^2/(4(alpha+eta^-1))*Var_{S(y)}(f), with actual differentiability and internally constructed true Markov/disintegration/reflection/density witnesses.',
 'scopes':'Only the smoothcompact pointwise C.1 ingredient. C.2 formula outer integration inside C.1, B.13 and rough gradient closure are separate; actual subsection C.2 half-turn and all main/error/work/composition remain outside. The proof uses its own G instead of the printed unit-direction supremum; same true law identified internally without asserting R or D identity.',
 'constant_dependencies':'Exact C_eta=(eta^-1-alpha)^2/[4(alpha+eta^-1)]. Reflected midpoint 1/2, quadratic 1/(8eta), parameter score factors 1/2 and 1/(4eta), reflected curvature quarter. Beta only constrains admissible eta and curvature; no dimension factor. Alpha=beta=eta=1 gives C=0.'}
ev={
 'objects':'Production constructs actual J/R/S through ConditionalScore; hSS rewrites the every-y two density formulas and subst transports score variance. hcov evaluates hfd.fderiv at G and uses global inner_gradient_left; no posterior/RGO law substitution.',
 'domains':'Reviewed whole imports/body and approved definitions. Compact continuity produces bounded f and MemLp2 under actual Markov S. Admissible produces score L1 and centered-square L1; L2-space representatives are linked a.e. through coeffFn_toLp. Both actual tests cover Gaussian precision and rank zero.',
 'quantifiers':'Exact sealed1356 and anonymous reconstruction have the same binder order and conjunctions. Kernel ext equality uses all y, then only S is substituted; R prime is not identified, no arbitrary a.e. version is substituted for a smooth density.',
 'assumptions':'All source binders retained; alpha/beta NNReal is a representation of positive source curvature, not a strengthened hypothesis. No public integrability/probability/PI/covariance/selector certificate. OriginalG is an actual gradient, not a supplied output.',
 'conclusion':'Whole local hpair proves genuine L2 inner-product integrals; hcs real CS and hcov lead to normG^4 <= Varf*VarY, hYvar plus variance_nonneg, with zero and positive norm cancellation treated separately. Every implication uses produced domains.',
 'scopes':'All six formula steps match this own-gradient equivalent route and preserve outer/rough boundaries. Source provenance/delivery metadata blockers below do not falsify or alter the source theorem. Tests assert their stated actual kernel/reflection and zero-gradient outputs; they do not independently assert every production conjunction.',
 'constant_dependencies':'Source raw physical4650 A3.Ex7 and production exact coefficient match. Source raw4612/4593 yields the quarter/parameter derivative scales. Positivity and zero case are proved internally; no unit vector requirement fails at rank zero.'}
slots={k:{'original':orig[k],'reconstructed':decoder[k],'relation':'explicit-elaboration' if k in ['objects','domains','scopes'] else 'equivalent','evidence':ev[k]} for k in orig}

issues=[
 {'slot':'scopes','severity':'blocking','description':'Publication provenance names a nonexistent qualified Mathlib declaration InnerProductSpace.inner_gradient_left. The actual directly invoked declaration is global inner_gradient_left.','evidence':'lesson /units/0/mathlib_dependencies/5; production line91; Mathlib Analysis/Calculus/Gradient/Basic.lean line291, no enclosing namespace.'},
 {'slot':'scopes','severity':'blocking','description':'Direct ASTIS proof-parent table omits the actually called Poincare.variance_nonneg, used in the positive/zero-aware cancellation.','evidence':'lesson /units/0/astis_dependencies lists only two conditional producer parents; production lines105 and110 directly invoke AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg; its declaration Poincare.lean:52.'},
 {'slot':'scopes','severity':'blocking','description':'Publication chapter_path targets an ungenerated companion slug proximal-bouncy-particle-sampler rather than the actual canonical proximal-bouncy-particle.','evidence':'publication /items/0/chapter_path; frontiers /cases/2/slug; samplewiki_companions.py:317 emits BASE+row[slug]+.html.'}]
repairs=[{'kind':'metadata-only-provenance','location':'website/content/declaration_lessons/pbps-conditional-gradient-variance.json /units/0/mathlib_dependencies/5','proposed_change':'Replace InnerProductSpace.inner_gradient_left with inner_gradient_left. No theorem/proof/source change.'},
 {'kind':'metadata-only-provenance','location':'website/content/declaration_lessons/pbps-conditional-gradient-variance.json /units/0/astis_dependencies','proposed_change':'Append exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg. Do not replace the two actual conditional parents.'},
 {'kind':'reader-locator-only','location':'website/content/publications/pbps-conditional-gradient-variance.json /items/0/chapter_path','proposed_change':'Replace with example-cases/samplewiki/companions/proximal-bouncy-particle.html.'}]
checks={'schema_version':1,'reviewer':'phase_source_reviewer_20261005','verified_utc':utc(),'all_frozen_inputs':lease['input_artifacts'],'count':len(lease['input_artifacts']),'all_raw_LF_matching':True,'additional_reader_API_checks':additional,'canonical_reviewer_packet_rebuilt_exact':True,'canonical_publication_payload_and_current_context_rebuilt_exact':True,'portable_decoder_payload_hash_recomputed':decoder['decoder_run_sha256'],'portable_decoder_run_raw_hash':pin(RUN/'anonymous-decoder/run.json')['raw_sha256'],'decoder_original_text_and_seven_strings_unchanged':True,'decoder_input_artifact_labels':['lean-statement','approved-definition-context'],'acyclic_execution_basis':'execution_payload excludes output/run references; original initial lease exact bytes independently matched','formula_encoding_checks':formula_checks,'source_original_actual_newlines':packet['source']['original_text'].count('\n'),'source_original_literal_backslash_n':0,'no_encoding_repair_necessary':True,'immutable_snapshots':snaps,'compiler_started':False}
checks['checks_run_sha256']=canon(checks)
write(RUN/'source.review.checks.json',checks)
result={'schema_version':1,'reviewer':'phase_source_reviewer_20261005','status':'BLOCKED_METADATA_PROVENANCE_AND_READER_LOCATOR_ONLY','verdict':'source-underspecified','blocking':True,'mathematical_source_comparison':'equivalent-after-elaboration','verdict_explanation':'Blocking applies to current publication provenance/delivery metadata, not a missing printed source hypothesis, false theorem, or changed mathematical statement. All seven mathematical slots agree after explicit finite-Hilbert/zero-dimension and own-gradient elaboration. Separate root repair and independent overlay review are required before accepting this current publication binding.','reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'semantic_slots':slots,'deltas':issues,'repairs':repairs,'source_excess':[],'independent_from_formalizer':True,'independent_from_decoder':True,'roles':packet['roles'],'review_evidence':'Own immutable primary48 contract was read before current implementation/reconstruction. Independently read pinned PBPS v1 standing352-358 and full C.1 density/score/quarter-curvature/CS/Ex7 chain, compared whole current production, both complete Tests and all six reader formula steps; reconstructed canonical publication/packet and portable decoder execution hash, checked all215 raw/LF frozen inputs. Mathematical Ex7 boundary is faithful with no extra public premise, but current metadata has three precise blocking defects: false qualified gradient API, omitted direct variance_nonneg parent, and wrong companion slug. Formula strings are already single-backslash and source.original_text has genuine newlines; no encoding repair is justified. No compiler, mathematical-verdict substitution, canonical edit or source completion admission.','review_evidence_details':ev,'input_artifacts':lease['input_artifacts'],'additional_input_artifacts':additional,'whole_module_covered':True,'whole_module_file_sha256':pin(prod)['raw_sha256'],'whole_module_file_lf_sha256':pin(prod)['lf_sha256'],'whole_module_private_coverage':'No top-level private declarations; all local have providers hSS/hpair/hcov/hnorm/hbound and both cancellation branches inspected. Complete imports, namespace and proof tail covered.','test_input':pin(ROOT/'Tests/ProximalBPSConditionalGradientVariance.lean'),'source_primary':pin(ROOT/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'),'primary_first_contract':pin(ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread48/primary.contract.json'),'source_read_anchors':['standing physical352-358','S2.SS2 actual Gaussian augmentation and reflection','C.1 physical4574-4653, A3.Ex1/Ex2/A3.E1/Ex3-Ex7','4653-4665 outer formula(C.2) excluded, actual C.2 starts4897'],'statement_sha256':packet['lean']['statement_sha256'],'source_text_sha256':packet['source']['text_sha256'],'reconstruction_sha256':packet['blind_reconstruction']['text_sha256'],'decoder_packet_sha256':packet['blind_reconstruction']['decoder_packet_sha256'],'decoder_run_sha256':decoder['decoder_run_sha256'],'checks_artifact':pin(RUN/'source.review.checks.json'),'exposure':{'historical_PBPS_and_SPHMC_source_and_prior_proof_reviews_known':True,'own_primary48_before_candidate_and_body':True,'preproof_binder_and_independent_topology_reviews_reused_by_exact_frozen_hash':True,'repaired_source_graph_creator':'original independent gauss; root representation-only repair, reviewer independently admitted','current_packet_embeds_prior_source_only_topology_receipt':'Disclosed authorized topology provenance; not used to infer mathematical fidelity.','current_whole_math_verdict_read':False,'compiler_started':False,'root_observations':'Root suggested locator/encoding issues during review; independently checked bytes/rendering rules. Locator is defective; encoding conjecture is false and no replacement is authorized by this review.'},'remaining_boundary':'Pointwise smoothcompact Ex7 only. Outer(C.2), B.13, rough-domain closure, actual subsection C.2 half-turn, sampler/main/errors/work/cost/composition and full browser/live/CopyDownload/PURIFIED remain separate. No new theorem credit from a metadata repair.','started_utc':own['opened_utc'],'finished_review_utc':utc(),'hash_recipe':'SHA256 UTF8 json.dumps(entire object minus review_run_sha256,ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False)','leases_at_return':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED','compiler_started':False}}
result['review_run_sha256']=canon(result)
out=RUN/'source.0.review.json';assert not out.exists();write(out,result)
assert canon({k:v for k,v in read(out).items() if k!='review_run_sha256'})==result['review_run_sha256']
for a in lease['input_artifacts']:
    now=pin(ROOT/a['path']);assert now['raw_sha256']==a['raw_sha256'] and now['lf_sha256']==a['lf_sha256']
for path,cur in [(RUN/'reviewer.source.lease.json',own),(RUN/'source.review.lease.json',lease)]:
    cur.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':utc(),'result':pin(out),'review_run_sha256':result['review_run_sha256'],'outcome':'BLOCKED_METADATA_ONLY; no frozen canonical/source input mutated'})
    cur.pop('lease_run_sha256',None);cur['lease_run_sha256']=canon(cur);write(path,cur)
print(json.dumps({'status':result['status'],'result':pin(out),'review_run_sha256':result['review_run_sha256'],'checks':pin(RUN/'source.review.checks.json'),'root_lease':pin(RUN/'source.review.lease.json'),'own_lease':pin(RUN/'reviewer.source.lease.json'),'input_count':len(lease['input_artifacts']),'all_leases':'CLOSED'},ensure_ascii=False))
