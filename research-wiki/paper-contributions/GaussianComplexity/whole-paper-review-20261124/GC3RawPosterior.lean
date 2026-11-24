import GC3QueryPosterior
import GC3GuardedTrace

/-! The conditional ambient law for the original unrestricted primitive-query algorithm,
on its actual records and the original product Haar probability space. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior.PublicFrame
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior

variable {N k : ℕ}

def historyKernel (b : ℝ) : Kernel (Trace k N) (Ambient k N) :=
  (ambientKernel b).comap foldFrames measurable_foldFrames

def liveKernel (b : ℝ) : Kernel (Live k N) (Ambient k N) :=
  (historyKernel b).comap Prod.fst measurable_fst

theorem initialKernel {b : ℝ} (hb : b = -1 ∨ b = 1) (hN : 0 < N) :
    liveKernel (k := k) b (([],false) : Live k N) =
      Measure.pi (fun _ : Fin k => componentHaar N b) := by
  change ambientKernel b (initialFrames k N) = _
  have hd (j : Fin k) : 0 < (initialFrames k N j).1 := hN
  rw [ambientKernel_apply _ hd hb]
  have he : decodeAt (profile (initialFrames k N)) (initialFrames k N) = id := by
    funext w j
    rw [decodeAt_match]
    exact BlockFrame.initial_realize N (w j)
  rw [he]
  change (Measure.pi fun _ : Fin k => componentHaar N b).map id = _
  exact Measure.map_id (μ := Measure.pi fun _ : Fin k => componentHaar N b)

theorem next_joint {b : ℝ} (hb : b = -1 ∨ b = 1) (hN : 0 < N)
    (select : Trace k N → Option (Query k N)) (hs : Measurable select) (p : Live k N) :
    let K := liveKernel (N := N) (k := k) b
    (K p).map (fun W => (nextState select (p,W),W)) =
      ((K p).map (fun W => nextState select (p,W))) ⊗ₘ K := by
  let _ := markov_ambientKernel (N := N) (k := k) hb
  let _ : IsMarkovKernel (historyKernel (N := N) (k := k) b) :=
    inferInstanceAs (IsMarkovKernel ((ambientKernel b).comap foldFrames measurable_foldFrames))
  let K := liveKernel (N := N) (k := k) b
  let _ : IsMarkovKernel K := inferInstanceAs
    (IsMarkovKernel ((historyKernel b).comap (Prod.fst : Live k N → _) measurable_fst))
  change (K p).map (fun W => (nextState select (p,W),W)) = _ ⊗ₘ K
  cases hq : pickQuery select p with
  | none =>
    apply joint_of_constant (K p) K _ ((measurable_nextState hs).comp measurable_prodMk_left) (pushState p none)
    · exact .of_forall (fun W => by simp [nextState,hq])
    · change ambientKernel b (foldFrames (p.1 ++ [none])) = _
      rw [foldFrames_append, updateRecord_none]
      rfl
  | some q =>
    cases k with
    | zero => exact Fin.elim0 q.1
    | succ k =>
      rcases q with ⟨i,v,back⟩
      let q : Query (k+1) N := (i,v,back)
      let F := foldFrames p.1
      have hready : 2 ≤ profile F i := pickQuery_ready hq
      let n := profile F i - 2
      have hi : profile F i = n+2 := by dsimp [n]; omega
      let tag (y : Vec N) := pushState p (some (q,y))
      have ht : Measurable tag := measurable_pushState.comp
        (measurable_const.prodMk (measurable_some.comp (measurable_const.prodMk measurable_id)))
      have hstep : (fun W => nextState select (p,W)) = fun W => tag (oracleAnswer W q) := by
        funext W; simp [nextState,hq,tag,q]
      have hpair : (fun W => (nextState select (p,W),W)) =
          (fun W => (tag (oracleAnswer W q),W)) := by
        funext W; exact congrArg (fun a => (a,W)) (congrFun hstep W)
      rw [hstep,hpair]
      exact query_joint_at hb F (foldFrames_pos hN p.1) i hi v back tag ht K
        (fun y => by change ambientKernel b (foldFrames (p.1 ++ [some (q,y)])) = _; rw [foldFrames_append])

theorem raw_ambient_posterior {N k T : ℕ} (hN : 2*T < N)
    (select : Trace k N → Option (Query k N)) (hs : Measurable select)
    (t : ℕ) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (cap : ∀ᵐ W ∂(Measure.pi fun _ : Fin k => componentHaar N b),
      ∀ j, blockCount j (rawRun select t [] W) ≤ 2*T) :
    (Measure.pi fun _ : Fin k => componentHaar N b).map (fun W => (rawRun select t [] W,W)) =
      ((Measure.pi fun _ : Fin k => componentHaar N b).map (rawRun select t [])) ⊗ₘ
        ((ambientKernel b).comap foldFrames measurable_foldFrames) := by
  let μ := Measure.pi (fun _ : Fin k => componentHaar N b)
  let J := historyKernel (N := N) (k := k) b
  let K := liveKernel (N := N) (k := k) b
  let _ := markov_ambientKernel (N := N) (k := k) hb
  let _ : IsMarkovKernel J := inferInstanceAs (IsMarkovKernel
    ((ambientKernel b).comap foldFrames measurable_foldFrames))
  let _ : IsMarkovKernel K := inferInstanceAs (IsMarkovKernel
    (J.comap (Prod.fst : Live k N → _) measurable_fst))
  let p : Live k N := ([], false)
  let next := nextState select
  let f := repeatState next p t
  have hm : Measurable f := measurable_repeatState next (measurable_nextState hs) p t
  have hp : K p = μ := initialKernel hb (by omega)
  let _ : IsProbabilityMeasure μ := hp ▸ inferInstanceAs (IsProbabilityMeasure (K p))
  have joint : μ.map (fun W => (f W,W)) = (μ.map f) ⊗ₘ K := by
    rw [← hp]
    exact repeat_joint K next (measurable_nextState hs) (next_joint hb (by omega) select hs) p t
  have hproj := project_joint (μ.map f) (Prod.fst : Live k N → _) measurable_fst K J (fun _ => rfl)
  rw [← joint, Measure.map_map (measurable_fst.prodMap measurable_id)
    (show Measurable (fun W => (f W,W)) from hm.prodMk measurable_id),
    Measure.map_map measurable_fst hm] at hproj
  have he : ∀ᵐ W ∂μ, (f W).1 = rawRun select t [] W := by
    filter_upwards [cap] with W hw
    exact guarded_eq_rawRun select hN t W hw
  have e1 : μ.map (fun W => ((f W).1,W)) = μ.map (fun W => (rawRun select t [] W,W)) := by
    apply Measure.map_congr
    filter_upwards [he] with W hw; rw [hw]
  have e2 : μ.map (fun W => (f W).1) = μ.map (rawRun select t []) := Measure.map_congr he
  change μ.map (fun W => ((f W).1,W)) = (μ.map (fun W => (f W).1)) ⊗ₘ J at hproj
  rwa [e1,e2] at hproj

#print axioms raw_ambient_posterior
end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
