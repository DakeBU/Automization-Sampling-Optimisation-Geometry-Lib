import collections, datetime, hashlib, json, os, pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
iv=json.loads((out/'source-coverage-inventory.json').read_bytes())
byid={x['id']:x for x in iv['math_items']}
def refs(ids):
 return [{k:byid[i][k] for k in ('id','alttext','RAW_bytes','RAW_sha256','source_RAW_range_end_exclusive','region')} for i in ids]
nodes=[]
def node(i,kind,statement,domain,quantifiers,ids,obligations=None):
 nodes.append(dict(id=i,kind=kind,statement=statement,domain=domain,quantifiers=quantifiers,
  primary_math=refs(ids),formal_status='not-assessed-source-only',
  source_to_implementation_obligations=obligations or []))

node('P0','source-hypotheses','mu(dx)=Z^-1 exp(-V(x)) dx; V in C^2(R^d); 0<alpha<=beta; alpha I <= Hess V <= beta I; 0<eta<=1/beta',
 'R^d; no positive-dimension requirement introduced','for every x in R^d',
 ['S1.p1.m1','S1.p1.m2','S1.p1.m3','S1.p1.m4','S1.E1.m1','S2.SS2.p1.m1'])
node('P1','actual-input-definition','pi_eta is the actual joint law; equivalently X~mu, independent standard Gaussian Z, Y=X+sqrt(eta)Z',
 'probability on R^d x R^d','same V, mu, eta throughout', ['S2.E6.m1','S2.E7.m1'])
node('P2','actual-reflection','F(x,y)=(x,2x-y) preserves pi_eta and is involutive; Uf=f composed with F',
 'U:L^2(pi_eta)->L^2(pi_eta)','all L^2 equivalence classes', ['S2.E14.m1','S2.I1.i3.p1.m1','A2.E4.m1'],
 ['derive U1=1 and mean preservation from this actual pullback; no separate caller premise'])
node('P3','actual-projection','P=conditional expectation given Y; HP=ran P; Hperp=ker P; Pperp=I-P',
 'real H=L^2(pi_eta)=HP orthogonal-sum Hperp','all f in H', ['A2.E1.m1','A2.E2.m1','A2.SS1.p1.m13','A2.SS1.p1.m14'],
 ['derive P1=1, P selfadjoint projection, mean(Pf)=mean(f), Hperp subset L^2_0'])
node('P4','source-block-identities','A=UPP, B=UperpP, D=Uperpperp; B*B=I-A^2; B*D=-A B*',
 'A:HP->HP; B:HP->Hperp; B*:Hperp->HP; D:Hperp->Hperp',
 'intrinsic block maps on their indicated spaces', ['A2.E3.m1','A2.Ex3.m1','A2.E5.m1'],
 ['derive selfadjoint A,D and block identities from SAME actual U and P; do not postulate them as public PBPS binders'])
node('P5','source-root-definition','Gamma=(I-A^2)^(1/2), the unique nonnegative root; Gamma^2=I-A^2 and A Gamma=Gamma A',
 'Gamma:HP->HP; same A, no unrelated square root','bounded real Hilbert operators', ['A2.E10.m1','A2.E11.m1','A4.SS1.p2.m7','A4.SS1.p2.m8','A4.SS1.p2.m9'],
 ['functional calculus yields commutation; Gamma1=0 and invariance of HP0 must be derived'])
node('P6','source-centered-gap','HP0=HP intersect L^2_0(pi_eta); rho_mac=(1-alpha eta)/(1+alpha eta); gamma=2 sqrt(alpha eta)/(1+alpha eta)>0; Gamma>=gamma I on HP0',
 'HP0 closed centered macro subspace; Gamma0 exact restriction','includes alpha eta=1 and HP0={0}',
 ['A2.Thmtheorem1.p1.m1','A2.E12.m1','A2.Thmtheorem1.p3.m1','A2.E14.m1','A2.E15.m1'],
 ['B15 is a source ingredient with its Appendix C.1 proof outside this finite audit; not an invented caller gap premise'])
