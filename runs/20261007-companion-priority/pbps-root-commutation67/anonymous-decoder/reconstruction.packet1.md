# Anonymous reconstruction 1

Let E be a finite-dimensional real inner product space with its normed additive commutative group structure and its Borel measurable structure. Let V:E->R be twice continuously Frechet differentiable, alpha,beta nonnegative real parameters, and eta real. Assume 0<alpha, alpha<=beta, eta>0, beta*eta<=1 and, for every x,v:E,
  alpha*||v||^2 <= (D(DV)(x)[v])[v] <= beta*||v||^2.
Real formulas use the real coercions of alpha,beta. DV(x) and D(DV)(x)[v] are bounded real-linear functionals on E. These are precisely the original public data, structures and premises.

Define mu=volume.tilted(x->-V(x)), normalized exponential tilting. Let J be the pushforward of mu times stdGaussian(E) by (x,z)->(x,x+sqrt(eta)*z), and nu=J.snd. Define Lambda as the pushforward of J by (x,y)->(y,2*x-y), and F(x,y)=(x,2*x-y). J uses coordinates (x,y), Lambda uses coordinates (y,2*x-y).

Use the product measurable structure on E x E. Let mY be the comap of E's measurable structure by the second-coordinate map, with containment in the product sigma algebra internally derived from measurability of that map. Set H=L2(J), K=L2(nu), complete real Hilbert spaces of square-integrable AE classes, and HP=lpMeas(R,R,mY,2,J), the closed mY-measurable subspace of H. Write i:HP->H for inclusion and pi:H->HP for orthogonal projection. Define P:H->H as inclusion composed with L2 conditional expectation onto mY. Let M:K->H be the real-linear isometric pullback by the second-coordinate map, with the measure-preserving witness internally derived from nu=J.snd.

Then mu,J,nu are probability measures; HP=range(P.toLinearMap); and P(i(f))=i(f) for every f:HP.

There exists a Markov kernel S from E to E with, for every y:E, exact equality of measures
  S(y)=volume.tilted(x->-V((y+x)/2)-||y-x||^2/(8*eta)).
This is a normalized every-state formula. S is a conditional kernel of Lambda in the supplied IsCondKernel sense, giving the second coordinate conditioned on the first. Lambda.fst=nu and Lambda.snd=nu.

There exists a real-linear isometric equivalence e:K->HP onto that exact subspace, with i(e(u))=M(u) for every u:K. There exists a real-linear isometry U:H->H such that for each g:H its representative U(g) equals g composed with F J-almost everywhere. U is involutive and its bounded operator is selfadjoint.

There exists a bounded real-linear endomorphism T:K->K which is selfadjoint and satisfies, for every u:K,
  ||T(u)||<=||u||,
  T(u)(y)=integral u(x) dS(y)(x) for nu-almost every y,
  integral T(u)(y) dnu(y)=integral u(y) dnu(y).
The U and T representative formulas are separately AE per observable, with no asserted common exceptional set.

Define A:HP->HP by A=pi composed with U composed with i, and B:HP->H by B=(I_H-P) composed with U composed with P composed with i. Then A=e composed with T composed with e^{-1}; A is selfadjoint and ||A(f)||<=||f|| for every f:HP; P(B(f))=0 for every f:HP.

There exists a positive bounded endomorphism Gamma:K->K with
  Gamma composed with Gamma=I_K-T composed with T,
  Gamma composed with T=T composed with Gamma.
Define GammaP:HP->HP by GammaP=e composed with Gamma composed with e^{-1}. Then GammaP is positive,
  GammaP composed with GammaP=I_HP-A composed with A,
  GammaP composed with A=A composed with GammaP,
  B.adjoint composed with B=GammaP composed with GammaP.
Here B.adjoint:H->HP. Gamma and GammaP are operators, not real scalar square roots. Positive means selfadjoint with nonnegative quadratic form. No positivity of T or A is asserted.

