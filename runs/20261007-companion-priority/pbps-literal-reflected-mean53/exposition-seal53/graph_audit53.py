import sys,json,hashlib,subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8'); sys.dont_write_bytecode=True
root=Path(r'E:\Samplinglib'); role=root/'runs/20261007-companion-priority/pbps-literal-reflected-mean53/exposition-seal53'
def sha(b): return hashlib.sha256(b).hexdigest()
def can(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def bind(p):
 b=p.read_bytes(); return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def write(p,o): p.write_bytes((json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8'))
opens=[]
def audit(event,args):
 if event!='open' or not isinstance(args[0],(str,bytes)): return
 p=Path(args[0]).resolve()
 try: rel=p.relative_to(root).as_posix()
 except ValueError:return
 if rel.startswith('runs/') or rel.startswith('.astis/'):
  if not str(p).startswith(str(role)): raise RuntimeError('Canonical digest unexpectedly attempted run/ignored evidence read: '+rel)
 opens.append(rel)
sys.addaudithook(audit)
sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'website/scripts'))
import publication_reader as reader
value=reader.graph_input_digest()
g=json.loads((root/'_site/data/underlying-lean-graph.json').read_bytes())
assert value==g['publication_inputs_sha256']
cell=reader.publication.inputs()['cells']['ASTIS-SW-PBPS-literal-reflected-mean']
name='AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean.reflected_gibbs_mean_c1'
decl=reader.publication.inputs()['declarations'][name]
helpers=[Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).startswith(str(root)) and Path(m.__file__).suffix=='.py']
source_bindings=[]
for rp in ['AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean','Tests/ProximalBPSReflectedMeanRegularity.lean']:
 b=(root/rp).read_bytes(); lf=b.replace(b'\r\n',b'\n'); rows=[]
 for commit in ['ccc75d59bcc7fe303b3aa6e68252cfcc5867d090','9f0305db380966529eb3b0fc17a62aa9bcd47a85']:
  gb=subprocess.check_output(['git','show',commit+':'+rp],cwd=root); glf=gb.replace(b'\r\n',b'\n'); assert lf==glf
  rows.append({'commit':commit,'git_raw_sha256':sha(gb),'git_lf_sha256':sha(glf),'current_raw_equals_git_raw':b==gb,'current_lf_equals_git_lf':lf==glf,'git_line_count':len(gb.decode('utf-8').splitlines())})
 source_bindings.append({'current':bind(root/rp),'current_line_count':len(b.decode('utf-8').splitlines()),'git':rows})
record={'status':'ACTUAL_CANONICAL_GRAPH_DIGEST_MATCH','publication_inputs_sha256':value,'recipe':'Invoke website/scripts/publication_reader.py graph_input_digest(): publication.digest of {lean: astis_site.source_digest(), items: publication.load(), cells: {bound cell id: publication.inputs().cells.get(id)}}. source_digest hashes each actual path UTF-8 then NUL then raw bytes then NUL in the exact function order. publication.digest uses sorted compact ensure_ascii=False JSON with Python default allow_nan=True UTF-8. This is distinct from the native role logical hash recipe (allow_nan=False).','canonical_digest_scope':'Necessary established canonical project/source/publication/cell/audit/lesson reads authorized for digest only; no semantic replay; audit hook rejected any run/ignored evidence access outside this role; bytecode writes disabled.','helpers':[bind(p) for p in dict.fromkeys(helpers)],'source_gitLF_bindings':source_bindings,'cell_path':cell['__path__'],'cell_binding':bind(root/cell['__path__']),'cell_status':cell.get('status'),'native_declaration_extraction':{k:str(v) for k,v in vars(decl).items() if k in ['full_name','source_file','module','line','statement','proof']},'open_paths':sorted(set(opens)),'graph_binding':bind(root/'_site/data/underlying-lean-graph.json')}
write(role/'graph-binding53.json',record)
print(json.dumps({'digest':value,'helper_count':len(record['helpers']),'canonical_open_count':len(record['open_paths']),'cell':record['cell_path'],'cell_status':record['cell_status'],'sources':source_bindings,'decl_fields':list(vars(decl))},ensure_ascii=False,indent=2))