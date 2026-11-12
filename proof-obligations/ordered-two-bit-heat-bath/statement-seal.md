# Prospective seal: an invariant nonreversible ordered two-bit heat bath

Exact target and definitions: `sweep-interface.lean`, SHA-256
`da6671c4531427141269de12159f9e86b7796b157f640950e6728e45c3efea95`.
The file elaborated under Lean 4.33.0 before proof search. Independent
prospective reviewer `ordered_sweep_preflight` accepted the exact type,
the full-support conditional law, composition order, and singleton
flux calculation. This is not retrospective proof or Bench admission.

For the four points in lexicographic order, the target masses are
`(3,1,1,3)/8`; every fixed-coordinate fiber has mass 1/2. The first
step draws the first bit conditional on the second, the second step
draws the second bit conditional on the refreshed first. This is one
homogeneous Markov step per full sweep on the four-point space, not
the per-update time-inhomogeneous process or scan-position augmentation.
Both factors are actual reversible Markov kernels; their composition
is invariant and violates reversibility on singleton pair 00,01
(both transition probabilities 3/16; fluxes 9/128 versus 3/128).
No claim about other targets, mixing times, all scan orders, or any
named paper theorem is included.

Conceptual background only:
[Chen–Štefankovič–Vigoda v4 §1.3, PDF p. 5](https://arxiv.org/pdf/2307.13826v4#page=5)
for single-site conditional updates, and
[He–De Sa–Mitliagkas–Ré v1 §5, PDF p. 6](https://arxiv.org/pdf/1606.03432v1#page=6)
for the nonreversibility issue and the scan-position distinction.
Their arXiv grants are distribution licenses to arXiv, not downstream
reuse grants. No source wording, figure, or page is redistributed.
This original example uses literal conditional retention; it does
not alter or close the monograph's separate copy-index audit.

The production port puts the same Dirac expressions in local let bindings of
one public theorem. Its focused test replays the literal signature exactly.