node('P7','centered-inverse-and-invariance','A preserves HP0; Gamma0 invertible on HP0; Inv=Gamma0^-1 bounded; A0 Gamma0=Gamma0 A0 and A0 Inv=Inv A0',
 'A0,Gamma0,Inv:HP0->HP0; full Gamma is not inverted across constants','for all u in HP0',
 ['A2.SS2.p5.m1','A2.SS2.p5.m2','A2.SS3.p4.m2','A2.SS3.p4.m3','A2.SS3.p4.m4','A2.SS3.p5.m12','A2.SS3.p5.m13'],
 ['A1=1 and selfadjoint A give centered invariance; inverse commutation is an adapter derived from same root and two-sided inverse'])
node('P8','same-polar-definition','V=B0 Inv:HP0->Hperp; B0=V Gamma0; V*V=I_HP0; V is an isometry into Hperp',
 'B0=B restricted to HP0; V*:Hperp->HP0','no surjectivity of V', ['A2.E16.m1'],
 ['retain SAME Gamma0 and Inv; distinguish B0* from full B*: natural inclusion and B1=0 remove constant component'])
node('P9','adjoint-domain-adapter','B*h=i(Gamma0 V*h), equivalently B0*h=Gamma0 V*h',
 'h in Hperp; i:HP0->HP inclusion','for every h in Hperp', ['A2.SS3.p3.m3','A2.SS3.p5.m10'],
 ['B1=0 follows Pperp U P 1=0; adjoint range centeredness must be derived, not an extra input assumption'])
node('P10','range-adapter','V*D h and A V*h both belong to HP0',
 'D:Hperp->Hperp; V*:Hperp->HP0; A0:HP0->HP0','for every h in Hperp',
 ['A2.SS3.p5.m14','A2.SS3.p5.m15','A2.SS3.p5.m16','A2.SS3.p5.m17','A2.SS3.p5.m18'])
node('P11','minimal-next-actual-operator-edge','V*D=-A0 V*',
 'equality of bounded maps Hperp->HP0','for every h in Hperp, V*(D h)=-A0(V*h)',
 ['A2.Ex14.m1','A2.SS3.p5.m19'],
 ['substitute B*=i Gamma0 V* into B*D=-A B*; commute A0 with Gamma0; cancel Gamma0 on HP0 using SAME Inv'])
node('P12','actual-centered-decomposition','fP=Pf; fperp=Pperp f; fV=V*fperp; fP,fV in HP0; ||fV||<=||fperp||',
 'f in L^2_0(pi_eta), fperp in Hperp; fP and fV in HP0','every original centered L^2 f',
 ['A2.SS3.p1.m2','A2.Ex6.m1','A2.Ex8.m1','A2.SS3.p3.m11','A2.SS3.p3.m15'],
 ['actual fP/fV are computed from the SAME f; arbitrary independently supplied coefficient vectors do not satisfy this actual-input contract'])
node('P13','actual-ideal-update-definition','Kid=U(P-Pperp); g=Kid f; gP=Pg; gV=V*Pperp g',
 'Kid:H->H; g in L^2_0; gP,gV in HP0','every original centered L^2 f',
 ['A2.Ex10.m1','A2.SS3.p5.m7','A2.Ex11.m1'],
 ['derive global mean preservation of Kid, then centeredness of Pg; no new caller condition mean(g)=0'])
node('P14','actual-projected-rotation','gP=A0 fP-Gamma0 fV; gV=Gamma0 fP+A0 fV',
 'actual projections of SAME g=Kid f; vectors in HP0','every original centered L^2 f',
 ['A2.Ex12.m1','A2.Ex13.m1','A2.Ex13.m2','A2.Ex15.m1','A2.Ex15.m2','A2.SS3.p5.m20','A2.SS3.p5.m21'],
 ['first component uses actual P,U and B*; second uses P11 plus V*B0=Gamma0; do not replace actual components by definitions of the right-hand sides'])
