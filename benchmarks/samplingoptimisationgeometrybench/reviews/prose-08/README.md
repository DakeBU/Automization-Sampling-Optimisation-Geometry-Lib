# Chewi Optimization Exercise 3.1 — editorial admission

`sogb-030` is the actual three-part exercise across printed/PDF pp. 22–23
of the existing hash-pinned v1 edition. The catalog contains our own
mathematical restatement and solution. The source PDF and page renders are
not included. The existing publication binds each requested part to a
distinct owned declaration in `ConvexSmoothGradient`.

The [first review](source-review.json) accepted the mathematics, primary-source
correspondence and owned-answer coverage, but required a rubric repair.
The [second, independent review](repair-review.json) accepted only the
[exact scoring change](packets/repair-input.json): equivalent proofs of
the tilt and endpoint steps receive credit, and cancellation is not mandatory.
The [original input](packets/prose-input.json) is immutable. The zero-modulus
branch is meaningful for (3.5) and the Lipschitz bound, not the reciprocal
expression (3.4). No Hessian or gradient-Lipschitz premise was added.

Editorial admission is recomputed from the pinned packets. A separate
Lean 4.33.0 trusted run checked all 13 existing fixed references and
5 named owned exercise answers across Exercises 3.1 and 3.2. The new
item remains an NL-only public development question with optional owned
Lean, not a new declaration, an aligned Lean reconstruction, a held-out
task or empirical calibration. Registry credit is unchanged.

Local desktop and 412px mobile readback checked both rendered proof
displays, the folded syntax-highlighted Lean, exact copy-versus-HTTP
source bytes, the two PDF page links and the three actual compiled graph
nodes. The long trial-step inequality is split only in the HTML display;
the reviewed math and exports are unchanged. The full local browser
suite stopped at Playwright's cancelled file download on this Windows
machine; the focused readback did not certify the browser file-save gate.
