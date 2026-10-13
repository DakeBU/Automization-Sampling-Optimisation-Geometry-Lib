from pathlib import Path
import json,hashlib,os,sys,traceback
ROOT=Path('E:/Samplinglib'); RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'; OWN=RUN/'independent-source72'
PRIOR=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72'
REL=OWN.relative_to(ROOT).as_posix();PREL=PRIOR.relative_to(ROOT).as_posix()
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def text(n,s):(OWN/n).write_text(s,encoding='utf-8',newline='\n')
def slot(a,b,e,r='explicit-elaboration'):return {'original':a,'reconstructed':b,'relation':r,'evidence':e}
def delta(s,d,e):return {'slot':s,'severity':'informational','description':d,'evidence':e}
OPEN='Actual conditional half-turn H, K/B7, real r/r_rho and B27 outputs, B28/B4 dynamics and residual estimates, H1/B2, invariance/nonexplosion, main/live, full paper results, errors/caps, expected-query costs and PBPS/SPHMC composition remain open. No Exposition Seal, PURIFIED, SCI, VERIFIED or Goal completion is granted by this source review.'

GENERIC_REVIEW='''The complete 54-line generic module and its six formula/BODY steps are source-admissible as the explicitly attributed ASTIS auxiliary Hilbert generalization of B20 and B4 Ex28–Ex34. This is not a claim that the paper states a theorem for arbitrary Hilbert operators. The source-facing contract and the independent reconstruction are equivalent after the displayed elaborations. There is no blocking mathematical, binder, definition, sign, constant or exposition delta.

The source graph was frozen before either 72 BODY: 24 nodes, 53 edges, 20 exact formula anchors and 27 obligations, with 361 finite source items (255 primary +106 supplemental;239 NODE,122 EXCLUDED). StageB preserves every classification and verifies each exact RAW interval against PBPSv1 d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760. NODE means relevant source material, not established proof. S17–S19 and S21–S23 retain explicit OPEN dispositions. No source graph is inferred from Lean.

I had already read 70 and71 full code/source/publication and the prospective72 headers and bounded B27 dependency diagnosis. I am not source-blind. StageA source pins predated current72 implementation; the current72 BODY, current exposition and decoder were first read only after the official StageB dispatch. I did not read other agents' math/header-math/source verdicts or root.math72. The canonical audit snapshots were opaque identity inputs; for native schema verification only their source/Lean/reconstruction/publication fields are selected, with no old slots/deltas/repairs/verdict consulted. The stale null approved-context field in the early own readview was an extraction-path error: the authorized neutral packet contains lean.approved_definition_context, which was read and checked separately.

On one complete real Hilbert H, define C(u,v)=(||u||²−||v||²)/2−<A(Inv u),v>. The signature states exactly the seven sealed primitive facts: selfadjoint A,G,Inv; A commutes with Inv; Inv G=G Inv=I; A²+G²=I. They are honest hypotheses of this algebra leaf, rather than invented public PBPS callers or a certificate for the result. The implementation needs no positivity, finite dimension, positive rank, spectral-gap inequality, onto-V premise, A/G commutation or B21/68-energy input. The explicit hAInv and hGInv are unused by this proof; retaining these already sealed structural facts is harmless redundancy, transparently reported. No weakening is silently applied.

Lines23–26 unfold C and obtain real inner-product transport;27–33 evaluate Inv G=I and the square-sum;34–37 give ||Ar||²+||Gr||²=||r||²;38–42 give Inv(A²r)+Gr=Inv r;43–45 give <A Inv u,Ar>+<u,Gr>=<u,Inv r>. The full increment before cancellation is
<u,Gr>+<v,Ar>+(||Gr||²−||Ar||²)/2+<A Inv u,Ar>−<Ar,v>+||Ar||².
Real symmetry cancels the v terms, the mixed term is <u,Inv r>, and the quadratic part is +||r||²/2. Lines46–49 implement exactly this calculation. The plus first perturbation, minus second perturbation, plus linear term, positive one-half and A(Inv u) order agree with B20/Ex28–Ex34. No inverse is extended across constants.

The decoder preserves every quantified object, all seven hypotheses, the same operator composition order, local C shadowing and the exact identity. H may be zero. The decoder's arbitrary r is correctly arbitrary: it is not source-produced r_rho. The real algorithm/kernel producer and actual B27 adapter are absent and honestly excluded from this result.

All six authored Lean snippets equal the exact contiguous RAW line spans and LF-normalized snippets; they cover the entire proof23–49 without gap/overlap. Every displayed formula and prose step describes that span with its earlier local definitions in scope. The complete module and all54 lines were independently read. Production scanner/disclosure was exercised only on the two candidate modules; generic has no private helper. This bounded fold check does not establish full browser, aggregate reader, Exposition Seal or live delivery.

Reader status overlay v1 and v2 were incomplete and never applied. Their failure/needs-revision evidence remains. The separately reviewed v3 changes16 suffix fields in6 current JSON files and has zero old pending suffix remaining. The two candidate-context string changes per unit are acknowledged; whole review_context hashes changed, while statement/formula/Lean/BODY/decoder stayed exact. Final official packet2 is the approved concrete proposed packet, and binding/context have been independently recomputed from current exact bytes. This is metadata repair only, not mathematics.

'''+OPEN+'\n'

