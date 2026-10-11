# Independent anonymous Lean reconstruction

Only the supplied anonymous statement, approved mathematical definition context, and packet metadata were read. No source theorem text, source anchor, original Lean declaration, previous audit or repair was consulted. This is a reconstruction, not a source-fidelity verdict. The packet reports compiled=true; no proof or independent Lean build was inspected.

## Objects, domains and hypotheses

Let E be any finite-dimensional real inner-product space with its normed additive group structure and Borel measurable structure, including dimension zero. Let V:E→R be twice continuously Frechet differentiable, α,β be nonnegative real numbers, and η be real. Assume

    0<α,   α≤β,   0<η,   βη≤1,
    α||v||² ≤ D²V(x)[v,v] ≤ β||v||²    for every x,v∈E.

The Hessian here is the displayed iterated Frechet derivative. Write ∇V for the inner-product gradient. There are no higher-derivative hypotheses or additional smoothness constants. Fix arbitrary y,r∈E and z₀=(x₀,v₀)∈E×E. The reference r need not equal x₀. None of y,r,z₀ is random under the input law below.

## All deterministic lets

Define the center c(y,r)=y−η∇V(r). For z=(x,v) and any real s, the flow is

    Φ(y,r,s,z)=(
      c(y,r)+cos(s)(x−c(y,r))+sqrt(η)sin(s)v,
      −sin(s)/sqrt(η)(x−c(y,r))+cos(s)v).

Write g_r(x)=∇V(x)−∇V(r). The reflection map and rate are

    S(r,(x,v))=(x,v−[2〈v,g_r(x)〉/||g_r(x)||²]g_r(x)),
    λ_r(x,v)=sqrt(η)max(0,〈v,g_r(x)〉).

Real division is total, with zero denominator giving quotient zero. In particular S is defined also at g_r(x)=0 and then fixes the state. No nonzero-normal assumption is implicit. The rate is a finite nonnegative real.

For u≥0 define the cumulative hazard

    Λ(y,r,z,u)=∫₀ᵘ λ_r(Φ(y,r,s,z)) ds.

This is the displayed real interval integral. For e≥0 define the extended nonnegative waiting time

    τ(y,r,z,e)=inf{u≥0 : Λ(y,r,z,u)−e≥0},

with infinity if this set is empty. This is exactly hittingAfter with starting time 0 and target [0,∞), using a weak crossing inequality. In particular e=0 gives τ=0. It is a hitting-time definition from the deterministic integrated hazard, not a newly postulated probability law for a waiting time.

Let Rec=([0,∞)×(E×E)) ⊔ {†}, where † denotes the distinct singleton second summand. For a live record (a,z), define next(y,r,e,(a,z)) by first evaluating τ(y,r,z,e). If it is infinity, the result is †; otherwise the result is

    (a+τ, S(r,Φ(y,r,τ,z))).

The map next sends † to †. The explicit comparison τ=∞ occurs BEFORE extracting its value with untopD 0, so the default zero is never used to turn an infinite waiting time into a live event. Flow precedes reflection, and the recorded state is post-reflection. The duration τ is relative; a+τ is an absolute time. There is no test against T in next.

For every nonnegative sequence e:N→[0,∞), the let-bound record is finite recursion:

    record(y,r,z₀,e,0)=(0,z₀),
    record(y,r,z₀,e,k+1)=next(y,r,e(k),record(y,r,z₀,e,k)).

These are finite indexed records, not a supplied global nonexplosive process. Each live step tests only whether its waiting time is infinite, and the cemetery tag is absorbing thereafter.

## Actual random inputs and marked history

Let Ω=R^N and P be the countable product of rate-one exponential measures on R. Under P the coordinate variables w(k) are independent Exp(1) variables. Set ε(w,k)=Real.toNNReal(w(k))=max(w(k),0), represented as a nonnegative real. This defines ε on all of Ω, including points off the support of P; it agrees with the coordinates almost surely.

For every n∈N, let Hist(n)=Rec^{0,...,n}. The let-bound history is

    H(w)(j)=record(y,r,z₀,ε(w),j),    0≤j≤n.

It includes the fixed initial record (0,z₀). It uses exactly the first n input coordinates w(0),...,w(n−1); subsequent coordinates do not affect H. No random initial state, random reference or extra reflection randomness is included. The let-bound readTime sends a live record (a,z) to a as a real and sends † to 0.

## Time-prefix domain, comap measure and reconstruction lets

Fix n∈N and T≥0. The let-bound Δ(n,T)⊂R^n is the set of tuples t=(t₁,...,t_n) with

    0=t₀<t₁<...<t_n<T.

Precisely, StrictMono is applied after prepending 0, and all of the n supplied coordinates must be below T. When n=0 these conditions are vacuous. Prefix(n,T) is the subtype of R^n consisting of Δ(n,T).

The let-bound m(n,T) is Measure.comap along the subtype inclusion of real product Lebesgue volume. It is the unnormalized measure on that measurable subtype: pushing it forward through the inclusion gives Lebesgue measure restricted to Δ(n,T). It is not a normalized uniform probability law. For n=0 the empty-coordinate space and Prefix are singletons, with volume one. For n≥1 and T=0 the subtype is empty.

For t∈Prefix(n,T), put t₀=0 and define the let-bound zAt by

    z_i=S(r,Φ(y,r,t_i−t_{i−1},z_{i−1})),    i=1,...,n,

