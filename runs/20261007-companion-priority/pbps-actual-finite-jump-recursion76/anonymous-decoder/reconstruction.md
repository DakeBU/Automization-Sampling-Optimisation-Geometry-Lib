# Anonymous statement reconstruction

Anonymous deterministic recursive-event proposition

Ambient data and assumptions.
E is an arbitrary type carrying a normed additive commutative group structure, a real inner-product-space structure, finite dimension over ℝ, a measurable-space structure, and the Borel-space compatibility instance. Dimension zero is allowed. V : E → ℝ, α, β : ℝ≥0, and η : ℝ are arbitrary subject to all of the following:
  0 < (α : ℝ);
  α ≤ β;
  V is twice continuously Fréchet differentiable over ℝ;
  for every x, v ∈ E,
    (α : ℝ) ‖v‖² ≤ (D(DV)(x)[v])[v]
    and (D(DV)(x)[v])[v] ≤ (β : ℝ) ‖v‖²;
  0 < η;
  (β : ℝ) η ≤ 1.
Here (D(DV)(x)[v])[v] is exactly the displayed iterated Fréchet derivative, and ∇V is the real Hilbert gradient.

Notation and meanings.
A phase z ∈ E × E has position z.1 and velocity z.2. Write R for the disjoint union (ℝ≥0 × (E × E)) ⊕ Unit. Its left tag inl(T,z) contains a finite nonnegative time and a phase. Its right tag inr() contains no phase and represents the stopped branch. Extended times lie in WithTop ℝ≥0, written ℝ≥0 ∪ {∞}; ∞ is the largest element. Nonnegative times are embedded into that extended-time order where indicated. Real division is total, including at a zero denominator. sqrt is the nonnegative real square root. untopD(0) returns a finite extended time's nonnegative value and has default zero at ∞. Real.toNNReal(r) is the nonnegative part of a real number. Scalar multiplication is denoted by •, and ⟨·,·⟩ is the real inner product.

The eleven literal local definitions, in their displayed order, are:

1. c : E → E → E,
   c(y,xRef) = y − η • ∇V(xRef).

2. Φ : E → E → ℝ → (E × E) → (E × E),
   Φ(y,xRef,t,z) =
     ( c(y,xRef) + cos(t) • (z.1 − c(y,xRef))
         + (sqrt(η) sin(t)) • z.2,
       (−sin(t) / sqrt(η)) • (z.1 − c(y,xRef))
         + cos(t) • z.2 ).
   The time argument of Φ is a real number.

3. S : E → (E × E) → (E × E),
   S(xRef,z) =
     ( z.1,
       z.2 −
         (2 ⟨z.2, ∇V(z.1) − ∇V(xRef)⟩ /
           ‖∇V(z.1) − ∇V(xRef)‖²)
         • (∇V(z.1) − ∇V(xRef)) ).
   This definition has no nonzero-gradient-difference premise.

4. rate : E → (E × E) → ℝ,
   rate(xRef,z) =
     sqrt(η) max(0, ⟨z.2, ∇V(z.1) − ∇V(xRef)⟩).

5. H : E → E → (E × E) → ℝ,
   H(y,xRef,z) =
     (η⁻¹ ‖z.1 − c(y,xRef)‖² + ‖z.2‖²) / 2.
   The two squared norms are separate vector norms exactly as displayed.

6. C : E → E → (E × E) → ℝ,
   C(y,xRef,z) =
     sqrt(η) (β : ℝ) sqrt(2 H(y,xRef,z))
       (sqrt(2 η H(y,xRef,z)) + ‖c(y,xRef) − xRef‖).

7. Λ : E → E → (E × E) → ℝ≥0 → ℝ,
   Λ(y,xRef,z,t) =
     ∫ from s = 0 to s = (t : ℝ) rate(xRef, Φ(y,xRef,s,z)) ds.
   This is the real Lebesgue interval integral with its oriented-interval convention.