node('P15','same-corrector-definition','C(u,v)=1/2 (||u||^2-||v||^2)-<A0 Inv u,v>',
 'u,v in HP0; real inner product','all pairs u,v in HP0; actual consumer u=fP,v=fV',
 ['A2.E20.m1','A4.E1.m1','A4.E2.m1'],
 ['bounded centered Inv only; no inversion on constants; no independent free corrector operator'])
node('P16','coefficient-algebra-ingredient','For R(u,v)=(A0u-Gamma0v,Gamma0u+A0v), C(R(u,v))-C(u,v)=-||u||^2+||v||^2',
 'real HP0 direct-sum HP0','all u,v in HP0', ['A2.Ex17.m1','A2.E21.m1'],
 ['derive from selfadjoint A0,Gamma0, commutation, A0^2+Gamma0^2=I, and SAME two-sided Inv; this ingredient alone is not actual B21'])
node('P17','B21-actual-input-target','C(gP,gV)-C(fP,fV)=-||fP||^2+||fV||^2',
 'f in L^2_0(pi_eta); g=U(P-Pperp)f; actual fP,fV,gP,gV',
 'for every original centered L^2 f under original source P0; no rho or omega binder needed',
 ['A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1'])
node('P18','leading-term-consumer','For 0<omega<rho, -rho||fperp||^2+omega(-||fP||^2+||fV||^2)<=-omega||fP||^2-(rho-omega)||fperp||^2',
 'actual f decomposition','rho and omega only enter this separate Lyapunov consumer',
 ['A2.SS3.p5.m22','A2.SS3.p5.m23','A2.Ex18.m1'])
node('P19','B4-shared-error-consumer','r_rho=V*[I+(1-rho)Hperpperp]fperp; (Kf)P=gP+Gamma0 r_rho; (Kf)V=gV-A0 r_rho',
 'r_rho in HP0; Hperpperp:Hperp->Hperp; K actual chain operator',
 'every centered f; actual SAME Kid comparator',
 ['A2.SS3.p8.m4','A2.SS3.p8.m9','A2.SS3.p8.m10','A2.Ex25.m2','A2.Ex26.m2','A2.Ex27.m1','A2.E27.m1'])
node('P20','B4-B28-direct-B21-consumer','C((Kf)P,(Kf)V)-C(fP,fV)=-||fP||^2+||fV||^2+<gP,Inv r_rho>+1/2||r_rho||^2',
 'actual f,g,Kf components and SAME corrector','every centered f under B4 context',
 ['A2.Ex28.m1','A2.Ex31.m1','A2.Ex33.m1','A2.Ex34.m1','A2.Ex35.m1','A2.Ex36.m1','A2.E28.m1'],
 ['explicit source href to B21 at RAW offset 926328; B21 supplies exactly the first two terms'])
node('P21','B4-error-and-decay-obligations','B17 and inverse bound control r_rho; B30 plus rotation norm budget yield B31; B18+B31 give Lyapunov decay; B22 converts norm to L_omega',
 '0<rho<=1/2, beta eta<=c0 with c0<=1/16; Lambda_rho=log(1/gamma)+(rho/gamma)^2; omega=c_hyp rho/Lambda_rho',
 'universal positive constants as B4; gamma<=1/2 is local B4 small-step consequence only',
 ['A2.E17.m1','A2.E25.m1','A2.Thmtheorem4.p1.m1','A2.Thmtheorem4.p1.m2','A2.E29.m1','A2.E29.m2','A2.E30.m1','A2.E30.m2','A2.SS3.p9.m2','A2.E31X.m2','A2.Ex40.m2','A2.Ex44.m1','A2.Ex45.m1','A2.E26.m1'],
 ['B17 proof in C.2/C.3 is outside finite source selection and remains separate; B21 alone never implies B4'])

