from pathlib import Path
import json,hashlib,subprocess,datetime,os,sys
R=Path('E:/Samplinglib');pre=Path(__file__).parent;r=pre.parent/'pbps-actual-finite-history-tail-law87'
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
checks=[]
for label,args in [
 ('local-history',['rg','-n','unused.clock|finite.history|head.tail|prefix|tail.*indep','AutoSamplingTheory/ExampleCases/ProximalBPS','AutoSamplingTheory/TechnicalLemmas/Probability']),
 ('shared-frontiers',['rg','-l','unused.clock.tail|finite.history.*tail|head.tail','research-wiki/frontier-cells','-g','*.json']),
 ('fixed-mathlib',['rg','-n','indep_iSup_of_disjoint|iIndepFun_iff_iIndep|indep_of_indep_of_le|map_infinitePi_infinitePi_of_inj|comap_process_pi|measure_inter_preimage_eq_mul|map_prod_eq_prod_map_map','\.lake/packages/mathlib/Mathlib/Probability/Independence','\.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace']),
 ('compatible-upstream',['rg','-n','head.tail|clock.tail|finite.history|prefix.*indep','research-wiki/external-lean-libraries','research-wiki/openai-math-2026-intake.json'])]:
 args=[s.removeprefix('\\') for s in args]
 q=subprocess.run(args,cwd=R,capture_output=True)
 p=pre/(label+'.retrieval.stdout.log');p.write_bytes(q.stdout)
 e=pre/(label+'.retrieval.stderr.log');e.write_bytes(q.stderr)
 assert q.returncode in (0,1),(label,q.stderr)
 checks.append({'label':label,'argv':args,'exit_code':q.returncode,'stdout':pin(p),'stderr':pin(e)})
graphs=pre.parent/'pbps-actual-finite-first-event-law86'
g=graphs/'topology-repair-review86/source-proof-graph86.single-edge-proposed-successor.json'
inv=graphs/'independent-source86/source-inventory86.exhaustive-successor.json'
assert pin(g)['raw_sha256']=='c7ed4b13d3471c42d2e516edfef3009345ce156e961685a0ad6f11344aa0f7d8'
assert pin(inv)['raw_sha256']=='cd5f487c3091946ab0699c4c50203a1703ff8b6e0f44a67cfa86920c9a26db3f'
parents=[R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
new(pre/'retrieval87.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'actual_compiled_parents':[pin(p) for p in parents],'decision':'adapt_existing: derive finite-prefix causality/past measurability of literal actual recursion; reuse fixed Mathlib disjoint sigma-algebra independence and infinitePi injective reindexing. No generic duplicate head-tail theorem or external port.','canonical_shared_substrate':'UnitExponentialProduct.unit_exponential_product_laws + fixed Mathlib independence/product-map APIs','shared_floor_classification':'adapt','planned_consumers':['G86-13 deterministic finite-event density factor iteration','G86-14 final finite-horizon survival conditional on generated live history'],'known_compiled_consumers':[],'upstream_compatibility':'SLT pinned Lean4.32.0 incompatible as dependency; no SLT or OpenAI theorem used. Mathlib pinned db584cd6d46c92f209a44c0f1c829460d327499d, Apache2.0.','global_source_graph_reused_unchanged':pin(g),'global_source_inventory_reused_unchanged':pin(inv),'truth_boundary':'This is the probability substrate part of G86-11. Conditional random-hazard/wait integration is a separate residual edge. Physical-time residual memorylessness, random stopping index, fullA7 and paper/main/composition completion stay open.'})
new(pre/'source-slice87.json',{'kind':'source-first dependency slice; not a Lean dependency certificate','primary_first_freeze':pin(pre/'independent-source-first87/source-first.freeze.native.json'),'global_source_graph':pin(g),'global_source_inventory':pin(inv),'nodes':[{'id':'S87-I1','claim':'Actual stopped finite history is measurable in consumed clock prefix','classification':'SOURCE_IMPLICIT_REQUIRED','anchors':['A1.SS1.p2/A1.E1/A1.E2','A1.SS2 joint Borel recursion paragraph']},{'id':'S87-I2','claim':'Mutual iid independence extends to disjoint prefix/tail generated sigma algebras','classification':'SOURCE_IMPLICIT_REQUIRED','anchors':['A1.SS1.p2/A1.E1/A1.E2']},{'id':'S87-I3','claim':'Actual finite history is independent of unchanged full unused clock tail','classification':'SOURCE_IMPLICIT_REQUIRED','anchors':['A1.SS1.SSS0.Px1.p4/A1.E7']},{'id':'S87-I4','claim':'Conditional random-hazard next-wait and final-survival integration','classification':'OPEN_NOT_CLOSED_BY_THIS_SAU','anchors':['A1.SS1.SSS0.Px1.p4/A1.E7']}],'dependencies':[{'from':'S87-I1','to':'S87-I3'},{'from':'S87-I2','to':'S87-I3'},{'from':'S87-I3','to':'S87-I4'}],'global_node_refinement':'S87-I1/I2/I3 are probability substrate of G86-11, not closure of all G86-11; G86-13/G86-14/G86-15 remain open. No unreviewed global-topology rewrite.','exclusions':[{'region':'Global A7 density iteration, non-explosion, reversal, invariance and semigroup analysis','reason':'Unchanged exhaustive reviewed global inventory reused; outside this strictly bounded source slice.'}],'topology_origin':'Independent primary-first source87 S87-I1/I2/I3/I4/I5, frozen before candidate exposure. Root records the same dependency slice; no Lean proof/body consulted.'})
# Preserve the failed syntax attempts and initial receipt. Distinct final receipt.
new(r/'header87.syntax-diagnosis.json',{'class':'HEADER_PARSER_BINDER_NAME','math_statement_changed':False,'attempts':['header87.syntax-attempt1.lean','header87.syntax-attempt2.lean'],'resolution':'Use ASCII w/w\u0027 as bound sample names; same literal functions and quantifiers. No proof search occurred.','candidate':pin(r/'header87.proposed.lean')})
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
q=subprocess.run([str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(r/'header87.proposed.lean')],cwd=R,env=env,capture_output=True)
(r/'header87.typecheck-final.stdout.log').write_bytes(q.stdout);(r/'header87.typecheck-final.stderr.log').write_bytes(q.stderr)
new(r/'header87.typecheck-final.receipt.json',{'exit_code':q.returncode,'terminal_closed':True,'header':pin(r/'header87.proposed.lean')});assert q.returncode==0
print('RAW source freeze/spans and prior exhaustive graph reverified; retrieval/source slice recorded; unchanged mathematical header final typecheck PASS.')
