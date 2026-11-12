# Exact local proof-body occurrences

The [trusted probe](proof-occurrences.lean) ran under Lean 4.33.0 on the
module with SHA-256
de2def31c3143fd10544e3e5965da8196a35f5950dbcfebe5921fffb0d9bf49d:

    lake env lean runs/20261112-chewi-opt-exercise-4-1/proof-occurrences.lean

It traversed 72 owner-local constants, including generated constants.
It observed these three external ASTIS names in the traversed proof bodies:

- Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt
- Gradient.fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt
- StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound

The probe starts from the exact compiled declaration and follows
owner-local private constants only. It records proof-term occurrences
through that bounded closure, not direct calls by the public theorem,
mathematical necessity, a complete transitive graph, or a new graph QA.
