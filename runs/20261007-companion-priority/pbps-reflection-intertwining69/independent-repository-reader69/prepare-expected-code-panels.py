import hashlib,json,os,pathlib,sys
out=pathlib.Path(__file__).resolve().parent;run=out.parent;repo=pathlib.Path(r'E:\Samplinglib')
sys.dont_write_bytecode=True;sys.path[:0]=[str(repo/'tools'),str(repo/'website/scripts')]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
m=json.loads((out/'input-manifest.json').read_bytes())
def pin(n,p,role):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 m['inputs'].append(dict(name=n,original_path=str(p),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)));return b
mb=pin('accepted-source211.current.ReflectionIntertwining.RAW.lean',run/'independent-source69/current.ReflectionIntertwining.RAW.lean','accepted-exact-current-module-bytes for expected DOM/copy/download; no-mathematical-rereview')
assert sha(mb)=='7bbaae1abd67305749d385153019061eb055a7968a707f919e7d9ac9fc21846d'
pin('renderer.astis_site.RAW.py',repo/'tools/astis_site.py','single-module declaration scanner only; no full-project scan')
import astis_site as base
import inline_lean
module=repo/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean'
assert module.read_bytes()==mb
base.project_lean_paths=lambda:[module]
_,decls=base.scan_project_sources();assert len(decls)==2
known={d.full_name:d for d in decls};base._SOURCE_BY_NAME=known
base._ACTIVE_GIT=base.GitContext(commit='',ref='bounded-preview',remote_url='',web_root='',commit_published=False,public_source_links=False,dirty_files=set())
public='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining';private=public+'_statement'
proof=inline_lean.display_source(known[public].source_text);signature,_=inline_lean.split_statement(proof);helper=inline_lean.display_source(known[private].source_text)
entries=[]
for label,name,role,text in [('public-statement',public,'statement',signature),('public-proof',public,'proof',proof),('private-literal-Prop-helper',private,'proof',helper)]:
 b=text.encode('utf-8');entries.append(dict(panel=label,data_inline_lean=name,role=role,text=text,LF_UTF8_bytes=len(b),LF_UTF8_sha256=sha(b)))
lesson=json.loads((out/'accepted-source211.final.lesson.RAW.json').read_bytes())['units'][0]
steps=[dict(step=i+1,title=s['title'],formula=s['formula'],text=s['text'],code=s['lean'],code_LF_UTF8_sha256=sha(s['lean'].encode('utf-8')),lines=[s['lean_source_region']['start_line'],s['lean_source_region']['end_line']]) for i,s in enumerate(lesson['steps'])]
preview=inline_lean.disclosure(public,role='statement',explanation=lesson['lean_statement'],page='declarations/bounded-repository-reader69.html',trim_following_docstring=True)+inline_lean.disclosure(public,role='proof',explanation=lesson['lean_proof'],page='declarations/bounded-repository-reader69.html',helpers=(private,),trim_following_docstring=True)
(out/'expected-three-code-panels.preview.html').write_text(preview,encoding='utf-8')
put('expected-code-and-reader-payload.before-final-packet.json',dict(schema='repository-reader69-expected-scoped-code-payload-v1',actual_pid=os.getpid(),final_packet_seen=False,code_panels=entries,code_panel_count=3,BODY_steps=steps,BODY_step_count=6,complete_natural_statement=lesson['statement'],assumptions=lesson['assumptions'],main_formula=lesson['formula'],private_helper_full_identity=private,private_helper_is_literal_Prop_record_not_provider=True,all_three_source_downloads=dict(RAW_bytes=len(mb),RAW_sha256=sha(mb),full_module=True),initial_closed_fold_policy='No open attribute on generated statement/proof/helper or six corresponding Lean-step details; browser may open them deliberately for captures/copy.',copy_callback_scope='closest data-lean-code-panel, immediate :scope > pre > code only; clipboard text compares with code panel LF_UTF8 hashes, downloads compare with complete module RAW hash.',no_visual_or_aggregate_acceptance_yet=True))
m['count']=len(m['inputs']);put('input-manifest.json',m)
print(json.dumps(dict(actual_pid=os.getpid(),expected_panels=3,expected_BODY_steps=6,input_count=m['count'],module_RAW_sha256=sha(mb),final_packet_seen=False),sort_keys=True))
