from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
root=Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(root))
from tools import astis_advance
out=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
J=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def pin(name):b=(out/name).read_bytes();return {'path':str((out/name).relative_to(root)),'sha256':H(b)}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()=='de220a52922fc2aa2c007ea14bf2c2949030b8d2'
assert json.loads((out/'pre-mutation-validation.json').read_bytes())['status']=='PASS'
ledger=root/'runs/substantive_advances.jsonl';before=gzip.decompress((out/'substantive_advances.jsonl.before.gz').read_bytes());assert ledger.read_bytes()==before
own='ASTIS-SA-20261107-GaussianComplexityFixedSpectrumQuery';state=astis_advance.current_advances();assert state[own]['state']=='PROVED_LOCAL'
foreign=gzip.decompress((out/'foreign-states-before.json.gz').read_bytes());current=json.dumps({k:v for k,v in state.items() if k!=own},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert current==foreign
apath=root/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-query.json';abefore=gzip.decompress((out/'huanjian-fixed-spectrum-query.json.before.gz').read_bytes());assert apath.read_bytes()==abefore
candidate=(out/'accepted-audit-candidate.json').read_bytes();a=json.loads(candidate);assert a['state']=='accepted' and a['source_review']['state']=='accepted'
for k in ['id','source','lean','reconstruction','publication_binding_sha256','publication_context','deltas','repairs']:assert a[k]==json.loads(abefore)[k]
# Only the expressly authorized own audit fragment is changed. The accepted bytes are a dirty successor to the checked commit.
tmp=out/'audit-replacement.tmp';tmp.write_bytes(candidate);os.replace(tmp,apath)
evidence={
 'verifier_id':'/root/reader_361904',
 'verified_commit':'de220a52922fc2aa2c007ea14bf2c2949030b8d2',
 'publication_declarations':['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query'],
 'gate':{'focused_direct_anonymous_checks':pin('fresh-lean-checks.json'),'critical_axioms':['propext','Classical.choice','Quot.sound'],'actual_ASTIS_proof_parents':[],'nine_actual_internal_bridges':pin('source-gap-implementation-bridges.json'),'standard_publication_and_roundtrip_gate':'The normal schema-v4 VERIFIED transition invokes check_advance(reviewed=True) on this exact declaration set. Read-only in-memory accepted-candidate registry and strict publication preflight already passed.','static_stock_reader_exact_code':pin('static-reader-check.json')},
 'source_audit':{'reviewer':'/root/reader_361904','verdict':'equivalent-after-elaboration','source_sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915','reviewer_packet_sha256':'146ae61276c657a6387e004ea2aa8ad877057608c659fc86dc22f131bc03d395','publication_binding_sha256':'fafc6866bd79667295b685939cb04e42374863753ab3e205c43ce6d0780e3970','run':pin('source-review-run.json'),'result':pin('source-review-result.json'),'phase1_freeze_sha256':'29bce28d1128e3ddbb4b4e398b65eab28a67c3d952febcf9391eba056efdb7c5','phase2_freeze_sha256':'22732114facd18a6432401c67ba55a60d5cad722ddd526ec97f98a4baac8d8b0','scope':'Actual pointwise same-O cosine-grid exact precision-matvec reply identities at kappa and2, d>=2/kappa>=2, plus actual same-x two-hidden-input consumer. Static-reader-only source V.'},
 'fake_closure_scan':pin('sanitized-fake-closure-scan.json'),
 'semantic_roundtrip_audit':{'audit_id':a['id'],'state':'accepted','verdict':a['verdict'],'source_review_run_sha256':a['source_review']['review_run_sha256'],'audit_path':str(apath.relative_to(root)),'accepted_audit_raw_sha256':H(candidate),'reviewer_packet_sha256':a['source_review']['reviewer_packet_sha256'],'publication_binding_sha256':a['publication_binding_sha256'],'provenance':pin('provenance-verification.json')},
 'accepted_audit_dirty_successor':{'checked_commit_audit_state':'blind-reconstructed / source pending','checked_commit_audit_raw_sha256':H(abefore),'accepted_bytes_in_checked_commit':False,'accepted_successor_raw_sha256':H(candidate),'note':'The source review updates only this own audit fragment in the working tree. Root will commit accepted successor bytes later; no accepted-state bytes are claimed inside de220a52922fc2aa2c007ea14bf2c2949030b8d2.'},
 'truth_boundary':['No formal PD/spectrum/normalizer/background theorem','No Gaussian target/covariance/TV/error/precision transport','No operational Borel/adaptive/seed/transcript/output or deterministic/expected/bit cost adapter','No Krylov/moment or either main lower-bound completion','No source/frontier/Registry/shared-site mutation, remote/stabilization or whole-Goal completion','Root/full site/actual browser and later purification/ExpositionSeal remain separate'],
}
(out/'normal-verified-transition-evidence.json').write_bytes(J(evidence))
# Exactly one real normal API transition; no manual ledger append and no state-repair loop.
astis_advance.transition_advance(own,'VERIFIED',worker_id='/root/reader_361904',modes=('source','Lean','reader'),evidence=evidence)
after=ledger.read_bytes();assert after.startswith(before);suffix=after[len(before):];rows=[json.loads(x) for x in suffix.splitlines() if x.strip()];assert len(rows)==1
row=rows[0];assert row['advance_id']==own and row['from_state']=='PROVED_LOCAL' and row['to_state']=='VERIFIED' and row['worker_id']=='/root/reader_361904'
state_after=astis_advance.current_advances();assert state_after[own]['state']=='VERIFIED' and state_after[own]['owner_id']==state[own]['owner_id']=='huanjian_gc_20261107_fixed_spectrum_query'
current=json.dumps({k:v for k,v in state_after.items() if k!=own},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert current==foreign
(out/'normal-verified-event.exact.jsonl.gz').write_bytes(gzip.compress(suffix,mtime=0))
receipt={'status':'PASS_REAL_NORMAL_API_TRANSITION','API':'tools.astis_advance.transition_advance','call_count':1,'advance_id':own,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','actor_and_verifier':'/root/reader_361904','proof_owner_unchanged':state_after[own]['owner_id'],'verified_commit':evidence['verified_commit'],'accepted_bytes_in_verified_commit':False,'accepted_audit_raw_sha256':H(candidate),'source_review_run_sha256':a['source_review']['review_run_sha256'],'before_ledger_bytes':len(before),'before_ledger_sha256':H(before),'after_ledger_bytes':len(after),'after_ledger_sha256':H(after),'old_ledger_prefix_preserved':True,'exactly_one_event_appended':True,'event_raw_sha256':H(suffix),'event':row,'foreign_states_unchanged':len(state_after)-1,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'normal-verified-transition-receipt.json').write_bytes(J(receipt))
print(json.dumps({k:v for k,v in receipt.items() if k!='event'},indent=2))
