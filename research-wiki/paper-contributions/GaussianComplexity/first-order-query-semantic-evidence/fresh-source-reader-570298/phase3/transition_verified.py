from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,subprocess,sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from tools import astis_advance as api
TARGET='ASTIS-SA-20261107-GaussianComplexityFirstOrderQuery'
NAME='AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query'
SELF='/root/reader_570298';COMMIT='214b6214c5b08bd52b6faa59a3ccd6ca35998420'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def filepin(name):
 p=OUT/name;b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)}
assert not (OUT/'verified-transition-receipt.json').exists()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==COMMIT
before=json.loads((OUT/'preservation-before.json').read_bytes())
prefix=gzip.decompress((OUT/before['advance_ledger_exact_snapshot']).read_bytes())
assert api.DEFAULT_ADVANCE_LEDGER.read_bytes()==prefix
assert sha(api.DEFAULT_DISCOVERY_LEDGER.read_bytes())==before['discovery_ledger_sha256']
for path,h in before['frontier_hashes'].items():assert sha((ROOT/path).read_bytes())==h,path
own_audit='research-wiki/semantic-roundtrip/audits/huanjian-first-order-query.json'
for path,h in before['audit_fragment_hashes'].items():
 if path!=own_audit:assert sha((ROOT/path).read_bytes())==h,path
assert sha((ROOT/'research-wiki/semantic-roundtrip/registry.json').read_bytes())==before['registry_sha256']
states=api.current_advances();foreign={k:v for k,v in states.items() if k!=TARGET}
assert len(foreign)==279 and sha(canonical(foreign))==before['foreign_states_sha256']
assert states[TARGET]['state']=='PROVED_LOCAL'
assert states[TARGET]['owner_id']=='huanjian_gc_20261107_first_order_query'
for label in ['focused-build','production-direct','test-direct','critical-expansion','reviewed-publication-gate','semantic-registry-gate']:
 r=json.loads((OUT/(label+'.receipt.json')).read_bytes());assert r['exit_code']==0
 assert r['checked_commit']==r['head_after']==COMMIT
 assert sha((ROOT/r['log']).read_bytes())==r['log_sha256']
result=json.loads((OUT/'review-result.json').read_bytes());audit=json.loads((ROOT/own_audit).read_bytes())
assert result['verdict']=='equivalent-after-elaboration'
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
assert audit['source_review']['reviewer']==SELF
assert sha((OUT/'review-run.json').read_bytes())==result['review_run_sha256']
assert sha((ROOT/own_audit).read_bytes())==json.loads((OUT/'audit-update-receipt.json').read_bytes())['new_sha256']
verification='Independent /root/reader_570298 reviewed exact immutable214b target/Test, actual canonical ASTIS ancestry, all meaning definitions, raw-source-first seven slots, blind reconstruction, authored formula proof and stock static reader. Fresh focused production/Test/critical-expansion checks and real reviewed publication/semantic gates pass. Complete sanitized ancestor scan is clean; printed target/regularity axioms are only propext/Classical.choice/Quot.sound. Full packet and publication bindings are exact. The checked214b tree contains the blind audit; this accepted audit is a later working-tree metadata update, not claimed present in214b. Browser/canonical root integration and all downstream adaptive/cap/law/lower-bound claims remain separate.'
evidence={
 'verifier_id':SELF,'verified_commit':COMMIT,'publication_declarations':[NAME],'lean_declarations':[NAME],
 'gate':{'scope':'Independent focused source-V, not canonical root/integration acceptance',
  'receipt_pins':[filepin(n+'.receipt.json') for n in ['focused-build','production-direct','test-direct','critical-expansion','reviewed-publication-gate','semantic-registry-gate']]},
 'source_audit':{'result':filepin('review-result.json'),'run':filepin('review-run.json'),
  'reviewer_packet_sha256':result['reviewer_packet_sha256'],'publication_binding_sha256':result['publication_binding_sha256'],
  'source_raw_sha256':result['source_raw_sha256'],'verdict':result['verdict']},
 'semantic_roundtrip_audit':{'id':'ASTIS-RT-20261107-HuanjianFirstOrderQuery','path':own_audit,
  'sha256':sha((ROOT/own_audit).read_bytes()),'state':'source-reviewed','source_review':'accepted'},
 'fake_closure_scan':filepin('sanitized-fake-closure-scan.json'),
 'independent_verification':verification,
 'static_reader':filepin('static-reader-review.json'),
 'truth_boundary':result['remaining_boundary'],
 'checked_tree_audit_state':'blind-reconstructed','accepted_audit_is_later_working_tree_metadata':True,
 'frontier_projection':'Left unchanged for root mechanical projection; no foreign frontier mutation.'}
