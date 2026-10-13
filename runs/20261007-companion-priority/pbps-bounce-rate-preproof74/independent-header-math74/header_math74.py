"""Prospective-header mathematical review only. No Lean or canonical writes."""
from __future__ import annotations
import ctypes, hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
PRE=OWN.parent
PLAN=ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preread74'
HEADER=PRE/'header74.proposed.lean'
TYPECHECK=PRE/'header74.typecheck.lean'
FIXED=PRE/'header74.typecheck-closed-sections.lean'
R73=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
EXPECTED='d72435795cd225af382948e8da683b6eb4b9e5b05509f8e3b0d10a3ed5a5a96e'
PROBE='1dd0d07c3d21fd3e5c0e1989755d15103ad495852defb1ce261484fc7f12c672'
LF='CRLF byte pairs -> LF only; preserve bare CR and every other byte.'
RECIPE='Delete ONLY top-level run_sha256; json.dumps ensure_ascii=False, sort_keys=True, separators=(comma,colon), allow_nan=False; UTF-8 without BOM or final newline; SHA256. Preserve all nested hashes and every other field.'
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def logical(v): return sha(canon({k:x for k,x in v.items() if k!='run_sha256'}))
def pin(p):
    p=Path(p); b=p.read_bytes(); lf=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':LF}
def read(p): return json.loads(Path(p).read_bytes())
def save(n,v):
    assert not (OWN/'lease.final.json').exists()
    p=OWN/n; assert OWN in p.resolve().parents
    p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8'))
def textfile(n,t):
    assert not (OWN/'lease.final.json').exists(); p=OWN/n; assert OWN in p.resolve().parents; p.write_bytes(t.encode('utf-8'))
def guard(pins):
    for p in pins: assert pin(p['path'])==p,('frozen input drift',p['path'])

