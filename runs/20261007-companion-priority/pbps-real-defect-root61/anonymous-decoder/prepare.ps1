$ErrorActionPreference = 'Stop'
$out = 'E:\Samplinglib\.astis\decoder-61\independent'
$utf8 = [System.Text.UTF8Encoding]::new($false)
function WriteUtf8([string]$name, [string]$value) { [System.IO.File]::WriteAllText(($out + '\' + $name), $value, $utf8) }
function Sha([byte[]]$bytes) { [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant() }
function Json($value) { ConvertTo-Json -InputObject $value -Depth 40 }
$p0 = [System.IO.File]::ReadAllText('E:\Samplinglib\.astis\decoder-61\packet0.json', $utf8) | ConvertFrom-Json
$p1 = [System.IO.File]::ReadAllText('E:\Samplinglib\.astis\decoder-61\packet1.json', $utf8) | ConvertFrom-Json
$pins = [System.IO.File]::ReadAllText(($out + '\input-pins.json'), $utf8) | ConvertFrom-Json
foreach ($p in @($p0,$p1)) { if ((Sha ($utf8.GetBytes($p.lean.statement))) -ne $p.lean.statement_sha256) { throw 'Statement digest mismatch' } }
$text0 = @'
Let Omega be any type equipped with a measurable space, let mu be any measure on Omega, and let H = L^2(Omega, mu; R). H consists of almost-everywhere equivalence classes of square-integrable measurable real functions, equipped with its integral real Hilbert structure. No finiteness, probability or sigma-finiteness assumption on mu is displayed.

For every bounded continuous real-linear endomorphism D of H, assume that D is positive: it is self-adjoint and its quadratic form is nonnegative, so <D u, u>_R >= 0 for every u in H. Then there exists a bounded continuous real-linear endomorphism Gamma of H such that Gamma is positive, Gamma composed with Gamma equals D, and, simultaneously for every u in H,

    ||Gamma u||^2 = <D u, u>_R.

The same Gamma serves all u, on the entire H. Positivity of D is an input hypothesis; positivity, the square identity and the energy identity for Gamma are conclusions. No chosen square root, continuous functional calculus certificate, complex extension, finite-dimensional H, or operator-production certificate is an input. The proposition asserts existence, not uniqueness of Gamma. Operator multiplication is composition, not pointwise multiplication or an adjoint operation. No rate, numerical constant or additional regularity condition appears.
'@
$text1 = @'
Let E be a finite-dimensional real inner-product normed additive group, equipped with a measurable space equal to its Borel measurable space and its canonical volume measure. Zero-dimensional E is allowed. Let V: E -> R, let alpha and beta be nonnegative real numbers, and let eta be real. Assume alpha > 0, alpha <= beta, V is C^2 over R, eta > 0, beta eta <= 1, and, for all x and v in E, the iterated Frechet derivative satisfies

    alpha ||v||^2 <= (D(DV)(x)[v])[v] <= beta ||v||^2.

These bounds are global and involve precisely the displayed Hessian quadratic form. No derivative above order two is assumed, and the step cap permits equality.

Define mu by normalized exponential tilting of volume with log-weight -V. Thus, in normalized-density notation, mu(dx) is proportional to exp(-V(x)) volume(dx); normalized exponential tilting is the supplied meaning of the measure construction. Let G be the standard Gaussian measure on E. Define J as the pushforward of the independent product mu x G under (z,g) |-> (z, z + sqrt(eta) g). Let nu be the second marginal of J. Define Lambda as the pushforward of J under (z,y) |-> (y, 2z - y). The proposition concludes that mu, J and nu are probability measures.

It further produces a measurable Markov kernel S from E to E such that, for every state y in E, S(y) is the normalized exponential tilt of volume with log-weight

    x |-> -V((y+x)/2) - ||y-x||^2/(8 eta).

This is an equality of measures at every y; the density expression includes its state-dependent normalization through the tilt. The kernel is a conditional kernel for Lambda: it supplies the conditional distribution of Lambda's second coordinate given its first coordinate. Both marginals of Lambda equal nu. Kernel measurability, probability normalization, this conditional-law certificate and both stationary marginals are conclusions.

For this same S, the proposition produces a bounded continuous real-linear endomorphism T of H = L^2(E, nu; R). It is self-adjoint and, for every u in H, all of the following hold:

    ||T u|| <= ||u||;
    (T u)(y) = integral_E u(x) S(y,dx) for nu-almost every y;
    integral_E (T u)(y) nu(dy) = integral_E u(y) nu(dy).

Here H consists of almost-everywhere equivalence classes of square-integrable real functions on the actual second marginal nu. The displayed pointwise formula uses representatives and is asserted separately almost everywhere for each u; no single exceptional null set common to all u is claimed. The mean equality is an equality of real integrals. Finite dimensionality of E does not assert finite dimensionality of H.

The bounded real operator I - T composed with T is positive, hence self-adjoint with nonnegative quadratic form. Finally the proposition produces a bounded continuous real-linear endomorphism Gamma of this same H such that Gamma is positive,

    Gamma composed with Gamma = I - T composed with T,

and, simultaneously for every u in H,

    ||Gamma u||^2 = ||u||^2 - ||T u||^2.

The choices of S, T and Gamma are nested in this order, and each fixed choice serves all the corresponding state and observable quantifiers. Multiplication of operators is composition; T*T here is T composed with T. The probability laws, kernel, operator, positivity of its squared defect, positive real square root and all-observable energy identity are produced conclusions, not extra public hypotheses. No complex extension, chosen square root, functional calculus certificate, finite-dimensional L^2 premise, spectral gap or convergence rate is asserted. No uniqueness claim is made for S, T or Gamma.
'@
WriteUtf8 'reconstructed0.txt' $text0
WriteUtf8 'reconstructed1.txt' $text1
$r0 = Sha ([System.IO.File]::ReadAllBytes(($out + '\reconstructed0.txt')))
$r1 = Sha ([System.IO.File]::ReadAllBytes(($out + '\reconstructed1.txt')))
$decoder = 'anonymous-decoder-61-independent'
$d0 = [ordered]@{
 schema_version=1; packet_id=$p0.packet_id; statement_sha256=$p0.lean.statement_sha256
 reconstructed_theorem_text=$text0; reconstructed_sha256=$r0; reconstructed_text_sha256=$r0
 objects=@('measurable type Omega','arbitrary measure mu','real Hilbert space H=L^2(mu)','bounded real-linear continuous operator D','produced bounded real-linear continuous operator Gamma')
 domains=@('mu need not be finite or a probability measure','u ranges over every AE L^2 class, with no finite-dimensional restriction')
 quantifiers='For every Omega and measurable structure, mu and positive D, there exists one Gamma such that its positivity and square identity hold, and for every u in H its energy identity holds.'
 assumptions=@('MeasurableSpace Omega','mu : Measure Omega','D bounded continuous real-linear endomorphism on H','D self-adjoint with nonnegative quadratic form')
 conclusion=@('Gamma positive','Gamma composed with Gamma equals D','for all u in H, ||Gamma u||^2=<D u,u>_R')
 scopes='Gamma depends on the given measure and D; all u use the same Gamma. No uniqueness is asserted.'
 constant_dependencies='No theorem constants or rate parameters are displayed.'
 produced_certificates=@('positive real square root','global square identity','full-domain energy identity')
 ambiguities=@('The positive-root existence conclusion does not itself assert uniqueness.','No sigma-finiteness restriction is displayed; none is inferred.')
 decoder=$decoder; source_text_visible=$false; source_identity_visible=$false; source_fidelity_verdict=$null; proof_validation_performed=$false
}
$d1 = [ordered]@{
 schema_version=1; packet_id=$p1.packet_id; statement_sha256=$p1.lean.statement_sha256
 reconstructed_theorem_text=$text1; reconstructed_sha256=$r1; reconstructed_text_sha256=$r1
 objects=@('finite-dimensional real Hilbert Borel base E with canonical volume','C2 potential V','nonnegative alpha and beta','positive eta','mu=normalized exp(-V) tilt of volume','standard Gaussian G','J=law of (Z,Z+sqrt(eta)G) under independent mu x G','nu=second marginal of J','Lambda=law of (Y,2Z-Y) induced by J','produced Markov kernel S','produced bounded real-linear operator T on H=L^2(nu)','produced positive bounded real-linear operator Gamma on H')
 domains=@('E may have dimension zero','H is the full real AE L^2 space over the actual nu, not assumed finite-dimensional','Hessian bound applies at every x and v in E','kernel measure equality applies to every state y','operator representative equality is nu-AE separately for every u')
 quantifiers='For every E with the displayed structures, V, alpha, beta and eta satisfying the hypotheses, define mu,J,nu,Lambda. All three probability certificates hold and there exists S with all-state measure equality and conditional-law/stationary-marginal certificates; for this S there exists T with self-adjointness and all-u contraction, AE action and mean preservation; its defect is positive and there exists Gamma with positivity, square identity and all-u energy identity.'
 assumptions=@('finite-dimensional real inner-product normed additive group E','Borel measurable structure on E','V is C2','alpha and beta are nonnegative reals','alpha>0','alpha<=beta','global alpha||v||^2 <= (D(DV)(x)[v])[v] <= beta||v||^2','eta>0','beta eta<=1')
 conclusion=@('mu,J,nu are probability measures','S is a Markov kernel','for every y, S(y) equals the displayed normalized tilt of volume','S is conditional kernel of Lambda','Lambda first and second marginals both equal nu','T is self-adjoint','for all u, contraction, per-u AE kernel-integral action, and mean preservation','I-T composed with T is positive','Gamma is positive','Gamma squared equals I-T composed with T','for all u, ||Gamma u||^2=||u||^2-||T u||^2')
 scopes='The outer parameters precede all let-defined laws. Existentials S then T then Gamma are nested. The same choices serve all quantified states and observables. AE representative equality has scope forall u then AE y; it does not assert AE y then forall u.'
 constant_dependencies='alpha,beta,eta are outer parameters subject only to the displayed restrictions. sqrt(eta), coefficients 1/2 and 2, and denominator 8 eta are fixed exactly as displayed. No numerical convergence constant is introduced.'
 produced_certificates=@('probability of mu,J,nu','Markov kernel normalization and measurability','all-state normalized kernel law','conditional kernel and equal marginals','actual bounded L2 operator','self-adjointness and contraction','mean preservation','positive squared defect','positive real root','full-domain scalar energy identity')
 ambiguities=@('Normalized tilt is supplied by approved context; its low-level implementation outside normalizable cases is not specified, and is unnecessary because normalizability/probability is concluded here.','IsCondKernel is read in the supplied disintegration context as second coordinate conditioned on first.','No common null set for all L2 observables is asserted.','No uniqueness of S,T,Gamma is asserted.')
 decoder=$decoder; source_text_visible=$false; source_identity_visible=$false; source_fidelity_verdict=$null; proof_validation_performed=$false
}
$payload = [ordered]@{
 schema_version=1
 native_run_id='anonymous-decoder-61-independent-2026-10-09-01'
 native_agent_task='/root/anonymous_decoder61'
 decoder=$decoder
 run_kind='fresh independent anonymous Lean-statement reconstruction'
 observed_input_pin_command=[ordered]@{chunk_id='8a06ad';exit_code=0;semantic_reading_occurred=$false}
 observed_semantic_read_command=[ordered]@{chunk_id='4e1e1a';exit_code=0}
 sole_original_input_paths=@($pins | ForEach-Object { $_.path })
 initial_input_pins=$pins
 restrictions_observed=@('no source text or identity','no repository inspection','no memory','no compiler','no internet','no other agents','no proof or source-fidelity verdict')
 reconstruction_decisions=@('Read only anonymous statements and approved context after raw/LF pinning.','Tracked theorem binders separately from produced certificates.','Tracked finite-dimensional base separately from full AE L2.','Tracked all-state kernel equality separately from per-observable AE operator equality.','Kept real operator composition and nested existential scope explicit.')
 statement_digests=@($p0.lean.statement_sha256,$p1.lean.statement_sha256)
 decoded_semantic_records=@($d0,$d1)
 named_payload_digest_recipe='decoder_payload_sha256 = SHA256(exact raw UTF-8 bytes of decoder-native-run.payload.json).'
 decoder_run_digest_recipe='decoder_run_sha256 = SHA256(UTF-8 bytes of ASCII domain prefix ASTIS-ANONYMOUS-DECODER-NATIVE-RUN-v1 followed by byte 0x00 followed by exact raw bytes of decoder-native-run.payload.json). This binds the complete named semantic run payload, including native identity, input pins, execution evidence and both decoded records, without a self-hash cycle. It differs deliberately from the named payload digest.'
 closure_contract='A subsequent foreground readback must verify exact bytes and digests with exit code 0; closure records bind this immutable payload, decoded outputs and scripts, and close the original neutral lease while retaining its original snapshot. CLOSED_LAST is written last; no artifact mutation follows.'
}
WriteUtf8 'decoder-native-run.payload.json' (Json $payload)
$payloadBytes = [System.IO.File]::ReadAllBytes(($out + '\decoder-native-run.payload.json'))
$payloadHash = Sha $payloadBytes
$prefix = $utf8.GetBytes('ASTIS-ANONYMOUS-DECODER-NATIVE-RUN-v1' + [char]0)
$boundBytes = [byte[]]::new($prefix.Length + $payloadBytes.Length)
[Array]::Copy($prefix,0,$boundBytes,0,$prefix.Length)
[Array]::Copy($payloadBytes,0,$boundBytes,$prefix.Length,$payloadBytes.Length)
$runHash = Sha $boundBytes
foreach ($d in @($d0,$d1)) {
 $d['decoder_run_sha256']=$runHash
 $d['decoder_payload_sha256']=$payloadHash
 $d['decoder_native_run_id']=$payload.native_run_id
 $d['decoder_run_digest_recipe']=$payload.decoder_run_digest_recipe
 $d['decoder_payload_digest_recipe']=$payload.named_payload_digest_recipe
}
WriteUtf8 'decoded0.json' (Json $d0)
WriteUtf8 'decoded1.json' (Json $d1)
WriteUtf8 'decoder-native-run.json' (Json ([ordered]@{schema_version=1; native_run_id=$payload.native_run_id; native_agent_task=$payload.native_agent_task; decoder=$decoder; named_payload='decoder-native-run.payload.json'; decoder_payload_sha256=$payloadHash; decoder_payload_bytes=$payloadBytes.Length; decoder_run_sha256=$runHash; decoder_run_digest_recipe=$payload.decoder_run_digest_recipe; decoder_payload_digest_recipe=$payload.named_payload_digest_recipe; source_text_visible=$false; source_identity_visible=$false; compiler_started=$false; reconstruction_only=$true}))
[ordered]@{prepared=$true; statement_sha256=@($p0.lean.statement_sha256,$p1.lean.statement_sha256); reconstructed_sha256=@($r0,$r1);decoder_payload_sha256=$payloadHash;decoder_run_sha256=$runHash} | ConvertTo-Json
