import sys,pathlib,json,subprocess,hashlib,re,datetime
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
import astis,astis_publication as pub
R=pathlib.Path('runs/20261006-companion-priority/scaled-resolvent-limit')
C='5cf2cd36f3e72cef6f61a4aa1856e1abaca3fa54'
V='picard_commit_verifier_20261005'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==C
def rd(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def sh(b):return hashlib.sha256(b).hexdigest()
def fr(p,git=False):
 p=str(p).replace(chr(92),'/');b=pathlib.Path(p).read_bytes()
 q={'path':p,'raw_sha256':sh(b),'lf_sha256':sh(b.replace(b'\r\n',b'\n')),'normalized_sha256':sh(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
 if git:
  g=subprocess.check_output(['git','show',C+':'+p])
  q.update(git_commit=C,git_raw_sha256=sh(g),git_lf_sha256=sh(g.replace(b'\r\n',b'\n')),git_LF_equals_worktree=g.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'))
  assert q['git_LF_equals_worktree'],p
 return q
claim=rd(R/'claim.json')
original=rd(R/'math-freeze.json')['inputs'];current=[]
for x in original:
 q=fr(x['path']);assert q['raw_sha256']==x['raw_sha256'] and q['lf_sha256']==x['lf_sha256'],x['path'];current.append(q)
assert len(current)==22
contexts=[q for q in current if '/frontier-cells/' in q['path'] or '/audits/' in q['path']]
snap=[]
for q in contexts:
 p=R/(pathlib.Path(q['path']).stem+'.math-reviewed.snapshot.json')
 b=pathlib.Path(q['path']).read_bytes()
 assert not p.exists() or p.read_bytes()==b
 if not p.exists():p.write_bytes(b)
 snap.append({'original':q,'snapshot':fr(p)})
pp=['AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/'+s+'.lean' for s in ['WeightedResolvent','ClosedGraphResolvent','GibbsGradientKernel','WeightedGradientDistribution','WeightedGradientWeak','WeightedGradient']]
pp+=['AutoSamplingTheory/TechnicalLemmas/Analysis/WeakGradientZero.lean']
pp+=['AutoSamplingTheory/ExampleCases/ProximalBPS/'+s+'.lean' for s in ['ConditionalScoreClosedDomain','ConditionalGradientKernel','ConditionalGradient','ConditionalScoreDomain','ConditionalScore','ConditionalBochner']]
parents=[fr(p,True) for p in pp]
prior_names=['weighted-c1-gradient-domain','weak-gradient-zero-kernel','global-weighted-resolvent-coercivity','compact-c1-gradient-domain']
oldmaps={n:{x['path']:x for x in rd('runs/20261006-companion-priority/'+n+'/math-review.json')['frozen_inputs']} for n in prior_names}
reuse=[]
for q in parents:
 matches=[n for n,m in oldmaps.items() if q['path'] in m and q['raw_sha256']==m[q['path']]['raw_sha256'] and q['lf_sha256']==m[q['path']].get('lf_sha256',m[q['path']].get('normalized_sha256'))]
 reuse.append({'path':q['path'],'matching_prior_independent_mathematical_receipts':matches,'review':'Exact-byte whole-proof reuse plus invoked-interface reread' if matches else 'Current full WeightedResolvent/ClosedGraphResolvent bodies read independently; no prior receipt assumed'})
api_names=['Analysis/InnerProductSpace/Dual.lean','Analysis/InnerProductSpace/ProdL2.lean','Analysis/Normed/Module/WeakDual.lean','Analysis/Normed/Lp/ProdLp.lean','Analysis/InnerProductSpace/Orthogonal.lean','Analysis/InnerProductSpace/Projection/Submodule.lean','Order/Filter/AtTopBot/CountablyGenerated.lean','MeasureTheory/Measure/SeparableMeasure.lean','MeasureTheory/Function/L2Space.lean','MeasureTheory/Function/LpSpace/Basic.lean','MeasureTheory/Function/LpSeminorm/Basic.lean','MeasureTheory/Measure/Tilted.lean','MeasureTheory/Integral/Bochner/Basic.lean','Topology/Algebra/Module/LinearPMap.lean','LinearAlgebra/LinearPMap.lean']
apis=[fr('.lake/packages/mathlib/Mathlib/'+p) for p in api_names]
mathlib=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD']).decode().strip()
assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert pathlib.Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
stable=[x for x in current if x not in contexts and '/anonymous.' not in x['path']]+parents+apis+[fr('lean-toolchain',True),fr('lake-manifest.json',True)]
prod=[q['path'] for q in current[:4]]
files=prod+pp
hits=[]
for p in files:
 text=astis.strip_lean_comments_and_strings(pathlib.Path(p).read_text(encoding='utf-8'))
 assert not(p.startswith('AutoSamplingTheory/') and re.search(r'^import Tests[.]',text,re.M))
 for i,line in enumerate(text.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append({'path':p,'line':i,'text':line})
assert not hits,hits
private=re.findall(r'^private (?:theorem|def) (\w+)',pathlib.Path(prod[0]).read_text(),re.M)
assert private==['weak_strong_closed_graph','bounded_weak_subsequence','bounded_kernel_orthogonal_sequence_tendsto_zero','scaled_energy_bounds']
reader=[]
for q in current:
 if '/declaration_lessons/' not in q['path']:continue
 unit=rd(q['path'])['units'][0]
 assert chr(92)*2 not in unit['formula'] and all(chr(92)*2 not in x['formula'] for x in unit['steps'])
 reader.append({'path':q['path'],'steps':len(unit['steps']),'statement_assumptions_all_steps_proofs_read':True,'astis_dependencies':unit['astis_dependencies'],'mathlib_dependencies':unit['mathlib_dependencies'],'single_command_backslash_checked':True})
assert [q['steps'] for q in reader]==[7,5,3]
pub.check_advance(claim['declarations'],reviewed=False)
logs=[fr(R/f'independent-direct-{i}.log') for i in range(4)]+[fr(R/'independent-focused.log'),fr(R/'independent-stress-attempt3.log')]
assert 'Build completed successfully (3323 jobs).' in (R/'independent-focused.log').read_text()
for log in logs:
 text=pathlib.Path(log['path']).read_text()
 assert 'error:' not in text and 'sorryAx' not in text
for p in ['independent-direct-3.log','independent-focused.log','independent-stress-attempt3.log']:
 text=(R/p).read_text();assert all(x in text for x in ['propext','Classical.choice','Quot.sound'])
findings={
'whole_generic':'All141 production lines/four private bodies reviewed. The actual graph is a closed submodule of genuine WithLp2 Hilbert product, comapped through actual continuous ofLp; double orthogonal yields (v,0) in original graph from weak H/strong K convergence. Complete H,K hypotheses genuinely used.',
'weak_subsequence':'Riesz isometric dual identification maps bounded residuals into a real weak-dual closed ball. Explicit H separability plus ProperSpace real gives actual sequential Banach-Alaoglu, strict subsequence and every-direction evaluation limit; inverse Riesz supplies H vector, not assumed weak-limit/range certificate. No K separability or finite-dimensional H assumed.',
'full_sequence':'For every cofinal ns, weak subsubsequence plus scaled-gradient strong0 puts the weak limit in EVERY original kernel. Kernel orthogonality and real inner symmetry make forcing pairing0; norm-square inequality and sqrt give strong residual0, then true Filter.tendsto_of_subseq_tendsto gives full sequence. epsilon monotonicity is absent and unused.',
'energy_constants':'From epsilon||u||^2+||Du||^2=<f,u>, derive ||epsilon u||<=||f||, ||epsilon u||^2<=<f,epsilon u>, ||epsilon Du||^2<=epsilon||f||^2 with exact coefficient1, positivity only. No divide by forcing norm; zero forcing/displacement/dimension remain legal.',
'gibbs':'All66 lines reviewed. True tilted probability derives f L1 from actual scalar Lp2, finite-dimensional Borel countable generation and finite measure yield genuine Lp second-countability/separability (Fact2!=top). Actual WeightedResolvent produces each same-original-D closure solution before choosing sequence. Retains actual ordinary scalar/vector localL1 and every legal compactC1 weak-test integrability. Actual kernel AEconstant plus integrable centered forcing proves every-kernel orthogonality, no supplied Poincare certificate.',
'actual_source':'All54 lines reviewed. Genuine common Gaussian augmentation J, conditional R and reflected S, true W_y normalized Gibbs law/C2/integrable exponential/positive partition and SAME original D_y fixed before every centered f/epsilon survive parent calls. Source returns true variational/residual facts; generic Gibbs also retains ordinary weakC1 facts. Fiberwise existential choice only, no joint selector or reflected/unreflected identity.',
'tests':'ENTIRE140-line Test incl private sin perturbation derivatives read/fresh compiled. Actual nonconstant Hessian potential eta1/2, true zero-dimensional W7 original compact-gradient D and centered forcing sequence. Actual closed zero operator with forcing7 gives residual7 and failure of strong zero, showing missing kernel orthogonality is genuinely false.',
'independent_stress':'Actual WithLp2 real2 projection D=(x,y)->y, forcing(0,7)!=0, exact whole-kernel orthogonality and constructed variational u=(0,7/(1+epsilon)); epsilon alternating1/2 divided by n+1 positive,tends0,and epsilon2<epsilon3. Both strong-zero conclusions from new public theorem fresh compiled. Two prior own stdin failures are coordinate-inner-order/Nat parity API errors, retained; production never edited.',
'source_boundary':'Readable source labels this authored Hilbert analytic prerequisite to PBPS background/Poincare, not an explicit source theorem already completed. Reflected quarter curvature/eta constants remain actual parent assumptions; complete PBPS/SPHMC main/composition remain open.'
}
out={'schema_version':1,'advance_id':claim['advance_id'],'reviewer_id':V,'role':'independent_mathematical_reviewer','status':'passed-scoped','verification_status':'passed-scoped','checked_base_head':C,'verified_commit':None,'cell_ids':claim['cells'],'reviewed_declarations':claim['declarations'],'scope':'ENTIRE141/66/54 production + ENTIRE140 Test incl every private helper/body; all7+5+3 reader steps, publications/blueprint/source prerequisite; fresh mathematical review only, no PROVED_LOCAL/VERIFIED/source admission.','frozen_inputs':stable,'frozen_input_count':len(stable),'original22_input_freeze':{'footprint':fr(R/'math-freeze.json'),'inputs':current,'all22_raw_LF_unchanged':True,'anonymous_packet_hashes_only_contents_not_read':True},'separately_scoped_metadata':contexts,'immutable_metadata_snapshots':snap,'unchanged_parent_files':parents,'matching_prior_parent_reuse':reuse,'pinned_mathlib':mathlib,'pinned_toolchain':'leanprover/lean4:v4.33.0','private_helpers_reviewed':private,'production_line_counts':{p:len(pathlib.Path(p).read_text().splitlines()) for p in prod},'findings':findings,'compiler_checks':[{'command':['lake','env','lean',prod[i]],'exit_code':0,'log':logs[i],'LEAN_NUM_THREADS':2} for i in range(4)]+[{'command':['lake','build','Tests.ScaledResolventLimit'],'exit_code':0,'jobs':3323,'log':logs[4],'LEAN_NUM_THREADS':2},{'command':['lake','env','lean','--stdin'],'exit_code':0,'log':logs[5],'source':fr(R/'independent-stress-attempt3.stdin.txt'),'LEAN_NUM_THREADS':2}],'raw_compiler_evidence':logs,'stress_stdin':[fr(R/f'independent-stress-attempt{i}.stdin.txt') for i in [1,2,3]],'retained_stress_diagnostics':[fr(R/f'independent-stress-attempt{i}.log') for i in [1,2]],'failed_stress_is_not_evidence':'Attempts1/2 compile errors/sorryAx are genuine failed own elaborations, never admitted; successful attempt3 has exactly standard3. All raw failures preserved.','stress_linter_warning':'One unnecessarySeqFocus suggestion retained raw in own stdin, no Lean error/no production change.','reader_checks':reader,'fake_closure_scan':{'status':'passed','files':files,'file_count':len(files),'method':'canonical astis comment/string stripping FORBIDDEN_REGEX plus no production Testsimports','matches':hits},'standard_axioms':['propext','Classical.choice','Quot.sound'],'draft_publication_validation':{'reviewed':False,'exact_three_declarations':claim['declarations'],'status':'passed','source_admission_not_claimed':True},'source_boundary':claim['truth_boundary'],'remaining_boundary':['No epsilon0 solution/range/unscaled uniform estimate/Poincare/BL/full operator core/adjoint, joint measurable fiber selector or reflected-unreflected law identification is proved by this packet. Both complete papers/main theorem/history/work/composition remain unfinished; TV never transfers unbounded expected cost.','Independent source-blind/source admission and exact committed VERIFIED remain later stages. Sharedimports/Registry/site/graph/fullgate/currentremoteCI belong original sole root stabilization queue.'],'source_verdicts_or_decoder_results_read':False,'anonymous_packet_contents_or_reconstructions_read':False,'no_verification_transition':True,'mutations':'Only owned run raw logs/immutable stdin/6 metadata snapshots/math-review+own writer. No production/Test/reader/cell/audit/ledger/shared/Goal/branch edits.','all_compiler_sessions_and_writes_closed':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
p=R/'math-review.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'passed-scoped','receipt':str(p),'raw_sha256':sh(p.read_bytes()),'lf_sha256':sh(p.read_bytes().replace(b'\r\n',b'\n')),'stable':len(stable),'snapshots':len(snap),'parents':len(parents),'Mathlib_APIs':len(apis),'focused':3323,'fake_files':len(files),'all_compilers_writes_closed':True}))
