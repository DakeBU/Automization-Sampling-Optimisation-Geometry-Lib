import collections,datetime,hashlib,json,os,pathlib,re
out=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((out/n).read_bytes())
headerb=(out/'candidate.header0-proposed-expanded.RAW.lean').read_bytes();header=headerb.decode('utf-8');lines=headerb.splitlines(keepends=True)
parent=(out/'parent69.literal-Prop.exactraw.fragment.lean').read_text(encoding='utf-8')
restored=header.replace('theorem actual_projected_rotation','private def actual_reflection_intertwining_statement',1)
old_binder='    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :\n'
assert restored.count(old_binder)==1
restored=restored.replace(old_binder,old_binder.rstrip('\n')+' Prop :=\n',1)
new_start=restored.index(' ∧\n                              let g : Lp ℝ 2 J := U (P f-(f-P f))')
oldrestored=restored[:new_start]+')\n'
assert oldrestored.rstrip('\r\n')==parent.rstrip('\r\n')
witnesses=re.findall(r'∃ ([^ :]+)\s*:',header)
assert witnesses==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R','fP','gP']
assert not re.search(r'\b(?:sorry|admit|axiom)\b|:=\s*by\b|Prop\s*:=\s*True|:=\s*trivial',header)
expected=['let g : Lp ℝ 2 J := U (P f-(f-P f))','(∫ z, g z ∂J)=0 ∧','∃ gP : HP0,','HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧','let gperp : Hperp := R g','let gV : HP0 := V0.adjoint gperp','gP=A0 fP-ΓP0 fV ∧','gV=ΓP0 fP+A0 fV ∧','‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2)']
assert all(x in header for x in expected)
callerpart=header[:header.index('    let μ :=')]
assert all(x not in callerpart for x in ['mean_g','gP','gV','Surjective','Inv','V0','ΓP0','68'])
assert 'let gP' not in header and 'let gV : HP0 := ΓP0' not in header
put('parent69-retention-and-binder-audit.json',dict(schema='header-source70-parent-retention-v1',complete_parent69_Prop_retained=True,comparison_recipe='Reverse theorem name/private literal declaration syntax; remove only appended conjunction from letg through exact energy; preserve old norm-bound and closing parenthesis; compare all remaining literal bytes modulo terminal CR/LF.',parent_fragment_RAW_sha256=sha((out/'parent69.literal-Prop.exactraw.fragment.lean').read_bytes()),candidate_RAW_sha256=sha(headerb),public_analytic_conditions=6,public_instance_conventions=['NormedAddCommGroup E','InnerProductSpace real E','FiniteDimensional real E','MeasurableSpace E','BorelSpace E'],same_common_witnesses=witnesses[:12],old_per_centered_f_witness='fP',new_per_centered_f_witness='gP constrained by actual condExpL2 g',old_D_semantics_and_all_kerP_intertwining_retained=True,old_globalf_tail_retained=True,no_added_mean_g_caller=True,no_ontoV_premise=True,no_sharp_energy68_premise=True,no_extra_smoothness=True,rank0_and_alphaeta1_retained=True,candidate_body_present=False,compiler_or_proof_search_run=False))
graph=load('frozen-source.source-proof-graph.json');nodes={x['id']:x for x in graph['nodes']};inventory=load('frozen-source.source-coverage-inventory.json');regions={x['name']:x for x in load('frozen-source.source-input-regions.json')['regions']}
direct=collections.defaultdict(list)
for n in graph['nodes']:
 for x in n['primary_math']:direct[x['id']].append(n['id'])
