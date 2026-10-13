from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
OUT = Path(__file__).parent
OLD = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def put(name, x):
    p = OUT / name
    assert not p.exists(), name
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode())
    assert json.loads(p.read_bytes()) == x
    return pin(p)
def pin(p):
    p = Path(p); b = p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(), 'bytes':len(b),
            'raw_sha256':sha(b), 'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}

# Only import the old immutable parser class, never execute the old evidence author.
s = (OLD/'extract_and_freeze_primary.py').read_text(encoding='utf8')
ns = {'HTMLParser':HTMLParser}
exec(s[s.index('class Parser'):s.index('b=(OLD/')], ns)
Parser, txt = ns['Parser'], ns['txt']
raw = (OLD/'primary-pbps.exactraw.snapshot.html').read_bytes()
assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
html = raw.decode(); parser=Parser(); pos=0
for line in html.splitlines(keepends=True): parser.offsets.append(pos); pos+=len(line)
parser.feed(html)
anchor_ids=['A2.E1','A2.E2','A2.E3','A2.E4','A2.E5','A2.E10','A2.E11',
            'A2.E15','A2.E16','A4.SS1','A3.E3','A3.E4','A3.E5','A3.E6','A3.E7',
            'bib.bib18','bib.bib19']
anchors=[]
for ident in anchor_ids:
    matches=[n for n in parser.nodes if n['attrs'].get('id')==ident]
    assert len(matches)==1,ident
    n=matches[0]; b=html[n['start']:n['end']].encode()
    anchors.append({'id':ident,'primary_start_utf8_byte':len(html[:n['start']].encode()),
                    'primary_end_utf8_byte_exclusive':len(html[:n['end']].encode()),
                    'slice_bytes':len(b),'slice_raw_sha256':sha(b),
                    'math_alttext_text':' '.join(txt(n).split()),'balanced':True})
put('primary.anchors.json',{'primary':pin(OLD/'primary-pbps.exactraw.snapshot.html'),
                          'anchors':anchors,'copied_primary_bytes':0})

env=dict(__import__('os').environ);env['PYTHONUTF8']='1'
r=subprocess.run([sys.executable,'tools/astis_advance.py','capsule'],cwd=ROOT,env=env,
                 capture_output=True,encoding='utf8')
assert r.returncode==0, r.stderr
c=json.loads(r.stdout)
put('capsule.bounded.json',{'actual_exit_code':r.returncode,'stdout_raw_sha256':sha(r.stdout.encode()),
 'stderr':r.stderr,'source_command':'python tools/astis_advance.py capsule',
 'slice':{k:c[k] for k in ['schema_version','generated_at','omitted_cell_count','omitted_advance_count',
 'single_stabilization_lane','raw_worker_transcripts_included']},
 'relevant_visible_cells':[x for x in c['frontier_cells'] if 'PBPS' in x.get('frontier_cell','')],
 'scope':'Default bounded capsule omitted PBPS cells; empty visible slice is not absence evidence.'})
execution=json.loads((ROOT/'website/content/samplewiki_companion_frontiers.json').read_text(encoding='utf8'))['execution']
put('execution.bounded.json',execution)

headers=[]
for i,f in enumerate(['AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean',
 'Tests/ProximalBPSMacroscopicRange.lean']):
    p=ROOT/f; t=p.read_text(encoding='utf8'); h=t.split(':= by',1)[0]
    op=OUT/f'public-header-{i}.snapshot.lean'; op.write_bytes(h.encode())
    headers.append({'original_at_observation':pin(p),'public_header':pin(op),
                    'selection':'Before first := by; proof body excluded from snapshot.'})

