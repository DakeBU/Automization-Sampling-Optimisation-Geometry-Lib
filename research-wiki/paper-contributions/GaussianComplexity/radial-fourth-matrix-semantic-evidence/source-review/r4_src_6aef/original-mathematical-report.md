# Independent anti-anchored source, exposition, and map review

## Original mathematical conclusion

The public producer's source fidelity is **equivalent after elaboration**.
All seven semantic slots match the pinned source. The explicit matrix
integrability is valid source-implicit content proved internally. There
is no blocking semantic delta and no repair is needed.

The complete authored local exposition and source/Lean map are also
accepted within their explicitly bounded scope. The private consumer is a
source-supported individual-summand inference, with Ex114 proved inside
it. It is not a separately printed source equation or the aggregate
variance/concentration theorem. Its review rests on this reviewer's
separately frozen whole-module reading, not on a decoder reconstruction
that does not cover it.

This report records the mathematical conclusion before consulting the
semantic core schema/validator for overlay formatting. Schema inspection
does not supply or change this conclusion.

## Exact inputs and independence

The exact generated reviewer packet was read. Its raw UTF-8 SHA-256 is
`61be7c0ee9e28ac4ef16d1963dd69b20e01a2918e152934e132cc3a73883477b`;
its canonical packet SHA-256 is
`c6639fe4bda9880f438e7d9c576f444ff448c1f92b3d37821d38f8e30e498e62`.
The canonical hash was reproduced from the packet without its packet hash
field, using sorted-key compact UTF-8 JSON. Its publication binding is
`128fff581c818c13f03d208c546c685e910ade6a30a202e7bee34ce60aa79179`.

The source pin remains the original HTML SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The raw original source reconstruction, selective-type judgment, and
complete code-only judgment were frozen earlier and remain unchanged.

Additional current inputs were the complete lesson
`website/content/declaration_lessons/huanjian-gaussian-radial-fourth-matrix.json`,
the complete corresponding publication JSON, and the root-authored source
map with SHA-256
`4215c8e8da2df765d7edb029c64f751a218cca5de0de6a04f462cdc19f185535`.
These are candidate claims being checked, not earlier review evidence.
The full current lesson unit agrees with the packet lesson on every field
included in the packet; the current unit additionally contains an explicit
remaining-boundary field. The packet's producer module equals the code-only
producer bytes. Current production P, T, and canonical ASTIS scalar provider
also still equal the earlier code-only inputs byte-for-byte.

Reviewer `/root/radial_fourth_fresh_source_6aef` differs from the formalizer
`huanjian_gc_20261111_radial_fourth_matrix` and anonymous decoder
`/root/neutral_decoder_72b6`. This reviewer did not act as either. The
packet reports the decoder's source-blind status; this phase does not
re-enact its run. The decoder's text and exact packet/run bindings are
review inputs. No compiler/native receipt, proof history, source graph,
other review verdict, or earlier foreign packet report was opened. The
packet's compiled flag and candidate prose about compilation were not
used as mathematical evidence.

## Seven semantic slots: source versus reconstruction

| Slot | Source meaning | Decoder reconstruction | Judgment |
| --- | --- | --- | --- |
| Objects | A row gamma_i~N(0,I_r), squared radius R_i, unnormalized rank-one matrix gamma_i gamma_i^T | Canonical stdGaussian vector x, R(x)=||x||^2, G(x)=xx^T, W(x)=R(x)G(x) | Equivalent naming and law formulation |
| Domains | r=q+1 real Euclidean coordinates; real r by r matrices | EuclideanSpace R (Fin(q+1)), real finite matrices with Euclidean operator norm and usual topology | Explicit elaboration of the source carriers and expectation space |
| Quantifiers | Each source row in the standing natural d,q range 2q+1<d | Every natural d,q with 2q+1<d, under the one fixed standard Gaussian law | Equivalent local-law quantification; it gives each identically distributed source row |
| Assumptions | Standard Gaussian row, r=q+1, standing 2q+1<d | Exactly that law and range; no extra moment, positivity, boundedness or regularity premise | Equivalent; no proof ingredient has become a premise |
| Conclusion | E[R_i gamma_i gamma_i^T]=(r+2)I_r using finite Gaussian fourth moments | Bochner integrability of W and exact integral (r+2)I | Explicit elaboration of source-implicit integrability plus the exact printed equation |
| Scopes/senses | Unconditional matrix expectation under the row's original Gaussian probability law | Real Bochner integral against the canonical Gaussian probability law, not Lebesgue or conditional law | Equivalent after elaboration; no totalized-integral shortcut |
| Constant dependencies | Exact r+2, independent of d and kappa in this local moment | Exact n+2=q+3 with n=q+1; independent of d | Same constant and dependencies |

The decoder uses n as a local alias for the dimension q+1. The paper uses
n=2q+1 for a separate cosine frequency, but that frequency is absent from
this public producer. The decoder's alias does not change or reinterpret
the paper's frequency variable. Its assertion ||W(x)||op=||x||^4 is true
for this nonnegative scalar times a rank-one matrix, including x=0.

At q=0, r=1, d>=2, and the theorem reduces to integrability and expectation
three for a scalar x^4 under N(0,1). The decoder says this explicitly.
There is no dimension-zero, nonzero-vector, or second-coordinate premise.

## Complete formulas and mathematical exposition

