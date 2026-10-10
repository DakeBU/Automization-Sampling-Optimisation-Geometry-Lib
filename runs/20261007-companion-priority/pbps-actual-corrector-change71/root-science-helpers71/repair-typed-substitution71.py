from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean')
raw=p.read_bytes();s=raw.decode();parent=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_text(encoding='utf8')
assert json.loads((r/'focused-first/receipt.json').read_bytes())['exit_code']==1
log=(r/'focused-first/stdout.log').read_text(encoding='utf8');assert '415:19' in log and 'timeout at `isDefEq`' in log
dest=r/'typed-substitution-repair';dest.mkdir(exist_ok=False);(dest/'before.exactraw.lean').write_bytes(raw)
begin=parent.index('  have hGlobal70 :\n');a=begin+len('  have hGlobal70 :\n');b=parent.index(' := by\n    intro f hf',a)
oldtail=parent[a:b].strip();anchor='  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL\n'
assert s.count(anchor)==1;s=s.replace(anchor,'  change '+oldtail+' at hGlobal\n'+anchor)
old='''    rw [hgPformula,hgVformula]
    exact hCorrector fP (V0.adjoint (R f))
'''
new='''    let fV : HP0 := V0.adjoint (R f)
    let gV : HP0 := V0.adjoint (R (U (P f-(f-P f))))
    have hgp : gP=A0 fP-ΓP0 fV := hgPformula
    have hgv : gV=ΓP0 fP+A0 fV := hgVformula
    let C : HP0 → HP0 → ℝ := fun u v => (‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v
    change C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2
    have hPair : C gP gV=C (A0 fP-ΓP0 fV) (ΓP0 fP+A0 fV) :=
      congrArg₂ C hgp hgv
    exact (congrArg (fun a : ℝ => a-C fP fV) hPair).trans (hCorrector fP fV)
'''
assert s.count(old)==1;s=s.replace(old,new)
header=Path('runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean').read_bytes();assert s.encode().startswith(header)
p.write_text(s,encoding='utf8',newline='\n')
diagnosis=dict(status='IMPLEMENTATION_DEFINITIONAL_EQUALITY_ROUTE_REPAIRED_NOT_COMPILED',actual_root_PID=os.getpid(),typed_failure_class='API_BLOCKED',exact_old_failure='focused-first PID29980 EXIT1 deterministic isDefEq timeout at actual-coordinate rw line415; failed #print output is not a certificate.',strict_reduction='Retain sealed statement and all algebra; collapse full parent70 interface to local types once, and replace rewriting a large dependent expression by typed two-argument congruence.',before_RAW_sha256=hashlib.sha256(raw).hexdigest(),after_RAW_sha256=hashlib.sha256(s.encode()).hexdigest(),statement_changed=False,extra_public_premises=[],heartbeat_limit_raised=False)
(dest/'diagnosis.json').write_text(json.dumps(diagnosis,indent=2)+'\n',encoding='utf8')
sys.path.insert(0,str(root/'tools'));import astis_advance as adv
claim=json.loads((r/'claim.json').read_bytes())
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='same-actual-B21/large-dependent-rw-first',progress_signature='isDefEq-timeout-line415-EXIT1-not-a-proof',mathematical_delta='Exact prospective B21 route unchanged; compiler residual reduced to typed actual-coordinate substitution.',exact_residual='Focused compile of typed full parent interface and congruence substitution; independent math/decoder/source/publication/integration still pending.')
print('PASS statement unchanged; one diagnosed compiler-route repair, no extra assumption or heartbeat escalation.')