There exists q:K equal to 1 nu-almost everywhere, with T(q)=q and <q,u>_K=integral u(y) dnu(y) for every u:K. Set qP=e(q), and HP0=ker(innerSL R qP) inside HP: the kernel of f-><qP,f>_HP. HP0 receives the inherited normed additive group, real inner product and completeness from closedness of this kernel. Write j:HP0->HP for inclusion. Set
  gamma=2*sqrt(alpha*eta)/(1+alpha*eta).
For every f:HP, f belongs to HP0 if and only if integral (e^{-1}(f))(y) dnu(y)=0. Moreover GammaP(qP)=0 and gamma>0.

There exists a bounded endomorphism GammaP0:HP0->HP0 such that j(GammaP0(f))=GammaP(j(f)) for every f:HP0. It is positive, GammaP0-gamma*I_HP0 is positive, and it is a unit in the bounded endomorphism algebra of HP0. There exists a bounded endomorphism Inv:HP0->HP0 satisfying BOTH
  Inv composed with GammaP0=I_HP0,
  GammaP0 composed with Inv=I_HP0,
with operator-norm bound ||Inv||<=1/gamma. This same Inv is selfadjoint.

There exists a bounded endomorphism A0:HP0->HP0 such that, for every u:HP0,
  j(A0(u))=A(j(u)).
A0 is selfadjoint and satisfies
  A0 composed with GammaP0=GammaP0 composed with A0,
  A0 composed with A0 + GammaP0 composed with GammaP0=I_HP0,
  A0 composed with Inv=Inv composed with A0.
These identities use the SAME previously produced GammaP0 and its SAME two-sided inverse Inv on this exact centered space. A0 is an internally produced restriction; neither its existence nor these commutation identities are public premises. Positivity of A0 is not asserted. The sum-of-squares identity uses the operator GammaP0, not the scalar gamma.

Define Hperp=ker(P) inside H with inherited normed additive group, real inner product and completeness from closedness of P's kernel. Write k:Hperp->H for inclusion. This is the space of zero conditional expectation onto mY, not merely global mean zero.

There exists a bounded map B0:HP0->Hperp such that k(B0(f))=B(j(f)) for every f:HP0. There exists a bounded map V0:HP0->Hperp satisfying
  V0=B0 composed with Inv,
  B0=V0 composed with GammaP0,
  V0.adjoint composed with V0=I_HP0,
and ||V0(f)||=||f|| for every f:HP0. V0.adjoint:Hperp->HP0. This is an isometric embedding with a domain-side left inverse, without a surjectivity assertion or reverse identity V0 composed with V0.adjoint=I_Hperp.

There exists a bounded map R:H->Hperp such that for EVERY g:H,
  k(R(g))=g-P(g),
  B.adjoint(g)=j(B0.adjoint(R(g))).
The ambient B.adjoint has all H as domain and HP as codomain. B0.adjoint:Hperp->HP0 is applied after R extracts the complementary component. These formulas are not restricted to globally centered g or to g already in Hperp.

For every f:H with zero joint Bochner integral, integral f(z) dJ(z)=0, there exists fP:HP0 such that
  j(fP)=condExpL2(f),
where condExpL2 is the displayed conditional expectation H->HP for J and mY. Define fperp=R(f):Hperp and fV=V0.adjoint(fperp):HP0. Then
  B.adjoint(k(fperp))=j(GammaP0(fV)),
  j(GammaP0(fV))=GammaP(j(fV)),
  ||f||^2=||fP||^2+||fperp||^2,
  ||fV||<=||fperp||.
The norm structures are inherited exactly as above. The zero-integral condition is local to this final universal implication, not an extra premise for the entire theorem. fP is produced for each such f; fperp,fV are defined internally. No assertion fperp=V0(fV) or equality of their norms is made.

