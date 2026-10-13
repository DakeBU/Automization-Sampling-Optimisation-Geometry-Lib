"""Admit independently verified position averaging through the existing sole lane."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
root=Path.cwd();r=Path(__file__).parent;sys.path.insert(0,str(root/'tools'));import astis_advance as adv
load=lambda p:json.loads(Path(p).read_bytes())
c=load(r/'claim.json');state=adv.current_advances()[c['advance_id']];assert state['state']=='VERIFIED';science=state['latest_evidence']['verified_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,'HEAD']).returncode==0
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING'];assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity';assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration109';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
rows=[]
for i,name in enumerate(owned):
 raw=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(raw);rows.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n')
def after(name,anchor,text):
 p=Path(name);b=p.read_bytes();hits=list(re.finditer(rb'(?m)^'+re.escape(anchor.encode())+rb'(\r?\n|$)',b));assert len(hits)==1 and text.encode() not in b;h=hits[0];p.write_bytes(b[:h.end()]+text.encode().replace(b'\n',h.group(1) or b'\n')+b[h.end():])
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging';decl=c['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality','import '+module+'\n')
note=f'Independent science {science}. Under the original six assumptions, retain the same108 global actual process Z, phase family A and canonical flip J. Construct the position lift B and Gaussian adjoint M=B*. For every arbitrary MemLp phase representative, derive Gaussian section integrability, output L2 membership and the literal Gaussian mean class. Prove JB=B and MJ=M, then K_T=M A_T B is selfadjoint, norm at most1 and K_0=id. Identify its literal Gaussian-outer clock-inner position expectation, with both nested AE integrability statements. Rank0 included. No new source premise. Markov positivity/constants, strong continuity, restart/semigroup, separate kernel witnesses, independent-reference averaging, hypocoercivity, errors, actual expected costs, composition and all four complete papers remain open.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPositionL2Averaging"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS Gaussian momentum averaging and position L2 contraction"','    upstreamFile := "arXiv2609.06905v1 Appendix A.1(iii) final averaging proof"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "L2", "Gaussian-average", "self-adjoint"]','    saldUse := "Actual PBPS position averaging; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();matches=re.findall(rb'formalizedTechnicalLemmaCount = (\d+)',b);assert len(matches)==1;after_count=int(matches[0])+1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = '+matches[0],b'formalizedTechnicalLemmaCount = '+str(after_count).encode(),1))
prefix=f'''## Actual PBPS Gaussian position L2 averaging (2026-10-12)

Independent science {science}. Original six analytic assumptions and all108
outputs remain on the same global actual process Z, phase family A_T and
canonical momentum flip J. With pi_y the actual tilted position law and
gamma the probability standard Gaussian, the canonical position lift B
pulls back along fst. Its adjoint M is identified with the literal Gaussian
integral for every arbitrary MemLp phase representative. Section integrability,
output L2 membership and quotient equality are proved internally.

Flip absorption JB=B and MJ=M gives the compressed position operator
K_T=M A_T B: K_T.adjoint=K_T, norm at most1, and K_0=id. The same108 actual
clock expectation identifies K_T[f] with the Gaussian-outer, clock-inner
position integral. Both nested AE integrability conclusions are proved;
there is no interchange of integrals or extra Borel assumption on MemLp inputs.

The source graph has123 nodes and247 edges after independently admitted
namespace and L1-indicator implementation adapters. The original sealed graph
and all source slices are retained. The L2-inner integrability route remains
an unselected alternative. Eight adjacent formula/Lean regions explain the
proof. Independent exact header, whole mathematics, fresh source-blind decoding,
primary-first source/exposition review and exact-commit admission passed.

Markov positivity/constants, strong continuity, restart/semigroup, separate
kernel-witness identification, independent-reference half-turn averaging,
hypocoercivity, implementation errors, actual expected costs and composition
remain red. Full paper completion remains0/4. Public integration uses the sole
SAU94 lane; actual browser acceptance, main merge and purification are separate.

'''
def prepend(name,text):
 p=Path(name);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1);assert text.splitlines()[0].encode() not in b;p.write_bytes(first+nl+nl+text.encode().replace(b'\n',nl)+rest)
prepend(owned[3],prefix)
p=Path(owned[4]);b=p.read_bytes();anchor=b'#actual-pbps-full-real-l2-flip-duality-2026-10-12';assert b.count(anchor)==1;p.write_bytes(b.replace(anchor,b'#actual-pbps-gaussian-position-l2-averaging-2026-10-12',1))
prepend(owned[5],f'## Actual Gaussian position L2 averaging109 (2026-10-12)\n\n{note}\n\nEight source-reviewed formula/Lean regions. Aggregate/visual acceptance, main merge and purification remain separate.\n\n')
entry=dict(key='pbps.actualPositionL2Averaging',local_decl=decl,local_file=c['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(f'Verified position averaging child admitted through sole lane; Registry{after_count}; aggregate gates pending.')