contract={
 'schema_version':1,'actor':'/root/next_primary59','status':'SOURCE_ONLY_NEXT_EDGE_AUDIT',
 'source':{'id':'arXiv:2609.06905v1','url':'https://arxiv.org/html/2609.06905v1',
 'version':'v1','primary':pin(OLD/'primary-pbps.exactraw.snapshot.html'),
 'license_url':'http://arxiv.org/licenses/nonexclusive-distrib/1.0/',
 'primary_extraction':pin(OUT/'primary.anchors.json'),'new_source_fetch':False},
 'recommended_one_edge':'Actual SAME scalar conditional operator T is self-adjoint on real L2(nu), with internally derived mean preservation and a genuine bounded self-adjoint restriction T0 to the actual closed centered subspace H0. This supplies the operator/domain prerequisite for I-T^2 and its actual centered defect consumer.',
 'source_standing_hypotheses':[
 'Printed Euclidean R^d; V C2; 0<alpha<=beta; global alpha I<=Hess V<=beta I.',
 'eta>0 and beta*eta<=1. No higher derivatives or narrower scale.',
 'Finite real Hilbert/Borel/rank0 is the explicitly disclosed local extension; never finite-dimensional L2 or Nontrivial centered L2.'
 ],
 'defined_actual_inputs':{'mu':'volume.tilted(-V)',
 'J':'map((x,z)->(x,x+sqrt(eta)z), mu.prod(stdGaussian E))','nu':'J.snd',
 'Lambda':'J.map((x,y)->(y,2x-y))',
 'S':'literal normalized source reflected kernel from actual55, with Lambda.IsCondKernel S and Lambda.fst=Lambda.snd=nu',
 'P':'actual conditional Y orthogonal projection on L2(J)',
 'U':'actual AE reflection pullback, involutive linear isometry and self-adjoint',
 'M':'canonical snd pullback, identified with actual55 M by literal AE snd action',
 'T':'actual55 uniform bounded conditional mean on all rough L2(nu), MT=AM and PM=M, where A=PUP'},
 'binder_classification':[
 {'class':'ambient-structure','condition':'Real complete L2 and closed subspace inherit the Hilbert structure; completeness is derived, not a caller finite-dimension assumption.'},
 {'class':'source-hypothesis','condition':'Original C2/two Hessian bounds/positive capped eta retained even though operator adjoint algebra alone needs less.'},
 {'class':'defined-actual-input','condition':'Law, probability, literal kernel, projection, U/M/T and normalization come from actual55/actual58 parents, never caller certificates.'},
 {'class':'derived-domain','condition':'H0=ker(innerSL(real, actual probability class1))={u: integral_nu u=0}; continuous functional gives closedness. T0 has every H0 vector as its domain.'},
 {'class':'derived-property','condition':'Self-adjoint T, integral(Tu)=integral(u), T(H0) subset H0 and symmetric restriction are conclusions; none is an extra theorem binder.'},
 {'class':'consumer-restriction','condition':'The sharp defect estimate is only centered; full D=I-T² is positive but has constants in its kernel.'}
 ],
 'exact_science_delta_to_seal_later':[
 'For all u,v in real L2(nu), <Tu,v>=<u,Tv>, using SAME M and real self-adjoint PUP.',
 'For all u in real L2(nu), integral_nu(Tu)=integral_nu(u), from SAME stationary Lambda/S disintegration and AE source mean.',
 'Construct actual closed H0 and T0:H0->L[real]H0 with T0u=Tu under subtype inclusion and IsSelfAdjoint T0; no supplied invariant-subspace certificate.',
 'Derive D=I-T² positive on all L2(nu); centered D0=I-T0² is its true restriction. In an actual Test consumer, join58 to obtain <D0u,u>=||u||²-||T0u||²>=delta||u||², delta=4alphaeta/(1+alphaeta)².',
 'Any centered invertibility consumer must act on this actual complete H0 and the same D0; it proves no Gamma inverse or square root. Production does not import Tests.'
 ],
 'source_graph':{
 'edges':['B1/B2 actual P/M -> B4 selfadjoint U -> B3/B5 selfadjoint A',
 'B2 exact real M identification + MT=AM -> actual scalar T selfadjoint',
 'D2 stationary Markov + actual Lambda/S disintegration -> mean preservation -> closed centered restriction',
 'selfadjoint T + norm contraction -> positive I-T² -> D1 positive-root adapter still needed -> B10/B11',
 'C3/C4 + actual58 true centered range -> exact D0 coercivity -> later B15 after root',
 'B15 centered root inverse -> B16 polar isometry -> halfturn/hypocoercive consumer'],
 'truth':'Source dependency blueprint only. No admitted Lean edge or source theorem completion.'},
 'omitted_detail_audit':[
 {'classification':'internal-paper-step/local-integration-gap','anchor':'B2-B5/D1','detail':'Source says macro compression is self-adjoint; literal scalar conditional mean and SAME isometry require a formal transport. Current actual55 public contract has no IsSelfAdjoint T conclusion.'},
 {'classification':'mathlib-available','anchor':'D1/D2','detail':'Orthogonal projection self-adjointness, isometry inner transport, closed continuous-linear kernel and bounded subspace restriction are available over RCLike including real.'},
 {'classification':'internal-paper-step/local-integration-gap','anchor':'D2/C3','detail':'Stationary actual disintegration and L2->L1 yield mean preservation. No caller mean-preservation or pointwise rough-fiber equality.'},
 {'classification':'source-background-convention/local-real-adapter-gap','anchor':'D1/B10','detail':'D1 explicitly states bounded Borel spectral calculus and unique nonnegative root. The concrete real complete-Hilbert operator construction remains separate; no spectral theorem bibliography is supplied at D1.'},
 {'classification':'external-cited-context','anchor':'B1 citations14/21','detail':'Actual links are bib.bib18/bib.bib19 and only accompany hypocoercivity terminology. Their bibliography is extracted in primary.anchors; no spectral/root theorem or source assumption is imported from them.'}
 ],
 'constant_precision':{'t':'alpha*eta in (0,1]','rho':'(1-t)/(1+t) in [0,1)',
 'delta':'1-rho²=4t/(1+t)²>0','Gamma_gap_only_after_root':'sqrt(delta)=2sqrt(t)/(1+t)',
 'endpoint':'t=1: T0=0 by sharp contraction; D0=I. No division by 1-t.',
 'rank0':'H0 may be zero/subsingleton; no nonzero vector or Nontrivial binder.',
 'full_space':'Constant class1 is fixed by T and killed by D; no full-space positive lower bound or inverse.',
 'Gamma_coefficient':'Gamma=(I-A²)^(1/2) has NO eta prefactor.'},
 'production_test_boundary':'actual55 production supplies U/M/T and stationary Lambda/S. Current58 allmacro contraction/squared gap is Test-only and still pending final source/commit/integration, not VERIFIED. The new production interface can derive self-adjointness/centering from actual55; sharp coercivity and optional inverse consume58 in Test until serialized promotion. No production imports Tests and no duplication of57 PI proofs.',
 'rejected_routes':[
 'Using instStarOrderedRingRCLike as a real CFC construction: it assumes precisely the real CFC instance.',
 'Treating Rayleigh TODO180 as absence of real spectralRadius_eq_nnnorm: theorem182 already proves RCLike including real.',
 'Assuming finite-dimensional L2, supplied root/CFC/adjoint/mean-preservation/law/normalization certificates.',
 'Constructing Gamma only on H0 as if it completed B10/B11 on all macro L2.',
 'Identifying Gamma with eta-scaled gradient/Laplacian/resolvent roots or claiming full inverse despite constants.'
 ],
 'remaining_boundary':[
 'General real complete possibly infinite-dimensional positive-root adapter with positivity, square identity, uniqueness and actual M/A compatibility.',
 'B11 allmacro norm identity and B15 centered Loewner root gap/inverse, B16 polar isometry.',
 'Full source weak-H1 equivalence; halfturn spectral-band/inverse/domain estimates; dynamics/nonexplosion/hypocoercivity/main/errors/cost and actual-input PBPS/SPHMC composition.',
 '58 independent final source, commit and serialized integration; review/purification/exposition acceptance for any later edge.'
 ],
 'chronology':{'primary_first_reconstruction_completed_before_current_candidate_headers':True,
 'candidate59_supplied':False,'candidate59_header_or_body_read':False,'candidate59_proof_started':False,
 'existing58_header_read':'After independent frozen source reconstruction; not a blind review of58.',
 'incidental_body_exposure':'rg displayed a few existing55/58/ReflectionL2/57Test proof lines, and pinned Mathlib proofs were read; no strict provider-body blindness. No59 candidate exists as supplied.',
 'contract_write_timing':'Written after source reconstruction and API inventory. This audit is not a preproof Statement Seal; no theorem/proof is being searched.'},
 'admission':False,'compiler_started':False,'no_sau_claim':True,'no_shared_or_git_or_goal_state_edits':True
}
put('source.contract.json',contract)

