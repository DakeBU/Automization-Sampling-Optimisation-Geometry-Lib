from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,'tools');import astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def checkrow(p,x):
 b=p.read_bytes();assert len(b)==x.get('raw_bytes',x.get('RAW_bytes')) and sha(b)==x.get('raw_sha256',x.get('RAW_sha256'))
 assert sha(b.replace(b'\r\n',b'\n'))==x.get('lf_sha256',x.get('LF_sha256'))
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(root).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
m=r/'independent-header-math68';s=r/'independent-header-source68';ml=load(m/'lease.final.json');sl=load(s/'lease.final.json');mr=load(m/'run.json');sr=load(s/'review-run.json')
assert sha((m/'lease.final.json').read_bytes())=='71cc0fecc36ddbbe0bdd25e7c778cca3a899578c484c606de8da5df0813c3c99'
assert sha((s/'lease.final.json').read_bytes())=='70c9407a26ac73e9c1d90d6b68032b63e73d516317dd7dc0fb9ccf4db570662f'
assert ml['status']==sl['status']=='CLOSED_LAST' and ml['final_owned_write'] and sl['last_owned_write']
for d,lease,run,expected,count in [(m,ml,mr,'6938a3acb8fd912084aa34fef8491290daac94a452d24ef311137f7d352f01b6',130),(s,sl,sr,'5eac88f7131b87cf25a1b9ab5f3fdc7d8c6d28a19c65f68b583d6f3219dc082d',91)]:
 assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']==expected
 files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()};assert len(files)==count
 assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
 if d==m:
  rows=lease['all_owned_except_final_lease'];names={Path(x['path']).relative_to(d).as_posix() for x in rows};assert set(files)==names|{'lease.final.json'}
  for x in rows:checkrow(Path(x['path']),x)
 else:
  manifest=load(s/'owned-manifest.json');assert sha((s/'owned-manifest.json').read_bytes())==lease['owned_manifest_RAW_sha256']=='f888974cb765e50fe1492e7001e449a4cf7bd8f45718a0e8f03f493915aea397'
  assert set(files)=={x['name'] for x in manifest['entries']}|{'owned-manifest.json','lease.final.json'}
  for x in manifest['entries']:checkrow(s/x['name'],x)
assert sha((m/'complete.named-review.RAW.json').read_bytes())=='6f154551e9d8efb97d3a92bf250a3f76f83d647c0eb9d0f93cb667b81b502c87'
assert sha((s/'complete-RAW-verdict.json').read_bytes())=='0b0c2d3ee8c7b542c7e08e81c95f582a13f312b6cbbcabed7355b0297ca737c3'
assert sha((s/'review-run.json').read_bytes())=='68895920e34e7abdaacc291b460f81f252ac8ae059d6c79a004b42eb23e755b7'
md=load(m/'header-mathematical-review.json');sd=load(s/'complete-RAW-verdict.json')
assert md['status']=='ACCEPTED_REPAIRED_HEADER_DRAFTS_MATHEMATICALLY_FEASIBLE' and not md['blockers'] and not md['proposed_mathematical_repairs']
assert sd['status']=='HEADER68_SOURCE_BINDER_LITERAL_DEFINITION_AND_GENUINE_ENERGY_CONSUMER_ACCEPTED_NOT_PROVED'
assert sd['source_first'] and sd['parser_alpha_renaming_accepted'] and sd['source_mathematical_repair'] is False and not sd['blocking_source_deltas']
for key in ['semantic_slots_generic','semantic_slots_actual_header1','semantic_slots_actual_header2']:assert set(sd[key])==set(rt.SEMANTIC_SLOTS)
for x in load(s/'header-inputs.manifest.json')['entries']:
 p=root/x['path'];checkrow(p,x);assert p.read_bytes()==(s/x['raw_snapshot']).read_bytes()
headers=[]
for i in range(3):
 p=r/f'header{i}-expanded.lean';q=r/f'statement{i}.definition.lean';row=dict(header=pin(p))
 if i:row['literal_definition']=pin(q)
 headers.append(row)
adoption=dict(status='THREE_REPAIRED_HEADER68_DRAFTS_ACCEPTED_NO_PROOF',actual_root_read_only_pid=os.getpid(),math_owned_files=130,source_owned_files=91,math_whole_logical_run_sha256=mr['run_sha256'],source_whole_logical_run_sha256=sr['run_sha256'],native_math_lease=pin(m/'lease.final.json'),native_source_lease=pin(s/'lease.final.json'),exact_current_headers=headers,alpha_renaming_map='alpha-renaming-weight68/applied.json',extra_statement2_terminal_empty_line_transparently_accepted=True,source_graph_reused='runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/independent-primary67/source-proof-graph.json',source_math_items=344,source_mathematical_repair=False,proof_search=False,SAU_claim=False,VERIFIED=False)
write(r/'root.header68.adoption.json',adoption)
write(r/'root.statement-seal68.json',dict(status='STATEMENT68_SEALED_NOT_CLAIMED_NOT_PROVED',actual_root_pid=os.getpid(),headers=headers,independent_header_adoption='root.header68.adoption.json',source_graph=adoption['source_graph_reused'],source_raw_sha256=sd['source_raw_sha256'],source_anchor='PBPS2609.06905v1 AppendixB3 B19/B20/B22/B23/B24 and LemmaB3',extra_paper_premises=[],original_actual_callers_unchanged=True,rank_zero_alpha_eta_one_retained=True,exact_alpha_renaming='alpha-renaming-weight68/applied.json',truth_boundary='Sharp corrector pair/global energy and LemmaB3 equivalence are targets, not yet proved. B21 rotation/B2/H1/B4/dynamics/main/errors/cost/composition remain separate.',proof_search=False,SAU_claim=False))
print('PASS header68 math130/source91 closed-native validation;3 exact revised statements sealed; no claim or proof credit.')
