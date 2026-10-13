from pathlib import Path
import json,subprocess,datetime
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Root must strictly adopt native exact verification before this script is executed.
v=j(r/'root.exact-verification58.adoption.json');head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert v['verified_commit']==head and v['native_verified']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=j(r/'publication-plan.json');assert not (r/'sync-before-integration58.json').exists()
w(r/'sync-before-integration58.json',dict(head=head,origin_main=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),action='Prior safe fetch preserved; no reset/checkout/merge.',utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
entries=[]
for i,(key,label,tags) in enumerate([('l2Pullback.rangeEqLpMeas','Canonical arbitrary-measure real L2 pullback range',['measure-preserving','L2','comap','factorization']),('pbps.actualMacroscopicCenteredRange','PBPS B1-B5 actual macro range and centered image',['PBPS','L2','conditional-expectation','centered-range'])]):
 assert key not in s;decl=plan['mathematical_declarations'][i]
 note=('Arbitrary measurable spaces/measures; genuine measure-preserving map. Exact range equals comap AE strongly measurable L2 submodule, with internally constructed factor and MemLp transfer; no probability/finite-measure/StandardBorel premise. Actual PBPS consumer.' if i==0 else 'Original C2, both Hessian bounds, positive capped eta. Actual Gibbs/Gaussian J and nu; canonical snd pullback range equals true conditional projection range; mean transport and full centered image. Finite real Hilbert/Borel/rank0 extension explicit. Real Test joins same55 reflection/mean with57 contraction to give allmacro sharp contraction and squared defect gap. No Gamma/root/inverse/weakH1/dynamics/cost/composition closure.')
 entry='  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(label)+'\n    upstreamFile := "arXiv2609.06905v1 AppendixB B1-B5/C3-C4"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note+' Independently verified '+head+'.')+'\n  },\n'
 entries.append(entry)
 row=dict(key=key,local_decl=decl,local_file=['AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean'][i],status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=label,upstream_file='arXiv2609.06905v1 AppendixB',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note)
 with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
p.write_text(s.replace(anchor,anchor+''.join(entries)),encoding='utf-8')
for file,anchor,addition in [('AutoSamplingTheory/TechnicalLemmas/Measure.lean','import AutoSamplingTheory.Probability','import AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean','import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange'),('Tests.lean','import Tests.GaussianMarginalPoincare','import Tests.ProximalBPSMacroscopicRange')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 498')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 498','formalizedTechnicalLemmaCount = 500'),encoding='utf-8')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');c=j(p);assert c['status']=='independently_verified';c['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,c)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS macroscopic centered range (2026-10-08)

Independently VERIFIED at {head}. The canonical real L2 pullback for any
measure-preserving map has range exactly the comap AE measurable L2 submodule.
No probability, finite-measure or StandardBorel assumption is added. Applied
to the actual Gaussian augmentation J and its second marginal nu, it proves
ran(M)=ran(P), integral_J(Mu)=integral_nu(u), and
M[L2_0(nu)]=ran(P) intersect L2_0(J). Probability and normalization are derived
from the standing original C2/two Hessian/positive capped eta assumptions.
Finite real Hilbert/Borel and rank-zero are disclosed source extensions;
real L2 may be finite or infinite dimensional.

The real Test identifies the SAME actual55 M/T with canonical pullback and
actual57 conditional mean. Every centered macro f=Mu therefore satisfies
||A f|| <= (1-alpha*eta)/(1+alpha*eta)||f|| and
4*alpha*eta/(1+alpha*eta)^2 ||f||^2 <= ||B f||^2.
The same reflection and conditional law occur throughout, including rank zero
and alpha*eta=1. Production imports no Tests and duplicates no Poincare proof.
These are squared-defect bounds; Gamma positivity/root/uniqueness and inverse
are independent remaining mathematics.

All three preproof signatures remain exact. Focused3908, complete independent
mathematics, anonymous source/identity-blind decoder and anti-anchored source
fidelity pass. Three original metadata negatives and independently reviewed
editorial overlays remain unchanged; current metadata has zero blockers.
The source0 schema classification addendum is separate from the immutable
original review. Exact-science verification is distinct from serialized
Registry500/root Tests, affected graph/page checks and later repository/
exposition seals. Main/live/postmerge PURIFIED and full-paper acceptance stay
open; earlier frontiers, cycles and memory remain preserved.

Next dependency-ready edge: the same actual scalar T is self-adjoint and
preserves mean by its genuine stationary conditional law. Restrict it to the
closed centered real L2 subspace, then obtain the positive defect I-T0^2 and
its sharp coercivity through the actual macro consumer. The bounded source-only
59 audit identifies fixed real-Hilbert APIs for this route without assuming
finite-dimensional L2 or a caller CFC certificate. A centered inverse of the
squared defect is separate from Gamma inverse. Full weighted weak H1,
C5-C7/half-turn, PBPS dynamics/nonexplosion/hypocoercivity/errors/cost/main and
actual-input PBPS/SPHMC composition remain open. SPHMC smoothing/Picard/Wp/
proxy-warmness remain independent. Gaussian Cloud and midpoint follow the
active four-paper priority. TV proximity does not transfer unbounded cost.
This local theorem packet completes neither a paper nor the Goal.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8')
p=Path('website/content/samplewiki_companion_frontiers.json');d=j(p);d['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-macroscopic-centered-range-2026-10-08';w(p,d)
print('58 serialized Registry500/imports/handoff prepared; actual aggregate checks required.')
