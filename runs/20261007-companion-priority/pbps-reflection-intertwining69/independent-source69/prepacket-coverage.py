import collections,datetime,hashlib,json,os,pathlib,re
out=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((out/n).read_bytes())
mb=(out/'current.ReflectionIntertwining.RAW.lean').read_bytes();module=mb.decode('utf-8');lines=mb.splitlines(keepends=True)
assert len(lines)==446 and sha(mb)=='7bbaae1abd67305749d385153019061eb055a7968a707f919e7d9ac9fc21846d'
lesson=load('current.lesson.RAW.json')['units'][0];pub=load('current.publication.RAW.json')['items'][0];cell=load('current.frontier-cell.RAW.json')
source=load('frozen-source.source-proof-graph.json');nodes={x['id']:x for x in source['nodes']};iv=load('frozen-source.source-coverage-inventory.json')
regions={x['name']:x for x in load('frozen-source.source-input-regions.json')['regions']}
assert len(nodes)==22 and len(source['edges'])==49 and iv['count']==419
direct=collections.defaultdict(list)
for n in source['nodes']:
 for m in n['primary_math']:direct[m['id']].append(n['id'])
source_entries=[]
for x in iv['math_items']:
 b=(out/('source.'+x['region']+'.RAW.html')).read_bytes();a,z=x['source_RAW_range_end_exclusive'];offset=regions[x['region']]['source_RAW_range_end_exclusive'][0]
 assert sha(b[a-offset:z-offset])==x['RAW_sha256']
 n=[i for i in direct[x['id']] if int(i[1:])<=12]
 role=x['source_role'];i=x['id']
 if n:
  status='NODE';reason='Exact source statement/definition/background/ingredient of current all-micro operator edge or retained actual parent contract.'
 elif i=='A2.SS3.p8.m10':
  status='NODE';n=['P11'];reason='Same full-micro identity explicitly reused by B4; occurrence is a source consumer, not B4 completion.'
 elif role in ['source-original-hypothesis','actual-law-reflection-definition-and-semantics','actual-P-U-subspaces-and-block-prerequisite','same-root-centered-gap-inverse-polar-prerequisite','real-L2-adjoint-order-root-convention','actual-centered-fP-fperp-fV-decomposition','actual-centered-intertwining-and-cancellation']:
  status='NODE';n={'source-original-hypothesis':['P0'],'actual-law-reflection-definition-and-semantics':['P1','P2'],
   'actual-P-U-subspaces-and-block-prerequisite':['P3','P4'],'same-root-centered-gap-inverse-polar-prerequisite':['P5','P6','P7','P8'],
   'real-L2-adjoint-order-root-convention':['P2','P4','P5'],'actual-centered-fP-fperp-fV-decomposition':['P12'],
   'actual-centered-intertwining-and-cancellation':['P10','P11']}[role]
  reason='Source-present supporting context for actual geometry, bounded Hilbert semantics, centered polar restriction, or retained decomposition; no separate Lean credit inferred.'
 else:
  status='EXCLUDED';reason={
   'excluded-whole-paper-introduction':'Whole-paper rates, warm start, oracle or narrative; no such conclusion in theorem69.',
   'joint-geometry-or-oracle-upstream-context':'Other joint geometry/RGO discussion; no new geometry or oracle conclusion claimed by this operator edge.',
   'B4-actual-K-halfturn-consumer-context':'Actual K/half-turn dynamics belongs to later B4; current target is U micro compression only.',
   'B4-halfturn-source-obligation-not-B21-premise':'B17 half-turn bound and small universal step are separate later ingredients, not assumptions of69.',
   'B13-upstream-not-new-H1-caller-premise':'B13 Sobolev/gradient result is not concluded here and does not become a public regularity premise.',
   'Markov-density-downstream-context':'Density evolution/chi-square downstream result is outside current operator statement.',
   'same-B20-corrector-and-Lyapunov-definitions':'B20 corrector/Lyapunov construction belongs to subsequent actual B21/B4.',
   'B18-ordinary-energy-B4-consumer-context':'B18 ordinary-energy contraction requires actual K dynamics not proved in69.',
   'B22-B24-energy-sibling-and-B4-consumer':'Sharp-energy/norm-equivalence sibling is not a dependency or claim of69.',
   'B4-statement-and-parameters-not-B21-premise':'B4 small-step constants/decay statement remains pending.',
   'B21-leading-term-consumer':'Leading Lyapunov terms require subsequent actual rotation/corrector identity.',
   'idealization-motivation-no-rho-or-halfturn-premise':'Idealization motivation is consumer context; no rho or half-turn premise added.',
   'actual-B21-corrector-change-target':'B21 corrector change is a future actual-input consumer, not the result of69.',
   'actual-Kid-projected-rotation':'Actual g=Kid f projected rotation remains separate;69 supplies its all-micro identity ingredient.',
   'B4-B28-direct-B21-consumer':'B28 explicitly consumes B21; no B28/B4 proof claim in69.',
   'B4-shared-error-intertwining-consumer':'B4 error vector/actual K components remain later consumers; identity occurrence is separately mapped.',
   'B4-actual-rotation-norm-consumer':'Rotation norm budget belongs to later actual rotation result.',
   'B4-error-estimation-and-decay-separate-obligations':'B4 error estimates/one-step decay and final constants are outside69.'}.get(role,'Not part of the current all-micro identity or retained literal parent conclusions; explicit source consumer/context only.')
 source_entries.append(dict(id=i,classification=status,reason=reason,source_nodes=n,source_role=role,
  RAW_sha256=x['RAW_sha256'],source_RAW_range_end_exclusive=x['source_RAW_range_end_exclusive']))
