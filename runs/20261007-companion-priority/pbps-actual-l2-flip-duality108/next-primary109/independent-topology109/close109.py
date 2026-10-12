import gzip
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
PKG=OUT.parent
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    p=OUT/name
    if p.exists(): raise RuntimeError('Preserve closed output: '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return p
checks=json.loads((OUT/'checks109.native.json').read_text(encoding='utf-8'))
review=[
 dict(topic='Source-selected boundary',status='PASS',reason='Original Proposition A.1(iii) names Gaussian momentum averaging and a self-adjoint Markov contraction. The final proof at3246-3259 derives self-adjointness from A.3 and flip absorption. The proposed edge explicitly selects actual averaging, real-L2 self-adjointness/contraction and zero time, leaving positivity/constant preservation red. It does not claim the whole Markov conclusion. The preceding strong-continuity proof is mathematically independent of this compression argument.'),
 dict(topic='One actual producer and witnesses',status='PASS',reason='Use actual_l2_flip_duality once. Retain its one global Z and all37 literal definitions and all inherited outputs. For each y,r retain that same all-time family A and its canonical J/hR. B is the canonical projection pullback for the same literal nu_y=pi_y times gamma; M=B.adjoint and K_T=M A_T B are derived definitions, not supplied providers. The fixed-reference proof never chooses another existential process or operator.'),
 dict(topic='Finite measure and lift',status='PASS',reason='pi_y is volume.tilted(-Vy_y), which has an IsZeroOrProbabilityMeasure instance; hence it is finite and SFinite. Standard Gaussian gamma is probability, finite and SFinite. measurePreserving_fst therefore supplies nu_y to pi_y without any position normalization premise. Its canonical real L2 pullback B is an isometry. The adjoint isometry and norm_toContinuousLinearMap_le give norm(M)<=1 and norm(B)<=1; LinearIsometry.adjoint_comp_self gives M B=id. Both L2 spaces are complete; no extra Hilbert-space completeness binder is needed.'),
 dict(topic='Gaussian L1 and identification without circularity',status='PASS',reason='For arbitrary raw G with MemLp2(nu_y), finite measure first gives G in L1. prod_right_ae gives pi_y-AE Gaussian-integrable sections and integral_prod_left gives gbar(x)=integral G(x,p) dgamma in L1. Separately, the existing class M[G] is L2 and hence L1. For measurable finite-measure s use indicatorConstLp(s,1). Its pullback and G have an integrable L2 inner product; AE representative identities identify that product with indicator_s(x)*G(x,p). Signed Fubini and adjoint_inner_right identify the s-integrals of M[G] and gbar. Integrable.ae_eq_of_forall_setIntegral_eq then gives equality AE. Only after this equality does MemLp.ae_eq give gbar in L2 and Lp.ext give the quotient identity. No L2 property of gbar is used to prove itself.'),
 dict(topic='Representative and integrability boundary',status='PASS',reason='Arbitrary MemLp representatives are permitted, including raw functions with only AE strong measurability. Product Fubini and representative equalities operate AE; there is no Borel upgrade or simultaneous exceptional set. Scalar indicator factors can be justified by the L2 product integrability already in the graph, so no unrecorded analytic domination premise is required. Finite/SFinite requirements in the pinned product APIs are internal consequences of the literal measures.'),
 dict(topic='Flip absorption and adjoint algebra',status='PASS',reason='Using Bf=f composed fst AE, Jg=g composed R AE, and transport by hR, R(x,p).1=x yields J B=B. The isometry and involution of J imply J.adjoint=J by inner-product extensionality. Taking adjoints gives M J=M. Thus (M A_T B).adjoint=B.adjoint A_T.adjoint M.adjoint=M J A_T J B=M A_T B. adjoint_comp has exactly this reversed composition order; adjoint_adjoint recovers B. Multiplicative norm bounds give contraction1, and A0=id plus M B=id gives K0=id. No sign or Gaussian normalizing factor is missing.'),
 dict(topic='Literal nested Gaussian-clock expectation',status='PASS',reason='For f in MemLp2(pi_y), let F(x,p)=f(x). MemLp.comp_measurePreserving gives F in MemLp2(nu_y), and pullback representative identities give B[f]=[F]. The same108 A_T contract gives pi_y times gamma-AE integrable clock sections and a MemLp literal opF(z)=integral f((Z(y,r,z,T,w)).1) dP. ae_ae_of_ae_prod yields pi_y-AE x, gamma-AE p clock integrability. Apply the new universal Gaussian identification to this actual opF: it gives outer Gaussian integrability AE and M[opF]=[integral_p opF(x,p)]. Together these identify K_T[f] with the specified Gaussian-outer, clock-inner expression. No triple-product Fubini or exchange of these two integrals is needed.'),
 dict(topic='Quantifiers and edge cases',status='PASS',reason='The same A family is chosen before T and all observables. B/M depend on the literal measures, not on a tested representative; K is defined from that family. All AE conclusions are parameterwise in y,r,T,f or G. Rank0 has no exceptional division or nontrivial-space requirement. T0 follows algebraically. A zero tilted measure, allowed by the generic tilted definition, gives the zero L2 space and does not invalidate this route. No source binder is added to exclude it.'),
 dict(topic='Pinned APIs and minimal reuse',status='PASS',reason='All26 listed API files, exact excerpts and line-span hashes were independently checked, together with inherited MemLp.comp_measurePreserving and adjoint_inner_left bindings. Scoped local search and inspection confirm L2Expectation is scalar averaging, L2PullbackRange is range/comap identification, and ActualCorrectorChange concerns a different joint projection. The private107 haverage_core is a useful mathematical pattern but is not callable; the proposed proof reconstructs its required argument from Mathlib. No external library port or private/mangled API is asserted.'),
 dict(topic='Topology and coverage',status='PASS',reason='Independent Kahn sorting consumes all122 distinct nodes and246 distinct edges. The107-node196-edge base records and inherited route logic are unchanged; the delta is15 nodes50 edges. All seven new AND groups have their parent edges, with no target as its own parent. The selected OR target POSITION-AVG109 does not occur in its own prerequisite list. Coverage assigns every node and edge exactly once and pins all24 source regions. Retained107 OR alternatives remain alternatives, not a mandatory union. A2 is a future consumer, not a prerequisite.'),
 dict(topic='Boundedness and scheduling',status='PASS',reason='This is one coherent actual Gaussian-average/position-compression interface with one producer and seven internal proof obligations. The nontrivial delta is universal literal integral identification and its same-process consumer, beyond abstract B.adjoint A B algebra. No missing mathematical hypothesis or API forces a strictly smaller prerequisite SAU. MOMENTUM-IDENTIFY109 is the natural internal checkpoint if implementation later exposes a concrete obstacle.108 delivery remains a scheduling condition, not a mathematical blocker identified here.')
]
decision=dict(kind='independent prospective source-only109 graph and mathematics admission',
 reviewer='/root/blind_decoder106',source_creator='/root/source_final96',
 decision='ACCEPT_EXACT_PROSPECTIVE109_GRAPH_AND_BOUNDED_ROUTE',
 recommendation_raw_sha256=h(PKG/'recommendation109.native.json'),
 interface_raw_sha256=h(PKG/'actual-interface109.native.json'),
 graph_raw_sha256=h(PKG/'source-proof-graph-delta109.native.json'),
 source_coverage_raw_sha256=h(PKG/'source-coverage109.native.json'),
 author_closure_raw_sha256=h(PKG/'closed-RAW-manifest109.native.json'),
 mathematical_review=review,blocking_findings=[],required_repairs=[],
 smaller_prerequisite_required=False,
 acceptance_boundary='Prospective source/math/topology admission only. No109 header, Statement Seal, proof, typecheck, SAU claim, integration, push or theorem-completion admission. Scheduling is conditional on root-confirmed108 delivery.',
 no_cost_inference='Norm<=1 and self-adjointness imply no query-cost, convergence, rate, implementation accuracy or full-paper result in this review.',
 remaining_red_boundaries=['Markov positivity and constant preservation','strong continuity and semigroup/restart','independent-reference integration at half-turn time','alignment with separately existential IdealHalfTurnKernel witness','complex L2 extension','hypocoercive convergence and actual expected query costs','actual-input composition and whole-paper/Goal completion'],
 owned_outputs_only=True,production_or_author_graph_mutation=False,
 no_creator_self_admission=True,checks='checks109.native.json',coverage='coverage109.native.json')
save('decision109.native.json',decision)
coverage=dict(kind='independent prospective109 coverage assessment',reviewer='/root/blind_decoder106',
 source_regions=checks['source_regions'],region_count=24,
 source_scope=[dict(lines='3000-3034',meaning='A.3 and A.1(iii): actual real-L2 Gaussian compression selected; Markov part explicitly deferred'),
  dict(lines='3246-3259',meaning='Flip absorption and compressed self-adjointness are the selected source mechanism'),
  dict(lines='3229-3243',meaning='Strong-continuity argument kept outside this edge, not smuggled in as a prerequisite'),
  dict(lines='3265-3287',meaning='Independent-reference half-turn operator is a future consumer only'),
  dict(lines='350-363;613-623;1395-1422',meaning='Unchanged six analytic source conditions and literal position/Gaussian phase laws'),
  dict(lines='Other inherited pinned regions',meaning='Actual process/count/reversal/density ancestry retained; no new109 completion credit for those regions')],
 node_edge_coverage=dict(nodes=122,edges=246,new_nodes=15,new_edges=50,
  all_node_dispositions_checked=True,all_edge_dispositions_checked=True,
  all_new_AND_groups_supported=True,ordinary_and_selected_route_cycles=False),
 proof_ingredients_vs_binders='Finite/SFinite, projection measure preservation, L2 and L1 membership, signed Fubini, quotient equality and adjoint algebra are internal proof edges/outputs. They may not be promoted to extra public premises.',
 limits='No header exists in the reviewed input. Exact binder/definition equality and compiled implementation consumption must be checked at their later gates. API source inspection and pin validation are not a new compiled ASTIS declaration.')
save('coverage109.native.json',coverage)
artifacts=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.suffix in ('.json','.py'):
        raw=p.read_bytes()
        dest=p.with_name(p.name+'.raw.gz')
        if dest.exists(): raise RuntimeError('Do not overwrite closed archive')
        dest.write_bytes(gzip.compress(raw,mtime=0))
        restored=gzip.decompress(dest.read_bytes())
        assert restored==raw
        artifacts.append(dict(path=p.name,raw_sha256=h(p),bytes=len(raw),
          archive=dest.name,gzip_sha256=h(dest),decompressed_sha256=hashlib.sha256(restored).hexdigest(),roundtrip_verified=True))
manifest=save('closed-RAW-topology109.native.json',dict(kind='closed independent prospective109 RAW evidence',
 reviewer='/root/blind_decoder106',status='closed',decision=decision['decision'],
 proposal_graph_raw_sha256=decision['graph_raw_sha256'],author_closure_raw_sha256=decision['author_closure_raw_sha256'],
 output_hashes=artifacts,closure_excluded_from_own_hash_list=True,
 source_inputs_bound_in='checks109.native.json',no_theorem_credit=True,no_canonical_mutation=True))
print(json.dumps(dict(decision_raw_sha256=h(OUT/'decision109.native.json'),closure_raw_sha256=h(manifest)),indent=2))
