from verify64 import *
def gates():
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==PARENT
 results=[]
 cmds=[('publication',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',PARENT]),('contributor',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('focused-reviewed-fakeclosure',[PY,'-B','-X','utf8',str(OUT/'gates64.py'),'direct'])]
 for label,args in cmds:
  r=command(label,args);results.append({'gate':label,'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'terminal_closed':r['terminal_closed'],'receipt':rawpin(OUT/label/'receipt.json')});print(json.dumps(results[-1]),flush=True)
 write('gates.result.json',{'status':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL','checked_commit':COMMIT,'parent':PARENT,'actual_observer_pid':os.getpid(),'fresh_focused_gates':results,'whole_astis_or_site_gate_run':False,'aggregate_integration':False})
 assert all(x['exit_code']==0 for x in results)
def direct():
 sys.path.insert(0,str(ROOT/'tools'));import astis_publication as pub,astis
 pub.check_advance(DECLS,reviewed=True);hits=astis.forbidden_pattern_hits();assert not hits,hits
 paths=[x['path'] for x in load(OUT/'mathematics-reuse.json')['three_exact_SOURCE_files']];private=[];decls=[];imports=[]
 for rel in paths:
  s=(ROOT/rel).read_text(encoding='utf-8');private+=re.findall(r'^private\s+(?:theorem|lemma|def|opaque|axiom)\s+(\S+)',s,re.M);decls+=re.findall(r'^(?:theorem|lemma|def|opaque|axiom)\s+(\S+)',s,re.M);imports.append({'file':rel,'imports':re.findall(r'^import (.+)$',s,re.M)})
 assert private==[] and decls==['positive_square_order','actual_centered_root_order_inverse','genuine_actual_centered_inverse_consumer']
 write('focused-reviewed-fakeclosure.result.json',{'status':'PASS','checked_commit':COMMIT,'actual_pid':os.getpid(),'reviewed_publication_declarations':DECLS,'repository_forbidden_pattern_hits':hits,'new_private_providers':private,'three_declarations_only':decls,'imports':imports,'import_assessment':'Generic leaf uses existing complex lift and targeted CFC order; actual node reuses accepted63 macro root plus SAME rough-gradient/Poincare production parents; genuine Test imports actual node. Shared root/Registry/Tests integration deferred.'});print(json.dumps({'status':'REVIEWED_PUBLICATION_AND_FAKE_CLOSURE_PASS','pid':os.getpid(),'reviewed_declarations':2,'private_providers':0,'forbidden_hits':0}))
if __name__=='__main__':direct() if len(sys.argv)>1 and sys.argv[1]=='direct' else gates()