assert len(source_entries)==419 and all(x['classification'] in ('NODE','EXCLUDED') and x['reason'] for x in source_entries)
put('primary419-NODE-EXCLUDED.json',dict(schema='source69-exhaustive-primary419-classification-v1',count=419,
 counts=dict(collections.Counter(x['classification'] for x in source_entries)),unclassified=0,source_regions=7,
 source_graph_nodes=22,source_graph_edges=49,entries=source_entries,entries_canonical_sha256=sha(canon(source_entries)),
 no_whole_paper_coverage_claim=True,no_implementation_edges_in_source_graph=True))

private_start=module.index('private def actual_reflection_intertwining_statement\n');private_end=module.index('\ntheorem actual_reflection_intertwining',private_start)
private=module[private_start:private_end].rstrip('\r\n')
assert private==(out/'sealed.statement0.definition.lean').read_text(encoding='utf-8').rstrip('\r\n')
public_start=module.index('theorem actual_reflection_intertwining\n');public_end=module.index(' := by\n',public_start)
public=module[public_start:public_end]+'\n'
assert public==(out/'sealed.header0-public.lean').read_text(encoding='utf-8')
parent=(out/'sealed.existing-parent67-statement.exactraw.fragment.lean').read_text(encoding='utf-8')
ds=private.index('                          let D : Hperp');de=private.index('                          (∀ f : Lp ℝ 2 J',ds)
reconstructed=(private[:ds]+private[de:]).replace('private def actual_reflection_intertwining_statement','private def actual_same_root_inverse_commutation_statement',1)
assert reconstructed.rstrip('\r\n')==parent.rstrip('\r\n')
witnesses=re.findall(r'∃ ([^ :]+)\s*:',private)
assert witnesses==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R','fP']
assert 'V0.adjoint ∘L D = -(A0 ∘L V0.adjoint)' in private
assert not re.search(r'^\s*(?:axiom|constant)\b|\b(?:sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial',module,re.M)
put('literal-statement-and-whole-module-audit.json',dict(schema='source69-current-literal-and-module-audit-v1',
 source_first_current_comparison=True,private_Prop_exact_seal=True,public_six_original_callers_exact=True,
 complete_parent_Prop_retained_except_exact_new_D_tail=True,main_witnesses=witnesses[:-1],main_witness_count=12,
 additional_per_centered_input_witness='fP under forall f with integral zero',
 no_global_inverse=True,rank0_and_alphaeta1_retained=True,no_onto_V_premise=True,
 whole_module_lines=446,whole_module_RAW_sha256=sha(mb),top_level_declarations=[
  dict(kind='private def',name='actual_reflection_intertwining_statement',lines=[17,123],owner='actual_reflection_intertwining',role='literal Prop only; no provider'),
  dict(kind='theorem',name='actual_reflection_intertwining',signature_lines=[125,133],proof_lines=[134,441])],
 imports=['ActualRootCommutation'],direct_ASTIS_calls=lesson['astis_dependencies'],
 fake_closure_scan='No axiom/constant/sorry/admit/Prop:=True/trivial closure in full current module; #print axioms is an inspection command.',
 formal_compilation_evidence='read-only PID43856 EXIT0/3948 jobs/standard3 receipt; does not establish source fidelity',
 no_final_source_verdict_before_packet=True))

