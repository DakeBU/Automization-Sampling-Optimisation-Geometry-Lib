# Independent n=0 integral-base review92

Accepted the frozen Base92.lean fragment for every horizon T>=0, including0, and every measurable ENNReal test of the complete initial history. All22 outer definitions exactly match the seal; no probability or density provider was added.

The proof derives H0=K0=live(0,z0), B0=univ, Delta0=univ and q0=1. It derives m0(univ)=1 from map/comap, restricted volume and the empty finite product. The rewrite of Delta0 to univ is restricted to the right-hand measure expression; the original simplex subtype remains the domain of m0. Canonical P normalization uses only UnitExponentialProduct.unit_exponential_product_laws.1. Both integrals reduce to F(initial history), including when that value is infinity.

Fresh pinned Lean compilation and full type/axiom inspection passed (exit0,11.109s), using only propext, Classical.choice and Quot.sound. No repairs needed. The successor step, all-n density law and measure equality remain open. No canonical or production changes were made.
