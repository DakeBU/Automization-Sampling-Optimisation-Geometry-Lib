from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
def pin(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
labels=['focused-both-staged-v10','focused-both-local-consumer-v11','focused-both-final-v12']
receipts=[json.loads((r/x/'receipt.json').read_bytes()) for x in labels]
assert all(x['terminal_closed'] for x in receipts)
assert [x['exit_code'] for x in receipts]==[1,0,0]
negative=(r/labels[0]/'stdout.log').read_text(encoding='utf-8')
assert 'TRACE66 reconstructed outer witnesses' in negative
assert 'TRACE66 actual global witnesses' not in negative
final=(r/labels[2]/'stdout.log').read_text(encoding='utf-8')
assert 'Build completed successfully (3946 jobs)' in final
decls=['AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition','Tests.ProximalBPSAmbientAdjointCorrector.genuine_actual_global_corrector_consumer']
for name in decls:
    found=re.search(re.escape("'"+name+"'")+r' depends on axioms: \[([^\]]+)\]',final)
    assert found and set(re.findall(r'\w+(?:\.\w+)*',found[1]))=={'propext','Classical.choice','Quot.sound'}
test=Path('Tests/ProximalBPSAmbientAdjointCorrector.lean')
assert 'TRACE66' not in test.read_text(encoding='utf-8')
out=r/'consumer-reconstruction66.resolution.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='LOCAL_EXPLICIT_CONSUMER_THEN_EXISTING_WITNESS_RECONSTRUCTION_COMPILED',receipts=[pin(r/x/'receipt.json') for x in labels],strict_reduction='Staged outer constructors completed in v10; timeout was after that construction. The same consumer was then proved as a local explicitly typed fact before reconstructing the unchanged deep public proposition.',resolution='The local consumer derives every original actual-input decomposition and squared norm budget from the same produced R and global implication. It is proved internally and never becomes a caller premise,private provider or separate credited declaration.',final_test=pin(test),final_standard_axioms=['propext','Classical.choice','Quot.sound'],final_jobs=3946,source_mathematical_statement_changed=False,heartbeat_budget_increased=False,temporary_traces_removed=True,independent_reviews_pending=True,PROVED_LOCAL=False,VERIFIED=False,full_paper_Goal=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS retained v10 negative; v11 and final v12 EXIT0,3946/standard3 both. Exact original statement preserved; no independent acceptance inferred.')
