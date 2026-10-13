"""Execute only after independent exact-commit VERIFIED; reuse the existing lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');load=lambda p:json.loads(Path(p).read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING'];assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration81';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability','import '+module+'\n')
note=f'Independently verified science {science}. Original six analytic conditions and literal actual recurrence give ideal exact-reference H_y at pi as a jointly measurable probability kernel. Exact q_y normalization is derived from Gibbs/conditional-kernel parents. Its independent reference x standard Gaussian x actual exponential product supports actual terminal arc and phase0 law dirac(x) x Gaussian. Full random all-time path law, version uniqueness, phase Markov/semigroup/invariance/mixing, reference implementation/errors/cost and actual PBPS-SPHMC composition remain OPEN. Local gates/visual/main/PURIFIED/live and whole-paper/Goal completion are distinct.'
block='  {\n'+'\n'.join(['    key := "pbps.idealHalfTurnKernel"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Ideal PBPS H_y half-turn returned-position kernel and actual product initialization"','    upstreamFile := "arXiv2609.06905v1 Algorithm1, Eq2.8, AppendixA1 SS2 p3.1-p4.1"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "ideal-reference", "kernel", "physical-time", "initialization"]','    saldUse := "Source ideal H_y invariance/mixing prerequisite; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 529')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 529',b'formalizedTechnicalLemmaCount = 530'))
prefix=f'''
## Ideal PBPS half-turn returned-position probability kernel (2026-10-10)

Independent exact-science commit {science}. The original six analytic conditions
and literal actual dynamics now produce the ideal exact-reference returned-position
kernel H_y at pi, jointly Borel in (y,x), with probability fibers. The exact
conditional reference law q_y is normalized internally via the canonical Gibbs
and Gaussian conditional-kernel parents. It is not the implemented approximate
reference law q-hat. Momentum is standard Gaussian, and input association is
((reference,momentum),actual exponential clock stream), independent as displayed.

The full finite-time origin/terminal live-arc event is proved Borel before product
Fubini. Hence, for each fixed y,x, this actual product law supports physical
initialization and a genuine live harmonic arc at pi. The phase0 pushforward is
dirac(x) x standard Gaussian. The previously verified joint phase and fixed-input
common-AE all-time properties remain intact, including last-live infinite waits,
rank0 and explicitly labelled exceptional fallback conventions. No arbitrary
correlated random-parameter substitution or uniform parameter AE event is inferred.

Ten exact formula/BODY regions passed independent mathematics, source-blind
reconstruction and source-first coverage review. This closes an ideal initialized
probability-kernel edge, not an implemented sampler or full PBPS theorem. Full
random all-time path law/version uniqueness, phase Markov/semigroup/invariance,
mixing/hypocoercivity, approximate-reference implementation/errors/oracle cost,
and actual-input PBPS-SPHMC composition remain OPEN. TV proximity never transfers
unbounded expected cost. Current next work must be selected from the capsule and
source-ready frontier, not old counts or this list interpreted as invented dependencies.

Priority remains PBPS/SPHMC and actual-input composition, then Gaussian Cloud,
then midpoint without extra higher derivatives. Preserve older routes/cycles and
collaborator work. The sole existing stabilization lane carries this VERIFIED
child; serialized aggregate/site/graph and reader visual acceptance are pending
for this snapshot. Main merge, PURIFIED/Exposition, live delivery and whole Goal
completion remain separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-jointly-measurable-physical-time-phase-2026-10-10';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#ideal-pbps-half-turn-returned-position-probability-kernel-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Ideal initialized half-turn probability kernel81 (2026-10-10)\n\nIndependent science {science}. Exact conditional q_y normalization and jointly Borel ideal H_y at pi are internally constructed. The actual independent reference/Gaussian/clock product supports physical origin and terminal live arc; phase0 law is dirac(x) x Gaussian. Original six conditions, all actual definitions and previous phase semantics retained. Ten formula/BODY regions are authored once beside exact folded Lean. This is ideal exact-reference semantics, not reference implementation, phase Markov/invariance, mixing, error/cost/composition or full-paper completion. Aggregate, reader visual, main/live and purification remain separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.idealHalfTurnKernel',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED81 inside sole existing lane; Registry530/imports/Tests; aggregate pending')