edges=[]
def edge(a,b,why):edges.append(dict(parent=a,child=b,kind='source-proof-ingredient-not-certified-Lean-edge',reason=why))
for a,b,why in [
 ('P0','P1','original actual-law data'),('P1','P2','actual reflection invariance'),('P1','P3','actual conditional expectation'),
 ('P2','P4','selfadjoint involution blocks'),('P3','P4','intrinsic block domains'),('P4','P5','positive square root of I-A^2'),
 ('P0','P6','B1 original parameter assumptions'),('P5','P6','same Gamma in B15'),('P2','P7','constants fixed and mean preserved'),
 ('P3','P7','P fixes constants and centered macro is reducing'),('P5','P7','same-root functional-calculus commutation'),
 ('P6','P7','centered bounded inverse'),('P4','P8','same B restriction'),('P7','P8','same centered inverse defines V'),
 ('P8','P9','adjoint of polar identity'),('P2','P9','B1=0 from reflection fixing constants'),('P3','P9','constant-complement inclusion'),
 ('P7','P10','A0 centered invariance'),('P8','P10','V* codomain HP0'),('P4','P11','B*D=-A B*'),
 ('P9','P11','replace B* by Gamma0 V* with explicit inclusion'),('P10','P11','both ranges are in cancellable centered space'),
 ('P7','P11','commutation and cancel SAME Gamma0 using SAME Inv'),('P3','P12','actual Pf and Pperp f; mean preservation'),
 ('P8','P12','actual polar adjoint and its contraction'),('P2','P13','actual U preserves mean'),('P3','P13','P-Pperp preserves centered input'),
 ('P13','P14','actual g and projections'),('P12','P14','original f decomposition'),('P9','P14','macro block computation'),
 ('P11','P14','micro coefficient computation'),('P8','P14','V*B0=Gamma0'),('P7','P15','well-defined SAME centered inverse'),
 ('P5','P16','selfadjoint commuting A,Gamma and A^2+Gamma^2=I'),('P7','P16','same inverse and inverse commutation'),
 ('P15','P16','specific B20 corrector'),('P14','P17','actual pair realizes rotation'),('P16','P17','substitution into actual pair'),
 ('P17','P18','negative macro plus coupled micro contribution'),('P12','P18','||fV||<=||fperp||'),
 ('P11','P19','same intertwining identity in B4 p8.m10'),('P9','P19','same B* polar adjoint in B4 p8.m9'),
 ('P13','P19','same actual comparator Kid'),('P19','P20','B27 perturbation of actual pair'),('P15','P20','expand B20 corrector'),
 ('P17','P20','explicit B21 addition yields B28'),('P14','P21','rotation coefficient norm budget'),
 ('P20','P21','B28 leading terms plus error estimate'),('P18','P21','macro/micro coercive mechanism'),
 ]:edge(a,b,why)

graph=dict(schema='primary69-independent-source-proof-graph-v1',built_from='exact RAW HTML only, before candidate69',
 source='arXiv:2609.06905v1 fixed primary',nodes=nodes,edges=edges,exact_primary_reference_B21_B4_RAW_offset=926328,
 source_dependency_edges_are_not_Lean_edges=True,no_prior_graph_or_verdict_used=True,
 external_source_proof_boundaries=[dict(source='B15 proof Appendix C.1',status='source-cited-not-audited-here'),
  dict(source='B17 proof Appendix C.2/C.3',status='source-cited-not-audited-here')])
put('source-proof-graph.json',graph)

explicit=[dict(id='H1',scope='B21 actual PBPS result',condition='V in C^2(R^d); 0<alpha<=beta; alpha I<=Hess V(x)<=beta I for every x',source_ids=['S1.p1.m3','S1.p1.m4','S1.E1.m1']),
 dict(id='H2',scope='B21 actual PBPS result',condition='0<eta<=1/beta (equivalently eta>0 and beta eta<=1)',source_ids=['S2.SS2.p1.m1','A2.Thmtheorem1.p1.m1']),
 dict(id='H3',scope='B21 actual observable',condition='f in real L^2_0(pi_eta); a.e. equivalence classes',source_ids=['A2.SS3.p1.m2','A4.E1.m1','A4.E2.m1']),
 dict(id='H4',scope='B4 only, never inserted in B21',condition='0<rho<=1/2; beta eta<=c0 universal small; c0<=1/16; Lambda,omega as B25',source_ids=['A2.SS3.p2.m1','A2.Thmtheorem4.p1.m2','A2.E25.m1','A2.SS3.p8.m1'])]
