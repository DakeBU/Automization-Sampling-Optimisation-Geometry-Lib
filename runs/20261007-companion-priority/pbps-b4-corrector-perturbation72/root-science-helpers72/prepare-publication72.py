from pathlib import Path
import copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
pre=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):
 p=Path(p);assert not p.exists(),p;save(p,x)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
freeze=load(r/'mathematics-freeze72.json')
for z in freeze['inputs']:assert sha(Path(z['path']).read_bytes())==z['RAW_sha256'],z['path']
claim=load(r/'claim.json');names=claim['target_declarations'];files=claim['proposed_files']
actualcid=claim['frontier_cell'];genericcid='ASTIS-SW-PBPS-hilbert-corrector-perturbation'
cp=Path('research-wiki/frontier-cells')/(actualcid+'.json');oldcell=load(cp)
assert oldcell['status']=='claimed';new(r/'cell.before-publication72.json',oldcell)
boundary='The bounded corrector perturbation identity is focused-compiled. Arbitrary r is not the actual source residual r_rho. Actual conditional half-turn H, K/B7, r/r_rho/B27, B4/B28 dynamics, H1/B2, invariance/nonexplosion, full PBPS/SPHMC results, implementation errors/caps, expected-query costs and actual-input composition remain open. Independent review, integration, Exposition Seal, PURIFIED, main/live and whole-Goal completion remain pending.'
cells=[]
for i,cid in enumerate([genericcid,actualcid]):
 c=copy.deepcopy(oldcell);c['cell_id']=cid
 c['title']=['Hilbert corrector perturbation algebra with an actual PBPS consumer','Exact corrector perturbation on the same actual PBPS Hilbert space'][i]
 c['target_statement']=(pre/['header72.generic.proposed.lean','header72.actual.named-literal.proposed.lean'][i]).read_text(encoding='utf8')
 c['parents']=[] if i==0 else ['ASTIS-SW-PBPS-actual-corrector-change',genericcid]
 c['consumers']=[names[1]] if i==0 else ['PBPS Appendix B4 B28 perturbation summand after actual r_rho/B27 producer']
 c['source_targets']=[names[i]]
 c['shared_floor_audit']['canonical_declaration']=names[i]
 c['shared_floor_audit']['canonical_shared_cell']=''
 c['shared_floor_audit']['decision']='new_route_local'
 c['shared_floor_audit']['reason']='Two publication cells are required by the canonical one-declaration-per-cell validator. They belong to ONE claimed SAU; generic algebra has the concrete actual72 production consumer. No second SAU, duplicated theorem, invented route or shared-foundation completion badge.'
 c['reuse_plan']['reused_declarations']=[] if i==0 else [names[0],oldcell['proof_digestion']['existing_substrate'][0]]
 c['reuse_plan']['new_shared_declarations']=[names[0]] if i==0 else []
 c['reuse_plan']['known_consumers']=c['consumers'] if i==0 else []
 c['evidence']['owned_files']=[files[i]]
 c['evidence']['focused_checks']=[dict(command=claim['focused_checks'][i],result='PASS; standard three axioms only; exact sealed mathematical header.',evidence=freeze['compiled'][i]['focused_receipt']['path'])]
 c['evidence']['truth_boundary']=boundary
 c['blocked']['reason']='Frozen focused-compiled result; independent mathematics, blind reconstruction, whole implementation/source and publication review pending.'
 c['source_detail_audit']['fidelity_boundary']=boundary
 c['source_detail_audit']['gap']='Actual H/K/r_rho/B27/B28 are separate open source adapters; no generic r identification.'
 c['learning_contract']['failure_class']='IMPLEMENTATION_FAILED'
 c['learning_contract']['salvage'].update(required=True,status='completed',reason='Recorded first generic compilation failed on coercion-sensitive selfadjoint rewrite. Explicit typed inner equalities repaired elaboration without changing any mathematical binder. Both frozen modules now compile.',promoted_fragments=[names[i]],discarded_fragments=[])
 c['learning_contract']['reader_backpressure']['lean_expansion_nodes']=[names[i]]
 c['proof_digestion']['existing_substrate']=[] if i==0 else [oldcell['proof_digestion']['existing_substrate'][0],names[0]]
 c['proof_digestion']['new_reusable']=[names[0]] if i==0 else []
 c['conceptual_mirror_audit']=load(r/'conceptual-mirror-audit72.json')
 c['purification']['scope']=boundary
 path=Path('research-wiki/frontier-cells')/(cid+'.json')
 if i==0:new(path,c)
 else:save(path,c)
 cells.append(c)
