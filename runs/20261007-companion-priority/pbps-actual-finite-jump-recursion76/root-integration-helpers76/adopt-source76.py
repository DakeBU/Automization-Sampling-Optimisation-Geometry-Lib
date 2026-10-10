from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');o=r.parent/'pbps-recursive-preproof76/fresh-compiled-source76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p;return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;write(p,x)
lp=o/'CLOSED_LAST.json';lease=load(lp);assert sha(lp.read_bytes())=='0ca0645db780b696424ca80753fcf5a843369a5037a2bb26049a553dbeeb7d79'
assert lease['state']=='CLOSED_LAST' and lease['reviewer']=='/root/fresh_source76' and lease['file_count_before_marker']==120
assert {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}=={z['path'] for z in lease['files']}|{'CLOSED_LAST.json'}
for z in lease['files']:
 p=o/z['path'];b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and len(lf)==z['CRLF_to_LF_only_bytes'] and sha(lf)==z['CRLF_to_LF_only_sha256'];assert p.stat().st_mtime_ns<=lp.stat().st_mtime_ns
raw=(o/lease['logical_run_file']).read_bytes();assert raw==(o/lease['named_RAW_payload']).read_bytes()
h=sha(raw);assert h==lease['review_run_sha256']=='f2c1461c58bf015a603c4cd94be6f6aec0da6745ae5f8163b8389dec257400f7'
run=json.loads(raw);report=load(o/lease['native_report_file']);assert sha((o/lease['native_report_file']).read_bytes())=='eef26b0e01adfc5f3c98d7b54be79e9eabf45ed6f23355752ae1ace098ac6168'
assert not run['prior_verdicts_or_other_reviewer_outcomes_seen'] and not run['canonical_audit_cell_publication_contents_seen'] and not run['hash_only_pins_used_as_content'] and not run['canonical_or_ledger_writes']
for z in run['readable_input_manifest']:assert check(z)==(o/z['own_raw_copy']).read_bytes()
assert len(run['readable_input_manifest'])==15 and run['current_module_lines']==412
assert run['state']==report['state']==report['audit_fields']['state']==report['source_review']['state']=='accepted'
assert not run['blocking_deltas'] and not run['repairs'] and not report['source_or_publication_mathematical_repair_required']
assert run['axioms']==['propext','Classical.choice','Quot.sound'] and run['direct_focused_Lean_and_axiom_evidence']['exit_code']==0
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'verify_closed_readonly76.py')],stdout=s,stderr=e);code=p.wait()
assert code==0
readonly=json.loads((out/'native-readonly.stdout.log').read_bytes());assert readonly['status']=='PASS_EXTERNAL_READ_ONLY_CLOSED_LAST_VALIDATION' and not readonly['filesystem_writes_performed']
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert adv.current_advances()[claim['advance_id']]['state']=='EXPLORING'
assert load(r/'root.math76.adoption.json')['native_files']==82 and load(r/'root.decoder76.adoption.json')['status']=='CLOSED_BLIND_DECODER76_ADOPTED_ONLY'
ap=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][0]+'.json');cp=Path('research-wiki/frontier-cells')/(plan['active_cells'][0]+'.json');pp=Path('website/content/publications')/(plan['slugs'][0]+'.json')
audit,cell,publication=load(ap),load(cp),load(pp);packet=load(r/'source-review.clean.packet.json')
assert audit['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(audit)==packet
assert report['reviewer_packet_sha256']==run['packet_sha256']==packet['packet_sha256']
assert report['publication_binding_sha256']==audit['publication_binding_sha256']==run['publication_binding_sha256']
accepted=copy.deepcopy(audit)
accepted.update({k:report['audit_fields'][k] for k in ['state','semantic_slots','verdict','repairs']})
# A mechanical schema adapter retains every native delta field. Nonblocking explicit
# elaborations map to informational; the description copies native source/Lean text.
accepted['deltas']=[]
for z in report['audit_fields']['deltas']:
 assert z['blocking'] is False and z['kind']=='explicit-elaboration'
 q=copy.deepcopy(z);q.update(severity='informational',description=z['classification']+': '+z['source']+' '+z['lean']);accepted['deltas'].append(q)
accepted['source_review']=copy.deepcopy(report['source_review'])
accepted['source_review']['run_artifact']=(o/lease['logical_run_file']).as_posix()
assert rt.semantic_reviewer_packet(accepted)==packet
projections=[load(o/'canonical-cell-source-proof-coverage76.json'),load(o/'canonical-publication-source-proof-coverage76.json')]
coverage=projections[0]['source_proof_coverage'];assert coverage==projections[1]['source_proof_coverage']
assert len(coverage['inventory'])==131 and len(coverage['reviewed_nodes'])==44 and len(coverage['excluded_with_reason'])==87
assert coverage['future_scope_status']=='OPEN' and coverage['no_whole_Proposition3_1_credit'] and coverage['no_whole_paper_or_Goal_credit']
cell['source_proof_coverage']=coverage;publication['items'][0]['source_proof_coverage']=coverage
registry=rt.load_registry();registry['audits']=[accepted if x['id']==accepted['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
for path,kind in [(ap,'audit'),(cp,'cell'),(pp,'publication')]:
 snapshot=r/(kind+'.before-source-admission76.exactraw.json');assert not snapshot.exists();snapshot.write_bytes(path.read_bytes())
write(ap,accepted);write(cp,cell);write(pp,publication);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==accepted['publication_binding_sha256'] and pub.review_context(item,item['bindings'][0],pub.inputs())==accepted['publication_context']
mirror=load(r/'conceptual-mirror-audit76.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary='Actual fixed-reference finite stopped recursion(A2), joint Borel indexed records, original initial-energy inheritance and uniform waiting increment including stopped infinity only. Focused compilation, independent full mathematics, strict blind decoder and fresh source-first full source/BODY review accepted. iid Exp1 product/a.s. positivity/partial-sum divergence/nonaccumulation, physical-time global path/Markov/invariance/terminal sampler/hypocoercivity/main/errors/expected-query costs/composition remain open. ExactSCI76, serialized aggregate/reader, full Exposition/PURIFIED/main/live/paper/Goal remain distinct and pending.'
math=load(r/'root.math76.adoption.json')['fresh_compiler'];focused=load(r/'mathematics-freeze76.json')['compiled'][0]
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result=f"Root{focused['focused_PID']} EXIT0/{focused['jobs']}jobs; independent directLean{math['actual_foreground_Lean_PID']} EXIT0/standard3; fresh anti-source fullLean40920 EXIT0/standard3. Statement/BODY unchanged; earlier failed inference routes retained.")],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+plan['slugs'][0]+'.json'],integration_notes='Actual73 flow/74 bounce+rate/75 hitting clock are genuine parents. Current recurrence is the consumer of their finite-time/Borel/energy laws and producer for actual iid-threshold event-time nonaccumulation. No provider premise, global path for arbitrary zero thresholds or false paper-completion credit. Fresh source-only topology and exhaustive131 inventory retained independently of older prospective graph. Exact native semantic-delta fields are copied with declared mechanical severity/description schema adapter; no mathematical repair or changed binding.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[key])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math76/decision.json').as_posix(),source_review=(o/lease['native_report_file']).as_posix(),execution_boundary=boundary);write(cp,cell)
new(r/'proved-local.json',e)
new(r/'root.source76.adoption.json',dict(status='ACCEPTED_FRESH_INDEPENDENT_SOURCE76_FINITE_STOPPED_RECURSION_ONLY',actual_root_PID=os.getpid(),native_owned_files=121,native_whole_logical_run_sha256=h,native_named_payload=pin(o/lease['named_RAW_payload']),native_report=pin(o/lease['native_report_file']),native_lease=pin(lp),native_readonly_PID=p.pid,native_readonly_EXIT=code,coverage_counts=dict(items=131,NODE=44,EXCLUDED=87,subclaims=9,external_citations=12),schema_adapter='Every native delta copied, explicit nonblocking elaboration -> informational; description concatenates native classification/source/Lean. Native review object copied; top-level native state/slots/verdict/repairs copied.',no_mathematical_repair=True,official_reviewer_packet_unchanged=True,publication_binding_unchanged=True,stale_coordinate_debt_retained=True,VERIFIED=False,Goal_complete=False))
print('PASS76 PROVED_LOCAL once after full math/strictblind/fresh anti-source and reviewed publication gate; exactSCI/aggregate/reader pending.')
