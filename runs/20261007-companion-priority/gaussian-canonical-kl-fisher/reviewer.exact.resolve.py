from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
r=Path(r'E:/Samplinglib');run=r/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher';prefix=run.relative_to(r).as_posix();sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
sys.path.insert(0,str(r));sys.path.insert(0,str(r/"tools"));from tools import astis
b=json.loads((run/'reviewer.exact.bindings.json').read_text()); unresolved=[];resolved=[]
# Historical input hashes must point to preserved snapshots, never current admission-mutated metadata.
lookup={}
for p in run.rglob('*'):
 if p.is_file() and not p.name.startswith('reviewer.exact.'):
  raw=p.read_bytes();lookup.setdefault(sha(raw),[]).append(p)
for x in b['pins']:
 if x['status']=='PASS':continue
 expect=x['expected'];raw=next((v for k,v in expect.items() if 'raw' in k.lower()),None);matches=lookup.get(raw,[])
 if x['status']=='MISSING':
  p=run/Path(x['owner']).parent/x['path'];matches=[p] if p.exists() else matches
 valid=[]
 for p in matches:
  data=p.read_bytes();okay=all(v==sha(lf(data) if 'lf' in k.lower() else data) for k,v in expect.items())
  if okay and (x['bytes'] is None or x['bytes']==len(data)):valid.append(p.relative_to(r).as_posix())
 if valid:resolved.append({'original_pin':x,'status':'PASS_HISTORICAL_SNAPSHOT_OR_DECODER_RELATIVE_PATH','matching_snapshots':valid})
 else:unresolved.append(x)
mathroot=r/'.lake/packages/mathlib';mathsha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathroot).decode().strip();mathpins=[]
for x in b['git_blobs']:
 if x['status']=='NOT_IN_COMMIT' and x['path'].startswith('.lake/packages/mathlib/'):
  pp=x['path'].split('.lake/packages/mathlib/',1)[1];raw=(r/x['path']).read_bytes();blob=subprocess.check_output(['git','show',mathsha+':'+pp],cwd=mathroot)
  mathpins.append({'path':x['path'],'commit':mathsha,'blob_oid':subprocess.check_output(['git','rev-parse',mathsha+':'+pp],cwd=mathroot).decode().strip(),'git_raw_sha256':sha(blob),'working_raw_sha256':sha(raw),'lf_identical':lf(raw)==lf(blob)})
actualanon=(r/'.astis/decoder-43/packet0.json').read_bytes();committedanon=(run/'anonymous-decoder/packet0.json').read_bytes();assert actualanon==committedanon
# All independently recorded digest payloads are recomputed with their observed serializer; no values repaired.
digests=[]
def digest_record(path,key,payload=None):
 j=load(path); value=j[key];payload=payload if payload is not None else {k:v for k,v in j.items() if k!=key}; matches=[]
 for sort in (True,False):
  for ascii in (True,False):
   for indent in (None,2):
    for compact in (True,False):
     for newline in ('','\n'):
      kw=dict(sort_keys=sort,ensure_ascii=ascii,indent=indent)
      if compact:kw['separators']=(',',':')
      if sha((json.dumps(payload,**kw)+newline).encode())==value:matches.append({'sort_keys':sort,'ensure_ascii':ascii,'indent':indent,'compact_separators':compact,'newline':bool(newline)})
 digests.append({'path':path,'key':key,'expected':value,'matching_serializations':matches,'status':'PASS' if matches else 'UNRESOLVED'})
for f,k in [('whole-proof-review43/reviewer.math.run.json','run_hash'),('source.0.review.json','review_run_sha256'),('source.1.review.json','review_run_sha256'),('source.review.lease.json','lease_run_sha256'),('source.review.repair1.lease.json','lease_run_sha256'),('source.review.repair1.overlay-review.json','review_run_sha256')]:digest_record(prefix+'/'+f,k)
j=load(prefix+'/anonymous-decoder/run.json');digest_record(prefix+'/anonymous-decoder/run.json','decoder_run_sha256',j['execution_payload'])
# Canonical root fake-closure scan without Lake invocation.
diag=astis.lean_diagnostics();fake={'status':'PASS' if diag['totals']['forbidden_hits']==0 else 'FAIL','canonical_file_count':diag['totals']['files'],'hits':diag['totals']['forbidden_hits'],'findings':[x for x in diag['files'] if x['forbidden']] if 'files' in diag else []}
# Exact43 patch whitespace only (CR accepted), old cross-main artifacts kept unchanged.
cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check','95414fb1b121cc15fccf71445ad06bb064384c41','19b569ae0fe37c97da0f98b4d1f4933ebabc7052','--','AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOKLFisher.lean','Tests/StandardizedRGOKLFisher.lean','research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-fisher.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-StandardizedRGOKLFisher.json','website/content/declaration_lessons/standardized-rgo-kl-fisher.json','website/content/publications/standardized-rgo-kl-fisher.json'];d=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(run/'reviewer.exact.focused-diff.log').write_bytes(d.stdout)
out={'resolved_historical_pin_count':len(resolved),'resolutions':resolved,'unresolved':unresolved,'Mathlib_commit':mathsha,'Mathlib_pins':mathpins,'anonymous_ignored_equals_committed':actualanon==committedanon,'digest_checks':digests,'canonical_fake_closure':fake,'focused_diff':{'command':cmd,'exit_code':d.returncode,'output':d.stdout.decode()},'initial_scanner_diagnosis':'Generic path checker first compared preserved pre-review/overlay input pins to current admitted metadata; those historical mutations must instead bind exact preserved raw snapshots. Decoder paths relative to anonymous-decoder, and Mathlib is a separately pinned Git repository. Initial broad cross-main whitespace scan flags historical committed compilerlogs/CR artifacts, not a Lean/source failure; unchanged records preserved.'}
(run/'reviewer.exact.resolutions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('RESOLVED',len(resolved),'UNRESOLVED',len(unresolved),'MATHLIB',mathsha,'FAKE',fake,'FOCUSED_DIFF',d.returncode)
for x in digests:print(x['path'],x['key'],x['status'],x['matching_serializations'][:1])
for x in unresolved:print(x)


