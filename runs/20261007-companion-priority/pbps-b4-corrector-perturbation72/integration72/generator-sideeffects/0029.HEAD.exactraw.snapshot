# Module card: `AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardInputLaw`

- **Purpose:** Realize Algorithm 3.1's first OU refresh and first finite Picard
  Gaussian array on their actual independent product law.
- **Blue declaration:**
  `PicardInputLaw.partial_refresh_with_picard_innovations`.
- **Inputs:** An incoming phase-state probability law with an integrable
  centered position-plus-momentum square bounded by a nonnegative budget.
- **Outputs:** Measurable refreshed state variables, their corrected moment
  budget, and measurable square-integrable Gaussian coordinates with exact
  second moment equal to the dimension.
- **Consumer:** `PicardCenterMoment.picard_center_gradient_moment`; the focused
  test passes the actual coordinate projections to it.
- **Red boundary:** The repeated Algorithm 3.1 law, the transport-derived
  run-wide state estimate, the second array/refresh, quadrature construction,
  numerical (D.7), (D.8), and Theorem 5.1 remain open.
- **Source:** Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Algorithm 3.1 and
  Lemma D.4.
