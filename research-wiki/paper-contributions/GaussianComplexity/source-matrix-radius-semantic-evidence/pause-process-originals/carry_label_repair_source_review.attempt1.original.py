from pathlib import Path
import json,hashlib,subprocess,sys
sys.path.insert(0,'tools')
import astis_publication as pub
import astis_frontier_cells as frontiers
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/radius_src_73c1/label_repair_v2')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='c4d031f237fa0e16fbba16987ca6b34c7f3dfd98'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
mf=R/'portable_incremental_manifest.label-repair.v2.json';assert sha(mf.read_bytes())=='8731bc61ae644fbc90b9aca71d759791a1fa93017cf5909375f55811f7e3c800'
m=json.loads(mf.read_bytes());dest=E/'source-review/radius_src_73c1/label-repair-v2/originals'
for n,x in m['files'].items():
    b=(R/n).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['raw_sha256'];create(dest/n,b)
for n in ['portable_incremental_manifest.label-repair.v2.json','closure_receipt.label-repair.v2.json','raw_commands.jsonl']:create(dest/n,(R/n).read_bytes())
a=json.loads(A.read_bytes());t=json.loads((W/'private-consumer-audit.label-repair.reconstructed.v2.json').read_bytes())
for audit,n,h in [(a,'P-canonical-audit-overlay.label-repair.v2.json','3adeafaeee5eb136aeaa425f83647549e2d0082513110d136fc369f29d56c49b'),(t,'T-private-bounded-review-overlay.label-repair.v2.json','d0431d7ac56930de0637ec9e5ccca56bbce0af1d835a860b3585a493107cd8a2')]:
    b=(R/n).read_bytes();assert sha(b)==h;o=json.loads(b);assert o['source_review']['state']=='accepted'
    assert rt.semantic_reviewer_packet(audit)['packet_sha256']==o['source_review']['reviewer_packet_sha256']
    for k in ['semantic_slots','deltas','verdict','repairs','source_review']:audit[k]=o[k]
    audit['state']='source-reviewed';audit['actual_math_commit']='4c3251454100a4591113b16ed119fdf758c876b7';audit['reader_commit']=head
    audit['independent_original_overlay']={'path':str(dest/n),'sha256':h}
a['reader_label_repair']['scope']='Single citation display label independently accepted under renewed exact context. Code, signatures, formulae and blind inputs unchanged; original failed reader build preserved.'
A.write_bytes(dump(a));private=E/'private-consumer-source-reviewed.label-repair.bounded.json';create(private,dump(t))
cell=json.loads(C.read_bytes());old=cell['evidence']['independent_source_review']
cell['evidence']['independent_source_review']={**old,'public_P_overlay':a['independent_original_overlay'],'private_T_overlay':t['independent_original_overlay'],'private_T_decision':{'file':str(private),'sha256':sha(private.read_bytes())},'public_P_run_sha256':a['source_review']['review_run_sha256'],'private_T_run_sha256':t['source_review']['review_run_sha256'],'label_repair_incremental_custody':{'file':str(dest/mf.name),'sha256':sha(mf.read_bytes()),'payload_files':len(m['files']),'closed_log_hash_receipt':str(dest/'closure_receipt.label-repair.v2.json')},'original_review_custody_retained':True}
cell['evidence']['source_label_reader_repair']['status']='Exact renewed source context independently accepted; actual repaired reader runtime acceptance separate.'
cell['reader_contract']['status']='Actual4b585 production generator failure preserved. Required citation label repaired atc4d031 and renewed P/T context independently source-reviewed; repaired generator builds. Runtime original-CSS mobile/desktop acceptance remains separate.'
C.write_bytes(dump(cell));pub.check_advance([a['lean']['declaration']],reviewed=True)
assert not frontiers.validate_cells(frontiers.load_cells())
paths=[A,C,private,*[p for p in sorted(dest.rglob('*')) if p.is_file()]]
spec=W/'label-repair-source-review-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','commit','--quiet','-m','Carry fresh source acceptance of exact Gaussian citation repair'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'source_review_carrier_commit':commit,'reader_candidate_commit':head,'current_publication_binding_sha256':a['publication_binding_sha256'],'exact_incremental_original_payload_files':len(m['files']),'extra_closed_custody_files':3,'publication_reviewed_admission':'passed','root_fidelity_verdicts':0,'ledger_calls':0}
create(W/'actual-label-repair-source-review-carrier.json',dump(result));print(json.dumps(result))
