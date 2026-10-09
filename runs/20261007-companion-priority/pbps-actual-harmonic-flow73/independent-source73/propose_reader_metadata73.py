from pathlib import Path
import copy, hashlib, json, os, sys
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=BASE/'independent-source73';OUT=OWN/'reader-metadata-overlay73'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF byte pairs -> LF only'}
def write(n,x):(OUT/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not(OWN/'lease.final.json').exists();OUT.mkdir(exist_ok=False)
old='Pending implementation; one actual deterministic theorem.'
new='One public deterministic theorem uses the complete private literal proposition definition; the literal is a specification, not a mathematical provider. The six original callers are retained. No retired candidate declaration occurs in this178-line module. This scoped audit grants neither an Exposition Seal nor PURIFIED admission.'
paths=[ROOT/'website/content/publications/pbps-actual-harmonic-flow.json',ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json']
pointers=['/items/0/purification/dead_code_audit','/purification/dead_code_audit'];rows=[]
for i,p in enumerate(paths):
 before=p.read_bytes();assert before.count(old.encode())==1
 after=before.replace(old.encode(),new.encode());jb=json.loads(before);ja=json.loads(after)
 if i==0:assert jb['items'][0]['purification']['dead_code_audit']==old;ja['items'][0]['purification']['dead_code_audit']=old
 else:assert jb['purification']['dead_code_audit']==old;ja['purification']['dead_code_audit']=old
 assert ja==jb
 (OUT/f'{i}.before.exactraw.json').write_bytes(before);(OUT/f'{i}.proposed.exactraw.json').write_bytes(after)
 rows.append({'canonical_path':p.relative_to(ROOT).as_posix(),'JSON_pointer':pointers[i],'old_value':old,'proposed_value':new,'before':pin(OUT/f'{i}.before.exactraw.json'),'proposed':pin(OUT/f'{i}.proposed.exactraw.json')})
pub=json.loads((OUT/'0.before.exactraw.json').read_bytes())['items'][0];propub=json.loads((OUT/'0.proposed.exactraw.json').read_bytes())['items'][0]
payload_fields=['source','statement','formulae','assumptions','obligations','bindings'];assert {k:pub[k] for k in payload_fields}=={k:propub[k] for k in payload_fields}
packet=json.loads((BASE/'source-review.packet.json').read_bytes())
proposal={'schema':'astis-independent-reader-process-metadata-proposal73/v1','status':'PROPOSED_AWAITING_DISTINCT_REPAIR_REVIEW','author':'/root/independent_primary69','actual_proposal_PID':os.getpid(),'exact_field_count':2,'exact_file_count':2,'changes':rows,'mathematical_reason_for_change':False,'reason':'The exact current proof exists; pending implementation is stale reader/process wording. This changes no mathematical statement, assumption, formula, BODY, source graph or blind reconstruction.','publication_binding_sha256_unchanged':packet['publication_binding_sha256'],'review_context_canonical_sha256_unchanged':sha(canon(packet['candidate_publication_context'])),'binding_context_invariance_basis':'tools/astis_publication.py lines82-117 exclude top-level publication purification and frontier cell metadata from binding_payload/review_context; all included fields remain exact equal.','canonical_or_old_CLOSED_written':False,'author_self_approval':False,'proof_source_VERIFIED_credit':False}
write('proposal.json',proposal);write('proposal.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False})
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'proposal':pin(OUT/'proposal.json'),'proposed_RAW_pins':[r['proposed'] for r in rows]},indent=2))
