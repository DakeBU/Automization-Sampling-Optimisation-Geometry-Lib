import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime,collections
O=pathlib.Path(__file__).resolve().parent;S=O.parent/'independent-source-first71';OLD=O.parents[1]/'pbps-actual-projected-rotation70/independent-source70'
H=lambda b:hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def put(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
manifest=J(S/'outputs.manifest.json');lease=J(S/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['owned_file_count']==116
for e in manifest['files']:
 b=pathlib.Path(e['path']).read_bytes();assert H(b)==e['raw_sha256'] and len(b)==e['raw_bytes'];assert H(b.replace(b'\r\n',b'\n'))==e['lf_sha256']
assert H((OLD/'lease.final.json').read_bytes())=='d3974254b5a27965de598361a64dc52439441357a5f95a2a30863d7ac4b09779'
oldgraph=OLD/'stageA.source-proof-graph70.frozen.json';assert H(oldgraph.read_bytes())=='f23f7c687517e9b65de67c549e8cf5e11328d01fea6f8b35236a14679f68dc26'
put('stageA.source-first-provenance-and-reuse.json',{'source_first71_CLOSED_owned_count':116,'opaque_manifest_files_checked':len(manifest['files']),'manifest_RAW_sha256':H((S/'outputs.manifest.json').read_bytes()),'lease_RAW_sha256':H((S/'lease.final.json').read_bytes()),'source_first_actual_close_worker_PID':lease['actual_close_worker_PID'],'source_first_actual_close_worker_EXIT':lease['actual_close_worker_exit_code'],'source_first_prior_decision_or_interface_read':False,'unchanged70_source_binder_background_reused_honestly':True,'original70_closed_count':319,'original70_lease_RAW_sha256':'d3974254b5a27965de598361a64dc52439441357a5f95a2a30863d7ac4b09779','original70_source_only_graph_RAW_sha256':H(oldgraph.read_bytes()),'original70_source_graph_nodes':22,'original70_source_graph_edges':49,'old_source_or_header_math_verdict_substituted_for71':False,'no_old_writes':True})
roles={'A2.E20.m1':('P15','same-centered-corrector-definition'),'A2.Ex10.m1':('P13','actual-ideal-update-retained-parent70'),'A2.SS3.p5.m7':('P13','same-actual-g-retained-parent70'),'A2.Ex11.m1':('P13','actual-output-components-retained-parent70'),'A2.Ex12.m1':('P14','actual-rotation-retained-parent70'),'A2.Ex16.m1':('P17','actual-C-difference-new-conclusion'),'A2.Ex17.m1':('P16','substitute-actual-rotation-into-same-C'),'A2.E21.m1':('P17','exact-minus-fP-square-plus-fV-square'),'A2.E27.m1':('P19','actual-B4-comparator-consumer-only'),'A2.Ex36.m1':('P20','B4-adds-exact-B21-consumer-only'),'A2.E28.m1':('P20','B4-corrector-error-identity-consumer-only')}
inv=J(O/'stageA.independent-RAW-math-inventory.json');out=[]
for q in inv['items']:
 e=dict(q)
 if q['id'] in roles:e.update(classification='NODE',source_node=roles[q['id']][0],reason=roles[q['id']][1])
 else:e.update(classification='EXCLUDED',source_node=None,reason='Outside this prospective71 header delta: unchanged70/global/D1 background is explicitly reused without full replay, or separate sharp-energy/modified-Lyapunov/B4-error/decay/cost boundary. Not a new71 premise or proof claim.')
 out.append(e)
counts=dict(collections.Counter(q['classification'] for q in out));assert counts=={'EXCLUDED':244,'NODE':11}
put('stageA.finite-source255-and-target18-coverage.frozen.json',{'schema':'prospective-header71-source-only-bounded-coverage-v1','count':255,'counts':counts,'unclassified':0,'RAW_regions':4,'target_formulas':18,'target_NODE':11,'target_EXCLUDED':7,'entries':out,'not_whole_source_replay_or_implementation_coverage':True})
ob=[
('H00','Exactly the original six analytic callers hα,hαβ,hV,hH,hη,hβη, same finite real Hilbert/Borel structural data.'),
('H01','Retain all12 common SAME witnesses S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R before every centered f; all parent70 clauses remain.'),
('H02','Corrector is C(u,v)=(1/2)*(||u||²-||v||²)-inner(A0(Inv u),v), on HP0×HP0 with the SAME A0 and SAME centered Inv.'),
('H03','Inv remains two-sided inverse of SAME ΓP0 only on HP0; no inverse on allHP or alternate root/polar witnesses.'),
('H04','Actual f globalzero-mean; fP actual condExp, fperp=Rf, fV=V0*Rf; old ambient adjoint/norm conclusions retained.'),
('H05','Same actual g=U(Pf-(f-Pf)), internal mean(g), gP actual condExp g, gperp=Rg,gV=V0*Rg; never RHS-defined coefficients.'),
('H06','Retain exact parent70 actual rotation signs and pair-energy conservation, not only abstract coefficient-vector identities.'),
('H07','Add exactly C(gP,gV)-C(fP,fV)=-||fP||²+||fV||², not a modified/weighted/sharp bound or opposite sign.'),
('H08','All original parent literal clauses, global-f conclusions and common witness scope remain byte-equivalent after removing only the new local corrector/value clause.'),
('H09','No extra probability/root/mean/commutation/rotation certificate caller, provider witness, ontoV, positive rank, 68sharpenergy parent, H1/extra smoothness or ρ/ω/c0 condition.'),
('H10','Rank0/HP0={0} and legal αη=1 endpoint retained; C and Inv are well-defined even on zero centered space.'),
('H11','P19/P20 B4 uses actual same g and B21 in B28; B4 errors/dynamics/main/query costs/composition remain open and are not header conclusions.'),
('H12','Named private literal may store complete proposition, never supply proof; future reader must expose complete exact literal adjacent to public signature/proof.'),
('H13','This prospective header review is not71 implementation/compilation/full-source acceptance, blind roundtrip or SAU VERIFIED; no proof search or canonical edits.')]
exposure={'schema':'prospective-header71-anti-anchoring-exposure-v1','task_description_seen':'Parent disclosed intended exact actual C-change delta and retained70 data before this pass.','primary_and_source_only71_material_seen':['source.regions.json','source.formulas.exact.json','source.math.inventory.json','opaque outputs.manifest.json/lease.final.json metadata'],'current71_header_or_proposal_seen':False,'current71_proof_exists_or_seen':False,'prior_header_math_verdict_seen':False,'parent70_exposure':'Reviewer previously performed full70 source review and knows parent statements/BODY; reused unchanged source/binder background explicitly. No70 source acceptance substitutes current71 header comparison.','sourcefirst71_verdict_or_interface_seen':False,'reading_aid_v1_retired':'Numeric placeholder prefix collision distorted later displayed formulas. Original RAW and all formula hashes/offsets unaffected. Correct v2 single-pass regex read occurred before this freeze.','freeze_before_current_header':True}
put('stageA.anti-anchoring-exposure.frozen.json',exposure)
put('stageA.source-expectations71.before-header.frozen.json',{'schema':'prospective-header71-primary-first-independent-expectation-v1','actual_pid':os.getpid(),'freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current71_header_seen':False,'fixed_primary_RAW_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','source_nodes':['P13','P14','P15','P16','P17','P19','P20'],'source_delta':'P16 exact same-C algebra applied to parent70 actual projected components yields P17 exact B21 corrector change; P19/P20 real B4 consumers, not extra assumptions or conclusions.','C_definition':'C(u,v)=1/2*(||u||²-||v||²)-<A0(Inv u),v> on SAME HP0×HP0','new_actual_conclusion':'C(gP,gV)-C(fP,fV)=-||fP||²+||fV||²','obligations':[{'id':k,'expectation':v,'status':'before-header-not-yet-compared'} for k,v in ob],'obligation_count':len(ob),'coverage':{'regions':4,'math_items':255,'NODE':11,'EXCLUDED':244,'exact_target_formulas':18},'source_hypothesis_is_binder_proof_ingredient_is_edge':True,'no_current_header_math_verdict_or_implementation_seen':True})
print(json.dumps({'actual_pid':os.getpid(),'StageA_frozen_before_header':True,'obligations':len(ob),'coverage':counts,'sourcefirst_opaque_checked':len(manifest['files']),'expectation_RAW_sha256':H((O/'stageA.source-expectations71.before-header.frozen.json').read_bytes())},ensure_ascii=False))