apis=[
 ('Mathlib/Analysis/InnerProductSpace/Adjoint.lean','IsSelfAdjoint.conj_starProjection',396,400,'Available real selfadjoint PUP; source actual P must first be matched to starProjection.'),
 ('Mathlib/Analysis/InnerProductSpace/Adjoint.lean','ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric',380,386,'Transport symmetry through SAME isometry M; no real CFC needed.'),
 ('Mathlib/Analysis/InnerProductSpace/LinearMap.lean','LinearIsometry.inner_map_map',115,121,'Actual M preserves the real inner product.'),
 ('Mathlib/MeasureTheory/Function/L2Space.lean','L2.inner_indicatorConstLp_one',222,226,'Probability class1 inner product equals integral on univ; build continuous mean kernel.'),
 ('Mathlib/Analysis/InnerProductSpace/LinearMap.lean','innerSL',167,175,'Bounded real mean functional as innerSL with class1.'),
 ('Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean','ContinuousLinearMap.isClosed_ker',669,671,'Genuine H0 closedness.'),
 ('Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean','ContinuousLinearMap.restrict',154,166,'Actual invariant centered endomorphism; invariance must be derived.'),
 ('Mathlib/Probability/Kernel/Disintegration/Basic.lean','Measure.IsCondKernel.disintegrate',58,66,'Actual55 Lambda.fst tensor S equals Lambda.'),
 ('Mathlib/Probability/Kernel/Composition/IntegralCompProd.lean','Measure.integral_compProd',469,473,'Finite stationary disintegration integral transport with integrability.'),
 ('Mathlib/Analysis/InnerProductSpace/Positive.lean','ContinuousLinearMap.isPositive_iff_isSelfAdjoint',273,284,'Positive real defect via quadratic form; exact name below verified by source span.'),
 ('Mathlib/Analysis/InnerProductSpace/Rayleigh.lean','ContinuousLinearMap.spectralRadius_eq_nnnorm',180,191,'Already proved for RCLike incl real; TODO is proof replacement.'),
 ('Mathlib/Analysis/InnerProductSpace/StarOrder.lean','ContinuousLinearMap.instStarOrderedRingRCLike',56,80,'Assumes real CFC; explicitly notes only complex operator CFC exists here; not a missing-instance solution.'),
 ('Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean','CFC.exists_sqrt_of_isSelfAdjoint_of_quasispectrumRestricts',255,267,'Assumes nonunital real CFC. Complex route works on complex Hilbert operators only after a real adapter.'),
 ('Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean','StarAlgHom.map_cfc',465,494,'Potential exact conjugation-equivariance ingredient for complex L2 real-subspace restriction; a suitable real star-algebra hom must be constructed, not presumed.'),
 ('Mathlib/MeasureTheory/Function/LpSpace/Basic.lean','ContinuousLinearMap.compLpL / coeFn_compLpL',813,830,'Complex.ofReal/re/im bounded Lp components for future actual complexification; no complete adapter found/admitted in this audit.'),
 ('Mathlib/Analysis/Analytic/Binomial.lean','Real.one_add_rpow_hasFPowerSeriesOnBall_zero',234,245,'Scalar open unit ball power series. Does not directly give boundary norm1 operator root, positivity or uniqueness.')
]
items=[]
for rel,name,a,b,note in apis:
    p=ROOT/'.lake/packages/mathlib'/rel;lines=p.read_text(encoding='utf8').splitlines()
    items.append({'file':pin(p),'name_or_search_locator':name,'start_line':a,'end_line':b,
                  'exact_source_span':'\n'.join(lines[a-1:b]),'assessment':note})