All original space, structure, potential and parameter data are universal under the public assumptions. Global witnesses are produced in dependent order S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R, followed by per-centered-f witness fP. Every other measure, projection, conjugate, subspace, compatibility fact and complete Hilbert instance is an internal definition or construction. Full-space invertibility of GammaP is not concluded; its constant kernel is explicit. No nontriviality or positive dimension is assumed for E,HP0,Hperp, and zero-space identities retain their own endomorphism-algebra meaning. Norm preservation by V0 does not assert operator norm 1 when HP0 is trivial. alpha=0 and eta=0 are excluded.

The approved context identifies the supplied expression as the literal expansion of a proposition-valued representation. That representation records this entire proposition, changes none of its original caller binders, and supplies neither a proof nor an extra mathematical premise. No source correctness, proof dependency between packets, theorem certification or compilation result is asserted by this reconstruction.

## objects

- Universal E,structures,V,alpha,beta,eta; definitions mu,J,nu,Lambda,F,mY,H,K,HP,P,M and inclusions i,j,k. Produced S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R. Per-centered-f produced fP and defined fperp=Rf,fV=V0.adjoint fperp.

## domains

- E finite-dimensional real inner product/Borel space. mu,nu on E; J,Lambda on product E x E; S:E to probability measures on E. Hessian form is (fderiv R (fderiv R V) x v) v.
- H=L2(J),K=L2(nu); HP=closed lpMeas(mY,2,J) inside H; HP0=ker(innerSL R qP) inside HP; Hperp=ker(P) inside H. Both kernel spaces have internally inherited complete Hilbert structures.
- i:HP->H,pi:H->HP,j:HP0->HP,k:Hperp->H; condExpL2:H->HP; P,U:H->H; M:K->H;e:K equiv_isometry HP.
- T,Gamma:K->K; A,GammaP:HP->HP; B:HP->H; B.adjoint:H->HP. GammaP0,Inv,A0:HP0->HP0; B0,V0:HP0->Hperp with adjoints:Hperp->HP0; R:H->Hperp.
- Every joint f in the final implication is in H; fP,fV in HP0 and fperp in Hperp. Final adjoint/restriction equalities have codomain HP.

## quantifiers

- Public universal binders: E; NormedAddCommGroup E; InnerProductSpace R E; FiniteDimensional R E; MeasurableSpace E; BorelSpace E; V:E->R; alpha,beta:nonnegative reals; eta:R; proof premises h_alpha,h_alpha_beta,h_V,h_H,h_eta,h_beta_eta.
- Both Hessian bounds hold for all x,v:E. S formula is every y:E. e coherence and T norm/integral statements and q pairing are every u:K. U action is per-g J-AE; T action per-u nu-AE.
- A contraction/P B=0/centered membership quantify all f:HP. GammaP0/A0 restrictions and B0 coherence/V0 norm equality quantify all inputs in HP0. R and ambient adjoint formulas quantify every g:H without centering.
- Dependent witness order S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R. For each f:H with zero J-integral, produce fP:HP0; then fperp,fV are defined from it and earlier maps. All complete-space, sigma-algebra and pullback compatibility witnesses are internal.

## assumptions

- The displayed five E structures, V:ContDiff R 2, alpha,beta nonnegative reals, eta real.
- 0<(alpha:R); alpha<=beta; for all x,v:E, (alpha:R)*||v||^2 <= (D(DV)(x)[v])[v] <= (beta:R)*||v||^2.
- 0<eta; (beta:R)*eta<=1. No caller normalization, probability, root, commutation, selfadjoint inverse, A0 restriction, isometric factorization, extra derivative or nontriviality premise.
- The zero J-integral assumption is the antecedent of the final universally quantified output implication only. A transparent Prop definition supplies no proof or additional premise.

## conclusion

