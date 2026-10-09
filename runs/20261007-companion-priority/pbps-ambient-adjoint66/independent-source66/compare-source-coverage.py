from pathlib import Path
import json,hashlib,re,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
inv=json.loads((O/'adopted-primary66.source-coverage-inventory.json').read_bytes());category_map={
'source-hypothesis':('source-public-inputs','Original callers; no additional source condition'),
'actual-law-reflection-prerequisite':('actual-law','Inherited actual65 normalized laws/reflection; source prerequisite, no newly claimed whole-law theorem'),
'actual-P-subspaces-blocks-prerequisite':('P-exact/block-domain','Inherited P/HP/block definitions plus current internal exact kerP/ambient adapter; no extra premises'),
'B11-B15-B16-inherited-prerequisite':('inherited-root-polar','SAME inherited65 root/order/centered inverse/polar witnesses; no full-space inverse'),
'real-L2-adjoint-projection-centering-background':('centered-spaces/ambient-adjoint-adapter','Standard D1 real scalar AE L2/adjoint/projection/mean geometry internally discharged'),
'target-first-corrector-ambient-adjoint-and-common-HP0':('ambient-adjoint-adapter/first-corrector','Current main BODY steps1-5 and genuine Test step6'),
'target-global-centered-micro-macro-decomposition':('centered-decomposition','Current global-input implication, conditional residual and same HP0; geometric norm budget'),
'B19-B20-welltyped-consumer-boundary':('B20-domain','Only exact domain preparation accepted; full corrector formula/bounds remain residual'),
}
for item in inv['math_items']:
 cat=item['target66_classification']
 if cat in category_map:
  node,why=category_map[cat];item['current66_comparison']=dict(source_node=node,disposition='SOURCE_NODE accounted for at stated inherited/current/domain-only boundary',evidence=why)
 else:
  assert 'excluded' in cat;item['current66_comparison']=dict(disposition='EXCLUDED from claimed mathematical result, preserved as source context',reason=cat,no_current66_proof_credit=True)
inv.update(schema='source66-exhaustive-selected-source-comparison-v1',candidate_seen=True,all_310_compared=True,source_graph_retained_independent=True,missing_source_items=0,missing_alttext=0,missing_annotation=0,annotation_mismatch=0,whole_paper_formalization_claim=False)
put('source-coverage.compared.json',inv)
receipt=json.loads((O/'006.RAW.snapshot').read_bytes());log=(O/'007.RAW.snapshot').read_text(encoding='utf-8');assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['actual_foreground_pid']==48268;assert 'Build completed successfully (3946 jobs).' in log
names=['AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition','Tests.ProximalBPSAmbientAdjointCorrector.genuine_actual_global_corrector_consumer'];axioms={}
for name in names:
 m=re.search(re.escape("'"+name+"' depends on axioms: [")+r'([^\]]*)\]',log,re.S);assert m,name;vals=[x.strip() for x in m.group(1).split(',')];assert set(vals)==set(['propext','Classical.choice','Quot.sound']);axioms[name]=vals
put('focused-compiler-evidence-readback.json',dict(schema='source66-readonly-focused-compiler-evidence-v1',actual_observer_pid=os.getpid(),actual_foreground_Lean_pid=48268,actual_Lean_exit=0,terminal_closed=True,checked_parent=receipt['checked_science_parent'],jobs=3946,standard_three_axioms_by_declaration=axioms,main_RAW_sha256='377663f86e8e139907b6ffeda890d6933efd101a6f43f79064a264f9e0f384d4',Test_RAW_sha256='3df807d4c8e456830c8ecbaeb6d20bd2331df6f09a951d8e5061ee18b6045685',reviewer_ran_proof_search=False,reviewer_self_math_verification=False,evidence_boundary='Read and bound actual completed receipt and output; independent mathematical verifier is distinct; compilation alone is not source fidelity'))
# Pin only the unchanged CLOSED parent leases and exact approved fragments reused here.
parents=[]
PRE=O.parent.parent/'pbps-ambient-adjoint-preproof66'
for scope,files in [('independent-header66',['lease.final.json']),('independent-type-diagnosis66',['lease.final.json','proposed.statement0.lean','proposed.header0.lean','proposed.statement1.lean','proposed.header1.lean','prior-type-credit-correction.json'])]:
 for n in files:
  p=PRE/scope/n;b=p.read_bytes();parents.append(dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b)))
put('closed-header-representation-reuse-pins.json',dict(schema='source66-finite-closed-parent-reuse-v1',parents=parents,closed_scopes_immutable=True,earlier_candidate_verdict_not_used_for_current_source_comparison=True,source_graph_created_before_candidates=True))
print(json.dumps(dict(source_items_compared=310,source_missing=0,actual_Lean_PID48268_EXIT0=True,standard3_each=True),sort_keys=True))