8. τ : E → E → (E × E) → ℝ≥0 → WithTop ℝ≥0.
   On the parameter space (E × E) × (E × E) × ℝ≥0, define the displayed process
     F(t,a) = Λ(a.1.1,a.1.2,a.2.1,t) − (a.2.2 : ℝ),
   where t ∈ ℝ≥0 and a = ((y,xRef),z,e) has the displayed product projections. Then
     τ(y,xRef,z,e) =
       hittingAfter(F, [0,+∞) ⊆ ℝ, start = 0, parameter = ((y,xRef),z,e)).
   Thus τ is the extended nonnegative infimum of times t at or after zero with
     Λ(y,xRef,z,t) − (e : ℝ) ≥ 0;
   it is ∞ when that set is empty.

9. next : E → E → ℝ≥0 → R → R,
   next(y,xRef,e,inr()) = inr().
   If r = inl(a) with a = (T,z) ∈ ℝ≥0 × (E × E), then:
     if τ(y,xRef,z,e) = ∞,
       next(y,xRef,e,inl(a)) = inr();
     otherwise, putting θ = untopD(0)(τ(y,xRef,z,e)) ∈ ℝ≥0,
       next(y,xRef,e,inl(a)) =
         inl(T + θ, S(xRef, Φ(y,xRef,(θ : ℝ),z))).
   The finite-time use of untopD(0) in this active branch is guarded by τ ≠ ∞.

10. record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → R,
    record(y,xRef,z₀,e,n) =
      Nat.rec(inl(0,z₀), (k,r) ↦ next(y,xRef,e(k),r), n).
    Here e is an arbitrary sequence of nonnegative thresholds, including sequences with zero entries or all entries zero. The entry e(k) is used in the transition from record k to record k+1.

11. eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0,
    eventTime(y,xRef,z₀,e,n) =
      if record(y,xRef,z₀,e,n) = inl(T,z), then (T : WithTop ℝ≥0);
      if record(y,xRef,z₀,e,n) = inr(), then ∞.
    Equivalently, this is the displayed Sum.elim of the record, with left function (T,z) ↦ (T : WithTop ℝ≥0) and right function () ↦ ∞.

Conclusion.
With those definitions in scope, the following ten groups hold as one conjunction.

(1) For every y,xRef ∈ E, z₀ ∈ E × E, and e : ℕ → ℝ≥0,
    record(y,xRef,z₀,e,0) = inl(0,z₀).

(2) For every y,xRef ∈ E, z₀ ∈ E × E, e : ℕ → ℝ≥0, and n ∈ ℕ,
    record(y,xRef,z₀,e,n+1) =
      next(y,xRef,e(n),record(y,xRef,z₀,e,n)),
    and, for every a = (T,z) ∈ ℝ≥0 × (E × E),
    if record(y,xRef,z₀,e,n) = inl(a), then both:
      record(y,xRef,z₀,e,n+1) = inr()
        if and only if τ(y,xRef,z,e(n)) = ∞;
      if τ(y,xRef,z,e(n)) ≠ ∞, then
        record(y,xRef,z₀,e,n+1) =
          inl(T + θ, S(xRef, Φ(y,xRef,(θ : ℝ),z))),
        where θ = untopD(0)(τ(y,xRef,z,e(n))).

(3) The single map
      ((y,xRef),u,r) ↦ next(y,xRef,u,r)
    from (E × E) × ℝ≥0 × R to R is measurable jointly in all its displayed parameters.

(4) For every fixed n ∈ ℕ, the map
      ((y,xRef),z₀,e) ↦ record(y,xRef,z₀,e,n)
    from (E × E) × (E × E) × (ℕ → ℝ≥0) to R is measurable jointly in y,xRef,z₀ and the entire threshold sequence e. The sequence space has its product measurable structure.

(5) For every fixed n ∈ ℕ, the map
      ((y,xRef),z₀,e) ↦ eventTime(y,xRef,z₀,e,n)
    from (E × E) × (E × E) × (ℕ → ℝ≥0) to WithTop ℝ≥0 is measurable jointly in y,xRef,z₀ and the entire threshold sequence e.