roles={'source-original-hypothesis':['P0'],'actual-law-reflection-definition-and-semantics':['P1','P2'],'actual-P-U-subspaces-and-block-prerequisite':['P3','P4'],'same-root-centered-gap-inverse-polar-prerequisite':['P5','P6','P7','P8'],'real-L2-adjoint-order-root-convention':['P2','P4','P5'],'actual-centered-fP-fperp-fV-decomposition':['P12'],'actual-centered-intertwining-and-cancellation':['P10','P11'],'actual-Kid-projected-rotation':['P13','P14']}
entries=[]
for x in inventory['math_items']:
 b=(out/('source.'+x['region']+'.RAW.html')).read_bytes();a,z=x['source_RAW_range_end_exclusive'];offset=regions[x['region']]['source_RAW_range_end_exclusive'][0]
 assert sha(b[a-offset:z-offset])==x['RAW_sha256']
 ns=[n for n in direct[x['id']] if int(n[1:])<=14]
 if ns:status='NODE';reason='Source-present current actual rotation,centering,energy or retained69 actual-input ingredient/definition; no Lean proof credit inferred.'
 elif x['source_role'] in roles:status='NODE';ns=roles[x['source_role']];reason='Source supporting context for same actual geometry and retained contract; source hypotheses/derived ingredients remain distinct.'
 else:status='EXCLUDED';reason='Outside current source/header target: corrector-change,sharp-energy,B4 dynamics/errors,other geometry/oracle or whole-paper context remains separate; this item supplies no new public premise and no completion claim.'
 entries.append(dict(id=x['id'],classification=status,reason=reason,source_nodes=ns,source_role=x['source_role'],RAW_sha256=x['RAW_sha256'],source_RAW_range_end_exclusive=x['source_RAW_range_end_exclusive']))
assert len(entries)==419 and len({x['id'] for x in entries})==419
counts=dict(collections.Counter(x['classification'] for x in entries))
put('primary419-NODE-EXCLUDED70.json',dict(schema='header-source70-typed-finite-source-coverage-v1',count=419,counts=counts,unclassified=0,source_regions=7,graph_nodes=22,graph_edges=49,entries=entries,entries_canonical_sha256=sha(canon(entries))))
new_line=next(i for i,b in enumerate(lines,1) if b'let g : Lp' in b)
line_entries=[]
for i,b in enumerate(lines,1):
 role='public-original-callers-and-representation' if i<=9 else 'retained-complete69-literal-conclusions' if i<new_line else 'new-actual-update-centering-projections-rotation-and-energy-conclusion'
 line_entries.append(dict(line=i,role=role,RAW_bytes=len(b),RAW_sha256=sha(b)))
put('header-line-coverage70.json',dict(schema='header-source70-exhaustive-header-lines-v1',line_count=len(lines),unclassified=0,new_actual_update_line=new_line,entries=line_entries,entries_canonical_sha256=sha(canon(line_entries))))
checks=[
 dict(id='H70-1',decision='PASS',field='same six original public conditions',evidence='Header1-9 matches parent69 callers exactly after declaration syntax; primary P0. No new caller certificate.'),
 dict(id='H70-2',decision='PASS',field='complete same69 witness/conclusion retention',evidence='Full literal deletion/reversal comparison is exact modulo terminal line endings. All12 common witnesses, D and all-micro intertwining, old globalf tail remain.'),
 dict(id='H70-3',decision='PASS',field='actual SAME g definition',evidence='letg=U(Pf-(f-Pf)); source A2.Ex10.m1[829175,829770),A2.SS3.p5.m7[829891,830255); same U/P/J from common witness scope.'),
 dict(id='H70-4',decision='PASS_WITH_INTERNAL_OBLIGATION',field='mean(g)=0',evidence='Conjoined conclusion after letg, no caller binder. Source actual reflection invariance S2.E14.m1/S2.I1.i3.p1.m1 plus conditional expectation A2.E1.m1 give integralUg=integralg and integralPf=integralf. Required ASTIS adapter is documented before candidate; not already explicitly exported by69 and not yet proved for70.'),
 dict(id='H70-5',decision='PASS',field='actual gP and gV',evidence='gP:HP0 is existential with inclusion=condExpL2 g; gperp=Rg; gV=V0.adjoint gperp. Source A2.Ex11.m1[830521,831484). Components are not defined as rotation RHS.'),
 dict(id='H70-6',decision='PASS',field='both exact signs of projected rotation',evidence='gP=A0fP-GammaP0fV; gV=GammaP0fP+A0fV. Source A2.Ex12.m1[832153,833887),A2.Ex13.m2[835227,837597),A2.Ex15.m2[845689,848662).'),
 dict(id='H70-7',decision='PASS',field='exact two-component energy',evidence='Norm-square sum equality is a derived rotation consequence of SAME selfadjoint commuting A0,GammaP0 and A0²+GammaP0²=I; source A2.SS3.p5.m20[848825,849369),m21[849410,849869). No ontoV/coisometry required and no arbitrary coefficients substituted for actual inputs.'),
 dict(id='H70-8',decision='PASS',field='source hypothesis vs internal ingredient separation',evidence='Mean preservation,actual conditional centering,adjoint block identities,root/inverse commutation and rotation algebra remain internal dependencies/conclusions. No68sharpenergy,H1,extra smoothness,rho/omega/smallc0,rank>0,alphaeta<1 or global inverse.'),
 dict(id='H70-9',decision='PASS',field='bounded scope/proposal consistency',evidence='Proposal exact_delta and source consumers match source P12/P13/P14; P16/P17 B21 corrector change and P19/B4 remain subsequent. Proposal parent-status text is historical draft metadata;69 is still not independently VERIFIED, and no status claim is adopted here.')]
