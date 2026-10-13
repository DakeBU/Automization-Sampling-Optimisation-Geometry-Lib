from pathlib import Path
import copy,hashlib,json
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
d=r/'presentation-overlay66';d.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
names=['website/content/publications/pbps-ambient-adjoint-corrector.json','website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json',(r/'publication-plan.json').as_posix()]
extra=['AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one','AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral']
entries=[];changes=[]
for i,name in enumerate(names):
    p=Path(name);raw=p.read_bytes();before=json.loads(raw);after=copy.deepcopy(before)
    selected=[]
    if i==0:
        selected=[['items',0,'proof_digestion','existing_substrate']]
    elif i==1:
        selected=[['units',0,'astis_dependencies']]
    elif i==2:
        selected=[['proof_digestion','existing_substrate']]
    else:
        selected=[['actual_ASTIS_parents']]
    for path in selected:
        obj=after
        for k in path[:-1]:obj=obj[k]
        old=copy.deepcopy(obj[path[-1]])
        assert isinstance(old,list) and all(x not in old for x in extra)
        new=old+extra
        obj[path[-1]]=new
        changes.append(dict(file=name,path=path,before=old,after=new))
    snap=d/f'{i}.before.exactraw.snapshot.json';snap.write_bytes(raw)
    proposed=d/f'{i}.proposed.json';write(proposed,after)
    entries.append(dict(canonical=name,before=pin(p),before_snapshot=pin(snap),proposed=pin(proposed),allowed_field_paths=selected))
assert len(changes)==4
formula_paths=[names[0],names[1]]
for name in formula_paths:
    data=json.loads(Path(name).read_bytes())
    formulas=[data['items'][0]['formulae'][0]['tex']] if 'items' in data else [data['units'][0]['formula']]+[s['formula'] for s in data['units'][0]['steps']]
    assert all(chr(92)*2 not in s for s in formulas)
write(d/'proposal.json',dict(status='PROPOSED_METADATA_ONLY_PENDING_INDEPENDENT_REVIEW',entries=entries,changes=changes,compiled_proof_inputs=[pin(Path(x)) for x in ['AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean','Tests/ProximalBPSAmbientAdjointCorrector.lean']],reason='Catalogue two existing ASTIS APIs directly invoked by the already compiled proof. Exact statements,bodies,caller binders,source graph and logical theorem remain unchanged. TeX countercheck confirms decoded strings are already correct single-backslash commands; raw JSON escaping does not justify formula edits.',source_mathematical_repair=False,private_provider_added=False,formula_changes=0,original_exposition_draft_preserved=True,original_math_freeze_preserved=True,canonical_write=False))
print('Proposed exact4 dependency catalogue changes across4 files; formulas/canonical bytes unchanged, independent review required.')
