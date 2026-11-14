#!/usr/bin/env python3
"""Apply only this independent audit and one normal source-V transition."""
from pathlib import Path
import datetime,gzip,hashlib,json,subprocess,sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_advance as adv
import astis_publication as pub
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(v):return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def project(raw):return adv._replay_advances([json.loads(l) for l in raw.splitlines() if l])
baseline=json.loads((OUT/'preservation-baseline.json').read_bytes())
ledger=ROOT/'runs/substantive_advances.jsonl'
prefix=gzip.decompress((OUT/'ledger-prefix.raw.jsonl.gz').read_bytes())
assert ledger.read_bytes()==prefix
audit_path=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-tv-amplification.json'
assert sha(audit_path.read_bytes())==baseline['canonical_audit_before_sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==baseline['head']
gate=json.loads((OUT/'prospective-reviewed-gate.receipt.json').read_bytes());assert gate['exit_code']==0
proposed=(OUT/'proposed-canonical-audit.json').read_bytes();audit=json.loads(proposed)
reviewer='/root/ex72_fresh_source_v2';target='ASTIS-SA-20261107-GaussianComplexityTVAmplification'
before=project(prefix);assert before[target]['state']=='PROVED_LOCAL'
assert before[target]['owner_id']=='huanjian_gc_20261107_ex72'
assert audit['source_review']['reviewer']==reviewer and audit['source_review']['state']=='accepted'
declarations=[audit['lean']['declaration']]
assert declarations==before[target]['publication_declarations']
assert pub.roundtrip.semantic_reviewer_packet(audit)['packet_sha256']=='06e1992c80f5cec08b2b959fdd8a3d7549fb6fd33fe289ab44b4b0b800ba9b38'
applied_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
audit_path.write_bytes(proposed)
evidence={
 'verifier_id':reviewer,'verified_commit':baseline['head'],
 'publication_declarations':declarations,
 'gate':{'kind':'fresh source-bound Lean target/Test/actual-producer elaborations and independent expanded statement/axioms probe; exact static candidate content review',
  'evidence_root':str(OUT.relative_to(ROOT)),
  'math_candidate_commit':'ebf76119351b23ef0718fc69aa5081515bab0b52',
  'target_sha256':'9c96a4b80420bf114e700ed61f4adf88f79b85d24c4d21848e466d67b93ba431',
  'test_sha256':'6bd58c4010c81dfa7948c9de1632c35fb0b14385bbdef5e5c28f5e1f2ca10cee',
  'prospective_reviewed_gate_receipt':str((OUT/'prospective-reviewed-gate.receipt.json').relative_to(ROOT)),
  'root_or_Registry_or_live_reader_or_remote_or_purification_acceptance':False},
 'source_audit':{'path':str(audit_path.relative_to(ROOT)),'sha256':sha(proposed),
  'review_run_sha256':audit['source_review']['review_run_sha256'],
  'reviewer_packet_sha256':audit['source_review']['reviewer_packet_sha256'],
  'publication_binding_sha256':audit['publication_binding_sha256'],
  'source_review_artifact':str((OUT/'review-result.json').relative_to(ROOT)),
  'raw_source_first_expectation_sha256':'9200b0c66a9339f3b8198b3128fffac25032c593080e956bf08356c0311d637c',
  'source_versus_blind_comparison_sha256':'3319ee82fecc1c5fab860338c036f20f0ba773a9461875d30a86e636409155c7'},
 'semantic_roundtrip_audit':audit['id'],
 'fake_closure_scan':{'artifact':str((OUT/'actual-source-closure-and-fakeclosure.json').relative_to(ROOT)),
  'sha256':sha((OUT/'actual-source-closure-and-fakeclosure.json').read_bytes()),
  'project_import_closure_modules':48,'matches':0,'compiled_axioms':['propext','Classical.choice','Quot.sound']},
 'remaining_boundary':'Source V only. Normal stabilization, current root/Registry/site gates, live rendered/Chrome/remote delivery and purification are later separate work; no whole-Goal completion.'}
adv.transition_advance(target,'VERIFIED',worker_id=reviewer,evidence=evidence)
after_raw=ledger.read_bytes();assert after_raw.startswith(prefix)
suffix=after_raw[len(prefix):];lines=suffix.splitlines();assert len(lines)==1
event=json.loads(lines[0]);assert event['event']=='transition' and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['advance_id']==target and event['worker_id']==reviewer
after=project(after_raw)
assert after[target]['owner_id']==before[target]['owner_id']
assert {k:v for k,v in after.items() if k!=target}=={k:v for k,v in before.items() if k!=target}
front=json.loads(gzip.decompress((OUT/'foreign-frontier-files.json.gz').read_bytes()))
assert len(front)==437 and all(sha((ROOT/f).read_bytes())==h for f,h in front.items())
cell=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-tv-amplification.json'
assert sha(cell.read_bytes())==baseline['target_frontier_sha256']
protected=json.loads(gzip.decompress((OUT/'protected-tracked-content.json.gz').read_bytes()))
changed=[f for f,h in protected.items() if not (ROOT/f).is_file() or sha((ROOT/f).read_bytes())!=h]
assert not changed,changed[:20]
for path,expected in [('phase1/source-expectations.json','9200b0c66a9339f3b8198b3128fffac25032c593080e956bf08356c0311d637c'),('phase2/source-versus-blind-comparison.json','3319ee82fecc1c5fab860338c036f20f0ba773a9461875d30a86e636409155c7')]:assert sha((OUT.parent/path).read_bytes())==expected
(OUT/'verified-append.raw.jsonl.gz').write_bytes(gzip.compress(suffix,mtime=0))
receipt={'applied_utc':applied_utc,'verified_after_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'head':baseline['head'],'source_V_state':after[target]['state'],'owner_retained':after[target]['owner_id'],
 'independent_verifier':reviewer,'canonical_audit_sha256':sha(audit_path.read_bytes()),
 'review_run_sha256':audit['source_review']['review_run_sha256'],
 'ledger_prefix_bytes':len(prefix),'ledger_prefix_sha256':sha(prefix),'ledger_prefix_preserved_exactly':True,
 'exactly_one_normal_API_append':True,'unique_append_bytes':len(suffix),'unique_append_raw_sha256':sha(suffix),
 'ledger_after_sha256':sha(after_raw),'ledger_records_before':len(prefix.splitlines()),'ledger_records_after':len(after_raw.splitlines()),
 'all_278_foreign_projected_states_preserved':True,'all_437_foreign_frontier_files_preserved':True,'target_frontier_unchanged':True,
 'protected_tracked_files':len(protected),'all_protected_tracked_content_preserved':True,'phase1_phase2_hashes_unchanged':True,
 'mutations':'Only canonical huanjian-tv-amplification audit and one normal PROVED_LOCAL→VERIFIED ledger append; all other newly created files are owned phase3 evidence.',
 'later_separate_scope':'No STAB, root/Registry/site gate, live browser acceptance, remote publication, purification or Goal transition.'}
(OUT/'actual-source-V-and-preservation-receipt.json').write_bytes(jb(receipt))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