put('independent-header-source70.decision.json',dict(schema='header-source70-independent-source-admission-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/independent_primary69',verdict='ADMIT_PROPOSED_HEADER_FOR_SUBSEQUENT_STATEMENT_SEAL_CONSIDERATION_ONLY',candidate_header_RAW_sha256=sha(headerb),source_expectations_before_candidate_RAW_sha256=sha((out/'source-expectations70.before-header.json').read_bytes()),header_only=True,mathematical_statement_repair_required=False,repair_proposals=[],missing_or_extra_public_source_premises=0,checks=checks,mean_g_internal_proof_obligation='Internally derive actual U integral preservation with valid AE/measure-preserving transport and conditional-P integral preservation, then mean g=0; no caller addition. This preflight neither proves nor searches that adapter.',source_math_count=419,source_coverage_counts=counts,header_lines=len(lines),complete_parent69_retained=True,all12_common_witnesses_retained=True,source_primary_only=True,old_math70_or_source69_verdict_not_used=True,no_proof_search_no_compilation_no_claim_no_seal=True,canonical_Git_ledger_Goal_edits=False,boundary='Source/header/binder/definition admission only. Parent69 not yet independently VERIFIED;70 not a proved SAU,VERIFIED,B21corrector/B4/main/fullpaper result.'))
m=load('input-manifest.json')
for context in load('source-expectations70.before-header.json')['source_context_fragments']:
 n=context['name'];b=(out/n).read_bytes();lf=b.replace(b'\r\n',b'\n');m['inputs'].append(dict(name=n,original_path='E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',source_RAW_range_end_exclusive=context['source_RAW_range_end_exclusive'],role='exact-bounded-context-derived-from-pinned-fixed-primary-already-covered-by7immutable-regions',RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)))
m['count']=len(m['inputs']);put('input-manifest.json',m)
put('bounded-synthesis70.json',dict(verdict='ADMIT_HEADER_ONLY',candidate_header_RAW_sha256=sha(headerb),source_expectations_frozen_before_header=True,six_original_callers_retained=True,common_witnesses=12,complete69_conclusions_retained=True,actual_gP_gV_not_RHS_definitions=True,mean_g_is_internal_conclusion=True,energy_is_exact_two_component_square_sum=True,rank0_alphaeta1_no_ontoV=True,source_math=419,source_counts=counts,header_lines=len(lines),individual_checks=len(checks),repair_required=False,internal_remaining='Produce actual mean preservation/centered g adapter and source-backed rotation proof; this header-only review proves none of them.',source_after='P16/P17 actual B21 corrector-change, P19/B4 remain open.',no_canonical_edits=True))
print(json.dumps(dict(actual_pid=os.getpid(),verdict='ADMIT_HEADER_ONLY',source_counts=counts,source_math=419,header_lines=len(lines),new_update_line=new_line,input_count=m['count'],repair_required=False),sort_keys=True))