implicit=[
 'mu,pi_eta are normalized probability laws; real L2 functions are measurable classes with finite second moment, hence integrable for centering',
 'P is the SAME conditional expectation for the SAME Y under the SAME pi_eta, not an arbitrary projection',
 'U is the SAME measure-preserving involution pullback; it fixes constants, is unitary and selfadjoint, and preserves global mean',
 'HP0 is closed and reducing for A and Gamma; all restrictions/inclusions must agree on inherited vectors',
 'Gamma is the unique nonnegative root of I-A^2 and is never swapped for an unrelated positive operator',
 'Gamma0 inverse exists only on HP0; its two-sided identities, boundedness, and commutation are derived ingredients',
 'V is precisely B0 Gamma0^-1; its adjoint codomain is HP0 and V*V=I; V V* is only a range projection',
 'Full B* has zero constant component because B1=0; the inclusion of centered B0* into HP must be explicit',
 'Kid preserves mean, so actual gP is in HP0; actual gV is in HP0 by the V* codomain',
 'Products and inner products use bounded operators on the indicated real Hilbert spaces; no pointwise representative equality is asserted']
forbidden=[
 'No rank>0, dim HP0>0, dimension>0, nonzero vector, or nontrivial-centered-space premise',
 'Do not replace beta eta<=1 by a strict bound, alpha eta<1, gamma<1, or gamma<=1/2 in B21; alpha eta=1 remains included',
 'No V onto Hperp premise, V V*=I_Hperp conclusion, or replacement fperp=V fV; an orthogonal residual is allowed',
 'No global Gamma inverse on HP across constants',
 'No extra H1, smoothness of f, boundedness of f, Hessian beyond C2, higher derivatives, or representative regularity',
 'No warm-start, density, oracle, rho, omega, half-turn error, or small universal c0 condition in the B21 identity',
 'No free selfadjointness, root-square, commutation, inverse, polar, centered-range, projected-rotation, or corrector-change public caller assumptions on an actual PBPS result',
 'No mere arbitrary-coefficient algebra theorem presented as actual-input B21',
 'No source-only preflight presented as compiled, independently source-reviewed candidate acceptance, B21 completion, B4 completion, or full-paper completion']
expect=dict(schema='primary69-source-expectations-seal-v1',freeze_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 before_candidate69=True,source_only=True,explicit_source_hypotheses=explicit,implicit_domain_and_semantic_contracts=implicit,
 forbidden_strengthening=forbidden,source_ingredients_are_obligations_not_public_binders=True,
 target=dict(intertwining=nodes[11],actual_rotation=nodes[14],actual_corrector_change=nodes[17]),
 minimal_independently_meaningful_next_edge=dict(id='P11',statement='forall h:Hperp, V*(D h)=-A0(V*h)',
  meaning='same actual PBPS root/inverse/polar operator; reusable for both ideal rotation and B4 error components',
  consumer_ids=['P14','P19'],status='source-backed expectation only; no Lean/API claim'),
 separate_adapters=[dict(id=i,statement=nodes[int(i[1:])]['statement']) for i in ['P7','P9','P10','P12','P13']],
 subsequent_actual_input_edge=['P13','P14','P15','P16','P17'],
 endpoints=dict(rank_zero='HP0={0} is allowed; operators and identities are interpreted on the zero space',
  alpha_eta_one='Allowed by beta eta<=1 and alpha<=beta; gamma=1 and rho_mac=0; A0=0 follows source B14; no division by rho_mac or log(1/gamma) in B21',
  B4='B4 small-step hypotheses separately force gamma<=1/2; their logarithmic denominator does not restrict B21'))
