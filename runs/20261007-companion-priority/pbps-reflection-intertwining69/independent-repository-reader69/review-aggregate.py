import hashlib,json,os,pathlib,re,subprocess,sys
sys.dont_write_bytecode=True
from snapshot_named_inputs import snapshot
out=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((out/n).read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
packet=load('final-reader-repository-packet69.RAW.json');manifest=load('final-input-manifest.json')
pathmap={pathlib.Path(e['original_path']).as_posix().lower():e for e in manifest['final_current_inputs']}
current=lambda name:(out/name).read_bytes()
commit='2d286c283a6fb5dfc13180204bb0da54531a5c67'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(out.parents[3])).decode('ascii').strip()
assert head==commit
for now,old in [('current.014.ReflectionIntertwining.lean','accepted-source211.current.ReflectionIntertwining.RAW.lean'),
                ('current.017.pbps-actual-reflection-intertwining.json','accepted-source211.final.publication.RAW.json'),
                ('current.018.pbps-actual-reflection-intertwining.json','accepted-source211.final.lesson.RAW.json')]:
    assert current(now)==current(old),now
registry=current('current.003.Registry.lean').decode('utf-8')
public='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining'
assert registry.count('localDecl := "'+public+'"')==1
assert registry.count('key := "pbps.actualReflectionIntertwining"')==1
assert len(re.findall(r'status\s*:=\s*LemmaMemoryStatus\.formalizedLocal',registry))==517
assert current('current.002.ExampleCases.lean').decode('utf-8').splitlines().count('import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining')==1
assert 'example : TechnicalLemmas.formalizedTechnicalLemmaCount = 517 := by native_decide' in current('current.004.Basic.lean').decode('utf-8')
notes=load('current.023.integration.notes.json');assert len(notes['checks'])==17
gates=[]
for c in notes['checks']:
    path='E:/Samplinglib/'+c['receipt']['path'] if not c['receipt']['path'].startswith('E:') else c['receipt']['path']
    entry=pathmap[pathlib.Path(path).as_posix().lower()];r=load(entry['name'])
    assert r['exit_code']==0 and r['terminal_closed'] and r['checked_parent']==commit
    assert sha(current(entry['name']))==c['receipt']['raw_sha256']
    gates.append(dict(label=c['label'],actual_pid=r['actual_foreground_pid'],actual_exit=r['exit_code'],terminal_closed=True,
        checked_parent=r['checked_parent'],receipt_name=entry['name'],started_utc=r['started_utc'],finished_utc=r['finished_utc']))
mandatory=load('current.028.receipt.json');log=current('current.029.stdout.log').decode('utf-8')
assert mandatory['actual_foreground_pid']==38812
assert 'Build completed successfully (9179 jobs).' in log and 'Build completed successfully (9479 jobs).' in log and 'ASTIS check passed' in log
cell=load('current.020.ASTIS-SW-PBPS-actual-reflection-intertwining.json')
assert cell['status']=='independently_verified'
assert cell['parents']==['ASTIS-SW-PBPS-actual-root-inverse-commutation','ASTIS-SW-PBPS-reflection-l2-blocks']
assert cell['purification']['status']=='pending'
assert cell['evidence']['serialized_shared_gate']['proof_commit']==commit
audit=load('current.019.ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json')
assert audit['source_review']['review_run_sha256']=='f1e5024fe6afdaedae4ac5f9b2dfc48bc86e09da51b490212c392bbc9bf2ce90'
assert audit['source_review']['state']=='accepted' and audit['publication_binding_sha256']=='571c2916738f1981c5074a9a5f4e1cdf3efce3f94fafd26670566c70c3b25152'
graph=load('current.015.underlying-lean-graph.json');target='decl:'+public
module='module:AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining'
incident=[e for e in graph['edges'] if e.get('source') in [target,module] or e.get('target') in [target,module]]
assert not any('SharpCorrectorEnergy' in json.dumps(e) for e in incident)
assert any(e['source']=='module:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation' and e['target']==module and e['relation']=='imports' for e in incident)
assert any(e['source']==module and e['target']==target and e['relation']=='declares' for e in incident)
assert graph['publication_inputs_sha256']==notes['publication_inputs_sha256']
assert sha(current('current.015.underlying-lean-graph.json'))==notes['current_graph']['raw_sha256']
assert sha(current('current.020.ASTIS-SW-PBPS-actual-reflection-intertwining.json'))==notes['final_cells'][0]['raw_sha256']
assert 'not elaborated proof dependencies' in graph['reference_contract']
events=[json.loads(l) for l in current('current.008.substantive_advances.jsonl').decode('utf-8').splitlines() if 'ASTIS-SA-20261009-PBPSActualReflectionIntertwining' in l]
verified=[e for e in events if e.get('to_state')=='VERIFIED'];assert len(verified)==1
assert verified[0]['worker_id']!='/root'
extras=[];negative_receipts=[]
for label,pid in [('semantic',47776),('frontier',46100)]:
    folder=out.parent/'integration69'/label
    for filename in ['receipt.json','stdout.log','stderr.log']:
        extras.append(snapshot(out,folder/filename,'negative-root.%s.%s'%(label,filename),'retained root wrong CLI negative; not PASS'))
    r=load('negative-root.%s.receipt.json'%label)
    assert r['actual_foreground_pid']==pid and r['exit_code']==2 and r['terminal_closed']
    negative_receipts.append(dict(label=label,actual_pid=pid,actual_exit=2,typed='wrong CLI subcommand; corrected distinct command passes'))
manifest['extra_named_negative_inputs']=extras;manifest['count']+=len(extras)
(out/'final-input-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8')
result=dict(schema='repository-reader69-bounded-current-aggregate-review-v1',actual_pid=os.getpid(),head=head,
    immutable_module_publication_lesson_identical_to_source211=True,registry_count=517,single69_registry_entry=True,
    ExampleCases_import_once=True,Tests_count_guard517=True,root_jobs=9179,test_jobs=9479,publication_units=238,
    actual_successful_gates=gates,actual_successful_gate_count=17,negative_CLI_attempts=negative_receipts,
    final_cell_RAW_sha256=notes['final_cells'][0]['raw_sha256'],final_graph_RAW_sha256=notes['current_graph']['raw_sha256'],
    final_publication_inputs_sha256=graph['publication_inputs_sha256'],affected_graph_incident_edges=incident,
    graph_reference_contract=graph['reference_contract'],cell_parents=cell['parents'],paper_consumers=cell['consumers'],
    independently_VERIFIED_event=verified[0],source_admission_reused=audit['source_review'],
    no_new_math_or_source_verdict=True,
    receipt_scope_note='Mandatory PID38812 bound unchanged SCI69 Lean. Its cell pin predates the admin-only shared-gate update; final cell and graph are pinned by later final-admin frontier/publication/semantic/contributor/graph/site receipts and final root packet.',
    graph_limitations='Name-scanned declaration references are incomplete and may include incidental name matches. The actual ReflectionL2 parent is preserved in the frontier cell and unchanged module proof; the graph is not an elaborated dependency certificate.',
    remaining_truth_boundary=notes['remaining'],prior66_graph_freshness_withheld_preserved=True,
    no_full_Exposition_PURIFIED_main_live_wholepaper_or_Goal_claim=True)
(out/'bounded-current-aggregate-review.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_pid=os.getpid(),head=head,successful_gates=17,registry_count=517,root_jobs=9179,test_jobs=9479,
    final_graph_RAW_sha256=result['final_graph_RAW_sha256'],complete_named_inputs=manifest['count']),sort_keys=True))
