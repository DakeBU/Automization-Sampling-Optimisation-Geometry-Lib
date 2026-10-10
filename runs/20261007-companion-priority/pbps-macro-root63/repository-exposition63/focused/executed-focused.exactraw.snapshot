from review63 import *
def focused():
 assert git('rev-parse','HEAD')==COMMIT
 names=git('ls-tree','-r','--name-only',COMMIT).splitlines()
 paths=[p for p in names if p.startswith(('AutoSamplingTheory/','Tests/','tools/','website/content/publications/','website/content/declaration_lessons/','research-wiki/semantic-roundtrip/','research-wiki/frontier-cells/')) and p.endswith(('.py','.lean','.json'))]
 paths+=['AutoSamplingTheory.lean','Tests.lean','research-wiki/process-memory.json','lean-toolchain','lake-manifest.json']
 before=[rawpin(ROOT/p) for p in sorted(set(paths))]
 write('focused.input.manifest.json',{'actual_pid':os.getpid(),'checked_commit':COMMIT,'before_independent_focused_validation':True,'paths':before,'selection':'Tracked committed canonical Lean/Test/tools/publication/lesson/audit/cell inputs only; uncommitted64 newcell/scratch/ledger tail excluded.'})
 sys.path.insert(0,str(ROOT/'tools'))
 import astis_frontier_cells as frontier,astis_publication as publication,astis
 cells=[]
 for p in names:
  if p.startswith('research-wiki/frontier-cells/') and p.endswith('.json') and not Path(p).name.startswith('_') and Path(p).name!='schema.json':
   c=json.loads(subprocess.check_output(['git','show',COMMIT+':'+p],cwd=ROOT));c['__path__']=p;cells.append(c)
 errors=frontier.validate_cells(cells);assert errors==[],errors
 # Isolate the exact committed cell population while validating existing publication bindings.
 frontier.load_cells=lambda root=frontier.DEFAULT_CELL_ROOT:cells
 publication.check_advance([DECL],reviewed=True)
 hits=astis.forbidden_pattern_hits();assert hits==[],hits
 after=[rawpin(ROOT/p) for p in sorted(set(paths))];assert before==after
 assert git('rev-parse','HEAD')==COMMIT
 write('focused.result.json',{'status':'PASS','actual_pid':os.getpid(),'checked_commit':COMMIT,'committed_cells_validated':len(cells),'reviewed_publication_declaration':DECL,'fake_closure_hits':hits,'input_pre_post_exact_raw_pins_equal':True,'input_count':len(before),'no_duplicate_Lean_build':'Actual root9170/Tests9465 receipts re-bound to exact integrated source; independent focused check covers final cell administration and reviewed publication/forbidden scan.'})
 print(json.dumps({'status':'PASS','actual_pid':os.getpid(),'committed_cells':len(cells),'reviewed_publication':True,'fake_hits':len(hits),'pre_post_pin_count':len(before)}))
if __name__=='__main__':focused()
