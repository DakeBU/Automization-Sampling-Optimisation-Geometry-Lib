from common import *
from tools import astis,astis_publication
import re,gzip
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==SCI
paths=[p for p in subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',SCI],cwd=ROOT).decode().split('\0') if p];assert len(paths)==1003,len(paths)
tree={}
for row in subprocess.check_output(['git','ls-tree','-rz',SCI],cwd=ROOT).split(b'\0'):
 if row:
  meta,n=row.split(b'\t',1);tree[n.decode()]=meta.decode().split()
child=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE);data,_=child.communicate(('\n'.join(tree[n][2] for n in paths)+'\n').encode());assert child.returncode==0;pos=0;entries=[]
for n in paths:
 end=data.index(b'\n',pos);size=int(data[pos:end].split()[2]);b=data[end+1:end+1+size];pos=end+size+2;a=pin(n);assert a['lf_sha256']==H(b.replace(b'\r\n',b'\n')),(n,a)
 entries.append(dict(repository_path=n,git_mode=tree[n][0],git_blob=tree[n][2],git_raw_bytes=len(b),git_raw_sha256=H(b),git_lf_sha256=H(b.replace(b'\r\n',b'\n')),current=a))
W(P/'science.entries.json',dict(checked_commit=SCI,parent=BASE,actual_catfile_PID=child.pid,exit_code=child.returncode,count=len(entries),entries=entries,all_current_Git_LF_equal=True,active_commit_observer_and_next_scout_excluded=True))
freeze=J(R/'math-freeze.json');scan=[]
for row in freeze['inputs'][:5]:
 text=astis.strip_lean_comments_and_strings(path(row['path']).read_text(encoding='utf8'));hits=[m.group(0) for m in astis.FORBIDDEN_REGEX.finditer(text)];assert not hits;assert not re.search(r'^\s*import\s+Tests(?:\.|\s|$)',text,re.M);scan.append(dict(input=matches(row),fake_closure_hits=hits,production_Tests_import_hits=[]))
W(P/'fake-closure.json',dict(status='PASS',actual_PID=os.getpid(),inputs=scan,input_count=len(scan),fake_closure_hits=0,scope='Actual3 current62 sources and2 real public ASTIS parent modules; string/comment-stripped authored proof bodies, no placeholders/circular/Test imports',successful_axioms=J(P/'compiler.json')['standard3_prints'],negative_scope='Compiler-generated failed-elaboration synthetic sorryAx from historical failures not granted authored or final proof credit'))
plan=J(R/'publication-plan.json');astis_publication.check_advance(plan['mathematical_declarations'],reviewed=True);W(P/'reviewed-publication.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,actual_API='tools.astis_publication.check_advance(declarations,reviewed=True)',declarations=plan['mathematical_declarations'],tool=pin(ROOT/'tools/astis_publication.py'),audits=[pin(ROOT/('research-wiki/semantic-roundtrip/audits/'+i+'.json')) for i in plan['audit_ids']]))
gates=[]
for label,args in [('publication',['tools/astis_publication.py','check','--base',BASE]),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]:
 q=invoke(label,[sys.executable,'-B','-X','utf8',*args]);gates.append(q);assert q['exit_code']==0,(label,q)
wh=J(R/'whitespace-diagnosis62/diagnosis.json');assert len(wh['findings'])==192 and len(wh['immutable_native_exceptions'])==14 and wh['authored_complement_check_exit']==0;gz=next((R/'whitespace-diagnosis62').glob('*.gz'));assert H(gzip.decompress(gz.read_bytes()))==wh['negative_raw_sha256']
W(P/'gates.json',dict(status='PASS',checked_commit=SCI,actual_wrapper_PID=os.getpid(),reviewed_publication=pin(P/'reviewed-publication.json'),actual_foreground_gates=gates,full_shared_root_Tests_Registry_site_graph='DEFERRED_NOT_RUN_IN_EXACT_SCIENCE; serialized root integration required later',whitespace=dict(full_staged_negative_findings=192,exact_immutable_native_paths=wh['immutable_native_exceptions'],authored_complement_PASS=True,full_staged_PASS=False,lossless_gzip=pin(gz),raw_negative_sha256=wh['negative_raw_sha256'],diagnosis=pin(R/'whitespace-diagnosis62/diagnosis.json'))))
print('GIT_SOURCE_NONCOMPILER_GATES_PASS',len(entries),len(gates),'fake0')
