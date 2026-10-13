from pathlib import Path
import json, hashlib, sys, datetime

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
import astis_semantic_roundtrip as rt

def read(p): return json.loads(p.read_text(encoding='utf8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def fresh(p, x):
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
def pin(p):
    return dict(path=p.relative_to(ROOT).as_posix(), raw_sha256=sha(p.read_bytes()), bytes=p.stat().st_size)

claim = read(RUN/'claim.json')
module = ROOT/claim['proposed_files'][0]
s = module.read_text(encoding='utf8')
receipt = RUN/'focused/production1-sealed-law/receipt.json'
r = read(receipt)
assert r['exit_code'] == 0 and r['source']['raw_sha256'] == sha(module.read_bytes())
seal = read(RUN/'root.statement-seal92.json')
literal = s.split('def actual_ordered_prefix_statement',1)[1].split('\n\nset_option',1)[0]
assert literal.strip() == seal['expanded_literal_Prop'].strip()
statement = literal.replace(' : Prop :=', ' :', 1)
context = read(ROOT/'runs/20261007-companion-priority/pbps-actual-finite-history-extension90/anonymous.lean-context90.json')['decoder_context']
context += [
    'Fin.cons inserts its first argument at index zero; Fin.induction is recursion on a finite ordered index. StrictMono means strict order preservation, and finite products over Fin0 equal one.',
    'The finite function-space volume is the product of real Lebesgue measures. Measure.comap along Subtype.val gives the measure on that measurable subtype; it is not a normalized probability measure.'
]
standing = read(ROOT/'website/content/publications/pbps-actual-absolute-next-event-time.json')['items'][0]['statement'].split('For every deterministic n')[0]
restatement = standing + (
    'For every deterministic finite n≥0 and finite horizon T≥0, let Hist_n=D^(Fin(n+1)) and H_n(w)=(R_j(ε(w)))_(0≤j≤n). '
    'Write rtime(live(a,z))=a and rtime(stopped)=0. Define the measurable ordered simplex Δ_n(T)={t∈ℝ^n:0<t_1<⋯<t_n<T}; its subtype carries m_n, the comap of product Lebesgue volume along inclusion. '
    'For t∈Δ_n(T), put s_0=0,s_i=t_i, z_0=z₀ and z_i=S_rΦ_(s_i−s_(i−1))(z_(i−1)) for 1≤i≤n. Define K_n(t)_j=live(s_j,z_j). '
    'Define qReal_n(t)=∏_(i=1)^n [λ_r(Φ_(s_i−s_(i−1))(z_(i−1))) exp(−Λ_(z_(i−1))(s_i−s_(i−1)))] and q_n=ofReal(qReal_n). '
    'Here the literal Lean definitions use toNNReal on times and elapsed times; these agree with the displayed nonnegative values on the simplex. '
    'Let A_n(T) be the abstract-history set in which all n+1 records are live, their read times are strictly increasing, and each postinitial read time is below T. A_n(T) does not itself constrain the initial record time. '
    'Set B_n(T)=H_n^(-1)(A_n(T)) and obs_n(w)_i=rtime(H_n(w)_(i+1)); actual H_n(w)_0 is always live(0,z₀). '
    'Then Δ_n(T) and A_n(T) are Borel. For fixed n,T, K_n and q_n are jointly Borel in (y,r,z₀,t). For every y,r,z₀, H_n,obs_n and B_n(T) are Borel, and qReal_n(t)≥0 for every simplex point. '
    'For every raw w∈B_n(T), there exists t∈Δ_n(T) with t=obs_n(w) and H_n(w)=K_n(t), as complete tagged histories. '
    'The exact unnormalized law is (H_n)_*(P restricted to B_n(T))=(K_n)_*(q_n m_n). For every Borel F:Hist_n→[0,∞], '
    '∫_(B_n(T))F(H_n(w))P(dw)=∫_(Δ_n(T))F(K_n(t))q_n(t)m_n(dt). Moreover ∫q_n dm_n=P(B_n(T))≤1. '
    'This includes n=0,T=0, zero hazard and extended-valued tests; there is no boundedness, integrability or positive-event-mass assumption. '
    'This is the strict first-n-prefix law, without a final survival factor, and is not a raw exact-n event-count law. It is an attributed ASTIS completion of the finite ordered iteration ingredient implicit in Appendix A.1(A.7), with joint Borel construction from Appendix A.2. '
    'The dimension-zero and ENNReal-test extensions are explicit ASTIS extensions. Terminal survival, endpoint/count identification, the full path-functional A.7 expansion, restart/Markovness, invariance, hypocoercivity, implementation errors, expected costs and full paper/composition remain outside this result.'
)
fresh(RUN/'authored-statement92.json', dict(statement=restatement, attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 and A.2; faithful attributed restatement of an implicit ingredient, not a standalone quoted theorem.'))
lean = dict(statement=statement, statement_sha256=sha(statement.encode()), compiled=True,
    decoder_context=context, declaration=claim['target_declarations'][0], file=claim['proposed_files'][0],
    formalizer='companion_root_20261005', compiler_evidence=receipt.relative_to(ROOT).as_posix())
audit = dict(id='ASTIS-RT-20261011-PBPSActualOrderedPrefix', state='draft',
    source=dict(source_id='companion-domain:pbps-actual-ordered-prefix', anchor=claim['source_anchor'],
        url='https://arxiv.org/html/2609.06905v1#A1.E7', original_text=restatement, text_sha256=sha(restatement.encode())),
    lean=lean, source_review=dict(state='pending'), repairs=[])
fresh(RUN/'decoder-draft92.json', audit)
fresh(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json', audit)
packet = rt.decoder_packet(audit)
out = ROOT/'runs/semantic-roundtrip/anonymous92/input.json'
fresh(out, packet)
fresh(RUN/'decoder-freeze92.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    module=pin(module), statement_seal=pin(RUN/'root.statement-seal92.json'), compile=pin(receipt),
    packet=pin(out), canonical_packet_sha256=packet.get('packet_sha256'), source_visible=False,
    publication_binding_pending=True, full_independent_math_pending=True))
print(json.dumps(dict(packet=pin(out), statement_sha256=lean['statement_sha256'])))
