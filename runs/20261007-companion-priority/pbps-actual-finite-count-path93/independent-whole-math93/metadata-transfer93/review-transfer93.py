import pathlib,json,hashlib,datetime
R=pathlib.Path('E:/Samplinglib'); O=pathlib.Path(__file__).parent
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/source-metadata-precision93/pbps-actual-finite-count-path.json'
new=R/'website/content/publications/pbps-actual-finite-count-path.json'
assert raw(old)['raw_sha256']=='661c774258fc549f58b5cac93d42a0c926ca5b5e9fcdfa75def58966063941d7'
a=json.loads(old.read_bytes()); b=json.loads(new.read_bytes())
before='Coordinate-product path sigma algebra, rank-zero and arbitrary nonnegative extended Borel tests are explicit.'
after='Coordinate-product path sigma algebra, rank-zero and arbitrary nonnegative extended tests measurable for the stated sigma algebras are explicit.'
assert a['items'][0]['bindings'][0]['assumption_deltas'][1]['lean']==before
assert b['items'][0]['bindings'][0]['assumption_deltas'][1]['lean']==after
a['items'][0]['bindings'][0]['assumption_deltas'][1]['lean']=after
assert a==b
assert old.read_bytes().replace(before.encode(),after.encode())==new.read_bytes()
prod=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-count-path.json'
assert raw(prod)['raw_sha256']=='4926508e4b11b3d4823056e1068f601d4a95b6a5e1ec495b7902cc3c4a1d2943'
assert raw(lesson)['raw_sha256']=='4247a27180d5c410ea9fe0831ec5624a7c3e3a8f26a45a356b97164538c9c4b6'
for label,p in [('old-publication',old),('new-publication',new)]: (O/(label+'.RAW.json')).write_bytes(p.read_bytes())
report={'schema_version':1,'reviewer':'independent_whole_math93','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'ACCEPT_EXACT_METADATA_ONLY_EXPOSITION_TRANSFER','scope':'Transfer previous mathematics/exposition consistency acceptance across exactly one metadata wording correction; no new source-fidelity or kernel/aggregate claim.','old_publication':raw(old),'new_publication':raw(new),'production':raw(prod),'lesson':raw(lesson),'exact_diff':{'json_pointer':'/items/0/bindings/0/assumption_deltas/1/lean','old':before,'new':after,'only_json_change':True,'only_raw_byte_change':True},'reason':'The revised classification wording now describes exactly the coordinate-product measurable test class in the checked theorem. It removes a potentially stronger Borel-topology interpretation without changing any mathematical statement, assumptions, proof or lemma explanation.','whole_review_credit':'Original whole-math decision and exposition supplement remain unchanged and applicable through this exact transfer. No kernel or whole-proof rerun was needed or performed.','necessary_fixes':[]}
save('metadata-transfer-decision93.native.json',report)
save('closed-RAW-metadata-transfer93.native.json',{'artifacts':[raw(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='closed-RAW-metadata-transfer93.native.json'],'closure':'Only this new metadata-transfer directory, excluding its own manifest. Original closed manifests were not modified.'})
print(json.dumps({'decision':raw(O/'metadata-transfer-decision93.native.json'),'manifest':raw(O/'closed-RAW-metadata-transfer93.native.json')},indent=2))
