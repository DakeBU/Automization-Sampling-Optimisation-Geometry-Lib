from pathlib import Path
import json, hashlib, re
R=Path('E:/Samplinglib'); O=Path(__file__).resolve().parent; RUN=O.parent
P=R/'runs/20261007-companion-priority/pbps-countable-endpoint-preread105'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepared=load(O/'prepared-inputs105.native.json')
for x in prepared['inputs']:assert info(R/x['path'])==x,x['path']
kernel=load(O/'fresh-kernel-receipt105.native.json');assert kernel['exit_code']==0 and kernel['terminal_closed']
axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",(O/'fresh-kernel.stdout.log').read_text(encoding='utf-8'))
assert len(axioms)==2 and all({v.strip() for v in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for _,a in axioms)
root=RUN/'focused105/production1';receipt=load(root/'receipt.json')
assert receipt['exit_code']==0 and receipt['terminal_closed']
assert receipt['input_raw_sha256']==sha(M.read_bytes())=='31003aa5df1826329f8e57740860e9a0e7c1b866ab110108974e1a339a96bbca'
assert (root/'input.exactraw.lean').read_bytes()==M.read_bytes()
assert load(O/'fake-closure-scan105.native.json')['decision']=='PASS'
top=load(P/'independent-header-math105/source-topology-admission105.native.json')
assert top['effective_graph']['node_count']==60 and top['effective_graph']['edge_count']==112
assert info(R/top['v2_graph']['path'])==top['v2_graph']
graph=load(R/top['v2_graph']['path'])
transfer=[]
for key in ['base_source_graph104','independent_base_topology_binding','independent_base_topology_admission','inherited_compiled_coverage']:
 x=graph[key];assert info(R/x['path'])==x;transfer.append(x)
raw=M.read_bytes();lines=raw.splitlines(keepends=True)
spec=[(1,19,'Actual104 and UnitExponentialProduct imports; namespace only.'),
 (20,154,'Private literal proposition exactly matches original Header and seal. Six original assumptions; literal actual93 recursion, actual phase Gibbs measure, one global Z with its four identification clauses, and three endpoint-law conclusions.'),
 (155,174,'One public theorem. All six source assumptions passed to public93; the SAME existential Z, joint measurability, raw-arc identity, fallback identity and zero-time AE identity returned without modification.'),
 (175,188,'Actual103 normalized phase equality transports its probability instance to literal nu. UnitExponentialProduct supplies actual P probability before product/Tonelli; joint Z gives measurable M and probability of its pushforward Q.'),
 (189,199,'Actual93 jointly measurable Gamma evaluated at T gives B; joint rho specializes with a measurable fixed-parameter embedding.'),
 (200,222,'Literal strict Delta is Borel by finite coordinate inequalities, including Fin0. Exact subtype comap maps to restricted ambient volume; sigma-finiteness pulled back using measurable subtype map.'),
 (223,230,'Measure equality tested against all measurable ENNReal functions. D is the exact sector integral; joint B/rho plus sigma-finite simplex prove measurable D in initial phase.'),
 (231,253,'For EACH fixed initial state, measurable Nat-count fibers are disjoint and cover every clock sequence. lintegral_iUnion then public93 all-test restricted law with terminal path evaluation identifies each fiber integral. No joint-in-z N assumption or exceptional-set uniformization.'),
 (254,280,'Measurable pushforward integral, actual product Tonelli, pointwise fixed-z identity, measurable nonnegative sum interchange, sector density/product formula and lintegral_sum_measure identify Q with sum L. Multiplication commuted explicitly; no subtraction, normalization per sector, domination or finite-integral condition.'),
 (281,292,'Public104 supplies J preservation for each literal sector. Its n=0 projection supplies global measurability of J even when a sector is zero; map_sum and pointwise map equality give the final global symmetry.')]
assert spec[0][0]==1 and spec[-1][1]==len(lines)
for a,b in zip(spec,spec[1:]):assert a[1]+1==b[0]
save('reviewed-code-regions105.native.json',{'production':info(M),'regions':[dict(line_start=a,line_end=b,raw_sha256=sha(b''.join(lines[a-1:b])),bytes=len(b''.join(lines[a-1:b])),review=n) for a,b,n in spec],'full_module_covered':True})
trials=[]
for d in sorted((RUN/'focused105').iterdir()):
 p=d/'receipt.json'
 if p.exists():
  v=load(p);trials.append({'name':d.name,'receipt':info(p),'exit_code':v.get('exit_code'),'artifacts':[info(x) for x in sorted(d.iterdir()) if x.is_file()]})
save('whole-math-decision105.native.json',{
 'decision':'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL','reviewer':'/root/exact_verifier96',
 'production':info(M),'header':info(P/'Header105.lean'),'seal':info(P/'root.statement-seal105.json'),'fresh_kernel':info(O/'fresh-kernel-receipt105.native.json'),'root_terminal_production':info(root/'receipt.json'),
 'kernel_contract':{'production_prefix_exact_bytes':True,'target_module_not_imported':True,'original_header_candidate_present':True,'literal_header_seal_privateProp_equal':True,'witness_checks_expanded_Prop':True,'axioms':[{'declaration':n,'axioms':[v.strip() for v in a.split(',')]} for n,a in axioms],'no_sorryAx':True},
 'whole_module_ownership':'Only one private statement and one public theorem. Every auxiliary fact is internal to this proof. No private producer access, added provider hypothesis, or arbitrary endpoint/process/density input.',
 'genuine_direct_parents':[
 {'declaration':'ActualFiniteCountPath.actual_finite_count_path_law','use':'One global actual Z and its identification clauses; joint Gamma/rho measurability; fixed-state count measurability and every measurable nonnegative fixed-count path test identity.'},
 {'declaration':'ActualPhaseNormalization.actual_phase_gibbs_normalization','use':'Actual normalized phase measure equality plus probability, transported to literal tilted-position times standard-Gaussian nu.'},
 {'declaration':'UnitExponentialProduct.unit_exponential_product_laws','use':'Actual infinite product Exp(1) probability, used both for Q probability and the SFinite P prerequisite of Tonelli.'},
 {'declaration':'ActualNormalizedEndpointSector.actual_normalized_endpoint_sector_reversal','use':'Momentum-flipped endpoint-swap measurability and map equality for every literal normalized sector.'}],
 'assumption_audit':'The original six hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta only; each parameterized actual producer receives these unchanged. Joint count measurability, normalizer, minimizer, nonzero rates, positive dimension, nonempty simplex and finite test integrals are not assumed.',
 'mathematical_findings':[
 'The global existential Z is extracted once before y,r,T; raw-arc/fallback/zero-time clauses come from that same witness. Sector densities and Gamma use the exact sealed actual93 literals.',
 'Nat fibers partition all clocks even on fallback or exceptional inputs. The actual93 restricted law already handles these at the fixed-state measure level; no unproved joint count or uniform AE claim is used.',
 'After the fixed-state equality, joint sector integrand measurability supplies measurable initial-state integrals. Tonelli uses probability P and internally derived SigmaFinite m; the repaired UnitExponentialProduct-to-ASSEMBLY105 dependency is genuinely consumed.',
 'Q is the actual nu.prod P pushforward. Equality against all measurable ENNReal tests proves the exact countable sum of endpoint sector measures, preserving phase-first product order and terminal evaluation.',
 'The same literal J is measurable globally from any104 sector preservation result, including n=0. Countable map_sum plus sector map equalities proves its preservation of Q.',
 'No signed duality, marginal invariance, semigroup property, convergence or complete-paper result is claimed.'
 ],
 'edge_cases':{'n0':'Fin0, empty products and unique zero-count tuple remain included in the sum; no positive-count argument.','T0':'Positive-count strict simplexes are empty; zero-count sector remains. Uniform actual93 and104 laws discharge the boundary.','rank0':'Finite-dimensional producers and Gaussian/volume contracts include zero dimension; no division by rank.','zero_normal_or_rate':'Literal total reflection, hitting/fallback convention and vanishing densities are retained; no cancellation by rate or density.','infinite_tests':'All assembly uses ENNReal nonnegative lintegrals and countable sums, including infinity. No finite-integral side condition or infinity subtraction.'},
 'source_graph_transfer':{'admission':info(P/'independent-header-math105/source-topology-admission105.native.json'),'v2_graph':top['v2_graph'],'effective_nodes':60,'effective_edges':112,'unchanged_inherited_bindings':transfer,'role':'Reused independent noncreator topology admission; implementation consumption checked. Not a fresh anti-anchored source verdict.'},
 'retained_failures':trials,'failure_scope':'Assembly1/2 are retained negative API/representation elaboration trials; they do not certify a theorem. Assembly3, exact production and independent expanded-header witness pass with standard three axioms.',
 'warnings':'Harmless letI/proposition style and candidate unused-binder lints only; no production repair requested.',
 'code_regions':info(O/'reviewed-code-regions105.native.json'),'fake_closure':info(O/'fake-closure-scan105.native.json'),'defects':[],
 'publication_used':False,'source_review_verdict_issued':False,'VERIFIED_transition':False,
 'remaining':'Mathematical acceptance only. Final independent source/decoder/publication and frozen exact-science commit admission remain. No integration, main-merge, purification or whole-paper credit.'})
inputs={x['path']:x for x in prepared['inputs']}
for x in transfer:inputs[x['path']]=x
for trial in trials:
 for x in trial['artifacts']:inputs[x['path']]=x
save('closed-RAW-manifest105.native.json',{'kind':'closed independent whole mathematical and kernel review','reviewer':'/root/exact_verifier96','inputs':list(inputs.values()),'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_shared_mutations':True,'no_new_primary_archive':True,'VERIFIED_transition':False})
for n in ['whole-math-decision105.native.json','fresh-kernel-receipt105.native.json','closed-RAW-manifest105.native.json']:print(n,info(O/n)['raw_sha256'])
