from pathlib import Path
import hashlib,json
r=Path(__file__).parent;seal=json.loads((r/'root.statement-seal85.json').read_bytes())
header=Path(seal['header']['path']);assert hashlib.sha256(header.read_bytes()).hexdigest()==seal['header']['RAW_sha256']
assert seal['proof_BODY_created'] is False
target=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean');assert not target.exists()
s=header.read_text(encoding='utf8');tail='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel\n'
assert s.endswith(tail)
s=s[:-len(tail)].replace('Prospective statement85 only.','Actual finite-time probability-kernel interface.',1)
body='''

/-- Actual full-phase law with joint finite-time index, Dirac initialization and
bounded Borel expectation transfer. Probability fibers do not assert process
Markovness, restart, invariance or Chapman-Kolmogorov. -/
set_option maxHeartbeats 1600000 in
theorem actual_phase_transition_kernel
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_phase_transition_kernel_statement hα hαβ hV hH hη hβη := by
  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  obtain ⟨Z, hZM, harc, hfallback, hgood⟩ :=
    ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase
      hα hαβ hV hH hη hβη
  let A := ((E × E) × (E × E)) × ℝ≥0
  let F : A × (ℕ → ℝ) → E × E := fun a =>
    Z a.1.1.1.1 a.1.1.1.2 a.1.1.2 a.1.2 a.2
  have hFM : Measurable F := hZM.comp
    (measurable_fst.fst.prodMk (measurable_fst.snd.prodMk measurable_snd))
  have hzM (y xRef : E) (z₀ : E × E) (t : ℝ≥0) :
      Measurable (Z y xRef z₀ t) := hZM.comp
    ((measurable_const.prodMk measurable_const).prodMk
      (measurable_const.prodMk measurable_id))
  let Q : Kernel A (ℕ → ℝ) := Kernel.const A P
  let K : Kernel A (E × E) := (Kernel.id ×ₖ Q).map F
  have hK : IsMarkovKernel K := Kernel.IsMarkovKernel.map _ hFM
  have hfiber (y xRef : E) (z₀ : E × E) (t : ℝ≥0) :
      K (((y, xRef), z₀), t) = Measure.map (Z y xRef z₀ t) P := by
    dsimp only [K]
    rw [Kernel.map_apply _ hFM, Kernel.prod_apply, Kernel.id_apply,
      show Q (((y, xRef), z₀), t) = P from rfl,
      Measure.dirac_prod, Measure.map_map hFM (by fun_prop)]
    rfl
  refine ⟨Z, hZM, harc, hfallback, hgood, K, hK, hfiber, ?_, ?_, ?_⟩
  · intro y xRef z₀ t B hB
    rw [hfiber, Measure.map_apply (hzM y xRef z₀ t) hB]
  · intro y xRef z₀
    rw [hfiber]
    calc
      Measure.map (Z y xRef z₀ 0) P =
          Measure.map (fun _ : ℕ → ℝ => z₀) P :=
        Measure.map_congr ((hgood y xRef z₀).mono fun _ hs => hs.2)
      _ = Measure.dirac z₀ := by simp
  · intro y xRef z₀ t g hg M hM hbound
    letI : IsMarkovKernel K := hK
    have hIntK : Integrable g (K (((y, xRef), z₀), t)) :=
      Integrable.of_bound hg.aestronglyMeasurable M
        (Filter.Eventually.of_forall fun z => by simpa only [Real.norm_eq_abs] using hbound z)
    have hIntP : Integrable (fun sample => g (Z y xRef z₀ t sample)) P :=
      Integrable.of_bound (hg.comp (hzM y xRef z₀ t)).aestronglyMeasurable M
        (Filter.Eventually.of_forall fun sample => by
          simpa only [Real.norm_eq_abs] using hbound (Z y xRef z₀ t sample))
    refine ⟨hIntK, hIntP, ?_⟩
    rw [hfiber]
    exact integral_map (hzM y xRef z₀ t).aemeasurable hg.aestronglyMeasurable
'''
target.write_text(s+body+tail,encoding='utf8',newline='\n')
statement=lambda text:text.split('private def ',1)[1].split('\n\n/--',1)[0].rstrip()
assert statement(target.read_text(encoding='utf8'))==statement(header.read_text(encoding='utf8').split('\nend\n',1)[0])
(r/'implementation85.initial.json').write_text(json.dumps(dict(statement_seal_RAW_sha256=hashlib.sha256((r/'root.statement-seal85.json').read_bytes()).hexdigest(),module=target.as_posix(),source_RAW_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),private_Prop_exact=True,compiler_result='PENDING',independent_BODY_review='PENDING'),indent=2)+'\n',encoding='utf8',newline='\n')
print('85 BODY written only after StatementSeal; exact private Prop retained; focused compile pending')
