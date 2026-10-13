from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-clock-preproof75');r=pre.parent/'pbps-actual-hazard-clock75';out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
gate=json.loads((r/'focused-primitive-direct-orbit/receipt.json').read_bytes());assert gate['terminal_closed'] and gate['exit_code']==0
seal=json.loads((pre/'root.statement-seal75.json').read_bytes());hb=Path(seal['header']['path']).read_bytes();assert hashlib.sha256(hb).hexdigest()==seal['header']['RAW_sha256'];header=hb.decode()
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean');before=p.read_bytes();(out/'module.before.exactraw.lean').write_bytes(before);text=before.decode();ending='end\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock\n';assert text.endswith(ending)
public='theorem actual_integrated_hazard_clock_laws\n'+header.split('theorem actual_integrated_hazard_clock_laws\n',1)[1]
lets=header[header.index('    let c :'):header.index('    Continuous (fun a : ((E × E)')]
conclusion=header[header.index('    Continuous (fun a : ((E × E)'):header.index('\n\ntheorem actual_integrated_hazard_clock_laws')]
body=Path('.astis/pbps-clock75/full-clock-body75.txt').read_text(encoding='utf8')
text=text.removesuffix(ending)+'set_option maxHeartbeats 1200000 in\n'+public+''.join(s[2:]+'\n' for s in lets.splitlines())+'  change\n'+conclusion+'\n'+body+'\n'+ending
p.write_text(text,encoding='utf8',newline='\n')
(out/'admission.json').write_text(json.dumps(dict(status='FULL_SEALED_TEN_CLAUSE_CANDIDATE_APPENDED_NOT_YET_COMPILED',actual_root_PID=os.getpid(),sealed_header_RAW_sha256=seal['header']['RAW_sha256'],original_public_telescope_unchanged=True,internal_primitive_gate_PID=gate['actual_foreground_PID'],internal_primitive_gate_EXIT=0,full75_proved=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
