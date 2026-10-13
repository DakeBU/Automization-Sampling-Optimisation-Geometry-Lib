import hashlib,json,os,pathlib,re
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def j(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
m=j('input.manifest.json');pairs=m['qualified_raw_LF_pairs'];assert len(pairs)==29
for row in pairs:
 for k in ['original','raw_snapshot','lf_snapshot']:assert pin(R/row[k]['path'])==row[k]
def f(i):return (R/pairs[i]['raw_snapshot']['path']).read_bytes().replace(b'\r\n',b'\n').decode('utf-8')
body=[f(i) for i in [0,1,2]];names=['positive_square_roots_unique','actual_unique_positive_real_defect_root']
for i,name in enumerate(names):assert ('theorem '+name+body[i].split('theorem '+name,1)[1].split(' := by',1)[0]).strip()==f(19+i).strip()
assert not re.findall(r'^private\s', ''.join(body),re.M)
scans=[]
for i,s in enumerate(body):
 t=re.sub(r'/\-.*?\-/','',s,flags=re.S);t=re.sub(r'--[^\n]*','',t)
 bad=re.findall(r'\b(?:sorry|admit|sorryAx)\b|^\s*axiom\s|Prop\s*:=\s*True|:=\s*trivial\b',t,re.M)
 assert not bad
 if i<2:assert not re.search(r'^import\s+Tests\.',s,re.M)
 scans.append(dict(file=pairs[i]['original'],forbidden_tokens=bad,production_Test_import=False if i<2 else 'consumer Test intentionally imports production',private_helpers=0))
log=(O/'focused.stdout.log').read_text(encoding='utf-8');records={}
for name in ['AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique','AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.actual_unique_positive_real_defect_root']:
 a=re.search(re.escape("'"+name+"'")+r' depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert a
 axioms=[x.strip() for x in a.group(1).split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'};records[name]=axioms
assert 'Build completed successfully (3918 jobs).' in log
API=json.loads(f(28));checked=[]
for x in API['qualified_native_API_maps']:
 for k in ['original','selected_raw','selected_LF']:assert pin(R/x[k]['path'])==x[k]
 lo,hi=x['lines'];b=(R/x['original']['path']).read_bytes();assert b''.join(b.splitlines(keepends=True)[lo-1:hi])==(R/x['selected_raw']['path']).read_bytes()
 checked.append(x)
# Secondary draft prose pinned ONLY after primary/current proof read and focused build.
slugs=['l2-positive-real-square-root-uniqueness','pbps-unique-positive-real-defect-root'];extra=[O.parent/'publication-plan.json']
extra += [R/'website/content/declaration_lessons'/f'{s}.json' for s in slugs]+[R/'website/content/publications'/f'{s}.json' for s in slugs]
helper=R/'.astis/pbps-real-root-unique62/seal-preproof62.failed-paths.py'
if helper.exists():extra.append(helper)
for p in extra:
 b=p.read_bytes();i=len(pairs);a=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),classification='Secondary draft math/publication/read-path provenance after primary+current62 proof review; decoder not read'))
wr('input.manifest.json',m)
expo=json.loads(f(18));less=[json.loads(f(i))['units'][0] for i in [30,31]];pub=[json.loads(f(i))['items'][0] for i in [32,33]]
assert len(expo['units'][0]['steps'])==4 and len(expo['units'][1]['steps'])==3
for i in [0,1]:
 assert less[i]['steps']==expo['units'][i]['steps'];assert less[i]['statement']==less[i]['lean_statement']==pub[i]['statement']
 assert less[i]['formula']==pub[i]['formulae'][0]['tex']
