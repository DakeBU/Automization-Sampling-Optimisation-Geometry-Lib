from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78');d=r/'fresh-source78'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
native=load(d/'source-review.result78.json');m=load(d/'source-review.run-manifest78.json');mh=sha((d/'source-review.run-manifest78.json').read_bytes())
assert mh==native['review_run_sha256']=='a839983a1ec1c1571bac7c667c9d2ce7b408f33b667522539381c0f0454d5934'
for group in ['inputs','outputs']:
 for p in m[group]:
  if 'raw_sha256' in p:assert sha(Path(p['path']).read_bytes())==p['raw_sha256'],p['path']
  if 'canonical_payload_sha256' in p:
   val=load(p['path']);assert rt.sha256_json({k:v for k,v in val.items() if k not in p['excluded_fields']})==p['canonical_payload_sha256']
assert native['verdict']=='equivalent-after-elaboration' and not native['repairs']
assert native['truth_boundary']['no_required_mathematical_repairs']
assert native['independence']['source_only_freeze_before_candidate'] and not native['independence']['previous_verdicts_seen']
assert native['authored_step_coverage']['gaps']==[] and len(native['authored_step_coverage']['steps'])==7
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualNonaccumulation.json');a=load(ap)
assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review78.packet.json')
assert packet['packet_sha256']==native['reviewer_packet_sha256'] and a['publication_binding_sha256']==native['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==native['full_module_sha256']
(r/'audit.before-source78.json').write_bytes(ap.read_bytes())
# Preserve the native richer delta classifications; map only schema fields.
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent source-review {x['id']} in {d.as_posix()}/source-review.result78.json; exact current module and seven-step coverage bound by run {mh}.",native_classification=x['classification']) for x in native['deltas']]
a.update(state='accepted',semantic_slots=native['semantic_slots'],deltas=deltas,verdict=native['verdict'],source_review=dict(state='accepted',reviewer=native['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=native['review_evidence'],review_run_sha256=mh,reviewer_packet_sha256=native['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-manifest78.json').as_posix()))
save(ap,a)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source78.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result78.json'),native_manifest=pin(d/'source-review.run-manifest78.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=native['reviewer'],full_current_module_RAW_sha256=native['full_module_sha256'],semantic_verdict=native['verdict'],source_graph_coverage=native['source_graph_coverage'],source_scale_supplement=pin(d/'source_supplement78.json'),VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math78/decision78.json').as_posix(),source_review=(d/'source-review.result78.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result78.json').as_posix(),fresh_source_graph=(d/'source_proof_graph78.json').as_posix(),fresh_source_inventory=(d/'source_inventory78.json').as_posix(),coverage_status='Independent complete scoped-source and seven-BODY/formula coverage accepted. Source direct Exp mean-one/SLLN remains OPEN alternative; ASTIS sufficient indicator route closed. No global-process claim.')
c['blocked']['reason']='Focused compiled actual nonaccumulation, independent math/blind/source accepted; exact-commit verification and public aggregation pending.'
evidence=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused78-attempt2/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math78.adoption.json'),blind_decoder=pin(r/'root.decoder78.adoption.json'),source_review=pin(r/'root.source78.adoption.json'),integration_notes='One actual source consumer joining finite recurrence and canonical stochastic input. Existing sole stabilization lane reused later; no new lane or self-VERIFIED transition.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=evidence)
c['status']='proved_locally';save(cp,c);new(r/'proved-local78.json',evidence)
print('PROVED_LOCAL78: actual nonaccumulation and finite index sets; independent exact-commit verification pending.')
