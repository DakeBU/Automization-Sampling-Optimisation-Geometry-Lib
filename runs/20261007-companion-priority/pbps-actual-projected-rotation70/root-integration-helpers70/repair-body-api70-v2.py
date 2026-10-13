from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
receipt=json.loads((r/'named-literal-diagnostic-v1/receipt.json').read_bytes())
assert receipt['terminal_closed'] and receipt['exit_code']==1
p=Path('.astis/pbps-actual-rotation70/diagnostic-named-literal70.lean')
s=p.read_text(encoding='utf-8')
old='''    rw [hA0self.isSymmetric (A0 u) u,hΓself.isSymmetric (ΓP0 u) u] at h
    simpa only [real_inner_self_eq_norm_sq] using h'''
new='''    have ha : inner ℝ (A0 (A0 u)) u=‖A0 u‖^2 :=
      (hA0self.isSymmetric (A0 u) u).trans (real_inner_self_eq_norm_sq _)
    have hg : inner ℝ (ΓP0 (ΓP0 u)) u=‖ΓP0 u‖^2 :=
      (hΓself.isSymmetric (ΓP0 u) u).trans (real_inner_self_eq_norm_sq _)
    rw [ha,hg,real_inner_self_eq_norm_sq] at h
    exact h'''
assert s.count(old)==1;s=s.replace(old,new)
old='''          rw [hA0self.isSymmetric u fP,←B0.adjoint_inner_right,hB0adjMicro]'''
new='''          have ha : inner ℝ (A0 u) fP=inner ℝ u (A0 fP) := hA0self.isSymmetric u fP
          have hb : inner ℝ (B0 u) fperp=inner ℝ u (ΓP0 fV) :=
            (B0.adjoint_inner_right u fperp).symm.trans
              (congrArg (fun z : HP0 => inner ℝ u z) hB0adjMicro)
          exact congrArg₂ (fun x y : ℝ => x-y) ha hb'''
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace('set_option maxHeartbeats 2000000','set_option maxHeartbeats 4000000',1)
s=s.replace('[hSubIntegral,hPIntegral,hf,sub_self,sub_zero]','[hSubIntegral,hPIntegral,hf,sub_self]',1)
q=Path('.astis/pbps-actual-rotation70/diagnostic-named-literal70-v2.lean');assert not q.exists()
q.write_text(s,encoding='utf-8',newline='\n')
(r/'compiler-diagnosis70/body-api-v2.json').write_text(json.dumps(dict(status='BODY_API_REPAIR_SCRATCH_ONLY_NOT_APPLIED',
 input=p.as_posix(),input_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
 candidate=q.as_posix(),candidate_RAW_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),
 failure_diagnosis='Two rw patterns carry unnormalized continuous-map coercions from inherited witness instances; replace by explicitly typed inner-product equalities, preserving identical mathematics. Other timeouts followed exhausted global heartbeats.',
 maxHeartbeats=4000000,statement_changed=False,canonical_unchanged=True,
 representation_admission_pending=True,no_proof_credit=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('BODY-only typed adjoint/symmetry equalities prepared in V2 scratch; exact literal statement unchanged.')