put('source-expectations.json',expect)

algebra=dict(schema='primary69-source-directed-B21-algebra-expansion-v1',status='mathematical reconstruction, no Lean proof claim',
 u_v_domain='u,v in HP0; apply to actual pair only after P14',
 definitions=['A=A0, G=Gamma0, J=Inv, L=A J','R(u,v)=(Au-Gv,Gu+Av)','C(u,v)=1/2(||u||^2-||v||^2)-<Lu,v>'],
 ingredients=['A,G selfadjoint','A G=G A','A^2+G^2=I','G J=J G=I','A J=J A'],
 steps=[
  'Expand the half norm difference: 1/2(||Au-Gv||^2-||Gu+Av||^2)=1/2<u,(A^2-G^2)u>-1/2<v,(A^2-G^2)v>-2<AGu,v>.',
  'Use JG=I to expand <A J(Au-Gv),Gu+Av>=||Au||^2-||Av||^2+<(A^3 J-A G)u,v>.',
  'Subtract C(u,v). The u diagonal is -||Gu||^2-||Au||^2=-||u||^2; the v diagonal is ||Gv||^2+||Av||^2=||v||^2.',
  'The remaining mixed operator is -A G-A^3 J+A J=A J(I-A^2)-A G=A J G^2-A G=0.',
  'Therefore C(R(u,v))-C(u,v)=-||u||^2+||v||^2.',
  'Insert u=fP and v=fV only after actual projected g components have been established as R(fP,fV).'],
 no_onto_V_used=True,no_strict_gap_endpoint_used=True)
put('source-directed-algebra-expansion.json',algebra)

