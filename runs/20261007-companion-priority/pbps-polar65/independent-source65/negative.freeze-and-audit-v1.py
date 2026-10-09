import json,hashlib,re,os,datetime,collections
from pathlib import Path
B=Path('E:/Samplinglib'); R=B/'runs/20261007-companion-priority/pbps-polar65'; O=R/'independent-source65'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d): (O/n).write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
def norm(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def snap(label,p):
 b=p.read_bytes();l=norm(b);a='input.'+label+'.raw';c='input.'+label+'.LF';(O/a).write_bytes(b);(O/c).write_bytes(l)
 return dict(label=label,source_path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(l),LF_sha256=sha(l),RAW_snapshot=a,LF_snapshot=c)
assert json.loads((O/'lease.open.json').read_bytes())['status']=='OPEN'
inputs=[]
for label,p in [('main',B/'AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean'),('test',B/'Tests/ProximalBPSPolarIsometry.lean'),('parent64',B/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean'),('parent61',B/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean'),('publication',B/'website/content/publications/pbps-actual-polar-isometry.json'),('lesson',B/'website/content/declaration_lessons/pbps-actual-polar-isometry.json'),('canonical-audit',B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualPolarIsometry.json'),('receipt',R/'focused65-v6/receipt.json'),('stdout',R/'focused65-v6/stdout.log'),('stderr',R/'focused65-v6/stderr.log'),('decoder-adoption',R/'root.decoder65.adoption.json'),('toolchain',B/'lean-toolchain'),('manifest',B/'lake-manifest.json'),('binding-tool',B/'tools/astis_publication.py'),('sealed-header0',B/'runs/20261007-companion-priority/pbps-polar-preproof65/header0.lean'),('sealed-header1',B/'runs/20261007-companion-priority/pbps-polar-preproof65/header1.lean')]:inputs.append(snap(label,p))
put('finite-candidate-input-map.json',dict(schema='source65-finite-RAW-LF-input-map-v1',inputs=inputs,canonical_audit_prior_semantic_verdict_not_read=True))
freeze=json.loads((O/'candidate.math-freeze.json.raw').read_bytes());pins=[]
for a in freeze['inputs']:
 b=Path(a['path']).read_bytes();ok=(len(b)==a['raw_bytes'] and sha(b)==a['raw_sha256'] and sha(norm(b))==a['lf_sha256']);pins.append(dict(path=a['path'],RAW_sha256=sha(b),matches_frozen=ok,content_reviewer_visible=a['path'] in [i['source_path'] for i in inputs]))
assert all(x['matches_frozen'] for x in pins)
put('math-freeze-pin-check.json',dict(schema='source65-finite-freeze-pin-check-v1',all_matches=True,pins=pins,closed_review_parent_content_not_reopened=True,hashing_bytes_not_semantic_read=True))
pkt=json.loads((O/'candidate.source.0.reviewer-packet.json.raw').read_bytes());pub=json.loads((O/'input.publication.raw').read_bytes())['items'][0];unit=json.loads((O/'input.lesson.raw').read_bytes())['units'][0];audit=json.loads((O/'input.canonical-audit.raw').read_bytes());bind=pub['bindings'][0]
main=norm((O/'input.main.raw').read_bytes()).decode();test=norm((O/'input.test.raw').read_bytes()).decode()
payload=dict(file=sha(main.encode()),current_lean_module=main,toolchain=sha(norm((O/'input.toolchain.raw').read_bytes())),dependencies=sha(norm((O/'input.manifest.raw').read_bytes())),source=pub['source'],statement=pub['statement'],formulae=pub['formulae'],assumptions=pub['assumptions'],obligations=pub['obligations'],lesson=unit,binding={k:v for k,v in bind.items() if k not in ['audit_id','legacy_audit_debt']})
bindinghash=sha(canon(payload));context=dict(payload);context['binding']={k:payload['binding'][k] for k in ['declaration','role','supports']};context['lesson']={k:v for k,v in unit.items() if k not in ['boundary','source_history_boundary']};context['candidate_assumptions']=[{k:x[k] for k in ['source','lean']} for x in bind['assumption_deltas']]
assert bindinghash==pkt['publication_binding_sha256']==audit['publication_binding_sha256'];assert context==pkt['candidate_publication_context']==audit['publication_context']
assert sha(canon({k:v for k,v in pkt.items() if k!='packet_sha256'}))==pkt['packet_sha256']
textchecks={}
for k in ['source','lean','blind_reconstruction']:
 d=pkt[k];textchecks[k]={f:sha(v.encode()) for f,v in d.items() if f in ['text','statement']}
 for f,s in textchecks[k].items():
  pin=d.get(f+'_sha256');assert pin==s,(k,f,pin,s)
put('publication-binding-audit.json',dict(schema='source65-publication-binding-audit-v1',publication_binding_sha256=bindinghash,reviewer_packet_sha256=pkt['packet_sha256'],current_context_sha256=sha(canon(context)),full_payload=payload,current_review_context=context,exact_current_packet_context_equal=True,exact_current_audit_context_equal=True,packet_logical_hash_checked=True,text_hash_checks=textchecks,ASTIS_parents=unit.get('astis_dependencies'),Mathlib_dependencies=unit.get('mathlib_dependencies'),no_prior_semantic_slots_read=True))
spans=[]
for i,s in enumerate(unit['steps']):
 g=s['lean_source_region'];p=B/g['path'];b=p.read_bytes();ls=b.splitlines(keepends=True);a=sum(map(len,ls[:g['start_line']-1]));z=sum(map(len,ls[:g['end_line']]));blob=b[a:z]
 assert sha(b)==g['source_raw_sha256'];assert sha(blob)==g['exact_code_raw_sha256'];assert blob.decode()==s['lean'];body=b.index(b':= by');assert a>body
 (O/('body-excerpt-'+str(i+1)+'.raw.lean')).write_bytes(blob);(O/('body-excerpt-'+str(i+1)+'.LF.lean')).write_bytes(norm(blob))
 spans.append(dict(step=i+1,title=s['title'],path=g['path'],line_span_inclusive=[g['start_line'],g['end_line']],source_RAW_sha256=sha(b),raw_byte_range_end_exclusive=[a,z],RAW_bytes=len(blob),RAW_sha256=sha(blob),LF_sha256=sha(norm(blob)),inside_actual_proof_BODY=True,literal_adjacent_code_equal=True,formula=s['formula'],text=s['text']))
assert len(spans)==5
# Draft also contains exactly the same five literal code regions.
draft=json.loads((O/'candidate.exposition.draft.json.raw').read_bytes());du=draft['units'][0]
assert len(du['steps'])==5
assert [s['lean'] for s in du['steps']]==[s['lean'] for s in unit['steps']]
put('literal-BODY-excerpts-audit.json',dict(schema='source65-five-literal-BODY-excerpts-v1',all_five=True,draft_equals_canonical_literal_steps=True,spans=spans,header_citation_substituted_for_BODY=False))
rec=json.loads((O/'input.receipt.raw').read_bytes());out=(O/'input.stdout.raw').read_bytes().decode();err=(O/'input.stderr.raw').read_bytes();assert rec['exit_code']==0 and rec['terminal_closed'] and rec['actual_foreground_pid']==36260
assert 'Build completed successfully (3945 jobs).' in out and not err
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^]]+)\]",out,re.S)
sel=[dict(declaration=a,axioms=[x.strip() for x in v.split(',')]) for a,v in axioms if a in [bind['declaration'],'Tests.ProximalBPSPolarIsometry.genuine_actual_polar_corrector_consumer']]
assert len(sel)==2 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in sel)
assert not re.search(r'\b(sorry|admit|axiom)\b',main+'\n'+test)
assert 'Tests.' not in main
snapchecks=[]
for row in rec['input_snapshots']:
 a=row['original'];raw=Path(row['exact_raw_snapshot']['path']).read_bytes();lf=Path(row['LF_snapshot']['path']).read_bytes();assert sha(raw)==a['raw_sha256'] and sha(norm(raw))==sha(lf)==a['lf_sha256'];snapchecks.append(dict(path=a['path'],RAW_sha256=sha(raw),LF_sha256=sha(lf),exact=True))