REVIEW='''# Independent prospective-header mathematical review74

Decision: ACCEPT HEADER MATHEMATICS ONLY, without repair. Exact candidate header74.proposed.lean is3537 RAW/LF bytes, SHA256 d72435795cd225af382948e8da683b6eb4b9e5b05509f8e3b0d10a3ed5a5a96e. The candidate ends in an empty theorem proof introducer. The3065-byte predicate-only probe is a separate exact input SHA1dd0d07c3d21fd3e5c0e1989755d15103ad495852defb1ce261484fc7f12c672. Root's original probe PID52824 EXIT1 omitted the end for an unnamed noncomputable section; its frozen input and failed receipt/stdout are preserved. The3069-byte repaired driver SHA3866b26c9a19e92b442c2861b1887c17d9b9423f334ea27b7ba25f7adcbab5f0 adds exactly one end before the named namespace end, preserving every predicate byte. Its native terminal receipt reports PID53780 EXIT0. I inspect and pin these existing driver receipts; I run no Lean, and predicate typing cannot prove the theorem. This review proves no Lean declaration and performs no proof search or implementation. It is independent of the root candidate writer, and is not source69's independent source admission or a strict blind reconstruction.

I inspected the complete private literal Prop, all local definitions c,h,R,S,rate,H, the full public caller block and all ten top-level conjunction clauses. The private literal is a specification, not an assumed provider. The ambient real inner-product normed space is finite dimensional and carries its Borel measurable structure. Finite dimension internally supplies completeness, separability/second-countability and Borel product compatibility when used; none is a new analytic caller. Exact private/public caller prefixes agree byte for byte with the original73 private prefix and the actual compiled73 module: hα, hαβ, hV, hH (both genuine Hessian inequalities), hη and hβη. There is no supplied Lipschitz, reflection, isometry, energy, clock, process, kernel, nonzero-normal, positive-dimension or stronger-regularity premise. The imports contain QuadraticRegularization, Mathlib reflection and Borel, with no ActualHarmonicFlow73 import or mathematical parent edge.73 only provides a caller/notation comparison here.

Clause1, joint Borel bounce: source normal h(xRef,x)=∇V(x)−∇V(xRef) is jointly continuous. The complete R formula is p−(2⟨p,n⟩/‖n‖²)n with total real division. Real reciprocal extended by0 at0 is Borel; inner product, squared norm, scalar multiplication, subtraction and product coordinates are Borel. Composition gives Borel S over the complete E×(E×E), including h=0. ContinuousInv₀.measurableInv and Measurable.div are the fixed native background. No continuity of R at n=0 is required or claimed. In dimension1, V(x)=x²/2, xRef=0, p=1, α=β=η=1 gives S's momentum−1 when x≠0 and1 at x=0, so a continuous-bounce requirement would be false. The current header correctly avoids it.

Clauses2–3, joint continuous/Borel rate: C2 gives continuous gradient; alternatively the same original assumptions yield actual LipschitzWith β (gradient V) internally. Inner product and max0 are continuous, and √η is a fixed positive real coefficient. Thus rate is jointly continuous and Borel on every parameter/state, including the zero-normal locus. A measurable E identified as its Borel structure and finite-dimensional product compatibility are sufficient.

Clause4, R0=id: for n=0 the numerator and denominator are0, Lean real0/0=0, and the subtracted vector is0. This precisely matches the source zero extension, without a hidden n≠0 assumption.

Clause5, all-normal Householder laws: for n≠0 put a=⟨p,n⟩ and d=‖n‖²>0. Then R_np=p−(2a/d)n and ⟨R_np,n⟩=a−2a=−a. Applying the SAME R_n twice gives p−(2a/d)n−(2(−a)/d)n=p. Squared norm expands as ‖p‖²−4a²/d+4a²/d=‖p‖², hence the norms agree. At n=0, R0=id and both pairing sides vanish. Equivalently R_n is Mathlib reflection in (span{n})-perp, the NEGATIVE of reflection in span{n}; Submodule.reflection_singleton_apply uses ⟨n,p⟩, equal to the header's ⟨p,n⟩ over R. Confusing span reflection with its orthogonal-complement reflection would reverse the map, but the header's sign/orientation is correct. These are output conclusions about a locally defined R, not generic algebra assumptions passed to the caller.

Clause6, actual phase bounce: S fixes position x, so h(xRef,x) is unchanged by a bounce. The all-normal involution therefore gives S(Sz)=z on the entire phase space. No reference point changes during composition.

Clause7, energy preservation: y and xRef and therefore c stay fixed; S changes only momentum, preserving its individual norm. Both terms η⁻¹‖x−c‖² and ‖p‖² are individually unchanged, so the exact weighted SUM divided by2 is unchanged. No product-space max-norm identity is used.

Clause8, nonnegative/flipped rate: √η>0 and max0≥0 give nonnegativity. With a=⟨p,h⟩, clause5 yields rate(Sz)=√η max(0,−a). The real identity max(0,a)−max(0,−a)=a gives rate(z)−rate(Sz)=√η a. The minus sign, coefficient and order of the rate difference in the header are correct, with no restriction on the sign of a.

Clause9, actual zero normal: h(xRef,x)=0 makes R0p=p and the inner product0, hence S(x,p)=(x,p) and rate0. This covers every p, rather than only zero momentum.

Clause10, energy nonnegativity/radii/exact majorant: η>0 gives η⁻¹>0 and both squared norms are nonnegative, so H(z0)≥0. Write e=H(z0), q=x−c and suppose the conclusion antecedent H(z)=H(z0). Then η⁻¹‖q‖²+‖p‖²=2e, giving ‖p‖²≤2e and ‖q‖²≤2ηe. Nonnegative norms and the nonnegative square root give exactly ‖p‖≤√(2e) and ‖q‖≤√(2ηe), including e=0. The existing ASTIS QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic with U=V,m=α,L=β,r=0,u=0 supplies LipschitzWith β (gradient V) internally from hV and hH. Its quadratic term is literally zero; no extra Lipschitz caller is permitted. Thus ‖h(xRef,x)‖≤β‖x−xRef‖. Cauchy–Schwarz and triangle inequality give

rate(z) ≤ √η‖p‖‖h‖ ≤ √η β‖p‖‖x−xRef‖
        ≤ √η β√(2e)(√(2ηe)+‖c−xRef‖).

Every multiplier used for an inequality is nonnegative. The header has exactly this scalar product: √η times β times √(2H(z0)) times the parenthesized sum, with no missing half, factor2, η power or dimension factor. Equality of H values is a universally quantified conclusion antecedent selecting one source energy layer, not a new standing caller. No independent energy bound, e>0 or positive rate premise is assumed.

Boundary cases: rank0 makes E and E×E singleton, all gradients/norms/energies/rates0 and all identities valid. αη=1 remains legal; no inverse1−αη or strict step cap appears. For e=0, positivity of the energy weights gives p=0 and x=c, so S fixes the state and rate=0 even when h(c)≠0; the majorant is0 without any division. For h=0 with nonzero p, clause9 still holds. Later clock proofs must branch on a zero majorant before waiting-time division; this header does not define any clock or assert no jumps for an unconstructed process. Conditions hα,hαβ,hβη are retained source-standing inputs; some algebraic clauses do not use them, and that redundancy is not false or a permission to drop them.

No missing mathematical condition or false premise was found. No mathematical repair is recommended. The sourceplan is a plan and is not an actual73 formal parent. Generic R laws are internal outputs reusing native geometry, not duplicate public wrapper lemmas. Root remains the sole canonical writer. Source correspondence/coverage, future blind reconstruction, successful Lean proof, independent exact-science admission, stochastic construction/nonexplosion/stationarity, terminal H_y, actual K/r_rho/B27/B28, full papers, errors/caps/costs/composition, Exposition/PURIFIED and Goal completion remain separate/open. The native finite input/output pins and CLOSED_LAST certify only this prospective mathematical review artifact.
'''

