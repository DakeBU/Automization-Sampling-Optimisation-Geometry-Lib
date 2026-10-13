from pathlib import Path
import datetime,json,os,subprocess,sys,hashlib
r=Path(__file__).parent
p=Path('runs/20261007-companion-priority/pbps-actual-l2-flip-preread108/Header108.lean')
s=p.read_text(encoding='utf8').replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality').replace('PBPSActualL2FlipDualityCandidate108','PBPSActualPositionL2Candidate109')
old='''            ∀ T : ℝ≥0, (A T).adjoint =
              J.toContinuousLinearMap.comp ((A T).comp J.toContinuousLinearMap))'''
new='''            (∀ T : ℝ≥0, (A T).adjoint =
              J.toContinuousLinearMap.comp ((A T).comp J.toContinuousLinearMap)) ∧
            let mu : Measure E := (volume : Measure E).tilted (fun x => -Vy y x)
            ∃ hfst : MeasurePreserving Prod.fst (nu y) mu,
              let B : Lp ℝ 2 mu →ₗᵢ[ℝ] Lp ℝ 2 (nu y) :=
                Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hfst
              let M : Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 mu := B.toContinuousLinearMap.adjoint
              (∀ f : Lp ℝ 2 mu, (B f : (E × E) → ℝ) =ᵐ[nu y] fun z => f z.1) ∧
              ‖B.toContinuousLinearMap‖ ≤ 1 ∧ ‖M‖ ≤ 1 ∧
              M.comp B.toContinuousLinearMap = ContinuousLinearMap.id ℝ (Lp ℝ 2 mu) ∧
              (∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 (nu y),
                let gbar : E → ℝ := fun x => ∫ p, G (x, p) ∂stdGaussian E
                (∀ᵐ x ∂mu, Integrable (fun p => G (x, p)) (stdGaussian E)) ∧
                ∃ hbar : MemLp gbar 2 mu, M (hG.toLp G) = hbar.toLp gbar) ∧
              (∀ f : Lp ℝ 2 mu, J (B f) = B f) ∧
              M.comp J.toContinuousLinearMap = M ∧
              let Kpos : ℝ≥0 → (Lp ℝ 2 mu →L[ℝ] Lp ℝ 2 mu) :=
                fun T => M.comp ((A T).comp B.toContinuousLinearMap)
              Kpos 0 = ContinuousLinearMap.id ℝ (Lp ℝ 2 mu) ∧
              ∀ T : ℝ≥0, (Kpos T).adjoint = Kpos T ∧ ‖Kpos T‖ ≤ 1 ∧
                ∀ f : E → ℝ, ∀ hf : MemLp f 2 mu,
                  let kTf : E → ℝ := fun x =>
                    ∫ p, (∫ w, f ((Z y xRef (x, p) T w).1) ∂P) ∂stdGaussian E
                  (∀ᵐ x ∂mu, ∀ᵐ p ∂stdGaussian E,
                    Integrable (fun w => f ((Z y xRef (x, p) T w).1)) P) ∧
                  (∀ᵐ x ∂mu, Integrable
                    (fun p => ∫ w, f ((Z y xRef (x, p) T w).1) ∂P) (stdGaussian E)) ∧
                  ∃ hk : MemLp kTf 2 mu, Kpos T (hf.toLp f) = hk.toLp kTf)'''
assert s.count(old)==1;s=s.replace(old,new)
header=r/'Header109.lean';assert not header.exists();header.write_text(s,encoding='utf8',newline='\n')
out=r/'type-only1';out.mkdir(exist_ok=False)
env=os.environ.copy();env['PATH']=str(Path.cwd()/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
cmd=[str(Path.cwd()/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(header)]
q=subprocess.run(cmd,capture_output=True,env=env);(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
(out/'receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,exit_code=q.returncode,header_raw_sha256=hashlib.sha256(header.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf8',newline='\n')
print((q.stdout+q.stderr).decode(errors='replace'));sys.exit(q.returncode)
