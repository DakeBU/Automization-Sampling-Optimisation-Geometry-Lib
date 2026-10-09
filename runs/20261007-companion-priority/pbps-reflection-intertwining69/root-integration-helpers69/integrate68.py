from pathlib import Path
import hashlib, json, subprocess

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-sharp-energy68'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def new(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def replace_json(p, value):
    nl = b'\r\n' if b'\r\n' in p.read_bytes() else b'\n'
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode().replace(b'\n', nl))
def insert_after(p, anchor, addition):
    b = p.read_bytes()
    nl = b'\r\n' if b'\r\n' in b else b'\n'
    a = anchor.encode() + nl
    assert b.count(a) == 1 and addition.encode() not in b
    p.write_bytes(b.replace(a, a + addition.encode() + nl, 1))

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
verification = load(r / 'root.exact-verification68.adoption.json')
assert verification['native_verified'] and verification['verified_commit'] == head
assert load(r / 'root.energy-alias-overlay68.adoption.json')['source_review_refreshed_from_exact_native_approval']
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).strip()
assert load(r.parent / 'pbps-root-commutation67/remote-ci67.accepted.json')['status'] == 'EXACT_INT67_REMOTE_ALL_SUCCESS'
plan, claim = load(r / 'publication-plan.json'), load(r / 'claim.json')
out = r / 'integration68'
out.mkdir(exist_ok=False)
snap = out / 'before'
snap.mkdir()
owned = ['AutoSamplingTheory/TechnicalLemmas/Registry.lean', 'AutoSamplingTheory/TechnicalLemmas.lean',
         'AutoSamplingTheory/ExampleCases.lean', 'Tests.lean', 'Tests/Basic.lean',
         'docs/companion-papers-handoff.md', 'website/content/samplewiki_companion_frontiers.json',
         'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl'] + [
             'research-wiki/frontier-cells/' + cid + '.json' for cid in plan['active_cells']]
history = []
for name in owned:
    b = (root / name).read_bytes()
    p = snap / (sha(name.encode()) + '.exactraw')
    p.write_bytes(b)
    history.append(dict(path=name, raw_sha256=sha(b), lf_sha256=sha(b.replace(b'\r\n', b'\n')),
                        exact_snapshot=p.relative_to(root).as_posix()))
new(out / 'owned-before.json', dict(head=head, owned=history))
entries = [dict(
    key='analysis.hilbertSharpQuadraticCorrectorBound', group='analysisMemory',
    decl=plan['mathematical_declarations'][0], file=claim['proposed_files'][0],
    title='Sharp quadratic corrector bound from a selfadjoint square identity',
    source='arXiv2609.06905v1 Appendix B3 (B23); ASTIS auxiliary Hilbert-space estimate',
    tags=['Hilbert', 'selfadjoint', 'quadratic-form', 'sharp-corrector'],
    note='Arbitrary complete real Hilbert space including zero: selfadjoint K,D, I+K²=D² and norm(D)<=c with c>=0 yield the exact c/2 two-component bound. Uses the sum of squared component norms. No c>=1, finite dimension, nontriviality, operator positivity or K,D commutation premise. Actual PBPS supplies D=Inv and K=A0 Inv. Not a separately printed paper theorem.'
), dict(
    key='pbps.actualSharpCorrectorEnergy', group='measureMemory',
    decl=plan['mathematical_declarations'][1], file=claim['proposed_files'][1],
    title='Sharp corrector bound and actual PBPS modified energy equivalence',
    source='arXiv2609.06905v1 Appendix B3 Lemma B3; B19,B20,B22,B23,B24',
    tags=['PBPS', 'L2', 'same-root', 'corrector', 'modified-energy'],
    note='Original finite real Hilbert/Borel/C2/two Hessians/positive capped eta inputs produce SAME actual root/inverse/coefficient and sharp |C(u,v)|<=(norm(u)²+norm(v)²)/(2gamma). Every globally centered actual f has SAME fP/fV, the actual norm budget and |C(fP,fV)|<=norm(f)²/(2gamma). Genuine original-input Test proves half/three-halves energy equivalence and exact perturbation bounds for every0<omegaWeight<=gamma. Rank0/alphaeta1 retained; literal private Props are representations only. B21 reflection rotation, H1/B2, B4 dynamics, main results, implementation errors, costs and composition remain open.'
)]
for entry in entries:
    entry['note'] = 'Independently exact-science68 VERIFIED ' + head + '. ' + entry['note']
    block = '  {\n' + '\n'.join([
        '    key := ' + json.dumps(entry['key']),
        '    localDecl := ' + json.dumps(entry['decl']),
        '    upstreamDecl := ' + json.dumps(entry['title']),
        '    upstreamFile := ' + json.dumps(entry['source']),
        '    status := LemmaMemoryStatus.formalizedLocal',
        '    tags := [' + ', '.join(json.dumps(tag) for tag in entry['tags']) + ']',
        '    saldUse := "PBPS actual consumer; no SALD admission"',
        '    note := ' + json.dumps(entry['note'])
    ]) + '\n  },\n'
    p = root / 'AutoSamplingTheory/TechnicalLemmas/Registry.lean'
    b = p.read_bytes()
    nl = b'\r\n' if b'\r\n' in b else b'\n'
    anchor = ('def ' + entry['group'] + ' : List LemmaMemoryEntry := [').encode() + nl
    assert b.count(anchor) == 1 and entry['key'].encode() not in b
    p.write_bytes(b.replace(anchor, anchor + block.encode().replace(b'\n', nl), 1))
    with (root / 'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as stream:
        stream.write((json.dumps(dict(key=entry['key'], local_decl=entry['decl'], local_file=entry['file'],
            status='formalized-local', sald_use='PBPS consumer; no SALD change', tags=entry['tags'],
            upstream_decl=entry['title'], upstream_file=entry['source'], verified_commit=head,
            evidence=(r / 'verified.json').relative_to(root).as_posix(), next_action=entry['note']),
            ensure_ascii=False) + '\n').encode())
insert_after(root / 'AutoSamplingTheory/TechnicalLemmas.lean',
    'import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean',
    'import AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound')
insert_after(root / 'AutoSamplingTheory/ExampleCases.lean',
    'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation',
    'import AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy')
insert_after(root / 'Tests.lean', 'import Tests.ProximalBPSActualRootCommutation',
    'import Tests.ProximalBPSSharpCorrectorEnergy')
p = root / 'Tests/Basic.lean'
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 514') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 514', b'formalizedTechnicalLemmaCount = 516'))
for cid in plan['active_cells']:
    p = root / 'research-wiki/frontier-cells' / (cid + '.json')
    cell = load(p)
    assert cell['status'] == 'proved_locally'
    cell['status'] = 'independently_verified'
    cell['evidence']['independent_verification'] = (r / 'verified.json').relative_to(root).as_posix()
    cell['evidence']['execution_boundary'] = ('Sharp first-corrector energy/Lemma B3 only; exact corrected SCI68B independently verified. Independent S,T prose overlay closes only the named notation limitation with refreshed source binding. B21, H1/B2, B4 dynamics/hypocoercivity, invariance/nonexplosion, main results, implementation errors/caps, expected-query costs and actual-input composition remain open. Original callers and all same witnesses retained; rank0 and alphaeta1 remain legal. Full Exposition/PURIFIED and main/live remain unearned.')
    cell['source_detail_audit']['gap'] = 'Sharp energy bound and modified-energy equivalence independently verified; B21, H1/B2, B4 dynamics, full paper results and costs remain open.'
    replace_json(p, cell)