put('api.inventory.json',{'toolchain':'leanprover/lean4:v4.33.0',
 'mathlib_commit':'db584cd6d46c92f209a44c0f1c829460d327499d','declarations':items,
 'local_headers':headers,
 'local_search_scope':'ProximalBPS production/Tests and TechnicalLemmas searched for selfadjoint T/root/centered restriction. No public actual IsSelfAdjoint T or actual T0 contract was located in this bounded search; not a repository-wide impossibility claim.',
 'future_root_routes':[
 {'route':'Actual complex L2 extension/restriction','obligations':'Complexify SAME real T from Lp real/imag components; prove exact complex inner/norm and selfadjoint contraction; use complex CFC positive root of I-Tc²; prove conjugation equivariance and fixed-real-subspace preservation via a real star-algebra conjugation hom or polynomial approximation; restrict through actual real embedding and prove positivity/square/uniqueness. This is not merely restrictScalars, which changes scalar field while retaining complex vectors.'},
 {'route':'Constructive binomial/polynomial real root','obligations':'Full-space T may have norm1 since constants are fixed; prove coefficient summability/convergence at endpoint1, operator series square identity, positivity and uniqueness. Scalar open-ball Binomial API is insufficient without these adapters; centered normrho<1 alone misses B10/B11 full macro space.'}],
 'absence_precision':'No general real-root adapter admitted here. Neither mathematical impossibility nor absence of every usable Mathlib building block is asserted.',
 'compiler':'NOT_STARTED'})

