# Prose round 11: a one-query quadratic oracle lower bound

`sogb-048` is an original L3 public-dev task. Choose two admissible quadratics
after the deterministic algorithm fixes its query. Unknown vertical shifts
make their exact values agree, and the curvatures make the derivatives agree.
A common output lies at least one quarter of the given radius from one of
the minimizers. Giving the optimal value in advance changes the model: one
reply then identifies the minimizer, including the zero-derivative case.

The [exact input](packets/prose-input.json) and
[independent review](source-review.json) record the math, assumptions and
rubric, including allowance for equivalent constructions and stronger lower
bounds. Chewi's first-order oracle and analytic regularization supply context,
not a numbered exercise or a matching formal oracle theorem. The existing
owned quadratic declaration was instantiated with a constant real base in a
local Lean 4.33.0 support probe. It supplies the analytic properties only.
Neither the oracle argument nor optimal-value recovery has an aligned Lean task.
The difficulty is editorial, not calibrated.
