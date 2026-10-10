from pathlib import Path
import copy,datetime,difflib,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;H=O.parent/'header84.proposed.lean';S=O/'header84.syntax-only-proposed.lean';B=R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
assert info(H)['RAW_sha256']=='936b76036df8d283acb212f2f1ba780c4446aa2e1c7dc84bfdff0ff9c02f29b0'
assert info(S)['RAW_sha256']=='5c4e379caa337d1ac903d509eca30ef7db7b1905715c7a65b878afb33f9d2ded'
assert S.read_bytes()==H.read_bytes().replace(b'set_option maxHeartbeats 1600000 in\n',b'')
assert info(B/'overlay-review84/topology-overlay.decision84.json')['RAW_sha256']=='eafcb63f0d819023fa1f68d303e997e936c7d6939f9576c6e0ec98bf57cb9035'
assert info(B/'overlay-review84/topology-overlay.run-manifest84.json')['RAW_sha256']=='5548e80396c8a3a9285a09075e34a4dd7300ed1acbeb21c03575a84e957933f5'
g=load(B/'source_proof_graph84.json');i=load(B/'source_inventory84.json');overlay=load(B/'independent-topology84/proposed-minimal-topology-overlay84.json')
for op in overlay['operations']:
 kind=op['operation']
 if kind=='append_node':g['nodes'].append(op['value'])
 elif kind=='append_edge':g['edges'].append(op['value'])
 elif kind=='replace_edge_field':
  e=next(e for e in g['edges'] if e['id']==op['edge_id']);assert e[op['field']]==op['old'];e[op['field']]=op['new']
 elif kind=='append_junction_edge':next(j for j in g['junctions'] if j['id']==op['junction_id'])['edges'].append(op['value'])
 elif kind=='replace_junction_field':
  j=next(j for j in g['junctions'] if j['id']==op['junction_id']);assert j[op['field']]==op['old'];j[op['field']]=op['new']
 elif kind=='append_inventory_graph_node':next(e for e in i['items'] if e['id']==op['inventory_id'])['graph_nodes'].append(op['value'])
 elif kind=='append_scope_coverage_graph_node':next(e for e in g['scope_coverage'] if e['inventory_id']==op['inventory_id'])['graph_nodes'].append(op['value'])
 elif kind=='replace_graph_counts':assert g['counts']==op['old'];g['counts']=op['new']
 else:raise AssertionError(kind)
ge=load(B/'source_proof_graph84.reviewed-effective.json');ie=load(B/'source_inventory84.reviewed-effective.json')
for k in ['nodes','edges','junctions','counts','scope_coverage']:assert ge[k]==g[k],k
for k in ['items','primary','source_anchor_coverage']:assert ie[k]==i[k],k
save('source-overlay-readback84.json',dict(status='PASS_MECHANICAL_EXACT_ADOPTION',accepted_distinct_decision=info(B/'overlay-review84/topology-overlay.decision84.json'),accepted_distinct_manifest=info(B/'overlay-review84/topology-overlay.run-manifest84.json'),exact_proposal=info(B/'independent-topology84/proposed-minimal-topology-overlay84.json'),effective_graph=info(B/'source_proof_graph84.reviewed-effective.json'),effective_inventory=info(B/'source_inventory84.reviewed-effective.json'),counts=ge['counts'],syntax_overlay_is_separate_and_not_yet_accepted=True))
h=S.read_text(encoding='utf8');tail='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity';assert h.count(tail)==1
checks='\n#check actual_outer_bounded_l2_continuity_statement\n#check MeasureTheory.StronglyMeasurable.integral_prod_right\n#check MeasureTheory.tendsto_integral_filter_of_dominated_convergence\n#check MeasureTheory.isProbabilityMeasure_tilted\n#check MeasureTheory.tilted_tilted\n#check AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel\n'
probe=O/'Header84CompletePrivatePropSyntaxProposalLocalCheck.lean';text=h.replace(tail,checks+tail);assert text.replace(checks,'')==h
with probe.open('x',encoding='utf8',newline='\n') as f:f.write(text)
with (O/'local-check-only84.diff').open('x',encoding='utf8',newline='\n') as f:f.writelines(difflib.unified_diff(h.splitlines(True),text.splitlines(True),fromfile=S.name,tofile=probe.name))
args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)];env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'syntax-proposal-typecheck84.stdout.log').open('xb') as out,(O/'syntax-proposal-typecheck84.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('Complete private syntax proposal foreground PID',child.pid,flush=True);code=child.wait()
save('syntax-proposal-typecheck84.receipt.json',dict(status='PASS' if code==0 else 'FAIL',command_argv=args,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_header=info(H),syntax_proposal=info(S),complete_named_private_Prop=info(probe),stdout=info(O/'syntax-proposal-typecheck84.stdout.log'),stderr=info(O/'syntax-proposal-typecheck84.stderr.log'),only_overlay='Remove one misplaced control line, then add local #check signatures before existing section end; full mathematical Prop preserved.',original_typecheck_retained=info(O/'original-typecheck84.receipt.json'),distinct_syntax_repair_acceptance=False,proof_BODY=False))
for e in load(O/'input-freeze84.json')['inputs']:assert info(R/e['path'])==e
print('COMPLETE SYNTAX PROPOSAL EXIT',code,flush=True)
raise SystemExit(code)