ACTUAL_REVIEW='''The complete 440-line actual module and four formula/BODY steps are source-admissible for the bounded same-input perturbation integration. The reconstruction and full literal result are equivalent after elaboration. The theorem retains every parent71 conclusion and adds precisely the universally quantified perturbation algebra on the same centered space. There is no blocking mathematical, assumption, definition, scope, formula or exposition delta. This does not establish actual B27/B28 dynamics.

StageA is the immutable source-first361-item/24-node/53-edge/20-formula/27-obligation contract frozen before current72 BODY. It is reused without rebuilding its source graph or copying its254-file closed bundle. All361 exact primary RAW ranges were rechecked and each item has a per-node generic/actual disposition. All27 obligations, all494 lines of both modules and all10 exact BODY spans are accounted for. Open source nodes remain OPEN; excluded source items receive no proof badge. Prior70/71 implementation and prospective72 header exposure is disclosed: this review is anti-anchored from other verdicts, not source-blind. Current72 BODY/publication/decoder were first read after official dispatch.

The actual signature has only the original six analytic callers: alpha>0,alpha<=beta,C² V, both Hessian inequalities for all x,v,eta>0,beta eta<=1. The finite-dimensional real Hilbert Borel structures and nonnegative alpha,beta are unchanged. Rank zero and alpha eta=1 remain admitted. There is no arbitrary H/kernel, mean-output, onto-V, strict endpoint, added smoothness, inverse or corrector-change certificate binder. The twelve witnesses S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R remain outside the final universal f, in identical order. Branch-local fP and gP remain inside its centered-input implication.

The parent retention check removes only the new final conjunction and compares the entire remaining literal text exactly with current ActualCorrectorChange.lean. It also compares both complete public caller signatures after reversing only the statement name. Both are exact. This detects any dropped or altered earlier law/kernel/root/inverse/polar/full-micro/observable/B21 clause without using an old acceptance verdict.

The same mu,J,nu,Lambda and actual AE reflection F/U persist; Lambda's map (y,2x−y) is correctly distinct from F's map (x,2x−y). The reflected S is every-state normalized tilted law and a conditional kernel for Lambda, not the missing conditional half-turn. e is onto HP by equivalence; V0 is only an isometric embedding into all kerP. D remains exactly R U inclusion with V0*D=−A0 V0* on all kerP. No restriction to range(V0) or V0 V0*=I is introduced.

The same positive Gamma is transported, then restricted to HP0=ker<qP,·>; the same two-sided Inv is defined only there. A0 is the same compression restriction and A0²+GammaP0²=I, A0/Inv commutation and Inv selfadjointness remain internal facts. Line314 uses positivity of GammaP0 to derive selfadjointness on this internally complete Hilbert space. Mathlib Positive.lean defines CLM positivity using symmetry and nonnegative quadratic form and supplies IsPositive.isSelfAdjoint on complete E. Thus the decoder's selfadjoint-plus-nonnegative wording is an equivalent definition elaboration here, not an extra binder. Mathlib tilted uses exp(f)/integral exp(f); the probability conclusions internally rule out its nonintegrable zero-measure fallback. No hidden normalization assumption is added.

For each globally centered joint f, fP is tied to actual condExpL2 f and fV=V0*Rf. The same output is g=U(Pf−(f−Pf)); its zero mean is retained as an internally proved conclusion, not a caller condition. gP is tied to actual condExpL2 g and gV=V0*Rg; neither is defined as a rotation RHS. Their exact rotation, pair-energy and B21 C-change persist. C is the same B20 half norm difference minus <A0(Inv u),v>.

The new forall u v r:HP0 lies syntactically inside each actual f/gP/C branch, and C does not depend on f. Lines315–320 apply the generic result using only the same internally produced A0,GammaP0,Inv and seven structural facts. Lines321–349 append it to the same g branch;350–435 reconstruct all earlier witnesses/clauses. This gives a real original-input PBPS consumer of the generic leaf, not just arbitrary operator premises. Its final r remains arbitrary; actual H/K/r/r_rho/B27 are not produced. The standalone Hilbert leaf does not depend on retained B21. Parent71 is an integration parent only; no invented68 sharp-energy edge appears.

The decoder reconstructs all six callers, twelve witnesses, probability/kernel/law, centered inverse, full kerP D identity, actual f/g semantics, internal mean, retained B21 and the final universal scope. It temporarily names kerP by K, while candidate source prose temporarily names A0 Inv by K. These are separate locally defined aliases; neither is the missing source Markov K. Exact definitions, not alias spelling, resolve the possible ambiguity. No decoder repair is required.

All four authored BODY snippets equal current exact RAW spans152–313,314–320,321–349,350–435, covering the complete proof without gap/overlap. The displayed formulas preserve Gamma/A order, signs, one-half and the same inverse. All440 lines and complete literal20–141 were read. A bounded production scanner identifies the full private statement identity and the helper renders all of it in an initially folded adjacent disclosure labelled “Full Lean proposition (definition)”, explicitly nonprovider. This is bounded rendering feasibility, not actual browser/full Exposition acceptance.

Approved metadata-only v3 resolves stale review/integration pending wording in16 exact fields. Official packet3 differs from original1 only in binding/own hash and two status strings in publication_context; the changed context hashes are honestly recorded. Current Lean/decoder/source/formulas and BODY are identical. The final official packet and all six current JSON files match approved proposed bytes; publication binding and candidate context were independently recomputed. Two cells expose two connected canonical declarations of one SAU, not two advances or a fake source consumer.

'''+OPEN+'\n'