def role(x):
 i=x['id'];r=x['region']
 if r=='global-assumptions': return 'source-original-hypothesis' if i.startswith('S1.p1.') or i=='S1.E1.m1' else 'excluded-whole-paper-introduction'
 if r=='actual-joint-law':
  return 'actual-law-reflection-definition-and-semantics' if i in {'S2.SS2.p1.m1','S2.SS2.p1.m2','S2.SS2.p1.m3','S2.E6.m1','S2.E7.m1','S2.E8.m1','S2.E14.m1','S2.I1.i3.p1.m1'} else 'joint-geometry-or-oracle-upstream-context'
 if r=='conditional-reflection-blocks-B1':
  return 'B4-actual-K-halfturn-consumer-context' if i.startswith('A2.SS1.p4.') or i.startswith('A2.Ex4.') or i.startswith('A2.Ex5.') or i in {'A2.E6.m1','A2.E7.m1','A2.Ex1.m1','A2.Ex2.m1'} else 'actual-P-U-subspaces-and-block-prerequisite'
 if r=='same-root-polar-B2':
  if i.startswith('A2.Thmtheorem2.') or i=='A2.E17.m1' or i.startswith('A2.SS2.p7.') or i in {'A2.SS2.p5.m6','A2.SS2.p5.m7'}:return 'B4-halfturn-source-obligation-not-B21-premise'
  if i=='A2.E13.m1' or i.startswith('A2.Thmtheorem1.p2.'):return 'B13-upstream-not-new-H1-caller-premise'
  return 'same-root-centered-gap-inverse-polar-prerequisite'
 if r=='real-L2-spectral-conventions-D1':
  return 'real-L2-adjoint-order-root-convention' if not (i.startswith('A4.Thmtheorem2.') or i.startswith('A4.SS1.p3.') or i in {'A4.E4.m1','A4.E5.m1'}) else 'Markov-density-downstream-context'
 if r=='corrector-sharp-energy-and-consumers-B3':
  if i.startswith('A2.SS3.p1.') or i.startswith('A2.Ex6.') or i.startswith('A2.SS3.p3.') or i.startswith('A2.Ex8.'):return 'actual-centered-fP-fperp-fV-decomposition'
  if i.startswith('A2.SS3.p4.') or i in {'A2.E19.m1','A2.E20.m1'}:return 'same-B20-corrector-and-Lyapunov-definitions'
  if i.startswith('A2.SS3.p2.') or i.startswith('A2.Ex7.') or i=='A2.E18.m1':return 'B18-ordinary-energy-B4-consumer-context'
  if i.startswith('A2.Thmtheorem3.') or i.startswith('A2.SS3.p6.') or i.startswith('A2.SS3.p7.') or i.startswith(('A2.Ex19.','A2.Ex20.','A2.Ex21.','A2.Ex22.','A2.E22.','A2.E23.','A2.E24.')):return 'B22-B24-energy-sibling-and-B4-consumer'
  if i.startswith('A2.Thmtheorem4.') or i.startswith(('A2.E25.','A2.E26.')):return 'B4-statement-and-parameters-not-B21-premise'
  if i.startswith('A2.Ex18.') or i in {'A2.SS3.p5.m22','A2.SS3.p5.m23','A2.SS3.p5.m24'}:return 'B21-leading-term-consumer'
  if i.startswith('A2.Ex9.') or i in {'A2.SS3.p5.m1','A2.SS3.p5.m2','A2.SS3.p5.m3','A2.SS3.p5.m4','A2.SS3.p5.m5','A2.SS3.p5.m6'}:return 'idealization-motivation-no-rho-or-halfturn-premise'
  if i.startswith(('A2.Ex14.',)) or i in {'A2.SS3.p5.m10','A2.SS3.p5.m11','A2.SS3.p5.m12','A2.SS3.p5.m13','A2.SS3.p5.m14','A2.SS3.p5.m15','A2.SS3.p5.m16','A2.SS3.p5.m17','A2.SS3.p5.m18','A2.SS3.p5.m19'}:return 'actual-centered-intertwining-and-cancellation'
  if i.startswith(('A2.Ex16.','A2.Ex17.','A2.E21.')):return 'actual-B21-corrector-change-target'
  return 'actual-Kid-projected-rotation'
 if r=='corrector-change-B4-consumer-proof':
  if i.startswith(('A2.Ex35.','A2.Ex36.','A2.E28.')):return 'B4-B28-direct-B21-consumer'
  if i in {'A2.SS3.p8.m9','A2.SS3.p8.m10'} or i.startswith(('A2.Ex25.','A2.Ex26.','A2.Ex27.','A2.E27.')):return 'B4-shared-error-intertwining-consumer'
  if i=='A2.SS3.p9.m2':return 'B4-actual-rotation-norm-consumer'
  return 'B4-error-estimation-and-decay-separate-obligations'
 raise AssertionError((i,r))
for x in iv['math_items']:x['source_role']=role(x)
iv['all_classified']=True;iv['classification_counts']=dict(sorted(collections.Counter(x['source_role'] for x in iv['math_items']).items()))
assert iv['count']==419 and len(set(x['id'] for x in iv['math_items']))==419
put('source-coverage-inventory.json',iv)
finite=[dict(id=x['id'],region=x['region'],RAW_sha256=x['RAW_sha256'],source_RAW_range_end_exclusive=x['source_RAW_range_end_exclusive'],source_role=x['source_role']) for x in iv['math_items']]
put('finite-coverage-manifest.json',dict(schema='primary69-typed-finite-source-coverage-v1',
 count=419,prior_six_region_count=344,new_B4_consumer_region_count=75,missing=0,unclassified=0,
 closure='all 419 selected math elements parsed from exact fixed RAW, TeX annotation equals alttext, exact offsets/hash checked; no whole-paper inventory claim',
 classification_counts=iv['classification_counts'],entries=finite,entries_canonical_sha256=sha(canon(finite))))
put('literal-formulas-and-conditions.json',dict(schema='primary69-exact-primary-expectation-anchors-v1',
 anchors=refs(sorted(set(y['id'] for n in nodes for y in n['primary_math']))),
 source_before_candidate69=True,source_prose_assertions=[dict(id='A2.SS3.p5',fact='both ranges centered, bounded inverse cancellation'),
  dict(id='A2.SS3.p8.8',fact='Consequently, combined with B21',explicit_href_RAW_offset=926328)]))
