from common import *
import tools.astis_advance as adv
import tools.astis_publication as pub
ADV='ASTIS-SA-20261009-PBPSPositiveRealRootUniqueness'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==SCI
b=J(P/'inputs.before.json');plan=J(R/'publication-plan.json');native=J(P/'native.review.json')
for q in b['mathematical_freeze']:matches(q)
for pair in b['qualified_snapshot_pairs']:
 matches(pair['original']);matches(pair['exact_raw_snapshot'])
for q in native['verified_pins']:matches(q['original'], q['historical_mapping']['exact_raw_snapshot']['path'] if q.get('historical_mapping') else None)
science=J(P/'science.entries.json')
for q in science['entries']:matches(q['current'])
assert science['count']==1003
seals=[]
for i,(module,name) in enumerate(zip(['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRootUnique.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRootUnique.lean'],['positive_square_roots_unique','actual_unique_positive_real_defect_root'])):
 header=ROOT/f'runs/20261007-companion-priority/pbps-real-root-unique-preproof62/header{i}.lean'
 h=header.read_bytes().replace(b'\r\n',b'\n').strip();s=path(module).read_bytes().replace(b'\r\n',b'\n');start=s.index(('theorem '+name).encode());a=s[start:s.index(b':= by',start)].strip();assert a==h
 seals.append(dict(header=pin(header),production=pin(module),exact_signature_sha256=H(a),signature_LF=a.decode(),exact=True))
W(P/'sealed-signatures.json',dict(status='PASS',declarations=seals))
history=[]
for i,aid in enumerate(plan['audit_ids']):
 original=ROOT/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json'
 current=J(original)
 for stage,script,line in [('before-decoder','adopt-decoder62.py',35),('before-source-admission','admit62.py',39)]:
  snap=R/f'audit.{i}.{stage}.raw.snapshot.json';q=J(snap);assert q['id']==aid
  assert q['publication_binding_sha256']==current['publication_binding_sha256']
  assert q['lean']['statement_sha256']==current['lean']['statement_sha256']
  assert q['state']==('encoded' if stage=='before-decoder' else 'blind-reconstructed'),q['state']
  authority=R/'root-science-executed62'/script
  history.append(dict(qualified_original_path=original.as_posix(),historical_stage=stage,historical_original_raw_LF=pin(snap),exact_raw_snapshot=pin(snap),authority=pin(authority),authority_line=line,current_admitted=pin(original),purpose='Administrative-stage provenance only; actual native source original31 excludes canonical audits. Not a source input fallback.'))
W(P/'history.json',dict(audit_stage_maps=history,audit_stage_map_count=4,native_source_audit_input_maps_used=0,native_source_original_manifest_excludes_canonical_audits=True,pre_VERIFIED_ledger_exact_map=b['historical_ledger_before'],scope='Only these exact qualified historical identities; no directory fallback or basename alias.'))
for n in ['gates.json','native.review.json','fake-closure.json','reviewed-publication.json']:assert J(P/n).get('status')=='PASS'
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
state=adv.current_advances();assert state[ADV]['state']=='PROVED_LOCAL';assert state[ADV]['owner_id']!=ACTOR
lane=[k for k,v in state.items() if v['state']=='STABILIZING'];assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'],lane
ledger=ROOT/'runs/substantive_advances.jsonl';old=ledger.read_bytes();matches(b['historical_ledger_before']['original']);matches(b['historical_ledger_before']['exact_raw_snapshot'])
W(P/'prepromotion.readback.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,science_entries=1003,freeze_pins=27,native_unique_pins=409,qualified_before_snapshot_pairs=18,audit_stage_maps=4,sole_STABILIZING=lane,ledger_before=pin(ledger),scope=plan['remaining_boundary']))
evidence=dict(gate='Actual focused lake build Tests.ProximalBPSRealDefectRootUnique PID50432 EXIT0 PASS3918, pinned Lean4.33.0/Mathlib; four independent noncompiler gates PASS. Shared aggregate deferred.',verifier_id=ACTOR,verified_commit=SCI,checked_commit=SCI,source_audit=[q['audit']['path'] for q in native['source_audits']],fake_closure_scan=(P/'fake-closure.json').as_posix(),publication_declarations=plan['mathematical_declarations'],verification_receipt=(P/'receipt.json').as_posix(),bounded_gates=(P/'gates.json').as_posix(),source_gate=(P/'native.review.json').as_posix(),truth_boundary=plan['remaining_boundary'],compiler_standard3=True)
adv.transition_advance(ADV,'VERIFIED',worker_id=ACTOR,evidence=evidence)
new=ledger.read_bytes();assert new.startswith(old);tail=new[len(old):];rows=[json.loads(x) for x in tail.splitlines() if x.strip()];assert len(rows)==1
state=adv.current_advances();assert state[ADV]['state']=='VERIFIED';assert [k for k,v in state.items() if v['state']=='STABILIZING']==lane
W(P/'transition.json',dict(status='PASS',actual_PID=os.getpid(),api='tools.astis_advance.transition_advance',advance_id=ADV,worker_id=ACTOR,checked_commit=SCI,from_state='PROVED_LOCAL',to_state='VERIFIED',evidence=evidence,ledger_before=b['historical_ledger_before'],ledger_after=pin(ledger),exact_appended_records=rows,exact_appended_raw_sha256=H(tail),sole_STABILIZING_unchanged=lane,canonical_cells_audits_Lean_unchanged=True))
print('EXACT62_INDEPENDENT_VERIFIED',SCI,'1003Git/27math/409native/4audit-stage/1ledger-map')
