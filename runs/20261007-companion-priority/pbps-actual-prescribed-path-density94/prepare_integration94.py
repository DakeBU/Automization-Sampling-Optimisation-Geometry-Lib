"""The sole existing stabilization lane admits only independently VERIFIED science."""
from pathlib import Path
import hashlib,json,subprocess,sys,re
R=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
claim=load(run/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED';science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
lanes=[x for x in adv.current_advances().values() if x['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=run/'integration94';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows=[]
for i,name in enumerate(owned):
 b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);rows.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.relative_to(R).as_posix()))
(out/'owned-before.json').write_bytes((json.dumps(rows,indent=2)+'\n').encode())
def after(name,anchor,text):
 p=R/name;b=p.read_bytes();hits=list(re.finditer(rb'(?m)^'+re.escape(anchor.encode())+rb'(\r?\n|$)',b));assert len(hits)==1 and text.encode() not in b
 h=hits[0];nl=h.group(1) or b'\n';p.write_bytes(b[:h.end()]+text.encode().replace(b'\n',nl)+b[h.end():])
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath','import '+module+'\n')
note=f'Independent science {science}. Under exactly the six original analytic assumptions and the literal actual93 prescribed interpolation, every finite strict event tuple has integrable path rate, an exact n+1-arc hazard integral sum, incoming phase and rate left limits, and rho=ofReal(exp(-whole-path hazard integral) times product of incoming jump rates). Terminal survival, n=0, T=0, rank0 and zero rates are retained. No additional path/integrability/limit provider. This deterministic ingredient does not yet compose the actual finite-count measure with the printed density or sum full A7. Restart/Markovness, invariance, hypocoercivity, implementation errors, expected cost, paper mains, actual-input composition and four-paper completion remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPrescribedPathDensity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS prescribed-path hazard and density identity"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 A7 prescribed trajectory ingredient"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "path", "hazard", "left-limit", "density"]','    saldUse := "Finite PBPS prescribed-path density consumer; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 542')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 542',b'formalizedTechnicalLemmaCount = 543'))
prefix=f'''## Actual PBPS prescribed-path hazard and density identity (2026-10-11)

Independent science {science}. All six original analytic assumptions and
twenty actual93 definitions are unchanged. For every finite strict event tuple,
the actual prescribed path Gamma, extended only by clamping real time, satisfies

integral_0^T lambda(gamma(s))ds = sum_(j=0)^n Lambda_(z_j)(a_(j+1)-a_j),
rho_n = ofReal(exp(-integral_0^T lambda(gamma(s))ds) product_(i=1)^n lambda(z_(i-))).

Rate interval integrability and the incoming phase/rate left limits are proved.
The terminal survival arc, zero-event and zero-horizon cases, rank0 and zero rates
are included. No continuity of reflection at zero normal or integrability/limit
provider has been added. The phase limit topology is ordinary E x E; there is no
new topology or Skorokhod assertion on the space of paths.

Independent whole math/kernel, anonymous decoder, primary-first source and seven
adjacent formula/Lean explanations passed, including exact science-commit review.
Proof prose explicitly records ordered intervals and continuous comparison arcs.
Only deterministic DENSITY94 closes. The next mathematical edge is TERM93: insert
this formula into the already verified actual finite-count history/path measure,
then assemble the source A7 all-count expansion with its exact test-function scope.
Markovness/restart, invariance, hypocoercivity, implementation errors, expected cost,
paper main results, actual-input composition and all four full papers remain OPEN.

Aggregate gates use the original sole stabilization lane. Actual paper-page and
fine-branch visual acceptance, main merge and postmerge purification remain separate.
The existing unbudgeted four-paper Goal remains active.

'''
p=R/owned[3];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1);assert prefix.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+prefix.encode().replace(b'\n',nl)+rest)
p=R/owned[4];b=p.read_bytes();old=b'#actual-pbps-finite-count-complete-path-law-2026-10-11';assert b.count(old)==1;p.write_bytes(b.replace(old,b'#actual-pbps-prescribed-path-hazard-and-density-identity-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1);txt=f'\n## Actual prescribed-path density94 (2026-10-11)\n\n{note}\n\nSeven source-reviewed formula/Lean proof regions; visual/main merge/purification remain distinct.\n\n';p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualPrescribedPathDensity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_bytes((json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n').encode())
print('Admitted verified94 into existing sole lane; Registry543 and actual root imports/tests; aggregate gates pending.')
