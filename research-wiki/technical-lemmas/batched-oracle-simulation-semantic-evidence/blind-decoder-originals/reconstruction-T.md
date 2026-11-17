# Reconstruction of packet T

Decoder: Codex independent source-blind mathematical decoder `/root/neutral_decode_c19`.
Source text visible: **false**. This reconstruction uses only `input-T.json` and its enclosed definition context; no source identity, source text, proof, or external definition was consulted.

## 1. Objects

Let `d,n ∈ ℕ` satisfy `3 ≤ n ≤ d`, and let `κ ∈ ℝ` satisfy `κ ≥ 4`. Put

`E_d = ℝ^d`, `E_n = ℝ^n`, `k = d div n`, `r = d mod n`, and `m = k·2`.

The Euclidean spaces are indexed by `Fin(d)` and `Fin(n)`. The divisions and remainder defining `k,r` are natural-number operations. In particular `k≥1`, so `m>0` and slot zero belongs to `Fin(m)`.

Let `S` and `Ω` be arbitrary types in their respective universes, each with a supplied sigma algebra. Let `μ` be a probability measure on `Ω`. Supply maps

`next : S → E_d ⊕ E_d`,

`updateFO : S × E_d × (ℝ × E_d) → S`,

`updateGrad : S × E_d × E_d → S`,

and `initial : Ω → S`.

In `next`, `inl(x)` denotes a terminal result, while `inr(x)` denotes a query; these branches have the same vector domain but retain distinct tags. The two update maps accept, respectively, a scalar/vector answer and a vector-only answer. They are arbitrary supplied maps and need not generate the same state evolution.

The other universal data are an arbitrary natural-number fuel `t` satisfying `2·t<n`, and a family

`O_j ∈ O(n),  j ∈ Fin(k)`.

Here `O(n)` is the full real orthogonal group, with no determinant restriction and no probability distribution imposed on these matrices.

## 2. Domains, coordinates, and measurable structures

Use the Borel sigma algebras on `E_d` and `E_n`. Equip `Option(E_d)` with exactly the pullback of the disjoint-sum sigma algebra under

`none ↦ inl(())`, `some(x) ↦ inr(x)`

into `Unit ⊕ E_d`. Products and sums carry the standard product and disjoint-sum sigma algebras.

The coordinate decomposition uses a specific bijection

`e : ((Fin(n) × Fin(k)) ⊕ Fin(r)) ≃ Fin(d)`.

To retain the packet's exact index choice, let `F_{a,b}` denote its standard finite-product bijection `finProdFinEquiv : Fin(a) × Fin(b) ≃ Fin(a·b)`, and let `U_{a,b}` denote its standard finite-sum bijection `finSumFinEquiv : Fin(a) ⊕ Fin(b) ≃ Fin(a+b)`. Then `e` is exactly the composite that first swaps `(i,j)` to `(j,i)` and applies `F_{k,n}` on the left summand, leaves the remainder summand unchanged, applies `U_{k·n,r}`, and finally transports the finite index along `k·n+r=d`. This is the equivalence displayed in the packet, not an arbitrary choice of a block coordinate system.

For `x ∈ E_d` and `j ∈ Fin(k)`, define the block vector `x_b(x,j) ∈ E_n` by

`x_b(x,j)(i) = x(e(inl(i,j)))`.

The remainder coordinates are `x(e(inr(ℓ)))` for `ℓ ∈ Fin(r)`. The conversions `WithLp.ofLp` and `WithLp.toLp 2` in the statement expose and restore these Euclidean coordinates.

Define

`Primitive = Fin(k) × E_n × Bool`,

`Micro = S × (Fin(m) → E_n) × Fin(m) × List(Primitive × E_n)`.

Write a primitive query as `p=(j,y,b)` and a microstate as `z=(s_z,a_z,i_z,h_z)`. The list sigma algebra is exactly the pullback under

`h ↦ (length(h), i ↦ h.get(i)) ∈ Σ_{q∈ℕ} (Fin(q) → Primitive × E_n)`

of the length-indexed finite-coordinate sigma algebra. The history stores pairs of a primitive query and its vector reply, with each new pair prepended. The microstate uses the product sigma algebra with this list structure.

The run record for a micro-run has type