(6) For every y,xRef ∈ E, z₀ ∈ E × E, and e : ℕ → ℝ≥0,
    eventTime(y,xRef,z₀,e,0) = 0,
    and n ↦ eventTime(y,xRef,z₀,e,n) is monotone:
    for all n,m ∈ ℕ, n ≤ m implies
      eventTime(y,xRef,z₀,e,n) ≤ eventTime(y,xRef,z₀,e,m).

(7) For every y,xRef ∈ E, z₀ ∈ E × E, e : ℕ → ℝ≥0, and n,k ∈ ℕ,
    record(y,xRef,z₀,e,n) = inr()
      implies record(y,xRef,z₀,e,n+k) = inr().

(8) For every y,xRef ∈ E, z₀ ∈ E × E, e : ℕ → ℝ≥0, n ∈ ℕ, and a = (T,z) ∈ ℝ≥0 × (E × E),
    record(y,xRef,z₀,e,n) = inl(a) implies:
      H(y,xRef,z) = H(y,xRef,z₀),
      and for every t ∈ ℝ≥0,
        (t : WithTop ℝ≥0) < τ(y,xRef,z,e(n))
      implies all three conclusions
        H(y,xRef,Φ(y,xRef,(t : ℝ),z)) = H(y,xRef,z₀),
        0 ≤ rate(xRef,Φ(y,xRef,(t : ℝ),z)),
        rate(xRef,Φ(y,xRef,(t : ℝ),z)) ≤ C(y,xRef,z₀).
    The trajectory assertions are explicitly guarded by strict inequality before this transition's hitting time.

(9) For every y,xRef ∈ E, z₀ ∈ E × E, and e : ℕ → ℝ≥0, all three assertions hold:
    0 ≤ C(y,xRef,z₀);
    if 0 < C(y,xRef,z₀), then for every n ∈ ℕ,
      eventTime(y,xRef,z₀,e,n)
        + (Real.toNNReal((e(n) : ℝ) / C(y,xRef,z₀)) : WithTop ℝ≥0)
        ≤ eventTime(y,xRef,z₀,e,n+1);
    if C(y,xRef,z₀) = 0, then for every n ∈ ℕ and a ∈ ℝ≥0 × (E × E),
      record(y,xRef,z₀,e,n) = inl(a)
        implies [0 < e(n) implies record(y,xRef,z₀,e,n+1) = inr()].
    The spacing inequality uses extended-time addition and is guarded by a strictly positive cap. The zero-cap stopping assertion requires both a finite current record and a strictly positive threshold.

(10) For every y,xRef ∈ E, z₀ ∈ E × E, e : ℕ → ℝ≥0, n ∈ ℕ, and a = (T,z) ∈ ℝ≥0 × (E × E),
     record(y,xRef,z₀,e,n) = inl(a) implies both:
       if e(n) = 0, then
         record(y,xRef,z₀,e,n+1) = inl(T,S(xRef,z));
       for every b = (T',z') ∈ ℝ≥0 × (E × E),
         0 < e(n) implies
           [record(y,xRef,z₀,e,n+1) = inl(b) implies T < T'].

Scope of the assertion.
The data e are arbitrary nonnegative inputs. Measurability concerns the displayed jointly parameterized maps, with n fixed in groups (4) and (5). The stopped tag carries no phase. Conservation and the rate cap in group (8) have exactly the finite-record and strict-before-hitting-time guards written there. Groups (9) and (10) retain their distinct positive-cap, zero-cap, zero-threshold, positive-threshold, and finite-successor guards. The conclusion contains no distributional assumption, stochastic-process existence claim, limit statement that eventTime(n) tends to infinity, or computational/query-cost bound.


Decoder run SHA256: d563440f1fa8e079ebf72a93af345e26817df67157f70c41a3a46ea1859f79dc
