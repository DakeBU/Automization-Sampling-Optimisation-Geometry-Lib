"""Carry original independent decisions verbatim; ROOT supplies no fidelity verdict."""
from pathlib import Path
import json,hashlib,subprocess,sys
sys.path.insert(0,'tools')
import astis_publication as pub
import astis_frontier_cells as frontiers
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/radius_src_73c1')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='4b58558a6003444af9964fba077e74bf5e63052d'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
mf=R/'portable_custody_manifest.v3.json';assert sha(mf.read_bytes())=='f4c9040dee309c0df07eaf7d33f47ba5398624b1d57980968eebb4d783dead39'
m=json.loads(mf.read_bytes());assert len(m['files'])==54
dest=E/'source-review/radius_src_73c1/originals'
for n,x in m['files'].items():
    p=R/n;b=p.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['raw_sha256']
    create(dest/n,b)
for n in ['portable_custody_manifest.v3.json','raw_commands.jsonl']:create(dest/n,(R/n).read_bytes())
keys=['semantic_slots','deltas','verdict','repairs','source_review']
a=json.loads(A.read_bytes());t=json.loads((W/'private-consumer-audit.reconstructed.v1.json').read_bytes())
for audit,n,expected_hash in [(a,'P-canonical-audit-overlay.v2.json','01baa81c4f8631acff5db69c4def95916a83b8f0930924f4ed9b75a8bb6d9dda'),(t,'T-private-bounded-review-overlay.v2.json','bf78d13d959360a25f2037f3ebd05ac9ac34d03ddef8c20c9d367207cfc7eb2c')]:
    b=(R/n).read_bytes();assert sha(b)==expected_hash;o=json.loads(b)
    assert o['source_review']['state']=='accepted'
    assert o['source_review']['reviewer_packet_sha256']==rt.semantic_reviewer_packet(audit)['packet_sha256']
    assert o['source_review']['reviewer'] not in [audit['lean']['formalizer'],audit['reconstruction']['decoder']]
    assert set(o['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
    for k in keys:audit[k]=o[k]
    audit['state']='source-reviewed'
    audit['actual_math_commit']='4c3251454100a4591113b16ed119fdf758c876b7';audit['reader_commit']=head
    audit['independent_original_overlay']={'path':str(dest/n),'sha256':expected_hash}
A.write_bytes(dump(a));create(E/'private-consumer-source-reviewed.bounded.json',dump(t))
supp=R/'reuse_supplement_v1/independent_assessment.v1.json'
assert sha(supp.read_bytes())=='1d31c6a30575892b6e89a9a23e7b83ae3df642f189169ec844df2302e61dd363'
cell=json.loads(C.read_bytes())
cell['evidence']['independent_source_review']={'public_P_overlay':a['independent_original_overlay'],'private_T_overlay':t['independent_original_overlay'],'private_T_decision':{'file':str(E/'private-consumer-source-reviewed.bounded.json'),'sha256':sha((E/'private-consumer-source-reviewed.bounded.json').read_bytes())},'original_custody_manifest':{'file':str(dest/mf.name),'sha256':sha(mf.read_bytes()),'payload_files':54,'extra_closed_raw_log_preserved':True},'public_P_run_sha256':a['source_review']['review_run_sha256'],'private_T_run_sha256':t['source_review']['review_run_sha256'],'source_review_scope':'Complete actual P/T code, raw source, seven slots, candidate author/context, mapping and extra reuse supplement. Native/browser/site/globalintegration acceptance separate.'}
cell['conceptual_mirror_audit']={'status':'none-found','discovery_ids':[],'authored_audit':str(E/'conceptual-mirror-audit.authored-v1.json'),'independent_reuse_supplement':{'file':str(dest/'reuse_supplement_v1/independent_assessment.v1.json'),'sha256':sha(supp.read_bytes())}}
cell['statement_seal']['status']='EXACT_UNCHANGED_SEALED_P_T_TYPES;LOCAL_COMPILED;INDEPENDENT_SOURCE_ACCEPTED;NATIVE_READER_SEPARATE'
cell['reader_contract']['status']='Complete formula proof and all226P+95privateT lines in6folds independently source-reviewed. Runtime reader and serialized production delivery separate.'
cell['graph_contribution']['visual_review']='Actual3 P parents and private T→P recorded; source-code map spans accepted independently. Focused runtime graph and global integrated graph pending.'
cell['learning_contract']['reader_backpressure']['assumptions_preserved']=True
cell['reuse_plan']['reused_declarations']=json.loads((E/'local-math-candidate.json').read_bytes())['canonical_ASTIS_P_parents']
cell['reuse_plan']['actual_private_consumer_parents']=[a['lean']['declaration']]
C.write_bytes(dump(cell))
pub.check_advance([a['lean']['declaration']],reviewed=True)
errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
create(E/'source-review/radius_src_73c1/transfer.json',dump({'source_candidate_commit':head,'independent_original_payload_files':54,'portable_manifest_plus_closed_raw_log_files':2,'source_original_paths_and_hashes_preserved':True,'canonical_fields_copied_verbatim':keys,'schema_correction_authored_by_reviewer':str(dest/'canonical_schema_serialization_envelope.v1.json'),'ROOT_fidelity_verdicts':0,'ledger_calls':0}))
paths=[A,C,*[p for p in sorted((E/'source-review').rglob('*')) if p.is_file()],E/'private-consumer-source-reviewed.bounded.json']
spec=W/'source-review-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(A),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent Gaussian radius source and whole-module reviews'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'source_review_carrier_commit':commit,'reader_candidate_commit':head,'exact_originals':56,'publication_check_reviewed':'passed','whole_frontier_schema':'passed','ledger_mutations':0,'ROOT_fidelity_verdicts':0}
create(W/'actual-independent-source-carrier-commit.json',dump(result));print(json.dumps(result))