`(Micro × Option(E_d)) × ℕ`,

and a direct run record has type

`(S × Option(E_d)) × ℕ`.

## 3. Quantifiers

The universal binder order is `d,n` and their inequalities; `κ` and its inequality; the displayed local measurable structures on the Euclidean and option spaces; the arbitrary measurable types `S,Ω`; the probability measure `μ`; `next`, `updateFO`, `updateGrad`, `initial`; their four measurability assumptions; fuel `t`; and the inequality `2·t<n`. Next come the local definitions depending on these data and, universally, the orthogonal family `(O_j)_{j∈Fin(k)}`. The matrix, quadratic function, oracles, and runs are then locally defined. Every conclusion holds for every such orthogonal family.

The pointwise conclusions quantify every `ω∈Ω` and every block `j∈Fin(k)`. The integrated block-count conclusions quantify every `j∈Fin(k)` separately. There are no existential constants, chosen optimizers, random orthogonal matrices, or unspecified exceptional sets.

## 4. Assumptions

Besides `3≤n`, `n≤d`, `4≤κ`, probability mass `μ(Ω)=1`, and `2·t<n`, the four functional assumptions are precisely:

1. `next` is measurable.
2. The uncurried map `(s,x,(v,g)) ↦ updateFO(s,x,(v,g))` is measurable.
3. The uncurried map `(s,x,g) ↦ updateGrad(s,x,g)` is measurable.
4. `initial` is measurable.

The state space is an arbitrary measurable space, without a stated topology. No separate differentiability assumption is supplied for the quadratic function below. No assumption says that `updateFO` and `updateGrad` agree, ignore a scalar answer, or implement a particular algorithm.

## 5. Local definitions and conclusion

### The matrix and its oracles

For each block define the real `n×n` matrix

`C_j = ((κ+1)/2) I_n − ((κ−1)/4)(O_j + O_j^T)`.

Define the real `d×d` matrix `A = blockPrecision κ O` by placing these `k` blocks on the diagonal, an `r×r` identity on the remainder, and zero matrices between distinct blocks and between a block and the remainder, with both matrix indices reindexed by the specific `e` above. Equivalently, its block action satisfies

`(Ax)(e(inl(i,j))) = (C_j x_b(x,j))(i)`

and

`(Ax)(e(inr(ℓ))) = x(e(inr(ℓ)))`.

This records the supplied definitions of `singleBlockPrecision`, `blockCoordinates`, and `blockPrecision`, including the identity remainder even when `r=0`.

Define

`f(x) = (x · (Ax))/2`,

`fo(x) = (f(x), gradient f(x))`, and `grad(x) = gradient f(x)`.

The dot product in `f` is the coordinate dot product from the packet. The symbol `gradient f(x)` has exactly the supplied meaning: apply the inverse Euclidean Riesz correspondence to the totalized Fréchet derivative of `f` at `x`. No additional derivative identity is inserted into the statement.

Define the primitive oracle by

`primitive(j,y,false) = O_j y`,

`primitive(j,y,true) = O_j^T y`.

The matrices `O_j` are the forward/transpose primitive oracle matrices; `C_j` are the block coefficient matrices; and `A` is the assembled coefficient matrix in the quadratic function. These are distinct roles.

### The schedule and reconstruction maps

For `x∈E_d` and `i∈Fin(m)`, write

`(j,b_index) = F_{k,2}^{−1}(i)`.

Define the planned primitive query to be

`plan(x,i) = (j, x_b(x,j), [b_index.val=1])`,

where the bracketed expression is its Boolean truth value. Thus the slots indexed by `F_{k,2}(j,0)` and `F_{k,2}(j,1)` use the same block vector with false and true tags, respectively. The schedule is the order supplied by `F_{k,2}` and has two queries per block.

For an arbitrary reply buffer `a : Fin(m) → E_n`, define

`g_j(x,a) = ((κ+1)/2) x_b(x,j)`

`             − ((κ−1)/4)(a(F_{k,2}(j,0)) + a(F_{k,2}(j,1)))`.

Define `G(x,a)=reconstruct(x,a)∈E_d` by

`G(x,a)(e(inl(i,j))) = g_j(x,a)(i)`,

`G(x,a)(e(inr(ℓ))) = x(e(inr(ℓ)))`.