def make_slots(n):
 if n==0:
  return {
   'objects':slot('Attributed auxiliary generalization of source B20/Ex28–Ex34: bounded A,G,Inv and exact locally defined C on H.','Decoder reconstructs the same three maps and C(a,b)=half norm difference minus <A(Inv a),b>.','generic9–21 and23–49; exact source E20,Ex28–Ex34; StageB.source20-formula-coverage.json'),
   'domains':slot('One complete real Hilbert H, including zero; no probabilistic/finite-dimension premise for auxiliary algebra. Actual source specialization is centered HP0.','Decoder universally quantifies exactly complete real Hilbert H including zero and bounded real endomorphisms.','generic10–12; StageA S00/S10/S15; no actual algorithm-domain claim'),
   'quantifiers':slot('For every H,A,G,Inv satisfying seven primitive facts and every u,v,r:H, the displayed exact identity.','Same universal order and scope; local C arguments are dummy binders.','generic10–21; source auxiliary contract explicitly distinguished from paper theorem',r='equivalent'),
   'assumptions':slot('A,G,Inv selfadjoint; Commute A Inv; Inv G=G Inv=I; A²+G²=I. Honest explicit auxiliary premises, all internal at actual consumer.','All seven and no added operator/result certificate reconstructed.','generic13–16; actual314–320. hAInv/hGInv remain sealed but unused in this proof.',r='same'),
   'conclusion':slot('C(u+Gr,v−Ar)−C(u,v)=<u,Inv r>+||r||²/2, with C=(||u||²−||v||²)/2−<A(Inv u),v>.','Exactly the same functional, perturbation signs, composition order, coefficient and RHS.','generic18–21,34–49; exact E20/Ex28–Ex34 algebra',r='same'),
   'scopes':slot('Only auxiliary arbitrary-vector algebra; r not actual r_rho; no H/K/B27/B28 conclusion. No B21 dependency.','Decoder is purely the arbitrary-vector statement and introduces no algorithm/output scope.','generic imports only Mathlib; final publication boundary; StageA S17–S23 remain OPEN'),
   'constant_dependencies':slot('Exact real coefficient1/2; no rho/c0/omega/Lambda/gamma parameter or extra regularity. Operator facts explicitly quantified.','Decoder preserves1/2 and operator dependence with no positivity/nonzero/scalar/probability premise.','generic18–21 and proof34–49; StageA O09/O10/O21/O22',r='same')}
 return {
  'objects':slot('Same complete parent71 actual laws, S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R; actual P,D,fP,gP,fV,gV,C; only new universal same-space perturbation.','Decoder reconstructs all twelve witnesses and definitions, actual g and conditional/polar components plus C and final identity.','StageB.parent-retention.exact-check.json; actual20–141,152–435; decoder full text'),
  'domains':slot('Finite-dimensional real Hilbert Borel E; real AE L2(J/nu); HP0 centered macro space; Hperp=all kerP. Inv only HP0; V0 not onto.','Decoder spells out inherited complete HP0/Hperp, conditional-mean-zero distinction, AE/null-set scopes and no onto V0.','actual29–118; StageA S00/S02/S05/S07; exact approved definition contexts'),
  'quantifiers':slot('Original6 caller conditions. Twelve global witnesses outside forall centered f; fP/gP inside implication. Final forall u v r inside gP/C branch.','Decoder states exactly these global/branch scopes and every-state S vs u-dependent AE kernel action.','actual20–28,45–141,143–151; exact parent/public-signature comparisons',r='equivalent'),
  'assumptions':slot('Only hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta with original structures. All operator/normalization/mean/generic ingredients conclusions produced internally.','Decoder lists six original callers and explicitly treats probability/root/centered/inverse/operator facts as concluded witnesses.','actual143–167,314–320; Positive.lean266–281; no extra provider/mean/onto/higher regularity'),
  'conclusion':slot('Every old clause including actual g mean/rotation/energy/B21 retained; append exact C(u+Gamma0r,v−A0r)−C(u,v)=<u,Inv r>+||r||²/2.','Decoder retains old conclusions and exact appended identity, same C/A0/Inv, signs and half.','actual119–141,314–435; exact literal deletion-to-parent check; source E20/Ex28–Ex34',r='same'),
  'scopes':slot('Private literal stores complete proposition, no provider. New identity inside real actual branch, arbitrary r distinct from algorithm residual; real H/K/B27/B28 open.','Decoder preserves actual g=U(Pf−(f−Pf)), real CE/P/V*R semantics, output mean as conclusion and final nested forall scope. K is only a local alias for kerP.','actual20–141 and321–349; bounded adjacent fold; source S17–S23; alias distinction does not change object'),
  'constant_dependencies':slot('Same gamma=2sqrt(alpha eta)/(1+alpha eta)>0; same Inv bound1/gamma; endpoint beta eta<=1 includes alpha eta=1; rank0; new exact half with no rho/cost parameter.','Decoder preserves gamma/inverse bound and no nonzero/strict endpoint/extra scalar assumption; final half and coefficient1 exact.','actual84–95,136–141; generic34–49; StageA O21–O24',r='equivalent')}

