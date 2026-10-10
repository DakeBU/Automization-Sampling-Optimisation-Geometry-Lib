from pathlib import Path
import ctypes, datetime, hashlib, json, os, re, subprocess, sys, traceback

ROOT=Path('E:/Samplinglib')
R73=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
PRE=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73'
OWN=R73/'independent-math73'
PARENT='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
MODSHA='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'
ACTOR='/root/header_math72'
PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
sys.stdout.reconfigure(encoding='utf-8')

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(j): return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def load(p): return json.loads(Path(p).read_bytes())
def save(n,j):
    p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf-8'))
def pin(p):
    p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def check(p,h,n=None,lfh=None):
    b=Path(p).read_bytes();assert sha(b)==h,str(p)
    if n is not None:assert len(b)==n,str(p)
    if lfh is not None:assert sha(b.replace(b'\r\n',b'\n'))==lfh,str(p)
def command(label,args,env=None):
    assert not (OWN/'terminals'/str(label+'.receipt.json')).exists(),'never overwrite a receipt'
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(json.dumps({'START':label,'actual_PID':p.pid,'driver_PID':os.getpid()}),flush=True)
    out,err=p.communicate();d=OWN/'terminals';d.mkdir(parents=True,exist_ok=True)
    (d/(label+'.stdout.RAW')).write_bytes(out);(d/(label+'.stderr.RAW')).write_bytes(err)
    rec={'label':label,'actual_PID':p.pid,'driver_PID':os.getpid(),'command':[str(x) for x in args],
         'terminal_EXIT':p.returncode,'terminal_closed':True,'started_UTC':start,
         'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'stdout':pin(d/(label+'.stdout.RAW')),'stderr':pin(d/(label+'.stderr.RAW'))}
    save('terminals/'+label+'.receipt.json',rec)
    print(json.dumps({'END':label,'actual_PID':p.pid,'terminal_EXIT':p.returncode}),flush=True)
    if p.returncode:raise RuntimeError(label+' failed; all raw negative evidence retained')
    return out,rec

def prepare():
    OWN.mkdir(parents=True,exist_ok=True)
    f=load(R73/'mathematics-freeze73.json');assert len(f['inputs'])==8
    assert f['compiled'][0]['lines']==178 and f['compiled'][0]['declaration']==DECL
    inputs=[]
    for i,item in enumerate(f['inputs']):
        check(item['path'],item['RAW_sha256'],item['RAW_bytes'],item['LF_sha256'])
        dest=OWN/'inputs'/str(str(i).zfill(2)+'.exactRAW.snapshot');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(Path(item['path']).read_bytes())
        inputs.append({'original':item,'snapshot':pin(dest)})
    additional=[R73/'mathematics-freeze73.json',PRE/'header73.proposed.lean',
       ROOT/'docs/theorem-publication-protocol.md',ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md',
       ROOT/'.agents/skills/astis-substantive-advance/SKILL.md']
    for i,p in enumerate(additional,8):
        dest=OWN/'inputs'/str(str(i).zfill(2)+'.exactRAW.snapshot');dest.write_bytes(p.read_bytes())
        inputs.append({'original':pin(p),'snapshot':pin(dest),
          'inspection_scope':'exact header/freeze, or bounded applicable truth-boundary and independent-review protocol sections'})
    check(MODULE,MODSHA,8519,MODSHA)
    head,rec=command('checked-parent',['git','rev-parse','HEAD']);assert head.decode().strip()==PARENT
    manifest=load(ROOT/'lake-manifest.json')
    mathlib=next(p for p in manifest['packages'] if p['name']=='mathlib')
    assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
    assert (ROOT/'lean-toolchain').read_bytes().replace(b'\r\n',b'\n')==b'leanprover/lean4:v4.33.0\n'
    save('inputs.manifest.json',{'input_count':len(inputs),'inputs':inputs,'checked_parent':PARENT,
       'module_is_uncommitted_candidate_at_parent_not_a_verified_SCI_commit':True,
       'RAW_LF_recipe':'replace CRLF byte pairs with LF ONLY; preserve lone CR and all other bytes',
       'recursive_native_review_history_copied':False,'actual_prepare_PID':os.getpid(),'git_receipt':pin(OWN/'terminals/checked-parent.receipt.json')})
    print(json.dumps({'phase':'prepare','status':'PASS','finite_inputs':len(inputs),'module_RAW_sha256':MODSHA}))

def compile():
    for e in load(OWN/'inputs.manifest.json')['inputs']:
        orig=e['original'];check(orig['path'],orig['RAW_sha256'],orig['RAW_bytes'],orig.get('LF_sha256'))
    b,_=command('fixed-lake-selected-env',['lake','env',PY,'-B','-X','utf8','-c',
       "import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"])
    prefix,_=command('fixed-lean-prefix',['lake','env','lean','--print-prefix'])
    exe=Path(prefix.decode().strip())/'bin/lean.exe';env=dict(ENV,**json.loads(b))
    version,_=command('fixed-lean-version',[exe,'--version'],env=env);assert '4.33.0' in version.decode()
    dest=OWN/'output/ActualHarmonicFlow.olean';dest.parent.mkdir(parents=True,exist_ok=True)
    out,rec=command('fresh-whole-module',[exe,'-o',dest,MODULE],env=env)
    text=out.decode('utf-8');lines=[l for l in text.splitlines() if 'depends on axioms:' in l]
    assert len(lines)==1 and DECL in lines[0]
    ax=re.search(r'depends on axioms:\s*\[([^]]*)\]',text,re.S)
    assert ax and {s.strip() for s in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'}
    check(MODULE,MODSHA,8519,MODSHA)
    save('fresh-compiler.json',{'status':'PASS','actual_foreground_Lean_PID':rec['actual_PID'],'terminal_EXIT':0,
       'declaration':DECL,'frozen_module':pin(MODULE),'fresh_source_elaboration':True,'Lake_build_cache_replay':False,
       'original_fixed_Lake_search_roots':True,'LEAN_PATH':env['LEAN_PATH'],'LEAN_SRC_PATH':env['LEAN_SRC_PATH'],
       'real_Lean_executable':pin(exe),'version_output':pin(OWN/'terminals/fixed-lean-version.stdout.RAW'),
       'output_olean':pin(dest),'standard_axioms':['propext','Classical.choice','Quot.sound'],
       'compiler_receipt':pin(OWN/'terminals/fresh-whole-module.receipt.json'),'canonical_olean_written':False})
    print(json.dumps({'phase':'compile','status':'PASS','actual_foreground_Lean_PID':rec['actual_PID'],'terminal_EXIT':0}))

def audit():
    import astis
    raw=MODULE.read_bytes();check(MODULE,MODSHA,8519,MODSHA)
    text=raw.decode('utf-8');assert len(text.splitlines())==178
    header=(PRE/'header73.proposed.lean').read_bytes().decode('utf-8')
    proof_start=text.index(' := by')+len(' := by')
    fixed_imports=['import Mathlib.Tactic.Module','import Mathlib.Tactic.FieldSimp',
       'import Mathlib.Tactic.FunProp','import Mathlib.Tactic.LinearCombination']
    assert text.splitlines()[:4]==fixed_imports
    restored='\n'.join(text[:proof_start].splitlines()[4:])+'\n'
    assert restored==header
    private=text[text.index('private def actual_harmonic_flow_statement'):text.index('\ntheorem actual_harmonic_flow_laws')]
    public=text[text.index('theorem actual_harmonic_flow_laws'):proof_start]
    expected=['hα','hαβ','hV','hH','hη','hβη']
    caller_regex=r'\((h(?:αβ|α|V|H|βη|η))\s*:'
    assert re.findall(caller_regex,private)==re.findall(caller_regex,public)==expected
    private_body=private.split(': Prop :=',1)[1].strip()
    expanded=(R73/'expanded73.frozen.header.lean').read_text(encoding='utf-8')
    assert expanded[expanded.index('    let c :'):].strip()==private_body
    cleaned=astis.strip_lean_comments_and_strings(text)
    hits=[{'line':i,'text':l} for i,l in enumerate(cleaned.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)]
    assert not hits,hits
    assert len(re.findall(r'^theorem ',cleaned,re.M))==1 and len(re.findall(r'^private def ',cleaned,re.M))==1
    ranges=[(1,19,'imports/documentation/namespace'),(20,28,'six caller/private binder prefix'),(29,35,'literal c/Phi/H'),
      (36,56,'nine private conjuncts'),(57,57,'separator'),(58,67,'public wrapper type'),(68,68,'separator'),
      (69,75,'same proof-local literal definitions'),(76,97,'literal change target'),(98,100,'sqrt positivity/nonzero/square'),
      (101,103,'C2 to continuous gradient via compiled parent API'),(104,106,'joint center continuity'),
      (107,110,'joint full-flow continuity'),(111,115,'time-zero'),(116,121,'group law'),(122,127,'both inverse laws'),
      (128,145,'both exact ODE derivatives'),(146,148,'nonnegative SUM energy'),(149,165,'weighted SUM conservation'),
      (166,172,'pi endpoint'),(173,173,'nine-clause result assembly'),(174,178,'closures and exact axiom command')]
    assert [n for a,b,_ in ranges for n in range(a,b+1)]==list(range(1,179))
    clauses=[
      {'id':1,'name':'joint continuity','statement_lines':[36,37],'proof_lines':[101,110]},
      {'id':2,'name':'joint Borel measurability','statement_lines':[38,39],'proof_lines':[173,173]},
      {'id':3,'name':'time zero','statement_lines':[40,40],'proof_lines':[111,115]},
      {'id':4,'name':'group for fixed y/xRef','statement_lines':[41,42],'proof_lines':[116,121]},
      {'id':5,'name':'both inverse compositions','statement_lines':[43,45],'proof_lines':[122,127]},
      {'id':6,'name':'both ODE signs and eta factors','statement_lines':[46,51],'proof_lines':[128,145]},
      {'id':7,'name':'nonnegative SUM-weighted energy','statement_lines':[52,52],'proof_lines':[146,148]},
      {'id':8,'name':'exact SUM-weighted energy conservation','statement_lines':[53,54],'proof_lines':[149,165]},
      {'id':9,'name':'exact pi endpoint','statement_lines':[55,56],'proof_lines':[166,172]}]
    save('statement-proof-audit.json',{'status':'PASS','module_lines':178,'clauses':clauses,
      'exhaustive_partition':[{'start':a,'end':b,'role':r} for a,b,r in ranges],
      'sealed_header_restored_by_removing_only_four_proof_imports':True,'expanded_literal_body_exact_equal':True,
      'private_public_six_callers':expected,'extra_public_analytic_premises':[],
      'fake_closure_hits':hits,'public_theorems':1,'private_literal_definitions':1,'axiom_command_instances':1,
      'parent_gradient_API':'continuous_gradient_of_contDiff_one : ContDiff real 1 f -> Continuous gradient f',
      'hidden_regularities_audit':{'C1_gradient_continuity':'derived internally from original C2 hV',
        'complete_space':'from FiniteDimensional real E, no new caller',
        'Borel_product_measurability':'finite-dimensional real Borel E and finite products; continuous implies measurable',
        'sqrt_eta_nonzero':'derived internally from original hη',
        'integrability_or_decay':'not required for these deterministic finite-vector equalities',
        'no_extra_higher_derivative_bound':True},
      'rank0_alphaeta1_zero_energy_allowed':True,'new_Lean_implementation_by_reviewer':False})
    print(json.dumps({'phase':'audit','status':'PASS','clauses':9,'line_coverage':178,'fake_closures':0}))

REVIEW='''# Independent mathematics review73

Reviewer: /root/header_math72. Checked parent: bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19. The reviewed candidate is the entire 178-line ActualHarmonicFlow.lean module, exact RAW/LF SHA256 506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c, not a committed SCI73 theorem. Root remains the sole canonical proving writer.

Verdict: ACCEPTED_MATHEMATICS_ONLY, conditional on the recorded fresh whole-module Lean terminal EXIT0. No mathematical statement or proof repair is required. All nine literal clauses and the full proof were reviewed. The current six original callers are retained; no caller is asked to provide one of the conclusions or a new analytic regularity fact. This is not source-fidelity admission, strict blind decoding, VERIFIED, publication acceptance or whole-paper completion.

## Exact mathematical reduction

Fix η>0, r=√η, y,xRef∈E, g=gradient V(xRef), c=y−ηg. For initial state z=(q₀,p₀), put w₀=(q₀−c)/r. The literal module defines

w(t)=cos(t) w₀+sin(t) p₀,
p(t)=−sin(t) w₀+cos(t) p₀,
q(t)=c+r w(t).

This is precisely the module's Φ, since η=r² and r>0. E is a finite-dimensional real inner product space; no nontriviality or positive dimension is assumed. y,xRef and η are fixed when forming the time group or differentiating time. Joint continuity/measurability additionally quantifies both y and xRef, the real time t and the entire initial pair z. The theorem does not assert continuity in η or a flow in which xRef changes with time.

## All nine clauses and their proofs

1. Joint continuity (statement36–37, proof101–110). Original hV:C² implies C¹. The imported ASTIS continuous_gradient_of_contDiff_one proves continuity of the actual Mathlib gradient, via the continuous inverse Riesz map applied to continuous fderiv. Thus c(y,xRef) is jointly continuous. Scalar sine/cosine, projections, vector addition and scalar multiplication give joint continuity of Φ on (E×E)×(ℝ×(E×E)). Division is only by the fixed positive r; no moving-parameter singularity is hidden. Proof fun_prop combines these actual continuous expressions rather than accepting a caller continuity certificate.

2. Joint Borel measurability (statement38–39, assembly173). The given MeasurableSpace E/BorelSpace E on finite-dimensional real E and their finite products are compatible with the topology; the proven joint continuous map is measurable. This includes y,xRef,t,z simultaneously, not only each fixed-parameter trajectory. No kernel, conditional law, measure preservation or stochastic process is claimed.

3. Time zero (statement40, proof111–115). cos0=1 and sin0=0 give q(0)=c+(q₀−c)=q₀ and p(0)=p₀. The vector module calculation is direct; it does not assume a flow axiom.

4. Group (statement41–42, proof116–121). In normalized coordinates M(t)=[[cos t,sin t],[-sin t,cos t]]. Trigonometric addition gives M(s)M(t)=M(s+t). The same c is reused in both compositions, so translating back proves the exact stated order Φ(s+t,z)=Φ(s,Φ(t,z)). The Lean proof expands both coordinates, uses sin/cos addition, and clears the nonzero constant r. There is no hidden change of y or xRef, nor an omitted root relation or extra semigroup premise.

5. Both inverses (statement43–45, proof122–127). Substitute (s,t)=(−t,t) and (t,−t) in the proved group law, then time zero. The proof supplies both left and right compositions, even for negative or zero times. It does not infer a global measure-preserving inverse.

6. Both actual ODEs (statement46–51, proof128–145). Differentiating the explicit normalized expressions gives w′=p and p′=−w, hence q′=r p and p′=−(q−c)/r. Since c=y−ηg and η=r²,

−r⁻¹(q−y)−r g=−r⁻¹(q−c)+(η/r−r)g=−r⁻¹(q−c).

This checks both negative signs and both √η factors exactly. In particular the gradient is evaluated at the frozen xRef, not at the moving q(t). The Lean proof uses actual HasDerivAt sine/cosine rules and congr_deriv to identify the computed derivatives, then hr0 and hr2. It neither assumes the desired ODE nor replaces derivatives by pointwise formal differentiation. No global Lipschitz theorem or additional derivative bound is needed for this explicit fixed-center solution.

7. Nonnegative energy (statement52, proof146–148). The literal H=(η⁻¹‖q−c‖²+‖p‖²)/2 is a SUM, with η⁻¹>0. Both squared norms are nonnegative and the denominator is positive. The result is nonnegativity, so zero energy is included.

8. Conserved weighted SUM energy (statement53–54, proof149–165). H=(‖w‖²+‖p‖²)/2. Expanding the two normalized squared norms gives

‖cos t·w₀+sin t·p₀‖²
  =cos²t‖w₀‖²+2 cos t sin t⟨w₀,p₀⟩+sin²t‖p₀‖²,
‖−sin t·w₀+cos t·p₀‖²
  =sin²t‖w₀‖²−2 sin t cos t⟨w₀,p₀⟩+cos²t‖p₀‖².

Cross terms cancel and sin²t+cos²t=1. The proof performs this exact inner-product norm expansion, rewrites η=r² and clears only nonzero r before using the trigonometric identity. It does not replace H by a difference of squares, an unweighted product norm or an assumed invariant. The positivity/normalization survives arbitrary dimension and all real times.

9. π endpoint (statement55–56, proof166–172). cosπ=−1 and sinπ=0 yield q(π)=c−(q₀−c)=2c−q₀ and p(π)=−p₀. Both components and the actual center are present. The proof reduces these exact trigonometric values and vector identities. This is a deterministic coordinate endpoint, not an admitted conditional half-turn operator or probability kernel.

The proof-local c/Φ/H and the change target reproduce the literal private Prop. The final tuple173 contains precisely all nine proven clauses. The 178-line exhaustive, nonoverlapping audit partition also covers imports, caller/type prefixes, local definitions, square-root facts, gradient/center continuity, namespace closures and the unique exact #print axioms command; there are no unreviewed mathematical lines.

## Binders, boundaries and edge cases

The private and public callers are exactly hα,hαβ,hV,hH,hη,hβη. Their content is α>0, α≤β, V∈C², the original Hessian lower/upper bound, η>0 and βη≤1. The proof uses hV for gradient continuity and hη for r>0 and η=r². The other original standing conditions remain explicit, even though the deterministic harmonic algebra does not need their quantitative force. It would be inappropriate to turn the derived continuity, time group, ODE, energy or endpoint into new caller assumptions.

Finite dimensionality supplies completeness for the gradient API and the usual finite-product Borel compatibility; no new CompleteSpace, second-countability, differentiability, measurability or nonzero-energy premise is passed to the caller. No third/higher derivative, boundary decay, integrability or domination assumption is needed for these deterministic pointwise formulas. The reviewed imported gradient API was pinned and read at its exact type/proof; the pinned Mathlib revision remains db584cd6d46c92f209a44c0f1c829460d327499d, with Lean4.33.0.

Rank zero is valid: all vectors are zero, so every coordinate, derivative, energy and endpoint identity reduces correctly; the alpha/Hessian conditions cause no contradiction since all v are zero. At αη=1, η remains strictly positive, and no formula divides by 1−αη or 1−βη. All nine clauses remain valid, including βη=1. Zero energy is valid: η>0 implies H=0 iff q₀=c and p₀=0; then Φ(t,z)=z and both ODE right sides are zero for every t. The proof never divides by H, a norm or a velocity. η=0 is outside the original caller, correctly.

The exact sealed header is restored by removing only the four proof tactic imports from the compiled module's prefix. The expanded frozen header's entire let-bound literal body matches the private Prop. The deterministic module imports no corrector72 result. No stronger statement about invariant measures, bounce/rates, stochastic construction, nonexplosion, Markov/reversal, actual conditional H/kernel, rρ/B27/B28, main/error/cap/query-cost or actual-input composition follows from this review. Reader/source admission, Exposition Seal, PURIFIED, live/main, full-paper and Goal completion remain separate and open. Because this reviewer has seen the named statement, implementation and header adoptions, it cannot act as strict blind decoder73.

## Evidence and independence

Finite original inputs are preserved as exact RAW snapshots with both RAW and bytewise CRLF→LF-only pins. No recursive history or large encoded source packet was copied. Fresh source elaboration runs the real pinned lean.exe on the exact whole canonical candidate, writes an olean only under independent-math73/output, and uses the original fixed Lake search roots. Its actual foreground PID, terminal EXIT and exact axiom output are recorded separately. The native fake-closure scanner strips Lean comments/strings and checks the entire module; mathematical review separately checks the literal definition and full proof.

There are no canonical, global-ledger, Git, Goal, source/publication/site writes and no VERIFIED transition. Bounded applicable independent-review/round-trip truth-boundary protocols were read; this task does not perform or impersonate their later blind/source review stages. Root's earlier compile/header receipts are input provenance, never substituted for this independent fresh check. All actual failures, if any, remain in the owned raw receipts and failure records. Wholelogical run hash removes ONLY the top-level run_sha256 and canonicalizes the entire remaining JSON with UTF8, sorted keys, ensure_ascii=False and comma/colon separators. Final lease is CLOSED_LAST; external verification afterwards is read-only.
'''

def close():
    check(MODULE,MODSHA,8519,MODSHA)
    compiler=load(OWN/'fresh-compiler.json');audit_result=load(OWN/'statement-proof-audit.json')
    assert compiler['terminal_EXIT']==0 and audit_result['status']=='PASS'
    receipts=[load(p) for p in sorted((OWN/'terminals').glob('*.receipt.json'))]
    assert all(r['terminal_closed'] and r['terminal_EXIT']==0 for r in receipts)
    failures=[load(p) for p in sorted(OWN.glob('failure.*.json'))]
    decision={'verdict':'ACCEPTED_MATHEMATICS_ONLY','reviewer':ACTOR,'checked_parent':PARENT,'candidate_module':pin(MODULE),
       'declaration':DECL,'nine_clauses_mathematically_correct':True,'minimum_mathematical_repair':None,
       'fresh_foreground_Lean_PID':compiler['actual_foreground_Lean_PID'],'fresh_Lean_terminal_EXIT':0,
       'standard_axioms_only':True,'fake_closures':0,'new_public_regularities':[],
       'rank_zero_allowed':True,'alphaeta_one_allowed':True,'zero_energy_allowed':True,
       'compiled_independently':True,'source_fidelity_admitted':False,'strict_blind_decoder':False,
       'VERIFIED':False,'whole_paper_complete':False,'Goal_complete':False,'canonical_writes':False}
    (OWN/'independent-mathematics73.utf8.md').write_bytes(REVIEW.encode('utf-8'))
    save('decision.json',decision)
    payload={'reviewer':ACTOR,'checked_parent':PARENT,'complete_named_review':REVIEW,'decision':decision,
       'input_manifest':load(OWN/'inputs.manifest.json'),'full_exact_module_UTF8':MODULE.read_text(encoding='utf-8'),
       'literal_and_proof_audit':audit_result,'fresh_compiler':compiler,'foreground_terminal_receipts':receipts,
       'negative_evidence':failures,'no_other_thread_messages':True,'post_task_blind_decoder73_ineligible':True}
    save('complete-named-review-decision-input-payload.json',payload)
    run={'schema':1,'reviewer':ACTOR,'status':'ACCEPTED_MATHEMATICS_ONLY','checked_parent':PARENT,
       'declaration':DECL,'candidate_module':pin(MODULE),'input_manifest':load(OWN/'inputs.manifest.json'),
       'decision':decision,'fresh_compiler':compiler,'literal_and_proof_audit':audit_result,'terminal_receipts':receipts,
       'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'negative_evidence':failures,
       'actual_last_writer_PID':os.getpid(),'canonical_Git_ledger_Goal_writes':False,'source_review':False,'VERIFIED':False,
       'wholelogical_recipe':'delete ONLY top-level run_sha256; entire logical JSON sorted UTF8 ensure_ascii=False separators comma colon allow_nan=False'}
    run['run_sha256']=sha(canon(run));save('run.json',run)
    entries=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['native.manifest.json','lease.final.json']]
    save('native.manifest.json',{'entries':entries,'entry_count':len(entries),'logical_entries_sha256':sha(canon(entries)),
       'excludes_only_manifest_self_and_final_lease':True})
    save('lease.final.json',{'status':'CLOSED_LAST','reviewer':ACTOR,'actual_last_writer_PID':os.getpid(),
       'run_sha256':run['run_sha256'],'manifest':pin(OWN/'native.manifest.json'),'owned_files':len(entries)+2,
       'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'decision':pin(OWN/'decision.json'),
       'last_write_contract':'THIS lease.final.json is the final owned write. No writes after CLOSED_LAST; external verifier read-only.',
       'writer_terminal_EXIT_contract':'return EXIT0 immediately; actual terminal code is reported separately',
       'VERIFIED':False,'source_fidelity_admission':False})
    print(json.dumps({'phase':'close','status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),
       'run_sha256':run['run_sha256'],'owned_files':len(entries)+2}))

def readonly():
    l=load(OWN/'lease.final.json');m=load(OWN/'native.manifest.json')
    check(OWN/'native.manifest.json',l['manifest']['RAW_sha256'],l['manifest']['RAW_bytes'])
    assert sha(canon(m['entries']))==m['logical_entries_sha256']
    for e in m['entries']:check(e['path'],e['RAW_sha256'],e['RAW_bytes'],e['LF_sha256'])
    files=[p for p in OWN.rglob('*') if p.is_file()]
    assert len(files)==l['owned_files']
    assert {p.as_posix() for p in files}=={e['path'] for e in m['entries']}|{(OWN/'native.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}
    r=load(OWN/'run.json');h=r.pop('run_sha256');assert sha(canon(r))==h==l['run_sha256']
    assert all(p.stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns for p in files)
    k=ctypes.WinDLL('kernel32',use_last_error=True);k.OpenProcess.argtypes=[ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32];k.OpenProcess.restype=ctypes.c_void_p
    assert not k.OpenProcess(0x1000,False,l['actual_last_writer_PID']),'writer still exists'
    check(MODULE,MODSHA,8519,MODSHA)
    for e in r['input_manifest']['inputs']:
        orig=e['original'];check(orig['path'],orig['RAW_sha256'],orig['RAW_bytes'],orig.get('LF_sha256'))
    print(json.dumps({'status':'PASS','external_readonly_PID':os.getpid(),'writer_PID':l['actual_last_writer_PID'],
       'writer_terminated':True,'owned_files':len(files),'run_sha256':h,'wholelogical_remove_ONLY_top_run_sha256':True,
       'canonical_input_bytes_unchanged':True,'terminal_EXIT_contract':0}))

if __name__=='__main__':
    phase=sys.argv[1];assert phase in ['prepare','compile','audit','close','readonly']
    if phase!='readonly':assert not (OWN/'lease.final.json').exists(),'CLOSED: no more writes'
    print(json.dumps({'phase':phase,'actual_driver_PID':os.getpid()}),flush=True)
    try:globals()[phase]()
    except BaseException:
        if phase!='readonly' and not (OWN/'lease.final.json').exists():
            save('failure.'+phase+'.'+str(os.getpid())+'.json',{'phase':phase,'actual_PID':os.getpid(),'traceback':traceback.format_exc(),
               'canonical_writes':False,'terminal_exit_contract':1})
        raise