starting from the given z₀. In the displayed Fin.induction, i.castSucc indexes the old state and old time in the tuple with zero prepended. All these durations are strictly positive. The let-bound history reconstruction K is

    K(y,r,z₀,n,T,t)(j)=(t_j,z_j),    j=0,...,n,

with the live tag at every index. Formally the times are converted by Real.toNNReal; it leaves the times unchanged on this subtype. K records the initial and all post-reflection states, not just event times.

The real density let is

    qReal(y,r,z₀,n,T,t)
      = product over i=1,...,n of
        λ_r(Φ(y,r,t_i−t_{i−1},z_{i−1}))
        × exp(−Λ(y,r,z_{i−1},t_i−t_{i−1})).

The event rate is evaluated BEFORE the reflection at the end of its segment, whereas the starting state z_{i−1} is the previous POST-reflection state. The Real.toNNReal used in the integral's duration leaves it unchanged. The let q is ENNReal.ofReal(qReal), the embedding of max(qReal,0) into [0,∞]. The theorem explicitly asserts qReal≥0 on Prefix. Each density value is finite, since qReal is a finite real product. An empty product is one.

There is no terminal survival factor exp(−Λ(y,r,z_n,T−t_n)). There is also no state flowed forward from t_n to T and no (n+1)-st waiting time in K or q. T appears in the admissible subtype/domain, not as a final evolution segment.

## Accepted history event and full theorem

The let A(n,T)⊂Hist(n) consists of histories h such that:

- Every coordinate is live: for each j, h(j) is some tagged (a,z).
- j↦readTime(h(j)) is strictly increasing.
- readTime(h(i))<T for i=1,...,n.

On the whole Hist(n), A itself does not impose h(0)=(0,z₀), an initial time of zero, consistency of states with Φ or S, or a terminal survival condition. H and K impose their own initial and dynamic conditions. Requiring all tags to be live prevents the readTime(†)=0 convention from admitting cemetery histories.

The theorem is universally quantified over all n∈N and T≥0 and asserts all of the following.

1. Δ(n,T) and A(n,T) are measurable sets.

2. K and q are jointly Borel measurable in (y,r,z₀,t), with domain ((E×E)×(E×E))×Prefix(n,T). The first component is ((y,r),z₀). This is joint measurability, not merely separate measurability with parameters fixed.

3. For every y,r∈E and z₀∈E×E, let H be the actual random history above, B=H^{-1}(A(n,T)), and

       obs(w)=(readTime(H(w)(1)),...,readTime(H(w)(n))).

   Then H and obs are measurable and B is a measurable subset of Ω. Also qReal(t)≥0 for every t∈Prefix(n,T).

4. For every w∈B there exists t∈Prefix(n,T) with t.val=obs(w) and H(w)=K(t). This is pointwise on B, not merely an almost-sure assertion. The statement explicitly asks for existence; equality of the underlying tuple also forces uniqueness in this subtype.

5. As measures on the full tagged marked-history space Hist(n),

       H_*(P restricted to B) = K_*(m(n,T) with density q).

   These are unnormalized measures. In particular P restricted to B is not the conditional probability law given B.

6. For every measurable F:Hist(n)→[0,∞],

       ∫_B F(H(w)) dP(w)
         = ∫_{Prefix(n,T)} F(K(t)) q(t) dm(n,T)(t).

   This is equality of extended nonnegative Lebesgue integrals. F may take infinity; there is no integrability or boundedness premise. A signed-real expectation identity for arbitrary real F is not the displayed claim.

7. The total mass is exactly

       ∫_{Prefix(n,T)} q(t) dm(n,T)(t)=P(B),    P(B)≤1.

   Thus the density describes a subprobability mass, not automatically a probability density with integral one. The theorem does not assert P(B)>0 for all states and parameters.

## Meaning of the prefix and boundary cases

For n≥1, B means the first n records after initialization are all live, their times strictly increase from zero, and their times are strictly less than T. No condition is imposed on the next record. Further events before T are permitted. Once an appropriate process/count construction and almost-sure absence of ties are separately justified, this supports a first-n prefix or at-least-n-events-before-T interpretation. It does not directly describe EXACTLY n events before T. The missing final no-event condition and its terminal survival factor prevent that interpretation. No such final factor is hidden in m, q, A or B.

At points where an input ε(w,k)=0, the corresponding live waiting time is zero, and an otherwise live prefix with that repeated time fails the strict-order condition. These points are defined by the statement even though exponential inputs are positive almost surely. Equality of a time with T also fails B. There are no additional infinity checks on a terminal waiting time, cumulative count, or density. Infinity remains allowed for F and for nonnegative integrals; the total-density integral is nevertheless finite by the mass bound.

For n=0, H is the deterministic one-record live history (0,z₀), B=Ω for all T≥0, obs is the empty tuple, Prefix is a singleton, q=1, and the two history measures are the unit point mass at the initial history. This remains true at T=0. For n≥1 and T=0, B and Prefix are empty and the total mass is zero. Rank-zero E is permitted: rates vanish, positive thresholds have infinite waiting time, and n≥1 accepted histories have zero P-mass. A zero threshold can still give a finite zero-time record, but it fails strict ordering.

This is a finite-prefix theorem for every finite n. It contains no assertion of nonexplosion, existence of a continuous-time path for all times, stationarity or target invariance, exact event counting, expected event counts, query costs, or evolution to the horizon. There are no asymptotic or unnamed constants. α and β constrain V and η but do not enter the definitions independently. The formulas depend on V,η,y,r,z₀ and the prefix times; n determines the dimension and number of segments, T limits the domain, and the random inputs always have exponential rate exactly one.
