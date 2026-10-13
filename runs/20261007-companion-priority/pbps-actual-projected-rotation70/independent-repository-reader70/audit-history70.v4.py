import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,subprocess,difflib
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib');C='c46af8a55e89419109f654c4553cf527993cbeed';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
extra=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();extra.append({'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))});return b
def jd(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'pointer':path+'/'+k,'before':a.get(k),'after':b.get(k)})
   else:out+=jd(a[k],b[k],path+'/'+k)
  return out
 return [] if a==b else [{'pointer':path,'before':a,'after':b}]
oldcell=pin(R/'integration70/cell.0.before-final-admin.exactraw.snapshot.json');cell=pin(B/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json');oldhandoff=pin(R/'integration70/generator-sideeffects/handoff.before-wording.exactraw.snapshot');handoff=pin(B/'docs/companion-papers-handoff.md')
diff=jd(json.loads(oldcell),json.loads(cell));print('CELL DELTAS',json.dumps(diff,ensure_ascii=False,indent=2));assert {x['pointer'] for x in diff}=={'/blocked/reason','/evidence/serialized_shared_gate','/graph_contribution/visual_review'}
ht=handoff.decode().replace('\r\n','\n');ot=oldhandoff.decode().replace('\r\n','\n');hd=list(difflib.unified_diff(ot.splitlines(keepends=True),ht.splitlines(keepends=True),fromfile='handoff.before-wording',tofile='handoff.current'));print('HANDOFF DELTA',''.join(hd))
oldword=b'repair is a separate reviewed code change with fresh current browser checks due.';newword=b'repair is a separate reviewed code change; fresh local browser checks passed. Remote70 CI remains pending.'
assert oldhandoff.count(oldword)==1 and oldhandoff.replace(oldword,newword)==handoff
assert 'INT69 site CI failed its old helper-panel count' in ht and C in ht and 'B21' in ht
for p in [B/'.astis/pbps-actual-rotation70/record-integration70.py',B/'.astis/pbps-actual-rotation70/narrow-generated-scope70.py']:
 bb=pin(p);print('ACTION SOURCE',p.name,len(bb),sha(bb));(O/(p.name+'.exactraw')).write_bytes(bb);(O/(p.name+'.LF')).write_bytes(bb.replace(b'\r\n',b'\n'))
checks=json.loads((O/'repository70.checks.json').read_bytes());mapped=[]
admin_old='Serialized Registry518/imports/Tests and current reader/graph gates are pending\nagainst final admin state; exact science verification is separate from these\naggregate admissions and from remote CI.'
admin_new='Serialized local aggregate70: root9180, Tests9480, Registry518;239 publication units.\nOne complete statement, eight formula/BODY steps, full private-Prop helper and actual\nbranch inspected; three isolated copy callbacks and three RAW downloads exact.\nCurrent graph regeneration follows these final cell writes; final gates are recorded\nin existing70 integration.notes.json. Current full Python regression and real-browser\nchecks use the reviewed helper-aware scripts. Independent repository/reader, remoteCI/main/live and\nfull Exposition/PURIFIED remain separate.'
nl='\r\n' if b'\r\n' in oldhandoff else '\n'
newblock=admin_new.replace('\n',nl).encode();oldblock=admin_old.replace('\n',nl).encode();assert oldhandoff.count(newblock)==1
initialhandoff=oldhandoff.replace(newblock,oldblock)
(O/'handoff.pre-admin.hash-verified-derived.exactraw.md').write_bytes(initialhandoff)
(O/'handoff.pre-admin.hash-verified-derived.LF.md').write_bytes(initialhandoff.replace(b'\r\n',b'\n'))
write('handoff.pre-admin.exact-derivation-recipe.json',{'operation':'replace exactly one literal post-admin block by its literal pre-admin block; retain every other byte and native newline','source_RAW_sha256':sha(oldhandoff),'from_literal':admin_new,'to_literal':admin_old,'native_newline':repr(nl),'derived_RAW_sha256':sha(initialhandoff),'authority':'Exact equality to independently pinned pre-admin native gate input RAW digest; this is a hash-verified derivation, not a contemporaneous snapshot claim.'})
for q in checks['earlier_gate_input_differences']:
 authority=oldcell if q['path'].endswith('ASTIS-SW-PBPS-actual-projected-rotation.json') else (oldhandoff if sha(oldhandoff)==q['recorded_RAW_sha256'] else initialhandoff)
 assert sha(authority)==q['recorded_RAW_sha256'],q
 locator=(R/'integration70/cell.0.before-final-admin.exactraw.snapshot.json') if authority is oldcell else ((R/'integration70/generator-sideeffects/handoff.before-wording.exactraw.snapshot') if authority is oldhandoff else O/'handoff.pre-admin.hash-verified-derived.exactraw.md')
 mapped.append({**q,'exact_before_evidence':str(locator).replace('\\','/'),'classification':'postcheck process/admin metadata only; later six scope gates bind current exact input'})
assert len(mapped)==31 and not any(q['gate'].startswith('scope-') for q in mapped)
# Exact older history in Registry is unchanged after removing one new record.
for i,n in enumerate(['AutoSamplingTheory/TechnicalLemmas/Registry.lean','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']):
 p=subprocess.Popen(['git','show',C+':'+n],cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();assert p.returncode==0;(O/f'history-v4-git{i}.stdout.RAW').write_bytes(out);(O/f'history-v4-git{i}.stderr.RAW').write_bytes(err)
 cur=(B/n).read_bytes().replace(b'\r\n',b'\n');base=out.replace(b'\r\n',b'\n')
 if n.endswith('.lean'):
  a=cur.index(b'  {\n    key := "pbps.actualProjectedRotation"');z=cur.index(b'  {\n    key := "pbps.actualReflectionIntertwining"',a);assert cur[:a]+cur[z:]==base
 else:
  cl=cur.splitlines(keepends=True);matches=[j for j,l in enumerate(cl) if D.encode() in l];assert len(matches)==1;assert b''.join(l for j,l in enumerate(cl) if j!=matches[0])==base
 print('HISTORY EXACT',n,'actualGitPID',p.pid,'EXIT',p.returncode)
result={'schema':'independent-history-and-gate-input70-v1','actual_PID':os.getpid(),'before_after_cell_deltas':diff,'handoff_exact_LF_diff':hd,'all31_earlier_input_changes_exhaustively_mapped':mapped,'six_final_scope_gate_current_inputs_exact':True,'Lean_and_publication_and_lesson_unchanged_during_gates':True,'Registry_one_exact_record_added_all_old_history_retained':True,'technical_memory_one_exact_record_added_all_old_history_retained':True,'original_e44_frontier_failure':'Native exact SCI frontier PID48288 EXIT1 retained; corrected c46 label supplement is separate independent verification.','INT69_remote_site_failure':'Current exact handoff retains old helper-panel-count CI failure and says current helper-aware local gate freshly exercised; no remote success inferred.','no_retrospective_pass_rewrite':True}
write('history70.checks.json',result);write('history70.additional-input-pins.json',{'count':len(extra),'LF_rule':'CRLF to LF only','inputs':extra});print('PASS history and exact gate-input mapping')
