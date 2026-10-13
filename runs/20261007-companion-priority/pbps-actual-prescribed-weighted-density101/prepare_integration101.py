"""Admit independently verified path reversal through the existing sole lane."""
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
out=run/'integration101';out.mkdir(exist_ok=False)
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
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal','import '+module+'\n')
note=f'Independent science {science}. Original six analytic assumptions and exact actual density rho=q*terminalweight. One reversed event-time map yields both w(z)dReal(z,t)=w(RA)dReal(RA,rho(t)) and ofReal(w(z))*rho(z,t)=ofReal(w(RA))*rho(RA,rho(t)). Four public actual parents94/98/99/100 discharge density bridge, Gibbs survival, incoming product and reflected survival. Includes n=0,T=0,rank0,zero normals/rates; no rate division. No weighted sector/integral invariance, normalized invariant probability, Markovness, hypocoercivity, errors, costs, main results or composition.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPrescribedWeightedDensity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS weighted prescribed density matching"','    upstreamFile := "arXiv2609.06905v1 Eq3.1 and Appendix A1 A7/A8 weighted density"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "weighted-density", "reversal", "finite-path"]','    saldUse := "Actual finite PBPS weighted density matching; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 550')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 550',b'formalizedTechnicalLemmaCount = 551'))
prefix=f'''## Actual PBPS weighted prescribed density matching (2026-10-12)

Independent science {science}. Under the original six analytic assumptions,
the exact actual density rho=q times terminal live survival satisfies

w(z) dReal(z,t) = w(RA) dReal(RA,rho(t)),
ofReal(w(z)) rho(z,t) = ofReal(w(RA)) rho(RA,rho(t)).

Here A is the actual terminal state, R flips momentum, w=exp(-U) uses
the target energy, and the same produced reversal map has zero-based
coordinates rho(t)_i=T-t_(n-1-i). The proof combines actual density94,
Gibbs survival98, incoming product99 and scalar integral reversal100.
No rate is divided out; zero rates, normals, dimension and horizon remain
covered. This is pointwise unnormalized density matching.

Independent whole mathematics, sealed-header kernel witness, fresh anonymous
decoding and primary-first source/exposition reviews passed. The six adjacent
formula/Lean steps state the indexing convention explicitly; its small
exposition clarification was independently reviewed. The original mathematical
statement and Lean proof are unchanged.

Next: weighted-sector substitution using the actual endpoint/time volume map,
then normalized Gibbs averaging/invariance. Markovness, hypocoercivity,
implementation errors, actual expected costs and actual-input composition
remain open. Full papers completed remains 0/4.

The existing sole SAU94 lane owns aggregate publication/graph/site integration.
Page/fine-branch visual acceptance, main merge and postmerge purification retain
separate evidence; the original four-paper Goal and reading contract persist.

'''
def prepend(name,text):
 p=Path(name);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
 assert text.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3],prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'#actual-pbps-path-reversal-and-survival-substitution-2026-10-12';assert b.count(old)==1
p.write_bytes(b.replace(old,b'#actual-pbps-weighted-prescribed-density-matching-2026-10-12',1))
prepend(owned[5],f'## Actual prescribed weighted density101 (2026-10-12)\n\n{note}\n\nSix source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry=dict(key='pbps.actualPrescribedWeightedDensity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Verified weighted-density child admitted through existing lane; Registry551; aggregate checks pending.')
