from pathlib import Path
import hashlib,json,subprocess,sys,tarfile,re,zipfile,io
sys.dont_write_bytecode=True;sys.path.insert(0,'tools');import astis_advance as adv
W=Path('.astis/huanjian-gc-fixed-spectrum-exact-means-20261110');R=Path('.astis/semantic-neutral-20261110/src_a74f20/normal-sourceV-runtime');E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-exact-means-semantic-evidence/actual-source-V');C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-exact-means.json');L=Path('runs/substantive_advances.jsonl');ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumExactMeans'
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p):return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def put(p,b):assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='6eca29f8704a024f9bbf2de986d8aa9fbe8c6129'
assert sha((R/'freeze-manifest.json').read_bytes())=='a3c5d1eefe696c782342ae6d819d7a38c9326ad694451e505efa5983b3788762'
files={R/'freeze-manifest.json'}
for row in json.loads((R/'freeze-manifest.json').read_bytes())['files']:
 p=Path(row['path']);assert sha(p.read_bytes())==row['sha256'] and p.stat().st_size==row['bytes'],p;files.add(p)
before=(R/'advance-ledger.before.raw.jsonl').read_bytes();append=(R/'ACTUAL-normal-V-append.raw.jsonl').read_bytes();after=L.read_bytes();assert after==before+append and len(append.splitlines())==1
assert sha(append)=='fc80cf92c691dae797dd34b903f20175259eb90d00f566bda1a0406306bdff20'
st=adv._replay_advances([json.loads(x) for x in after.splitlines()]);ev=json.loads((R/'ACTUAL-V-evidence.raw.json').read_bytes());inventory=json.loads((R/'ACTUAL-V-evidence-key-inventory.json').read_bytes())
assert st[ADV]['state']=='VERIFIED' and st[ADV]['latest_evidence']==ev and ev['verifier_id']=='/root/source_reader_a74f20' and ev['verified_commit']=='6eca29f8704a024f9bbf2de986d8aa9fbe8c6129'
assert set(ev)==set(inventory['actual_keys']) and len(ev)==inventory['actual_key_count']
assert sha((R/'ACTUAL-V-evidence.canonical.json').read_bytes())==inventory['canonical_evidence_sha256']=='9fb2c42e4d7ca6823398a512d6b120b1a86c3838e0991891e9b695ee2b997279'
for k,v in ev.items():assert sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==inventory['per_value_canonical_sha256'][k]
baseline=json.loads((W/'preproof-baseline.json').read_bytes());assert {k:v for k,v in st.items() if k!=ADV}==baseline['all_current_SAU_states']
for p,h in baseline['all_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
for p,h in baseline['protected_shared_hashes'].items():assert sha(Path(p).read_bytes())==h,p
assert C.read_bytes()==(R/'own-frontier.after.raw.json').read_bytes();assert sha(C.read_bytes())=='79c703a9281efc98d5430a54f8adccbce08d719b66d052c2d9b717bc647db3b8'
c=json.loads(C.read_bytes());assert c['status']=='independently_verified' and isinstance(c['evidence']['independent_verification'],str)
for p in files:
 b=p.read_bytes();assert not re.search(rb'wxid_[a-z0-9]{8,}',b),p
 if p.suffix=='.zip':
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for n in z.namelist():assert not re.search(rb'wxid_[a-z0-9]{8,}',z.read(n)),(p,n)
archive=E/'independent-normal-sourceV-and-own-projection.frozen-files.lossless.tar.gz';archive.parent.mkdir(parents=True,exist_ok=True);assert not archive.exists()
with tarfile.open(archive,'w:gz',dereference=True) as t:
 for p in sorted(files):t.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for p in files:assert t.extractfile(str(p)).read()==p.read_bytes()
for n in ['freeze-manifest.json','NORMAL-SOURCE-V-REPORT.md','transition-return.json','transition.stdout','transition.stderr','ACTUAL-normal-V-append.raw.jsonl','ACTUAL-normal-V-event.pretty.json','ACTUAL-V-evidence.raw.json','ACTUAL-V-evidence.pretty.json','ACTUAL-V-evidence.canonical.json','ACTUAL-V-evidence-key-inventory.json','original-V-evidence-preservation-contract.json','after-preservation-checks.json','own-frontier.before.raw.json','own-frontier.after.raw.json','own-frontier-exact-changed-fields.json','current-four-metadata-gates.json','post-projection-frontier.receipt.json']:
 put(E/n,(R/n).read_bytes())
put(E/'runtime-archive-manifest.json',dump({'archive':ref(archive),'files':[ref(p) for p in sorted(files)],'actual_normal_API_calls_by_independent_actor':1,'root_normalV_API_calls':0,'actual_original_evidence_field_count':len(ev),'actual_original_keys':sorted(ev),'canonical_evidence_sha256':inventory['canonical_evidence_sha256'],'per_value_canonical_sha256':inventory['per_value_canonical_sha256'],'later_release_rule':'Retain ALL actual original key/value fields; only add post_integration after actual independent integration acceptance. Do not substitute prior packet12/13field shapes.','sourceV_verified_commit':ev['verified_commit'],'actual_fresh_native_commit':'d823dddd8b7f203af3191b94ba2eb763fc0edc9b','actual_current_reader_commit':'64922804e1f7f0927e85bb6a26aeb24d06eea6f7','foreign_SAU_states_preserved':len(baseline['all_current_SAU_states']),'exact_independent_sourceV_and_frontier_bytes_carried':True,'no_new_build_STAB_global_UI_remote_purification_or_Goal_credit':True}))
put(E/'root-byte-carry-check.json',dump({'normal_state':'VERIFIED','independent_actor':ev['verifier_id'],'append_sha256':sha(append),'own_frontier_sha256':sha(C.read_bytes()),'actual_original_evidence_fields_preserved':len(ev),'no_root_API_or_projection':True,'scope':'Actual C8 closed Gaussian means/integrability plus genuine actual sign/mean-upper/normalized-bias consumer only. Fourth moments/variances, exponential bias, rotated/Krylov/adaptive/oracle/TV/precision/deterministic-cap/expected-cost/main bounds and whole Goal remain open; shared integration/website/remote/purification queued.'}))
p=Path('research-wiki/paper-contributions/GaussianComplexity/README.md');old=p.read_bytes();note='''## 2026-11-10: exact C8 Gaussian means source-verified; integration queued

The actual centered Gaussian now has both closed Fact C.8 mean formulas and norm/Q integrability, together with a genuine actual-integral consumer giving positive/upper norm mean, signed quadratic positivity and the exact normalized absolute-bias ratio. Fresh independent source/whole-module/kernel/cache checks accepted mathematical commitd823dddd. The exact reader successor64922804 supplies six literal Lean code folds and the complete Test module/source context; the original reader HOLD and all failed tool routes remain preserved. The original independent reviewer performed one normal source VERIFIED transition at accepted-review carrier6eca29f8 and projected only its own frontier. All actual15 original evidence fields are retained. See `fixed-spectrum-exact-means-semantic-evidence/actual-source-V/NORMAL-SOURCE-V-REPORT.md`.

This is local proof and independent source verification. Shared latest-main integration, actual desktop/mobile/source-index/graph acceptance, remote publication, purification and Exposition Seal remain separate and queued behind the original foreign stabilization owner. Fourth moments/variances, exponential bias estimates, rotated/Krylov/adaptive laws, exact oracle/TV/precision/deterministic worst-cap/explicit expected-cost adapters and both full main lower bounds remain open. Continue the same Goal; preserve PBPS/SPHMC and every existing queue/result.

'''.encode();p.write_bytes(note+old)
print(json.dumps({'normal_state':'VERIFIED','actual_original_evidence_fields':len(ev),'root_normalV_calls':0,'append_sha256':sha(append),'frontier_sha256':sha(C.read_bytes()),'runtime_archive_sha256':sha(archive.read_bytes()),'Goal_or_integration_complete':False}))
