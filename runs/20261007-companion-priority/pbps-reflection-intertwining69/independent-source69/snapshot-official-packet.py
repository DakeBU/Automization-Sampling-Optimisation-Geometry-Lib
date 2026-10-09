import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent;repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
m=json.loads((out/'current-input-manifest.json').read_bytes())
def pin(n,p,role):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 m['inputs'].append(dict(name=n,original_path=str(p),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)));return b
p=pin('official.source.0.reviewer-packet.RAW.json',run/'source.0.reviewer-packet.json','canonical-current-anti-anchored-source-review-packet; first-seen-after-own-source-seven-slots')
pin('official.reader-api-overlay.application.RAW.json',run/'reader-api-overlay69/application.json','root-exact-two-metadata-fields-application; no-mathematical-repair')
for n,pth,role in [
 ('final.lesson.RAW.json',repo/'website/content/declaration_lessons/pbps-actual-reflection-intertwining.json','post-approved-reader-API-metadata-only-overlay-current-lesson'),
 ('final.publication.RAW.json',repo/'website/content/publications/pbps-actual-reflection-intertwining.json','current-attributed-publication'),
 ('final.frontier-cell.RAW.json',repo/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json','current-bounded-cell'),
 ('final.publication-freeze69.RAW.json',run/'publication-freeze69.json','current-publication-freeze-exact-native-bytes')]:
 pin(n,pth,role)
m['count']=len(m['inputs']);m['reviewer_packet_received']=True;m['blind_reconstruction_received']=True;m['official_packet_first_seen_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
put('current-input-manifest.json',m)
d=json.loads(p)
put('official-packet-structure.json',dict(schema='source69-official-packet-first-read-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),RAW_bytes=len(p),RAW_sha256=sha(p),top_level_keys=list(d),canonical_packet_SHA_expected_from_parent='98e9a39c9f7eafea5a7a6660c162631fed010e9533ef2ab6debbdcdcd6405fc6'))
print(json.dumps(dict(actual_pid=os.getpid(),RAW_bytes=len(p),RAW_sha256=sha(p),keys=list(d),input_count=m['count']),sort_keys=True))