Finally define

`decodeFO(x,a) = (⟨x,G(x,a)⟩/2, G(x,a))`,

where the scalar uses the real Euclidean inner product. These formulas define the decoders even for arbitrary reply buffers; the displayed conclusion below concerns running them with the actual primitive oracle.

### The two microtransitions

Define `nextB(z)` by inspecting `next(s_z)`:

- on `inl(x)`, return `inl(x)`;
- on `inr(x)`, return `inr(plan(x,i_z))`.

For either update mode, if `next(s_z)` is terminal, its micro-update leaves `z` unchanged. Otherwise let `next(s_z)=inr(x)`, let `a'` be `a_z` with coordinate `i_z` replaced by the supplied reply `a`, and let `h'=(p,a)::h_z`, where `p` is the supplied primitive query. If `i_z.val+1<m`, both modes return

`(s_z, a', i_z+1, h')`.

If that inequality fails, they respectively return

`updateBFO(z,p,a) = (updateFO(s_z,x,decodeFO(x,a')), (i↦0), 0, h')`,

`updateBGrad(z,p,a) = (updateGrad(s_z,x,G(x,a')), (i↦0), 0, h')`.

Each zero in the buffer is the zero vector of `E_n`, and the zero slot is the element of `Fin(m)` justified by `m>0`. The incremented slot has the proof of its strict bound as in the packet.

Set

`start(ω) = (initial(ω), (i↦0), 0, [])`.

For a micro-run record `R=(((s_R,a_R,i_R,h_R),status_R),C_R)`, define

`readback(R) = ((s_R,status_R), C_R div m)`

and

`blockCalls(j,R) = #{(p,a) in h_R : p.first = j}`.

The block-call count includes both Boolean tags, all replies, and all repetitions; it tests only the first component of the primitive query stored in the history. The readback keeps the full terminal/exhaustion tag.

### The execution rule

For an arbitrary transition system and oracle `o`, the supplied `Run(next,update,o; t,s)` returns `((s_final,status),c)` and is defined as follows:

1. If `next(s)=inl(x)`, return `((s,some(x)),0)` at any fuel, including zero.
2. If `next(s)=inr(x)` with zero fuel, return `((s,none),0)`.
3. With `next(s)=inr(x)` and fuel `u+1`, call `o(x)`, recur from `update(s,x,o(x))` at fuel `u`, and add one to the resulting call count.

Define the four random records, meaning measurable functions of the initial randomness once measurability is concluded, by

`D_FO(ω) = Run(next,updateFO,fo; t,initial(ω))`,

`B_FO(ω) = Run(nextB,updateBFO,primitive; m·t,start(ω))`,

`D_Grad(ω) = Run(next,updateGrad,grad; t,initial(ω))`,

`B_Grad(ω) = Run(nextB,updateBGrad,primitive; m·t,start(ω))`.

The oracle data, transition maps, and fuel are fixed across `ω`; only the initial state is supplied as `initial(ω)`.

### Measurability assertions

The conclusion first asserts that all of the following are measurable:

- `primitive` and `nextB`;
- the uncurried map `(z,p,a) ↦ updateBFO(z,p,a)`;
- the uncurried map `(z,p,a) ↦ updateBGrad(z,p,a)`;
- `start`;
- `B_FO` and `D_FO`;
- `B_Grad` and `D_Grad`.

### The complete conclusions for both update modes

For each mode `M ∈ {FO, Grad}`, let `D_M(ω)=((s_D,status_D),C_D(ω))`, let `C_B(ω)` be the natural call-count component of `B_M(ω)`, and set `H_j(ω)=blockCalls(j,B_M(ω))`. The proposition asserts the following full conjunction separately for `FO` and for `Grad`, using that mode's own direct and batched records:

1. For every `ω∈Ω`,

   `readback(B_M(ω)) = D_M(ω)`,

   `C_B(ω) = m·C_D(ω)`,

   `C_D(ω) ≤ t`, and `C_B(ω) ≤ m·t`.

   In addition, for every `j∈Fin(k)`,

   `H_j(ω) = 2·C_D(ω)`,

   `H_j(ω) ≤ 2·t`, and `H_j(ω)<n`.

