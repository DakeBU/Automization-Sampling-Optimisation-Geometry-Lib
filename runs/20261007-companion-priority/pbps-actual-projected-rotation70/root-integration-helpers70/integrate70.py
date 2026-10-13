from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-actual-projected-rotation70'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification70.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration70';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]
rows=[]
for name in owned:
 b=(root/name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=p.relative_to(root).as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf-8',newline='\n')
entry=dict(key='pbps.actualProjectedRotation',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual PBPS projected reflection rotation and two-component energy',source='arXiv2609.06905v1 Appendix B1/B3; B21 and Lemma B4 prerequisites',tags=['PBPS','L2','reflection','conditional-expectation','projected-rotation'],note='Independently exact-science70 VERIFIED '+head+'. Same six original analytic callers and twelve witnesses yield actual g=U(P-Pperp)f, internally mean(g)=0, actual conditional gP and polar gV, gP=A0fP-Gamma0fV and gV=Gamma0fP+A0fV, with exact pair-energy conservation. No right-hand-side-defined output, mean premise, extra regularity or sharp-energy68 premise. Rank0/alphaeta1 remain legal. B21 corrector change, B4 dynamics, main, invariance/nonexplosion, errors/caps, expected-query costs/composition and full Exposition/PURIFIED remain open.')
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := '+json.dumps(entry['source']),'    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(entry['note'])])+'\n  },\n'
p=root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=b'def measureMemory : List LemmaMemoryEntry := ['+nl
assert b.count(a)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(a,a+block.encode().replace(b'\n',nl),1))
with (root/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as stream:stream.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file=entry['source'],verified_commit=head,evidence=(r/'verified.json').relative_to(root).as_posix(),next_action=entry['note']),ensure_ascii=False)+'\n').encode())
p=root/'AutoSamplingTheory/ExampleCases.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation'+nl
assert b.count(a)==1 and addition not in b;p.write_bytes(b.replace(a,a+addition,1))
p=root/'Tests/Basic.lean';b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 517')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 517',b'formalizedTechnicalLemmaCount = 518'))
for cid in plan['active_cells']:
 p=root/'research-wiki/frontier-cells'/(cid+'.json');cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence']['independent_verification']=(r/'verified.json').relative_to(root).as_posix();cell['evidence']['execution_boundary']=entry['note'];cell['source_detail_audit']['gap']='Actual projected rotation and pair energy independently verified. B21 corrector change, B4/H1/dynamics/main/errors/cost/composition remain open.';write(p,cell)
p=root/'docs/companion-papers-handoff.md';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Actual PBPS projected rotation (2026-10-10)

Independently VERIFIED science commit {head}. For SAME actual original globally
centered f and actual g=U(P-Pperp)f, mean(g)=0 is proved internally. The actual
conditional gP and polar gV satisfy gP=A0fP-Gamma0fV and gV=Gamma0fP+A0fV,
with exact sum-of-squared-norm preservation. All six original analytic callers
and twelve witnesses persist; rank0 and alphaeta=1 remain legal. There is no
extra mean premise, RHS-defined output or sharp-energy68 proof dependency.
The whole544-line module, expanded private literal Prop, eight exact formula/BODY
steps and seven decoder/source slots have independent math and source review.
The full private Prop is exposed adjacent to the proof as a proposition definition.

This closes actual projected rotation and pair energy only. Next is the actual
B21 corrector change on SAME witnesses, then Lemma B4. B4/H1/B2 dynamics,
invariance/nonexplosion, PBPS/SPHMC mains, implementation errors/caps and actual-input
expected-query costs/composition remain open. TV proximity does not transfer
unbounded expected cost. Four-paper priority and all older frontiers/cycles/memory
persist. Full Exposition/PURIFIED, main/live and whole-paper/Goal completion remain
unearned. INT69 site CI failed its old helper-panel count; the helper-aware gate
repair is a separate reviewed code change with fresh current browser checks due.

Serialized Registry518/imports/Tests and current reader/graph gates are pending
against final admin state; exact science verification is separate from these
aggregate admissions and from remote CI.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=root/'website/content/samplewiki_companion_frontiers.json';frontiers=load(p);frontiers['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-projected-rotation-2026-10-10';write(p,frontiers)
print('Prepared serialized70 Registry518/imports/handoff only after exact independent SCI70 verification; aggregate/reader/graph admission pending.')
