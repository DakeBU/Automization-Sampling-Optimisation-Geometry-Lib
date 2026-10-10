from pathlib import Path
import json,hashlib,re,sys

r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
receipt=json.loads((r/sys.argv[1]/'receipt.json').read_bytes())
assert receipt['terminal_closed'] and receipt['exit_code']==0
log=(r/sys.argv[1]/'stdout.log').read_text(encoding='utf-8')
name='AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound'
m=re.search(re.escape("'"+name+"'")+r' depends on axioms: \[([^\]]+)\]',log)
assert m and set(re.findall(r'\w+(?:\.\w+)*',m[1]))=={'propext','Classical.choice','Quot.sound'}
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean');before=p.read_bytes()
pin=next(z for z in receipt['inputs'] if z['path']==p.resolve().as_posix())
assert hashlib.sha256(before).hexdigest()==pin['raw_sha256']
s=before.decode('utf-8')
s,n=re.subn(r'(?m)^([ ]*)run_tac do\n\1  let _ ← IO\.FS\.writeFile [^\n]+\n\1  pure \(\)\n','',s)
assert n==35,n
assert 'run_tac' not in s and 'IO.FS' not in s
d=r/'compiler-diagnosis68';q=d/'main.diagnostic-compiled.exactraw.snapshot.lean';assert not q.exists();q.write_bytes(before)
markers=[]
for pattern in ['stage4-*.log','stage6-*.log','stage7-*.log','projection7-*.log','stage8-*.log','projection8-*.log','reassembly8-*.log','stage9-*.log','projection9-*.log','reassembly9-*.log','global9-*.log','stage10-*.log','projection10-*.log','reassembly10-*.log','global10-*.log','stage11-*.log','projection11-*.log','reassembly11-*.log','global11-*.log']:
 for f in sorted(Path('.astis/pbps-sharp-energy68').glob(pattern)):
  out=d/('closed-'+f.name);assert not out.exists();out.write_bytes(f.read_bytes());markers.append(dict(path=out.as_posix(),RAW_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),observed_original_mtime_ns=f.stat().st_mtime_ns))
p.write_text(s,encoding='utf-8',newline='\n')
payload=dict(status='DIAGNOSTIC_MAIN_COMPILED_STANDARD3_NOW_DEBUG_IO_REMOVED_FINAL_CODE_RECOMPILE_REQUIRED',
 removed_IO_blocks=n,exact_compiled_receipt=(r/sys.argv[1]/'receipt.json').as_posix(),
 compiled_before_RAW_sha256=hashlib.sha256(before).hexdigest(),clean_after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
 markers=markers,public_statement_and_all_mathematical_proof_ingredients_unchanged=True,final_clean_compiler_credit=False,
 typed_route_reduction='Deep parent rcases was replaced by bounded conjunction projections and12 atomic eliminations of the exact existing existential witnesses. Transparent Classical.choose aliases removed the extraction bottleneck but moved it to reconstruction; atomic elimination also removed that stage. The last actual-input decomposition uses one atomic existential and5 original proof projections in an explicitly typed compact local have BEFORE outer reconstruction. This context change removed the final elimination bottleneck. Opaque-target-only diagnosis did not remove the original bottleneck. A redundant ring after successful field_simp was then removed.',
 accidental_unchanged_diagnostic_dispatch='v4 was immediately stopped after instrumentation assertion failure; retained explicitly, no proof/retry credit.')
(d/'diagnostics-removed.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('35 diagnostic IO blocks removed after exact diagnostic compilation; all phase bytes retained; clean code needs final fresh compile.')
