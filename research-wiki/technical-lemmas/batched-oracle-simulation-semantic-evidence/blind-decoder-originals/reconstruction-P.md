# Reconstruction of packet P

Decoder: Codex independent source-blind mathematical decoder `/root/neutral_decode_c19`.
Source text visible: **false**. This reconstruction uses only `input-P.json` and its enclosed definition context; no source identity, source text, proof, or external definition was consulted.

## 1. Objects

Let `S, Q, A, B, X, P, J` be arbitrary types in their respective universes. Equality on `J` is decidable. The data are a positive integer `m`, a distinguished blank answer `blank ∈ A`, maps

- `next : S → X ⊕ Q` and `update : S × Q × B → S`;
- `primitive : P → A` and `target : Q → B`;
- `plan : Q × Fin(m) → P` and `decode : Q × A^{Fin(m)} → B`;
- `label : P → J` and `slot : Fin(m) → J`.

Here `Fin(m) = {0,…,m−1}`. The two branches of `next` have distinct meanings: `inl(x)` halts with result `x`; `inr(q)` requests an answer to `q`.

For any such transition system and oracle `o`, define

`Run(next, update, o; t, s) = ((s_final, status), c)`,

with a natural-number fuel `t`, a final state `s_final`, a status in `Option(X)`, and a natural-number count `c`. The definition is exactly:

1. If `next(s) = inl(x)`, return `((s, some(x)), 0)`, for every fuel value, including zero.
2. If `next(s) = inr(q)` and the fuel is zero, return `((s, none), 0)`.
3. If `next(s) = inr(q)` and the fuel is `t+1`, call `o(q)`, recurse with fuel `t` from `update(s,q,o(q))`, and add one to the recursive count while preserving its final state and status.

Thus the count records actual oracle calls, and `none` and `some(x)` retain the distinction between fuel exhaustion while requesting a query and a terminal result.

## 2. Domains

The microstate domain is the right-associated product

`Micro = S × (Fin(m) → A) × Fin(m) × List(P × A)`.

Write a microstate as `z = (s_z, a_z, i_z, h_z)`. Its components are the underlying state, an indexed answer buffer, the current slot, and a list of primitive-query/answer pairs. Lists may contain repetitions. The list is a history with the newest entry prepended. No measurability, topology, probability measure, norm, linear structure, or finiteness of the arbitrary types is assumed.

## 3. Quantifiers

Universally quantify the seven types and the decidable-equality instance for `J`; then quantify, in order, `m`, the proof `0 < m`, `blank`, `next`, `update`, `primitive`, `target`, `plan`, `decode`, `label`, and `slot`. After the two assumptions below, quantify every natural fuel `t` and every initial state `s ∈ S`.

There are no existentially chosen constants or algorithms in the proposition. The plan and decoder are supplied as universally quantified data satisfying the assumptions.

## 4. Assumptions

For every `q ∈ Q`, decoding the complete planned vector of actual primitive replies gives the target reply:

`decode(q, i ↦ primitive(plan(q,i))) = target(q)`.

For every `q ∈ Q` and every `i ∈ Fin(m)`, the primitive query in slot `i` has the prescribed label:

`label(plan(q,i)) = slot(i)`.

The slot labels need not be distinct. Neither assumption requires the plan to be injective. The plan is a function of `q` and the slot; the displayed plan does not take earlier replies as an argument.

## 5. Conclusion and all local definitions

Define the microtransition `nextB : Micro → X ⊕ P` by inspecting only `next(s_z)`:

- if it is `inl(x)`, return `inl(x)`;
- if it is `inr(q)`, return `inr(plan(q,i_z))`.

Define `updateB(z,p,a)` as follows. If `next(s_z)` is terminal, leave `z` unchanged. Otherwise write `next(s_z) = inr(q)`, replace buffer coordinate `i_z` by `a`, and call the new buffer `a'`. Set `h' = (p,a) :: h_z`. If `i_z.val+1 < m`, return

`(s_z, a', i_z+1, h')`.

Here `i_z+1` is the element of `Fin(m)` with value `i_z.val+1`, justified by that strict inequality. Otherwise return

`(update(s_z,q,decode(q,a')), (i ↦ blank), 0, h')`.

The zero slot is the element of `Fin(m)` with value zero, justified by `m>0`. In particular the supplied primitive query `p` is recorded in the history; the slot being filled is the current slot, and completing a block updates the original state, resets the answer buffer to blank, and resets the slot to zero.

Starting from the blank buffer, slot zero, and empty history, define

`batch = Run(nextB, updateB, primitive; m·t, (s, (i ↦ blank), 0, []))`,

and define

`direct = Run(next, update, target; t, s)`.

Write these records as

`batch = (((s_B, a_B, i_B, h_B), status_B), C_B)`

and

`direct = ((s_D, status_D), C_D)`.

Then the proposition asserts the following conjunction:

1. `((s_B, status_B), C_B div m) = ((s_D, status_D), C_D)`.
2. `C_B = m·C_D`.
3. `C_D ≤ t`.
4. For every `j ∈ J`,

   `#{(p,a) in h_B : label(p)=j} = #{i ∈ Fin(m) : slot(i)=j} · C_D`.

All counts include multiplicity. On the right of the last equality, the Lean expression is the predicate count on `List.ofFn slot`; on the left it is the predicate count on the history list. The division in the first equality is natural-number division. The equality in item 1 includes the final underlying state and the complete `Option(X)` status, as well as the rescaled count.

## 6. Scopes and senses

The conclusions hold for every allowed fuel and initial state, with the same supplied maps. They are exact deterministic equalities, not asymptotic or probabilistic statements. The conclusion compares the underlying state, terminal/exhaustion tag, and rescaled count; it does not identify the complete microstate with the original state. Buffer, slot, and history remain extra microstate data.

The count `C_D` is the number of oracle calls actually performed, which may be smaller than `t` because a terminal branch is tested before fuel exhaustion. The micro-run's fuel is `m·t`. The theorem states an exact factor `m` for actual calls. The per-label factor is the multiplicity of `j` in the supplied slot list, including zero multiplicities and repeated labels.

## 7. Constant dependencies and ambiguity record

The block size `m` and blank value are arbitrary supplied data with only `m>0`. The label multiplier depends only on `m` and `slot`. The microtransition is determined by `next`, `plan`, `decode`, `update`, `blank`, and `m`; the primitive and target oracles enter their respective runs. The history label count additionally uses `label`. There are no hidden universal numerical constants or unspecified probability laws.

No semantic ambiguity requiring external context remains for this reconstruction. The named finite enumeration `List.ofFn` is used in its supplied sense of enumerating all slots. No identity of an external theorem or source is inferred.
