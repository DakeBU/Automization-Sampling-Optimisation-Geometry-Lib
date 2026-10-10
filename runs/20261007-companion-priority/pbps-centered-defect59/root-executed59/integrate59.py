from pathlib import Path
import json,subprocess
r=Path('runs/20261007-companion-priority/pbps-centered-defect59');load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
v=load(r/'root.exact-verification59.adoption.json');head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert v['native_verified'] and v['verified_commit']==head=='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad';assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json')
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1;key='pbps.actualCenteredSelfadjointDefect';assert key not in s;decl=plan['mathematical_declarations'][0]
note='Original C2/global two Hessian/positive capped eta. Actual stationary reflected Gaussian kernel produces real L2 selfadjoint mean operator and canonical AE constant; its whole closed centered restriction and actual full/centered positive squared defects are proved. Real Test consumes exact58 macro contraction for rho/delta and IsUnit of the squared defect only on the centered domain. Rank-zero extension and alpha*eta=1 retained; no finite-dimensional L2 or caller regularity/root certificate. Gamma/root/polar/fullH1/dynamics/main/error/cost/composition remain open. Independently verified '+head+'.'
entry='  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := "PBPS actual centered selfadjoint squared defect"\n    upstreamFile := "arXiv2609.06905v1 AppendixB B1-B5/D1-D2"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ["PBPS", "L2", "centered", "selfadjoint", "squared-defect"]\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n';p.write_text(s.replace(anchor,anchor+entry),encoding='utf-8',newline='\n')
row=dict(key=key,local_decl=decl,local_file='AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean',status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=['PBPS','L2','centered','selfadjoint','squared-defect'],upstream_decl='PBPS actual centered selfadjoint squared defect',upstream_file='arXiv2609.06905v1 AppendixB/D',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note)
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
for file,anchor,addition in [('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange','import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator'),('Tests.lean','import Tests.ProximalBPSMacroscopicRange','import Tests.ProximalBPSCenteredDefect')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 500')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 500','formalizedTechnicalLemmaCount = 501'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS centered squared defect (2026-10-08)

Independently VERIFIED science commit {head}. Under the original C2,
both global Hessian bounds, 0<alpha<=beta, eta>0 and beta*eta<=1, the actual
reflected Gaussian marginal kernel produces the SAME real L2 operator T.
Its selfadjointness, mean preservation, canonical constant q, exact closed
centered kernel H0=L2_0(nu), actual selfadjoint restriction T0, and positive
full/centered squared defects D=I-T^2,D0=I_H0-T0^2 are proved internally.
The full D annihilates q; the centered D0 is its actual restriction.
The real Test consumes exact58 allmacro contraction and the actual M mean
transport, yielding rho=(1-alpha*eta)/(1+alpha*eta),
delta=4*alpha*eta/(1+alpha*eta)^2>0,
inner(D0u,u)>=delta||u||^2 and IsUnit D0 on exactly H0.
Rank zero is explicitly extended, L2 may be infinite dimensional, and
alpha*eta=1 is included. Production imports no Tests or copied Poincare proof.

Root focused3911, independent complete mathematics, source/identity-blind
reconstruction, primary-first anti-anchored seven-slot source review and ten
current formula-proof steps pass. Two exact definitionally equal syntax
successors preserve all hypotheses; original negatives and distinct repair
reviews remain immutable. Exact-science verification is separate from current
serialized Registry501/root Tests, graph/page gates, repository/exposition
seals and postmerge purification. Current source outcome is an attributed
ASTIS squared-defect background completion, not printed B5 block identity
or Gamma/root/main theorem completion.

The next mathematical boundary is actual positive real Gamma/root construction
and its exact centered domain/inverse/polar adapter. IsUnit D0 is only the
centered squared-defect inverse, not Gamma inverse. The previously recorded
real-to-complex-L2/CFC mechanism remains an unvalidated, uncompiled candidate;
no caller CFC, finite-L2, extension or root certificate is allowed. Promote
actual Test-only sharp/inverse consumers into production only through a
reviewed real interface when needed; production may not import Tests.
Full weighted weakH1, PBPS event dynamics/nonexplosion/invariance,
discrete hypocoercivity, mixing, implementation errors and query cost remain
independent. SPHMC smoothing/Picard/Wp/proxy-warmness and actual-input
PBPS/SPHMC composition remain open. Gaussian Cloud and midpoint follow the
active four-paper priority. TV proximity transfers no unbounded expected cost.
This packet completes neither a paper nor the active Goal.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n');p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-centered-squared-defect-2026-10-08';w(p,x)
print('Prepared serialized Registry501/root imports/Tests/handoff; real aggregate gates remain required.')
