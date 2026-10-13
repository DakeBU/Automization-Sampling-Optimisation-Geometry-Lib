"""Bounded independent exact-commit verification; real foreground receipts."""
from pathlib import Path
import datetime, gzip, hashlib, json, os, subprocess, sys
ROOT=Path('E:/Samplinglib'); os.chdir(ROOT)
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78'
OUT=RUN/'exact-commit-verification78'; OUT.mkdir(exist_ok=True)
COMMIT='bbcad09376c51bbf27c0ed4c16be0dc053bb01c5'
BASE='d0872b10d3e9c78058059e95cce69c09ec8a314b'
MODULE='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation'
CELL='ASTIS-SW-PBPS-actual-event-time-nonaccumulation'
AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualNonaccumulation.json'
BINDING='f812375b3e96e4b089af570ccd3a0f2f0852e0bd950290f77791b89974fc9069'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
    p=Path(p); b=p.read_bytes(); return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
    p=OUT/n; assert not p.exists(),p
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*a): return subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==COMMIT
archives={}
for name in ['immutable-log-archives78.json','immutable-whitespace-archives78.json']:
    for e in load(RUN/name)['files']:
        archives[e['raw_path']]=e['archive']
matches=[]
def exact(p):
    p=Path(p); p=p if p.is_absolute() else ROOT/p
    rel=p.relative_to(ROOT).as_posix(); raw=p.read_bytes()
    q=subprocess.run(['git','show',COMMIT+':'+rel],capture_output=True)
    archived=False
    if q.returncode:
        assert rel in archives,'Not committed or indexed: '+rel
        blob=gzip.decompress(git('show',COMMIT+':'+archives[rel])); archived=True
    else: blob=q.stdout
    same=blob==raw
    assert same or (rel != MODULE and blob.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')),rel
    matches.append(dict(**info(p),git_blob_sha256=sha(blob),exact_equal=same,lossless_archive=archived,newline_only_checkout_difference=not same))
    return raw
paths=[MODULE,'lean-toolchain','lake-manifest.json',AUDIT,
 'website/content/declaration_lessons/pbps-actual-event-time-nonaccumulation.json',
 'website/content/publications/pbps-actual-event-time-nonaccumulation.json']
for n in ['root.statement-seal78.json','claim.json','proved-local78.json','root.math78.adoption.json','root.decoder78.adoption.json','root.source78.adoption.json','source-review78.packet.json']:
    paths.append((RUN/n).relative_to(ROOT).as_posix())
for p in paths: exact(p)
assert sha((ROOT/MODULE).read_bytes())=='e6d71cb969b30f6ac8e6be65e5cd067166b4f29213d9328ed9edc0971fd026fc'
assert git('-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
# Reuse own unchanged fresh complete-source proof evidence, checking every input and log.
receipt=load(RUN/'independent-math78/fresh-whole-module-axioms.receipt.json')
assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['full_source_prefix_exact']
for e in receipt['inputs']:
    assert info(e['path'])['RAW_sha256']==e['RAW_sha256']; exact(e['path'])
for e in [receipt['stdout'],receipt['stderr']]:
    assert info(e['path'])['RAW_sha256']==e['RAW_sha256']; exact(e['path'])
for n in ['decision78.json','whole-proof-mathematics78.json','statement-and-definition-audit78.json','fresh-whole-module-axioms.receipt.json','fresh-compiler-summary78.json']:
    exact(RUN/'independent-math78'/n)
assert info(RUN/'independent-math78/decision78.json')['RAW_sha256']=='9e2d5529437717aab24950a4b09d9105faaba82364807d7a09beceab7df66eb5'
manifest=load(RUN/'fresh-source78/source-review.run-manifest78.json')
for e in manifest['inputs']:
    assert info(e['path'])['RAW_sha256']==e['raw_sha256']; exact(e['path'])
for e in manifest['outputs']:
    if 'raw_sha256' in e:
        assert info(e['path'])['RAW_sha256']==e['raw_sha256']; exact(e['path'])
exact(RUN/'fresh-source78/source-review.run-manifest78.json')
exact(RUN/'fresh-source78/source-review.result78.json')
for n in ['run-manifest.json','response.json','parent-packet.json','native-response.md']: exact(RUN/'anonymous-decoder78'/n)
audit=load(ROOT/AUDIT); assert audit['state']=='accepted'
lesson=load(ROOT/paths[4])['units'][0]; source=(ROOT/MODULE).read_bytes(); lines=source.splitlines(keepends=True)
regions=[]
for s in lesson['steps']:
    r=s['lean_source_region']; code=b''.join(lines[r['start_line']-1:r['end_line']])
    assert code==s['lean'].encode() and sha(code)==r['exact_code_raw_sha256'] and r['source_raw_sha256']==sha(source)
    assert s['formula'] and s['text']
    regions.append(dict(title=s['title'],start=r['start_line'],end=r['end_line'],sha256=sha(code),formula=s['formula'],text=s['text']))
assert len(regions)==7
assert b''.join(s['lean'].encode() for s in lesson['steps'])==b''.join(lines[regions[0]['start']-1:regions[-1]['end']])
save('input-freeze.json',dict(checked_commit=COMMIT,exact_commit_matches=matches,seven_contiguous_BODY_regions=regions,
 reused_fresh_source_receipt=info(RUN/'independent-math78/fresh-whole-module-axioms.receipt.json'),
 reuse_reason='Every source, parent, seal, full-source probe, toolchain, manifest and terminal log hash is unchanged and bound to this commit. No new native reasoning trajectory is claimed.',audit_state=audit['state']))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(name,args):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OUT/(name+'.stdout.log')).open('xb') as stdout,(OUT/(name+'.stderr.log')).open('xb') as stderr:
        p=subprocess.Popen(args,cwd=ROOT,env=env,stdout=stdout,stderr=stderr)
        print(name,'foreground PID',p.pid,flush=True); code=p.wait()
    save(name+'.receipt.json',dict(command=args,cwd=str(ROOT),checked_commit=COMMIT,started_utc=start,
      finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=p.pid,
      exit_code=code,terminal_closed=True,stdout=info(OUT/(name+'.stdout.log')),stderr=info(OUT/(name+'.stderr.log'))))
    print(name,'EXIT',code,flush=True)
    assert code==0,name+' failed; logs retained'
py=[sys.executable,'-X','utf8'];lake=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
for name,args in [
 ('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),
 ('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation']),
 ('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),
 ('publication',py+['tools/astis_publication.py','check','--base',BASE]),
 ('semantic',py+['tools/astis_semantic_roundtrip.py','check']),
 ('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(name,args)
packet=load(OUT/'packet.stdout.log'); assert len(packet['targets'])==1
assert packet['targets'][0]['publication_binding_sha256']==BINDING
sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from tools import astis
hits=astis.forbidden_pattern_hits()
save('fake-closure-scan.json',dict(checked_commit=COMMIT,verifier_id='/root/exact_verify77',
 algorithm='tools.astis.forbidden_pattern_hits',scanned_files=len(astis.lean_source_files()),hits=hits))
assert not hits
assert exact(MODULE)==source
save('checks-complete.json',dict(status='PASS',checked_commit=COMMIT,publication_binding_sha256=BINDING,
 source_review='/root/fresh_source78',blind_decoder='/root/blind_decoder78',verifier_id='/root/exact_verify77',
 reused_own_fresh_full_source_elaboration=True,axioms=['propext','Classical.choice','Quot.sound'],
 aggregate_gate='Pending serialized stabilization; not run in this bounded admission'))
print('ALL BOUNDED CHECKS PASS',flush=True)