steps=[
dict(step=1,formula='Ac,Bc>=0; Acι=ιA; Bcι=ιB; ||ιu||=||u||',judgment='PASS',reason='Canonical60 applied twice with EXACT same μ and canonical ofReal/re/im quotient maps. Every-g formula and every-u intertwining are genuine parent outputs. Neither positive complex extension nor isometry is caller assumption.',support='hNorm,hAf,hBf,hAi,hBi; L2RealComplexOperator.exists_positive_complex_lift'),
dict(step=2,formula='Ac²g=ιA²Rg+iιA²Qg=ιB²Rg+iιB²Qg=Bc²g',judgment='PASS',reason='All complex g covered by extensionality using literal lift formula, complex-linearity and intertwining. Applies original hSq separately at Rg,Qg. No density-only extension, missing decomposition certificate, preservation premise or multiplicativity assumption.',support='hReal,hComplexSquare; map_add,map_smul,ContinuousLinearMap.ext'),
dict(step=3,formula='Ac=sqrt(Bc²)=Bc',judgment='PASS',reason='Proof-local complex CFC and restricted-real selfadjoint CFC live on complex bounded-operator C*-algebra. sqrt_unique hComplexSquare hAcNonneg gives sqrt(Bc²)=Ac, reversed; sqrt_unique rfl hBcNonneg gives sqrt(Bc²)=Bc. Both positivity conditions used. No real-algebra CFC premise, commutation assumption or circular real uniqueness.',support='three internal letI; hAcNonneg,hBcNonneg; CFC.sqrt_unique; hSame'),
dict(step=4,formula='ιAu=Acιu=Bcιu=ιBu ⇒ A=B',judgment='PASS',reason='Canonical norm equality constructs real linear isometry e; injectivity works even zero/subsingleton. Evaluate on every real u and use operator extensionality. Arbitrary measure and possibly infinite-dimensional real L2 preserved.',support='e,e.injective,hAi,hBi,hSame; no private helper'),
dict(step=5,formula='same actual61 μ/J/ν/S/T/D/Γ and full scalar energy',judgment='PASS',reason='Actual public proof calls original-input parent61 with exactly hα,hαβ,hV,hH,hη,hβη and returns every parent witness/property unchanged. All probabilities, every-y normalized density, stationary disintegration, selfadjoint contractive mean-preserving per-u AE T and D/root positivity are internal conclusions.',support='RealDefectRoot.actual_positive_real_defect_root; rcases tuple/refine unchanged'),
dict(step=6,formula='∀ Γprime>=0, Γprime²=D=Γ² ⇒ Γprime=Γ',judgment='PASS',reason='Unique quantifier is outside parenthesized forall-u energy. Alternative requires only positivity and SAME D square; no energy/Γ certificate supplied. hΓprimeSq.trans hΓSq.symm is exact common-square equality; generic theorem used in correct direction Γprime=Γ.',support='intro Γprime hΓprime hΓprimeSq; positive_square_roots_unique _ Γprime Γ'),
dict(step=7,formula='∀ positive alternative, equality + all-u contraction/energy',judgment='PASS',reason='Genuine original-input anonymous Test obtains SAME S/T/Γ from public theorem, applies all-root uniqueness, substitutes alternative by Γ, then derives norm contraction from exact energy and nonnegative ||Tu||². No spectral gap, alternative energy assumption, fake object producer or full inverse.',support='Tests.ProximalBPSRealDefectRootUnique example; hUnique,heq,hEnergy,nlinarith')]
wr('mathematical-proof.review.json',dict(verdict='accepted-scoped-whole-math62',reviewer='/root/next_primary59',independent_from_formalizer=True,decoder_read_before_or_after_decision=False,checked_science_base='d1b150d6e59b3a9c398cc41e75a3330ef1915790',exact_math_freeze_inputs=27,all27_before_after_unchanged=True,full_public_proofs=2,private_helpers=0,seven_mathematical_formula_steps=steps,exact_headers=True,genuine_actual_input_consumer=True,public_axioms=records,fake_closure_production_import_scans=scans,API_maps_checked=checked,source_topology_reuse='Pinned original23 regions/45coverage/14node9hyperedges are SOURCE graph, not the actual Lean proof route. Current route canonical60 lift -> complex CFC uniqueness -> real isometry injection -> actual61 sameD integration. Literal D1 background unique root and scalar scope only.',domains_and_hidden_hypotheses='No finite/probability μ, finite-dimensional L2, Nontrivial, supplied CFC/root/extension/embedding/preservation certificate. Finite base E (rank0 allowed) only actual geometry. alphaη=1 legal under beta cap; no strict centered conclusion. Pointwise C is not operator adjoint; not used as a hidden extra premise in62.',secondary_publication_math='Both exact draft full statements and4+3 formulas matched current proof/Test; ASTIS parents separate from Mathlib APIs. Content is attributed scalar uniqueness; independent anti-anchored source/decoder/publication rendering/full Exposition Seal are separate gates.',compiler_evidence=j('focused.receipt.json'),negative_evidence='No independent compiler negative: exactly one nonforced focused build succeeds. Root first focused run520 positive preserved among27inputs. Historical root preproof reader-path negative has qualified helper pin if present and immutable seal bytes, no math/proof failure credit. Reviewer wrong draft-path lookup retained process-only negative.',remaining_boundary='Exported REAL scalar equal-positive-square uniqueness and SAME original-input defect/root uniqueness only. Printed jointGammaP/ontoM/typedB*B, centeredorder/inverse/polar,H1,dynamics/main/error/querycost/composition remain OPEN. No full repository gate or proof-state transition performed.',repairs=[],blocking_issues=[],state_transition_performed=False))
wr('mathematical.decision.sealed.json',dict(verdict='accepted-scoped-whole-math62',reviewer='/root/next_primary59',science_base='d1b150d6e59b3a9c398cc41e75a3330ef1915790',accepted_declarations=list(records),exact_headers=True,original27_unchanged=True,focused_build_exit_code=0,focused_build_actual_pid=3700,focused_build_jobs=3918,compiler_runs=1,nonforced=True,public_axioms=records,private_helpers=0,genuine_actual_input_all_positive_alternative_Test=True,seven_formula_steps_checked=True,decoder_not_read=True,repairs=[],blocking_issues=[],remaining_boundary=j('mathematical-proof.review.json')['remaining_boundary'],full_repository_gate_run=False,publication_source_exposition_seals_separate=True))
wr('author.receipt.json',dict(actual_foreground_pid=os.getpid(),verdict='accepted-scoped-whole-math62',original27_exact=True,pairs=len(pairs),API_maps=18,public_axioms_standard3=True,formula_steps=7,private_helpers=0,compiler_runs=1,decoder_read=False,no_canonical_Git_ledger_mutation=True))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),verdict='accepted-scoped-whole-math62',pairs=len(pairs),original27_exact=True,axioms=records,formula_steps=7,decoder_read=False)))
