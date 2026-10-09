import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
rows=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();rows.append({'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))});return b
native=pin(R/'integration70/record-admin-observer/inputs/14.exactraw.snapshot');assert sha(native)=='379230baf93f09adb8d80d51b87b52502aeb6868b76f06f2877171e3895bad5d';assert native==(O/'handoff.pre-admin.hash-verified-derived.exactraw.md').read_bytes()
admin=json.loads(pin(R/'integration70/record-admin-observer/receipt.json'));assert admin['inputs'][14]['RAW_sha256']==sha(native);print('native preadmin equality PASS; observer actualPID',admin.get('actual_foreground_PID'),'EXIT',admin.get('exit_code'))
for n in ['run-browser70.py','inspect-cdp70.mjs','inspect-copy70.mjs']:
 bb=pin(B/'.astis/pbps-actual-rotation70'/n);t=bb.decode();print('\nROOT NATIVE BROWSER HELPER',n,'sha',sha(bb))
 for line in t.splitlines():
  if any(w.lower() in line.lower() for w in ['chrome','browser','executable','Popen','spawn','playwright','clipboard']):print(line[:300])
 (O/(n+'.root-helper.exactraw')).write_bytes(bb);(O/(n+'.root-helper.LF')).write_bytes(bb.replace(b'\r\n',b'\n'))
assert b'chrome' in (B/'.astis/pbps-actual-rotation70/run-browser70.py').read_bytes().lower()
for p in [R/'integration70/visual70/render-chrome.stderr.log',R/'integration70/visual70/copy-chrome.stderr.log']:
 bb=p.read_bytes();assert b'DevTools listening' in bb;print('native Chrome DevTools marker PASS',p.name)
br=json.loads((R/'integration70/browser-full-current/receipt.json').read_bytes());assert br['exit_code']==0
scope=[]
for p in sorted((R/'integration70').glob('scope-*/receipt.json')):
 if p.parent.name=='scope-gates-observer':continue
 x=json.loads(p.read_bytes());assert x['exit_code']==0
 for q in x['inputs']:
  b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
 scope.append({'label':p.parent.name,'actual_PID':x['actual_foreground_PID'],'EXIT':0,'exact_current_inputs':len(x['inputs'])})
assert len(scope)==6
snap=[]
for i in [0,1,2,4,14,15,16,19,20,21,22,23,24,25,26,27,28,29,30,139]:
 q=json.loads((O/'packet140.current-input-pins.json').read_bytes())['inputs'][i];p=pathlib.Path(q['path']);b=p.read_bytes();name=f'input{i:03d}.{p.name}.exactraw';(O/name).write_bytes(b);(O/(name+'.LF')).write_bytes(b.replace(b'\r\n',b'\n'));snap.append({'original_path':q['path'],'snapshot':name,'LF_snapshot':name+'.LF','RAW_sha256':sha(b)})
verified=json.loads((R/'verified.json').read_bytes());ledger=(B/'runs/substantive_advances.jsonl').read_bytes();(O/'unique-nonowner-VERIFIED.append.exactraw.jsonl').write_bytes(ledger[verified['ledger_before']['raw_bytes']:])
write('current-input-snapshot-map70.json',{'recipe':'RAW verbatim; LF only CRLF->LF; remaining finite inputs pinned in manifests without duplicating existing native bundles','count':len(snap),'snapshots':snap})
write('corroboration70.json',{'actual_PID':os.getpid(),'native_pre_admin_snapshot_matches_independent_exact_reverse_derivation':True,'native_pre_admin_snapshot_RAW_sha256':sha(native),'original_recorded_native_path':str(R/'integration70/record-admin-observer/inputs/14.exactraw.snapshot').replace('\\','/'),'root_native_browser_helpers_pinned_for_provenance_only':True,'native_actual_Chrome_DevTools_markers':True,'six_scope_gates_exact_current_input_pins':scope,'no_browser_compile_site_replay':True})
write('corroboration70.additional-input-pins.json',{'count':len(rows),'LF_rule':'CRLF to LF only','inputs':rows});print('PASS final corroboration',len(scope),'scope gates; snapshots',len(snap))
