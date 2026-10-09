from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path('tools').resolve()));import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-macro-root63');n=Path('.astis/decoder-63');d=n/'independent'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.resolve().as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
run,receipt,lease,parent,payload=[load(p) for p in [d/'native.run.json',d/'native.receipt.json',d/'lease.json',n/'lease.json',d/'decoded.payload.json']]
assert lease['status']=='CLOSED_LAST' and parent['status']=='CLOSED' and lease['allowed_inputs']==['packet0.json']
assert (d/'lease.json').read_bytes()==(d/'proposed-lease.closed.json').read_bytes()
assert sha((d/'lease.json').read_bytes())==parent['independent_native_lease_raw_sha256']=='78588443e347f29f3f744588cba832c8214b62ae452ad14d23625959d24124b2'
assert sha((d/'native.receipt.json').read_bytes())==parent['independent_native_receipt_raw_sha256']=='c8645fe07460fa348d491afa20a8eb7776d9a9d8569f0daba86272e11d05d6c1'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==receipt['whole_logical_run_sha256']==lease['whole_logical_run_sha256']==parent['whole_logical_run_sha256']=='3b1928ff12fd5ab82215efd237c8144b032e46dcf07b4fe35cf8b002cdf0ecce'
assert sha((d/'decoded.payload.json').read_bytes())==receipt['decoded_payload_raw_sha256']==lease['decoded_payload_raw_sha256']==parent['decoded_payload_raw_sha256']=='78d9c4093240fd7dc550f8bb262da49d751b5f3fc31999e07187147850099710'
assert (d/'decoded.txt').read_bytes()==payload['reconstructed_theorem_text'].encode() and sha((d/'decoded.txt').read_bytes())==payload['reconstructed_text_sha256']==run['reconstructed_text_sha256']
assert set(payload['slots'])=={'hypotheses','definitions','domains','quantifiers','scopes','conclusions','invariants'} and all(payload['slots'].values()) and not payload['unresolved_syntax']
assert payload['source_fidelity_verdict'] is None and payload['mathematical_proof_correctness_judgement'] is None
for x in [run,receipt,lease,parent,payload]:
 assert not any(x[k] for k in ['source_text_visible','source_identity_visible','compiler_started'])
for x in [run['owned_artifacts_before_finalization'],receipt['owned_artifacts'],load(d/'closure.bindings.json')['owned_artifacts'],lease['owned_artifacts']]:
 for name,digest in x.items():assert sha((d/name).read_bytes())==digest,name
assert {p.name for p in d.iterdir() if p.is_file()}==set(lease['owned_artifacts'])|{'lease.json','proposed-lease.closed.json'}
assert len(list(d.iterdir()))==24
term=lease['terminal_readback'];assert term['observed_finalizer_exit_code']==0 and term['all_receipt_bindings_passed'] and parent['candidate_check_observed_exit_code']==0
initial=(n/'initial-lease.raw.snapshot.json').read_bytes();assert initial==(d/'parent-lease.open.raw.json').read_bytes() and sha(initial)==parent['historical_open_raw_sha256']==lease['parent_lease_open_raw_sha256']
packet=load(n/'packet0.json');assert packet==load(r/'anonymous.0.decoder.json') and (n/'packet0.json').read_bytes()==(d/'packet0.raw.json').read_bytes()
assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==run['input_digests']['packet_declared_sha256']
assert sha(packet['lean']['statement'].encode())==payload['statement_sha256']==packet['lean']['statement_sha256'] and (d/'statement.raw.txt').read_bytes()==packet['lean']['statement'].encode()
context=json.dumps(packet['lean']['approved_definition_context'],ensure_ascii=False,separators=(',',':')).encode()
assert context==(d/'approved-context.canonical.json').read_bytes() and sha(context)==payload['context_sha256']
assert payload['context_declared_sha256'] is None and run['input_digests']['context_declared_sha256'] is None
aid='ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot';slug='pbps-unique-positive-macroscopic-defect-root';ap=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=load(ap)
assert a['state']=='draft' and rt.decoder_packet(a)==packet
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']
dest=r/'anonymous-decoder';dest.mkdir(exist_ok=False);mappings=[]
for p in [*sorted(d.iterdir()),n/'packet0.json',n/'lease.json',n/'initial-lease.raw.snapshot.json']:
 if p.is_file():
  t=dest/('parent-lease.closed.json' if p==n/'lease.json' else p.name);assert not t.exists();t.write_bytes(p.read_bytes());mappings.append(dict(original=pin(p),exact_raw_snapshot=pin(t)))
adapter=dest/'decoded0.root-adapter.json';w(adapter,dict(native_payload=pin(dest/'decoded.payload.json'),native_complete_payload=payload,decoder_run_sha256=run['run_sha256'],named_payload_sha256=receipt['decoded_payload_raw_sha256'],reconstructed_text_sha256=payload['reconstructed_text_sha256'],native_bytes_unchanged=True,context_declared_sha256=None))
w(r/'root.decoder63.adoption.json',dict(status='ACTUAL_CLOSED_FRESH_ANONYMOUS_DECODER63_ADOPTED',actual_adopter_pid=os.getpid(),native_run_sha256=run['run_sha256'],native_named_RAW_payload_sha256=receipt['decoded_payload_raw_sha256'],whole_run_hash_recipe=run['logical_run_hash_encoding'],payload_hash_recipe='SHA256 of complete exact RAW decoded.payload.json bytes',raw_snapshot_mappings=mappings,native_owned_files=24,source_text_visible=False,source_identity_visible=False,context_declared_sha256=None,native_receipt=pin(dest/'native.receipt.json'),CLOSED_LAST=pin(dest/'lease.json')))
(r/'audit.0.before-decoder.raw.snapshot.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=payload['reconstructed_theorem_text'],text_sha256=payload['reconstructed_text_sha256'],decoder='/root/anonymous_decoder63',decoder_run_sha256=run['run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/'packet0.json')],run_artifact=adapter.as_posix(),run_binding=(dest/'native.receipt.json').as_posix(),native_named_payload_sha256=receipt['decoded_payload_raw_sha256'],run_hash_recipe=run['logical_run_hash_encoding']))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');w(r/'source.0.reviewer-packet.before-presentation-fix.json',rt.semantic_reviewer_packet(a))
print('PASS fresh anonymous63 CLOSED_LAST adopted; 24 native files plus initial/closed parent bytes; complete seven slots unchanged. No source verdict.')
