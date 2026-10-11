"""Admit independently verified endpoint science through the existing sole lane."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
root=Path.cwd();run=Path(__file__).parent;sys.path.insert(0,str(root/'tools'))
import astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
claim=load(run/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED';science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=run/'integration98';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows=[]
for i,name in enumerate(owned):
    raw=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(raw)
    rows.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n')
def after(name,anchor,text):
    p=Path(name);b=p.read_bytes();hits=list(re.finditer(rb'(?m)^'+re.escape(anchor.encode())+rb'(\r?\n|$)',b))
    assert len(hits)==1 and text.encode() not in b
    h=hits[0];p.write_bytes(b[:h.end()]+text.encode().replace(b'\n',h.group(1) or b'\n')+b[h.end():])
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal','import '+module+'\n')
note=f'Independent science {science}. Under the original six analytic assumptions, both actual prescribed-path rate integrals are finite and U_y(A)-U_y(z)=Iplus-Iminus, hence exp(-U_y(z))*exp(-Iplus)=exp(-U_y(A))*exp(-Iminus). The reverse rate uses momentum reversal along the same path. Actual flow, bounce, finite-count path and endpoint laws discharge all private premises. Includes n=0,T=0,rank0,zero normals and zero rates. No reverse-event density matching, weighted Theta preservation, invariant probability, Markovness, hypocoercivity, errors, actual expected costs, main results or composition.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPrescribedGibbsSurvival"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS finite-path energy and Gibbs/survival balance"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 A4 and its integrated Gibbs/survival identity"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "energy", "Gibbs", "survival", "finite-path"]','    saldUse := "Actual finite PBPS target-energy and survival balance; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 547')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 547',b'formalizedTechnicalLemmaCount = 548'))
prefix=f"""## Actual PBPS finite-path Gibbs and survival balance (2026-10-12)

Independent science {science}. The original six analytic assumptions and literal
actual path definitions remain fixed. Both real-time rates along every finite
prescribed path are interval integrable, and

U_y(A)-U_y(z)=Iplus-Iminus,
exp(-U_y(z))*exp(-Iplus)=exp(-U_y(A))*exp(-Iminus).

Here A=Gamma(T), U_y(x,p)=V(x)+norm(x-y)^2/(2 eta)+norm(p)^2/2,
and Iminus integrates the rate at R(Gamma(s)) along the SAME path.
Actual harmonic ODE, bounce norm preservation, finite-count open-arc identity
and terminal endpoint law are the four invoked parent producers. Finite arc
calculus, integration and energy telescoping are proved internally.
Zero events, horizon, dimension, rates and reflection normals remain included.

Independent whole mathematics, fresh sealed-header kernel witness, source-blind
decoding and primary-first source/exposition reviews passed. All six adjacent
formula/Lean proof regions retain their exact source-bound code.
The next source edges are reverse-arc and incoming-rate product correspondence,
then weighted sector substitution and Gibbs averaging. Pointwise equality of
right-continuous paths at reversed jumps is not claimed. Invariance, Markovness,
hypocoercivity, implementation errors, actual expected costs and composition
remain open; full papers completed is still0/4.

The existing sole SAU94 lane handles aggregate publication/graph/site gates.
Actual paper-page/fine-branch visual acceptance, main merge and postmerge
purification are separate; retain the existing four-paper Goal and reader contract.

"""

def prepend(name,text):
    p=Path(name);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
    assert text.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3],prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'#actual-pbps-finite-endpoint-and-event-time-reversal-2026-10-12';assert b.count(old)==1
p.write_bytes(b.replace(old,b'#actual-pbps-finite-path-gibbs-and-survival-balance-2026-10-12',1))
prepend(owned[5],f'## Actual prescribed Gibbs and survival balance98 (2026-10-12)\n\n{note}\n\nSix source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry=dict(key='pbps.actualPrescribedGibbsSurvival',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Verified endpoint child admitted through existing lane; Registry548; aggregate checks pending.')
