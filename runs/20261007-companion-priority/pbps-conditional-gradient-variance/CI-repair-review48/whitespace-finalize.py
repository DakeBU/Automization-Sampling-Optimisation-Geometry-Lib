import json,hashlib,datetime,subprocess
from pathlib import Path
r=Path('E:/Samplinglib');out=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance/CI-repair-review48'
def H(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text('utf-8'))
def encode(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=Path(p).read_bytes();return {'path':str(Path(p).relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(b.replace(b'\r\n',b'\n'))}
review=read(out/'whitespace.review.json');assert review['verdict']=='ACCEPTED_NARROW_EXTERNAL_RAW_DIAGNOSTIC_EXCLUSION_ONLY';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()==review['base_commit']
for name,expected in [('review.json','27667e273a02c0396371d0a9d5eeba53d0a3fc0a221a83f3822986086d09f6dc'),('reviewer.ci.lease.json','91fab398ab25268f86f658b19601f71a15be77474afef4fb1dc4b8cab0631131')]:assert bind(out/name)['raw_sha256']==expected
outputs=[bind(p)for p in sorted(out.iterdir())if p.is_file()and(p.name.startswith('whitespace')or p.name=='reviewer.ci.whitespace.lease.open.raw.snapshot.json')and p.name not in ['whitespace.run.json']]
packet={'actor':'picard_commit_verifier_43','base_commit':review['base_commit'],'verdict':review['verdict'],'outputs':outputs,'original_review_immutable':bind(out/'review.json'),'compiler':'NOT_STARTED_CLOSED','run_hash_recipe':'SHA256 UTF8 json.dumps whole-minus-run_sha256, ensure_ascii=False, sort_keys=True, separators=(comma,colon)','all_roles_after_final_write':'CLOSED'};packet['run_sha256']=H(json.dumps(packet,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());(out/'whitespace.run.json').write_bytes(encode(packet));reviewbinding=bind(out/'whitespace.review.json');runbinding=bind(out/'whitespace.run.json')
p=out/'reviewer.ci.whitespace.lease.json';lease=read(p);assert lease['status']=='OPEN';lease.update({'status':'CLOSED','read':'CLOSED','Python':'CLOSED','write':'CLOSED','compiler':'NOT_STARTED_CLOSED','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':0,'verdict':review['verdict'],'no_original_or_canonical_writes':True});data=encode(lease)
# Final filesystem operation: actual successor lease closure.
p.write_bytes(data)
print(json.dumps({'review':reviewbinding,'run':runbinding,'run_sha256':packet['run_sha256'],'closedlease_raw_LF_sha256':H(data),'all_actual_roles':'CLOSED','compiler':'NOT_STARTED_CLOSED','fresh_checks':[2,0],'external_blobs':2,'external_rows':29}))
