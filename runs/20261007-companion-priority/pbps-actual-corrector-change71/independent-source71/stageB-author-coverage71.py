import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,collections,re
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
extra=[B/'tools/astis_site.py',B/'runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean',B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json',B/'.agents/skills/astis-semantic-roundtrip/SKILL.md',B/'docs/theorem-publication-protocol.md']
rows=[]
for i,p in enumerate(extra):
 b=p.read_bytes();n=f'stageB.additional-input.{i:02d}.exactraw.snapshot';(O/n).write_bytes(b);(O/(n+'.LF')).write_bytes(b.replace(b'\r\n',b'\n'));rows.append({**pin(p),'snapshot':n,'LF_snapshot':n+'.LF','use':'Current audit read only by mechanical packet regeneration, not used as a prior semantic verdict.' if i==2 else 'Exact bounded source-review or renderer-contract input.'})
write('stageB.additional-exact-inputs71.json',{'schema':'source71-additional-finite-inputs-v1','actual_pid':os.getpid(),'inputs':rows,'count':len(rows),'LF_recipe':'ONLY CRLF byte pairs to LF'})
module=(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_bytes();lines=module.splitlines(keepends=True)
groups=[(1,1,['P14'],'Compiled-parent dependency import; exact actual70 theorem is called at161-162.'),(18,26,['P0'],'Complete literal typing and original six public analytic callers.'),(27,41,['P1','P2','P3'],'Same normalized joint/reflected laws and actual conditional projection definitions.'),(42,59,['P1','P2','P3','P4'],'Retained probability/kernel/pullback and same AE reflection/operator conclusions.'),(60,73,['P4','P5'],'Retained actual compression, off-diagonal block and same positive root identities.'),(74,97,['P6','P7'],'Exact centered domain, SAME restricted root/two-sided inverse and A0 restrictions/commutation.'),(98,116,['P8','P9','P10','P11'],'Exact ker P, SAME polar/R/D and all-micro intertwining retained.'),(117,124,['P12'],'Every centered actual f; actual condExp fP, residual/polar fV and norm identities.'),(125,133,['P13','P14'],'Actual g, internally concluded mean0, actual condExp gP/polar gV, rotation and pair energy.'),(134,136,['P15','P17'],'Exact B20 C on SAME HP0/A0/Inv and actual B21 signed change.'),(138,146,['P0','P17'],'Public theorem has only six callers and asserts the complete literal proposition.'),(147,160,['P0','P1','P2','P3','P17'],'Unfold literal and define same actual spaces/laws/projection; no provider or new premise.'),(161,285,[f'P{i}' for i in range(15)],'Apply actual70 parent with exact original callers, extracting all common witnesses and every old fact.'),(286,304,['P3','P7','P8','P9'],'Expose inherited closed Hilbert domains and exact parent residual/adjoint types.'),(305,321,['P12','P13','P14'],'Expose complete parent actual global-f implication, including internal mean0 and pair energy.'),(322,325,['P11'],'Retain same actual D compression and full-domain intertwining.'),(326,341,['P5','P16'],'Internally derive energy and cross-inner identities from selfadjointness, commutation and square sum.'),(342,361,['P7','P15','P16'],'Define local K=A0 Inv and derive both root/inverse cancellations and K/A0 commutation.'),(362,382,['P16'],'Derive mixed-vector then mixed-inner cancellation; correct typed real adjoint transport.'),(383,395,['P16'],'Derive diagonal inner identities and align mixed terms using real symmetry.'),(396,402,['P16'],'Expand exact B20 coefficient corrector; nlinarith uses proved energy/mixed identities only.'),(403,440,['P12','P13','P14','P15','P17'],'Retain actual f/g component semantics and substitute actual rotation into proved algebra.'),(441,463,['P11','P12','P13','P14','P15','P17'],'Reassemble full micro and global-f conclusion with new corrector equality.'),(464,523,[f'P{i}' for i in range(18)],'Reinsert exact same twelve common witnesses and every retained parent clause, ending in actual new equality.')]
out=[];off=0
for i,line in enumerate(lines,1):
 group=next((g for g in groups if g[0]<=i<=g[1]),None)
 if group:cl='NODE';ns=group[2];reason=group[3]
 else:cl='EXCLUDED';ns=[];reason='Whitespace, source attribution comment, namespace/scoped syntax/options/end, or #print axioms diagnostic; not an independent mathematical obligation.'
 out.append({'line':i,'RAW_start':off,'RAW_end_exclusive':off+len(line),'RAW_bytes':len(line),'RAW_sha256':sha(line),'text':line.decode().rstrip('\r\n'),'classification':cl,'source_nodes':ns,'reason':reason});off+=len(line)
assert off==len(module) and len(out)==528
counts=dict(collections.Counter(x['classification'] for x in out));assert counts=={'NODE':506,'EXCLUDED':22}
write('stageB.whole-module528-NODE-EXCLUDED71.json',{'schema':'source71-whole-module-exhaustive-line-audit-v1','module':pin(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'),'count':528,'counts':counts,'unclassified':0,'BODY_lines':377,'BODY_range_inclusive':[147,523],'new_coefficient_algebra_range':[326,402],'actual_substitution_range':[403,440],'every_new_algebra_and_every_retained_clause_read':True,'entries':out,'classification_contract':'Source attribution, typing, inherited mathematical edges, new proof material and actual theorem result; this is not a Lean dependency graph and adds no theorem-completion claim.'})
stageA=json.loads((O/'stageA.primary255-NODE-EXCLUDED71.before-current-BODY.frozen.json').read_bytes())
node_ranges=collections.defaultdict(list)
for a,z,ns,reason in groups:
 for n in ns:node_ranges[n].append([a,z])
source=[]
for e in stageA['entries']:
 ns=e['source_nodes'];consumer=any(int(n[1:])>=18 for n in ns)
 status='EXCLUDED_WITH_REMAINING_BOUNDARY' if e['classification']=='EXCLUDED' else 'OPEN_REAL_CONSUMER_NOT_CLAIMED' if consumer else 'CURRENT71_SOURCE_COMPARISON_ACCEPTED'
 source.append({**e,'stageB_disposition':status,'current71_line_ranges':[] if consumer else sorted({tuple(x) for n in ns for x in node_ranges[n]}),'source_vs_Lean_graph':'Source graph edge/consumer attribution only; range mapping is evidence, not a certified Lean implication.'})
write('stageB.primary255-source-implementation-coverage71.json',{'schema':'source71-exhaustive-frozen-primary-to-current-implementation-v1','source_count':255,'source_counts':stageA['counts'],'unclassified':0,'source_stageA_file':'stageA.primary255-NODE-EXCLUDED71.before-current-BODY.frozen.json','module_lines':528,'module_counts':counts,'BODY_steps':8,'BODY_lines':377,'entries':source,'full_paper_completion':False,'all_open_consumer_roles_remain_open':True})

evidence={
'H00':'Literal19-26/public139-146; no new caller; sealed147 prefix and parent literal exact.',
'H01':'Literal45-116 and BODY174-277/469-520; twelve same common witnesses precede arbitrary f.',
'H02':'Literal134-136; BODY342/396-402/421-440; B20 RAW821632-823578.',
'H03':'Literal78-97 and BODY343-361; inverse acts on exact HP0; both products retained.',
'H04':'Literal117-124; BODY305-312/425-427; actual condExp, R and V0 adjoint retained.',
'H05':'Literal125-130; BODY313-318/412-417/425-435; current70 mean route312-330/412-417 is internal.',
'H06':'Literal131-133; BODY319-321/418-420/434-440 and full hGlobal reassembly.',
'H07':'Literal134-136 and BODY396-402/428-440; exact -normfP^2+normfV^2 sign.',
'H08':'stageB.parent-retention-and-seal71.json: only four-line new C clause removed and name reversed; whole parent literal exactly equal.',
'H09':'Public139-146; one imported actual70 parent; internal343-402; no rho,omega,ontoV,rank-positive,H1,smoothness or68 certificate.',
'H10':'Original callers permit rank0 and alpha eta1; all new identities quantified HP0 use algebra on possible zero space, never nonzero dimension.',
'H11':'Primary A2.Ex27/B27/Ex36/B28 and href926328; no corresponding B4 implementation/conclusion in71.',
'H12':'Private18-136 stores literal; theorem147 unfolds and proves; exact scanner/full adjacent definition/nonprovider fold contract recorded.',
'H13':'Old prospective review remains header-only; this separately authorized whole-module source review grants only source fidelity, not proof search, exactSCI or VERIFIED.',
'W14':'Arbitrary u,v hCorrector396-402 then actual hGlobal71 substitution424-440; actual fV/gV never RHS defined.',
'W15':'326 positivity gives Gamma selfadjoint; A0 selfadjoint extracted257; explicit inner transport331-341/373-395. Inv selfadjoint retained, local K selfadjoint not required.',
'W16':'343-361: SAME left/right inverses and A0/Inv commute produce KGamma=GammaK=A0 and KA0=A0K.',
'W17':'396-401 norm_sub_sq_real/norm_add_sq_real and real hCross/hSwap; independently expanded norm-change matches frozen signs.',
'W18':'362-395 mixed and diagonal identities; independent expansion gives cross change cancelling all 2t terms; only hEnergy/hMixed used at402.',
'W19':'327-336/362-365 exact square sum on all HP0; micro domain ker P remains116/325, no ran V restriction.',
'W20':'stageB.whole-module528-NODE-EXCLUDED71.json:528/528,506NODE22EXCLUDED;8exactBODY spans147-523,377lines.',
'W21':'Canonical schema has seven slots; eight mathematical concerns include exact new C-change facet separately.51 decoder rows independently mapped; no invented eighth schema key.',
'W22':'One exact private def and public theorem only; adjacent helper label Full Lean proposition (definition), no provider; all details begin folded. Full reader/browser/Exposition not accepted here.',
'W23':'B28 includes independent error term and half normr_rho^2; B17/B18/B22/B4/main/errors/cost/composition retained open.'}
expect=json.loads((O/'stageA.source-expectations71.before-current-BODY.frozen.json').read_bytes())
obs=[{**x,'status':'satisfied-in-bounded-source-review','independent_evidence':evidence[x['id']]} for x in expect['obligations']]
assert len(obs)==24
write('stageB.all24-source-obligations71.json',{'schema':'source71-all-frozen-source-obligations-reviewed-v1','count':24,'satisfied':24,'blocking':0,'entries':obs,'source_acceptance_only':True})

decoder=json.loads((R/'anonymous-decoder/slot-decisions.json').read_bytes())
def decoded_map(k):
 if k<=7:return ['P0'],[[19,26],[139,146]],'Original six analytic callers and structural typing; all subsequent certificates are concluded.'
 if k<=13:return ['P1','P2','P3'],[[27,44]],'Actual normalized measures, two distinct maps and exact conditional projection/range.'
 if k<=18:return ['P1','P2','P3','P4'],[[45,59]],'Same normalized every-state kernel, onto e and per-observable AE U/T; no onto V claim.'
 if k<=23:return ['P4','P5'],[[60,73]],'Exact compression/ambient off-diagonal and same positive root/commutation.'
 if k<=30:return ['P6','P7'],[[74,97]],'Constant, mean, HP0, same gamma, same bounded two-sided inverse and centered A0.'
 if k<=38:return ['P8','P9','P10','P11'],[[98,116]],'All ker P, same V/R/D, actual adjoints and full micro intertwining; V is only an embedding.'
 if k<=41:return ['P12'],[[117,124]],'Every centered actual f and actual conditional/polar input coefficients.'
 if k<=45:return ['P13','P14'],[[125,133]],'Actual output and mean conclusion before conditional/polar coefficients, signed rotation and energy.'
 if k==46:return ['P15','P16','P17'],[[134,136],[326,440]],'Exact same-C half/sign/inverse and actual B21 conclusion; independently checked new algebra and substitution.'
 if k<=49:return ['P0','P7','P12','P13','P17'],[[19,136]],'Common witnesses before f; local fP/gP; exact measures/domains/AE scopes.'
 return ['P17','P20','P21'],[[134,136]],'Decoder states no source/proof verdict. Source review retains independent B4/full-paper boundary.'
decoded=[]
for x in decoder['slots']:
 k=int(x['slot']);ns,lr,reason=decoded_map(k)
 decoded.append({'decoder_row':x['slot'],'decoded_text_sha256':sha(x['reconstructed_slot_text'].encode()),'source_nodes':ns,'current71_line_ranges':lr,'independent_comparison':'equivalent-after-explicit-domain-elaboration' if k in [0,7,11,12,25,26,29,31,36,47,48,49] else 'same-bounded-mathematical-content','reason':reason,'unresolved':False})
assert len(decoded)==51
write('stageB.all51-blind-reconstruction-comparisons71.json',{'schema':'source71-all-decoder-rows-independent-primary-comparison-v1','count':51,'unresolved':0,'canonical_semantic_slots':7,'new_corrector_mathematical_facet':'Same B20 definition and actual B21 change (row46), separately explicit without changing seven-key protocol schema.','entries':decoded,'no_decoder_source_verdict_assumed':True})
write('stageB.target18-final-classification71.json',{'schema':'source71-all18-exact-formula-decisions-v1','count':18,'entries':[{**f,'final_disposition':next(e['stageB_disposition'] for e in source if e['math_id']==f['id']),'repair_required':False} for f in json.loads((O/'stageA.target18-exact-RAW-formulas71.frozen.json').read_bytes())['formulas']],'B20_exact':True,'B21_actual_exact':True,'B28_real_consumer_only':True,'no_sharp68_dependency':True})
print(json.dumps({'actual_pid':os.getpid(),'status':'PASS_INDEPENDENT_FINITE_COVERAGE','source':{'total':255,'NODE':144,'EXCLUDED':111},'whole_module':{'total':528,'NODE':506,'EXCLUDED':22},'BODY':{'steps':8,'lines':377},'obligations_satisfied':24,'decoder_rows_compared':51,'repair_required':False},indent=2))
