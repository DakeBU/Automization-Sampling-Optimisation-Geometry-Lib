"""Bounded reuse search; not a proof certificate or a proof-search attempt."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "retrieval90"
OUT.mkdir(exist_ok=False)

def desc(p):
    b = p.read_bytes()
    return {"path": str(p), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

queries = [
    ("local-actual", ["rg", "-n", "actual_finite_history|actual_conditional_next_wait|Fin.snoc|history.*append", "AutoSamplingTheory/ExampleCases/ProximalBPS"]),
    ("frontier", ["rg", "-l", "actual_finite_history_extension|ActualFiniteHistoryExtension|actual next-history extension", "research-wiki/frontier-cells"]),
    ("tuple", ["rg", "-n", "def snoc|theorem snoc_castSucc|theorem snoc_last|snoc_init_self|lastCases", ".lake/packages/mathlib/Mathlib/Data/Fin/Tuple/Basic.lean"]),
    ("measurable-tuple", ["rg", "-n", "measurable_pi_iff|measurable_pi_lambda|snoc|lastCases", ".lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean"]),
    ("measure-map", ["rg", "-n", "theorem map_congr|theorem map_map|map_apply_of_aemeasurable|map_apply|map_univ", ".lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean"]),
    ("restrict-ae", ["rg", "-n", "ae_restrict_mem|ae_restrict_iff|ae_restrict_of_forall_mem", ".lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean"]),
    ("lintegral", ["rg", "-n", "lintegral_congr_ae|setLIntegral_congr_fun", ".lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Basic.lean"]),
]
results = []
for label, cmd in queries:
    q = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    assert q.returncode in (0, 1), (cmd, q.stderr)
    log = OUT / (label + ".log")
    log.write_bytes(q.stdout)
    results.append({"label": label, "command": cmd, "exit_code": q.returncode,
                    "output": desc(log)})
inputs = [
    "lean-toolchain", "lake-manifest.json",
    "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean",
    "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean",
    "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean",
    "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean",
    "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean",
    "AutoSamplingTheory/TechnicalLemmas/Probability.lean",
    "AutoSamplingTheory/TechnicalLemmas/SDE.lean",
    "research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel.md",
    "research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.md",
    ".lake/packages/mathlib/Mathlib/Data/Fin/Tuple/Basic.lean",
    ".lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean",
    ".lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean",
    ".lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean",
    ".lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Basic.lean",
]
present, absent = [], []
for name in inputs:
    p = ROOT / name
    if p.is_file():
        present.append(desc(p))
    else:
        absent.append(name)
record = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "queries": results, "exact_inputs": present, "not_at_guessed_path": absent,
    "chosen_existing_producers": ["ActualConditionalNextWaitDensity.actual_conditional_next_wait_density",
        "ActualFiniteHistoryTailLaw.actual_finite_history_tail_law",
        "ActualHarmonicFlow.actual_harmonic_flow_laws",
        "ActualBounceRate.actual_bounce_rate_energy_laws"],
    "fixed_mathlib": "db584cd6d46c92f209a44c0f1c829460d327499d / Lean4.33.0",
    "compatible_upstream": "Generic finite tuple operations, Borel products, measurable pushforward composition and ae restriction are supplied by pinned Mathlib; no upstream port, dependency or toolchain change is needed.",
    "new_background_copy": False,
    "consumer": "Actual full next-history is necessary for iterating the verified finite-density factor within S87-I5/G86-11. Complete ordered absolute-time and final-survival assembly remain open.",
    "not_AND_parents": ["survival88", "a separate no-atom theorem", "the alternative direct87/86 density reconstruction"],
    "process_memory": "Reuse unchanged exact process-memory audit from retrieval89; no clock-density process instruction applicable.",
    "proof_credit": False,
}
(HERE / "retrieval90.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"queries": len(results), "exact_inputs": len(present), "not_at_guessed_path": absent}))