def prefix(s,start,stop):
    i=s.index('    {E : Type*}',start); j=s.index(stop,i); return s[i:j]
def inspect():
    assert not (OWN/'decision.json').exists()
    hb=HEADER.read_bytes(); tb=TYPECHECK.read_bytes()
    assert len(hb)==3537 and sha(hb)==EXPECTED and hb.replace(b'\r\n',b'\n')==hb
    assert len(tb)==3065 and sha(tb)==PROBE and tb.replace(b'\r\n',b'\n')==tb
    s=hb.decode('utf-8'); t=tb.decode('utf-8'); public=s.index('\ntheorem actual_bounce_rate_energy_laws')
    assert s[s.rindex(':= by')+5:].strip()==''
    assert t.startswith(s[:public]) and 'theorem actual_bounce_rate_energy_laws' not in t and '#check actual_bounce_rate_energy_statement' in t
    fixed=FIXED.read_bytes(); assert len(fixed)==3069 and sha(fixed)=='3866b26c9a19e92b442c2861b1887c17d9b9423f334ea27b7ba25f7adcbab5f0'
    end=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate'
    assert tb.count(end)==1 and tb.replace(end,b'end\n'+end)==fixed
    failed_dir=R73/'typecheck-prospective-header74'; fixed_dir=R73/'typecheck-prospective-header74-section-close-repair'
    failed_receipt=read(failed_dir/'receipt.json'); fixed_receipt=read(fixed_dir/'receipt.json')
    assert failed_receipt['actual_foreground_PID']==52824 and failed_receipt['exit_code']==1 and failed_receipt['terminal_closed']
    assert fixed_receipt['actual_foreground_PID']==53780 and fixed_receipt['exit_code']==0 and fixed_receipt['terminal_closed']
    for directory,receipt in [(failed_dir,failed_receipt),(fixed_dir,fixed_receipt)]:
        for key in ['stdout','stderr']:
            p=directory/(key+'.log')
            for k in ['RAW_bytes','RAW_sha256','LF_sha256']: assert pin(p)[k]==receipt[key][k]
    private=prefix(s,s.index('private def'),' : Prop :=')
    caller_public=prefix(s,public,' :\n    actual_bounce_rate_energy_statement')
    original=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean'
    actual73=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
    old=original.read_text(encoding='utf-8'); actual=actual73.read_text(encoding='utf-8')
    assert private==caller_public==prefix(old,old.index('private def'),' : Prop :=')==prefix(actual,actual.index('private def'),' : Prop :=')
    imports=[x for x in s.splitlines() if x.startswith('import ')]
    assert len(imports)==3 and not any('ActualHarmonicFlow' in x for x in imports)
    body=s[s.index('    Measurable (fun a :'):public].strip(); depth=0; begin=0; clauses=[]
    for i,c in enumerate(body):
        if c=='(': depth+=1
        elif c==')': depth-=1
        elif c=='∧' and depth==0: clauses.append(body[begin:i].strip()); begin=i+1
        assert depth>=0
    clauses.append(body[begin:].strip()); assert depth==0 and len(clauses)==10
    seal=read(PRE/'root.statement-seal74.json'); adoption=read(PRE/'root.preread74.adoption.json'); lease=read(PLAN/'lease.final.json')
    assert seal['status']=='SEALED_BEFORE_PROOF_SEARCH_PENDING_INDEPENDENT_HEADER_REVIEWS'
    for k in ['RAW_bytes','RAW_sha256','LF_sha256']: assert seal['header'][k]==pin(HEADER)[k] and seal['typecheck_predicate_only'][k]==pin(TYPECHECK)[k]
    assert adoption['status']=='ACCEPTED_SOURCE_FIRST_PLAN_ONLY_NOT_PROOF' and lease['status']=='CLOSED_LAST'
    assert adoption['native_whole_logical_run_sha256']==lease['run_sha256']=='8af15894b1054212a347336eb08b5848469afaa1ceb737dc20632ae26fc795ed'
    assert adoption['native_lease']['RAW_sha256']==pin(PLAN/'lease.final.json')['RAW_sha256']
    paths=[HEADER,TYPECHECK,PRE/'root.statement-seal74.json',PRE/'root.preread74.adoption.json',PLAN/'capsule74.json',PLAN/'plan74.json',PLAN/'lease.final.json',PLAN/'minimal.actual-API-audit74.json',original,actual73,ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Reflection.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Arithmetic.lean',ROOT/'docs/proof-digestion-protocol.md',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
    paths += [FIXED,PRE/'typecheck-driver-diagnosis74.json']+[directory/name for directory in [failed_dir,fixed_dir] for name in ['receipt.json','stdout.log','stderr.log']]
    pins=[pin(p) for p in paths]; guard(pins)
    labels=['Joint Borel S','Joint continuous rate','Joint Borel rate','R0=id','All-normal involution/norm/flipped pairing','Actual position and S involution','Weighted SUM energy preservation','Rate nonnegative/flip/difference','Actual zero-normal S/rate','Nonnegative H, same-layer coordinate radii and exact uniform rate majorant']
    clause_audit=[{'index':i+1,'label':label,'exact_literal':literal,'mathematically_correct':True,'missing_condition':None} for i,(label,literal) in enumerate(zip(labels,clauses))]
    decision={'schema':'astis-independent-prospective-header-math74/v1','verdict':'ACCEPT_HEADER_MATHEMATICS_ONLY','reviewer':'/root/header_math72','candidate_header':pin(HEADER),'predicate_only_probe':pin(TYPECHECK),'candidate_compiled_or_proved_by_this_review':False,'root_probe_compilation_observed':False,'actual_reader_PID':os.getpid(),'checked_parent':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'complete_literal_reviewed':True,'ten_clauses':clause_audit,'same_original_six_callers_byte_equal':True,'private_public_original73_actual73_caller_prefix':private,'missing_conditions':[],'false_premises':[],'minimal_mathematical_repair':None,'rank0_allowed':True,'alphaeta1_allowed':True,'zero_energy_allowed':True,'total_zero_normal_extension_correct':True,'Householder_orientation_correct':True,'exact_energy_majorant_factors_correct':True,'no_actual73_formal_parent':True,'extra_public_regularities':[],'source69_decision_consumed':False,'strict_blind_decoder':False,'proof_search_or_implementation':False,'canonical_Git_ledger_Goal_writes':False,'source_admission':False,'VERIFIED':False,'inputs':pins,'failures':[]}
    decision['root_probe_compilation_observed']=True
    decision['root_predicate_driver_only']={'input':pin(FIXED),'actual_foreground_PID':53780,'terminal_EXIT':0,'exact_one_scope_end_inserted':True,'full_predicate_bytes_unchanged':True,'no_theorem_proof':True,'receipt':pin(fixed_dir/'receipt.json')}
    decision['failures']=[{'kind':'ROOT_TYPECHECK_DRIVER_SECTION_CLOSE_ERROR_NOT_MATHEMATICS','actual_foreground_PID':52824,'terminal_EXIT':1,'receipt':pin(failed_dir/'receipt.json'),'stdout':pin(failed_dir/'stdout.log'),'original_frozen_input':pin(TYPECHECK),'resolution':'Only one end inserted in separate driver; frozen header and predicate unchanged.'}]
    save('decision.json',decision)
    save('finite.inputs.json',{'inputs':pins,'LF_recipe':LF})
    save('full.header-and-predicate-inputs.json',{'candidate_complete_exact_RAW_UTF8':s,'predicate_only_complete_exact_RAW_UTF8':t,'scope_closed_driver_complete_exact_RAW_UTF8':fixed.decode('utf-8'),'caller_prefix':private,'ten_exact_top_level_clauses':clauses})
    textfile('named.prospective-header-mathematical-review74.utf8.md',REVIEW)
    print(json.dumps({'actual_reader_PID':os.getpid(),'verdict':decision['verdict'],'clauses':len(clauses),'finite_inputs':len(pins),'proof_search_implementation_compiler':False,'EXIT':0},ensure_ascii=False))

def launch():
    assert not (OWN/'reader.terminal.json').exists()
    command=[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'inspect']
    with (OWN/'reader.stdout.txt').open('wb') as out,(OWN/'reader.stderr.txt').open('wb') as err:
        p=subprocess.Popen(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=out,stderr=err); code=p.wait()
    save('reader.terminal.json',{'actual_foreground_PID':p.pid,'terminal_EXIT':code,'command':command,'observer_PID':os.getpid(),'stdout':pin(OWN/'reader.stdout.txt'),'stderr':pin(OWN/'reader.stderr.txt')})
    print(json.dumps(read(OWN/'reader.terminal.json'),ensure_ascii=False)); return code
def close():
    d=read(OWN/'decision.json'); terminal=read(OWN/'reader.terminal.json'); assert terminal['terminal_EXIT']==0 and terminal['actual_foreground_PID']==d['actual_reader_PID']; assert (OWN/'reader.stderr.txt').read_bytes()==b''; guard(d['inputs'])
    complete={'schema':'astis-complete-named-prospective-header-math74/v1','named_review':REVIEW,'complete_named_decision_and_input_payload':d,'full_exact_candidate_inputs':read(OWN/'full.header-and-predicate-inputs.json'),'terminal_receipt':terminal,'actual_closure_writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE}
    save('complete-named-review-decision-input-payload.json',complete)
    run={'schema':'astis-prospective-header-math74-run/v1','candidate':pin(HEADER),'reviewer':d['reviewer'],'inputs':d['inputs'],'decision':pin(OWN/'decision.json'),'named_review':pin(OWN/'named.prospective-header-mathematical-review74.utf8.md'),'complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload.json'),'actual_reader_terminal':terminal,'actual_final_writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE,'failures':d['failures'],'proof_search_implementation_Lean_run':False,'source_or_formal_truth_admission':False,'VERIFIED':False}
    run['run_sha256']=logical(run); save('run.json',run)
    owned=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['native.manifest.json','lease.final.json']]
    save('native.manifest.json',{'owned_root':OWN.as_posix(),'owned_files':owned,'LF_recipe':LF,'run_sha256':run['run_sha256'],'wholelogicalrun_recipe':RECIPE,'exclusions':['native.manifest.json self-reference','lease.final.json final write']})
    lease={'status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),'owned_files':len(owned)+2,'run_sha256':run['run_sha256'],'manifest':pin(OWN/'native.manifest.json'),'decision':pin(OWN/'decision.json'),'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'candidate':pin(HEADER),'last_write_contract':'THIS lease.final.json is the final owned write. No writes after CLOSED; external validation read-only.','writer_terminal_EXIT_contract':'Exit0 immediately; external tool observes actual terminal EXIT','scope':'Prospective-header mathematics only. No compiled proof/source/Exposition/PURIFIED/VERIFIED/Goal credit.'}
    save('lease.final.json',lease)
    print(json.dumps({'actual_writer_PID':os.getpid(),'owned_files':lease['owned_files'],'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json'),'EXIT':0},ensure_ascii=False))
