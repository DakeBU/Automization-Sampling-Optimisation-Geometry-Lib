from pathlib import Path
import sys,json,copy,gzip,subprocess
sys.dont_write_bytecode=True;sys.path.insert(0,'.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact,put_new,sha
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
S=Path('.astis/semantic-neutral-20261110/tl_src_e028af');E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
candidate='8ee639d3aced826aa5b4e39fa6f8bedd3b830327'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==candidate
phase_hashes=[('','a338a45313de484509ce9dc35074ecedd769d5e88cd8bf064aa98dfa9d6fd700','b80c1b91af9b1ddb0fd0fcefd4f1d07a3c91227a00d6895caef6302bd76cef0c'),('phase2','4d4800f4c77f5a8981b4332e3f58a20c09eecbf6d1f32baf742317e3248d7ded','241fa5b417eda966ffb526916afb2a9f0378af9fa891a83038ec7fb754b10d83'),('phase3','408ac22b1923ac0a7a07e2334ba84e20a788c63c08a47694d287d228cab246b7','ede7a87a506bb7d5000dc374ba5afb8e92865dd1cfd92e0878658d1f5ec7cf4a')]
covered=set()
for phase,mh,rh in phase_hashes:
    d=S/phase;mp=d/'manifest.json';rp=d/'freeze_receipt.json';assert sha(mp.read_bytes())==mh and sha(rp.read_bytes())==rh
    covered.update([str(mp.relative_to(S)),str(rp.relative_to(S))])
    for r in json.loads(mp.read_bytes())['files']:
        p=d/r['path'];b=p.read_bytes();assert sha(b)==r['sha256'] and len(b)==r['bytes'] and p.stat().st_mode&0o777==0o444,p
        covered.add(str(p.relative_to(S)))
files={str(p.relative_to(S)):p.read_bytes() for p in S.rglob('*') if p.is_file() and not p.is_symlink()}
assert covered==set(files),(covered^set(files))
for p in S.rglob('*'):
    if p.is_file() and not p.is_symlink():assert p.stat().st_mode&0o777==0o444,p
proposalraw=files['phase3/canonical-five-field-audit-proposal.json'];assert sha(proposalraw)=='966772dade74559edba0fd73d86f3480069dbd77da22e4b423d0b33b95059ade'
proposal=json.loads(proposalraw);fields={'state','verdict','semantic_slots','deltas','source_review'};assert set(proposal)==fields and proposal['state']=='source-reviewed'
assert proposal['source_review']['reviewer']=='/root/targetlaw_fresh_source_9c7d21' and proposal['source_review']['state']=='accepted'
assert proposal['source_review']['review_run_sha256']=='f5f3b8e590c824241e7a4691208946a4da26ed51e290c35022eff09de20d7c30'
assert all(x['severity']!='blocking' for x in proposal['deltas'])
native=json.loads((E/'independent-native-fullmodule-static.archive-manifest.json').read_bytes());assert sha(Path(native['archive']).read_bytes())==native['sha256']=='22c843c570e1584a4718f03f78454280adec72493286448aa4e8d1b26942a6fb'
source=archive_exact(files,E/'independent-full-source-all-phases.lossless-file-bytes.tar.gz')
source.update({'original_verifier_actor':'/root/targetlaw_fresh_source_9c7d21','checked_mathematical_commit':candidate,'all3_independent_phase_freezes_exact':True})
put_new(E/'independent-full-source-all-phases.archive-manifest.json',dump(source))
put_new(E/'independent-source-five-field-proposal.raw.json',proposalraw)
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-target-law.json');oldraw=ap.read_bytes();old=json.loads(oldraw)
assert old['state']=='blind-reconstructed' and old['source_review']=={'state':'pending'} and old['publication_binding_sha256']=='3f8f86b61bf73df0bf7a51f989239ca2246fa5c88de21364b468816869ee86bc'
put_new(E/'audit-before-independent-full-source-application.raw.json',oldraw)
new=copy.deepcopy(old)
for k in fields:new[k]=proposal[k]
assert {k:v for k,v in old.items() if k not in fields}=={k:v for k,v in new.items() if k not in fields}
ap.write_bytes(dump(new))
put_new(E/'independent-source-proposal-exact-application.json',dump({'source_proposal_sha256':sha(proposalraw),'source_phase3_freeze_sha256':phase_hashes[2][2],'native_freeze_sha256':native['original_freeze_sha256'],'mathematical_checked_commit':candidate,'changed_audit_fields':sorted(fields),'all_other_audit_values_exact':True,'all5_original_proposal_values_exact':True,'root_invented_semantic_verdict':False,'normal_sourceV_API_calls':0,'no_global_browser_purification_or_Goal_credit':True}))
cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json');raw=cp.read_bytes();c=json.loads(raw);assert c['status']=='proved_locally'
put_new(E/'frontier-before-accepted-independent-reviews.raw.json.gz',gzip.compress(raw,mtime=0))
c['evidence'].update({'independent_verification':'Original fresh source-first/selective/full-code reviewer9c7d21 accepted bounded fixed-O law and genuine norm L1/mean auxiliary; native reader4b8e73 independently accepted fresh P/T/kernel, all29 exact locators and isolated static six literal-code steps at8ee639d3. Normal sourceV pending; no global/browser/purification or Goal acceptance.','independent_source_archive':source,'independent_native_static_archive':native})
c['source_detail_audit']['gap']='Selected fixed-O actual Gaussian transformation and private target norm L1/finite inverse-spectrum mean source/code/native/static reviewed. Full Lemma4.5, random-basis joint/conditional/adaptive laws, target pass probability, source concentration constant, operational oracle/TV/precision/cap/expected-cost adapters, both mains and global delivery/purification remain separate.'
cp.write_bytes(dump(c))
put_new(E/'latest-main-original-owner-after-mathematical-candidate.json',(W/'latest-main-original-owner-after-mathematical-candidate.json').read_bytes())
print(json.dumps({'source_files_byte_exact':len(files),'source_archive_sha256':source['sha256'],'native_files_byte_exact':native['file_count'],'audit_state':new['state'],'root_sourceV_API_calls':0}))
