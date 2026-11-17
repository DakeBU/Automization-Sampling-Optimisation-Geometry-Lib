import AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation
import AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
import Mathlib.MeasureTheory.MeasurableSpace.Prod
import Mathlib.Data.List.OfFn

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
open AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation
open AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
set_option autoImplicit false
universe uS uΩ

namespace AutoSamplingTheory.Tests.GaussianComplexityBatchedPrimitiveSimulation

private theorem sigma_mk_embedding {I : Type*} {F : I → Type*}
    [∀ i, MeasurableSpace (F i)] (i : I) :
    MeasurableEmbedding (Sigma.mk i : F i → Sigma F) where
  injective := by intro a b h; simpa using h
  measurable := Measurable.of_le_map (iInf_le _ i)
  measurableSet_image' := by
    classical
    intro t ht
    apply MeasurableSpace.measurableSet_iInf.mpr
    intro j
    change MeasurableSet ((Sigma.mk j) ⁻¹' ((Sigma.mk i) '' t))
    by_cases h : j = i
    · subst j
      have he : (Sigma.mk i) ⁻¹' ((Sigma.mk i) '' t) = t := by
        ext x
        simp
      rw [he]
      exact ht
    · have he : (Sigma.mk j) ⁻¹' ((Sigma.mk i) '' t) = ∅ := by
        ext x
        simp only [Set.mem_preimage, Set.mem_image, Set.mem_empty_iff_false, iff_false,
          not_exists, not_and]
        intro y _ hy
        exact h (congrArg Sigma.fst hy).symm
      rw [he]
      exact MeasurableSet.empty

private theorem measurable_prod_sigma {I : Type*} {F : I → Type*}
    {U V : Type*} [Countable I] [∀ i, MeasurableSpace (F i)]
    [MeasurableSpace U] [MeasurableSpace V]
    (f : U × Sigma F → V)
    (hf : ∀ i, Measurable (fun p : U × F i => f (p.1, ⟨i, p.2⟩))) :
    Measurable f := by
  intro t ht
  have he : f ⁻¹' t = ⋃ i, (fun p : U × F i => (p.1, (⟨i, p.2⟩ : Sigma F))) ''
      ((fun p : U × F i => f (p.1, ⟨i, p.2⟩)) ⁻¹' t) := by
    ext p
    constructor
    · rcases p with ⟨a, i, b⟩
      intro h
      exact Set.mem_iUnion.mpr ⟨i, ⟨(a,b), h, rfl⟩⟩
    · intro h
      rcases Set.mem_iUnion.mp h with ⟨i, q, hq, rfl⟩
      exact hq
  rw [he]
  apply MeasurableSet.iUnion
  intro i
  exact (MeasurableEmbedding.id.prodMap (sigma_mk_embedding i)).measurableSet_image.mpr
    (hf i ht)

private theorem measurable_list_cons {U : Type*} [MeasurableSpace U] :
    letI : MeasurableSpace (List U) := MeasurableSpace.comap
      (fun l : List U => (⟨l.length, fun i : Fin l.length => l.get i⟩ :
        Σ t : ℕ, Fin t → U)) inferInstance
    Measurable (fun p : U × List U => p.1 :: p.2) := by
  classical
  let : MeasurableSpace (List U) := MeasurableSpace.comap
    (List.equivSigmaTuple : List U → Σ t : ℕ, Fin t → U) inferInstance
  apply measurable_comap_iff.mpr
  have hcons : Measurable (fun p : U × (Σ t : ℕ, Fin t → U) =>
      (⟨p.2.1 + 1, Fin.cons p.1 p.2.2⟩ : Σ t : ℕ, Fin t → U)) := by
    apply measurable_prod_sigma
    intro n
    apply (sigma_mk_embedding (n+1)).measurable.comp
    apply measurable_pi_iff.mpr
    intro i
    refine Fin.cases ?_ (fun j => ?_) i
    · exact measurable_fst
    · exact (measurable_pi_apply j).comp measurable_snd
  have hencode : Measurable (List.equivSigmaTuple : List U → Σ t : ℕ, Fin t → U) :=
    comap_measurable _
  convert hcons.comp (measurable_fst.prodMk (hencode.comp measurable_snd)) using 1 <;>
    first | rfl | skip
  funext p
  change (⟨p.2.length+1, fun i => (p.1 :: p.2).get i⟩ : Σ t : ℕ, Fin t → U) =
    ⟨p.2.length+1, Fin.cons p.1 p.2.get⟩
  apply congrArg (fun v : Fin (p.2.length+1) → U =>
    (⟨p.2.length+1, v⟩ : Σ t : ℕ, Fin t → U))
  funext i
  refine Fin.cases ?_ (fun j => ?_) i <;> rfl

private theorem measurable_batch_callbacks
    {S Q A B X P : Type*} [MeasurableSpace S] [MeasurableSpace Q]
    [MeasurableSpace A] [MeasurableSpace B] [MeasurableSpace X] [MeasurableSpace P]
    (m : ℕ) (hm : 0 < m) (blank : A)
    (next : S → Sum X Q) (update : S → Q → B → S)
    (plan : Q → Fin m → P) (decode : Q → (Fin m → A) → B)
    (hnext : Measurable next)
    (hupdate : Measurable (fun p : S × Q × B => update p.1 p.2.1 p.2.2))
    (hplan : Measurable (fun p : Q × Fin m => plan p.1 p.2))
    (hdecode : Measurable (fun p : Q × (Fin m → A) => decode p.1 p.2)) :
    letI : MeasurableSpace (List (P × A)) := MeasurableSpace.comap
      (List.equivSigmaTuple : List (P × A) → Σ t : ℕ, Fin t → P × A) inferInstance
    let Micro := S × (Fin m → A) × Fin m × List (P × A)
    let nextB : Micro → Sum X P := fun z => match next z.1 with
      | .inl x => .inl x
      | .inr q => .inr (plan q z.2.2.1)
    let updateB : Micro → P → A → Micro := fun z p a => match next z.1 with
      | .inl _ => z
      | .inr q =>
        let answers := Function.update z.2.1 z.2.2.1 a
        let history := (p,a) :: z.2.2.2
        if h : z.2.2.1.val + 1 < m then
          (z.1, answers, ⟨z.2.2.1.val+1,h⟩, history)
        else (update z.1 q (decode q answers), (fun _ => blank), ⟨0,hm⟩, history)
    Measurable nextB ∧
      Measurable (fun p : Micro × P × A => updateB p.1 p.2.1 p.2.2) := by
  classical
  let : MeasurableSpace (List (P × A)) := MeasurableSpace.comap
    (List.equivSigmaTuple : List (P × A) → Σ t : ℕ, Fin t → P × A) inferInstance
  let M := S × (Fin m → A) × Fin m × List (P × A)
  dsimp only
  have hd : Measurable (fun z : M =>
      (MeasurableEquiv.prodSumDistrib M X Q) (z, next z.1)) :=
    (MeasurableEquiv.prodSumDistrib M X Q).measurable.comp
      (measurable_id.prodMk (hnext.comp measurable_fst))
  have hl : Measurable (fun p : M × X => (Sum.inl p.2 : Sum X P)) :=
    measurable_inl.comp measurable_snd
  have hr : Measurable (fun p : M × Q => (Sum.inr (plan p.2 p.1.2.2.1) : Sum X P)) :=
    measurable_inr.comp (hplan.comp (measurable_snd.prodMk measurable_fst.snd.snd.fst))
  constructor
  · convert (hl.sumElim hr).comp hd using 1
    funext z
    cases h : next z.1 <;> simp only [Function.comp_apply, h] <;> rfl
  · let D := M × P × A
    have hanswers : Measurable (fun p : D => Function.update p.1.2.1 p.1.2.2.1 p.2.2) := by
      apply measurable_pi_iff.mpr
      intro i
      have he : MeasurableSet {p : D | p.1.2.2.1 = i} :=
        measurable_fst.snd.snd.fst (measurableSet_singleton i)
      have hh : Measurable (fun p : D =>
          if p.1.2.2.1 = i then p.2.2 else p.1.2.1 i) :=
        measurable_snd.snd.ite he
          ((measurable_pi_apply i).comp measurable_fst.snd.fst)
      simpa only [Function.update_apply, eq_comm] using hh
    have hhistory : Measurable (fun p : D => (p.2.1,p.2.2) :: p.1.2.2.2) :=
      measurable_list_cons.comp
        ((measurable_snd.fst.prodMk measurable_snd.snd).prodMk measurable_fst.snd.snd.snd)
    let advance : Fin m → Fin m := fun i =>
      if h : i.val+1<m then ⟨i.val+1,h⟩ else ⟨0,hm⟩
    have hadvance : Measurable advance := measurable_of_countable _
    have hphase : Measurable (fun p : D × Q => p.1.1.2.2.1) :=
      measurable_fst.fst.snd.snd.fst
    have hcontinue : Measurable (fun p : D × Q =>
        (p.1.1.1, Function.update p.1.1.2.1 p.1.1.2.2.1 p.1.2.2,
          advance p.1.1.2.2.1, (p.1.2.1,p.1.2.2) :: p.1.1.2.2.2)) :=
      measurable_fst.fst.fst.prodMk ((hanswers.comp measurable_fst).prodMk
        ((hadvance.comp hphase).prodMk (hhistory.comp measurable_fst)))
    have hcommit : Measurable (fun p : D × Q =>
        (update p.1.1.1 p.2 (decode p.2
          (Function.update p.1.1.2.1 p.1.1.2.2.1 p.1.2.2)),
          (fun _ : Fin m => blank), (⟨0,hm⟩ : Fin m),
          (p.1.2.1,p.1.2.2) :: p.1.1.2.2.2)) :=
      (hupdate.comp (measurable_fst.fst.fst.prodMk
        (measurable_snd.prodMk (hdecode.comp
          (measurable_snd.prodMk (hanswers.comp measurable_fst)))))).prodMk
        (measurable_const.prodMk (measurable_const.prodMk (hhistory.comp measurable_fst)))
    have hcond : MeasurableSet {p : D × Q | p.1.1.2.2.1.val+1<m} :=
      hphase (Set.toFinite {i : Fin m | i.val+1<m}).measurableSet
    have hright : Measurable (fun p : D × Q =>
        if p.1.1.2.2.1.val+1<m then
          (p.1.1.1, Function.update p.1.1.2.1 p.1.1.2.2.1 p.1.2.2,
            advance p.1.1.2.2.1, (p.1.2.1,p.1.2.2) :: p.1.1.2.2.2)
        else (update p.1.1.1 p.2 (decode p.2
          (Function.update p.1.1.2.1 p.1.1.2.2.1 p.1.2.2)),
          (fun _ : Fin m => blank), (⟨0,hm⟩ : Fin m),
          (p.1.2.1,p.1.2.2) :: p.1.1.2.2.2)) := hcontinue.ite hcond hcommit
    have hdist : Measurable (fun p : D =>
        (MeasurableEquiv.prodSumDistrib D X Q) (p,next p.1.1)) :=
      (MeasurableEquiv.prodSumDistrib D X Q).measurable.comp
        (measurable_id.prodMk (hnext.comp measurable_fst.fst))
    have hleft : Measurable (fun p : D × X => p.1.1) := measurable_fst.fst
    convert (hleft.sumElim hright).comp hdist using 1
    funext p
    cases h : next p.1.1 with
    | inl x => simp only [Function.comp_apply,h]; rfl
    | inr q =>
      simp only [Function.comp_apply,h]
      change (if h : p.1.2.2.1.val+1<m then
        (p.1.1, Function.update p.1.2.1 p.1.2.2.1 p.2.2,
          ⟨p.1.2.2.1.val+1,h⟩, (p.2.1,p.2.2) :: p.1.2.2.2)
        else (update p.1.1 q (decode q (Function.update p.1.2.1 p.1.2.2.1 p.2.2)),
          (fun _ => blank), ⟨0,hm⟩, (p.2.1,p.2.2) :: p.1.2.2.2)) =
        (if p.1.2.2.1.val+1<m then
          (p.1.1, Function.update p.1.2.1 p.1.2.2.1 p.2.2,
            advance p.1.2.2.1, (p.2.1,p.2.2) :: p.1.2.2.2)
        else (update p.1.1 q (decode q (Function.update p.1.2.1 p.1.2.2.1 p.2.2)),
          (fun _ => blank), ⟨0,hm⟩, (p.2.1,p.2.2) :: p.1.2.2.2))
      dsimp only [advance]
      split_ifs <;> rfl

private theorem block_slot_count (k : ℕ) (j : Fin k) :
    (List.ofFn (fun i : Fin (k*2) =>
      (finProdFinEquiv.symm i : Fin k × Fin 2).1)).countP
        (fun v => decide (v=j)) = 2 := by
  classical
  let l := List.ofFn (finProdFinEquiv.symm : Fin (k*2) → Fin k × Fin 2)
  have hn : l.Nodup := List.nodup_ofFn_ofInjective finProdFinEquiv.symm.injective
  have hall : l.toFinset = Finset.univ := by
    ext p
    simp only [List.mem_toFinset, l, List.mem_ofFn, Finset.mem_univ, iff_true]
    exact finProdFinEquiv.symm.surjective p
  have hf : (Finset.univ : Finset (Fin k × Fin 2)).filter (fun p => p.1=j) =
      ({j} : Finset (Fin k)) ×ˢ (Finset.univ : Finset (Fin 2)) := by
    ext p
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_product,
      Finset.mem_singleton, and_true]
  rw [show List.ofFn (fun i : Fin (k*2) =>
      (finProdFinEquiv.symm i : Fin k × Fin 2).1) = l.map Prod.fst by
    simp only [l, List.map_ofFn, Function.comp_def], List.countP_map]
  change l.countP (fun p => decide (p.1=j)) = 2
  rw [← hn.card_eq_countP, hall, hf]
  simp

-- The sealed statement names hκ although no later binder depends on its proof term.
set_option linter.unusedVariables false in
set_option backward.isDefEq.respectTransparency false in
private theorem actual_block_first_order_primitive_simulation_laws_and_costs :
  ∀ {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d),
    ∀ {κ : ℝ} (hκ : 4 ≤ κ),
    letI : MeasurableSpace (EuclideanSpace ℝ (Fin d)) := borel _
    letI : MeasurableSpace (EuclideanSpace ℝ (Fin n)) := borel _
    letI : MeasurableSpace (Option (EuclideanSpace ℝ (Fin d))) :=
      MeasurableSpace.comap
        (fun x : Option (EuclideanSpace ℝ (Fin d)) =>
          x.elim (Sum.inl () : Unit ⊕ EuclideanSpace ℝ (Fin d)) Sum.inr) inferInstance
    ∀ {S : Type uS} {Ω : Type uΩ} [MeasurableSpace S] [MeasurableSpace Ω]
      (μ : Measure Ω) [IsProbabilityMeasure μ]
      (next : S → Sum (EuclideanSpace ℝ (Fin d)) (EuclideanSpace ℝ (Fin d)))
      (updateFO : S → EuclideanSpace ℝ (Fin d) →
        (ℝ × EuclideanSpace ℝ (Fin d)) → S)
      (updateGrad : S → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) → S)
      (initial : Ω → S),
      Measurable next →
      Measurable (fun p : S × EuclideanSpace ℝ (Fin d) ×
        (ℝ × EuclideanSpace ℝ (Fin d)) => updateFO p.1 p.2.1 p.2.2) →
      Measurable (fun p : S × EuclideanSpace ℝ (Fin d) ×
        EuclideanSpace ℝ (Fin d) => updateGrad p.1 p.2.1 p.2.2) →
      Measurable initial →
      ∀ (fuel : ℕ), 2 * fuel < n →
        let k := d / n
        let m := k * 2
        let zero : Fin m := ⟨0, Nat.mul_pos (Nat.div_pos hnd (by omega)) (by decide)⟩
        let e : ((Fin n × Fin k) ⊕ Fin (d % n)) ≃ Fin d :=
          ((Equiv.sumCongr
            ((Equiv.prodComm (Fin n) (Fin k)).trans finProdFinEquiv)
            (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
            (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
        let Ed := EuclideanSpace ℝ (Fin d)
        let En := EuclideanSpace ℝ (Fin n)
        let Primitive := Fin k × En × Bool
        letI : MeasurableSpace (List (Primitive × En)) :=
          MeasurableSpace.comap
            (fun l : List (Primitive × En) =>
              (⟨l.length, fun i : Fin l.length => l.get i⟩ :
                Σ t : ℕ, Fin t → Primitive × En)) inferInstance
        let Micro := S × (Fin m → En) × Fin m × List (Primitive × En)
        let xb : Ed → Fin k → En := fun x j =>
          WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
        let plan : Ed → Fin m → Primitive := fun x i =>
          let ij : Fin k × Fin 2 := finProdFinEquiv.symm i
          (ij.1, xb x ij.1, decide (ij.2.val = 1))
        let reconstruct : Ed → (Fin m → En) → Ed := fun x replies =>
          let gb : Fin k → En := fun j =>
            ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
              (replies (finProdFinEquiv (j, (0 : Fin 2))) +
                replies (finProdFinEquiv (j, (1 : Fin 2))))
          WithLp.toLp 2 (fun a => Sum.elim
            (fun ij => gb ij.2 ij.1)
            (fun i => x (e (Sum.inr i))) (e.symm a))
        let decodeFO : Ed → (Fin m → En) → ℝ × Ed := fun x replies =>
          (inner ℝ x (reconstruct x replies) / 2, reconstruct x replies)
        let nextB : Micro → Sum Ed Primitive := fun z =>
          match next z.1 with
          | .inl x => .inl x
          | .inr x => .inr (plan x z.2.2.1)
        let updateBFO : Micro → Primitive → En → Micro := fun z p a =>
          match next z.1 with
          | .inl _ => z
          | .inr x =>
            let answers := Function.update z.2.1 z.2.2.1 a
            let history := (p, a) :: z.2.2.2
            if h : z.2.2.1.val + 1 < m then
              (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
            else
              (updateFO z.1 x (decodeFO x answers), (fun _ => 0), zero, history)
        let updateBGrad : Micro → Primitive → En → Micro := fun z p a =>
          match next z.1 with
          | .inl _ => z
          | .inr x =>
            let answers := Function.update z.2.1 z.2.2.1 a
            let history := (p, a) :: z.2.2.2
            if h : z.2.2.1.val + 1 < m then
              (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
            else
              (updateGrad z.1 x (reconstruct x answers), (fun _ => 0), zero, history)
        let start : Ω → Micro := fun ω => (initial ω, (fun _ => 0), zero, [])
        let readback : (Micro × Option Ed) × ℕ → (S × Option Ed) × ℕ := fun r =>
          ((r.1.1.1, r.1.2), r.2 / m)
        let blockCalls : Fin k → ((Micro × Option Ed) × ℕ) → ℕ := fun j r =>
          r.1.1.2.2.2.countP (fun pa => decide (pa.1.1 = j))
        ∀ (Os : Fin k → Matrix.orthogonalGroup (Fin n) ℝ),
          let A := blockPrecision κ Os
          let f : Ed → ℝ := fun x =>
            (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
          let primitive : Primitive → En := fun p =>
            WithLp.toLp 2 (if p.2.2 then
              (Os p.1 : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp p.2.1
            else (Os p.1 : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp p.2.1)
          let fo : Ed → ℝ × Ed := fun x => (f x, gradient f x)
          let grad : Ed → Ed := fun x => gradient f x
          let directFO := fun ω => run next updateFO fo fuel (initial ω)
          let batchFO := fun ω => run nextB updateBFO primitive (m * fuel) (start ω)
          let directGrad := fun ω => run next updateGrad grad fuel (initial ω)
          let batchGrad := fun ω => run nextB updateBGrad primitive (m * fuel) (start ω)
          Measurable primitive ∧ Measurable nextB ∧
          Measurable (fun p : Micro × Primitive × En => updateBFO p.1 p.2.1 p.2.2) ∧
          Measurable (fun p : Micro × Primitive × En => updateBGrad p.1 p.2.1 p.2.2) ∧
          Measurable start ∧
          Measurable batchFO ∧ Measurable directFO ∧
          (∀ ω, readback (batchFO ω) = directFO ω ∧
            (batchFO ω).2 = m * (directFO ω).2 ∧
            (directFO ω).2 ≤ fuel ∧
            (batchFO ω).2 ≤ m * fuel ∧
            ∀ j : Fin k, blockCalls j (batchFO ω) = 2 * (directFO ω).2 ∧
              blockCalls j (batchFO ω) ≤ 2 * fuel ∧
              blockCalls j (batchFO ω) < n) ∧
          μ.map (fun ω => readback (batchFO ω)) = μ.map directFO ∧
          IsProbabilityMeasure (μ.map directFO) ∧
          Integrable (fun ω => ((directFO ω).2 : ℝ)) μ ∧
          Integrable (fun ω => ((batchFO ω).2 : ℝ)) μ ∧
          (∫ ω, ((batchFO ω).2 : ℝ) ∂μ) =
            (m : ℝ) * (∫ ω, ((directFO ω).2 : ℝ) ∂μ) ∧
          (∫ ω, ((batchFO ω).2 : ℝ) ∂μ) ≤ (m * fuel : ℕ) ∧
          (∀ j : Fin k,
            Integrable (fun ω => (blockCalls j (batchFO ω) : ℝ)) μ ∧
            (∫ ω, (blockCalls j (batchFO ω) : ℝ) ∂μ) =
              2 * (∫ ω, ((directFO ω).2 : ℝ) ∂μ) ∧
            (∫ ω, (blockCalls j (batchFO ω) : ℝ) ∂μ) ≤ (2 * fuel : ℕ)) ∧
          Measurable batchGrad ∧ Measurable directGrad ∧
          (∀ ω, readback (batchGrad ω) = directGrad ω ∧
            (batchGrad ω).2 = m * (directGrad ω).2 ∧
            (directGrad ω).2 ≤ fuel ∧
            (batchGrad ω).2 ≤ m * fuel ∧
            ∀ j : Fin k, blockCalls j (batchGrad ω) = 2 * (directGrad ω).2 ∧
              blockCalls j (batchGrad ω) ≤ 2 * fuel ∧
              blockCalls j (batchGrad ω) < n) ∧
          μ.map (fun ω => readback (batchGrad ω)) = μ.map directGrad ∧
          IsProbabilityMeasure (μ.map directGrad) ∧
          Integrable (fun ω => ((directGrad ω).2 : ℝ)) μ ∧
          Integrable (fun ω => ((batchGrad ω).2 : ℝ)) μ ∧
          (∫ ω, ((batchGrad ω).2 : ℝ) ∂μ) =
            (m : ℝ) * (∫ ω, ((directGrad ω).2 : ℝ) ∂μ) ∧
          (∫ ω, ((batchGrad ω).2 : ℝ) ∂μ) ≤ (m * fuel : ℕ) ∧
          (∀ j : Fin k,
            Integrable (fun ω => (blockCalls j (batchGrad ω) : ℝ)) μ ∧
            (∫ ω, (blockCalls j (batchGrad ω) : ℝ) ∂μ) =
              2 * (∫ ω, ((directGrad ω).2 : ℝ) ∂μ) ∧
            (∫ ω, (blockCalls j (batchGrad ω) : ℝ) ∂μ) ≤ (2 * fuel : ℕ))
 := by
  classical
  intro d n hn hnd κ hκ
  let Ed := EuclideanSpace ℝ (Fin d)
  let En := EuclideanSpace ℝ (Fin n)
  let : MeasurableSpace Ed := borel _
  let : MeasurableSpace En := borel _
  let : BorelSpace Ed := ⟨rfl⟩
  let : BorelSpace En := ⟨rfl⟩
  let : MeasurableSpace (Option Ed) := MeasurableSpace.comap
    (fun x : Option Ed => x.elim (Sum.inl () : Unit ⊕ Ed) Sum.inr) inferInstance
  dsimp only
  intro S Ω mS mΩ μ hμ next updateFO updateGrad initial hnext huFO huGrad hi
    fuel hsmall
  let k := d / n
  let m := k * 2
  let zero : Fin m := ⟨0, Nat.mul_pos (Nat.div_pos hnd (by omega)) (by decide)⟩
  let e : ((Fin n × Fin k) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin k)).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let Primitive := Fin k × En × Bool
  let : MeasurableSpace (List (Primitive × En)) :=
    MeasurableSpace.comap
      (fun l : List (Primitive × En) =>
        (⟨l.length, fun i : Fin l.length => l.get i⟩ :
          Σ t : ℕ, Fin t → Primitive × En)) inferInstance
  let Micro := S × (Fin m → En) × Fin m × List (Primitive × En)
  let xb : Ed → Fin k → En := fun x j =>
    WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
  let plan : Ed → Fin m → Primitive := fun x i =>
    let ij : Fin k × Fin 2 := finProdFinEquiv.symm i
    (ij.1, xb x ij.1, decide (ij.2.val = 1))
  let reconstruct : Ed → (Fin m → En) → Ed := fun x replies =>
    let gb : Fin k → En := fun j =>
      ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
        (replies (finProdFinEquiv (j, (0 : Fin 2))) +
          replies (finProdFinEquiv (j, (1 : Fin 2))))
    WithLp.toLp 2 (fun a => Sum.elim
      (fun ij => gb ij.2 ij.1)
      (fun i => x (e (Sum.inr i))) (e.symm a))
  let decodeFO : Ed → (Fin m → En) → ℝ × Ed := fun x replies =>
    (inner ℝ x (reconstruct x replies) / 2, reconstruct x replies)
  let nextB : Micro → Sum Ed Primitive := fun z =>
    match next z.1 with
    | .inl x => .inl x
    | .inr x => .inr (plan x z.2.2.1)
  let updateBFO : Micro → Primitive → En → Micro := fun z p a =>
    match next z.1 with
    | .inl _ => z
    | .inr x =>
      let answers := Function.update z.2.1 z.2.2.1 a
      let history := (p, a) :: z.2.2.2
      if h : z.2.2.1.val + 1 < m then
        (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
      else
        (updateFO z.1 x (decodeFO x answers), (fun _ => 0), zero, history)
  let updateBGrad : Micro → Primitive → En → Micro := fun z p a =>
    match next z.1 with
    | .inl _ => z
    | .inr x =>
      let answers := Function.update z.2.1 z.2.2.1 a
      let history := (p, a) :: z.2.2.2
      if h : z.2.2.1.val + 1 < m then
        (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
      else
        (updateGrad z.1 x (reconstruct x answers), (fun _ => 0), zero, history)
  let start : Ω → Micro := fun ω => (initial ω, (fun _ => 0), zero, [])
  let readback : (Micro × Option Ed) × ℕ → (S × Option Ed) × ℕ := fun r =>
    ((r.1.1.1, r.1.2), r.2 / m)
  let blockCalls : Fin k → ((Micro × Option Ed) × ℕ) → ℕ := fun j r =>
    r.1.1.2.2.2.countP (fun pa => decide (pa.1.1 = j))
  intro Os
  let A := blockPrecision κ Os
  let f : Ed → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let primitive : Primitive → En := fun p =>
    WithLp.toLp 2 (if p.2.2 then
      (Os p.1 : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp p.2.1
    else (Os p.1 : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp p.2.1)
  let fo : Ed → ℝ × Ed := fun x => (f x, gradient f x)
  let grad : Ed → Ed := fun x => gradient f x
  let directFO := fun ω => run next updateFO fo fuel (initial ω)
  let batchFO := fun ω => run nextB updateBFO primitive (m * fuel) (start ω)
  let directGrad := fun ω => run next updateGrad grad fuel (initial ω)
  let batchGrad := fun ω => run nextB updateBGrad primitive (m * fuel) (start ω)
  have hm : 0 < m := Nat.mul_pos (Nat.div_pos hnd (by omega)) (by decide)
  have hxb (j : Fin k) : Continuous (fun x : Ed => xb x j) := by
    apply (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
    exact continuous_pi (fun i => PiLp.continuous_apply 2 (fun _ : Fin d => ℝ) (e (Sum.inl (i,j))))
  have hplan : Measurable (fun p : Ed × Fin m => plan p.1 p.2) := by
    apply measurable_from_prod_countable_left
    intro i
    dsimp only [plan]
    exact (measurable_const (a := (finProdFinEquiv.symm i : Fin k × Fin 2).1)).prodMk
      ((hxb _).measurable.prodMk
        (measurable_const (a := (decide ((finProdFinEquiv.symm i : Fin k × Fin 2).2.val = 1) : Bool))))
  have hrec : Continuous (fun p : Ed × (Fin m → En) => reconstruct p.1 p.2) := by
    apply (PiLp.continuous_toLp 2 (fun _ : Fin d => ℝ)).comp
    apply continuous_pi
    intro a
    cases h : e.symm a with
    | inl ij =>
      change Continuous (fun p : Ed × (Fin m → En) =>
        (((κ+1)/2) • xb p.1 ij.2 - ((κ-1)/4) •
          (p.2 (finProdFinEquiv (ij.2,(0 : Fin 2))) +
            p.2 (finProdFinEquiv (ij.2,(1 : Fin 2))))) ij.1)
      exact (PiLp.continuous_apply 2 (fun _ : Fin n => ℝ) ij.1).comp
        ((((hxb ij.2).comp continuous_fst).const_smul ((κ+1)/2)).sub
          ((((continuous_apply (finProdFinEquiv (ij.2,(0 : Fin 2)))).comp continuous_snd).add
            ((continuous_apply (finProdFinEquiv (ij.2,(1 : Fin 2)))).comp continuous_snd)).const_smul ((κ-1)/4)))
    | inr i =>
      change Continuous (fun p : Ed × (Fin m → En) => p.1 (e (Sum.inr i)))
      exact (PiLp.continuous_apply 2 (fun _ : Fin d => ℝ) _).comp continuous_fst
  have hdecodeFO : Measurable (fun p : Ed × (Fin m → En) => decodeFO p.1 p.2) :=
    ((continuous_fst.inner hrec).div_const 2 |>.prodMk hrec).measurable
  have hprimitive : Measurable primitive := by
    have hb : Measurable (fun p : (Fin k × En) × Bool =>
        primitive (p.1.1,p.1.2,p.2)) := by
      apply measurable_from_prod_countable_left
      intro b
      apply measurable_from_prod_countable_right
      intro j
      cases b
      · change Measurable (Matrix.toEuclideanCLM (𝕜 := ℝ) (Os j : Matrix (Fin n) (Fin n) ℝ))
        exact (Matrix.toEuclideanCLM (𝕜 := ℝ) _).continuous.measurable
      · change Measurable (Matrix.toEuclideanCLM (𝕜 := ℝ)
          (Os j : Matrix (Fin n) (Fin n) ℝ).transpose)
        exact (Matrix.toEuclideanCLM (𝕜 := ℝ) _).continuous.measurable
    exact hb.comp ((measurable_fst.prodMk measurable_snd.fst).prodMk measurable_snd.snd)
  have hdecode (x : Ed) : decodeFO x (fun i => primitive (plan x i)) = fo x := by
    have hx := (AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query
      hn hnd hκ Os x).2
    have h0 (j : Fin k) : primitive (plan x (finProdFinEquiv (j,(0 : Fin 2)))) =
        WithLp.toLp 2 ((Os j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp (xb x j)) := by
      simp only [plan, Equiv.symm_apply_apply]
      rfl
    have h1 (j : Fin k) : primitive (plan x (finProdFinEquiv (j,(1 : Fin 2)))) =
        WithLp.toLp 2 ((Os j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp (xb x j)) := by
      simp only [plan, Equiv.symm_apply_apply]
      rfl
    simpa only [decodeFO, reconstruct, h0, h1, fo, f, A, xb, e, Bool.false_eq_true, if_false, if_true, eq_self_iff_true] using hx.symm
  have hdecodeGrad (x : Ed) : reconstruct x (fun i => primitive (plan x i)) = grad x :=
    congrArg Prod.snd (hdecode x)
  have hfo : Measurable fo := by
    have hreplies : Measurable (fun x : Ed => fun i => primitive (plan x i)) := by
      apply measurable_pi_iff.mpr
      intro i
      exact hprimitive.comp (hplan.comp (measurable_id.prodMk measurable_const))
    have hh := hdecodeFO.comp (measurable_id.prodMk hreplies)
    exact (funext hdecode) ▸ hh
  have hgrad : Measurable grad := measurable_snd.comp hfo
  have hstart : Measurable start :=
    hi.prodMk (measurable_const.prodMk (measurable_const.prodMk measurable_const))
  have hcallbacksFO := measurable_batch_callbacks m hm (0 : En) next updateFO
    plan decodeFO hnext huFO hplan hdecodeFO
  have policy (B : Type) [MeasurableSpace B]
      (update : S → Ed → B → S) (target : Ed → B)
      (decode : Ed → (Fin m → En) → B)
      (hu : Measurable (fun p : S × Ed × B => update p.1 p.2.1 p.2.2))
      (htarget : Measurable target)
      (hd : Measurable (fun p : Ed × (Fin m → En) => decode p.1 p.2))
      (hcorrect : ∀ x, decode x (fun i => primitive (plan x i)) = target x) :
      let updateB : Micro → Primitive → En → Micro := fun z p a =>
        match next z.1 with
        | .inl _ => z
        | .inr x =>
          let answers := Function.update z.2.1 z.2.2.1 a
          let history := (p,a) :: z.2.2.2
          if h : z.2.2.1.val+1<m then
            (z.1,answers,⟨z.2.2.1.val+1,h⟩,history)
          else (update z.1 x (decode x answers), (fun _ => 0), zero, history)
      let direct := fun ω => run next update target fuel (initial ω)
      let batch := fun ω => run nextB updateB primitive (m*fuel) (start ω)
      Measurable (fun p : Micro × Primitive × En => updateB p.1 p.2.1 p.2.2) ∧
      Measurable batch ∧ Measurable direct ∧
      (∀ ω, readback (batch ω) = direct ω ∧
        (batch ω).2 = m * (direct ω).2 ∧
        (direct ω).2 ≤ fuel ∧
        (batch ω).2 ≤ m * fuel ∧
        ∀ j : Fin k, blockCalls j (batch ω) = 2 * (direct ω).2 ∧
          blockCalls j (batch ω) ≤ 2 * fuel ∧
          blockCalls j (batch ω) < n) ∧
      μ.map (fun ω => readback (batch ω)) = μ.map direct ∧
      IsProbabilityMeasure (μ.map direct) ∧
      Integrable (fun ω => ((direct ω).2 : ℝ)) μ ∧
      Integrable (fun ω => ((batch ω).2 : ℝ)) μ ∧
      (∫ ω, ((batch ω).2 : ℝ) ∂μ) =
        (m : ℝ) * (∫ ω, ((direct ω).2 : ℝ) ∂μ) ∧
      (∫ ω, ((batch ω).2 : ℝ) ∂μ) ≤ (m * fuel : ℕ) ∧
      (∀ j : Fin k,
        Integrable (fun ω => (blockCalls j (batch ω) : ℝ)) μ ∧
        (∫ ω, (blockCalls j (batch ω) : ℝ) ∂μ) =
          2 * (∫ ω, ((direct ω).2 : ℝ) ∂μ) ∧
        (∫ ω, (blockCalls j (batch ω) : ℝ) ∂μ) ≤ (2 * fuel : ℕ)) := by
    let updateB : Micro → Primitive → En → Micro := fun z p a =>
      match next z.1 with
      | .inl _ => z
      | .inr x =>
        let answers := Function.update z.2.1 z.2.2.1 a
        let history := (p,a) :: z.2.2.2
        if h : z.2.2.1.val+1<m then
          (z.1,answers,⟨z.2.2.1.val+1,h⟩,history)
        else (update z.1 x (decode x answers), (fun _ => 0), zero, history)
    let direct := fun ω => run next update target fuel (initial ω)
    let batch := fun ω => run nextB updateB primitive (m*fuel) (start ω)
    have hc := measurable_batch_callbacks m hm (0 : En) next update plan decode
      hnext hu hplan hd
    have hNB : Measurable nextB := by
      convert hc.1 using 1
      funext z
      cases h : next z.1 <;> simp only [nextB, h]
    have hUB : Measurable (fun p : Micro × Primitive × En => updateB p.1 p.2.1 p.2.2) := by
      convert hc.2 using 1
      funext p
      cases h : next p.1.1 with
      | inl x => simp only [updateB, h]
      | inr x => simp only [updateB, h]; rfl
    have hdir := measurable_simulation_joint_law_and_cost μ next update target target
      (fun _ a => a) initial hnext hu htarget measurable_snd hi (fun _ => rfl) fuel
    rcases hdir with ⟨_, hMD, _, _, hprob, hID, _, _⟩
    have hbat := measurable_simulation_joint_law_and_cost μ nextB updateB primitive primitive
      (fun _ a => a) start hNB hUB hprimitive measurable_snd hstart (fun _ => rfl) (m*fuel)
    have hMB : Measurable batch := hbat.2.1
    have hp (ω : Ω) := batch_simulation_with_trace_and_label_costs
      m hm (0 : En) next update primitive target plan decode
      (fun p : Primitive => p.1)
      (fun i : Fin m => (finProdFinEquiv.symm i : Fin k × Fin 2).1)
      hcorrect (fun _ _ => rfl) fuel (initial ω)
    have hpoint (ω : Ω) : readback (batch ω) = direct ω ∧
        (batch ω).2 = m * (direct ω).2 ∧ (direct ω).2 ≤ fuel ∧
        (batch ω).2 ≤ m*fuel ∧
        ∀ j : Fin k, blockCalls j (batch ω) = 2 * (direct ω).2 ∧
          blockCalls j (batch ω) ≤ 2*fuel ∧ blockCalls j (batch ω) < n := by
      have hh : readback (batch ω) = direct ω ∧
        (batch ω).2 = m*(direct ω).2 ∧ (direct ω).2 ≤ fuel ∧
        (∀ j : Fin k, blockCalls j (batch ω) =
          (List.ofFn (fun i : Fin m => (finProdFinEquiv.symm i : Fin k × Fin 2).1)).countP
            (fun v => decide (v=j)) * (direct ω).2) := by
        have he := hp ω
        dsimp only at he
        generalize hRun : run _ _ primitive (m*fuel) _ = result at he
        have hResult : result = batch ω := by
          rw [← hRun]
          unfold batch
          congr 1
          · funext z
            cases h : next z.1 <;> simp only [nextB, h]
          · funext z p a
            cases h : next z.1 with
            | inl x => simp only [updateB, h]
            | inr x => simp only [updateB, h]; rfl
        rw [hResult] at he
        exact he
      rcases hh with ⟨hr,hc,hcap,hblocks⟩
      have htotal : (batch ω).2 ≤ m*fuel := by
        change (batch ω).2 = m*(direct ω).2 at hc
        rw [hc]
        exact Nat.mul_le_mul_left m hcap
      refine ⟨hr,hc,hcap,htotal,?_⟩
      intro j
      have hb : blockCalls j (batch ω) = 2*(direct ω).2 := by
        have hh := hblocks j
        rw [block_slot_count k j] at hh
        exact hh
      have hbc : blockCalls j (batch ω) ≤ 2*fuel := by
        rw [hb]
        exact Nat.mul_le_mul_left 2 hcap
      exact ⟨hb,hbc,lt_of_le_of_lt hbc hsmall⟩
    have hlaw : μ.map (fun ω => readback (batch ω)) = μ.map direct :=
      congrArg (fun g => μ.map g) (funext fun ω => (hpoint ω).1)
    have htotal : (fun ω => ((batch ω).2 : ℝ)) =
        fun ω => (m : ℝ) * ((direct ω).2 : ℝ) := by
      funext ω
      rw [(hpoint ω).2.1, Nat.cast_mul]
    have hIB : Integrable (fun ω => ((batch ω).2 : ℝ)) μ := by
      rw [htotal]
      exact hID.const_mul (m : ℝ)
    have hmean : (∫ ω, ((batch ω).2 : ℝ) ∂μ) ≤ (m*fuel : ℕ) := by
      have h := integral_mono hIB (integrable_const ((m*fuel : ℕ) : ℝ))
        (fun ω => Nat.cast_le.mpr (hpoint ω).2.2.2.1)
      simpa using h
    have hblocks (j : Fin k) :
        Integrable (fun ω => (blockCalls j (batch ω) : ℝ)) μ ∧
        (∫ ω, (blockCalls j (batch ω) : ℝ) ∂μ) =
          2 * (∫ ω, ((direct ω).2 : ℝ) ∂μ) ∧
        (∫ ω, (blockCalls j (batch ω) : ℝ) ∂μ) ≤ (2*fuel : ℕ) := by
      have he : (fun ω => (blockCalls j (batch ω) : ℝ)) =
          fun ω => (2 : ℝ) * ((direct ω).2 : ℝ) := by
        funext ω
        rw [((hpoint ω).2.2.2.2 j).1, Nat.cast_mul, Nat.cast_ofNat]
      have hi : Integrable (fun ω => (blockCalls j (batch ω) : ℝ)) μ := by
        rw [he]
        exact hID.const_mul 2
      refine ⟨hi, ?_, ?_⟩
      · rw [he, integral_const_mul]
      · have h := integral_mono hi (integrable_const ((2*fuel : ℕ) : ℝ))
          (fun ω => Nat.cast_le.mpr ((hpoint ω).2.2.2.2 j).2.1)
        simpa using h
    refine ⟨hUB,hMB,hMD,hpoint,hlaw,hprob,hID,hIB,?_,hmean,hblocks⟩
    rw [htotal, integral_const_mul]
  have hFO := policy (ℝ × Ed) updateFO fo decodeFO huFO hfo hdecodeFO hdecode
  have hGrad := policy Ed updateGrad grad reconstruct huGrad hgrad hrec.measurable hdecodeGrad
  rcases hFO with ⟨huF,hf1,hf2,hf3,hf4,hf5,hf6,hf7,hf8,hf9,hf10⟩
  rcases hGrad with ⟨huG,hg1,hg2,hg3,hg4,hg5,hg6,hg7,hg8,hg9,hg10⟩
  have hNB : Measurable nextB := by
    convert hcallbacksFO.1 using 1
    funext z
    cases h : next z.1 <;> simp only [nextB, h]
  exact ⟨hprimitive,hNB,huF,huG,hstart,
    hf1,hf2,hf3,hf4,hf5,hf6,hf7,hf8,hf9,hf10,
    hg1,hg2,hg3,hg4,hg5,hg6,hg7,hg8,hg9,hg10⟩

end AutoSamplingTheory.Tests.GaussianComplexityBatchedPrimitiveSimulation
