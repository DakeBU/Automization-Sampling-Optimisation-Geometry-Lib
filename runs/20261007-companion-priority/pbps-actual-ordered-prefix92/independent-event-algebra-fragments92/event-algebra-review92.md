# Independent event/algebra fragments92 review

Accepted the frozen Events92 and Algebra92 private fragments. Fresh pinned Lean compilation, ten full types and all axiom lists passed; every theorem uses only propext, Classical.choice and Quot.sound.

The event equality exactly splits the extended guard into the old guard and both live records, strict time increase and strict cutoff. The old-live conjunct is explicitly derived from the old guard. This is pointwise for arbitrary record sequences, including the relevant zero-clock/stopped boundaries, without claiming a raw counting equivalence.

Algebra retains the previously reviewed recursion body exactly. timedHistory_snoc preserves every old tagged record, and its final time addition uses the explicit last>=0 and u>=last conditions. ordered_last_nonneg includes n0. weight_snoc_ofReal correctly needs only nonnegativity of the old real weight.

Generic record/step/factor and support/nonnegativity premises remain private ingredients to instantiate from the literal actual model and Geometry. Main density induction and all-n law are still open. No canonical or production changes were made.