code=0
try:
 assert not (OWN/'lease.final.json').exists()
 text('source.0.review.RAW.md',GENERIC_REVIEW);text('source.1.review.RAW.md',ACTUAL_REVIEW)
 deltas=[[
 delta('domains','The generic unit is explicitly an ASTIS auxiliary real-Hilbert generalization, not a verbatim PBPS theorem or actual algorithm result.','source original auxiliary attribution; generic10–21; StageA S15; actual consumer separate'),
 delta('assumptions','hAInv and hGInv are sealed explicit structural facts unused by this proof; actual consumer supplies both internally. No premise removal or addition is proposed.','generic14–16 versus proof23–49; actual315–320'),
 delta('objects','C local argument names shadow outer u/v only within the function; same A(Inv u) order.','generic18–21; decoder text local-scope paragraph'),
 delta('scopes','Arbitrary r is not source r_rho and no actual H/K/B27/B28 producer follows.','source Ex23–Ex27/B27/B28; final boundaries; open graph S17–S23'),
 delta('scopes','Reader status v3 is metadata-only, with acknowledged changes to two context strings; initial0/1 packets retained and final2/3 bound.','reader-status-overlay72.v3.independent-decision.json; final-binding checks; no math or decoder change')],
 [delta('objects','The literal private definition stores the complete result and supplies no provider or additional hypothesis. Its exact full helper is adjacent and initially folded.','actual20–141,143–152; StageB.unit.1.bounded-adjacent-fold.html'),
 delta('domains','AE L2/closed conditional subspaces and normalized tilted measures elaborate source notation; no extra input normalizer or integrability premise.','actual29–43,45–52; Tilted.lean36–44; inherited probability conclusions'),
 delta('assumptions','GammaP0 positivity supplies selfadjointness internally on complete HP0; decoder selfadjoint/nonnegative positivity wording is equivalent here.','actual82–83,90,314; Positive.lean266–281'),
 delta('quantifiers','Twelve global witnesses and two branch-local components are distinct scopes, exactly retained; early observer counting all fourteen together was corrected without candidate change.','StageB.parent-retention.exact-check.json; failed PID33468 EXIT1, corrected PID8608 EXIT0'),
 delta('domains','V0 maps into all kerP as an isometric embedding; no onto-V0 or range-only D identity. e is onto HP by equivalence and is a separate object.','actual51–52,103–118; decoder full-domain paragraph'),
 delta('conclusion','Actual g and real condExpL2 gP / V0*Rg gV are defined before their formulas; mean(g)=0 is an inherited internal conclusion.','actual119–138,321–349; exact parent retention'),
 delta('scopes','Decoder K=kerP and source-contract K=A0 Inv are independent local aliases, neither the still-open algorithm Markov K. Exact definitions resolve the name ambiguity.','decoder text Hperp paragraph; source contract cross operator; StageA S17; complete literal uses Hperp and A0(Inv u)'),
 delta('scopes','Final forall u v r is nested inside each actual f/gP/C branch; C is independent of f. This consumes actual witnesses without asserting r=r_rho or B27 outputs.','actual139–141,315–349; source Ex27/B27 outside result'),
 delta('scopes','Parent71/B21 retained for integration, not a pure-Hilbert algebra parent; no invented68 sharp-energy dependency. Two cells expose one SAU with two connected canonical declarations.','actual imports/parent call and generic Mathlib-only imports; source graph vs Lean graph distinction'),
 delta('constant_dependencies','Rank0 and alpha eta=1 remain legal; same centered inverse and exact half, signs/order survive; no rho, cost or higher-regularity assumption.','actual20–28,84–102,136–141; generic18–21'),
 delta('scopes','Reader status16-field v3 overlay changes only boundary/process strings; context hash changes are acknowledged and final packet3 is exact approved proposed bytes.','reader-status-overlay72.v3.independent-decision.json; StageB.final-binding-checks.json')]]
 for n in [0,1]:
  p=load(RUN/f'source-review.packet.{n+2}.json')
  assert set(make_slots(n))==set(p['review_contract']['semantic_slots'])
  dec={'schema_version':1,'semantic_slots':make_slots(n),'deltas':deltas[n],'verdict':'equivalent-after-elaboration','repairs':[],'reviewer':'independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'review_evidence':f'{REL}/source.{n}.review.RAW.md','reviewer_packet_sha256':p['packet_sha256'],'official_packet_RAW_sha256':sha((RUN/f'source-review.packet.{n+2}.json').read_bytes()),'publication_binding_sha256':p['publication_binding_sha256'],'unit_index':n,'blocking_deltas':0,'truth_boundary':OPEN,'source_blind':False,'mathematical_or_binder_repairs_required':False,'reader_overlay':'approved/applied exact v3 metadata overlay, separate evidence; no mathematical repair'}
  write(f'source.{n}.decision.core.json',dec)
 obligations=load(PRIOR/'stageA.all27-source-header-obligations72.frozen.json')['entries']
 evidence=[
 'Immutable StageA source expectations/graph/classifications verified through preparation.inputs.json; all361 RAW ranges rechecked.',
 'Prior70/71/header72/B27 diagnosis disclosed; current72 BODY/publication/decoder first after official dispatch; no other math/source verdict read.',
 'generic18–19; actual136–137; exact source B20 same half/minus/A Inv order.',
 'generic10–12,17; actual80–83,139–141. No inverse on full HP or constants.',
 'generic13–16 explicit primitives; no result certificate; exact auxiliary attribution.',
 'actual72–102,314–320 obtains same positivity/SA/inverse/commutation facts internally.',
 'generic24–37 yields energy from SA and square-sum; no rank/onto input.',
 'generic20; actual140 exact +Gamma r and −A r.',
 'generic27–33,46–49; real v cancellation, Inv G=I.',
 'generic38–45 mixed linear operator/inner transport gives exact inner(u,Inv r).',
 'generic34–37,46–49 positive norm(r)^2/2.',
 'generic imports Mathlib only; retained B21 is actual integration history, not leaf parent; no68 import.',
 'actual119–141,315–349 original-input f/gP/gV branch consumes same-space generic theorem.',
 'StageB.parent-retention.exact-check.json proves complete deletion-to-parent literal/signature equality; same12 globals.',
 'actual127,129–134 actual U observable, CE gP and V*R gV precede RHS formulas.',
 'actual128 is conclusion; parent call retains internally established reflection-law/CE-integral centering.',
 'actual139–141 arbitrary r explicitly distinct from source Ex27 r/r_rho; no producer credit.',
 'OPEN source S17/S18: actual H/K/r_rho not constructed. This is a required future producer, not a new caller.',
 'OPEN source S18: actual r_rho same-HP0 adapter not produced. Current generic r already typed HP0, not identified with it.',
 'OPEN source S19/B27: actual Kf output-component adapter remains absent.',
 'OPEN source S21/B28: source B21 retained but real B27 substitution needed; no combined dynamics claimed.',
 'No rho/c0/omega/Lambda hypotheses in new algebra; actual B4 regime separate and open.',
 'Exact original endpoint <= and noNontrivial/onto/higher derivative binder; rank0 and alpha eta=1 allowed.',
 'All same root/inverse/e/V/HP0 witnesses retained; no independent inverse inserted.',
 'OPEN S22/S23: B29–B31, fullB4/decay/main/H1B2/errors/cost/composition unproved by this advance.',
 'Exact private literal scanner identity and full adjacent initially folded nonprovider helper checked on bounded modules.',
 'This closes only independent source-fidelity for bounded72 units. No proof ownership, SCI/VERIFIED/PURIFIED/wholepaper/Goal transition.'
 ]
 open_ids={17,18,19,20,24}
 assert len(obligations)==len(evidence)==27
 out=[]
 for i,(o,e) in enumerate(zip(obligations,evidence)):
  out.append({'id':o['id'],'type':o['type'],'frozen_expectation':o['expectation'],'StageB_status':'OPEN_REQUIRED_FUTURE_EDGE_EXPLICITLY_NOT_DISCHARGED' if i in open_ids else 'CHECKED_WITHIN_BOUNDED_SOURCE_ADMISSION','evidence':e,'new_public_binder':False})
 write('StageB.all27-obligations.decisions.json',{'count':27,'entries':out,'open_required_future_edges':len(open_ids),'unclassified':0})
 text('bounded-synthesis72.md','''Both bounded units are source-admissible, with equivalent-after-elaboration verdicts and zero blocking deltas. The generic leaf establishes the exact B20/Ex28–Ex34 algebra under its sealed explicit Hilbert premises. The actual consumer internally supplies all seven structural facts on the same HP0 and retains all six callers, twelve common witnesses and every parent71 clause. No mathematical/binder repair is required.

Exhaustive finite coverage is361 source rows (239 NODE/122 EXCLUDED),24 source nodes/53 edges,20 exact formulas,27 obligations,494 module lines and six+four exact contiguous formula/BODY spans. Source graph, Lean dependencies and reader evidence remain distinct. The independently checked reader v3 repair is status metadata only; final official packets2/3 bind current exact context and publication digests.

Arbitrary r remains arbitrary. The source-produced half-turn H, Markov K/B7, r/r_rho, actual B27 outputs and B28/B4 dynamics remain open, as do main/live/fullpaper/errors/cost/composition. This review grants no SCI/VERIFIED, Exposition Seal, PURIFIED or Goal completion. Bounded adjacent helper rendering is checked; repository integration/full browser delivery is separate.

Native evidence reuses immutable StageA/CLOSED254 pins without copying historical packet files. Initial packets0/1, unapplied incomplete status proposals and observer failures are preserved. RAW and CRLF-only LF recipes are explicit. Canonical, ledger, Git and prior CLOSED trees were not written.
''')
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'unit_verdicts':['equivalent-after-elaboration']*2,'blocking_deltas':[0,0],'informational_deltas':[len(x) for x in deltas],'obligations':27},indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:write('StageB.author-reviews.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