spans=[(134,295),(296,315),(316,327),(328,350),(351,369),(370,441)]
math_explanations=[
 'Original six caller conditions internally produce the SAME actual laws/P/S/e/U/T/root/inverse/A0/B0/V0/R; this step only extracts and types them, including unchanged global-f conclusion.',
 'D=R U inclusion has exact residual action. Per-observable AE pullback equality and Lp/extensionality identify U2=U before B_J*D_J=-A_J B_J* is used. No unrelated reflection is substituted.',
 'Actual inclusions identify BA iota=B0, AJ iota=iota A0, and DA inclusion=inclusion D on every h:kerP. D-domain uses Ph=0, not h in ran V.',
 'For every centered u and every micro h, inner transport gives <u,B0*Dh>=-<u,A0B0*h>; separation proves B0*D=-A0B0*. Both selfadjointness facts are produced internally.',
 'V0=B0 Inv and selfadjoint SAME centered Inv imply V0*=Inv B0*. Then B0*D=-A0B0* and produced A0/Inv commutation yield V0*D=-A0V0*. No onto V or inverse outside HP0.',
 'The new D action/identity is conjoined with unchanged original global-f tail and reassembled with all SAME12 witnesses. No later rotation/corrector/B4 statement is asserted.']
step_entries=[]
for j,((a,z),s) in enumerate(zip(spans,lesson['steps']),1):
 code=b''.join(lines[a-1:z]);r=s['lean_source_region']
 assert r['start_line']==a and r['end_line']==z and r['source_raw_sha256']==sha(mb)
 assert sha(code)==r['exact_code_raw_sha256'] and code.decode('utf-8')==s['lean']
 step_entries.append(dict(step=j,title=s['title'],BODY_lines=[a,z],RAW_bytes=len(code),RAW_sha256=sha(code),
  exact_authored_code_matches=True,formula=s['formula'],mathematical_formula_review=math_explanations[j-1],
  formula_verdict='matches-current-proof-and-source-boundary',scope='current module locals preceding this span retained'))
assert sum(z-a+1 for a,z in spans)==308
assert lesson['statement']==pub['statement']==lesson['lean_statement']
assert lesson['formula']==pub['formulae'][0]['tex']
assert lesson['assumptions']==pub['assumptions']
put('six-BODY-formula-and-code-review.json',dict(schema='source69-six-exact-BODY-formula-review-v1',
 step_count=6,BODY_line_count=308,proof_line_range=[134,441],complete_contiguous_no_gaps=True,
 steps=step_entries,complete_authored_statement_matches_publication=True,main_formula_matches=True,
 formulas_use_single_LaTeX_command_backslashes=all(all(len(r)==1 for r in re.findall(r'\\+',x['formula'])) for x in lesson['steps']),
 no_final_source_verdict_before_packet=True))
