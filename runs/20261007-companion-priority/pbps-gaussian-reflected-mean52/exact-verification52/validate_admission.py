import pathlib,json,hashlib,sys,subprocess
ROOT=pathlib.Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52';OUT=P/'exact-verification52'
sys.path.insert(0,str(ROOT))
from tools import astis_publication
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=read(P/'source.0.review.json');rows=[];changed=[]
mapping={r['input_path'].replace('\\','/'):r['snapshot'] for r in s['raw_snapshot_bindings']}
assert len(s['input_artifacts'])==len(mapping)==347
for e in s['input_artifacts']:
 p=pathlib.Path(e['path']);snap=mapping[p.as_posix()];a=pin(pathlib.Path(snap['path']))
 assert all(a[k]==snap[k]==e[k] for k in ['raw_sha256','lf_sha256','bytes'])
 current=pin(p);row={'original_input':e,'preserved_raw_snapshot':a,'current':current,'current_matches_original':all(current[k]==e[k] for k in ['raw_sha256','lf_sha256','bytes'])}
 if not row['current_matches_original']:
  assert current['path'] in ['research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianReflectedMean.json','research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json']
  old=read(pathlib.Path(snap['path']));new=read(p)
  if current['path'].endswith('GaussianReflectedMean.json'):
   if 'audits' in old:old=old['audits'][0]
   if 'audits' in new:new=new['audits'][0]
   for k in ['source','lean','reconstruction','publication_binding_sha256','publication_context']:assert old[k]==new[k],'mathematical audit data changed '+k
  row['changed_top_level_fields']=[k for k in set(old)|set(new) if old.get(k)!=new.get(k)]
  row['reason']='Source admission/proved-local status updates; all original source-review raw inputs preserved in the exact existing snapshots. No restoration, raw pin rewrite or mathematical input mutation.'
  changed.append(row)
 rows.append(row)
audit=read(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianReflectedMean.json')
if 'audits' in audit:audit=audit['audits'][0]
item=next(i for i in astis_publication.load() if i['id']=='gaussian-reflected-mean');binding=item['bindings'][0]
current=astis_publication.review_context(item,binding);digest=astis_publication.binding_digest(item,binding)
assert digest==audit['publication_binding_sha256']==s['publication_binding_sha256']
assert current==audit['publication_context']==s['current_review_context']
assert audit['source_review']['state']=='accepted' and audit['state']=='accepted' and audit['verdict']=='equivalent-after-elaboration'
assert audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==s['reviewer_packet_sha256']
assert audit['source_review']['reviewer']=='phase_source_reviewer_20261005' and audit['lean']['formalizer']=='root-samplinglib-writer'
assert len({audit['source_review']['reviewer'],audit['lean']['formalizer'],audit['reconstruction']['decoder'],'whole_math52'})==4
assert audit['reconstruction']['source_text_visible'] is False
write(OUT/'source-admission-bindings.json',{'strict_source_review_original_inputs':347,'current_unchanged':347-len(changed),'changed_admission_inputs':changed,'inputs':rows,'audit':pin(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianReflectedMean.json'),'publication_binding_sha256':digest,'current_context_exact_match':True,'source_review':pin(P/'source.0.review.json'),'source_verdict':s['verdict'],'source_reviewer':s['reviewer'],'strict_source_identity_blindness_claimed':False,'note':'Anonymous statement/source-text-blind decoder has disclosed inherited general source identities; accepted source0 documents the exposure. No new strict-blindness claim.'})
print(json.dumps({'source_originals':347,'changed_admission_inputs':[(r['current']['path'],r['changed_top_level_fields']) for r in changed],'binding':digest,'context_exact':True}))
