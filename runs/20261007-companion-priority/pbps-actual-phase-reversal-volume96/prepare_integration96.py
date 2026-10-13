"""Admit verified phase-volume science through the existing sole stabilization lane."""
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
out = run / 'integration96'
out.mkdir(exist_ok=False)
owned = ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows = []
for i, name in enumerate(owned):
    raw = (root / name).read_bytes()
    p = out / f'{i}.before.exactraw.snapshot'
    p.write_bytes(raw)
    rows.append(dict(path=name, raw_sha256=hashlib.sha256(raw).hexdigest(), snapshot=p.relative_to(root).as_posix()))
(out / 'owned-before.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n')
def after(name, anchor, text):
    p = root / name
    b = p.read_bytes()
    hits = list(re.finditer(rb'(?m)^'+re.escape(anchor.encode())+rb'(\r?\n|$)', b))
    assert len(hits) == 1 and text.encode() not in b
    h = hits[0]
    p.write_bytes(b[:h.end()]+text.encode().replace(b'\n',h.group(1) or b'\n')+b[h.end():])
module = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume'
decl = claim['target_declarations'][0]
for name in owned[:2]:
    after(name, 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion', 'import '+module+'\n')
note = f'Independent science {science}. Under the original six analytic assumptions, the literal harmonic flow, state-dependent bounce and momentum reversal preserve canonical phase product volume. Joint Borel maps, both flow inverses, bounce/reversal involutions, R Phi_u R=Phi_-u, R S=S R, rate(R S z)=rate(z), and the real integrable-test A6 identity are proved. Covers rank0, zero normals and all real times without an unscaled isometry claim. Volume and regularity are derived, not provider assumptions. Finite prescribed endpoint/time reversal, stationary averaging, invariance, Markovness, hypocoercivity, implementation errors, expected costs, main results and actual-input composition remain open.'

block = '  {\n'+'\n'.join(['    key := "pbps.actualPhaseReversalVolume"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS phase product-volume and reversal laws"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 flow A5 A6 and elementary A8 mechanics"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "volume", "reflection", "reversal", "integrability"]','    saldUse := "Actual PBPS phase-volume changes of variables; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1], 'def analysisMemory : List LemmaMemoryEntry := [', block)
p = root / owned[2]
b = p.read_bytes()
assert b.count(b'formalizedTechnicalLemmaCount = 545') == 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 545',b'formalizedTechnicalLemmaCount = 546'))
prefix = f"""## Actual PBPS phase-volume preservation and reversal (2026-10-12)

Independent science {science}. The original six analytic hypotheses and eight
literal definitions are unchanged. The actual harmonic flow Phi, state-dependent
bounce S and momentum reversal R preserve ell=volume_E tensor volume_E:

(Phi_u)_#ell = (S_r)_#ell = R_#ell = ell,
R Phi_u R = Phi_(-u), R S_r = S_r R, lambda_r(R S_r z)=lambda_r(z).

Joint Borel maps, both flow inverses and both involutions are proved/reused from
actual parents. For every real ell-integrable F, F composed with S_r is integrable
and its integral equals that of F (A6). Covers all real u, zero normals and rank0.
The harmonic volume proof factors into translations and shears, with cos(u)=-1
handled by simultaneous negation. No unscaled phase-norm isometry is asserted.

Independent whole mathematics/kernel, anonymous decoding, primary-first source,
seven formula/Lean proof explanations and exact science-commit verification passed.
The next genuine source dependency is finite prescribed endpoint/time reversal
in A8, followed by weighted A7 averaging and Gibbs density balance. At internal
jumps, reversal must respect left limits/off-finite-event time equivalence, not
naive equality of right-continuous path values. Restart/Markovness is separate.

Aggregate publication/graph/site gates use the original sole stabilization lane.
Actual paper-page/fine-branch visual acceptance, main merge and postmerge
purification remain separate. No stationary invariant law, hypocoercivity,
implementation error, expected cost, main theorem or actual-input composition
is claimed. Four full papers remain open; the existing unbudgeted Goal is active.

"""
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
old = b'#actual-pbps-bounded-path-functional-expansion-2026-10-11'
assert b.count(old) == 1
p.write_bytes(b.replace(old,b'#actual-pbps-phase-volume-preservation-and-reversal-2026-10-12',1))
prepend(owned[5], f'## Actual phase-volume and reversal96 (2026-10-12)\n\n{note}\n\nSeven independently source-reviewed formula/Lean regions. Aggregate and visual checks, main merge and purification retain separate evidence.\n\n')
entry = dict(key='pbps.actualPhaseReversalVolume',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (root / owned[6]).open('ab') as f:
    f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Verified phase-volume child admitted through existing lane; Registry546; aggregate checks pending.')
