from pathlib import Path
import copy
import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))
import astis_publication as pub
import astis_semantic_roundtrip as rt

def load(p):
    return json.loads(p.read_bytes())

def sha(b):
    return hashlib.sha256(b).hexdigest()

def pin(p):
    return {"path": p.relative_to(ROOT).as_posix(), "raw_sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}

def save(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")

def fresh(p, obj):
    assert not p.exists(), p
    save(p, obj)

claim = load(RUN / "claim.json")
decl, file, cid = claim["target_declarations"][0], claim["proposed_files"][0], claim["frontier_cell"]
module = ROOT / file
raw = module.read_bytes()
s = raw.decode("utf-8")
receipt = RUN / "leaf-build90/receipt.json"
assert load(receipt)["exit_code"] == 0 and load(receipt)["module_raw_sha256"] == sha(raw)
seal = load(RUN / "root.statement-seal90.json")
literal = s.split("private def ", 1)[1].split("\n\nset_option", 1)[0]
assert literal.strip() == seal["expanded_literal_Prop"].strip()
cellpath = ROOT / "research-wiki/frontier-cells" / (cid+".json")
cell = load(cellpath)
standing = load(ROOT / "website/content/publications/pbps-actual-finite-history-tail-law.json")["items"][0]["statement"].split("For every deterministic n≥0 define", 1)[0]
statement = standing + (
    "For every deterministic n≥0 let Hist_n=D^(Fin(n+1)), H_n(w)=(R_j(ε(w)))_(0≤j≤n), and μ_n=(H_n)_*P. "
    "Define W(live(T,z),e)=τ_z(max(e,0)), W(stopped,e)=0 and t(r,e)=real(untopD_0 W(r,e)). "
    "Define ρ(live(T,z),s)=ofReal[λ_r(Φ_s z)exp(−Λ_z(max(s,0)))] and ρ(stopped,s)=0. "
    "Write A_n(h,s) for the complete history obtained by preserving every old coordinate h_j and appending "
    "live(T+max(s,0),S_rΦ_s z) when h_n=live(T,z), and appending stopped when h_n=stopped. "
    "Put L_n(h,s)=(A_n(h,s),s). Negative real times use the displayed raw-real harmonic flow with a clipped cumulative increment; "
    "this and the stopped branch are auxiliary totalizations, with actual positive finite jump identification only on the guard below. "
    "H_(n+1), A_n and L_n are Borel, and A_n(h,s)_j=h_j for every old index0≤j≤n and every abstract(h,s). "
    "For every fixed Borel d:Hist_n→[0,∞), each value finite but with no uniform bound, define "
    "D_d(h,s)=1_{0<s<d(h)}ρ(h_n,s), B_d={w:0<W(R_n(ε(w)),w_n)<d(H_n(w))}, "
    "X_n(w)=(H_n(w),t(R_n(ε(w)),w_n)), Y_n(w)=(H_(n+1)(w),t(R_n(ε(w)),w_n)) "
    "and ν_d=D_d(μ_n⊗real Lebesgue). B_d and Y_n are Borel. For every w∈B_d, "
    "H_(n+1)(w)=A_n(X_n(w)), preserving the actual old records and appending exactly the actual cumulative next time and post-bounce state. "
    "The actual restricted laws satisfy (Y_n)_*(P|B_d)=(L_n)_*ν_d and (H_(n+1))_*(P|B_d)=(A_n)_*ν_d, "
    "and ((L_n)_*ν_d)(Hist_(n+1)×ℝ)≤1. These are restricted finite-component laws; no unrestricted next-history law is asserted. "
    "For every jointly Borel F:Hist_(n+1)×ℝ→[0,∞], the function h↦∫_ℝF(L_n(h,s))D_d(h,s)ds is Borel. "
    "For every Borel A⊆Hist_n, ∫_{B_d∩{H_n∈A}}F(Y_n(w))P(dw)=∫_A[∫_ℝF(L_n(h,s))D_d(h,s)ds]μ_n(dh). "
    "No boundedness/integrability hypothesis on F, positive μ_n(A), normalized conditioning, constructor-law or measurability provider is assumed. "
    "The cases n=0, d=0, null A, stopped/infinite waits, zero hazard/normal, rank zero and unrealizable histories are included; infinite waits and zero/cutoff endpoints fail the strict guard, without an atom-equivalence assertion. "
    "This is attributed ASTIS completion of one actual complete-history extension ingredient implicit in Appendix A.1(A.7), "
    "using the already verified conditional finite-density law. Ordered absolute-time iteration, final survival/path-factor assembly, full(A.7), "
    "physical-time residual restart/Markovness, global conclusions, implementation/error/unbounded cost/main/composition/wholepaper/Goal remain OPEN. "
    "Survival88 and a separate no-atom theorem are not proof prerequisites."
)
assumptions = [
    "E is a finite-dimensional real inner-product space with its Borel structure, including rank zero; V:E→ℝ is C².",
    "The six original analytic hypotheses are α>0, α≤β, V∈C², α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for every x,v, η>0 and βη≤1, with α,β≥0.",
    "y,r,z₀ and deterministic depth n are universally quantified. The actual stopped recursion and raw iid Exp1 product P are literal definitions.",
    "d:Hist_n→NNReal is any fixed Borel finite-valued cutoff, possibly unbounded across histories; F:Hist_(n+1)×ℝ→ENNReal is any jointly Borel test, and A is any Borel old-history event, including null events.",
    "Every history/append/lift measurability fact, actual guarded constructor identity and transported law is a conclusion, not an input premise. The strict finite guard is never normalized."
]
formulae = [
    r"A_n(h,s)=\operatorname{snoc}\!\left(h,\begin{cases}\operatorname{live}(T+s,S_r\Phi_s z),&h_n=\operatorname{live}(T,z),\ s>0,\\\mathrm{stopped},&h_n=\mathrm{stopped},\end{cases}\right)\quad L_n(h,s)=(A_n(h,s),s).",
    r"B_d=\{0<W_n<d(H_n)\},\quad D_d(h,s)=\mathbf1_{\{0<s<d(h)\}}\rho(h_n,s),\quad \nu_d=D_d(\mu_n\otimes ds).",
    r"w\in B_d\ \Longrightarrow\ H_{n+1}(w)=A_n(H_n(w),t_n(w)),\quad A_n(h,s)_j=h_j\ (0\le j\le n).",
    r"(Y_n)_*(P|_{B_d})=(L_n)_*\nu_d,\qquad(H_{n+1})_*(P|_{B_d})=(A_n)_*\nu_d,\qquad((L_n)_*\nu_d)(\mathrm{univ})\le1.",
    r"\int_{B_d\cap\{H_n\in A\}}F(Y_n)\,dP=\int_A\left[\int_{\mathbb R}F(L_n(h,s))D_d(h,s)\,ds\right]\mu_n(dh)."
]
body = s.index(":= by\n", s.index("theorem actual_finite_history_extension"))+len(":= by\n")

def step(title, text, formula, start, end):
    a = s.index(start, body)
    b = s.index(end, a)
    code = s[a:b]
    return {"title": title, "text": text, "formula": formula, "lean": code,
            "detail": "Exact contiguous compiled BODY region; no proof ingredient is a supplied source premise.",
            "lean_source_region": {"path": file, "source_raw_sha256": sha(raw),
                "start_line": s[:a].count("\n")+1, "end_line": s[:b].count("\n"),
                "exact_code_raw_sha256": sha(code.encode())}}

steps = [
    step("Keep the actual model and complete next history",
         "Retain all14 literal model/input/observer definitions. Consume the verified conditional density law, finite-history Borel law and actual harmonic flow/reflection producers under the same six source hypotheses. Fix n,y,r,z₀. Define the old and next complete histories, append A_n and paired lift L_n. The append uses Fin.snoc, so it retains every earlier record; its last entry is the literal cumulative-time and reflected-flow update. Its negative-time and stopped branches are declared auxiliary totalizations, not positive finite jump laws.",
         formulae[0], "  classical\n", "  -- Borel actual histories"),
    step("Prove the complete append and next history are Borel",
         "The verified actual-history theorem at n+1 gives Borel H_(n+1), including the integrated-hazard/threshold-crossing/finite-recursion ingredients already proved there. For the append update, distribute the live/stopped record sum over real time. On live records the actual harmonic flow is jointly continuous/Borel and the zero-safe reflection is Borel; adding max(s,0) to the cumulative time is Borel. The stopped branch is constant. For every next-history coordinate, split into the new last entry and an old castSucc entry. These are respectively the Borel update and an old-history projection, proving Borel A_n. Pairing with s gives Borel L_n. Fin.snoc_castSucc proves exact preservation of every old entry for all abstract histories and real times.",
         r"H_{n+1},\ A_n,\ L_n\ \text{are Borel};\qquad A_n(h,s)_j=h_j\quad(0\le j\le n).",
         "  -- Borel actual histories", "  intro d hd\n"),
    step("Reuse the exact strict finite-density component",
         "Fix any Borel finite-valued d, with no uniform bound. Define μ_n,D_d,B_d,X_n,Y_n and ν_d literally. Producer89 supplies Borel B_d and X_n, the exact restricted law (X_n)_*(P|B_d)=ν_d, ν_d mass≤1, and all nonnegative joint tests on old histories. Combining Borel H_(n+1) with the real-time projection of X_n gives Borel Y_n. No density, independence, finite wait or measurability is introduced as a new premise.",
         formulae[1], "  intro d hd\n", "  -- The positive finite guard"),
    step("Identify the actual full recursion on the finite guard",
         "Take w∈B_d. If its current record is stopped then W_n=0 contradicts the positive guard. For a live record (T,z), τ_z(ε_n)=∞ contradicts the finite upper bound, so the actual next branch is live. Split the next finite history into its final index and the earlier indices. Earlier entries are unchanged by definition. At the final index, unfold Nat.rec once: the source next record is live(T+untopD₀τ,S_rΦ_(real untopD₀τ)z). The observed t_n is precisely real untopD₀τ and toNNReal(t_n)=untopD₀τ, so this equals the appended final record. Thus H_(n+1)=A_n∘X_n pointwise on B_d and Y_n=L_n∘X_n there. No endpoint-mass or restart argument is used.",
         formulae[2], "  -- The positive finite guard", "  -- Compose the exact89"),
    step("Transport the actual joint law and its marginal",
         "Pointwise equality on the Borel event gives equality almost everywhere under P restricted to B_d. Replace Y_n by L_n∘X_n in its pushforward, compose measurable pushforwards, and use the exact89 joint law to obtain (L_n)_*ν_d. Apply the same argument directly to H_(n+1)=A_n∘X_n for the marginal. Since L_n is measurable, the total mass of its pushforward is exactly ν_d(univ), hence≤1 by89. This is a subprobability mass bound, without renormalizing missing mass or claiming an unrestricted next-history distribution.",
         formulae[3], "  -- Compose the exact89", "  -- All joint ENNReal tests"),
    step("Integrate every joint test on every old-history event",
         "For jointly Borel ENNReal F on the extended history and relative time, F∘L_n is a jointly Borel test admitted by89. Its parameter integral is Borel, even when infinite. For any Borel old-history A, use the pointwise Y_n=L_n(X_n) identity throughout B_d∩{H_n∈A} to replace the actual integrand. Producer89 then gives the displayed unnormalized iterated integral. Null A, unbounded F and unbounded finite-valued d require no additional premise. The result closes one actual next-history extension step; ordered absolute-time iteration and the terminal survival factor remain separate.",
         formulae[4], "  -- All joint ENNReal tests", "\nend\n"),
]
assert "".join(x["lean"] for x in steps) == s[body:s.index("\nend\n", body)]
slug = "pbps-actual-finite-history-extension"
aid = "ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension"
title = "Actual PBPS one-step complete finite-history extension"
source = {"url": "https://arxiv.org/html/2609.06905v1#A1.E2", "edition": "arXiv2609.06905v1",
          "anchor": claim["source_anchor"], "wording_status": "faithful paraphrase",
          "attribution": "Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv2609.06905v1 Appendix A.1(A.1),(A.2),(A.7) and Appendix A.2. The explicit Borel complete-history append and its restricted next-history transport are attributed ASTIS completion of one iteration ingredient, not a printed standalone theorem. Full A.7 remains open."}
deltas = [
    {"source": "Actual fixed-reference recursion driven by independent Exp1 thresholds.",
     "lean": "Same six analytic conditions, literal actual stopped recursion and full deterministic-depth history.",
     "classification": "source-implicit", "reason": "Finite-dimensional inner-product realization includes rank zero; raw-real clipped thresholds give an explicit ambient null-set extension."},
    {"source": "Finite next-jump cumulative time and reflected harmonic state in A.2, with Borel recursion justified in Appendix A.2.",
     "lean": "Borel full-history append/lift, all-prefix preservation and actual guarded identification are derived internally.",
     "classification": "source-implicit", "reason": "No constructor-law or measurability provider premise. Raw-negative/stopped append branches are disclosed auxiliary totalizations."},
    {"source": "A.7 iterates jump density and state-update factors.",
     "lean": "Use verified89 strict joint density to derive actual restricted n+1-history joint/marginal laws and all ENNReal joint tests on every Borel old-history event.",
     "classification": "source-implicit", "reason": "d,F,A are admissible tests; missing mass remains unnormalized; no finite-wait/no-atom assumption or fabricated survival88 parent."},
    {"source": "Full ordered-time path formula and final survival/count partition.",
     "lean": "Only one actual full-history extension edge within S87-I5/G86-11; full A7 and global/main/Goal remain OPEN.",
     "classification": "unresolved", "reason": "No unrestricted next-history, whole iteration, terminal survival, physical-time restart or main/composition result follows."},
]
cell["evidence"]["focused_checks"] = [{"command": claim["focused_checks"][0],
    "result": "PASS exact sealed declaration; independent whole BODY/source admission pending.", "evidence": str(receipt)}]
save(cellpath, cell)
item = {"id": slug, "library": "pbps", "chapter": "pbps-01",
    "chapter_path": "example-cases/samplewiki/companions/proximal-bouncy-particle.html", "title": title,
    "source": source, "statement": statement, "assumptions": assumptions,
    "formulae": [{"label": "Actual complete-history extension "+str(i+1), "tex": f} for i, f in enumerate(formulae)],
    "obligations": [{"id": "actual-history-extension", "label": "Actual Borel complete-history append and strict finite next-history transport"},
                    {"id": "ordered-path-assembly", "label": "Full ordered-time iteration, final survival/path assembly and A7"}],
    "bindings": [{"declaration": decl, "cell": cid, "role": "proof-edge", "supports": ["actual-history-extension"],
        "audit_id": aid, "boundary": claim["truth_boundary"], "assumption_deltas": deltas}]}
for key in ["declaration_level", "statement_seal", "source_proof_coverage", "proof_digestion", "purification"]:
    item[key] = copy.deepcopy(cell[key])
unit = {"kind": "theorem", "declaration": decl, "title": title,
    "sources": [{"url": source["url"], "label": source["anchor"], "scope": claim["truth_boundary"]}],
    "tests": claim["focused_checks"], "assumptions": assumptions, "statement": statement,
    "formula": formulae[4], "boundary": claim["truth_boundary"], "steps": steps,
    "lean_statement": statement, "lean_proof": "; ".join(x["title"] for x in steps),
    "helpers": [decl+"_statement"], "astis_dependencies": cell["parents"],
    "mathlib_dependencies": ["Fin.snoc", "Fin.snoc_castSucc", "Fin.snoc_last", "Fin.lastCases",
        "MeasurableEquiv.sumProdDistrib", "Measurable.sumElim", "measurable_pi_lambda",
        "measurable_inl", "measurable_real_toNNReal", "Measure.map_map", "Measure.map_congr",
        "ae_restrict_of_forall_mem", "Measure.map_apply", "setLIntegral_congr_fun"]}
pp = ROOT / "website/content/publications" / (slug+".json")
lp = ROOT / "website/content/declaration_lessons" / (slug+".json")
fresh(pp, {"schema_version": 1, "items": [item]})
fresh(lp, {"schema_version": 1, "units": [unit]})
pub.inputs.cache_clear()
pub.load.cache_clear()
anon_statement = literal.removeprefix("actual_finite_history_extension_statement").replace(" : Prop :=", " :", 1)
anon = {"statement": anon_statement, "statement_sha256": sha(anon_statement.encode()), "compiled": True,
    "decoder_context": [
        "All displayed functions are literal definitions on a finite-dimensional real inner-product Borel space, including rank zero. fderiv is Frechet derivative, gradient the inner-product gradient, and ContDiff real2 twice continuous differentiability.",
        "expMeasure1 is the rate-one exponential law on real numbers; infinitePi is its canonical countable product. Real.toNNReal is max(x,0) represented as a nonnegative real.",
        "WithTop NNReal includes infinity. hittingAfter is the infimum of nonnegative entry times, infinity if none exists. untopD0 returns the finite value with default zero at infinity. Sum.inl/inr are distinct Borel tags; Unit is a singleton; products associate right.",
        "Fin(n+1) indexes0 through n. Fin.snoc h a appends a as the last coordinate and keeps all earlier coordinates. j.castSucc embeds an old Fin index in the larger tuple with the same value.",
        "Measurable is Borel measurability. Measure.map is pushforward, restrict is unnormalized measure restriction, withDensity multiplies the reference measure by the indicated nonnegative density. Real volume is Lebesgue measure.",
        "Real division is total with division by zero equal to zero. Interval integrals are real Bochner integrals; Nat.rec is the displayed finite recursion; ENNReal.ofReal embeds max(x,0). Nonnegative extended Lebesgue integrals need no integrability premise."
    ]}
fresh(RUN / "anonymous.lean-context90.json", anon)
lean = copy.deepcopy(anon)
lean.update(declaration=decl, file=file, formalizer="root-samplinglib-writer", compiler_evidence=str(receipt),
    statement_representation={"kind": "exact-literal-private-Prop-expansion",
        "actual_header": s[s.index("theorem actual_finite_history_extension"):body-len(":= by\n")],
        "private_definition": "private def "+literal, "expanded_header": "theorem actual_finite_history_extension"+anon_statement,
        "source_approved_overlay": str(RUN / "root.statement-seal90.json"),
        "kernel_header_and_literal_expansion_checked": True})
original = source["attribution"]+"\n"+statement+"\n"+source["anchor"]
audit = {"id": aid, "state": "draft",
    "source": {"source_id": "companion-domain:"+slug, "anchor": source["anchor"], "url": source["url"],
               "original_text": original, "text_sha256": sha(original.encode())},
    "lean": lean, "source_review": {"state": "pending"}, "repairs": [],
    "publication_binding_sha256": pub.binding_digest(item, item["bindings"][0], pub.inputs()),
    "publication_context": pub.review_context(item, item["bindings"][0], pub.inputs())}
fresh(RUN / "anonymous.decoder90.json", rt.decoder_packet(audit))
ap = ROOT / "research-wiki/semantic-roundtrip/audits" / (aid+".json")
fresh(ap, audit)
fresh(RUN / "publication-freeze90.json", {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "DRAFT_BEFORE_INDEPENDENT_BODY_REVIEW", "inputs": [pin(x) for x in [pp, lp, ap, cellpath]],
    "module": pin(module), "publication_binding_sha256": audit["publication_binding_sha256"],
    "steps": len(steps), "exhaustive_BODY_coverage": True, "PROVED_LOCAL": False, "VERIFIED": False})
pub.check_advance([decl], reviewed=False)
print("Draft90 publication admitted; six exhaustive exact BODY regions; independent acceptance pending.")
