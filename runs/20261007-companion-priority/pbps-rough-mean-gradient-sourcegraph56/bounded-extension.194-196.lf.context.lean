theorem extendOfNorm_eq (h_dense : DenseRange e) (h_norm : ∃ C, ∀ x, ‖f x‖ ≤ C * ‖e x‖)
    (x : E) : f.extendOfNorm e (e x) = f x 