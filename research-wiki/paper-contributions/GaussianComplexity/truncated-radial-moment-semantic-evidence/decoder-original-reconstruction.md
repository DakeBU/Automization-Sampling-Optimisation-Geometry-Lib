**Theorem.** Let $d,q\in\mathbb N$ satisfy $2q+1<d$. Let $E=\mathbb R^{q+1}$ with its Euclidean norm and Borel measurable structure, and let $\mu$ be the centered Gaussian probability measure on $E$ with independent variance-one coordinates in an orthonormal basis. Define
$$
R(x)=\|x\|^2,\qquad L=2(q+1)+3\log(1000d),
$$
where the expression for $L$ uses real arithmetic and $\log$ is the natural logarithm. Define the real-valued functions
$$
B(x)=\mathbf{1}_{\{x\in E\,:\,L<R(x)\}}(x)R(x)\quad(x\in E),\qquad
T(s)=\mu\bigl(\{x\in E\,:\,L+s<R(x)\}\bigr)\quad(s\in\mathbb R),
$$
where $B$ is zero outside the indicated set and $T(s)$ is the ordinary real mass of its event. Then

1. $B$ is integrable with respect to $\mu$ on $E$.
2. $T$ is integrable with respect to Lebesgue measure restricted to the open ray $(0,\infty)$.
3. The following equality holds.
   $$
   \int_E B(x)\,\mathrm d\mu(x)
   = L\,T(0)+\int_{(0,\infty)}T(s)\,\mathrm ds .
   $$
4. The same Gaussian integral satisfies
   $$
   \int_E B(x)\,\mathrm d\mu(x)\le \frac{L+3}{1000d}.
   $$

The integrals are real Bochner integrals. In the equality, $T(0)$ is the value at zero, namely the real mass of $\{x\in E\,:\,L<R(x)\}$.
