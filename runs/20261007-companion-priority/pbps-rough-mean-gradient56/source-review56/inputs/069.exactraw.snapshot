from pathlib import Path
import json,hashlib,copy,datetime
base=Path('runs/20261007-companion-priority'); pre=base/'pbps-rough-mean-gradient-preproof56'; review=base/'pbps-rough-mean-gradient-preproof-review56'; graph=base/'pbps-rough-mean-gradient-sourcegraph56'
j=lambda p:json.loads(Path(p).read_text(encoding='utf8')); sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=Path(p); b=p.read_bytes(); return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
checks=0
def tree(d):
 global checks
 if isinstance(d,dict):
  if {'path','raw_sha256','bytes','crlf_to_lf_sha256'}<=set(d):
   b=Path(d['path']).read_bytes(); assert sha(b)==d['raw_sha256'] and len(b)==d['bytes'] and sha(b.replace(b'\r\n',b'\n'))==d['crlf_to_lf_sha256'],d['path']; checks+=1
  for value in d.values():tree(value)
 elif isinstance(d,list):
  for value in d:tree(value)
q=j(review/'statement.review.json'); nr=j(review/'reviewer.statement.run.json'); lease=j(review/'lease.json')
for filename,expected in [('statement.review.json','aa89c47778a1ff9325af3fe61c406cb7baf398c4d46fd50fd8f68ff42a43bcc9'),('reviewer.statement.run.json','13ad4ff9a8ad2d2dc6dcdf29f625552d2b85323d6827a4d5897505391f591390'),('lease.json','c2770e3482065b6fa05312de77063a470a8dc6da2979e7d6c7e7a63e6659ae29')]:assert sha((review/filename).read_bytes())==expected
for obj in [q,nr,lease]:
 projection=copy.deepcopy(obj); h=projection.pop('content_self_sha256'); assert sha(canon(projection))==h; tree(obj)
assert lease['status']=='CLOSED' and lease['resources']==dict(read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED')
assert q['verdict']=='ACCEPT_SCOPED_STATEMENT_ONLY' and not q['excess_public_premises'] and not q['blocking_deltas'] and not q['minimal_source_repair'] and not q['proof_admission']
assert sha((graph/'primary-before-signature.freeze.json').read_bytes())=='031343dd45d286aef4a97771cb95b8c2a4e48285abd92faca12466d3663cbe88'
gf=j(graph/'primary-before-signature.freeze.json'); closure=j(graph/'first-stage-resource-closure.json')
assert not any(gf['forbidden_material_read'].values()) and closure['artifact_digest_validation']=='PASS' and closure['compiler']=='NOT_STARTED_CLOSED'
for name,row in gf['first_stage_artifacts'].items():
 b=(graph/name).read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['crlf_to_lf_sha256']; checks+=1
signature=(pre/'prospective-statement.txt').read_bytes().replace(b'\r\n',b'\n'); assert len(signature)==1755 and sha(signature)=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
assert j(pre/'statement.typecheck.0.status.json')['exit_code']==0
cl=j(pre/'statement.typecheck.0.compiler.lease.json'); assert cl['status']==cl['compiler']==cl['Python']=='CLOSED' and cl['exit_code']==0
proposal=j(pre/'root.statement-proposal.json')
result=dict(status='STATEMENT_SEALED_INDEPENDENT_SOURCE_PREPROOF_ONLY',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),signatures=[dict(full_declaration=proposal['declaration'],file=proposal['proposed_files'][0],signature_text=signature.decode(),signature_lf_sha256=sha(signature),signature_raw_sha256=sha((pre/'prospective-statement.txt').read_bytes()),LF_bytes=len(signature))],independent_statement_review=pin(review/'statement.review.json'),independent_native_run=pin(review/'reviewer.statement.run.json'),actual_closed_lease=pin(review/'lease.json'),creator_source_first_freeze=pin(graph/'primary-before-signature.freeze.json'),creator_first_stage_closure=pin(graph/'first-stage-resource-closure.json'),actual_pin_checks=checks,source_boundary=proposal['source_boundary'],remaining_boundary=proposal['not_claimed'],source_topology='Creator exhaustive56 binder/provider graph and independent topology admission pending; preceding55 exact verification and serialized cycle pending.',proof_search_started=False,implementation_started=False)
p=pre/'statement-seals.accepted.json'; assert not p.exists(); p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print('56 exact1755 independent StatementSeal/source-first creator freeze adopted;',checks,'native source checks; no topology/claim/proof admission.')