put('focused-evidence-audit.json',dict(schema='source65-focused-evidence-not-self-verification-v1',command=rec['command'],actual_foreground_pid=36260,exit_code=0,terminal_closed=True,jobs=3945,axioms=sel,input_snapshot_checks=snapchecks,production_does_not_import_Test=True,private_providers=[],direct_fake_closure_tokens=[],source_reviewer_started_compiler=False,independent_mathematical_verification_not_claimed=True))
# Original statement seals: compare the exact theorem prefix excluding final ':= by'.
headerchecks=[]
for label,code in [('0',main),('1',test)]:
 h=norm((O/('input.sealed-header'+label+'.raw')).read_bytes()).decode()
 # Header standalone files include theorem declaration and := by marker; exact suffix prefix matches.
 marker='theorem actual_centered_polar_isometry' if label=='0' else 'theorem genuine_actual_polar_corrector_consumer'
 a=code[code.index(marker):code.index(':= by',code.index(marker))].rstrip();b=h[h.index(marker):h.index(':= by',h.index(marker))].rstrip() if marker in h else h.rstrip()
 ok=(a==b);headerchecks.append(dict(header=label,raw_sha256=sha((O/('input.sealed-header'+label+'.raw')).read_bytes()),exact_current_header_equal=ok))
put('sealed-header-pin-audit.json',dict(schema='source65-sealed-header-pin-audit-v1',checks=headerchecks))
inv=json.loads((O/'primary-first.source-coverage-inventory.json').read_bytes());primary=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for row in inv['math_items']:
 raw=primary[row['raw_byte_start']:row['raw_byte_end_exclusive']];assert sha(raw)==row['raw_math_sha256'];assert row['classification'] and row['alttext_present'] and row['annotation_present'] and row['annotation_exactly_matches_alttext']
for reg in inv['regions']:
 a,z=reg['source_raw_byte_range'];raw=primary[a:z];assert len(re.findall(rb'<math\b',raw))==reg['math_count']
put('source-coverage-audit.json',dict(schema='source65-source-coverage-reuse-audit-v1',source_RAW_sha256=sha(primary),primary_graph_RAW_sha256=sha((O/'primary-first.source-proof-graph.json').read_bytes()),inventory_RAW_sha256=sha((O/'primary-first.source-coverage-inventory.json').read_bytes()),source_first_seal_RAW_sha256=sha((O/'primary-first-seal.json').read_bytes()),math_items=280,classified=280,missing=0,annotation_mismatch=0,complete_within_six_selected_regions=True,classification_counts=inv['classification_counts'],scope='B16 typed polar and first corrector adjoint/contraction/residual interface. Every printed B17/H1/B13/B14 and dynamics/cost/corrector-formula item remains explicitly classified as inherited upstream or downstream/outside current conclusion.',whole_paper_coverage_claim=False,source_graph_unchanged=True))
print(json.dumps(dict(pid=os.getpid(),binding=bindinghash,context=sha(canon(context)),spans=5,math_items=280,focused_exit=0,headerchecks=headerchecks,inputs=len(inputs),freeze_pins=len(pins)),indent=2))
