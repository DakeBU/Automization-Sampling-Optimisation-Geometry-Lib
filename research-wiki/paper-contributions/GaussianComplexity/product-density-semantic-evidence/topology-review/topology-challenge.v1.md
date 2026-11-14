# Independent topology challenge, v1

The current source graph needs a bounded metadata repair before this review permits proof search. This is an incomplete review artifact, not a mathematical counterexample or a source correction. The sealed theorem interface is source-compatible and requires no new binder.

The raw source SHA is `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`; the reviewed seal SHA is `eb015980dd1ad6dcc1c7d23ae3e8b95350e108fc806a74345617e451dbb5f10b`, signature `c0d36b866977a6f04fd7a9e63d02541c02370acec456ba69833592bcbf2362fe`; graph v1 SHA is `4f3df3b3222793a288066d8326ad4176670b68ebe23c89274d7a567ab9f6331e` and inventory SHA is `7c5a2678317425b952a1271f37dad2eba509d4c90deb5c433042f3cd872b6126`.

The inventory covers all 349 items in its bounded source scope. An independent parser found no missing leaf paragraphs, displays, inline/display formulas or citation links, and no duplicate or unreasoned disposition. All 13 links match the raw source. The only raw formula-byte difference is harmless newline-to-space normalization in excluded query-complexity formula S2.E2.m1. Every substantive B.2.3 paragraph and display is represented. The upstream B.2.1/B.2.2 proofs have explicit exclusions, so this does not certify full separation-root closure.

The graph correctly directs the actual construction through Eq6 to Ex70, then onward to Ex71 and Ex72. Eq25 feeds the final Ex72 bound, not Ex70. The two residual-dimension cases remain OR routes; the final Ex72 row legitimately needs both affinity tensorization and Eq25. The source's actual Gaussian and actual mixture laws remain the named objects, and the seal makes no unsupported product/Pi maximum-norm isometry assertion.

Two records need repair:

1. Even counting `omitted_bridge(s)` as dependencies, the graph lists `source:S2.p1.1` and `source:S3.SS1.p1.1` as root ancestors without any dependency path to Ex70. The graph also names the `kn<d` and `kn=d` guards without an explicit source-implied arithmetic discharge from `k=floor(d/n)` and `n>=3`. Add the standing-context dependencies and the `kn<=d`, `r=d-kn=d%n`, exhaustive branch bridge internally.
2. The sealed `p` is an explicit precision-density formula and `pb` is its conditioned-Haar integral. The raw source instead names `p_O` and `p_b` by their actual Gaussian and mixture laws. The graph's existing product-density gap starts after those factors are actual densities. Add the separate standard Gaussian density and Haar-mean mixture representative identifications before the product-density bridge. They are proof ingredients, never new public hypotheses.

The all-case residual formula with the explicit `r=0 -> phi=1` conclusion faithfully realizes the source's two-case omission convention. Its unit-volume zero-dimensional Gaussian bridge remains an internal proof obligation. The actual Ex71 affinity equality and Ex72 separation remain later consumers and are not completion claims of this Ex70 seal.

The full seven-slot comparison, exact blockers and nonblocking notes are in `topology-challenge.v1.json`; independent mechanical results are in `independent-mechanical-check.v1.json`. This reviewer read no implementation Lean or extractor private rationale and changed no shared ledger or frontier. Preserve v1; re-review an exact v2 graph before lifting this gate.
