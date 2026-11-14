from pathlib import Path
import hashlib,json,sys,subprocess,copy,tarfile,gzip
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W=Path('.astis/huanjian-gc-fixed-spectrum-exact-means-20261110');R=Path('.astis/semantic-neutral-20261110/src_a74f20');E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-exact-means-semantic-evidence')
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p):p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def put(p,b):assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='d823dddd8b7f203af3191b94ba2eb763fc0edc9b'
assert not subprocess.check_output(['git','diff','HEAD','--name-only']).strip()
expected={'phase1':'5afcacc0ea702615faed565f8b99ed770d712c9839c1bedde12f9bd7ca4591db','phase2':'74b7234b3956027167581a37b3f8ddbf59ca62cfdf2a962490d9a548fa31a7ad','phase3':'4932582ef2ff7976624eaf2672910a11aeb447292b1a72e1f84e9b63a67ff621'}
files=set()
for phase,h in expected.items():
 f=R/phase/'freeze-manifest.json';assert sha(f.read_bytes())==h;files.add(f)
 for row in json.loads(f.read_bytes())['files']:
  p=Path(row['path']);assert sha(p.read_bytes())==row['sha256'] and p.stat().st_size==row['bytes'],p;files.add(p)
proposal=R/'phase3/canonical-audit-four-field-proposal.json';q=json.loads(proposal.read_bytes());assert sha(proposal.read_bytes())=='bdc2ebf1fee38b132e7eb8b87cb377886807ef229ebc9e3c45981162aad2928a';assert q['source_review']['static_reader_status']=='HOLD_PRIVATE_CONSUMER_EXACT_ADJACENT_LEAN'
lesson=Path('website/content/declaration_lessons/huanjian-fixed-spectrum-exact-means.json');candidate=W/'lesson-exact-step-code-candidate-v2.json';assert sha(lesson.read_bytes())=='791449da588b8dc902d10229b42d970bb2ce83ae75e70e8b906700acbc262d91';assert sha(candidate.read_bytes())=='4252152a1df92598351878fe7a0089feebd400de30f8398f7752b19d958c69d6'
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-exact-means.json');old_a=ap.read_bytes();a=json.loads(old_a);assert a['state']=='blind-reconstructed' and a['source_review']=={'state':'pending'}
old_c=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-exact-means.json').read_bytes();c=json.loads(old_c);assert c['status']=='proved_locally'
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
# Select only frozen real files, never dereference the large dependency-overlay symlink forest.
archive=E/'fresh-source-reader-a74f20/source-first-phases-and-original-reader-HOLD.frozen-files.lossless.tar.gz';archive.parent.mkdir(parents=True,exist_ok=True);assert not archive.exists()
with tarfile.open(archive,'w:gz',dereference=True) as t:
 for p in sorted(files):t.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for p in sorted(files):assert t.extractfile(str(p)).read()==p.read_bytes()
put(archive.parent/'original-frozen-files-manifest.json',dump({'archive':ref(archive),'files':[ref(p) for p in sorted(files)],'scope':'All phase1–3 frozen files selected exactly; dependency overlay symlinks excluded, dependency cache bytes bound by independent hashes. Original source/native acceptance and reader HOLD preserved, no normalV.'}))
for phase,names in {'phase1':['freeze-manifest.json','source-cognition.md','read-exposure.json'],'phase2':['freeze-manifest.json','independent-statement-review.md','semantic-slots-deltas-verdict.json'],'phase3':['freeze-manifest.json','whole-module-source-native-reader-review.md','canonical-audit-four-field-proposal.json','review-run.json','static-reader-checks.json']}.items():
 for n in names:put(E/'fresh-source-reader-a74f20'/phase/n,(R/phase/n).read_bytes())
repair=E/'exact-reader-repair-v2'
for f in [candidate,W/'exact-step-reader-repair-v2-manifest.json',W/'reader-repair-candidate-v3-render/actual-static-check.json',W/'check_reader_repair_candidate_v2.py',W/'retained-reader-repair-static-tool-v1.py',W/'retained-reader-repair-static-tool-v2.py']:
 put(repair/f.name,f.read_bytes())
for p in sorted(Path('.astis/huanjian-resume-20261103').glob('*-exact-means-unapplied-exact-step-reader-repair-v2-static-check*.receipt.json')):
 d=json.loads(p.read_bytes());b=Path(d['log']).read_bytes();assert sha(b)==d['log_sha256'];put(repair/'actual-root-static-checks'/p.name,p.read_bytes());put(repair/'actual-root-static-checks'/(Path(d['log']).name+'.gz'),gzip.compress(b,mtime=0))
put(repair/'canonical-audit-before-lesson-rebinding.raw.json',old_a);put(repair/'frontier-before-lesson-rebinding.raw.json',old_c)
lesson.write_bytes(candidate.read_bytes())
preserved={k:copy.deepcopy(a[k]) for k in a if k not in ['publication_binding_sha256','publication_context']}
pub.inputs.cache_clear();pub.load.cache_clear()
item=pub.load()
# Resolve the exact already-authored public binding rather than create any new node.
# binding helpers are stable; selecting raw item avoids changing its source fields.
raw=json.loads(Path('website/content/publications/huanjian-fixed-spectrum-exact-means.json').read_bytes());it=raw['items'][0];binding=it['bindings'][0]
a['publication_binding_sha256']=pub.binding_digest(it,binding);a['publication_context']=pub.review_context(it,binding)
assert all(a[k]==v for k,v in preserved.items())
assert rt.decoder_packet(a)['packet_sha256']=='01239c09b2aef4c0e8f960f5500fcf8468190f8c7905b18b1ec824268cda3411'
ap.write_bytes(dump(a));pub.check_advance([a['lean']['declaration']],reviewed=False)
packet=rt.semantic_reviewer_packet(a);put(E/'fresh-source-reviewer-packet-v2-exact-reader-code.json',dump(packet))
c['evidence']['publication_binding_sha256']=a['publication_binding_sha256'];c['evidence']['original_independent_reader_HOLD']=ref(E/'fresh-source-reader-a74f20/phase3/static-reader-checks.json');c['evidence']['exact_reader_repair_v2']='Own lesson now has exact per-step code and full Test module source context; original HOLD retained, exact successor review pending. No sourceV.'
Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-exact-means.json').write_bytes(dump(c))
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
put(repair/'actual-own-lesson-rebinding.json',dump({'scope':'Exact lesson-only display repair and pending audit binding refresh, no source/Lean/statement/reconstruction/repair/verdict change or normalAPI. Original independent source/native pass and readerHOLD not applied as overall acceptance.','old_binding_sha256':q['source_review']['publication_binding_sha256'],'new_binding_sha256':a['publication_binding_sha256'],'new_canonical_reviewer_packet_sha256':packet['packet_sha256'],'new_packet_raw':ref(E/'fresh-source-reviewer-packet-v2-exact-reader-code.json'),'mathematical_checked_commit':'d823dddd8b7f203af3191b94ba2eb763fc0edc9b','wholemodule_Lean_bytes_unchanged':True,'anonymous_decoder_packet_unchanged':True,'normal_state':'PROVED_LOCAL'}))
print(json.dumps({'new_binding':a['publication_binding_sha256'],'new_reviewer_packet_canonical_sha256':packet['packet_sha256'],'original_reader_HOLD_retained':True,'sourceV_or_STAB':False}))