2. The pushforward measures on the full direct-record space agree:

   `μ.map(ω ↦ readback(B_M(ω))) = μ.map(D_M)`.

   Moreover `μ.map(D_M)` is a probability measure.

3. The real-valued functions `ω ↦ C_D(ω)` and `ω ↦ C_B(ω)`, obtained by coercing the natural counts to real numbers, are Bochner integrable under `μ`, and

   `∫ C_B(ω) dμ(ω) = (m : ℝ) · ∫ C_D(ω) dμ(ω)`,

   `∫ C_B(ω) dμ(ω) ≤ (m·t : ℕ)`.

   In the last inequality the natural bound is coerced to a real number.

4. For every `j∈Fin(k)`, the real-valued function `ω ↦ H_j(ω)` is Bochner integrable and

   `∫ H_j(ω) dμ(ω) = 2 · ∫ C_D(ω) dμ(ω)`,

   `∫ H_j(ω) dμ(ω) ≤ (2·t : ℕ)`,

   with the same real coercion of the natural bound.

This paired presentation is a notation for the two explicit conjunctions in the packet. It does not assert equality between `D_FO` and `D_Grad`, between their counts, or between the two batched runs.

## 6. Scopes and senses

All execution and per-block count statements are pointwise for every `ω`, including points in measure-zero sets. The pushforward equality is for the record containing the final underlying state, the `Option(E_d)` result with its tag, and the rescaled actual query count. It is stronger than merely matching the distribution of a returned vector, and its stated space is not the unprojected microstate record.

The natural counts measure actual oracle calls made before a terminal branch or fuel exhaustion. `some(x)` is produced when the terminal branch is encountered, even if no fuel remains; `none` denotes an active query branch encountered at zero fuel. The fuel inequality is the deterministic requirement `2·t<n`, not an assumption about an expected number of calls. It allows `t=0`.

The integral statements are ordinary real expectations under the supplied probability measure, expressed with Bochner integrability. They concern direct counts, total primitive counts, and per-block primitive counts. They do not assert integrability of objective values, output vectors, or states. The explicit mean bound per block is `≤2·t`; the displayed strict bound `<n` is pointwise. No additional expectation inequality is added to the reconstruction.

The construction covers `r=0` and positive remainder dimensions. The remainder is acted on by the identity in `A` and copied directly by reconstruction. Primitive oracle calls operate on the `k` full blocks. The false/true Boolean tags distinguish `O_j` from its transpose; the factor two in per-block counts includes both tags. The plan for a given query is fixed by its block coordinates and slot and takes no previous replies as input.

## 7. Constant dependencies and ambiguity record

The only numerical parameters supplied independently are `d,n,κ,t`, with the displayed bounds. The integers `k,r,m`, the initial slot zero, and the coordinate bijection depend on `d,n`. The exact rescaling factor is `m=2·(d div n)`; each block's exact multiplier is `2`. There are no hidden big-O constants or existential numerical constants.

The block matrices `C_j` and assembled matrix `A`, and hence `f`, `fo`, and `grad`, depend on `d,n,κ` and the universally quantified orthogonal family. The primitive oracle depends on the orthogonal family and the block dimensions; its formula has no `κ` dependence. The block projection and plan depend on `d,n` and the queried point, with no direct dependence on `κ`, the orthogonal family, or earlier replies. The reconstruction and scalar decoder additionally depend on `κ`; the orthogonal family affects them through the actual replies, rather than appearing as an argument in their formulas.

The micro-next map depends on `next` and the plan. The two micro-updates additionally use their respective original update map, the common reconstruction data, and their buffer/history mechanisms. `start` depends on `initial` and the dimensions. Their run records depend on the corresponding fixed data and fuel, while their pushforward laws and integrals additionally use `μ`.

The approved context does not expand the arithmetic enumeration convention inside `finProdFinEquiv` or `finSumFinEquiv`. This reconstruction retains those exact bijections and the displayed composition rather than selecting an unprovided arithmetic ordering. This leaves no choice of bijection in the reconstruction: `F`, `U`, and `e` are precisely the ones in the packet. The supplied gradient definition is retained without importing an unprovided derivative formula. No further semantic ambiguity requiring external input is identified, and no identity of an external theorem or source is inferred.
