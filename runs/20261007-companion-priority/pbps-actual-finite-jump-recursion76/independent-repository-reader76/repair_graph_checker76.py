import os
import review76 as r
path=r.O/'check_reader76.py'; raw=path.read_bytes()
before=r.O/'check_reader76.attempt2.RAW.py'; assert not before.exists();before.write_bytes(raw)
text=raw.decode()
old="""    for parent in ['ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']:
        assert any(edge['source']=='module:AutoSamplingTheory.ExampleCases.ProximalBPS.'+parent and edge['target']==mid and edge['relation']=='imports' for edge in graph['edges'])"""
new="""    literal_local_imports=['module:'+line.split()[1] for line in src.decode().splitlines() if line.startswith('import AutoSamplingTheory.')]
    direct_local_imports=[edge['source'] for edge in graph['edges'] if edge['target']==mid and edge['relation']=='imports']
    assert sorted(direct_local_imports)==sorted(literal_local_imports)==['module:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock']
    imported_edges=[edge for edge in graph['edges'] if edge['relation']=='imports']
    parent_paths={}
    for parent in ['ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']:
        origin='module:AutoSamplingTheory.ExampleCases.ProximalBPS.'+parent
        queue=[(origin,[origin])];seen=set();found=None
        while queue:
            node,path=queue.pop(0)
            if node==mid:found=path;break
            if node in seen:continue
            seen.add(node)
            queue.extend((edge['target'],path+[edge['target']]) for edge in imported_edges if edge['source']==node and edge['target'] not in seen)
        assert found is not None,parent
        parent_paths[parent]=found
        assert any(edge['source'].startswith('decl:'+origin[len('module:'):]+'.') and edge['relation']=='source reference (scanner)' for edge in direct)"""
assert old in text
text=text.replace(old,new)
text=text.replace('three_actual_parent_module_imports=True','actual_local_module_imports=direct_local_imports,three_actual_producer_module_import_paths=parent_paths')
path.write_text(text,encoding='utf-8',newline='\n')
r.save('checker-diagnosis2.json',dict(status='CHECKER_DIRECT_VERSUS_TRANSITIVE_IMPORT_ERROR',actual_diagnosis_writer_PID=os.getpid(),failed_actual_child_PID=19824,failed_actual_child_EXIT=1,failed_receipt=r.pin(r.O/'terminals/independent-finite-reader76-checks-literal-location.receipt.json'),original_checker=r.pin(before),corrected_checker=r.pin(path),finding='The literal current module directly imports ActualHazardClock plus two Mathlib modules. HarmonicFlow and BounceRate are available through the actual import chain; all three concrete producer declarations have correctly typed scanner-reference edges. The checker had incorrectly demanded three direct module imports.',repair='Compare direct local imports to the literal source, then independently find the actual imports paths for the three producer modules and verify each declaration scanner edge. No graph/input/canonical mutation.',mathematical_or_publication_failure=False))
print(r.json.dumps(dict(status='CORRECTED_IMPORT_TOPOLOGY_CHECKER_ONLY',actual_writer_PID=os.getpid())))
