import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def artifact(name, data):
    return {
        "path": ".astis/decoder-48/" + name,
        "raw_sha256": sha(data),
        "lf_sha256": sha(data.replace(b"\r\n", b"\n")),
        "bytes": len(data),
    }

def encode(value):
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")

packet_bytes = (BASE / "packet0.json").read_bytes()
lease_bytes = (BASE / "lease.json").read_bytes()
packet = json.loads(packet_bytes)
lease = json.loads(lease_bytes)
assert lease["status"] == "OPEN", "Use only the original opening lease; do not overwrite a closed run."
assert not packet["non_disclosure"]["source_text_included"]
assert not lease["source_text_visible"]
assert sha(packet["lean"]["statement"].encode("utf-8")) == packet["lean"]["statement_sha256"]
for expected in lease["input_artifacts"]:
    if expected["path"] == ".astis/decoder-48/packet0.json":
        assert expected == artifact("packet0.json", packet_bytes)

text = """Let E be a finite-dimensional real inner-product space, equipped with its norm, Borel measurable structure, and canonical volume measure; the dimension may be zero. Let V : E → ℝ be twice continuously Fréchet differentiable. Let α and β be nonnegative real numbers with 0 < α ≤ β, and suppose that, for all x,a ∈ E,
α‖a‖² ≤ D²V(x)[a,a] ≤ β‖a‖².
Let η > 0 satisfy βη ≤ 1. Define μ to be the probability measure obtained by normalizing exp(-V(x)) against canonical volume. Let γ be the canonical centered Gaussian with identity covariance on E, and define J as the pushforward of μ ⊗ γ under (x,g) ↦ (x, x + √η g).
There exist measurable Markov kernels R,S from E to E such that R is a regular conditional kernel of the first coordinate X given the second coordinate Y of J, in the precise sense that R is a conditional kernel for the coordinate-swapped joint measure J.map(Prod.swap). For every y ∈ E, S(y) is the pushforward of R(y) under x ↦ 2x - y. Moreover, for every y ∈ E, S(y) is exactly the normalized tilt of canonical volume with log-weight
u ↦ -V((y+u)/2) - ‖y-u‖²/(8η).
These same kernels satisfy the following assertion for every globally smooth compactly supported real-valued function f on E. The function F_f(z) = ∫ f(u) S(z)(du) is Fréchet differentiable at every y ∈ E, and its genuine Riesz gradient obeys
‖∇F_f(y)‖² ≤ ((1/η - α)² / (4(α + 1/η))) Var_{S(y)}(f),
where Var_{S(y)}(f) = ∫ (f(u) - ∫ f(v) S(y)(dv))² S(y)(du)."""

result = dict(packet["output_contract"])
assert all(isinstance(v, str) or k == "source_text_visible" for k, v in result.items())
result.update({
    "reconstructed_theorem_text": text,
    "reconstructed_text_sha256": sha(text.encode("utf-8")),
    "objects": "E is a real inner-product space; V is a real potential; α,β are nonnegative curvature constants; η is a positive noise parameter; μ is the normalized volume tilt by -V; γ is stdGaussian E; J is the specified joint pushforward; R,S are produced measurable probability-transition kernels; f is a real smooth compactly supported test; F_f is its literal Bochner expectation under S; the gradient is the Riesz inverse of the actual Fréchet derivative; variance is the literal centered second-moment integral.",
    "domains": "E is any finite-dimensional real inner-product space, including dimension zero, with NormedAddCommGroup, InnerProductSpace ℝ, MeasurableSpace, and BorelSpace structures. V,f : E → ℝ; α,β : ℝ≥0; η : ℝ; x,a,y,u,z ∈ E. J is a measure on E × E. R,S : Kernel E E. All derivatives are over ℝ.",
    "quantifiers": "For every admissible E,V,α,β,η satisfying the displayed hypotheses, define μ and J, then there exist R,S. The Markov and disintegration properties hold for those kernels. Both reflection and normalized-density equalities hold for every y, not merely almost everywhere. For the same R,S, for every f : E → ℝ, if f is globally C∞ and compactly supported, then for every y ∈ E both differentiability and the gradient bound hold.",
    "assumptions": "Finite-dimensional real inner-product/Borel space E; V globally C² over ℝ; α,β nonnegative; 0 < α; α ≤ β; for every x,a the genuine Hessian quadratic form satisfies α‖a‖² ≤ D²V(x)[a,a] ≤ β‖a‖²; η > 0; βη ≤ 1. Only the final test-function assertion assumes f globally C∞ and HasCompactSupport. There are no assumed posterior kernels, covariance bounds, Poincaré certificates, differentiability certificates, or desired-bound certificates.",
    "conclusion": "Produce Markov kernels R,S with the actual swapped-J conditional disintegration for R; for all y, identify S(y) both as reflected R(y) and as the exact normalized volume tilt exp(-V((y+u)/2)-‖y-u‖²/(8η)); for every allowed f and every y prove actual DifferentiableAt of z ↦ ∫ f dS(z), and bound its squared gradient norm by (1/η-α)²/[4(α+1/η)] times its actual variance under S(y).",
    "scopes": "μ and J are local definitions determined by the initial data, preceding the existential kernels. R,S depend on the initial data and are chosen before f and y. IsCondKernel is tied to the literal coordinate-swapped J and thus to the literal Gaussian construction. The reflection and density outputs are pointwise in every y; the conditional-kernel condition retains its precise regular-disintegration semantics. The variance, expectation, and derivative in the final inequality all concern the same produced S. Differentiability is separately asserted at every y. No admission or source-fidelity verdict is reconstructed.",
    "constant_dependencies": "The exact displayed multiplier is (1/η-α)²/[4(α+1/η)], depending only on α and η. β constrains the Hessian and admissible η through βη ≤ 1, but does not appear in that multiplier. The density constants are exactly 1/2 in the midpoint and 1/(8η) in the quadratic term. No dimension-dependent constant occurs. The measures and kernels depend on E,V,η; the common kernels are independent of f.",
    "decoder": "Fresh independent source-blind statement decoder. Read only packet0.json and the original opening lease.json. Reconstructed from the anonymized Lean statement and its approved definition context. No source text, theorem implementation, Tests, review, history, or compiler was accessed; no admission granted.",
    "source_text_visible": False,
})

