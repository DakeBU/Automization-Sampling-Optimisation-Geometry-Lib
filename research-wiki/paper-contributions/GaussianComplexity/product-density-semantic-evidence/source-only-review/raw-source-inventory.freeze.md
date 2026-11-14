# Raw source bounded inventory

Source SHA256: `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

Generated solely from the pinned HTML; every item has NODE or EXCLUDED(reason).

- NODE `S2.p1.1` (raw line 639): Standing Euclidean norm, identity, and Loewner-order conventions.
  Source: We write $\|\cdot\|$ for the Euclidean norm and $I_{d}$ for the $d\times d$ identity matrix. For symmetric matrices $A$ and $B$, the notation $A\preceq B$ means that $B-A$ is positive semidefinite.
- NODE `S2.p2.1` (raw line 645): Actual orthogonal group and determinant-conditioned Haar laws.
  Source: Let $O(n):=\{O\in\mathbb{R}^{n\times n}:O^{\top}O=I_{n}\}$ denote the real orthogonal group, equipped with Haar probability measure. It has two components, $\{\det O=+1\}$, $\{\det O=-1\}$, and each have Haar probability $1/2$. For $b\in\{-1,+1\}$, we write $\mu_{n,b}$ for Haar probability measure conditioned on $\det O=b$.
- NODE `S2.SS0.SSS0.Px1.p1.1` (raw line 658): Typing/standing precision-class context only; algorithmic motivation is not a premise.
  Source: We restrict the target class to centered Gaussians. This restriction removes the hardness of locating the target and isolates the difficulty of sampling with an unknown covariance. For an integer $d\geq 1$ and a parameter $\kappa\geq 1$, without loss of generality, we normalize the spectral bounds to $1$ and $\kappa$ by rescaling and consider the precision class
- NODE `S2.Ex1` (raw line 663): Precision class and spectral normalization for the actual Gaussian target.
  Source: $\mathcal{A}_{d,\kappa}:=\left\{A\in\mathbb{R}^{d\times d}:A=A^{\top},\quad I_{d}\preceq A\preceq\kappa I_{d}\right\}.$
- NODE `S2.SS0.SSS0.Px1.p1.2` (raw line 670): Actual target pi_A=N(0,A^{-1}); oracle clause is excluded as a subregion.
  Source: An input $A\in\mathcal{A}_{d,\kappa}$ specifies the quadratic potential $f_{A}(x):=\frac{1}{2}x^{\top}Ax$ and the target distribution $\pi_{A}:=N(0,A^{-1})$. At a point $x\in\mathbb{R}^{d}$, the exact first-order oracle returns
- EXCLUDED `S2.E1` (raw line 674): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: $\operatorname{FO}_{A}(x):=\bigl(f_{A}(x),\nabla f_{A}(x)\bigr)=\left(\frac{1}{2}x^{\top}Ax,Ax\right).$ (1)
- EXCLUDED `S2.SS0.SSS0.Px1.p2.1` (raw line 684): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: On this class, exact first-order access is equivalent to exact matrix–vector access. Indeed, a first-order response contains $Ax$, while a matrix–vector response determines both the gradient $Ax$ and the function value $\frac{1}{2}\langle x,Ax\rangle$. Thus the exact value-and-gradient, gradient-only, and matrix–vector query complexities coincide.
- EXCLUDED `S2.SS0.SSS0.Px2.p1.1` (raw line 697): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: A randomized algorithm chooses its queries and stopping decisions as Borel functions of its internal randomness and previous oracle responses, where the randomness is independent of the input. Its output may be any $\mathbb{R}^{d}$-valued Borel function of the same information. The algorithm has fixed query budget $T$ if it makes at most $T$ queries for every admissible input and every realization of its internal randomness.
- NODE `S2.SS0.SSS0.Px3.p1.1` (raw line 711): TV convention, used in consumer Ex69/Ex72 only.
  Source: For probability measures $P$ and $Q$ on a common measurable space, their total variation distance is
- NODE `S2.Ex2` (raw line 713): TV density formula, used in consumer Ex69/Ex72 only.
  Source: $\operatorname{TV}(P,Q):=\sup_{B}|P(B)-Q(B)|=\frac{1}{2}\int|p-q|\,d\lambda,$
- NODE `S2.SS0.SSS0.Px3.p1.2` (raw line 720): Common dominating measure convention; bounded-test clause is upstream separation context only.
  Source: where the supremum ranges over measurable sets, and $p$ and $q$ are the densities of $P$ and $Q$ with respect to any common dominating measure $\lambda$. In particular, $|\mathbb{E}_{P}h-\mathbb{E}_{Q}h|\leq\operatorname{TV}(P,Q)$ for every measurable function $h$ taking values in $[0,1]$.
- EXCLUDED `S2.SS0.SSS0.Px4.p1.1` (raw line 732): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: For a fixed input $A$, let $\rho_{A}^{\mathrm{Alg}}$ denote the law of the algorithm’s output, with all internal randomness included. For $0<\varepsilon<1$, define
- EXCLUDED `S2.E2` (raw line 736): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: $Q_{G}(d,\kappa,\varepsilon):=\inf\left\{T\in\mathbb{Z}_{\geq 0}:\begin{array}[]{l}\exists\,\mathrm{Alg}\text{ with fixed query budget }T\\[2.0pt] \text{such that }\displaystyle\sup_{A\in\mathcal{A}_{d,\kappa}}\operatorname{TV}\bigl(\rho_{A}^{\mathrm{Alg}},\pi_{A}\bigr)\leq\varepsilon\end{array}\right\}.$ (2)
- EXCLUDED `S2.SS0.SSS0.Px4.p1.2` (raw line 746): Oracle/algorithm/query-complexity content has no role in Ex70 density or Ex71/Ex72 integration.
  Source: The accuracy requirement is uniform over inputs and concerns the output law after averaging over the algorithm’s seed. Throughout the paper, query budgets are deterministic caps on the number of queries in each run, rather than bounds on the expected number of queries.
- NODE `S3.SS1.p1.1` (raw line 792): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: Fix $\kappa\geq 4$. Let $3\leq n\leq d$ be the block dimension and $k:=\lfloor d/n\rfloor$ the number of blocks. In the proof of the main theorem, we choose $n=2T+1$, where $T$ is the algorithm’s query budget. This choice applies when $T\geq 1$ and $2T+1\leq d$. The remaining cases are treated separately. For $O\in O(n)$, define
- NODE `S3.E4` (raw line 800): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: $A_{O}:=\frac{\kappa+1}{2}I_{n}-\frac{\kappa-1}{4}(O+O^{\top}).$ (4)
- NODE `S3.SS1.p1.2` (raw line 808): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: For $\bm{O}=(O_{1},\ldots,O_{k})\in O(n)^{k}$, set
- NODE `S3.E5` (raw line 809): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: $A_{\bm{O}}:=\operatorname{diag}\bigl(A_{O_{1}},\ldots,A_{O_{k}},I_{d-kn}\bigr).$ (5)
- NODE `S3.SS1.p2.1` (raw line 819): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: For each $b\in\{-1,+1\}$, draw $O_{1},\ldots,O_{k}$ independently from $\mu_{n,b}$, and let $\mathcal{D}_{b}$ denote the law of $A_{\bm{O}}$. Thus the orthogonal matrices share the same determinant sign.
- NODE `S3.SS1.p3.1` (raw line 825): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: Writing $P_{b}:=\mathbb{E}_{O\sim\mu_{n,b}}[N(0,A_{O}^{-1})]$ for the single-block target mixture, the averaged target under $\mathcal{D}_{b}$ is
- NODE `S3.E6` (raw line 829): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: $\bar{\pi}_{b}:=\mathbb{E}_{A\sim\mathcal{D}_{b}}[\pi_{A}]=P_{b}^{\otimes k}\otimes N(0,I_{d-kn}).$ (6)
- NODE `S3.SS1.p3.2` (raw line 837): Actual source family/prior/product-law construction; query-budget subregion is separately excluded.
  Source: When $kn=d$, the identity block and the final Gaussian factor are omitted.
- EXCLUDED `A2.SS2::citation-occurrence-1` (raw line 2321): Section introduction/navigation only; target destination is recorded separately.
  Source: 3.3
- EXCLUDED `A2.SS2.p1.1` (raw line 2324): Section introduction/navigation only; target destination is recorded separately.
  Source: In this section, we prove Lemma 3.3.
- EXCLUDED `A2.SS2.p1.1::citation-occurrence-1` (raw line 2324): Section introduction/navigation only; target destination is recorded separately.
  Source: 3.3
- NODE `A2.Thmtheorem5.p1.1` (raw line 2329): Separation destination context; not a prerequisite of Ex70.
  Source: The averaged targets satisfy
- NODE `A2.E14` (raw line 2330): Separation destination context; not a prerequisite of Ex70.
  Source: $\operatorname{TV}(\bar{\pi}_{+1},\bar{\pi}_{-1})\geq 1-\exp\left\{-\frac{k}{8}\exp\left(-\frac{10n}{\sqrt{\kappa}}\right)\right\}.$ (14)
- NODE `A2.SS2.p2.1` (raw line 2341): Standing n/kappa/Haar conventions and actual p_O/p_b density definitions.
  Source: We first separate the single-block mixtures using a bounded radial test, and then amplify this separation across independent blocks. The single-block argument combines a cancellation identity for Gaussian normalization factors with two spherical Poisson identities. Throughout this section, $n\geq 3$, $\kappa\geq 4$, and $O$ is Haar distributed on the full orthogonal group $O(n)$. Write $U:=O_{11}$, let $p_{O}$ be the density of $N(0,A_{O}^{-1})$, and let $p_{b}$ be the density of $P_{b}$, for $b\in\{-1,+1\}$.
- EXCLUDED `A2.SS2.SSS1.p1.1` (raw line 2354): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: The difference between averages over the two determinant components can be expressed as a Haar expectation weighted by $\det(O)$. The next lemma evaluates this signed expectation when the integrand contains the Gaussian normalization factor $\sqrt{\det A_{O}}$ and otherwise depends only on $U$.
- EXCLUDED `A2.Thmtheorem6.p1.2` (raw line 2363): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: For every Borel function $h$ with $\mathbb{E}|h(U)|<\infty$,
- EXCLUDED `A2.E15` (raw line 2364): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\displaystyle\mathbb{E}\left[\det(O)\sqrt{\det A_{O}}\,h(U)\right]=\frac{(-1)^{n-1}(\sqrt{\kappa}-1)^{n-1}}{2^{n}}\mathbb{E}\left[\bigl((\sqrt{\kappa}+1)U-(\sqrt{\kappa}-1)\bigr)h(U)\right].$ (15)
- EXCLUDED `A2.SS2.SSS1.p2.2` (raw line 2378): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: We first express the normalization factor as a determinant. The definition of $A_{O}$ gives
- EXCLUDED `A2.E16` (raw line 2380): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $A_{O}=\frac{1}{4}\bigl((\sqrt{\kappa}+1)I_{n}-(\sqrt{\kappa}-1)O\bigr)^{\top}\bigl((\sqrt{\kappa}+1)I_{n}-(\sqrt{\kappa}-1)O\bigr).$ (16)
- EXCLUDED `A2.SS2.SSS1.p2.3` (raw line 2388): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: For $0\leq t\leq\sqrt{\kappa}-1$ and $v\in\mathbb{R}^{n}$,
- EXCLUDED `A2.Ex52` (raw line 2389): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\|((\sqrt{\kappa}+1)I_{n}-tO)v\|\geq(\sqrt{\kappa}+1-t)\|v\|\geq 2\|v\|.$
- EXCLUDED `A2.SS2.SSS1.p2.4` (raw line 2396): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: Thus $(\sqrt{\kappa}+1)I_{n}-tO$ is invertible throughout this interval. Its determinant is positive at $t=0$ and remains positive by continuity. Hence Eq. (16) implies
- EXCLUDED `A2.SS2.SSS1.p2.4.1::citation-occurrence-1` (raw line 2398): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: 16
- EXCLUDED `A2.E17` (raw line 2400): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\sqrt{\det A_{O}}=\frac{1}{2^{n}}\det\bigl((\sqrt{\kappa}+1)I_{n}-(\sqrt{\kappa}-1)O\bigr).$ (17)
- EXCLUDED `A2.SS2.SSS1.p2.5` (raw line 2408): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: Multiplying the matrix inside the determinant by $O^{\top}$, and using $\det(O^{\top})=\det(O)$, yields
- EXCLUDED `A2.E18` (raw line 2410): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\displaystyle\det(O)\sqrt{\det A_{O}}$ $\displaystyle=\frac{1}{2^{n}}\det\bigl((\sqrt{\kappa}+1)O^{\top}-(\sqrt{\kappa}-1)I_{n}\bigr)$ (18) $\displaystyle=\frac{1}{2^{n}}\det\bigl((\sqrt{\kappa}+1)O-(\sqrt{\kappa}-1)I_{n}\bigr),$
- EXCLUDED `A2.SS2.SSS1.p2.6` (raw line 2424): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: where the last equality follows by transposing.
- EXCLUDED `A2.SS2.SSS1.p3.1` (raw line 2427): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: We next identify the principal minors that survive averaging. For $S\subseteq\{1,\ldots,n\}$, write $O_{S,S}$ for the corresponding principal submatrix, with $\det O_{\varnothing,\varnothing}=1$. If $S$ contains an index $i\geq 2$, the row reflection $D_{i}:=I_{n}-2e_{i}e_{i}^{\top}$ satisfies
- EXCLUDED `A2.Ex53` (raw line 2433): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $D_{i}O\overset{d}{=}O,\qquad(D_{i}O)_{11}=U,\qquad\det((D_{i}O)_{S,S})=-\det O_{S,S}.$
- EXCLUDED `A2.SS2.SSS1.p3.2` (raw line 2440): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: Consequently,
- EXCLUDED `A2.Ex54` (raw line 2441): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\displaystyle\mathbb{E}[\det O_{S,S}h(U)]$ $\displaystyle=\mathbb{E}\left[\det((D_{i}O)_{S,S})h((D_{i}O)_{11})\right]$ $\displaystyle=-\mathbb{E}[\det O_{S,S}h(U)],$
- EXCLUDED `A2.SS2.SSS1.p3.3` (raw line 2454): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: so this expectation is zero. All expectations are finite because $|\det O_{S,S}|\leq 1$. Thus only $S=\varnothing$ and $S=\{1\}$ contribute when we expand Eq. (18) in principal minors:
- EXCLUDED `A2.SS2.SSS1.p3.3.1::citation-occurrence-1` (raw line 2457): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: 18
- EXCLUDED `A2.Ex55` (raw line 2458): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: $\displaystyle\mathbb{E}[\det(O)\sqrt{\det A_{O}}\,h(U)]$ $\displaystyle=\frac{1}{2^{n}}\sum_{S\subseteq\{1,\ldots,n\}}(\sqrt{\kappa}+1)^{|S|}\bigl(-(\sqrt{\kappa}-1)\bigr)^{n-|S|}\mathbb{E}[\det O_{S,S}h(U)]$ $\displaystyle=\frac{1}{2^{n}}\left[\bigl(-(\sqrt{\kappa}-1)\bigr)^{n}\mathbb{E}[h(U)]+(\sqrt{\kappa}+1)\bigl(-(\sqrt{\kappa}-1)\bigr)^{n-1}\mathbb{E}[Uh(U)]\right]$ $\displaystyle=\frac{(-1)^{n-1}(\sqrt{\kappa}-1)^{n-1}}{2^{n}}\mathbb{E}\left[\bigl((\sqrt{\kappa}+1)U-(\sqrt{\kappa}-1)\bigr)h(U)\right].$
- EXCLUDED `A2.SS2.SSS1.p3.4` (raw line 2481): Determinant-cancellation proof is not an ancestor of actual Ex70 or Ex71; upstream proof of the separately cited B.7 is outside this minimal packet.
  Source: ∎
- EXCLUDED `A2.SS2.SSS2.p1.1` (raw line 2489): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: We distinguish $P_{+1}$ and $P_{-1}$ using a test of the form $x\mapsto e^{-\lambda\|x\|^{2}}$. After Gaussian integration and determinant cancellation, its expectation difference reduces to a spherical integral. The following identities evaluate that integral.
- EXCLUDED `A2.SS2.SSS2.p2.1` (raw line 2496): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Choosing $\lambda$ so that these identities apply gives the following quantitative separation.
- NODE `A2.Thmtheorem7.p1.1` (raw line 2502): B.7 statement is a consumer-side input to Eq25 and Ex72, never an ancestor of Ex70.
  Source: For $n\geq 3$ and $\kappa\geq 4$,
- NODE `A2.E19` (raw line 2503): B.7 statement is a consumer-side input to Eq25 and Ex72, never an ancestor of Ex70.
  Source: $\operatorname{TV}(P_{+1},P_{-1})\geq\frac{\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{n}}{2+\frac{4n\sqrt{\kappa}}{(\sqrt{\kappa}+1)^{2}}}\geq\frac{1}{2}e^{-5n/\sqrt{\kappa}}.$ (19)
- EXCLUDED `A2.SS2.SSS2.p3.1` (raw line 2516): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: For $\lambda\geq 0$, let $h_{\lambda}(x):=e^{-\lambda\|x\|^{2}}$ and define
- EXCLUDED `A2.Ex56` (raw line 2518): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $H(\lambda):=\mathbb{E}\left[\det(O)\int_{\mathbb{R}^{n}}h_{\lambda}(x)p_{O}(x)\,dx\right].$
- EXCLUDED `A2.SS2.SSS2.p3.2` (raw line 2525): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Since the two determinant components have Haar probability $1/2$,
- EXCLUDED `A2.Ex57` (raw line 2526): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $H(\lambda)=\frac{1}{2}\left(\mathbb{E}_{P_{+1}}h_{\lambda}-\mathbb{E}_{P_{-1}}h_{\lambda}\right).$
- EXCLUDED `A2.SS2.SSS2.p3.3` (raw line 2533): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: As $0<h_{\lambda}\leq 1$, it follows that
- EXCLUDED `A2.E20` (raw line 2534): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\operatorname{TV}(P_{+1},P_{-1})\geq 2|H(\lambda)|.$ (20)
- EXCLUDED `A2.SS2.SSS2.p3.4` (raw line 2542): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: We compute $H(\lambda)$ and then choose $\lambda>0$.
- EXCLUDED `A2.SS2.SSS2.p4.1` (raw line 2545): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: For every $Q\in O(n)$, conjugation preserves Haar measure and the determinant sign, while $A_{QOQ^{\top}}=QA_{O}Q^{\top}$ and $p_{QOQ^{\top}}(Qx)=p_{O}(x)$. Consequently, for every $x\in\mathbb{R}^{n}$,
- EXCLUDED `A2.Ex58` (raw line 2549): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\mathbb{E}[\det(O)p_{O}(x)]=\mathbb{E}[\det(O)p_{O}(\|x\|e_{1})].$
- EXCLUDED `A2.SS2.SSS2.p4.2` (raw line 2556): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: At $\|x\|e_{1}$, the Gaussian exponent depends on $O$ only through $U$, since $e_{1}^{\top}A_{O}e_{1}=(\kappa+1-(\kappa-1)U)/2$. Moreover, $I_{n}\preceq A_{O}\preceq\kappa I_{n}$ gives the integrable bound
- EXCLUDED `A2.Ex59` (raw line 2561): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $h_{\lambda}(x)p_{O}(\|x\|e_{1})\leq\left(\frac{\kappa}{2\pi}\right)^{n/2}e^{-\|x\|^{2}/2}.$
- EXCLUDED `A2.SS2.SSS2.p4.3` (raw line 2568): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Using $|\det(O)|=1$, Fubini’s theorem, and Gaussian integration, we obtain
- EXCLUDED `A2.Ex60` (raw line 2570): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle H(\lambda)$ $\displaystyle=\frac{1}{(2\pi)^{n/2}}\mathbb{E}\left[\det(O)\sqrt{\det A_{O}}\int_{\mathbb{R}^{n}}e^{-[\kappa+1+4\lambda-(\kappa-1)U]\|x\|^{2}/4}\,dx\right]$ $\displaystyle=2^{n/2}\mathbb{E}\left[\frac{\det(O)\sqrt{\det A_{O}}}{(\kappa+1+4\lambda-(\kappa-1)U)^{n/2}}\right],$
- EXCLUDED `A2.SS2.SSS2.p4.4` (raw line 2583): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: where $\int_{\mathbb{R}^{n}}e^{-a\|x\|^{2}/4}\,dx=(4\pi/a)^{n/2}$ for $a>0$. The denominator is at least $2+4\lambda$, so Lemma B.6 applies with $h(u)=(\kappa+1+4\lambda-(\kappa-1)u)^{-n/2}$ and gives
- EXCLUDED `A2.SS2.SSS2.p4.4.1::citation-occurrence-1` (raw line 2586): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: B.6
- EXCLUDED `A2.E21` (raw line 2588): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $H(\lambda)=\frac{(-1)^{n-1}(\sqrt{\kappa}-1)^{n-1}}{2^{n/2}}\mathbb{E}\left[\frac{(\sqrt{\kappa}+1)U-(\sqrt{\kappa}-1)}{(\kappa+1+4\lambda-(\kappa-1)U)^{n/2}}\right].$ (21)
- EXCLUDED `A2.SS2.SSS2.p4.5` (raw line 2596): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Since $Oe_{1}$ is uniform on $\mathbb{S}^{n-1}$, Lemma A.1 applies to $U$.
- EXCLUDED `A2.SS2.SSS2.p4.5.1::citation-occurrence-1` (raw line 2597): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: A.1
- EXCLUDED `A2.SS2.SSS2.p5.4` (raw line 2600): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: We now match the denominator with a positive multiple of $1+r^{2}-2rU$. At $\lambda=0$, this matching gives $r=(\sqrt{\kappa}-1)/(\sqrt{\kappa}+1)$, but $H(0)=0$ because both target distributions have total mass one. We therefore decrease $r$ by a factor $1-1/n$ and set
- EXCLUDED `A2.E22` (raw line 2606): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle r$ $\displaystyle:=\left(1-\frac{1}{n}\right)\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1},$ (22) $\displaystyle\lambda$ $\displaystyle:=\frac{\kappa-1}{8r}(1+r^{2})-\frac{\kappa+1}{4}=\frac{4n\sqrt{\kappa}+(\sqrt{\kappa}-1)^{2}}{8n(n-1)}.$
- EXCLUDED `A2.SS2.SSS2.p5.5` (raw line 2620): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Then $0<r<1$, $\lambda>0$, and
- EXCLUDED `A2.E23` (raw line 2621): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle\kappa+1+4\lambda-(\kappa-1)U$ $\displaystyle=\frac{\kappa-1}{2r}(1+r^{2}-2rU)$ (23) $\displaystyle=\frac{n(\sqrt{\kappa}+1)^{2}}{2(n-1)}(1+r^{2}-2rU).$
- EXCLUDED `A2.SS2.SSS2.p5.6` (raw line 2635): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: The two Poisson identities yield
- EXCLUDED `A2.Ex61` (raw line 2636): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle\mathbb{E}\left[\frac{(\sqrt{\kappa}+1)U-(\sqrt{\kappa}-1)}{(1+r^{2}-2rU)^{n/2}}\right]$ $\displaystyle=\frac{(\sqrt{\kappa}+1)r-(\sqrt{\kappa}-1)}{1-r^{2}}$ $\displaystyle=-\frac{\sqrt{\kappa}-1}{n(1-r^{2})}.$
- EXCLUDED `A2.SS2.SSS2.p5.7` (raw line 2649): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Substitution into Eq. (21) gives
- EXCLUDED `A2.SS2.SSS2.p5.7.1::citation-occurrence-1` (raw line 2649): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: 21
- EXCLUDED `A2.E24` (raw line 2650): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle H(\lambda)$ $\displaystyle=\frac{(-1)^{n-1}(\sqrt{\kappa}-1)^{n-1}}{(\sqrt{\kappa}+1)^{n}}\left(1-\frac{1}{n}\right)^{n/2}\left(-\frac{\sqrt{\kappa}-1}{n(1-r^{2})}\right)$ (24) $\displaystyle=\frac{(-1)^{n}}{n}\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{n}\frac{(1-1/n)^{n/2}}{1-r^{2}}.$
- EXCLUDED `A2.SS2.SSS2.p6.1` (raw line 2666): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: It remains to lower-bound the test gap. Since $n/2\geq 1$, convexity of $t\mapsto t^{n/2}$ implies
- EXCLUDED `A2.Ex62` (raw line 2668): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\left(1-\frac{1}{n}\right)^{n/2}\geq 1-\frac{n}{2}\cdot\frac{1}{n}=\frac{1}{2}.$
- EXCLUDED `A2.SS2.SSS2.p6.2` (raw line 2675): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Also,
- EXCLUDED `A2.Ex63` (raw line 2676): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle n(1-r^{2})$ $\displaystyle=\frac{4n\sqrt{\kappa}}{(\sqrt{\kappa}+1)^{2}}+\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{2}\left(2-\frac{1}{n}\right)$ $\displaystyle\leq\frac{4n\sqrt{\kappa}}{(\sqrt{\kappa}+1)^{2}}+2.$
- EXCLUDED `A2.SS2.SSS2.p6.3` (raw line 2689): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Together with Eq. (20) and Eq. (24), these estimates give
- EXCLUDED `A2.SS2.SSS2.p6.3.1::citation-occurrence-1` (raw line 2689): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: 20
- EXCLUDED `A2.SS2.SSS2.p6.3.1::citation-occurrence-2` (raw line 2690): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: 24
- EXCLUDED `A2.Ex64` (raw line 2691): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle\operatorname{TV}(P_{+1},P_{-1})$ $\displaystyle\geq\frac{2}{n}\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{n}\frac{(1-1/n)^{n/2}}{1-r^{2}}$ $\displaystyle\geq\frac{\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{n}}{2+\frac{4n\sqrt{\kappa}}{(\sqrt{\kappa}+1)^{2}}}.$
- EXCLUDED `A2.SS2.SSS2.p6.4` (raw line 2704): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: This proves the first claimed bound. For the second, $\kappa\geq 4$ implies
- EXCLUDED `A2.Ex65` (raw line 2706): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\displaystyle\log\left(\frac{\sqrt{\kappa}+1}{\sqrt{\kappa}-1}\right)$ $\displaystyle=2\int_{0}^{1/\sqrt{\kappa}}\frac{dt}{1-t^{2}}$ $\displaystyle\leq\frac{2}{\sqrt{\kappa}(1-\kappa^{-1})}\leq\frac{8}{3\sqrt{\kappa}}\leq\frac{3}{\sqrt{\kappa}}.$
- EXCLUDED `A2.SS2.SSS2.p6.5` (raw line 2719): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Hence $((\sqrt{\kappa}-1)/(\sqrt{\kappa}+1))^{n}\geq e^{-3n/\sqrt{\kappa}}$. Using $1+t\leq e^{t}$, we also have
- EXCLUDED `A2.Ex66` (raw line 2722): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $2+\frac{4n\sqrt{\kappa}}{(\sqrt{\kappa}+1)^{2}}\leq 2+\frac{4n}{\sqrt{\kappa}}\leq 2e^{2n/\sqrt{\kappa}}.$
- EXCLUDED `A2.SS2.SSS2.p6.6` (raw line 2729): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: Therefore,
- EXCLUDED `A2.Ex67` (raw line 2730): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: $\operatorname{TV}(P_{+1},P_{-1})\geq\frac{e^{-3n/\sqrt{\kappa}}}{2e^{2n/\sqrt{\kappa}}}=\frac{1}{2}e^{-5n/\sqrt{\kappa}}.$
- EXCLUDED `A2.SS2.SSS2.p6.7` (raw line 2737): Single-block separation derivation is outside actual Ex70/Ex71; B.7 statement is retained solely for the quantitative Ex72 consumer context.
  Source: ∎
- NODE `A2.SS2.SSS3.p1.1` (raw line 2745): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Under each prior, the $k$ blocks of a target sample are independent and have the same single-block mixture law. We convert the preceding separation into an upper bound on Hellinger affinity, which multiplies across independent blocks.
- NODE `A2.SS2.SSS3.2::citation-occurrence-1` (raw line 2751): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: 3.3
- NODE `A2.SS2.SSS3.p2.1` (raw line 2753): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Let $a$ denote the single-block Hellinger affinity:
- NODE `A2.Ex68` (raw line 2754): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $a:=\int_{\mathbb{R}^{n}}\sqrt{p_{+1}(x)p_{-1}(x)}\,dx.$
- NODE `A2.SS2.SSS3.p2.2` (raw line 2761): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Cauchy–Schwarz and $\int p_{+1}=\int p_{-1}=1$ give $0\leq a\leq 1$ and
- NODE `A2.Ex69` (raw line 2763): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $\displaystyle\operatorname{TV}(P_{+1},P_{-1})$ $\displaystyle=\frac{1}{2}\int_{\mathbb{R}^{n}}|\sqrt{p_{+1}}-\sqrt{p_{-1}}|(\sqrt{p_{+1}}+\sqrt{p_{-1}})$ $\displaystyle\leq\frac{1}{2}\left(\int_{\mathbb{R}^{n}}(\sqrt{p_{+1}}-\sqrt{p_{-1}})^{2}\right)^{1/2}\left(\int_{\mathbb{R}^{n}}(\sqrt{p_{+1}}+\sqrt{p_{-1}})^{2}\right)^{1/2}$ $\displaystyle=\frac{1}{2}\sqrt{(2-2a)(2+2a)}=\sqrt{1-a^{2}}.$
- NODE `A2.SS2.SSS3.p2.3` (raw line 2781): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Proposition B.7 therefore implies
- NODE `A2.SS2.SSS3.p2.3.1::citation-occurrence-1` (raw line 2781): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: B.7
- NODE `A2.E25` (raw line 2782): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $a\leq\sqrt{1-\frac{1}{4}e^{-10n/\sqrt{\kappa}}}\leq\exp\left\{-\frac{1}{8}e^{-10n/\sqrt{\kappa}}\right\},$ (25)
- NODE `A2.SS2.SSS3.p2.4` (raw line 2790): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: where the last inequality follows from $\log(1-t)\leq-t$ for $0\leq t<1$.
- NODE `A2.SS2.SSS3.p3.1` (raw line 2794): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Let $\bar{p}_{b}$ be the density of $\bar{\pi}_{b}$. When $kn<d$, write $\varphi_{d-kn}$ for the standard Gaussian density on $\mathbb{R}^{d-kn}$. By Eq. (6),
- NODE `A2.SS2.SSS3.p3.1.1::citation-occurrence-1` (raw line 2797): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: 6
- NODE `A2.Ex70` (raw line 2798): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $\bar{p}_{b}(x_{1},\ldots,x_{k},z)=\prod_{j=1}^{k}p_{b}(x_{j})\,\varphi_{d-kn}(z).$
- NODE `A2.SS2.SSS3.p3.2` (raw line 2805): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: Tonelli’s theorem and $\int\varphi_{d-kn}=1$ give
- NODE `A2.Ex71` (raw line 2806): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $\displaystyle\int_{\mathbb{R}^{d}}\sqrt{\bar{p}_{+1}(x)\bar{p}_{-1}(x)}\,dx$ $\displaystyle=\prod_{j=1}^{k}\left(\int_{\mathbb{R}^{n}}\sqrt{p_{+1}(x_{j})p_{-1}(x_{j})}\,dx_{j}\right)\int_{\mathbb{R}^{d-kn}}\varphi_{d-kn}(z)\,dz$ $\displaystyle=a^{k}.$
- NODE `A2.SS2.SSS3.p3.3` (raw line 2824): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: When $kn=d$, the same identity holds with the Gaussian factor omitted. Finally, $\min\{u,v\}\leq\sqrt{uv}$ for $u,v\geq 0$ implies
- NODE `A2.Ex72` (raw line 2827): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: $\displaystyle\operatorname{TV}(\bar{\pi}_{+1},\bar{\pi}_{-1})$ $\displaystyle=1-\int_{\mathbb{R}^{d}}\min\{\bar{p}_{+1}(x),\bar{p}_{-1}(x)\}\,dx$ $\displaystyle\geq 1-\int_{\mathbb{R}^{d}}\sqrt{\bar{p}_{+1}(x)\bar{p}_{-1}(x)}\,dx$ $\displaystyle=1-a^{k}$ $\displaystyle\geq 1-\exp\left\{-\frac{k}{8}e^{-10n/\sqrt{\kappa}}\right\},$
- NODE `A2.SS2.SSS3.p3.4` (raw line 2850): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: where the last step uses Eq. (25). ∎
- NODE `A2.SS2.SSS3.p3.4.1::citation-occurrence-1` (raw line 2850): Complete B.2.3 source step/definition/display or its explicit consumer citation.
  Source: 25