- mu,J,nu probability; HP=range(P.toLinearMap); P fixes included HP. Exact every-state normalized Markov S formula; Lambda.IsCondKernel S and both Lambda marginals nu.
- Produced e coherent with M, involutive selfadjoint U implementing F J-AE per observable, and selfadjoint contraction T with S-integral action nu-AE per observable and preserved nu integral.
- A=pi U i=e T e^{-1} selfadjoint/contractive; B=(I_H-P) U P i and P Bf=0.
- Positive Gamma with Gamma^2=I_K-T^2 AND Gamma T=T Gamma. GammaP=e Gamma e^{-1} positive with GammaP^2=I_HP-A^2 AND GammaP A=A GammaP; B.adjoint B=GammaP^2.
- Produced q=1 nu-AE, Tq=q, integral pairing. qP=e(q), exact centered HP0 membership, GammaP qP=0 and gamma>0.
- Positive restricted GammaP0 obeys GammaP0-gamma I positive and IsUnit. SAME Inv is two-sided inverse, ||Inv||<=1/gamma AND selfadjoint.
- Produced A0:HP0->HP0 restricts A after j, is selfadjoint, commutes with SAME GammaP0, satisfies A0^2+GammaP0^2=I_HP0, and commutes with SAME Inv.
- Produced B0 agrees after inclusions with B. V0=B0 Inv, B0=V0 GammaP0, V0.adjoint V0=I_HP0, and every-vector norm preservation.
- Produced R:H->Hperp with k(Rg)=g-Pg and B.adjoint g=j(B0.adjoint(Rg)) for EVERY g:H.
- For every f:H with integral f dJ=0: produced fP in HP0 with j(fP)=condExpL2 f; fperp=Rf,fV=V0.adjoint fperp; B.adjoint(k fperp)=j(GammaP0 fV)=GammaP(j fV); ||f||^2=||fP||^2+||fperp||^2 and ||fV||<=||fperp||.

## scopes

- Normalized tilt; endomorphism products mean composition; isometric conjugation means e C e^{-1}; positivity means selfadjoint/nonnegative quadratic form. Scalar gamma differs from operator GammaP0 in sum-of-squares and inverse identities.
- Commute Gamma T, Commute GammaP A, Commute A0 GammaP0 and Commute A0 Inv are outputs, not new caller premises. T,A,A0 are selfadjoint where stated; positivity of those three is not asserted. No theorem/proof dependency with packet0 is inferred.
- Every-state S law differs from per-observable AE U/T action; no uniform null set. Hperp means zero conditional expectation, whereas final f has global joint centering and HP0 represents centered measurable components.
- Ambient B.adjoint acts on all H through R and B0.adjoint, not only Hperp. V0.adjoint V0 is a left-inverse isometry identity on HP0, with no onto or reverse-product assertion. Final corrector inequality does not assert fperp=V0 fV or equal norms.
- SAME GammaP0 and SAME Inv appear in centered restriction/commutation/factorization and final outputs. Both inverse identities are only on HP0. GammaP has its explicit constant kernel. Trivial spaces are permitted, alpha=0/eta=0 excluded, no norm(V0)=1 claim on trivial HP0.
- Transparent literal Prop representation changes no binder and supplies no proof/premise. No source-correctness, source-fidelity, theorem certification or compilation claim.

## constant_dependencies

- gamma=2*sqrt((alpha:R)*eta)/(1+(alpha:R)*eta)>0; inverse norm <=1/gamma. These explicit scalar bounds depend on alpha,eta; beta also constrains upper Hessian and beta*eta<=1.
- Constants sqrt(eta),reflection 2,midpoint 1/2,denominator 8*eta are exact. Identity/sum-of-squares, norm-preservation and corrector contraction have coefficient 1. No hidden constants, dimension factors, asymptotic rates or extra derivative assumptions.

## Reconstruction decision

Derived measures and nested witnesses under exact public binders, including all global-observable outputs; no source, proof or compilation verdict.

## Ambiguities

- No unresolved displayed-formula ambiguity. Implementation-level normalized-tilt and IsCondKernel conventions are retained at the abstraction supplied, without extra pointwise/source claims.
