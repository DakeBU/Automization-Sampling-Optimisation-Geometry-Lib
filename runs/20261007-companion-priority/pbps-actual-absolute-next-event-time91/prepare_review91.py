from pathlib import Path
import datetime, hashlib, json, subprocess, sys

ROOT=Path('E:/Samplinglib')
RUN=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def fresh(p,x):
    assert not p.exists(),p
    save(p,x)
def pin(p):
    return dict(path=p.relative_to(ROOT).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)

claim=load(RUN/'claim.json')
module=ROOT/claim['proposed_files'][0]
raw=module.read_bytes();s=raw.decode('utf-8')
assert sha(raw)=='8e28fb218233358a9b1c7a2b41689071ca3c410faa58a0883a0885243d588ab2'
seal=load(RUN/'root.statement-seal91.json')
literal=s.split('private def ',1)[1].split('\n\nset_option',1)[0]
assert literal.strip()==seal['expanded_literal_Prop'].strip()
receipt=RUN/'focused/production7-absolute-joint-law/receipt.json'
assert load(receipt)['exit_code']==0 and load(receipt)['module_raw_sha256']==sha(raw)

# Freeze current worktree and Frontier Cells before the read-only remote fetch.
snapshot=RUN/'review-start91'
snapshot.mkdir(exist_ok=False)
for name,args in [('status',['git','status','--porcelain=v1','-uall']),('head',['git','rev-parse','HEAD']),('branch',['git','branch','--show-current'])]:
    q=subprocess.run(args,cwd=ROOT,capture_output=True,check=True)
    (snapshot/(name+'.log')).write_bytes(q.stdout)
cells=sorted((ROOT/'research-wiki/frontier-cells').glob('*.json'))
fresh(snapshot/'frontier-RAW.json',[pin(p) for p in cells])
changed=subprocess.run(['git','diff','--name-only'],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
fresh(snapshot/'tracked-RAW.json',[pin(ROOT/f) for f in changed])
q=subprocess.run(['git','fetch','origin'],cwd=ROOT,capture_output=True)
(snapshot/'fetch.stdout.log').write_bytes(q.stdout);(snapshot/'fetch.stderr.log').write_bytes(q.stderr)
fresh(snapshot/'fetch.receipt.json',dict(exit_code=q.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch_updated=False))
assert q.returncode==0
for p in load(snapshot/'tracked-RAW.json'):
    assert sha((ROOT/p['path']).read_bytes())==p['raw_sha256']

# Record actual third dependency; leave original claim and sealed source graph immutable.
cp=ROOT/'research-wiki/frontier-cells'/f"{claim['frontier_cell']}.json"
(RUN/'frontier-before-actual-dependencies91.exactraw.snapshot.json').write_bytes(cp.read_bytes())
c=load(cp)
dep='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
for xs in [c['parents'],c['reuse_plan']['reused_declarations'],c['proof_digestion']['existing_substrate']]:
    if dep not in xs:xs.append(dep)
reason='Reuse actual90 full-history law and actual89 Borel density/fiber mass. Reuse canonical UnitExponentialProduct first component solely for input probability normalization. Coordinate transport is proved fiberwise with measurePreserving_add_left.lintegral_comp and Tonelli; no separate skew-product certificate is claimed.'
c['reuse_plan']['decision_reason']=reason
c['shared_floor_audit']['reason']=reason
c['purification']['canonicalization']=reason
save(cp,c)
fresh(RUN/'actual-dependencies91.json',dict(module=pin(module),parents=c['parents'],reason=reason,source_graph_unchanged=True,statement_seal_unchanged=True,status='IMPLEMENTATION_DEPENDENCIES_PENDING_INDEPENDENT_KERNEL_REVIEW'))

old=load(ROOT/'runs/20261007-companion-priority/pbps-actual-finite-history-extension90/anonymous.lean-context90.json')
statement=literal.removeprefix('actual_absolute_next_event_time_statement').replace(' : Prop :=',' :',1)
lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=old['decoder_context'])
candidate=ROOT/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-source-first91/candidate91.source-proposal.v2.native.json'
draft=dict(id='ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime',state='draft',
    source=dict(source_id='companion-domain:pbps-actual-absolute-next-event-time',anchor=claim['source_anchor'],original_text=candidate.read_text(encoding='utf-8')),
    lean=dict(**lean,declaration=claim['target_declarations'][0],file=claim['proposed_files'][0]),repairs=[])
fresh(RUN/'decoder-draft91.json',draft)
packet=rt.decoder_packet(draft)
out=ROOT/'runs/semantic-roundtrip/anonymous91'
out.mkdir(exist_ok=False)
fresh(out/'input.json',packet)
fresh(RUN/'decoder-freeze91.json',dict(module=pin(module),seal=pin(RUN/'root.statement-seal91.json'),compile=pin(receipt),packet=pin(out/'input.json'),canonical_packet_sha256=packet.get('packet_sha256'),source_visible=False,publication_binding_pending=True))
print('Frozen source-blind packet:',out/'input.json')
print('Statement SHA256:',lean['statement_sha256'])
print('Original source graph/seal and production unchanged; actual dependency recorded; fetch preserved tracked files.')
