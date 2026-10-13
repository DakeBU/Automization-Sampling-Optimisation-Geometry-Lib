import sys,os,json,traceback
from pathlib import Path
import review68 as R
import final68 as F
O=R.O;P=R.P;pin=R.pin;sha=R.sha;save=R.save;get=R.get;read=R.read;now=R.now
try:
 path=P/'decoder-state-map.for-math68.json';assert pin(path)['raw_sha256']=='d14d281ddf9127af9488d984094c0781d6af0d112af329d4e978a90528615232';m=read(path);assert len(m['rows'])==2
 paths=[path];resolved=[]
 for q in m['rows']:
  canonical=Path(q['canonical_file']);before=Path(q['frozen_exact_before_snapshot']);after=Path(q['current_exact_after_snapshot']);pr=next(x for x in get('final.inputs.manifest.json')['inputs'] if x['original']['path']==canonical.as_posix())
  assert pin(before)['raw_sha256']==pr['original']['raw_sha256']==q['before_RAW_sha256'] and before.read_bytes()==Path(pr['RAW_snapshot']['path']).read_bytes()
  assert pin(after)['raw_sha256']==q['current_RAW_sha256']==pin(canonical)['raw_sha256'] and after.read_bytes()==canonical.read_bytes()
  b=read(before);a=read(after);allowed=set(q['allowed_changed_top_fields']);assert allowed=={'state','reconstruction'}
  changed={k for k in set(a)|set(b) if a.get(k)!=b.get(k)};assert changed==allowed
  assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}
  resolved.append(dict(canonical_path=canonical.as_posix(),original_frozen_input=pr['original'],explicit_before_snapshot=pin(before),explicit_after_snapshot=pin(after),current_observed=pin(canonical),only_changed_top_fields=sorted(changed),all_other_fields_exact=True,no_decoder_verdict_or_reconstruction_used_as_mathematical_credit=True));paths.extend([before,after])
 for q in get('final.inputs.manifest.json')['inputs']:
  if q['original']['path'] not in {x['canonical_path'] for x in resolved}:assert pin(q['original']['path'])==q['original']
 rows=[]
 for i,p in enumerate(paths):
  raw=p.read_bytes();rp=O/f'resolution-inputs/{i:03}.RAW.snapshot';lp=O/f'resolution-inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(raw);lp.write_bytes(raw.replace(b'\r\n',b'\n'));rows.append(dict(original=pin(p),RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('resolution.inputs.manifest.json',dict(actual_PID=os.getpid(),utc=now(),input_count=len(rows),inputs=rows,finite_exact_mapping_only=True))
 save('finite-input-resolution.json',dict(status='QUALIFIED_TWO_EXACT_DECODER_STATE_ONLY_HISTORICAL_INPUTS',actual_PID=os.getpid(),utc=now(),root_explicit_map=pin(path),rows=resolved,original44_rows_and_snapshots_untouched=True,source_or_decoder_verdict_consumed=False,retained_finalizer_negative=pin(O/'finalize.failure.json'),prose_overlay_still_not_applied=True,mathematical_inputs_or_verdict_changed=False))
 print(json.dumps(dict(status='QUALIFIED',actual_PID=os.getpid(),canonical_audit_rows=2,all_other_final_original_rows=42,root_map_RAW=pin(path)['raw_sha256'])))
except Exception as e:
 save((sys.argv[2] if len(sys.argv)>2 else 'resolution')+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()));raise