def readonly():
    lease=read(OWN/'lease.final.json'); assert lease['status']=='CLOSED_LAST'
    for name,key in [('native.manifest.json','manifest'),('decision.json','decision'),('complete-named-review-decision-input-payload.json','complete_named')]: assert pin(OWN/name)==lease[key]
    manifest=read(OWN/'native.manifest.json'); guard(manifest['owned_files'])
    actual={p.as_posix() for p in OWN.rglob('*') if p.is_file()}; expected={p['path'] for p in manifest['owned_files']}|{(OWN/'native.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}
    assert actual==expected and len(actual)==lease['owned_files']; latest=(OWN/'lease.final.json').stat().st_mtime_ns; assert all(Path(p).stat().st_mtime_ns<=latest for p in actual)
    run=read(OWN/'run.json'); assert logical(run)==run['run_sha256']==lease['run_sha256']==manifest['run_sha256']; guard(run['inputs']); assert pin(HEADER)==lease['candidate']
    k=ctypes.windll.kernel32; handle=k.OpenProcess(0x1000,False,lease['actual_last_writer_PID']); gone=not bool(handle)
    if handle:
        code=ctypes.c_ulong(); assert k.GetExitCodeProcess(handle,ctypes.byref(code)); k.CloseHandle(handle); gone=code.value!=259
    assert gone
    print(json.dumps({'actual_external_readonly_PID':os.getpid(),'terminal_EXIT':0,'writer_PID':lease['actual_last_writer_PID'],'writer_exited':gone,'owned_files':len(actual),'finite_inputs':len(run['inputs']),'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json')},ensure_ascii=False))
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='inspect': inspect()
    elif mode=='launch': raise SystemExit(launch())
    elif mode=='close': close()
    elif mode=='readonly': readonly()
    else: raise ValueError(mode)