put('visibility-and-negative-observations.json',dict(schema='primary69-visibility-boundary-v1',
 no_candidate69_seen=True,no_candidate69_header_seen=True,no_Lean_module_semantics_reviewed=True,
 no_decoder_files_read=True,no_prior_source_math_verdict_used=True,
 opaque_predecessor_hashing_authorized_by_parent=True,upstream_payload_non_HTML_entries_not_decoded=True,
 incidental_agent_status_exposure=dict(tool='collaboration.list_agents',content='unrelated decoder68 completion status summary',
  files_read=False,used_in_source_reconstruction=False,disclosed_to_parent=True),
 transient_console_observations=[dict(tool_chunk='cfda4f',actual_exit=0,issue='initial allowed upstream RAW-input metadata console output truncated; re-read structurally with HTML-only semantic extraction'),
  dict(tool_chunk='0c2b64',actual_exit=0,issue='first B4 finite slice ended at p9; extended to include p9 then p10, with final boundary before p11'),
  dict(tool_chunk='1881f4',actual_exit=1,issue='UTF-8 context sample ended mid-character; display failed, no source bytes changed; exact source parser already used UTF-8 boundary-complete elements'),
  dict(tool_chunk='bd853e',actual_exit=0,issue='fixed-primary context preview included later source after B4; excluded from source conclusion and finite selection; whole primary exact bytes bound separately')],
 mathematical_or_formal_completion_claim=False))
summary=dict(schema='primary69-bounded-synthesis-v1',outcome='PRIMARY_SOURCE_EXPECTATIONS_FROZEN',
 claim_boundary='Source-only preflight. No Goal/SAU claim, no Lean proof, no candidate/header review, no B21/B4/paper completion.',
 fixed_primary_RAW_bytes=1482128,fixed_primary_RAW_sha256='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760',
 source_coverage=dict(prior_CLOSED59_opaque_integrity_verified=True,prior_six_region_count=344,new_B4_count=75,total=419,unclassified=0),
 next_edge='P11: actual same-polar centered intertwining V*D=-A0 V* on all Hperp',
 actual_input_target='g=U(P-Pperp)f; (Pg,V*Pperp g)=(A0 fP-Gamma0 fV,Gamma0 fP+A0 fV); same B20 corrector change=-||fP||²+||fV||²',
 B4_consumers=['p8.m10 uses intertwining to construct SAME error vector B27','B28 explicitly adds B21 into actual corrector difference','rotation norm identity feeds B31','B31+B18 and B22 lead to B26 under separate B4 hypotheses'],
 separate_adapters=['constant/mean preservation','centered A/Gamma restrictions','centered inverse and commutation','full B* inclusion into HP from B0*','both cancellation ranges in HP0','actual g centeredness'],
 forbidden_strengthening=['rank>0','alpha eta<1','V onto','global inverse','B21 small-c0/halfturn/rho/omega premise','actual source ingredient moved to public caller binder'],
 source_proof_graph_node_count=len(nodes),source_proof_graph_edge_count=len(edges),source_only_before_candidate69=True,
 unresolved='Formal implementation/API compatibility and candidate69 source fidelity are not assessed. B15/B17 source proof leaves outside finite selection are referenced, not independently proved here.')
put('bounded-synthesis.json',summary)
freeze=dict(schema='primary69-source-expectations-freeze-receipt-v1',actual_pid=os.getpid(),freeze_utc=expect['freeze_utc'],
 candidate69_seen=False,source_graph_RAW_sha256=sha((out/'source-proof-graph.json').read_bytes()),
 expectations_RAW_sha256=sha((out/'source-expectations.json').read_bytes()),
 finite_coverage_RAW_sha256=sha((out/'finite-coverage-manifest.json').read_bytes()),source_math_count=419)
put('source-expectations-frozen.json',freeze)
print(json.dumps(freeze,sort_keys=True))