assert isinstance(evidence['independent_verification'],str)
dump('verified-transition-evidence.json',evidence)
# Required normal independent verifier API; it performs the reviewed publication gate again.
api.transition_advance(TARGET,'VERIFIED',worker_id=SELF,modes=['independent-source-review','whole-module-review','static-reader-review'],evidence=evidence)
after_raw=api.DEFAULT_ADVANCE_LEDGER.read_bytes();assert after_raw.startswith(prefix)
tail=after_raw[len(prefix):];events=[json.loads(x) for x in tail.splitlines() if x.strip()]
assert len(events)==1
event=events[0]
assert event['advance_id']==TARGET and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==SELF
after=api.current_advances();after_foreign={k:v for k,v in after.items() if k!=TARGET}
assert after_foreign==foreign
assert after[TARGET]['state']=='VERIFIED' and after[TARGET]['owner_id']==states[TARGET]['owner_id']
assert after[TARGET]['publication_declarations']==states[TARGET]['publication_declarations']==[NAME]
assert api.DEFAULT_DISCOVERY_LEDGER.read_bytes() and sha(api.DEFAULT_DISCOVERY_LEDGER.read_bytes())==before['discovery_ledger_sha256']
for path,h in before['frontier_hashes'].items():assert sha((ROOT/path).read_bytes())==h,path
for path,h in before['audit_fragment_hashes'].items():
 if path!=own_audit:assert sha((ROOT/path).read_bytes())==h,path
assert sha((ROOT/'research-wiki/semantic-roundtrip/registry.json').read_bytes())==before['registry_sha256']
(OUT/'verified-event.exact.jsonl').write_bytes(tail)
dump('verified-transition-receipt.json',{'status':'PASS','api':'tools.astis_advance.transition_advance',
 'advance_id':TARGET,'worker_id':SELF,'verified_commit':COMMIT,
 'from_state':'PROVED_LOCAL','to_state':'VERIFIED','proof_owner_preserved':after[TARGET]['owner_id'],
 'publication_declaration_set_unchanged':[NAME],'event':event,
 'old_ledger_bytes':len(prefix),'old_ledger_sha256':sha(prefix),'new_ledger_bytes':len(after_raw),'new_ledger_sha256':sha(after_raw),
 'appended_bytes':len(tail),'appended_sha256':sha(tail),'exact_original_prefix_preserved':True,
 'foreign_advances_preserved':279,'foreign_states_sha256_before':sha(canonical(foreign)),'foreign_states_sha256_after':sha(canonical(after_foreign)),
 'discovery_ledger_byte_unchanged':True,'all_frontier_files_byte_unchanged':True,'all_foreign_audit_fragments_byte_unchanged':True,
 'canonical_semantic_registry_byte_unchanged':True,'audit_update_receipt':filepin('audit-update-receipt.json'),
 'checked_tree_audit_state':'blind-reconstructed','accepted_dirty_audit_bytes_not_claimed_in_checked_commit':True,
 'completed_utc':datetime.now(timezone.utc).isoformat(),'no_stabilization_or_merge_transition':True})
print('Normal API VERIFIED transition PASS; owner and exact target set preserved; exact ledger prefix and279 foreign advance states/discoveries/frontiers/foreign audits unchanged.')
print('receipt SHA256',sha((OUT/'verified-transition-receipt.json').read_bytes()))
