from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79');d=r/'fresh-source79'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
native=load(d/'source-review.result79.json');m=load(d/'source-review.run-manifest79.json')
assert sha((d/'source-review.result79.json').read_bytes())=='a63a96ff5c14ba40b1cbd321f11bb6cf3934e7035a0356e97a5cefda477d5f37'
assert sha((d/'source-review.run-manifest79.json').read_bytes())=='fd5696efb3afef6d4f6367b2bb46c35e41e33efa4d5df5d17e531698eaafc365'
for group in ['raw_inputs','raw_outputs']:
 for item in m[group]:assert sha(Path(item['path']).read_bytes())==item['raw_sha256'],item['path']
runhash=sha((d/'source-review.run-evidence79.json').read_bytes());assert runhash==native['review_run_sha256']=='ad2e7dd0780745409d6a8b460563891212c1675b7f8eff692f599a6746945c0e'
assert native['verdict']=='equivalent-after-elaboration' and not native['repairs'] and native['no_required_mathematical_repairs']
assert native['independence']['source_inventory_frozen_independently_before_candidate'] and not native['independence']['previous79_verdicts_seen']
assert native['authored_step_coverage']['gaps']==[] and native['authored_step_coverage']['step_count']==9
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeCover.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review79.packet.json')
assert packet['packet_sha256']==native['reviewer_packet_sha256'] and a['publication_binding_sha256']==native['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==native['full_module_sha256']
(r/'audit.before-source79.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent source review {x['id']} in {d.as_posix()}/source-review.result79.json; exact current module and nine proof regions bound by run {runhash}.",native_classification=x['classification']) for x in native['deltas']]
a.update(state='accepted',semantic_slots=native['semantic_slots'],deltas=deltas,verdict=native['verdict'],source_review=dict(state='accepted',reviewer=native['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=native['review_evidence'],review_run_sha256=runhash,reviewer_packet_sha256=native['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence79.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest79.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source79.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result79.json'),native_manifest=pin(d/'source-review.run-manifest79.json'),native_run_evidence=pin(d/'source-review.run-evidence79.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=native['reviewer'],full_current_module_RAW_sha256=native['full_module_sha256'],semantic_verdict=native['verdict'],source_graph_coverage=native['source_graph_coverage'],VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math79/decision79.json').as_posix(),source_review=(d/'source-review.result79.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result79.json').as_posix(),fresh_source_graph=(d/'source_proof_graph79.json').as_posix(),fresh_source_inventory=(d/'source_inventory79.json').as_posix(),coverage_status='Independent complete scoped source inventory, every edge and nine BODY/formula regions accepted for actual-interval-cover. Source physical initialization/interpolation and global properties remain PARTIAL/OPEN, not silently discharged.')
c['blocked']['reason']='Actual interval/live-record/elapsed focused compile, independent mathematics/blind/source accepted; exact-commit verification and serialized aggregation pending.'
evidence=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused79-attempt2/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math79.adoption.json'),blind_decoder=pin(r/'root.decoder79.adoption.json'),source_review=pin(r/'root.source79.adoption.json'),integration_notes='One actual interval/live-record/elapsed consumer joining exact actual finite recursion and actual nonaccumulation. Existing sole stabilization lane reused later; no new lane or self-VERIFIED transition.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=evidence)
c['status']='proved_locally';save(cp,c);new(r/'proved-local79.json',evidence)
print('PROVED_LOCAL79: actual interval/live record/elapsed; independent exact-commit verification pending.')
