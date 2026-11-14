from pathlib import Path
import sys,json,copy,gzip,subprocess
sys.dont_write_bytecode=True
sys.path.insert(0,'.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact,put_new,sha
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence')
S=Path('.astis/semantic-neutral-20261110/z_src_2f8a71')
D=W/'independent-native-reader-6c82f1'
candidate='eed870294de059136900110ade59b4a292a126ad'
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==candidate
nm=D/'manifest.json';nr=D/'freeze.receipt.json'
assert sha(nm.read_bytes())=='ece9f8b0d701ee77fe68a1c758e1d479200c494f03368e5dbd8e578d0f859af5'
assert sha(nr.read_bytes())=='72536a68929170162a582e39f3cdadec991b564ebc3dbae623e0bf4e1b103406'
m=json.loads(nm.read_bytes());assert m['candidate']==candidate and not m['symlinks']
files={}
for r in m['raw_files']:
    p=D/r['path'];b=p.read_bytes()
    assert not p.is_symlink() and len(b)==r['bytes'] and sha(b)==r['sha256'] and p.stat().st_mode&0o777==0o444,p
    files[r['path']]=b
for n in ['manifest.json','freeze.receipt.json']:
    p=D/n;assert p.stat().st_mode&0o777==0o444;files[n]=p.read_bytes()
assert set(files)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and not p.is_symlink()}
j=json.loads(files['judgment.json']);assert j['candidate']==candidate and j['native_judgment']=='PASS within exact candidate scope'
assert j['static_judgment']=='QUALIFIED; HOLD complete reader-neighbor source/download acceptance for private T'
native=archive_exact(files,E/'independent-native-fullmodule-static.lossless-file-bytes.tar.gz')
native.update({'original_actor':'/root/zeroquery_native_reader_6c82f1','checked_mathematical_commit':candidate,'original_freeze_sha256':sha(nr.read_bytes()),'all256_original_raw_files_plus_manifest_and_receipt_byte_exact':True,'fresh_compiler_artifacts_included_as_actual_original_bytes':True,'dependency_symlinks':[],'actual_judgment_preserved':j,'root_diagnostic':'Initial bounded readback guessed freeze_receipt.json; actual original name is freeze.receipt.json. The failed read did not mutate or replay anything. Exact original inventory is authoritative.'})
put_new(E/'independent-native-fullmodule-static.archive-manifest.json',dump(native))
put_new(E/'independent-native-judgement.raw.json',files['judgment.json'])
phases=[('phase1','d8e1def94411192058922b64b4b7cb61e1c26ceb3ade1816b69fce2ecd9788ce','ef13349dd0f6b894a6ba171184c65f19edb89b1e42e394ef7d0bd6d550320653'),('phase2','0ca53710dee6acfe75295f075b7465fc5483b2fa57e6968ed0f59657458ab6a6','fe71e48e45deac24afca70fdc1050e65ab80639093d26e547bac7cd17dd61ceb'),('phase3','ccf7b16ec6988d0cbfcb2b80ecad72758de126a52df81708d83c44425c2f9529','68c4da2106048fab40a0cbff4c78f42a4011508d3b1e881de59a0753e84e6070')]
covered=set()
for ph,mh,rh in phases:
    d=S/ph;mp=d/'manifest.json';rp=d/'receipt.json'
    assert sha(mp.read_bytes())==mh and sha(rp.read_bytes())==rh
    for p in [mp,rp]:
        assert p.stat().st_mode&0o777==0o444;covered.add(str(p.relative_to(S)))
    for r in json.loads(mp.read_bytes())['payload_files']:
        p=d/r['path'];b=p.read_bytes()
        assert not p.is_symlink() and sha(b)==r['sha256'] and len(b)==r['bytes'] and p.stat().st_mode&0o777==0o444,p
        covered.add(str(p.relative_to(S)))
