from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,time

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a/phase3'
EVID=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence'
EXPECTED='9d306d837fbddf1518b0035494baaf5c21c24488'
H=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==EXPECTED
packet_raw=(EVID/'full-anti-anchored-reviewer-packet.json').read_bytes()
assert H(packet_raw)=='0510cc019b9bcdb0b389b097a88108f3c7d0732d342174e27274dd43428f5168'
packet=json.loads(packet_raw)
p_without=dict(packet);p_without.pop('packet_sha256')
assert H(json.dumps(p_without,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==packet['packet_sha256']
pins_raw=(EVID/'full-review-input-pins.json').read_bytes();pins=json.loads(pins_raw)
assert pins['checked_candidate_commit']==EXPECTED
pin_receipts=[]
for rel,sha in pins['exact_inputs'].items():
    raw=(ROOT/rel).read_bytes()
    assert H(raw)==sha,(rel,H(raw),sha)
    committed=subprocess.check_output(['git','show',EXPECTED+':'+rel],cwd=ROOT)
    assert committed==raw,rel
    pin_receipts.append({'path':rel,'sha256':H(raw),'bytes':len(raw),'matches_HEAD_bytes':True,
      'semantic_read':not (rel.startswith('runs/') or '/semantic-roundtrip/audits/' in rel)})
    if not (rel.startswith('runs/') or '/semantic-roundtrip/audits/' in rel):
        dest=OUT/'inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
for name,raw in [('full-anti-anchored-reviewer-packet.json',packet_raw),('full-review-input-pins.json',pins_raw)]:
    (OUT/'inputs'/name).write_bytes(raw)
for rel in ['lean-toolchain','lake-manifest.json']:
    (OUT/'inputs'/rel).write_bytes((ROOT/rel).read_bytes())
assert H((ROOT/'lean-toolchain').read_bytes())==packet['candidate_publication_context']['toolchain']
assert H((ROOT/'lake-manifest.json').read_bytes())==packet['candidate_publication_context']['dependencies']
assert H((ROOT/packet['lean']['file']).read_bytes())==packet['candidate_publication_context']['file']
assert (ROOT/packet['lean']['file']).read_text()==packet['candidate_publication_context']['current_lean_module']
lesson=json.loads((ROOT/'website/content/declaration_lessons/huanjian-fixed-spectrum-first-order.json').read_text())['units'][0]
context_lesson=packet['candidate_publication_context']['lesson']
assert all(lesson[k]==v for k,v in context_lesson.items())
dump(OUT/'input_pin_receipt.json',{
 'checked_utc':datetime.now(timezone.utc).isoformat(),'checked_candidate_commit':head,
 'packet_raw_sha256':H(packet_raw),'packet_canonical_excluding_self_sha256':packet['packet_sha256'],
 'pins_raw_sha256':H(pins_raw),'publication_binding_sha256':packet['publication_binding_sha256'],
 'exact_inputs':pin_receipts,'whole_module_matches_packet_text':True,
 'toolchain_and_manifest_hashes_match_packet':True,
 'official_lesson_matches_packet_authored_fields':True,
 'extra_official_lesson_field':'boundary is present in the official lesson and independently reviewed; the packet omits that field rather than providing conflicting wording.',
 'audit_and_ledger_handling':'Hashed and compared to immutable HEAD bytes only; no audit verdict or ledger content decoded/read as mathematical guidance.'
})
lakepath=subprocess.check_output(['lake','env','printenv','LEAN_PATH'],cwd=ROOT,text=True).strip()
env=dict(os.environ);env['LEAN_PATH']=str(OUT/'lean-build')+':'+lakepath
leanbin=Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
version=subprocess.check_output([str(leanbin),'--version'],cwd=ROOT,env=env,text=True).strip()
records=[]
modules=[
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAffine.lean',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumFirstOrder.lean',
 'Tests/GaussianComplexityFixedSpectrumFirstOrder.lean']
for rel in modules:
    dest=(OUT/'lean-build'/rel).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=[str(leanbin),'-o',str(dest),rel]
    start=time.time()
    run=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    logfile=OUT/'logs'/(Path(rel).stem+'.fresh.log');logfile.write_text(run.stdout)
    record={'source':rel,'source_sha256':H((ROOT/rel).read_bytes()),'command':cmd,
      'returncode':run.returncode,'elapsed_seconds':time.time()-start,
      'log':str(logfile.relative_to(OUT)),'olean':str(dest.relative_to(OUT)),
      'olean_exists':dest.is_file()}
    if dest.is_file():record['olean_sha256']=H(dest.read_bytes())
    records.append(record)
    dump(OUT/'fresh_compile_receipt.json',{'checked_candidate_commit':EXPECTED,'lean_version':version,
      'isolation':'Freshly compile actual source files into owned lean-build; prepend owned build to LEAN_PATH so downstream imports use freshly built critical ancestors. No canonical source or .lake project olean is overwritten.',
      'owned_LEAN_PATH_prefix':str(OUT/'lean-build'),'base_LEAN_PATH':lakepath,'runs':records})
    print(json.dumps(record),flush=True)
    if run.returncode:raise SystemExit(run.returncode)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==EXPECTED
print('All four pinned actual sources freshly compiled into the independent owned overlay.',flush=True)
