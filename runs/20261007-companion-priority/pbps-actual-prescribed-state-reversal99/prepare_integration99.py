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
out=run/'integration99';out.mkdir(exist_ok=False)
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
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival','import '+module+'\n')
note=f'Independent science {science}. Original six analytic assumptions and actual path definitions. Reversing the strict event tuple gives barPost_j=R(arrive_(n-j)) and barArrive_j=R(post_(n-j)) on all n+1 arcs; products of the n incoming event rates agree. Actual phase reversal and endpoint laws discharge all private premises. Includes n=0,T=0,rank0,zero normals and rates. No all-time right-continuous path equality, survival time substitution, weighted density equality, invariant probability, Markovness, hypocoercivity, errors, expected costs, main results or composition.'

block='  {\n'+'\n'.join(['    key := "pbps.actualPrescribedStateReversal"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS finite-state reversal and incoming-rate product"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 A5 and A8 finite incoming-state reversal"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "reversal", "incoming-rates", "finite-path"]','    saldUse := "Actual finite PBPS paired-state reversal and rate product; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 548')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 548',b'formalizedTechnicalLemmaCount = 549'))
prefix=f"""## Actual PBPS finite-state and incoming-rate reversal (2026-10-12)

Independent science {science}. Under the original six analytic assumptions and
literal actual path definitions, reversing the strict event tuple produces

barPost_j=R(arrive_(n-j)), barArrive_j=R(post_(n-j)) for j=0,...,n,
product_(i<n) lambda(barArrive_i)=product_(i<n) lambda(arrive_i).

The n+1 arc indices and n event indices have distinct reversals. The terminal
arrival is not an event-rate factor. A reversed post-bounce state corresponds
to an original incoming state. Right-continuous path values at genuine jumps
are not asserted to reverse pointwise. Actual phase-volume/reversal and actual
endpoint/time-reversal laws are the two invoked producers; finite induction,
reverse grid gaps and incoming-rate reindexing are proved internally.
Zero events, horizon, dimension, reflection normals and rates remain included.

Independent whole mathematics, fresh sealed-header kernel witness, anonymous
decoding and primary-first source/exposition reviews passed. Six adjacent
formula/Lean steps preserve the reviewed exact code and full assumptions.
Next: actual open-arc/off-event reversal and survival-integral time substitution,
then weighted sector substitution and Gibbs averaging. Invariance, Markovness,
hypocoercivity, implementation errors, actual expected costs and composition
remain open; full papers completed remains 0/4.

The existing sole SAU94 lane owns aggregate publication/graph/site integration.
Actual page/fine-branch visual acceptance, main merge and postmerge purification
remain separate; retain the four-paper Goal and its reading contract.

"""

def prepend(name,text):
    p=Path(name);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
    assert text.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3],prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'#actual-pbps-finite-path-gibbs-and-survival-balance-2026-10-12';assert b.count(old)==1
p.write_bytes(b.replace(old,b'#actual-pbps-finite-state-and-incoming-rate-reversal-2026-10-12',1))
prepend(owned[5],f'## Actual prescribed state reversal99 (2026-10-12)\n\n{note}\n\nSix source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry=dict(key='pbps.actualPrescribedStateReversal',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Verified finite-state child admitted through existing lane; Registry549; aggregate checks pending.')