inputs = [artifact("packet0.json", packet_bytes), artifact("lease.json", lease_bytes)]
final_leases = {"read_lease": "CLOSED", "write_lease": "CLOSED", "python_lease": "CLOSED", "compiler_lease": "CLOSED"}
execution_payload = {
    "schema_version": 1,
    "task": "blind-theorem-reconstruction",
    "packet_id": packet["packet_id"],
    "input_artifacts": inputs,
    "statement_sha256": packet["lean"]["statement_sha256"],
    "reconstruction": {k: v for k, v in result.items() if k != "decoder_run_sha256"},
    "method": "Read approved packet and opening lease; validate literal statement/input hashes; reconstruct the quantified theorem; close file handles; write result and closed lease; bind their exact bytes in the run receipt; exit Python. No compiler or other input access.",
    "run_recipe": "From E:\\Samplinglib, execute: python .astis/decoder-48/decode.py (once, while lease.json is OPEN).",
    "final_leases": final_leases,
    "compiler_started": False,
    "source_text_visible": False,
}
canonical_payload = json.dumps(execution_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
run_hash = sha(canonical_payload)
result["decoder_run_sha256"] = run_hash
assert list(result) == list(packet["output_contract"])
assert all(type(result[k]) is type(v) for k, v in packet["output_contract"].items())
result_bytes = encode(result)
(BASE / "result0.json").write_bytes(result_bytes)
result_artifact = artifact("result0.json", result_bytes)

lease.update({
    "status": "CLOSED",
    **final_leases,
    "compiler_started": False,
    "source_text_visible": False,
    "original_opening_lease": inputs[1],
    "output_artifacts": [result_artifact],
    "decoder_run_sha256": run_hash,
    "closure": "All input and output file handles close synchronously; Python finishes after writing this lease and the run receipt. Compiler never started. Original opening-lease snapshot preserved without access or modification.",
})
closed_lease_bytes = encode(lease)
(BASE / "lease.json").write_bytes(closed_lease_bytes)
run = {
    "schema_version": 1,
    "status": "CLOSED",
    "execution_payload": execution_payload,
    "execution_payload_hash_rule": "SHA256 of UTF-8 json.dumps(execution_payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False); payload excludes output/run references and decoder_run_sha256.",
    "decoder_run_sha256": run_hash,
    "input_artifacts": inputs,
    "output_artifacts": [result_artifact, artifact("lease.json", closed_lease_bytes)],
    "final_leases": final_leases,
    "source_text_visible": False,
    "compiler_started": False,
    "run_recipe": execution_payload["run_recipe"],
}
run_bytes = encode(run)
(BASE / "run.json").write_bytes(run_bytes)
print(json.dumps({"decoder_run_sha256": run_hash, "reconstructed_text_sha256": result["reconstructed_text_sha256"], "outputs": [result_artifact, artifact("lease.json", closed_lease_bytes), artifact("run.json", run_bytes)], "final_leases": final_leases}, ensure_ascii=False))
