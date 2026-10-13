"""Admit verified A7 science through the existing sole stabilization lane."""
from pathlib import Path
import hashlib, json, re, subprocess, sys
root = Path(__file__).resolve().parents[3]
run = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'tools'))
import astis_advance as adv
load = lambda p: json.loads(p.read_bytes())
claim = load(run / 'claim.json')
state = adv.current_advances()[claim['advance_id']]
assert state['state'] == 'VERIFIED'
science = state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip() == science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=root).strip()
lanes = [s for s in adv.current_advances().values() if s['state'] == 'STABILIZING']
assert len(lanes) == 1 and lanes[0]['advance_id'] == 'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'
assert lanes[0]['latest_evidence']['integration_owner'] == 'companion_root_20261005'
out = run / 'integration95'
out.mkdir(exist_ok=False)
owned = ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows = []
for i, name in enumerate(owned):
    raw = (root / name).read_bytes()
    p = out / f'{i}.before.exactraw.snapshot'
    p.write_bytes(raw)
    rows.append(dict(path=name, raw_sha256=hashlib.sha256(raw).hexdigest(), snapshot=p.relative_to(root).as_posix()))
(out / 'owned-before.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
def after(name, anchor, text):
    p = root / name
    b = p.read_bytes()
    hits = list(re.finditer(rb'(?m)^'+re.escape(anchor.encode())+rb'(\r?\n|$)', b))
    assert len(hits) == 1 and text.encode() not in b
    h = hits[0]
    p.write_bytes(b[:h.end()]+text.encode().replace(b'\n',h.group(1) or b'\n')+b[h.end():])
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion'
decl = claim['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity', 'import '+module+'\n')
note = f'Independent science {science}. Under the six original analytic assumptions, the literal stopped-clock process satisfies the full A7 expectation expansion for every bounded real functional measurable for the coordinate-product path sigma algebra. Every weighted finite-simplex term is integrable and the signed component integrals are absolutely summable. Actual finite-count joint laws and the whole-path density identity are consumed internally. Covers n=0,T=0,rank0,zero rates and infinite waits. ASTIS uses countable probability-partition integration as an alternative to the printed rate-cap/factorial proof. No Skorokhod assertion, unbounded-test/cost transfer, restart/Markovness, invariance, hypocoercivity, implementation error, main result or actual-input composition completion.'
block = '  {\n'+'\n'.join(['    key := "pbps.actualBoundedPathExpansion"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS bounded real path functional expansion"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 A7"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "path", "density", "integrability", "summation"]','    saldUse := "Actual PBPS bounded path expectations; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = root / owned[2]
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 544') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 544',b'formalizedTechnicalLemmaCount = 545'))
prefix = f'''## Actual PBPS bounded path functional expansion (2026-10-11)

Independent science {science}. Under the original six analytic assumptions,
the actual jointly measurable stopped-clock process Z satisfies the full A7
identity for every globally bounded real F measurable for the coordinate-product
sigma algebra on phase-valued paths over [0,T]:

E[F(Z_T)] = sum_(n>=0) integral_Delta_n(T) F(Gamma_n(t)) w_n(t) dm_n(t),
w_n(t) = exp(-integral_0^T lambda(Gamma_n(t)(s))ds) product_i lambda(z_(i-)).

The left observable and every weighted simplex term are integrable. The family
of signed component integrals is unconditionally summable, hence absolutely
summable. The finite-count joint law and prescribed-path density are proved
parents, not supplied hypotheses. Zero events, zero horizon, rank0, zero rates,
stopping and infinite waits remain covered with the same actual raw fallback.
The source printed cap/factorial route remains separately indexed; the ASTIS
proof uses countable probability-partition integration to justify signed sums.

Independent mathematics/kernel, source-blind decoding, primary-first source
review, five adjacent formula/Lean explanations and exact-commit review passed.
The next source dependency is actual phase-volume preservation and reversal
mechanics (A6 and the flow), consumed by finite prescribed endpoint/time reversal
in A8. Restart/Markovness is separate from fixed-time stationarity. Reversal at
internal jump times must use the correct left-limit convention, not naive
pointwise reversal of a right-continuous path.

The sole existing stabilization lane handles aggregate publication/graph/site
checks. Actual page/fine-branch visual acceptance, main merge and postmerge
purification remain separate. No unbounded expectation or oracle-cost transfer,
Skorokhod identification, invariance, hypocoercivity, implementation errors,
main paper results or actual-input composition is claimed. All four full papers
remain open and the existing unbudgeted Goal remains active.

'''
def prepend(name, text):
    p = root / name
    b = p.read_bytes()
    nl = b'\r\n' if b'\r\n' in b else b'\n'
    first, rest = b.split(nl,1)
    assert text.splitlines()[0].encode() not in b
    p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3], prefix)
p = root / owned[4]
b = p.read_bytes()
old = b'#actual-pbps-prescribed-path-hazard-and-density-identity-2026-10-11'
assert b.count(old) == 1
p.write_bytes(b.replace(old,b'#actual-pbps-bounded-path-functional-expansion-2026-10-11',1))
prepend(owned[5], f'## Actual bounded path expansion95 (2026-10-11)\n\n{note}\n\nFive independently source-reviewed formula/Lean regions. Aggregate and visual checks, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualBoundedPathExpansion',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (root / owned[6]).open('ab') as f:
    f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8')
print('Verified A7 child admitted through existing lane; Registry545; aggregate checks pending.')
