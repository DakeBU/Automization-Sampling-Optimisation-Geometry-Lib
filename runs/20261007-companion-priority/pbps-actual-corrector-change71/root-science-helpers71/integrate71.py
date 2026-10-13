from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-actual-corrector-change71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification71.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration71';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]
rows=[]
for name in owned:
 b=(root/name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=p.relative_to(root).as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
entry=dict(key='pbps.actualCorrectorChange',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual PBPS exact corrector change under the reflected step',source='arXiv2609.06905v1 Appendix B3 B20/B21; Lemma B4/B28 ingredient',tags=['PBPS','L2','reflection','conditional-expectation','corrector'],note='Independently exact-science71 VERIFIED '+head+'. Same six original analytic callers and twelve witnesses, actual g=U(P-Pperp)f and its actual conditional gP/polar gV satisfy C(gP,gV)-C(fP,fV)=-norm(fP)^2+norm(fV)^2, with C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v). Exact half, signs and same inverse. No extra smoothness/domain, onto-V0, mean premise or sharp-energy68 dependency. Rank0/alphaeta1 remain legal. B4/B27/B28 actual-update perturbation, H1/B2 dynamics, invariance/nonexplosion, mains, implementation errors/caps, actual-input expected-query costs/composition and full Exposition/PURIFIED remain open.')
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := '+json.dumps(entry['source']),'    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(entry['note'])])+'\n  },\n'
p=root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=b'def measureMemory : List LemmaMemoryEntry := ['+nl
assert b.count(a)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(a,a+block.encode().replace(b'\n',nl),1))
with (root/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as stream:stream.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file=entry['source'],verified_commit=head,evidence=(r/'verified.json').relative_to(root).as_posix(),next_action=entry['note']),ensure_ascii=False)+'\n').encode())
p=root/'AutoSamplingTheory/ExampleCases.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange'+nl
assert b.count(a)==1 and addition not in b;p.write_bytes(b.replace(a,a+addition,1))
p=root/'Tests/Basic.lean';b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 518')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 518',b'formalizedTechnicalLemmaCount = 519'))
for cid in plan['active_cells']:
 p=root/'research-wiki/frontier-cells'/(cid+'.json');cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence']['independent_verification']=(r/'verified.json').relative_to(root).as_posix();cell['evidence']['execution_boundary']=entry['note'];cell['source_detail_audit']['gap']='Actual discrete corrector change B21 independently verified. Actual B4 perturbation/B27/B28,H1/B2,dynamics/main/errors/cost/composition remain open.';write(p,cell)
p=root/'docs/companion-papers-handoff.md';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Actual PBPS corrector change (2026-10-10)

Independently VERIFIED science commit {head}. For SAME actual original globally
centered f and actual g=U(P-Pperp)f, its actual conditional gP and polar gV obey
C(gP,gV)-C(fP,fV)=-norm(fP)^2+norm(fV)^2, where
C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v).
The half, signs and SAME inverse are exact. Six original analytic callers,
twelve common witnesses and every parent70 clause persist. Rank0 and
alphaeta=1 remain legal; no onto, extra regularity, mean or sharp-bound premise.
The whole528-line module, full private literal and eight exact formula/BODY
steps have independent math, blind reconstruction and primary-first source review.

This closes the actual discrete B21 ingredient only. Next is B4's exact
corrector perturbation and its actual-update component/B27 interface, followed
by the half-turn estimate and full one-step dynamics. H1/B2, invariance/nonexplosion,
PBPS/SPHMC mains, errors/caps and actual-input expected-query costs/composition
remain independent. TV proximity does not transfer unbounded costs. Four-paper
priority, Chewi and older frontiers/cycles/memory persist. Full Exposition/PURIFIED,
main/live and whole-paper/Goal completion remain unearned.

Serialized Registry519/imports/Tests and current reader/graph gates are pending
against final admin state. Exact science verification is separate from aggregate,
reader and remote CI admission. Previous INT70 site and contributor CI passed;
its formalization CI status is recorded separately without extrapolation.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=root/'website/content/samplewiki_companion_frontiers.json';frontiers=load(p);frontiers['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-corrector-change-2026-10-10';write(p,frontiers)
print('Prepared serialized71 Registry519/imports/handoff only after exact independent SCI71 verification; aggregate/reader/graph pending.')
