from pathlib import Path
import copy,hashlib,json,re,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
pre=Path('runs/20261007-companion-priority/pbps-reflection-rotation-preproof69')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
 p=Path(p);assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes()
 return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
freeze=load(r/'math-freeze.theorem-only69.json')
for z in freeze['inputs']:assert sha(Path(z['path']).read_bytes())==z['raw_sha256']
claim=load(r/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0]
seal=load(pre/'root.statement-seal69.json'); cid='ASTIS-SW-PBPS-actual-reflection-intertwining'
cp=Path('research-wiki/frontier-cells')/(cid+'.json');cell=load(cp)
assert cell['status']=='claimed'
mirror=dict(status='none-found',discovery_ids=[],checked=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json'],reason='Full micro-space reflection block intertwining on the same PBPS conditional geometry. Existing discrete-hypocoercivity family already contains the mechanism; no new source-backed cross-domain bridge or transport certificate found.')
w(r/'conceptual-mirror-audit69.json',mirror)
w(r/'cell.before-focused-publication69.json',cell)
cell['conceptual_mirror_audit']=mirror
cell['evidence']['focused_checks']=[dict(command='lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining',result='PASS3948;standard3;exact sealed actual full-micro statement.',evidence=(r/'focused69-v2/receipt.json').as_posix())]
cell['blocked']['reason']='Local focused target compiled; independent mathematical/decoder/source review and serialized integration pending.'
cell['learning_contract']['salvage'].update(status='completed',reason=freeze['typed_negative']['strict_reduction'],promoted_fragments=[decl],discarded_fragments=[])
cell['learning_contract']['reader_backpressure'].update(assumptions_preserved=True,boundary_preserved=True)
cell['shared_floor_audit']['canonical_declaration']=decl
cell['shared_floor_audit']['canonical_shared_cell']=cid
save(cp,cell);w(r/'frozen-cell69.json',cell)
old=load('website/content/publications/pbps-actual-root-inverse-commutation.json')['items'][0]
statement=old['statement'].split('The genuine original-input Test proves K=')[0]
statement=re.sub(r'The preceding independently reviewed ambient-adjoint Test derives .*?The global zero-mean condition','The global zero-mean condition',statement)
statement+='''Define D=R U i_perp:H_perp→H_perp using the SAME produced U,R and the inclusion i_perp. For every h∈H_perp, i_perp D h=U i_perp h−P(U i_perp h). On ALL of H_perp the SAME actual polar adjoint satisfies V_0* D=−A_0 V_0*. This identity is not restricted to the range of V_0; no surjectivity or coisometry is assumed. Every preceding actual law/kernel/root/inverse/polar/ambient-adjoint and globally centered-observable conclusion persists with the same witnesses. The reflection is fixed by its almost-everywhere pullback formula; the already compiled actual reflection block identity is transported only after proving equality of that reflection with the current U. This is the full micro-space intertwining ingredient used in Appendix B.3 (B.21) and Lemma B.4. The actual projected rotation and corrector change, weak H1/B2, B4 dynamics, invariance/nonexplosion, main convergence, implementation errors/caps, expected query costs and actual-input composition remain separate. One private literal Prop stores the complete sealed proposition and supplies no mathematical proof provider or additional premise.'''
title='Actual PBPS reflection intertwining on the full conditional-complement space'
formula=r'D=RUi_\perp,\quad i_\perp Dh=Ui_\perp h-PUi_\perp h,\quad V_0^*D=-A_0V_0^*\quad(h\in\ker P).'
boundary=seal['remaining_truth_boundary'];s=Path(file).read_text(encoding='utf-8');body=s.index(':= by',s.index('theorem '))
def step(title,text,formula,start,end):
 a=s.index(start,body);b=s.index(end,a);code=s[a:b].rstrip()+'\n'
 return dict(title=title,text=text,formula=formula,lean=code,detail='Literal compiled BODY span; exact preceding module locals remain in scope.',lean_source_region=dict(path=file,source_raw_sha256=sha(Path(file).read_bytes()),start_line=s[:a].count('\n')+1,end_line=s[:a+len(code)].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Fix the original probability geometry and the same witnesses','Apply the original-input production parent and retain every probability, kernel, centered-root, inverse, polar and globally centered-observable conclusion. Both complete subspaces have their inherited Hilbert structures.',r'H_P^0=\ker\langle q_P,\cdot\rangle,\qquad H_\perp=\ker P.', '  classical','  let D :'),
 step('Use the actual compression and identify the reflection','Define D by the residual map and current reflection. The existing actual block theorem produces a reflection with the same AE pullback action; L2 extensionality proves it equals the current U before its block identity is used. Put A_J=PUP, B_J=(I-P)UP and D_J=(I-P)U(I-P).',r'i_\perp Dh=Ui_\perp h-PUi_\perp h,\quad U_2=U,\quad B_J^*D_J=-A_JB_J^*.', '  let D :','  let ι :'),
 step('Match the actual inclusions','Let iota=i i_0 include the centered macro space in the joint space. The defining B0/A0 inclusions and P h=0 for every micro h identify the actual compressed maps exactly.',r'B_J\iota=i_\perp B_0,\quad A_J\iota=\iota A_0,\quad D_Ji_\perp=i_\perp D.', '  let ι :','  have hB0intertwine'),
 step('Transport the block adjoint identity on every micro input','Test against an arbitrary centered macro vector u. Move the adjoints across the inner products, apply the actual ambient block identity, then use selfadjoint A_J and A0. The inclusion identities give the displayed equality for every h in ker P; inner-product separation yields the operator identity.',r'\langle u,B_0^*Dh\rangle=\langle B_J\iota u,D_Ji_\perp h\rangle=-\langle B_0A_0u,h\rangle=-\langle u,A_0B_0^*h\rangle.', '  have hB0intertwine','  have hVdefTyped'),
 step('Pass from B0 to the same polar adjoint','The exact produced equation V0=B0 Inv and selfadjointness of the same Inv give V0*=Inv B0*. Its previously proved commutation with A0 then transports B0*D=-A0B0* without any range or surjectivity restriction.',r'V_0^*=\mathrm{Inv}\,B_0^*,\quad V_0^*D=-\mathrm{Inv}A_0B_0^*=-A_0\mathrm{Inv}B_0^*=-A_0V_0^*.', '  have hVdefTyped','  have hFinal :'),
 step('Preserve the complete original conclusion','Prove the exact new tail with D semantics, full micro intertwining and the old globally centered-f conclusion, then reassemble the original witnesses. The new identity is an internal conclusion from the same six caller conditions.',r'\text{same }\mu,J,\nu,S,e,U,T,\Gamma,\Gamma_0,\mathrm{Inv},A_0,B_0,V_0,R;\quad\forall h\in\ker P.', '  have hFinal :','\n\nend\n')]
slug='pbps-actual-reflection-intertwining';aid='ASTIS-RT-20261009-PBPSActualReflectionIntertwining'
source=dict(url='https://arxiv.org/html/2609.06905v1#A2',edition='arXiv:2609.06905v1;Lean4.33.0/fixedMathlib',anchor=cell['source_anchor'],wording_status='faithful paraphrase',attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv:2609.06905v1 Appendix B.1 and B.3 (B.21), Lemma B.4. ASTIS expands the same actual conditional-complement compression and all-domain polar-adjoint intertwining.')
assumptions=copy.deepcopy(old['assumptions'])
assumptions.append('D=R U inclusion and V0*D=-A0V0* on all ker P are internally proved conclusions, not source hypotheses. No onto-V0, sharp-energy estimate or additional smoothness is required.')
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path=old['chapter_path'],title=title,source=source,statement=statement,assumptions=assumptions,formulae=[dict(label=title,tex=formula)],obligations=[dict(id='reflection-intertwining',label=title),dict(id='remaining-paper',label='Actual B21 rotation/corrector change,B4 dynamics,H1,main,errors,costs/composition')],bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['reflection-intertwining'],audit_id=aid,boundary=boundary,assumption_deltas=[dict(source=assumptions[0],lean=assumptions[0],classification='same',reason='Exact original input seal independently admitted before proof search.'),dict(source='B21 actual rotation/corrector change, B4 dynamics and whole-paper conclusions.',lean=boundary,classification='unresolved',reason='The full-micro intertwining is one substantive prerequisite; no subsequent conclusion is inferred.')])])
for k in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[k]=copy.deepcopy(cell[k])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=boundary)],tests=claim['focused_checks'],assumptions=assumptions,statement=statement,formula=formula,boundary=boundary,steps=steps,lean_statement=statement,lean_proof='; '.join(z['title'] for z in steps),astis_dependencies=cell['proof_digestion']['existing_substrate'],mathlib_dependencies=['Lp.ext','LinearIsometry.ext','ContinuousLinearMap.adjoint_inner_right','ContinuousLinearMap.adjoint_comp','IsSelfAdjoint.adjoint_eq','Commute.eq','Submodule.isSelfAdjoint_starProjection'])
pp=Path('website/content/publications')/(slug+'.json');lp=Path('website/content/declaration_lessons')/(slug+'.json');ap=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json')
w(pp,dict(schema_version=1,items=[item]));w(lp,dict(schema_version=1,units=[unit]));pub.inputs.cache_clear();pub.load.cache_clear()
expanded=(pre/'header0-expanded.lean').read_text(encoding='utf-8');stmt=expanded[expanded.index('theorem ')+len('theorem '+decl.rsplit('.',1)[1]):].rstrip('\n')
context=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualRootInverseCommutation.json')['lean']['decoder_context']
context+=['D is the displayed residual compression of the same produced isometric involution. The adjoint-composition equality is asserted on the whole displayed conditional-complement domain, not only the range of the produced isometry.']
original=source['attribution']+'\n'+statement+'\n'+source['anchor']
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=source['anchor'],url=source['url'],original_text=original,text_sha256=sha(original.encode())),lean=dict(declaration=decl,file=file,statement=stmt,statement_sha256=sha(stmt.encode()),compiled=True,formalizer='root-samplinglib-writer',decoder_context=context,statement_representation=dict(kind='exact-literal-private-Prop-expansion',actual_header=s[s.index('theorem '):body].rstrip()+'\n',private_definition=(pre/'statement0.definition.lean').read_text(encoding='utf-8'),expanded_header=expanded,source_approved_overlay=(pre/'root.header69.adoption.json').as_posix(),kernel_header_and_literal_expansion_checked=True),compiler_evidence=(r/'focused69-v2/receipt.json').as_posix()+' actualPID43856 EXIT0 PASS3948; standard3 only.'),source_review=dict(state='pending'),repairs=[],publication_binding_sha256=pub.binding_digest(item,item['bindings'][0],pub.inputs()),publication_context=pub.review_context(item,item['bindings'][0],pub.inputs()))
w(ap,audit);packet=rt.decoder_packet(audit)
neutral=Path('.astis/decoder-69');neutral.mkdir(exist_ok=False)
w(neutral/'packet0.json',packet);w(r/'anonymous.0.decoder.json',packet)
w(neutral/'lease.json',dict(status='OPEN',allowed_inputs=['packet0.json'],source_text_visible=False,source_identity_visible=False,compiler_started=False))
(neutral/'initial-lease.raw.snapshot.json').write_bytes((neutral/'lease.json').read_bytes())
w(r/'publication-plan.json',dict(slugs=[slug],audit_ids=[aid],mathematical_declarations=[decl],active_cells=[cid],remaining_boundary=boundary,actual_ASTIS_parents=cell['proof_digestion']['existing_substrate'],private_providers=[],formula_proof_steps=[6],source_graph_and_lean_graph_distinct=True,exact_multiline_step_Lean=True,no_Test_wrapper_or_production_sharp_energy_dependency=True))
names=[pp,lp,ap,cp,r/'frozen-cell69.json',r/'conceptual-mirror-audit69.json',r/'publication-plan.json',r/'anonymous.0.decoder.json']
w(r/'publication-freeze69.json',dict(schema='publication69-draft-before-decoder-and-independent-source-v1',mathematics_freeze=pin(r/'math-freeze.theorem-only69.json'),inputs=[pin(p) for p in names],source_review=False,independently_verified=False,PROVED_LOCAL=False))
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='same-actual-block/same-U-equality/full-inner-transport/polar-inverse-commutation',progress_signature='3948EXIT0-standard3-original-callers-full-kerP',mathematical_delta=claim['theorem_delta'],exact_residual='Independent mathematics,blind decoder,primary-first whole-module source and publication review; integration and B21/B4/main/cost/composition remain.')
pub.check_advance([decl],reviewed=False)
print('PASS publication69 draft frozen:one production declaration,six literal BODY steps,one neutral decoder packet; no PROVED_LOCAL or VERIFIED.')
