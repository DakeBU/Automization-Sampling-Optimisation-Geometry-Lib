import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=[R/'source-review.packet.0.json',R/'source-review.freeze71.json',R/'canonical71.frozen.exactraw.lean',R/'canonical71.frozen.LF.lean',R/'expanded71.frozen.header.lean',B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean',B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean',B/'website/content/publications/pbps-actual-corrector-change.json',B/'website/content/declaration_lessons/pbps-actual-corrector-change.json',B/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json',R/'publication-freeze71.json',R/'mathematics-freeze71.json',R/'root.decoder71.adoption.json',R/'anonymous.0.decoder.json',R/'anonymous.lean-context71.json',B/'tools/astis_semantic_roundtrip_core.py',B/'tools/astis_publication.py',B/'website/scripts/declaration_lessons.py',B/'website/scripts/inline_lean.py',B/'lean-toolchain',B/'lake-manifest.json',R/'focused-typed-substitution/receipt.json',R/'focused-typed-substitution/stdout.log',R/'focused-typed-substitution/stderr.log']
# Exact decoder native byte provenance, no science/source verdicts.
paths.extend(sorted(p for p in (R/'anonymous-decoder').rglob('*') if p.is_file()))
rows=[]
for k,p in enumerate(paths):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');n=f'stageB.input.{k:02d}.exactraw.snapshot';(O/n).write_bytes(b);(O/(n+'.LF')).write_bytes(lf)
 rows.append({'original_path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':'ONLY CRLF byte pairs to LF','snapshot':n,'LF_snapshot':n+'.LF','mtime_ns':p.stat().st_mtime_ns})
packet=json.loads(paths[0].read_bytes());freeze=json.loads(paths[1].read_bytes())
for k in ['packet','source_body','publication','lesson','frontier']:
 q=freeze[k];b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256']
module=(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_bytes()
assert module==paths[2].read_bytes()==paths[3].read_bytes()
assert module.decode()==packet['candidate_publication_context']['current_lean_module']
official=packet['packet_sha256'];omit=sha(canon({k:v for k,v in packet.items() if k!='packet_sha256'}));whole=sha(canon(packet))
assert official==omit
write('stageB.exact-input-manifest71.json',{'schema':'source71-stageB-exact-current-inputs-v1','actual_pid':os.getpid(),'input_count':len(rows),'inputs':rows,'packet_RAW_sha256':sha(paths[0].read_bytes()),'packet_official_omit_top_packet_sha256':official,'packet_canonical_whole_sha256':whole,'packet_official_recipe':'Canonical sorted compact JSON deleting ONLY top-level packet_sha256. Distinct from native whole-logical run recipe.','no_root_math_or_old_source_verdict_read':True})
lines=module.decode().splitlines(keepends=True);assert len(lines)==528
(O/'stageB.module71.numbered.readview.txt').write_text(''.join(f'{i+1:03d}: {x}' for i,x in enumerate(lines)),encoding='utf-8',newline='\n')
(O/'stageB.decoder71.complete.readview.txt').write_text(packet['blind_reconstruction']['text'],encoding='utf-8',newline='\n')
print(json.dumps({'actual_pid':os.getpid(),'inputs':len(rows),'module_lines':len(lines),'module_RAW_sha256':sha(module),'packet_RAW_sha256':sha(paths[0].read_bytes()),'packet_official_omit_top':official,'packet_canonical_whole':whole},indent=2))