steps=[
 'Choose SAME actual55 laws/S/U/M/T under original binders; match M to canonical snd pullback and P to actual orthogonal projection. Reuse58 range evidence only after its pending admission.',
 'Derive selfadjoint A=PUP using actual selfadjoint U and starProjection; transport <Tu,v>=<u,Tv> through PM=M and MT=AM and M.inner_map_map. Conclude actual selfadjoint T.',
 'From actual Lambda.IsCondKernel S, both marginals nu, AE source Tu formula and derived L2->L1, obtain integral_nu Tu=integral_nu u. No caller centering/stationarity premise.',
 'Define the continuous mean functional using probability class1 and innerSL; identify H0 with its kernel and derive closedness/completeness. Restrict T using derived mean preservation and prove actual T0 selfadjoint by subtype inner products.',
 'Derive positive D=I-T² and D0=I-T0², with D0 the true restriction and quadratic defect equality. Constant class1 witnesses full D kernel; legal rank0/subsingleton H0 needs no Nontrivial assumption.',
 'In an actual source Test consumer, identify58 SAME U via literal AE reflection, M via literal snd action and T via MT=AM/injectivity or source AE mean. Transport its sharp macro estimate to T0 and obtain delta=4alphaeta/(1+alphaeta)² coercivity. Production imports no Tests; an optional D0 inverse is centered-only and separate from Gamma.',
 'Stop with this one actual selfadjoint centered-operator integration prerequisite. Independently seal/review/prove later; root positivity/uniqueness, full B11, Loewner B15 and polar B16 remain separate. Do not rerun57 PI or promote58 pending status.'
]
put('next-edge.blueprint.json',{'schema_version':1,'one_edge':contract['recommended_one_edge'],
 'steps':steps,'step_count':len(steps),'maximum_steps':7,
 'proof_search_started':False,'exact_Lean_statement_or_name_authored':False,
 'downstream_actual_consumer':'D=I-T² and D0=I-T0² on the actual L2/closed centered space before real Gamma construction; actual58 Test transports the exact positive squared gap.',
 'failure_policy':'If SAME operator identification or stationary integrability fails, retire the exact route and return the minimal missing identity/domain contract. Do not replace it with caller CFC/selfadjoint/centering assumptions, finite L2 or a copied theorem consumer.',
 'source_contract':pin(OUT/'source.contract.json'),'formal_admission':False})

inputs=[OLD/'primary-pbps.exactraw.snapshot.html',OLD/'extract_and_freeze_primary.py',
 OLD/'primary.contract.json',OLD/'source.precision-addendum.json',
 ROOT/'runs/20261007-companion-priority/phase-pbps-next-primary58/source.contract.json',
 ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'docs/companion-papers-handoff.md',
 ROOT/'lean-toolchain',ROOT/'lake-manifest.json',
 ROOT/'.agents/skills/astis-source-dependency-audit/SKILL.md',ROOT/'research-wiki/technical-lemmas/README.md',
 ROOT/'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.md']
inputs += [ROOT/'.lake/packages/mathlib'/x[0] for x in apis]
put('input.manifest.json',{'schema_version':1,'inputs':[pin(p) for p in dict.fromkeys(inputs)],
 'header_inputs':headers,'mutable_control_observation':'Execution and handoff pins bind this observation; current files may change under root sole stabilization. Inputs are not immutable claims about future state.',
 'bounded_primary_reuse':True,'recursive_evidence_copy':False,'memory_use':'Memory quick pass only: current source/contracts supersede historical GibbsPositionMoment/PR301 boundaries; no old result reused as admission.'})
put('collection.process.json',{'status':'AUTHOR_SCRIPT_REACHED_NORMAL_END','timestamp':NOW(),
 'capsule_actual_exit_code':r.returncode,'compiler_started':False,
 'earlier_read_diagnostics':['Default capsule stdout GBK UnicodeEncodeError; UTF8 rerun returned0.',
 'bs4 unavailable; reused immutable stdlib HTMLParser class instead, without rerunning original author.',
 'Wrong optional precision/Map/Submodule/SDE-card paths corrected by exact rg discovery or actual source.precision-addendum.json; no proof route failed.',
 'Some earlier tool output truncation occurred; final exact anchors/headers/API spans are bounded and pinned.'],
 'no_detached_or_compiler_or_canonical_commands':True})
print(json.dumps({'status':'AUDIT_AUTHORED_FOREGROUND','anchors':len(anchors),'api_spans':len(items),
 'blueprint_steps':len(steps),'new_Lean_or_SAU_or_Git':False,'lease':'OPEN until independent foreground output readbacks exit0'}))
