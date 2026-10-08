from verify import *
old=load(D/'before-admin.json');claim=load(R/'proved-local.json')
for m in old['canonical_mappings']: assert matches(m['original'],path(m['original']['path']))
cell=ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-l2-pullback-range.json';q=load(cell);assert q['route']=='samplewiki-route' and q['shared_floor_audit']['decision']=='new_canonical_shared';q['route']='shared';write(cell,q)
cell=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-centered-macro-defect-gap.json';q=load(cell);name='AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange.actual_macroscopic_centered_range';assert name not in q['reuse_plan']['reused_declarations'];q['reuse_plan']['reused_declarations'].append(name);write(cell,q)
write(D/'administrative-correction.json',dict(status='EXACT_TWO_AUTHORIZED_METADATA_CORRECTIONS',source_or_proof_change=False,current_science_commit=SCI,corrections=[dict(path='research-wiki/frontier-cells/ASTIS-SHARED-l2-pullback-range.json',pointer='/route',old='samplewiki-route',new='shared',actual_failed_gate=pin(D/'gate.frontier.status.json')),dict(path='research-wiki/frontier-cells/ASTIS-SW-PBPS-centered-macro-defect-gap.json',pointer='/reuse_plan/reused_declarations/-',new=name,actual_failed_gate=pin(D/'gate.contributor.status.json'))],optional_source_review_lists_preserved=True,independent_verification_STRING_required_at_verified_status=True,source_review_list_prediction_corrected=True))
py=sys.executable
records=[]
for name,args in [('frontier',[py,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[py,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base','origin/main'])]:records.append(dict(name=name,**command('gate.corrected.'+name,args)))
records=[dict(name=n,**load(D/('gate.'+n+'.status.json'))) for n in ['reviewed-publication','publication-base','semantic']]+records
write(D/'gates.json',dict(status='PASS',actual_driver_PID=os.getpid(),focused=load(D/'focused.status.json'),records=records,retained_first_negatives=[pin(D/'gate.frontier.status.json'),pin(D/'gate.contributor.status.json')],no_duplicate_compiler=True))
print('PASS corrected noncompiler gates only',os.getpid())