new(r/'publication-cell-split72.json',dict(reason='Existing publication validator enforces one canonical declaration per Frontier Cell; connected two-cell slice, one sole-owner SAU, real generic-to-actual edge.',advance_id=claim['advance_id'],primary_cell=actualcid,supporting_cell=genericcid,extra_mathematical_claim=False))
old=load('website/content/publications/pbps-actual-corrector-change.json')['items'][0]
genericstatement='''Let H be a complete real Hilbert space, allowing the zero space. Let A,G,Inv:H→H be bounded real-linear endomorphisms. Assume A,G,Inv are selfadjoint, A commutes with Inv, Inv G=G Inv=I, and A²+G²=I. Every one of these structural conditions is an explicit hypothesis of this auxiliary algebra theorem. For arbitrary u,v,r∈H define C(a,b)=(||a||²−||b||²)/2−⟨A(Inv a),b⟩. Then C(u+Gr,v−Ar)−C(u,v)=⟨u,Inv r⟩+||r||²/2. The half, plus sign, operator order and same three operators are exact. This is an ASTIS Hilbert-space auxiliary generalization of the algebra in Chen–Chewi–Lu–Zhang's PBPS B20 and Lemma B4 expansion Ex28–Ex34, rather than a claim that the paper states a theorem for arbitrary Hilbert operators. No positivity, finite dimension, spectral gap, surjectivity or probability hypothesis is needed by this algebra identity. The actual PBPS consumer constructs all seven operator facts internally on its same centered space. Arbitrary r is not yet the paper's r_rho; the actual H/K/B27 adapter and B4/B28 decay proof remain open.'''
actualstatement=old['statement'].split('This closes the discrete corrector-change ingredient')[0]+'''For the SAME C and the SAME produced A_0,Γ_0,Inv on H_P^0, for every u,v,r∈H_P^0 one further has C(u+Γ_0 r,v−A_0 r)−C(u,v)=⟨u,Inv r⟩+||r||²/2. All structural conditions of the auxiliary Hilbert theorem are internally supplied by the same parent witnesses, including selfadjoint Γ_0 from its positivity. The universal identity lies syntactically inside each centered f/output-component branch; C has no f dependence. Every earlier clause, the original six analytic caller conditions and twelve common witnesses remain. No new analytic premise or arbitrary kernel is introduced. This closes the exact perturbation algebra needed after a future actual B27 adapter. It does not construct the actual conditional half-turn H, K/B7 or the source residual r_rho, and does not assert the remaining B4/B28 dynamics, nonexplosion, full paper results, errors, expected costs or composition.'''
formulas=[r'C(u,v)=\frac{\|u\|^2-\|v\|^2}{2}-\langle A\operatorname{Inv}u,v\rangle,\quad C(u+Gr,v-Ar)-C(u,v)=\langle u,\operatorname{Inv}r\rangle+\frac{\|r\|^2}{2}.',r'C(u+\Gamma_0r,v-A_0r)-C(u,v)=\langle u,\operatorname{Inv}r\rangle+\frac{\|r\|^2}{2},\qquad u,v,r\in H_P^0.']
titles=['Hilbert corrector perturbation identity','Actual PBPS corrector perturbation with the same witnesses']
slugs=['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation']
aids=['ASTIS-RT-20261010-PBPSHilbertCorrectorPerturbation','ASTIS-RT-20261010-PBPSActualCorrectorPerturbation']
sources=[];lessons=[];items=[];written=[]
for i in range(2):
 s=Path(files[i]).read_text(encoding='utf8');short=names[i].rsplit('.',1)[1]
 body=s.index(' := by\n',s.index('theorem '+short))
 def step(title,text,formula,start,end):
  assert s.count(start,body)==1,(title,start)
  a=s.index(start,body);b=s.index(end,a);code=s[a:b].rstrip()+'\n'
  return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled contiguous BODY span; preceding local definitions and inherited Hilbert structures remain in scope.',lean_source_region=dict(path=files[i],source_raw_sha256=sha(Path(files[i]).read_bytes()),start_line=s[:a].count('\n')+1,end_line=s[:a+len(code)].count('\n'),exact_code_raw_sha256=sha(code.encode())))
 if i==0:
  steps=[
   step('Expose the exact functional and typed selfadjoint identities','Unfold only C. State each selfadjointness consequence as an equality of real inner products on the same H, avoiding coercion-sensitive rewrites. No mathematical assumption is added.',r'\langle Ax,y\rangle=\langle x,Ay\rangle,\quad\langle Gx,y\rangle=\langle x,Gy\rangle,\quad\langle\operatorname{Inv}x,y\rangle=\langle x,\operatorname{Inv}y\rangle.','  dsimp only','  have hIG'),
   step('Evaluate the inverse and square-sum operator equalities','Apply Inv G=I and A²+G²=I to an arbitrary vector x. These give vector equalities without dividing by a scalar or assuming a nonzero space.',r'\operatorname{Inv}(Gx)=x,\qquad A(Ax)+G(Gx)=x.','  have hIG','  have hEnergy'),
   step('Obtain the energy identity','Take the inner product of the square-sum equality with x and move A and G across the inner product by selfadjointness. The two summands become squared norms.',r'\|Ax\|^2+\|Gx\|^2=\|x\|^2.','  have hEnergy','  have hLinear'),
   step('Recover the remaining linear operator','Use Inv(G(Gx))=Gx and linearity to write Inv(A(Ax))+Gx=Inv(A(Ax)+G(Gx))=Inv x. This avoids any additional A–G commutation hypothesis.',r'\operatorname{Inv}(A(Ax))+Gx=\operatorname{Inv}x.','  have hLinear','  have hMixed'),
   step('Identify the mixed linear contribution','Move A and Inv through the inner products and apply the preceding vector identity with x=r. Thus the sum of the two surviving u-linear terms is exactly the claimed right-hand linear term.',r'\langle A\operatorname{Inv}u,Ar\rangle+\langle u,Gr\rangle=\langle u,\operatorname{Inv}r\rangle.','  have hMixed','  rw [norm_add_sq_real'),
   step('Expand and cancel the perturbation terms','Expand the two squared norms and C cross term. Since Inv Gr=r, the increment is ⟨u,Gr⟩+⟨v,Ar⟩+(||Gr||²−||Ar||²)/2+⟨A Inv u,Ar⟩−⟨Ar,v⟩+||Ar||². Real symmetry cancels the v terms, the energy identity reduces the quadratic terms to ||r||²/2, and the mixed identity gives ⟨u,Inv r⟩. The result retains the exact positive half.',formulas[i],'  rw [norm_add_sq_real','\n\nend\n')]
 else:
  steps=[
   step('Retain every actual law, conditional operator and parent witness','Apply the accepted actual corrector-change theorem with the original six analytic callers. Extract the same twelve witnesses and every earlier clause. Expose the inherited complete Hilbert spaces H_P^0 and H_perp=ker P, and retain D and its full-domain intertwining identity. None of these structural facts becomes a new caller premise.',r'\Gamma_0^2+A_0^2=I,\quad\operatorname{Inv}\Gamma_0=\Gamma_0\operatorname{Inv}=I,\quad g=U(Pf-(f-Pf)).','  unfold actual_corrector_perturbation_statement','  have hΓself'),
   step('Instantiate the Hilbert algebra on the same centered space','Positivity of Γ_0 supplies its selfadjointness. Apply the generic compiled identity with H=H_P^0, A=A_0, G=Γ_0 and the same Inv. The other selfadjointness, commutation, inverse and square-sum facts are parent conclusions. This is a production use of the auxiliary theorem.',formulas[i],'  have hΓself','  have hGlobal72'),
   step('Adjoin the universal identity to actual conditional components','For each globally centered f, retain its actual f_P, f_V, g, g_P and g_V, output mean, projected formulas, pair energy and B21 corrector change. Add only the identity for arbitrary u,v,r in the same H_P^0 and same C scope. No identification of r with the still-unconstructed source residual is made.',r'C(g_P,g_V)-C(f_P,f_V)=-\|f_P\|^2+\|f_V\|^2,\qquad\forall u,v,r\in H_P^0:\ C(u+\Gamma_0r,v-A_0r)-C(u,v)=\langle u,\operatorname{Inv}r\rangle+\tfrac12\|r\|^2.','  have hGlobal72','  have hFinal'),
   step('Reassemble the original-input theorem without an extra premise','Keep the all-ker-P intertwining and every previous law, kernel, root, inverse and polar conclusion with the same witness tuple. The final theorem now contains the perturbation identity. Producing actual H/K/r_rho/B27 and using it in B28 remains a separate source dependency.',formulas[i],'  have hFinal','\n\nend\n')]
 source=dict(url='https://arxiv.org/html/2609.06905v1#A2',edition=old['source']['edition'],anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv:2609.06905v1, B20 and Lemma B4 perturbation expansion Ex28–Ex34. '+('ASTIS auxiliary real Hilbert generalization with all structural assumptions explicit; not a verbatim source theorem.' if i==0 else 'ASTIS original-input integration of the same perturbation algebra; all actual71 clauses retained.'))
 assumptions=(["H is a complete real Hilbert space, including the zero space; A,G,Inv are bounded real-linear endomorphisms.","A,G,Inv are selfadjoint; A commutes with Inv; Inv G=G Inv=I; A²+G²=I. All seven structural facts are explicit premises of this auxiliary algebra theorem.","u,v,r are arbitrary in H; C is the exact displayed local definition. No finite dimension, positivity, spectral gap, nontriviality or probability premise."] if i==0 else copy.deepcopy(old['assumptions'])+['The new perturbation identity is a conclusion on the same H_P^0 and same A_0,Γ_0,Inv; all generic hypotheses are internally produced. Arbitrary r is not the source r_rho.'])
 statement=[genericstatement,actualstatement][i]
 deltas=[dict(source=('B20 and the B4 operator algebra on the source centered Hilbert space.' if i==0 else assumptions[0]),lean=assumptions[0],classification=('generalization' if i==0 else 'same'),reason=('ASTIS explicitly generalizes only the algebra to any complete real Hilbert space; actual72 supplies a concrete source consumer.' if i==0 else 'Exact original six analytic callers and all twelve witnesses are retained.'))]
 deltas.append(dict(source='Actual H/K/r_rho/B27/B28 and full paper conclusions.',lean=boundary,classification='unresolved',reason='The perturbation algebra does not produce the algorithm-specific residual or dynamics/cost results.'))
 item=dict(id=slugs[i],library='pbps',chapter='pbps-01',chapter_path=old['chapter_path'],title=titles[i],source=source,statement=statement,assumptions=assumptions,formulae=[dict(label=titles[i],tex=formulas[i])],obligations=[dict(id='perturbation-algebra',label='Exact signed perturbation algebra'),dict(id='remaining-paper',label='Actual H/K/r_rho/B27/B28 and full paper/cost/composition')],bindings=[dict(declaration=names[i],cell=cells[i]['cell_id'],role='proof-edge',supports=['perturbation-algebra'],audit_id=aids[i],boundary=boundary,assumption_deltas=deltas)])
 for k in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[k]=copy.deepcopy(cells[i][k])
 unit=dict(kind='theorem',declaration=names[i],title=titles[i],sources=[dict(url=source['url'],label=source['anchor'],scope=boundary)],tests=[claim['focused_checks'][i]],assumptions=assumptions,statement=statement,formula=formulas[i],boundary=boundary,steps=steps,lean_statement=statement,lean_proof='; '.join(z['title'] for z in steps),helpers=[] if i==0 else [names[i].rsplit('.',1)[0]+'.actual_corrector_perturbation_statement'],astis_dependencies=cells[i]['proof_digestion']['existing_substrate'],mathlib_dependencies=['IsSelfAdjoint.isSymmetric','ContinuousLinearMap.mul_apply','ContinuousLinearMap.one_apply','real_inner_self_eq_norm_sq','norm_add_sq_real','norm_sub_sq_real','real_inner_comm','congrArg']+([] if i==0 else ['ContinuousLinearMap.IsPositive.isSelfAdjoint']))
 pp=Path('website/content/publications')/(slugs[i]+'.json');lp=Path('website/content/declaration_lessons')/(slugs[i]+'.json')
 new(pp,dict(schema_version=1,items=[item]));new(lp,dict(schema_version=1,units=[unit]))
 items.append(item);lessons.append(unit);sources.append(source);written.extend([pp,lp])
pub.inputs.cache_clear();pub.load.cache_clear()
for i in range(2):
 lean=load(r/f'anonymous.{i}.lean-context72.json');s=Path(files[i]).read_text(encoding='utf8');short=names[i].rsplit('.',1)[1]
 body=s.index(' := by\n',s.index('theorem '+short))
 lean.update(declaration=names[i],file=files[i],formalizer='root-samplinglib-writer',compiler_evidence=freeze['compiled'][i]['focused_receipt']['path'])
 if i==1:lean['statement_representation']=dict(kind='exact-literal-private-Prop-expansion',actual_header=s[s.index('theorem '+short):body].rstrip()+'\n',private_definition=s[s.index('private def actual_corrector_perturbation_statement'):s.index('theorem '+short)].rstrip()+'\n',expanded_header=(r/'expanded72.actual.frozen.header.lean').read_text(encoding='utf8'),source_approved_overlay=(pre/'root.statement-seal72.json').as_posix(),kernel_header_and_literal_expansion_checked=True)
 original=sources[i]['attribution']+'\n'+items[i]['statement']+'\n'+sources[i]['anchor']
 audit=dict(id=aids[i],state='draft',source=dict(source_id='companion-domain:'+slugs[i],anchor=sources[i]['anchor'],url=sources[i]['url'],original_text=original,text_sha256=sha(original.encode())),lean=lean,source_review=dict(state='pending'),repairs=[],publication_binding_sha256=pub.binding_digest(items[i],items[i]['bindings'][0],pub.inputs()),publication_context=pub.review_context(items[i],items[i]['bindings'][0],pub.inputs()))
 assert rt.decoder_packet(audit)==load(r/f'anonymous.{i}.decoder.json')
 ap=Path('research-wiki/semantic-roundtrip/audits')/(aids[i]+'.json');new(ap,audit);written.append(ap)
new(r/'publication-plan.json',dict(slugs=slugs,audit_ids=aids,mathematical_declarations=names,active_cells=[genericcid,actualcid],remaining_boundary=boundary,literal_statement_helpers=lessons[1]['helpers'],formula_proof_steps=[len(x['steps']) for x in lessons],source_graph_and_lean_graph_distinct=True,one_SAU_two_connected_publication_cells=True,no_fake_consumer=True))
written.extend([Path('research-wiki/frontier-cells')/(c['cell_id']+'.json') for c in cells])
new(r/'publication-freeze72.json',dict(status='DRAFT_BEFORE_WHOLE_INDEPENDENT_SOURCE_REVIEW',actual_root_PID=os.getpid(),mathematics_freeze=pin(r/'mathematics-freeze72.json'),inputs=[pin(p) for p in written],source_review=False,VERIFIED=False,PROVED_LOCAL=False))
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='same-C/InvG-square-sum/typed-selfadjoint-inner/actual-six-input-consumer',progress_signature='2392+3952jobsEXIT0-standard3-sealed-6plus4BODYformulaSteps',mathematical_delta=claim['theorem_delta'],exact_residual=boundary)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(names,reviewed=False)
print('PASS draft72:two connected publication cells,one SAU,two unchanged anonymous packets,6+4 exact BODY/formula steps. No PROVED_LOCAL or VERIFIED.')
