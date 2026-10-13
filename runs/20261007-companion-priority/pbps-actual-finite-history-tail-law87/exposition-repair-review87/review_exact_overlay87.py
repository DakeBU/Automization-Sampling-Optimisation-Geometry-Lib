"""Independent, read-only assessment of the exact three-field exposition overlay."""
from __future__ import annotations
import copy
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87'
AUTHOR=BASE/'independent-math87'
OUT=BASE/'exposition-repair-review87'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def descriptor(p,kind):
    raw=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(raw),'bytes':len(raw),'kind':kind}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,value):
    p=OUT/name
    assert not p.exists(),'Do not replace immutable review output'
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return descriptor(p,'native-independent-review-output')

proposal_path=AUTHOR/'proposed-exposition-overlay87.json'
closed_path=AUTHOR/'exposition-overlay87.closed-RAW-manifest.json'
assert sha(proposal_path.read_bytes())=='750c744f686b6db7938cd54cdbabe680027028b1a22fdf5102ec143121e865a3'
assert sha(closed_path.read_bytes())=='168c99885e0ce5e3b20e6633bd75ee2091b2d5635377b9c30c3a0086f8b281b2'
proposal=load(proposal_path);closed=load(closed_path)
inputs=[descriptor(proposal_path,'exact-proposal'),descriptor(closed_path,'exact-proposer-closed-manifest')]
def verify(d,kind):
    p=ROOT/d['path'];v=descriptor(p,kind)
    assert v['raw_sha256']==d['raw_sha256'] and v['bytes']==d['bytes'],d['path']
    if not any(z['path']==v['path'] for z in inputs):inputs.append(v)
    return p
for d in closed['original_inputs']:verify(d,'exact-original-snapshot-or-index')
for pair in closed['exact_proposed_successors']:
    verify(pair['original'],'unchanged-production-exposition')
    verify(pair['proposed'],'exact-proposed-successor')
module_path=verify(proposal['module'],'unchanged-production-Lean')
verify(proposal['original_freeze'],'original-publication-freeze')
verify(proposal['original_snapshot_index'],'original-snapshot-index')
assert proposal['required_changes']==3 and len(proposal['changes'])==3
assert proposal['proposer_id']=='/root/exact_verify77'

def at(doc,pointer):
    value=doc
    for key in pointer.strip('/').split('/'):
        value=value[int(key)] if isinstance(value,list) else value[key]
    return value
def set_at(doc,pointer,value):
    keys=pointer.strip('/').split('/');parent=doc
    for key in keys[:-1]:parent=parent[int(key)] if isinstance(parent,list) else parent[key]
    key=keys[-1];parent[int(key) if isinstance(parent,list) else key]=value
