# Independent raw-source reconstruction, phase 1

The exact source is arXiv:2610.20492v1, raw SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
This baseline was written before seeing any candidate statement, code, decoder,
seal, publication payload, prior verdict, or canonical reviewer packet.

For the source hard family, fix κ≥4, 3≤n≤d and k=floor(d/n), and choose
O_j∈O(n). Let r=d-kn. The actual precision is the block diagonal matrix with
blocks A_j=((κ+1)/2)I-((κ-1)/4)(O_j+O_jᵀ), followed by I_r.
For any x=(x_1,…,x_k,z), obtain F_j=O_j x_j and I_j=O_jᵀ x_j from two
primitive calls per block. Then

    g_j=((κ+1)/2)x_j-((κ-1)/4)(F_j+I_j)=A_j x_j,
    g=(g_1,…,g_k,z)=A_boldO x=∇f_(A_boldO)(x),
    v=(1/2)〈x,g〉=f_(A_boldO)(x).

Thus (v,g) is exactly the Section 2 first-order response for the actual
Section 3 E4/E5 quadratic. The residual requires no primitive call. If r=0,
the source omits that block; its zero-dimensional encoding has zero contribution.
The pointwise count is at most two calls per block, hence 2k across all blocks.

The coefficients and value factor are exact. No probability statement or
nonzero-vector restriction occurs. The source parameter restrictions and
orthogonality identify the family, but the algebraic identities extend beyond
some of those restrictions. The source's ambient 2T<n is needed downstream;
it is not used in the pointwise equalities. This review does not establish
adaptive transcript simulation, Borel measurability, indistinguishability,
TV separation, or any full lower bound.

The authoritative detailed baseline is `source-semantic-slots.json`.
Exact source byte slices and offsets are in `source-excerpt-index.json`.
Readable text derivatives are provided only for inspection, not as raw evidence.
