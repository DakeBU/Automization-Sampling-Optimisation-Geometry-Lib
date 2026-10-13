# Anonymous reconstruction of the visible statement

Let E be a finite-dimensional real inner-product space, with its compatible norm, its norm topology, and a measurable structure equal to the Borel measurable structure. The zero-dimensional space is allowed. Let V : E -> R and let alpha, beta be nonnegative real scalars. Write alpha and beta also for their real coercions. Let eta be real. Assume:

1. 0 < alpha and alpha <= beta.
2. V is twice continuously Frechet differentiable over R.
3. For every x, v in E, alpha ||v||^2 <= D(DV)(x)[v](v) <= beta ||v||^2. Here DV(x) is a continuous real linear functional and D(DV)(x)[v] is such a functional, then evaluated at v. Both inequalities hold for all vectors, including v = 0, with the same global alpha and beta.
4. 0 < eta and beta eta <= 1. Equality in the last inequality is permitted.

The gradient grad V(x) is the real Hilbert-space gradient representing DV(x) under the Riesz isometry. Scalar multiplication below is real scalar multiplication on E. Every displayed norm is the given norm of an individual E-vector. No norm of an ordered pair occurs in the definitions or conclusions.

For y, xRef in E, t in R, and z = (q,p) in E x E, define, exactly:

    c(y,xRef) = y - eta grad V(xRef),

    Phi(y,xRef,t,(q,p)) =
      ( c(y,xRef) + cos(t)(q-c(y,xRef)) + sqrt(eta) sin(t) p,
        (-sin(t)/sqrt(eta))(q-c(y,xRef)) + cos(t) p ),

    H(y,xRef,(q,p)) = (eta^(-1) ||q-c(y,xRef)||^2 + ||p||^2)/2.

Thus c : E -> E -> E, Phi : E -> E -> R -> (E x E) -> (E x E), and H : E -> E -> (E x E) -> R. These are the local definitions whose conclusions are conjoined in the statement. They introduce no further hypotheses or existential choices. The two vector coordinates q and p are independently quantified. The parameters y and xRef, and therefore grad V(xRef) and c(y,xRef), are held fixed when time is composed or differentiated.

The square root is the nonnegative real square root. Because eta > 0, sqrt(eta) > 0, eta^(-1) = 1/eta, and (sqrt(eta))^(-1) = 1/sqrt(eta). The coefficient -sin(t)/sqrt(eta) is a negative real quotient. In the derivative below, -(sqrt(eta))^(-1) means the negative of the reciprocal of sqrt(eta). Time and both composition times range over all real numbers, including zero and negative times; they are not restricted to a nonnegative interval.

All nine following conclusions hold simultaneously.

1. **Joint continuity.** The map F : (E x E) x (R x (E x E)) -> E x E given by F((y,xRef),(t,z)) = Phi(y,xRef,t,z) is continuous for the product topologies.

2. **Joint measurability.** The same F is measurable for the product measurable structures and the product measurable structure on E x E. The given measurable structure on E is Borel. This is measurability of a deterministic map, with no probability measure supplied.

3. **Identity at zero time.** For every y, xRef in E and every z in E x E, Phi(y,xRef,0,z) = z.

4. **Composition law.** For every y, xRef in E, s,t in R, and z in E x E,

       Phi(y,xRef,s+t,z) = Phi(y,xRef,s,Phi(y,xRef,t,z)).

   Both maps on the right have the same y and xRef, and the outer map is at time s.

5. **Both inverse identities.** For every y, xRef in E, t in R, and z in E x E,

       Phi(y,xRef,-t,Phi(y,xRef,t,z)) = z,
       Phi(y,xRef,t,Phi(y,xRef,-t,z)) = z.

6. **The two time derivatives.** Fix any y, xRef in E and z in E x E. Put q_t = (Phi(y,xRef,t,z)).1 and p_t = (Phi(y,xRef,t,z)).2. At every t in R, the E-valued functions of real time have derivatives in the norm sense specified by HasDerivAt:

       (d/ds at s=t) (Phi(y,xRef,s,z)).1 = sqrt(eta) p_t,
       (d/ds at s=t) (Phi(y,xRef,s,z)).2
         = -(sqrt(eta))^(-1) (q_t-y) - sqrt(eta) grad V(xRef).

   Both derivative assertions hold at the same arbitrary t. The first coordinate derivative is scaled by sqrt(eta), not by 1. The gradient in the second derivative is evaluated at the fixed xRef. The reciprocal coefficient acts on q_t-y, with the separate displayed gradient term.

7. **Nonnegativity.** For every y, xRef in E and z in E x E, 0 <= H(y,xRef,z).

8. **Conservation.** For every y, xRef in E, t in R, and z in E x E,

       H(y,xRef,Phi(y,xRef,t,z)) = H(y,xRef,z).

9. **Time-pi identity.** For every y, xRef in E and z=(q,p) in E x E,

       Phi(y,xRef,pi,z) = (2 c(y,xRef)-q,-p).

   Here pi is the usual real pi, 2 c denotes real scalar multiplication, and -p is additive negation in E.

The ambient structure, V, alpha, beta and eta are outer parameters, subject to the assumptions above. Each universal quantifier inside a numbered conclusion is local to that conclusion. There is no restriction on y or xRef, no relation required between them, and no restriction on either component of z. No positive-dimensional or nonzero-coordinate condition is assumed. The only strict scalar positivity assumptions are alpha > 0 and eta > 0; beta > 0 follows from alpha <= beta. All formulas depend on the given V through grad V(xRef), and on eta; alpha and beta enter as global hypothesis constants and do not occur in c, Phi or H. No additional constants are existentially asserted. The conclusions specify no stochastic process, distributional preservation, sampling statement, numerical discretization error, or quantitative convergence rate.
