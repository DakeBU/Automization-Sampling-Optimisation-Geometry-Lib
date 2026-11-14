#!/usr/bin/env python3
"""Deterministic, source-only phase-1 extraction and expectation freeze.

Mathematical evidence input: the one pinned raw HTML file in SOURCE, exclusively.
This script does not discover, enumerate, or read repository context.
"""
from pathlib import Path
from html.parser import HTMLParser
import datetime
import gzip
import hashlib
import json
import os

SOURCE = Path('/Users/zhouhuanjian/ASTIS-GC/.astis/huanjian-resume-20261103/2610.20492v1.html')
OUT = Path(__file__).resolve().parent
PIN = '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
raw = SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == PIN
html = raw.decode('utf-8')
line_starts = [0]
for i, c in enumerate(html):
    if c == '\n':
        line_starts.append(i + 1)


class Node:
    def __init__(self, tag, attrs, start, end=None):
        self.tag, self.attrs, self.start, self.end = tag, dict(attrs), start, end
        self.children = []


class SourceParser(HTMLParser):
    voids = {'meta', 'link', 'br', 'hr', 'img', 'input', 'wbr', 'source', 'area', 'base', 'embed', 'param', 'track', 'col'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', [], 0, len(html))
        self.stack, self.ids = [self.root], {}

    def character_offset(self):
        line, column = self.getpos()
        return line_starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.character_offset()
        node = Node(tag, attrs, start, start + len(self.get_starttag_text()) if tag in self.voids else None)
        self.stack[-1].children.append(node)
        if 'id' in node.attrs:
            assert node.attrs['id'] not in self.ids
            self.ids[node.attrs['id']] = node
        if tag not in self.voids:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        start = self.character_offset()
        node = Node(tag, attrs, start, start + len(self.get_starttag_text()))
        self.stack[-1].children.append(node)
        if 'id' in node.attrs:
            assert node.attrs['id'] not in self.ids
            self.ids[node.attrs['id']] = node

    def handle_endtag(self, tag):
        end = html.index('>', self.character_offset()) + 1
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                for node in self.stack[i:]:
                    node.end = end
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


parser = SourceParser()
parser.feed(html)
blocks = {'p', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'div', 'li'}


def extract(node):
    if isinstance(node, str):
        return node
    if node.tag == 'math':
        return '$' + node.attrs.get('alttext', '') + '$'
    if node.tag in {'script', 'style', 'annotation'}:
        return ''
    value = ''.join(extract(child) for child in node.children)
    return '\n' + value + '\n' if node.tag in blocks else value


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def write_json(name, value):
    (OUT / name).write_bytes(jbytes(value))


def write_gzip(name, value):
    # Raw payload bytes, including outer/trailing whitespace, are never stripped.
    (OUT / name).write_bytes(gzip.compress(value, mtime=0))


def anchor(ident):
    node = parser.ids[ident]
    assert node.end is not None
    chunk = html[node.start:node.end].encode('utf-8')
    return {
        'element_id': ident,
        'tag': node.tag,
        'character_range_half_open': [node.start, node.end],
        'byte_range_half_open': [len(html[:node.start].encode('utf-8')), len(html[:node.end].encode('utf-8'))],
        'line_range_inclusive_1_based': [html.count('\n', 0, node.start) + 1, html.count('\n', 0, node.end - 1) + 1],
        'exact_raw_span_sha256': hashlib.sha256(chunk).hexdigest(),
        'alttext': node.attrs.get('alttext'),
    }


sections = ['S2', 'S3.SS1', 'S3.SS2', 'S3.Thmtheorem1', 'A1', 'A2.SS2', 'A2.SS3']
anchor_ids = sections + [
    'S2.Ex1', 'S2.Ex2', 'S3.E4', 'S3.E5', 'S3.E6', 'S3.E8',
    'A2.E14', 'A2.E15', 'A2.E16', 'A2.E17', 'A2.E18', 'A2.E19',
    'A2.E20', 'A2.E21', 'A2.E22', 'A2.E23', 'A2.E24', 'A2.E25',
    'A2.Ex68', 'A2.Ex69', 'A2.Ex70', 'A2.Ex71', 'A2.Ex72',
    'A2.Ex72X.m2', 'A2.Ex72X.m3', 'A2.Ex72Xa.m2', 'A2.Ex72Xb.m2',
    'A2.Ex72Xc.m2', 'A2.SS2.SSS3', 'A2.SS2.SSS3.p3.3', 'A2.SS2.SSS3.p3.4', 'A2.E26',
]
# Identify the Poisson equation by its actual local equation number, without
# presupposing an unrelated repository's name for it.
for ident, node in parser.ids.items():
    if ident.startswith('A1.') and node.tag == 'table':
        anchor_ids.append(ident)
anchors = {ident: anchor(ident) for ident in dict.fromkeys(anchor_ids)}

write_gzip('pinned-source.raw.html.gz', raw)
for ident in sections:
    node = parser.ids[ident]
    write_gzip('source-span.' + ident + '.html.gz', html[node.start:node.end].encode('utf-8'))
    write_gzip('source-text.' + ident + '.txt.gz', extract(node).encode('utf-8'))
write_json('source-anchors.json', anchors)

expectations = {
    'document_kind': 'Independent raw-source-first phase-1 mathematical expectations; no comparison or implementation verdict',
    'phase': '1-frozen-before-blind-packet',
    'source_identity': {
        'title': 'On Complexity of Gaussian Sampling',
        'authors': ['Huanjian Zhou', 'Taiji Suzuki'],
        'watermark': 'arXiv:2610.20492v1 [cs.CC] 14 Oct 2026',
        'raw_path': str(SOURCE),
        'raw_sha256': PIN,
        'raw_bytes': len(raw),
        'target_anchor': 'A2.Ex72',
        'target_description': 'Final display of Appendix B.2.3, Amplification Across Blocks, proof of Lemma 3.3',
    },
    'seven_slots': {
        'objects': {
            'precision': 'A_O=((κ+1)/2) I_n - ((κ-1)/4)(O+Oᵀ), O∈O(n); A_𝐎=diag(A_O₁,…,A_Oₖ,I_(d-kn)).',
            'haar_and_priors': 'O(n) has Haar probability; μ_(n,b) is Haar conditioned on det O=b, b∈{-1,+1}. Under D_b, O₁,…,Oₖ are independent draws from μ_(n,b), and D_b is the law of A_𝐎. Each of the two determinant components has full-Haar probability 1/2.',
            'targets': 'π_A=N(0,A⁻¹); P_b=E_(O∼μ_(n,b))[N(0,A_O⁻¹)] on R^n; barπ_b=E_(A∼D_b)[π_A]=P_b^⊗k ⊗ N(0,I_(d-kn)) on R^d, with the final factor omitted when kn=d.',
            'densities': 'p_O is the Lebesgue density of N(0,A_O⁻¹), p_b the Lebesgue density of P_b, and barp_b the Lebesgue density of barπ_b. For m=d-kn>0, φ_m is the normalized standard Gaussian density on R^m.',
            'affinity': 'a=∫_(R^n) sqrt(p_+1(x) p_-1(x)) dx is the single-block Hellinger affinity, with 0≤a≤1.',
            'evidence': ['S2', 'S3.E4', 'S3.E5', 'S3.E6', 'A2.SS2', 'A2.Ex68', 'A2.Ex70'],
        },
        'domains': {
            'parameters': 'd and n are integer dimensions with 3≤n≤d; κ is real with κ≥4; k=floor(d/n) is the number of blocks; m=d-kn is an integer with 0≤m<n and k≥1.',
            'spaces': 'The underlying sample spaces are Euclidean spaces with their measurable/Borel structure; x_j∈R^n and, only when m>0, z∈R^m; product coordinates identify the total space with R^d.',
            'orthogonal_group': 'O(n)={O∈R^(n×n):OᵀO=I_n}. The precision class is A_(d,κ)={A=Aᵀ:I_d≼A≼κ I_d}.',
            'domain_boundaries': 'The separation claim is in the n≥3, κ≥4 standing regime of B.2 and the §3.1 construction. n need not be odd. The later choice n=2T+1 is a main-theorem application, not a hypothesis of Ex72.',
            'evidence': ['S2', 'S3.SS1', 'A2.SS2', 'A2.SS3'],
        },
        'quantifiers': {
            'main': 'For every permitted d,n,κ, form k and the two actual priors and averaged targets as above; the resulting pair barπ_+1,barπ_-1 satisfies the final lower bound.',
            'signs': 'b ranges over exactly {-1,+1}; all k blocks share b, while the O_j are independent within each fixed-b prior.',
            'proof_points': 'The density product is for each b and each product-coordinate point (up to density versions); the min≤sqrt pointwise inequality is for nonnegative density values, and the integrals are over the full relevant Euclidean spaces.',
            'excluded_imports': 'No query budget T, algorithm, output law, target accuracy ε, indistinguishability assumption, or randomized common-sign mixture is quantified in the Ex72 separation result itself.',
            'evidence': ['S3.SS1', 'S3.SS2', 'A2.SS2.SSS3'],
        },
        'assumptions': {
            'construction': 'The P_b and barπ_b are the Gaussian mixtures defined by the actual determinant-conditioned construction, not arbitrary measures identified solely by a name.',
            'single_block_input': 'Proposition B.7 proves TV(P_+1,P_-1)≥(1/2) exp(-5n/sqrtκ), using n≥3 and κ≥4. Ex72 does not independently assume this estimate without its upstream source boundary.',
            'normalization': 'p_±1 are nonnegative probability densities, so ∫p_±1=1 and 0≤a≤1. When m>0 the common residual density φ_m is nonnegative and integrates to 1.',
            'independence': 'Averaging independent O_j under each D_b produces the product P_b^⊗k. The same residual factor appears on both sides. Independence is conditional on the selected sign, not after randomizing that sign jointly.',
            'analysis': 'Cauchy–Schwarz supplies TV(P_+1,P_-1)≤sqrt(1-a²); log(1-t)≤-t applies to t=(1/4)exp(-10n/sqrtκ)∈[0,1). Tonelli applies to the nonnegative product affinity integrand. k is a nonnegative integer, in fact ≥1 here, permitting the kth-power bound.',
            'regularity': 'Orthogonality gives I_n≼A_O≼κ I_n, hence valid nonsingular Gaussian targets, and the block precision including any residual belongs to A_(d,κ).',
            'evidence': ['A2.E19', 'A2.E25', 'A2.Ex69', 'A2.Ex70', 'A2.Ex71', 'A2.Ex72', 'A2.E26'],
        },
        'conclusion': {
            'final_inequality': 'TV(barπ_+1,barπ_-1) ≥ 1 - exp{-(k/8) exp(-10n/sqrtκ)}.',
            'full_target_display_chain': [
                'TV(barπ_+1,barπ_-1) = 1 - ∫_(R^d) min{barp_+1(x),barp_-1(x)} dx',
                '≥ 1 - ∫_(R^d) sqrt(barp_+1(x)barp_-1(x)) dx',
                '= 1 - a^k',
                '≥ 1 - exp{-(k/8) exp(-10n/sqrtκ)}',
            ],
            'target_of_distance': 'The two averaged target laws, not two algorithm output laws, not their componentwise TV distances, and not individual fixed-precision Gaussian targets.',
            'kind': 'Explicit finite-parameter lower bound with the displayed inequality directions. The final exponential estimate is not an equality assertion.',
            'evidence': ['A2.Ex72', 'A2.Ex72X.m2', 'A2.Ex72X.m3', 'A2.Ex72Xa.m2', 'A2.Ex72Xb.m2', 'A2.Ex72Xc.m2'],
        },
        'senses': {
            'tv_convention': 'TV(P,Q)=sup_(measurable B)|P(B)-Q(B)|=(1/2)∫|p-q|dλ, for probabilities with densities with respect to any common dominating λ. Its range is [0,1]. A measurable [0,1]-valued test h has |E_P h-E_Q h|≤TV(P,Q).',
            'overlap_convention': 'For normalized densities, TV=1-∫min(p,q). The factor 1/2 in the L1 convention is essential to both this identity and the single-block affinity calculation.',
            'hellinger_convention': 'a is unsquared affinity ∫sqrt(pq), not Hellinger distance or squared affinity. Tensorization yields a^k, with the shared residual contributing a factor 1.',
            'residual_convention': 'If kn<d, retain the identical standard Gaussian residual on R^(d-kn) and its integral 1 in the density/affinity product. If kn=d, omit the final Gaussian/identity block and every residual integral; the source explicitly uses this omitted-factor convention rather than requiring a density on R^0.',
            'probability_and_averaging': 'Haar measures and Gaussian laws are probability measures. P_b and barπ_b are mixtures/averages of target laws. The density of a mixture and the product structure are at the distribution level.',
            'arithmetic': 'exp and sqrtκ use real arithmetic; κ≥4 makes sqrtκ positive and all divisions meaningful. k is an integer power/multiplicity, read as its real value in k/8.',
            'evidence': ['S2.Ex2', 'S3.E6', 'A2.Ex68', 'A2.Ex69', 'A2.Ex71', 'A2.Ex72', 'A2.SS2.SSS3.p3.3'],
        },
        'constants': {
            'single_block_coarse': 'δ=(1/2) exp(-5n/sqrtκ).',
            'single_block_sharp': 'TV(P_+1,P_-1) ≥ ((sqrtκ-1)/(sqrtκ+1))^n / (2+4n sqrtκ/(sqrtκ+1)^2) ≥ δ.',
            'squared_gap': 'δ²=(1/4) exp(-10n/sqrtκ).',
            'affinity_bound': 'a≤sqrt(1-(1/4)exp(-10n/sqrtκ))≤exp{-(1/8)exp(-10n/sqrtκ)}.',
            'block_bound': 'a^k≤exp{-(k/8)exp(-10n/sqrtκ)}; final complement is 1 minus this expression.',
            'origin_of_1_over_8': 'Squaring 1/2 produces 1/4, then the square root/log estimate contributes another 1/2, giving 1/8. The 10 in the exponent is twice the single-block 5.',
            'exactness': 'All constants are the explicit source constants; there is no unspecified universal constant or asymptotic/O notation in Ex72.',
            'evidence': ['A2.E19', 'A2.E25', 'A2.Ex72Xc.m2'],
        },
    },
    'proof_steps': [
        {'step': 1, 'claim': 'Use the probability density normalizations to define a∈[0,1].', 'anchors': ['A2.Ex68', 'A2.Ex69']},
        {'step': 2, 'claim': 'Factor |p_+-p_-| as |sqrt(p_+)-sqrt(p_-)|(sqrt(p_+)+sqrt(p_-)); Cauchy–Schwarz and ∫p_±=1 yield TV≤(1/2)sqrt((2-2a)(2+2a))=sqrt(1-a²).', 'anchors': ['A2.Ex69']},
        {'step': 3, 'claim': 'Combine the proven B.7 gap with the preceding inequality: δ≤TV≤sqrt(1-a²) implies a≤sqrt(1-δ²), using a≥0.', 'anchors': ['A2.E19', 'A2.E25']},
        {'step': 4, 'claim': 'Apply log(1-t)≤-t for t=δ² to obtain sqrt(1-t)≤exp(-t/2), i.e. Eq.25.', 'anchors': ['A2.E25']},
        {'step': 5, 'claim': 'Use the actual mixture factorization Eq.6 to identify barp_b(x₁,…,xₖ,z)=∏p_b(x_j)φ_m(z) when m>0.', 'anchors': ['S3.E6', 'A2.Ex70']},
        {'step': 6, 'claim': 'Tonelli factors the total affinity into the product of k single-block affinities and the residual integral 1, giving a^k. When m=0 the source instead omits the residual factor and obtains the same a^k.', 'anchors': ['A2.Ex71', 'A2.SS2.SSS3.p3.3']},
        {'step': 7, 'claim': 'The probability-density identity TV=1-∫min and min(u,v)≤sqrt(uv) give TV(barπ_+,barπ_-)≥1-a^k.', 'anchors': ['S2.Ex2', 'A2.Ex72']},
        {'step': 8, 'claim': 'Raise the nonnegative Eq.25 bound to integer k, then take complements to obtain the final Ex72 inequality.', 'anchors': ['A2.E25', 'A2.Ex72Xc.m2', 'A2.SS2.SSS3.p3.4']},
    ],
    'upstream_boundaries': [
        {
            'boundary': 'Standing objects and legal targets',
            'source': ['S2', 'S3.SS1', 'A2.SS3'],
            'content': 'Haar probability and its two equal-mass components; centered target π_A=N(0,A⁻¹); the exact A_O/A_𝐎/prior/averaged-target definitions; orthogonality and Cauchy–Schwarz prove the precision spectral bounds. Symmetry plus positive definiteness ensures Gaussian densities. Identity residual is explicitly omitted when m=0.',
            'closure': 'The source includes the spectral verification in B.3; basic Gaussian/probability conventions are standing definitions.',
        },
        {
            'boundary': 'Lemma B.6 determinant cancellation',
            'source': ['A2.E15', 'A2.E16', 'A2.E17', 'A2.E18', 'A2.SS2'],
            'content': 'For any Borel h with E|h(U)|<∞, U=O_11 under full Haar, E[det(O)sqrt(det A_O)h(U)]=((-1)^(n-1)(sqrtκ-1)^(n-1)/2^n) E[((sqrtκ+1)U-(sqrtκ-1))h(U)]. Factor A_O as one quarter BᵀB; B_t=(sqrtκ+1)I-tO stays invertible for 0≤t≤sqrtκ-1 by norm lower bound ≥2||v||, so det B_t is positive. Thus the positive square root of det A_O equals 2^-n det B. Multiply by det O and expand principal minors. Row reflections preserving O_11 cancel all minors containing i≥2, leaving only the empty minor and {1}. |det O_(S,S)|≤1 ensures integrability.',
            'closure': 'This is an actual source-proved identity for the real orthogonal construction; it is not an unconstrained symbolic cancellation assumption.',
        },
        {
            'boundary': 'Lemma A.1 spherical Poisson identities',
            'source': ['A1'],
            'content': 'For U the first coordinate of a uniform point on S^(n-1) and 0<r<1: E[(1+r²-2rU)^(-n/2)]=1/(1-r²), and E[U(1+r²-2rU)^(-n/2)]=r/(1-r²). The source derives them by applying the unit-ball Poisson representation to harmonic functions 1 and x↦x₁ at re₁, with normalized spherical measure.',
            'closure': 'The Poisson representation formula is the external mathematical boundary, cited by the paper as [5, Theorem 1.21]; the cited reference itself was not read. The local lemma wording contains both n≥2 and a trailing n≥3 phrase; the Ex72 dependency uses n≥3, satisfying both.',
        },
        {
            'boundary': 'Proposition B.7 bounded radial test and signed integral',
            'source': ['A2.E19', 'A2.E20', 'A2.E21', 'A2.SS2'],
            'content': 'h_λ(x)=exp(-λ||x||²), λ≥0; H(λ)=E_full-Haar[det(O)∫h_λ p_O]. Equal component masses give H=(1/2)(E_P+ h_λ-E_P- h_λ), and [0,1]-test convention gives TV≥2|H|. Conjugation invariance makes E[det(O)p_O(x)] radial. At ||x||e₁ its exponent depends only on U since e₁ᵀA_Oe₁=(κ+1-(κ-1)U)/2. The source supplies integrable domination (κ/(2π))^(n/2)exp(-||x||²/2), invokes Fubini and Gaussian integration, then B.6 with denominator ≥2+4λ, giving Eq.21.',
            'closure': 'These operations are source-provided analytic steps; an implementation proving only a numeric exponential inequality would leave this actual source input unaccounted for.',
        },
        {
            'boundary': 'Proposition B.7 parameter selection and exact gap',
            'source': ['A2.E22', 'A2.E23', 'A2.E24', 'A2.SS2'],
            'content': 'Set q=(sqrtκ-1)/(sqrtκ+1), r=(1-1/n)q, λ=(κ-1)(1+r²)/(8r)-(κ+1)/4=(4n sqrtκ+(sqrtκ-1)²)/(8n(n-1)); then 0<r<1 and λ>0. The denominator is (κ-1)/(2r)(1+r²-2rU)=n(sqrtκ+1)²/(2(n-1))(1+r²-2rU). Since Oe₁ is uniform on S^(n-1), A.1 yields H(λ)=((-1)^n/n)q^n(1-1/n)^(n/2)/(1-r²). The λ=0 match is expressly rejected by the source because H(0)=0.',
            'closure': 'The actual nonzero radial test and its positivity conditions belong to the dependency of the coarse gap.',
        },
        {
            'boundary': 'Proposition B.7 coarse constants',
            'source': ['A2.E19', 'A2.E24', 'A2.SS2'],
            'content': 'Convexity gives (1-1/n)^(n/2)≥1/2; n(1-r²)=4n sqrtκ/(sqrtκ+1)²+q²(2-1/n)≤4n sqrtκ/(sqrtκ+1)²+2. Together with TV≥2|H| this proves the sharp first bound. For κ≥4, log((sqrtκ+1)/(sqrtκ-1))=2∫₀^(1/sqrtκ)dt/(1-t²)≤8/(3sqrtκ)≤3/sqrtκ, so q^n≥exp(-3n/sqrtκ). Also 2+4n sqrtκ/(sqrtκ+1)²≤2+4n/sqrtκ≤2exp(2n/sqrtκ), giving δ=(1/2)exp(-5n/sqrtκ).',
            'closure': 'The constants 5, 10, and 1/8 in the amplification trace to these explicit estimates and the affinity conversion, without asymptotic substitutions.',
        },
        {
            'boundary': 'Actual product-mixture law before tensorization',
            'source': ['S3.SS1', 'S3.E6', 'A2.Ex70', 'A2.Ex71'],
            'content': 'Block-diagonal Gaussian targets factor for fixed 𝐎. Independent determinant-conditioned O_j under fixed b allow the average of that product to factor into P_b^⊗k. The identical standard Gaussian residual has mass 1. Ex71 is the resulting affinity factorization on R^d.',
            'closure': 'The actual-law identification Eq.6 and the coordinate/residual dimensions must be connected to any abstract product-affinity theorem used later.',
        },
        {
            'boundary': 'Separate lower-bound ingredients outside Ex72',
            'source': ['S3.SS2', 'S3.Thmtheorem1'],
            'content': 'Lemma 3.2 indistinguishability for T<n/2, the application n=2T+1, and the theorem error range 0<ε≤1/16 belong to the query-complexity argument. They are not premises for the separation/amplification theorem itself.',
            'closure': 'The indistinguishability proof, query algorithm implementation, and full main-theorem proof were not read and are not claimed to be dependencies of Ex72.',
        },
    ],
    'source_questions_for_later_comparison': [
        {'id': 'Q1', 'question': 'Are the compared objects demonstrably the actual averaged target laws from Eqs.4–6, with determinant-conditioned Haar mixtures, rather than unconstrained distributions or substituted scalar names?'},
        {'id': 'Q2', 'question': 'Does the later statement retain d,n integer with 3≤n≤d, real κ≥4, k=floor(d/n), and m=d-kn, or explicitly prove a general theorem and its specialization to these actual source parameters?'},
        {'id': 'Q3', 'question': 'Is the B.7 single-block estimate established for the actual P_b, with its analytic input boundary explicit, before it is converted to Eq.25?'},
        {'id': 'Q4', 'question': 'Are TV and affinity normalized exactly as in the source, so the factors 1/2, 1/4, 1/8 and exponent 10 remain justified?'},
        {'id': 'Q5', 'question': 'Is the product density/affinity identification for the actual barπ_b connected to the source construction, including the common normalized Gaussian residual and the kn=d omitted-factor case?'},
        {'id': 'Q6', 'question': 'Does the final comparison recover the full lower-bound chain TV≥1-a^k≥1-exp{-(k/8)exp(-10n/sqrtκ)}, with the correct two averaged targets and direction?'},
        {'id': 'Q7', 'question': 'If an abstract product/probability result is used, are its assumptions discharged for the source measures and dimensions, rather than left as extra hypotheses under a source-specific theorem label?'},
        {'id': 'Q8', 'question': 'Are assumptions on algorithms, T, odd n, or ε introduced only as explicit application restrictions, rather than silently changing the source separation domain?'},
        {'id': 'Q9', 'question': 'The paper has local editorial anomalies: B.5 is titled “Separation (Lemma 6 restated)” while the surrounding proof identifies Lemma 3.3, and A.1 has redundant n≥2/n≥3 wording. Are these raw-source facts preserved without confusing the target statement or weakening its n≥3 domain?'},
        {'id': 'Q10', 'question': 'Which upstream analytic results are proved, imported as general mathematics, or left conditional? The raw paper alone does not determine the coverage of any implementation; that comparison remains open.'},
    ],
    'explicit_review_limits': [
        'This record precedes any blind packet, exported candidate source, repository formalization, current/old audit, ledger, lesson, source graph, seal, or other reviewer result.',
        'No implementation acceptance, publication verdict, Lean proof review, canonical audit, or ledger change is made.',
        'Only the pinned raw HTML supplied as mathematical evidence was read. External reference [5] and Appendix B.1 were not read.',
        'Derived restatements and arithmetic consequences are identified in this record; exact source spans and math alttext remain independently recoverable from the raw archive and anchor hashes.',
    ],
    'anchor_index_file': 'source-anchors.json',
}
write_json('source-expectations.json', expectations)

operations = {
    'reviewer': '/root/ex72_fresh_source_v2',
    'phase': '1',
    'mathematical_input_allowlist': [str(SOURCE)],
    'inputs_not_read': ['repository inventory', 'AGENTS.md', 'source graph', 'seals', 'current or old audits', 'proof or Lean module', 'candidate publication context', 'lesson', 'review packet', 'previous reviewer or decoder output'],
    'operations_before_freeze': [
        'Read original raw file bytes; compute SHA256 and byte count; inspect title prefix and direct textual matches for B.2.3, TV, and Suzuki.',
        'Parse that same raw HTML using Python standard-library HTMLParser; print S2, S3.SS1, S3.SS2 and A2.SS2; replace math subtree with its source alttext only for derived reading output.',
        'Parse that same raw HTML; print A1, A2.SS3, S3.Thmtheorem1 and the local B.2.3 IDs and math alttext.',
        'Read that same raw HTML to confirm exact title, Huanjian Zhou/Taiji Suzuki author names, and arXiv watermark from frontmatter.',
        'Read that same raw HTML to locate local source equation IDs around the inspected spans.',
        'Create only the designated owned fresh-source-v2/phase1 directory and this source-only extraction/freeze script.',
        'The first execution stopped before extraction/archive output because a helper named offset collided with HTMLParser.offset (an integer). Rename the helper character_offset and rerun; the pinned input remains unchanged.',
        'Run this script: reverify pinned hash, archive exact original bytes with deterministic lossless gzip, archive exact selected HTML spans and deterministic derived text, save source anchors and independently written seven-slot expectations, and freeze all phase1 files read-only.',
    ],
    'extraction_semantics': 'UTF-8 decode of exact raw bytes; HTMLParser(convert_charrefs=True); math emitted as $alttext$; script/style/annotation excluded from derived text; original data whitespace retained; newlines added around named block tags. The derived text is not claimed lossless; exact source HTML archives are lossless.',
    'whitespace_policy': 'No strip(), rstrip(), trailing-whitespace cleanup, line-ending rewrite, or raw-input modification. Text/log payloads with outer/trailing whitespace are stored using gzip.compress(payload,mtime=0). Exact decompressed sizes and hashes are recorded in manifest.json.',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
write_json('provenance-and-operations.json', operations)
run_log = ('Pinned source verified: ' + PIN + '\n'
           + 'Raw bytes: ' + str(len(raw)) + '\n'
           + 'Source-only phase1 extraction and independent expectations frozen.\n'
           + 'No candidate or implementation comparison has occurred.\n')
write_gzip('freeze-operation.log.txt.gz', run_log.encode('utf-8'))

manifest_files = {}
for path in sorted(OUT.iterdir()):
    if not path.is_file() or path.name in {'manifest.json', 'FREEZE.sha256'}:
        continue
    data = path.read_bytes()
    entry = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if path.suffix == '.gz':
        payload = gzip.decompress(data)
        entry.update({'decompressed_bytes': len(payload), 'decompressed_sha256': hashlib.sha256(payload).hexdigest(), 'compression': 'gzip,mtime=0'})
    manifest_files[path.name] = entry
expectation_sha = manifest_files['source-expectations.json']['sha256']
manifest = {
    'phase': '1-frozen-before-blind-packet',
    'mathematical_input_raw_sha256': PIN,
    'expectation_file': 'source-expectations.json',
    'expectation_sha256': expectation_sha,
    'files': manifest_files,
    'freeze_note': 'All phase1 regular files made mode 0444 after manifest generation. No later comparison may edit this phase1 snapshot.',
}
write_json('manifest.json', manifest)
manifest_sha = hashlib.sha256((OUT / 'manifest.json').read_bytes()).hexdigest()
(OUT / 'FREEZE.sha256').write_bytes((expectation_sha + '  source-expectations.json\n' + manifest_sha + '  manifest.json\n').encode('ascii'))
for path in OUT.iterdir():
    if path.is_file():
        os.chmod(path, 0o444)
print(json.dumps({'expectation_sha256': expectation_sha, 'manifest_sha256': manifest_sha, 'raw_sha256': PIN, 'phase1_directory': str(OUT), 'target_anchor': anchors['A2.Ex72']}, ensure_ascii=False, indent=2))
