from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81/api-diagnosis81'
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,d):
 p=O/n
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return raw(p)
pos=O/'api-reproducer.inferred.closed-lets.receipt.json';neg=O/'api-reproducer.direct.closed-lets.receipt.json';full=O/'inferred-composition.receipt.json'
assert load(pos)['exit_code']==0 and load(neg)['exit_code']==1
assert 'timeout at `isDefEq`' in (O/'api-reproducer.direct.closed-lets.stdout.log').read_text(encoding='utf-8')
for r in [pos,neg,full]:
 d=load(r);assert d['terminal_closed']
 for e in [d['input'],d['stdout'],d['stderr']]:assert raw(R/e['path'])==e
for e in load(O/'input-freeze81.json')['inputs']:assert raw(R/e['path'])==e
decision=save('diagnosis81.json',{
 'status':'API_BOUNDARY_REPRODUCED_AND_COMPILING_ALTERNATIVE','reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'exact_failed_source_RAW_sha256':'8eb2cfe48244ada2af79740b07430cf72167fe4aaa5cf6c692098e66568c657b',
 'boundary':'Joint actual tau measurability composed with ((y,reference),actual live-projection phase,actual epsilon_n); no source/binder or mathematical definition repair.',
 'cause':'Expected-result-type-directed higher-order composition elaboration at direct exact hτM.comp haM reaches expensive isDefEq/whnf through actual let-defined tau/record expressions. Infer the composition type from its already typed measurable operands before checking the result against the target. This changes elaboration direction only, not the composed map or theorem assumptions. Native contrast confirms this boundary; no claim is made of a kernel soundness or mathematical defect.',
 'minimal_local_change':'have hcomp := hτM.comp haM\nexact hcomp',
 'pinned_comp_API':raw(R/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Defs.lean'),
 'API_signature':'Measurable.comp {g : beta -> gamma} {f : alpha -> beta} (hg : Measurable g) (hf : Measurable f) : Measurable (g compose f)',
 'negative_strict_API_reproducer':raw(O/'api-reproducer.direct.closed-lets.lean'),'negative_terminal_receipt':raw(neg),
 'compiling_strict_API_alternative':raw(O/'api-reproducer.inferred.closed-lets.lean'),'positive_terminal_receipt':raw(pos),
 'reproducer_scope':'Context-preserving strict smaller API theorem with original actual definitions and original parents. Not claimed to be globally shortest source reproducer. Both variants expose initial let binders before forall intro and differ only in inferred-vs-direct composition.',
 'heartbeat_budget':1600000,'heartbeat_escalation':False,
 'full_attempt3_copy_probe':raw(full),
 'full_copy_observation':'The two-line change passes the formerly failing composition and reveals only downstream record-equality measurability, record rewrite expansion and map-congruence namespace errors. Full copy EXIT1 honestly retained; it is not a full-theorem PASS.',
 'retained_extraction_negatives':'The first reduced probes accidentally introduced initial let bindings as y/x/n, causing wrong types; both files/logs/receipts and typed extraction diagnosis remain. The closed-lets probes repair only the diagnostic extraction.',
 'production_shared_edits_by_reviewer':False,'source_statement_repair':False,'proof_review_or_VERIFIED_credit':False
})
files=sorted([p for p in O.iterdir() if p.is_file()],key=lambda p:p.name)
manifest=save('closed-manifest81.json',dict(status='CLOSED_IMPLEMENTATION_API_DIAGNOSIS',reviewer='/root/exact_verify77',decision=decision,all_frozen_inputs_unchanged=True,artifacts=[raw(p) for p in files],manifest_self_hash_omitted=True,production_shared_state_edits=False,VERIFIED=False))
print(json.dumps({'decision':decision,'manifest':manifest,'positive_receipt':raw(pos),'negative_receipt':raw(neg)},ensure_ascii=False))