p = root / 'docs/companion-papers-handoff.md'
b = p.read_bytes()
nl = b'\r\n' if b'\r\n' in b else b'\n'
anchor = b'# Companion-paper formalization handoff' + nl + nl
assert b.startswith(anchor)
prefix = f'''## Sharp PBPS corrector bound and modified energy (2026-10-09)

Independently VERIFIED science commit {head}. The reusable Hilbert estimate
I+K²=D² gives the exact c/2 bound without finite dimension or nontriviality.
SAME original PBPS inputs produce K=A0 Inv and D=Inv, hence B23 with 1/(2gamma).
Every actual globally centered f has its original conditional fP, perpendicular
component and fV, with norm(fP)²+norm(fV)²<=norm(f)² and the same sharp C bound.
The genuine original-input Test proves Lemma B3's half/three-halves energy
equivalence and exact perturbation bound for every0<omegaWeight<=gamma.
No caller/provider, extra regularity, strict endpoint or nontriviality is added.
Rank0 and alphaeta=1 remain legal. Full original literal private statements and
three whole modules have independent math, blind decoding and primary-first
source review; eleven formula steps have exact adjacent Lean BODY spans.
The corrected frontier classification records only the evidenced PBPS route;
the compiled Test is its transitive consumer, not a second consuming route.
The separately approved S,T notation overlay defines both energy sums in place
and refreshes the source packet without changing Lean, formulas or proof spans.

This closes sharp corrector energy only. Next dependency-ready source target
is B21's actual reflection intertwining and then corrector rotation, with the
exact U(P-Pperp) action and B4 consumer independently checked. The next bounded
reflection-intertwining Statement Seal69 is accepted but not yet proved.
H1/B2, B4 dynamics/hypocoercivity, invariance/nonexplosion, main results,
implementation errors and actual-input expected-query costs/composition remain
open. TV proximity does not transfer unbounded expected cost. Four-paper
priority and older routes remain intact. Full Exposition/PURIFIED, merged/live
and whole-paper/Goal completion remain separate unearned claims.

INT67 38e5f34 has all four exact remote workflows SUCCESS and scoped current
reader/graph admission. Historical INT66 graph-freshness withholding remains
historical. Serialized Registry516/imports/Tests/current reader/graph gates for
this cycle are pending and must be recorded against final admin state.

'''
p.write_bytes(anchor + prefix.encode().replace(b'\n', nl) + b[len(anchor):])
p = root / 'website/content/samplewiki_companion_frontiers.json'
frontiers = load(p)
frontiers['execution']['current_checkpoint'] = 'docs/companion-papers-handoff.md#sharp-pbps-corrector-bound-and-modified-energy-2026-10-09'
replace_json(p, frontiers)
print('Prepared serialized68 Registry516/imports/Tests/handoff; aggregate/current-reader/graph admission pending.')