The lesson and publication assumptions provide all local objects: natural
d,q with 2q+1<d, r=q+1, canonical standard Gaussian row, squared radius,
source midpoint grid, row reindexing, cosine feature coordinates, explicit
Euclidean feature length, source cutoff L=2r+3 log(1000d), closed event R<=L,
original Gaussian expectation, and PSD order. Integrability is stated as
a proved conclusion, not a source premise.

The publication carries all three complete local formulas:

    E[R Z Z^T] = (r+2) I_r,  R=||Z||^2;

    Y_i = d^(-1) (Z Z^T tensor t_i t_i^T) 1_{R<=L},
    Y_i^2 = d^(-2) R ||t_i||^2
                 (Z Z^T tensor t_i t_i^T) 1_{R<=L};

    E[Y_i^2] <= ((r+2)||t_i||^2/d^2) (I_r tensor t_i t_i^T).

The lesson reproduces the moment formula and, beside its actual proof
steps, the complete square and individual PSD formulas. The five authored
steps explain quartic domination and matrix integrability; a single-
coordinate reflection for off-diagonal entries; scalar second/fourth and
independent mixed moments for the diagonal; actual rank-one/Kronecker
square algebra; and an integrable PSD residual whose expectation lies in
the closed convex PSD cone. These are formula proofs corresponding to
the actual code, not tactic paraphrases.

The last prose step calls its untruncated matrix W without a separate
displayed definition, but it is unambiguously the displayed square with
the indicator removed, and its exact literal definition appears in the
adjacent complete private code. This is mathematically sufficient in
the local progressive lesson. The proof step states residual
integrability, closedness/convexity, and transport of the exact producer
mean; none is silently made a public hypothesis.

The dependency list's named ASTIS scalar fourth-moment provider is the
same actual call in the producer. The direct consumer call to the new
producer uses both its integrability and its exact mean. Named Mathlib
dependencies agree with the operations reviewed in the complete code.
No source-facing assumption is licensed merely by listing a dependency.

## Exact adjacent code blocks and private citation

Every embedded code string was compared byte-for-byte with the earlier
complete exact module, including its final LF. All five comparisons pass:

| Lesson step | Exact line interval | UTF-8 bytes | SHA-256 |
| --- | --- | --- | --- |
| Quartic/matrix integrability | P35–78 | 2434 | `a6cd7c0af855366993a49ceff61f5a68986aeecb9945b68cd30f5e651f43999d` |
| Off-diagonal reflection | P80–103 | 1319 | `7382cfd19cdfae2143e4f8785beb7d8daac4f92c9393a7baad57b070c49b860a` |
| Diagonal/product law and matrix conclusion | P105–188 | 4770 | `99757c7718725b2f5a57c209596c1a2947e517cefaf0edf0a7df5ac25bf4ba45` |
| Complete private statement, setup and square | T1–101 | 5136 | `5193d85b7d5771c31aefa969bac7fcd9456489823f93994033cac714e14631bb` |
| PSD residual, integration, exact mean and end | T103–160 | 2948 | `67b21acab66805492a77286c54360467a465e9e2f52d75d122bb48e030161e67` |

The intervening omitted lines are blank. In particular, the private
consumer's full literal statement and its module assumptions are present
in the fourth fold, and its complete mathematical proof is available
across folds four and five. The lesson's private source citation points
to T line 14, which is exactly the private theorem declaration.

The current lesson requests the progressive reading layout and associates
each formula/prose step with the exact code string intended for the
adjacent closed disclosure. This source-data review verifies that content
and adjacency assignment; it does not certify generated DOM state,+browser behavior, desktop/mobile layout, or public deployment. Those are
explicitly outside this phase.

## Source/Lean map and inference scope

The root-authored source map has ten substantive mapping groups and five
background-provider groups. This reviewer independently verified every
mapped source element identity, character interval, UTF-8 byte interval,
LF source line/column locator, and span hash against the pinned HTML.
Every mapped code line interval, character/byte interval, complete-file
hash, and span hash also matches the exact complete inputs. The checks
cover 23 source spans, 16 Lean spans and 10 background source/consumer
spans. The Convex.integral_mem excerpt matches this reviewer's already
frozen pinned API excerpt, not a later foreign receipt.

The map meanings follow the actual source and proof: standing query
range; canonical row and radius; Ex113 integrability and expectation;
reflection; diagonal moments; exact midpoint feature; cutoff; square;
individual PSD removal; and tensor transport of the producer mean.
The aggregate RHS is appropriately described as provenance for a
termwise inference. It does not supply an asserted aggregate Lean
theorem. The static direct calls support the listed ASTIS proof-parent
relations. This phase does not claim compiler extraction of private
generated symbol names or a compiled dependency graph.

Both the current lesson boundary and publication boundary explicitly
retain original-family law/integral transport, summed and centered
variance, concentration, full Lemma 4.4, main lower bounds and oracle/TV/
cost adapters as open. They also retain serialized integration,+desktop/mobile delivery, and purification as pending. This is consistent
with the exact code. The producer canonical-law claim and the consumer
termwise claim must retain these two scope boundaries when published.

## Retained limits

The public decoder covers only the producer. The private consumer is
covered by this reviewer's exact complete code review, strengthened here
by the full authored statements/formulas, precise citation, and source
map checks. No aggregate theorem, full-source assimilation, publication
deployment, or normal VERIFIED transition is certified here.

This phase writes only inside the neutral reviewer directory, preserves
every prior frozen original, and produces a separate six-field audit
overlay after schema-only conformance inspection. It makes no canonical
mutation, normal ledger/API call, process grant, commit, push, browser
claim, or integration action.