line_roles=[]
for i,b in enumerate(lines,1):
 if 17<=i<=123:role='NODE-literal-full-private-Prop'
 elif 125<=i<=133:role='NODE-public-original-six-callers'
 elif 134<=i<=441:role='NODE-BODY-step-'+str(next(j for j,(a,z) in enumerate(spans,1) if a<=i<=z))
 else:role='EXCLUDED-namespace-import-options-source-docstring-formatting-or-axiom-inspection-not-an-extra-mathematical-declaration'
 line_roles.append(dict(line=i,role=role,RAW_sha256=sha(b),RAW_bytes=len(b)))
put('whole-module446-line-coverage.json',dict(schema='source69-whole-module-finite-line-coverage-v1',count=446,unclassified=0,
 entries=line_roles,entries_canonical_sha256=sha(canon(line_roles)),all_private_helpers_covered=True))

proof_graph_delta=dict(schema='source69-source-vs-implementation-route-v1',
 source_route='B5 block identity; B16 SAME polar adjoint; commute A/Gamma; both ranges in HP0; cancel Gamma using centered inverse to obtain V*D=-A V*.',
 implementation_route='Same B5 ambient identity; actual U2=U and exact inclusions; inner transport proves B0*D=-A0B0*; V*=Inv B0* and SAME A0/Inv commutation yield target.',
 classification='equivalent derived algebra factorization; internal implementation route, not a changed source hypothesis',
 explanation='Both use the same actual blocks/polar factor/centered inverse. The implementation proves the centered B0-adjoint identity before multiplying by the inverse; the source instead substitutes Gamma V* and then cancels Gamma. No new caller binder.',
 source_nodes=['P4','P7','P8','P9','P10','P11'],real_consumers=['P14','P19'],
 forbidden_parent='No sharp-energy68 parent or dependence.',remaining=['P14 actual projected rotation','P17 B21 corrector change','P19/P20/P21 B4 dynamics and errors'])
put('source-implementation-route-comparison.prepacket.json',proof_graph_delta)

put('prepacket-bounded-observations.json',dict(schema='source69-prepacket-observations-v1',actual_pid=os.getpid(),
 completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_math_covered=419,module_lines_covered=446,BODY_steps_covered=6,
 current_mathematical_findings='No extra/missing public source premise found in direct current comparison; final seven-slot verdict awaits official packet and blind reconstruction.',
 potential_reader_limitations=[dict(kind='static-renderer-complete-statement-fold',
  observation='The current lesson does not list helpers. inline_lean.disclosure statement code is the exact public signature referencing the private literal Prop. The complete Prop is in the module link, not unfolded inside that adjacent fold.',
  status='Reported to root; not a mathematical source repair; actual rendered reader acceptance remains root-owned.')],
 metadata_notes=[dict(path='source_detail_audit.gap',value=cell['source_detail_audit']['gap'],
  note='Draft cell still says not yet proved while focused proof has compiled; source/aggregate admission and stabilization remain pending. Root owns any later status reconciliation.')],
 final_source_verdict=False,canonical_reviewer_packet_received=False,blind_reconstruction_received=False,
 all_prior_semantic_verdicts_slots_deltas_repairs_not_used=True))
manifest=load('current-input-manifest.json')
for name,rel in [('renderer.inline_lean.RAW.py','website/scripts/inline_lean.py'),('renderer.declaration_lessons.RAW.py','website/scripts/declaration_lessons.py')]:
 p=repo/rel;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/name).write_bytes(b);(out/(name+'.LF')).write_bytes(lf)
 manifest['inputs'].append(dict(name=name,original_path=str(p),role='bounded-static-adjacent-code-renderer-evidence; only relevant functions reviewed',RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)))
manifest['count']=len(manifest['inputs']);put('current-input-manifest.json',manifest)
print(json.dumps(dict(actual_pid=os.getpid(),source_math_count=419,source_classification_counts=dict(collections.Counter(x['classification'] for x in source_entries)),
 module_lines=446,BODY_lines=308,BODY_steps=6,current_inputs=manifest['count'],final_source_verdict=False),sort_keys=True))