sourcefiles={str(p.relative_to(S)):p.read_bytes() for p in S.rglob('*') if p.is_file() and not p.is_symlink()}
assert covered==set(sourcefiles),(covered^set(sourcefiles))
proposalraw=sourcefiles['phase3/source_review_proposal.json']
assert sha(proposalraw)=='d0ad989c10877211b93a73cecb6be3714fc3ffb15ecb442577f813a98ded6ac6'
proposal=json.loads(proposalraw);fields={'state','verdict','semantic_slots','deltas','source_review'}
assert set(proposal)==fields and proposal['state']=='source-reviewed'
assert proposal['source_review']['reviewer']=='/root/zeroquery_fresh_source_2f8a71' and proposal['source_review']['state']=='accepted'
assert proposal['source_review']['review_run_sha256']=='e0a9a484aed67e87ebdf7c80efb7818c9b8ba712a6dd337e9fb34144eef2838d'
assert not any(x['severity']=='blocking' for x in proposal['deltas'])
source=archive_exact(sourcefiles,E/'independent-full-source-all-phases.lossless-file-bytes.tar.gz')
source.update({'original_verifier_actor':'/root/zeroquery_fresh_source_2f8a71','checked_mathematical_commit':candidate,'all3_independent_phase_freezes_exact':True,'qualified_exposure_and_delivery_limits_retained':True})
put_new(E/'independent-full-source-all-phases.archive-manifest.json',dump(source))
put_new(E/'independent-source-five-field-proposal.raw.json',proposalraw)
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json')
oldraw=ap.read_bytes();old=json.loads(oldraw)
assert old['state']=='blind-reconstructed' and old['source_review']=={'state':'pending'}
assert old['publication_binding_sha256']=='6191ef91c7d9b320585d3cf7a2385ad81b9515930d6e5b2e1106773be58e58b2'
put_new(E/'audit-before-independent-full-source-application.raw.json',oldraw)
new=copy.deepcopy(old)
for k in fields:new[k]=proposal[k]
assert {k:v for k,v in old.items() if k not in fields}=={k:v for k,v in new.items() if k not in fields}
ap.write_bytes(dump(new))
put_new(E/'independent-source-proposal-exact-application.json',dump({'source_proposal_sha256':sha(proposalraw),'source_phase3_freeze_sha256':phases[2][2],'native_freeze_sha256':native['original_freeze_sha256'],'mathematical_checked_commit':candidate,'changed_audit_fields':sorted(fields),'all_other_audit_values_exact':True,'all5_original_proposal_values_exact':True,'root_invented_semantic_verdict':False,'normal_sourceV_API_calls':0,'static_reader_neighbor_HOLD_preserved':True,'no_global_browser_purification_or_Goal_credit':True}))
cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-zero-query-separation.json')
raw=cp.read_bytes();c=json.loads(raw);assert c['status']=='proved_locally'
put_new(E/'frontier-before-accepted-independent-reviews.raw.json.gz',gzip.compress(raw,mtime=0))
c['evidence'].update({'independent_verification':'Original fresh source-first/selective/full-code reviewer2f8a71 accepted the bounded signed-event auxiliary and private common-law obstruction; native reader6c82f1 independently passed strict fresh P/T/kernel, all38 locators and six exact code folds at eed87029. Static reader is QUALIFIED with HOLD on privateT adjacent source/download actions. Normal sourceV is pending; no global/browser/purification or Goal acceptance.','independent_source_archive':source,'independent_native_static_archive':native,'reader_integration_obligation':'Retain actual static HOLD: step6 fullT has no adjacent own source/download actions; its source link is in later Sources fold and exported T source HTML has no download action. Repair and independently accept the actual reader under the authorized integration lease, then verify desktop/mobile, neighboring Lean/source-index/graph. Artifact existence alone gives no link-neighbor credit.'})
c['source_detail_audit']['gap']='Selected actual two-Gaussian signed gap and arbitrary-common-probability-law obstruction have bounded source/code/native acceptance. Actual Borel seed/stopping/output/common-law and source precision-class/accuracy adapters, T>=1/Q_G and both main lower bounds remain open. Different spectra prevent disclosed-spectrum transfer. Static privateT source/download adjacency HOLD and all global integration/rendered delivery/purification obligations remain open.'
cp.write_bytes(dump(c))
put_new(E/'latest-main-original-owner-after-mathematical-candidate.json',(W/'latest-main-owner-after-mathematical-candidate.json').read_bytes())
print(json.dumps({'source_files_byte_exact':len(sourcefiles),'source_archive_sha256':source['sha256'],'native_files_byte_exact':native['file_count'],'native_archive_sha256':native['sha256'],'audit_state':new['state'],'static_reader_neighbor':'HOLD preserved','root_sourceV_API_calls':0}))
