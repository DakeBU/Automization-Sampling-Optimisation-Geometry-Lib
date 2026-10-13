/-- The graph of a `LinearPMap` viewed as a submodule on `E × F`. -/
def graph [Module R F] (f : E →ₗ.[R] F) : Submodule R (E × F) :=
  f.toFun.graph.map (f.domain.subtype.prodMap (LinearMap.id : F →ₗ[R] F))

theorem mem_graph_iff' [Module R F] (f : E →ₗ.[R] F) {x : E × F} :
    x ∈ f.graph ↔ ∃ y : f.domain, (↑y, f y) = x := by simp [graph]

@[simp, grind =]
theorem mem_graph_iff [Module R F] (f : E →ₗ.[R] F) {x : E × F} :
    x ∈ f.graph ↔ ∃ y : f.domain, (↑y : E) = x.1 ∧ f y = x.2 := by
  cases x
  simp_rw [mem_graph_iff', Prod.mk_inj]