def delta(a,b,path=''):
    if type(a)!=type(b):return [path]
    if isinstance(a,dict):
        assert set(a)==set(b)
        return sum((delta(a[k],b[k],path+'/'+k) for k in a),[])
    if isinstance(a,list):
        assert len(a)==len(b)
        return sum((delta(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
    return [] if a==b else [path]

snapshot_index=load(AUTHOR/'original-exposition-snapshot-index87.json')
snapshots={p['original']['path']:ROOT/p['immutable_snapshot']['path'] for p in snapshot_index['snapshots']}
bindings=[];documents={}
for pair in closed['exact_proposed_successors']:
    target=pair['original']['path'];old_path=snapshots[target];new_path=ROOT/pair['proposed']['path']
    before=load(old_path);after=load(new_path);expected=copy.deepcopy(before);raw=old_path.read_bytes()
    assert (ROOT/target).read_bytes()==raw
    changes=[c for c in proposal['changes'] if c['target']['path']==target]
    for c in changes:
        assert at(before,c['pointer'])==c['before'] and at(after,c['pointer'])==c['after']
        set_at(expected,c['pointer'],c['after'])
        encoded_before=json.dumps(c['before'],ensure_ascii=False).encode('utf-8')
        encoded_after=json.dumps(c['after'],ensure_ascii=False).encode('utf-8')
        assert raw.count(encoded_before)==1
        raw=raw.replace(encoded_before,encoded_after)
    actual=delta(before,after)
    assert expected==after and sorted(actual)==sorted(c['pointer'] for c in changes)
    assert raw==new_path.read_bytes(),'No unlisted formatting/raw-byte rewrite permitted'
    bindings.append({'production_path':target,'before':descriptor(old_path,'immutable-exact-before'),'after':descriptor(new_path,'exact-proposed-after'),'changed_fields':changes,'structural_delta':actual,'exact_raw_substitution_only':True})
    documents[target]=(before,after)

lesson_key='website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json'
old_lesson,new_lesson=documents[lesson_key]
unit=new_lesson['units'][0];old_unit=old_lesson['units'][0]
assert len(unit['steps'])==6
module_raw=module_path.read_bytes();lines=module_raw.decode('utf-8').splitlines(keepends=True)
regions=[]
for number,(old_step,step) in enumerate(zip(old_unit['steps'],unit['steps']),1):
    r=step['lean_source_region'];code=step['lean']
    assert r==old_step['lean_source_region'] and code==old_step['lean']
    assert r['source_raw_sha256']==sha(module_raw)
    assert r['path']==proposal['module']['path']
    assert ''.join(lines[r['start_line']-1:r['end_line']])==code
    assert sha(code.encode('utf-8'))==r['exact_code_raw_sha256']
    regions.append({'step':number,**r,'unchanged_exact_adjacent_region':True})
step2,step3,step4=unit['steps'][1:4]
assert all(name in step2['lean'] for name in ['have hcausal','have hprefix','have hHmeas : Measurable','have hTmeas : Measurable'])
assert 'Measurable[past n]' not in step2['lean']
assert 'have htruncated : Measurable[past n]' in step3['lean']
assert 'have hHp : Measurable[past n]' in step4['lean'] and 'hcausal (truncated w)' in step4['lean']
assert '\\mathcal F_n' not in step2['formula'] and '\\mathcal F_n' in step4['formula']
assert all(len(m.group())==1 for m in re.finditer(r'\\+',step2['formula']))

producer=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
producer_text=producer.read_text(encoding='utf-8')
assert 'Prospective header76' in producer_text
assert 'theorem actual_fixed_reference_finite_jump_recursion' in producer_text
assert 'ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion' in module_raw.decode()
inputs.append(descriptor(producer,'producer-identity-source'))
producer_metadata={}
for name,num in [('pbps-actual-finite-jump-recursion',76),('pbps-actual-event-time-nonaccumulation',78)]:
    path=ROOT/f'website/content/publications/{name}.json'
    # Only title and statement-seal location are evidence; no reviewer verdict is consumed.
    item=load(path)['items'][0]
    seal=item['statement_seal']['evidence']
    assert str(num) in seal
    producer_metadata[name]={'title':item['title'],'statement_seal_location_only':seal,'used_for':'producer identity only; no theorem-verdict adoption'}
    inputs.append(descriptor(path,'selected-title-and-seal-location-only'))

checks={
 'step2':'Exact lines148–171 derive deterministic finite-prefix causality and ambient Borel measurability of H_n and Y_n. Proposed formula states exactly these facts, including all real input sequences; no provider premise, probability-one restriction, conditional law or restart assumption is introduced.',
 'step4':'Past-sigma F_n history measurability remains in unchanged step4 lines187–200, after step3 derives F_n measurability of the clipped/truncated stream. Causality identifies that proof factorization with the original actual history. This preserves the stronger theorem conclusion and repairs only its premature step2 placement.',
 'producer_identity':'Current01fc module consumes ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion. Producer source labels header76 and its publication seal location identifies recursive-preproof76; actual78 metadata identifies event-time nonaccumulation. Both78→76 edits correct prose attribution without changing dependency edges or proof credit.',
 'unchanged_semantics':'Full private Prop, public binders, literal flow/rate/hazard/stopped recursion, six standing hypotheses, definitions and conclusion are unchanged because whole production Lean RAW remains01fc. Lesson statement/assumptions/source attribution/boundary, publication source body/obligations/topology/status and all six exact proof regions remain byte/value unchanged outside the three enumerated strings.',
 'scope':'Independent exact exposition proposal review only. No author verdict inherited, canonical write, self-repair, Lean build claim, mathematical/full-source admission, graph promotion, decoder-content read or VERIFIED transition.'
}
chronology=put('exposition-repair-review87.chronology.json',{
 'reviewer':'/root/fresh_source86','proposal_creator':'/root/exact_verify77','scope':'Exact three-field exposition repair; no full theorem re-review',
 'sequence':['Read pinned proposal and closed manifest first.','Read exact original/proposed snapshots and current01fc Lean; examined step2/3/4 matching regions.','Independently checked ambient versus past-sigma distinctions, six exact source regions and decoded TeX command slash lengths.','Checked actual76 imported producer identity against source declaration/header and selected publication title/seal-location;78 selected metadata identifies nonaccumulation.','Compared entire JSON trees and exact RAW substitutions: precisely three fields, no serialization or other byte changes.','Rehashed every exact input and preserved canonical before bytes; emitted new immutable independent native outputs.'],
 'diagnostics':[{'kind':'bounded-search-diagnostic','detail':'Initial broad producer-number rg matched many irrelevant metadata lines and was truncated; one guessed nonaccumulation filename did not exist. Focused source/header and selected title/seal-location checks resolved identity; no foreign reviewer decision or status was used.'}],
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
run=put('exposition-repair-review87.run.json',{
 'schema':'astis.independent.exact-exposition-repair-review-run87.v1','reviewer':'/root/fresh_source86',
 'proposal_raw_sha256':sha(proposal_path.read_bytes()),'proposer_manifest_raw_sha256':sha(closed_path.read_bytes()),
 'inputs':inputs,'before_after_bindings':bindings,'proof_regions':regions,'producer_identity_evidence':producer_metadata,
 'chronology':chronology,'checks':checks,'canonical_mutations':False,
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
decision=put('exposition-repair-review87.decision.json',{
 'schema':'astis.independent.exact-exposition-repair-decision87.v1',
 'reviewer':'/root/fresh_source86','proposal_creator':'/root/exact_verify77','independent_from_author_and_stabilizer':True,
 'verdict':'ACCEPTED_EXACT_THREE_FIELD_EXPOSITION_REPAIR','decision':'accepted',
 'reason':'The exact successor formula matches its ambient-measurability/causality region, leaves F_n history measurability in step4, and corrects two producer identities78→76. No premise, proposition, Lean code, proof-region binding, source text, boundary, dependency or completion status changes.',
 'proposal':descriptor(proposal_path,'accepted-exact-proposal'),'proposal_sha256':sha(proposal_path.read_bytes()),
 'proposer_closed_manifest':descriptor(closed_path,'exact-proposer-closed-manifest'),
 'full_module_sha256':sha(module_raw),'review_run_sha256':run['raw_sha256'],
 'changed_field_count':3,'before_after_bindings':bindings,'checks':checks,'blocking_deltas':[],
 'authorized_application':'Root sole stabilization writer may apply only exact lesson successor e6ba0183... and publication successor a8088607... bound in this decision; reviewer applied nothing.',
 'boundary':'Proposal-only exposition acceptance, not a new mathematical/full-source verification or theorem VERIFIED transition.',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
outputs=[descriptor(p,'native-independent-review-output') for p in sorted(OUT.iterdir()) if p.is_file()]
manifest=put('exposition-repair-review87.closed-RAW-manifest.json',{
 'schema':'astis.independent.closed-raw-manifest87.v1','hash_algorithm':'SHA256','hash_mode':'RAW exact bytes',
 'inputs':inputs,'outputs':outputs,'closed':True,'decision_sha256':decision['raw_sha256'],'review_run_sha256':run['raw_sha256'],
 'closure':'Every created file listed, except this manifest itself to avoid recursive hashing; manifest RAW hash reported externally.',
 'source_extracts':[],'private_exclusion_list':[],'canonical_mutations':False
})
for d in inputs+outputs:
    raw=(ROOT/d['path']).read_bytes()
    assert sha(raw)==d['raw_sha256'] and len(raw)==d['bytes']
print(json.dumps({'decision':decision,'run':run,'manifest':manifest,'chronology':chronology},indent=2))
