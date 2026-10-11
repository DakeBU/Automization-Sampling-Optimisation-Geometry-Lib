# Independent subtype-integral fragment review92

Accepted snocPrefix and subtype_simplex_lintegral_snoc in the frozen SubtypeCoordinates92.lean. The previously reviewed coordinate body is retained exactly. Fresh pinned Lean type/axiom checking passed (exit0,9.234s), with only propext, Classical.choice and Quot.sound.

The arbitrary measurable ENNReal test remains defined on the enlarged simplex subtype. Its measurable ambient extension agrees pointwise there, and the proof uses that extension only under the relevant restricted/comap measures. Every nested snocPrefix point lies in the enlarged simplex, so values outside it do not influence the result. Outer and inner subtype domains and volume dimensions are correct, including n0, T0, empty simplexes and infinite-valued tests.

This closes the generic subtype coordinate-integral adapter identified in the prior review. The private measurable-set premises must be supplied by Geometry. Concrete density/test instantiation and the actual all-n probability law remain open. No canonical or production file was changed.
