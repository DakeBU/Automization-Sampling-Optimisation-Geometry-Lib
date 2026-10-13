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
out=run/'integration97';out.mkdir(exist_ok=False)
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
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume','import '+module+'\n')
note=f'Independent science {science}. Under the original six analytic assumptions, rho(t)_i=T-t_(n-1-i) is a measurable involution preserving exact strict-simplex comap volume m. A=Gamma(T) equals the final flow after the recursive post-bounce state, is jointly Borel and preserves phase volume ell for each event tuple. A(R A(z,t),rho t)=Rz. Theta(z,t)=(R A(z,t),rho t) is jointly Borel, involutive and preserves ell tensor m. Includes n=0, T=0, rank0 and zero normals. Actual OrderedPrefix, FiniteCountPath and PhaseReversalVolume supply dependencies internally. Gibbs-weight balance, stationary averaging/invariance, restart/Markovness, hypocoercivity, implementation errors, expected costs, main results and actual-input composition remain open.'
block='  {\n'+'\n'.join(['    key := "pbps.actualEndpointTimeReversal"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS finite endpoint and event-time reversal"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 endpoint/time substitution surrounding A8"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "endpoint", "simplex", "reversal", "volume"]','    saldUse := "Actual finite PBPS endpoint/time change of variables; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 546')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 546',b'formalizedTechnicalLemmaCount = 547'))
prefix=f'''## Actual PBPS finite endpoint and event-time reversal (2026-10-12)

Independent science {science}. The original six analytic assumptions and thirteen
actual path definitions are unchanged. For every n>=0 and T>=0, rho reverses the
strict ordered event tuple and preserves its exact unnormalized comap volume m.
The actual terminal map A=Gamma(T) is jointly Borel and preserves phase volume
ell for every tuple. Its finite flow/bounce word gives

A(R A(z,t),rho t)=R z,
Theta(z,t)=(R A(z,t),rho t), Theta^2=id,
Theta_#(ell tensor m)=ell tensor m.

Independent whole mathematics, fresh sealed-header kernel witness, anonymous
decoding, primary-first source and six formula/Lean proof-region reviews passed.
Actual OrderedPrefix, FiniteCountPath and PhaseReversalVolume are the three
compiled parent producers. All generic helper premises are discharged internally.
The exact subtype measure is proved sigma finite before the skew-product step.
Zero events, zero horizon, rank zero and zero reflection normals are included.

The next bounded source dependency is Gibbs-weight balance for finite prescribed
paths, leading to weighted A8 sector substitution and stationary averaging.
At internal jumps use left/right limits or off-finite-event time equality;
pointwise reversal of right-continuous path values is not claimed.
Restart/Markovness remains separate. No invariant probability law, hypocoercivity,
implementation error, expected query cost, main theorem or composition is closed.

Aggregate publication/graph/site checks use the existing sole SAU94 lane.
Actual paper-page/fine-branch visual acceptance, main merge and postmerge
purification remain separate. All four full papers remain open; retain the
existing Goal and its four-paper priority, fixed versions and reader contract.

'''
def prepend(name,text):
    p=Path(name);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
    assert text.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3],prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'#actual-pbps-phase-volume-preservation-and-reversal-2026-10-12';assert b.count(old)==1
p.write_bytes(b.replace(old,b'#actual-pbps-finite-endpoint-and-event-time-reversal-2026-10-12',1))
prepend(owned[5],f'## Actual endpoint and time reversal97 (2026-10-12)\n\n{note}\n\nSix source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification retain separate evidence.\n\n')
entry=dict(key='pbps.actualEndpointTimeReversal',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Verified endpoint child admitted through existing lane; Registry547; aggregate checks pending.')
