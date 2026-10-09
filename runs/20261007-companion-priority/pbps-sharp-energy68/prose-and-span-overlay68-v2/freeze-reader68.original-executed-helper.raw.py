from pathlib import Path
import copy, hashlib, json, re, sys

root=Path.cwd(); sys.path.insert(0,str(root/'tools'))
import astis_advance as adv, astis_publication as pub, astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
pre=Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68')
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
    p=Path(p); assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))

c=load(r/'claim.json'); files=c['proposed_files']; leaf,decl,test=c['target_declarations']
fr=r/sys.argv[1]; receipt=load(fr/'receipt.json');log=(fr/'stdout.log').read_text(encoding='utf-8')
assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=int(re.search(r'Build completed successfully \((\d+) jobs\)',log)[1])
for name,file in zip([leaf,decl,test],files):
    s=Path(file).read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
    m=re.search(re.escape("'"+name+"'")+r' depends on axioms: \[([^\]]+)\]',log)
    assert m and set(re.findall(r'\w+(?:\.\w+)*',m[1]))=={'propext','Classical.choice','Quot.sound'},name
    assert next(z for z in receipt['inputs'] if z['path']==(root/file).as_posix())['raw_sha256']==pin(file)['raw_sha256']
for i in [1,2]:
    s=Path(files[i]).read_text(encoding='utf-8');a=s.index('private def ');b=s.index('\ntheorem ',a)
    assert s[a:b].rstrip()+'\n'==(pre/f'statement{i}.definition.lean').read_text(encoding='utf-8').rstrip()+'\n'
    assert len(re.findall(r'^private def ',s,re.M))==1 and not re.findall(r'^private (?:abbrev|lemma|theorem) ',s,re.M)
assert 'import Tests.' not in Path(files[1]).read_text(encoding='utf-8')
mirror=dict(status='none-found',discovery_ids=[],checked=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json'],
    reason='Direct selfadjoint two-component Hilbert square identity and scalar Cauchy-Schwarz on SAME actual objects. Existing discrete-hypocoercivity family already records the energy mechanism; no new independently source-backed cross-domain adapter found.')
ids=['ASTIS-SHARED-hilbert-corrector-square-bound','ASTIS-SW-PBPS-sharp-corrector-energy']
cells=[]
for i,cid in enumerate(ids):
    cp=Path('research-wiki/frontier-cells')/(cid+'.json');cell=load(cp);w(r/f'cell{i}.before-focused68.json',cell)
    cell['conceptual_mirror_audit']=mirror
    cell['evidence']['focused_checks']=[dict(command='lake build Tests.ProximalBPSSharpCorrectorEnergy',result=f'PASS{jobs};all3 standard3;actual original-input LemmaB3 consumer.',evidence=(fr/'receipt.json').as_posix())]
    cell['blocked']['reason']='Focused proof compiled; independent mathematics, blind decoder and whole-module primary-first source review pending.'
    cell['learning_contract']['salvage'].update(status='completed',promoted_fragments=[leaf,decl,test],reason='Exact typed selfadjoint inner identities and symmetry orientation resolve coercion matching. Bounded proof projections, atomic elimination of the same existential witnesses, and an explicitly typed local final proof remove diagnosed elaboration bottlenecks without changing any statement or ingredient. The redundant ring after field_simp is removed. Original seals, negative/stopped compiler receipts and exact diagnostic snapshots remain retained.')
    if i==0:
        cell['route']='shared'
        cell['evidence']['owned_files']=[files[0]]
        cell['evidence']['truth_boundary']='ASTIS sharp quadratic-form auxiliary on an arbitrary complete real Hilbert space; explicit selfadjoint square identity and norm bound. Actual PBPS inputs and these internal hypotheses are supplied by the actual production consumer. No full dynamics, mixing or cost result.'
        cell['source_detail_audit']['fidelity_boundary']=cell['evidence']['truth_boundary']
        cell['proof_digestion']=dict(existing_substrate=[],bookkeeping=['Sum of two squared component norms; no product max-norm claim.'],new_reusable=[leaf],new_topology='Selfadjoint square identity gives block energy cancellation; scalar Cauchy-Schwarz gives the sharp quadratic bound.')
        cell['graph_contribution']['lean_view']='new-node'
        cell['learning_contract']['reader_backpressure']['lean_expansion_nodes']=[leaf]
    else:
        cell['proof_digestion']['existing_substrate'].append(leaf)
        cell['reuse_plan']['reused_declarations'].append(leaf)
        cell['shared_floor_audit'].update(canonical_declaration=decl,canonical_shared_cell=cid)
    save(cp,cell);w(r/f'frozen-cell{i}.json',cell);cells.append(cell)
w(r/'conceptual-mirror-audit68.json',mirror)
old=load('website/content/publications/pbps-actual-root-inverse-commutation.json')['items'][0]
statement=old['statement'].split('The genuine original-input Test proves K=')[0]+'''The SAME coefficient K=A_0 Inv is selfadjoint and I+K²=Inv². Define C(u,v)=(‖u‖²−‖v‖²)/2−⟨Ku,v⟩ on the SAME centered Hilbert space H_P^0. For every u,v in H_P^0, |C(u,v)|≤(‖u‖²+‖v‖²)/(2γ). For every actual f∈L²(J;ℝ) with ∫f dJ=0, the SAME f_P,f_perp,f_V and all preceding identities persist, and ‖f_P‖²+‖f_V‖²≤‖f‖² and |C(f_P,f_V)|≤‖f‖²/(2γ). All coefficient identities, domains and bounds are conclusions from the original potential and step inputs. The genuine original-input Test then proves, for every real 0<omegaWeight≤γ and L=‖f‖²+omegaWeight C(f_P,f_V), that ‖f‖²/2≤L≤3‖f‖²/2 and |L−‖f‖²|≤omegaWeight ‖f‖²/(2γ)≤‖f‖²/2. These are the first-corrector bound and Lemma B.3 energy equivalence. B21 rotation, weak H1/B2, B4 dynamics, mixing, nonexplosion, implementation error, expected costs and actual-input composition remain separate. One private literal Prop per actual module stores the full sealed statement and adds no proof provider or premise.'''
auxstatement='Let H be any complete real inner-product space, including the zero space. Let K,D:H→H be bounded real-linear selfadjoint operators with I+K²=D². Let c≥0 and ‖D‖≤c. Then for every u,v∈H, |(‖u‖²−‖v‖²)/2−⟨Ku,v⟩|≤(c/2)(‖u‖²+‖v‖²). No finite-dimensionality, nontriviality, c≥1, positivity of K or D, or commutation is assumed. This ASTIS auxiliary Hilbert-space lemma supplies the sharp two-component estimate in the PBPS B23 proof; its actual consumer internally produces K,D,c and all hypotheses.'

def step(title,text,formula,file,start,end):
    s=Path(file).read_text(encoding='utf-8');body=s.index(':= by',s.index('theorem '));a=s.index(start,body);b=s.index(end,a)
    code=s[a:b].rstrip()+'\n'
    return dict(title=title,text=text,formula=formula,lean=code,detail='Literal compiled BODY span; exact preceding locals remain in scope.',
        lean_source_region=dict(path=file,source_raw_sha256=pin(file)['raw_sha256'],start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
af,mf,tf=files
auxsteps=[
    step('Turn the operator square into a norm identity','Evaluate I+K²=D² against x. Selfadjointness moves the outer K and D across the inner product.',r'\|x\|^2+\|Kx\|^2=\|Dx\|^2.',af,'  have hEnergy','  have hSym'),
    step('Cancel the two block cross terms','Use the sum of the two squared component norms. Symmetry cancels the mixed terms; this is the Hilbert sum energy, without a product max-norm assertion.',r'\|u-Kv\|^2+\|Ku+v\|^2=\|Du\|^2+\|Dv\|^2,\quad E=\langle u-Kv,u\rangle-\langle Ku+v,v\rangle.',af,'  have hSym','  have hAbs'),
    step('Bound the quadratic form and block energy','Triangle inequality and the inner-product bound control E. The operator norm controls each D component.',r'|E|\le\|u-Kv\|\|u\|+\|Ku+v\|\|v\|,\quad T\le c^2 S.',af,'  have hAbs','  have hCS'),
    step('Apply two-component Cauchy-Schwarz','The scalar inequality follows from a single nonnegative square. Combine with the block energy bound, keeping S nonnegative.',r'(ab+de)^2\le(a^2+d^2)(b^2+e^2),\quad E^2\le S T\le c^2S^2.',af,'  have hCS','  have hBound'),
    step('Take the nonnegative square root and divide by two','Both |E| and cS are nonnegative, so their square inequality gives |E|≤cS. The corrector is E/2.',r'|E|\le cS\quad\Longrightarrow\quad\left|\frac{\|u\|^2-\|v\|^2}{2}-\langle Ku,v\rangle\right|\le\frac c2S.',af,'  have hBound','\nend\nend ')]
steps=[
    step('Retain the exact actual input and witnesses','Call the production parent at the unchanged potential and step assumptions; fix the same laws, kernel, centered spaces, inverse and global centered-observable geometry.',r'H_P^0=\ker\langle q_P,\cdot\rangle,\quad\Gamma_0^{-1}=\mathrm{Inv},\quad f_V=V_0^*Rf.',mf,'  classical','  have hKself'),
    step('Produce the coefficient identity inside production','Commuting selfadjoint A0 and Inv give selfadjoint K. Multiply A0²+Γ0²=I by the SAME Inv² and use both inverse identities.',r'K=A_0\mathrm{Inv}=K^*,\quad I+K^2=(\Gamma_0^2+A_0^2)\mathrm{Inv}^2=\mathrm{Inv}^2.',mf,'  have hKself','  let γ :'),
    step('Apply the sharp Hilbert estimate on the actual centered space','Take D=Inv and c=1/γ. Positivity of γ and the existing norm bound discharge all leaf hypotheses without a new public premise.',r'\|\mathrm{Inv}\|\le1/\gamma\quad\Longrightarrow\quad |C(u,v)|\le\frac{\|u\|^2+\|v\|^2}{2\gamma}.',mf,'  let γ :','  have hFinal'),
    step('Use the actual norm budget','Pythagoras and the adjoint contraction give the sum-of-squares budget. Apply the pair bound to the SAME actual fP,fV. An explicitly typed local have proves exactly this final conclusion before the outer witnesses are reconstructed.',r'\|f_P\|^2+\|f_V\|^2\le\|f\|^2\quad\Longrightarrow\quad |C(f_P,f_V)|\le\frac{\|f\|^2}{2\gamma}.',mf,'  have hFinal','  unfold actual_sharp_corrector_bound_statement'),
    step('Preserve every preceding actual conclusion','Reassemble the same witnesses with the new internally proved coefficient, pair bound and exact local actual-input conclusion. The literal statement retains each original probability and domain conclusion.',r'\text{same }\mu,J,\nu,S,e,U,T,\Gamma,\Gamma_0,\mathrm{Inv},A_0,B_0,V_0,R.',mf,'  refine ⟨hμ','\nend\nend '),
    step('Consume the sharp bound in Lemma B.3','The Test calls production at the original inputs. For every 0<omegaWeight≤γ, bound the perturbation by half of the squared norm and use both sides of the absolute-value inequality. Its local have proves the exact final Test tail, then retains all original witnesses.',r'|L-\|f\|^2|\le\frac{\omega}{2\gamma}\|f\|^2\le\frac12\|f\|^2,\quad\frac12\|f\|^2\le L\le\frac32\|f\|^2.',tf,'  have hFinal','\nend\nend ')]
configs=[dict(slug='hilbert-sharp-quadratic-corrector-bound',aid='ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound',title='Sharp quadratic corrector bound on a real Hilbert space',cell=cells[0],decl=leaf,file=af,header=(pre/'header0-expanded.lean').read_text(encoding='utf-8'),statement=auxstatement,assumptions=['Complete real inner-product space H; bounded selfadjoint real operators K,D; I+K²=D²; c≥0 and ‖D‖≤c. Zero H is legal.'],steps=auxsteps,formula=r'\left|\tfrac12(\|u\|^2-\|v\|^2)-\langle Ku,v\rangle\right|\le\tfrac c2(\|u\|^2+\|v\|^2).',apis=['IsSelfAdjoint.isSymmetric','norm_add_sq_real','norm_sub_sq_real','abs_real_inner_le_norm','ContinuousLinearMap.le_opNorm','sq_le_sq₀'],attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, Appendix B.3 B23. ASTIS general Hilbert-space auxiliary proves the sharp two-component estimate; it is not a separately printed PBPS theorem.'),
    dict(slug='pbps-sharp-corrector-energy',aid='ASTIS-RT-20261009-PBPSSharpCorrectorEnergy',title='Actual PBPS sharp first-corrector bound and Lemma B.3 consumer',cell=cells[1],decl=decl,file=mf,header=(pre/'header1-expanded.lean').read_text(encoding='utf-8'),statement=statement,assumptions=old['assumptions'],steps=steps,formula=r'|C(u,v)|\le\frac{\|u\|^2+\|v\|^2}{2\gamma},\quad |C(f_P,f_V)|\le\frac{\|f\|^2}{2\gamma},\quad\tfrac12\|f\|^2\le L\le\tfrac32\|f\|^2.',apis=['IsSelfAdjoint.commute_iff','Commute.eq','sq_le_sq₀','div_le_div_of_nonneg_right','abs_le','div_le_iff₀'],attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv:2609.06905v1 Appendix B.3 B19/B20/B22/B23/B24 and Lemma B.3. ASTIS derives the sharp bound from the same actual original-input operators; the genuine Test proves modified-energy equivalence.')]
neutral=Path('.astis/decoder-68');neutral.mkdir(exist_ok=False);auditpaths=[];pubpaths=[];lessonpaths=[]
for i,x in enumerate(configs):
    source=dict(url='https://arxiv.org/html/2609.06905v1#A2',edition='arXiv:2609.06905v1;Lean4.33.0/fixedMathlib',anchor=x['cell']['source_anchor'],wording_status='faithful paraphrase',attribution=x['attribution'])
    boundary=x['cell']['evidence']['truth_boundary']
    deltas=[dict(source=x['assumptions'][0],lean=x['assumptions'][0],classification='same',reason='Exact independently reviewed header; actual operator facts are conclusions.'),dict(source='B21 rotation,weak H1/B2,B4 dynamics,full main results and expected costs/composition.',lean=boundary,classification='unresolved',reason='Sharp first-corrector estimate and energy equivalence only.')]
    item=dict(id=x['slug'],library='pbps',chapter='pbps-01',chapter_path=old['chapter_path'],title=x['title'],source=source,statement=x['statement'],assumptions=x['assumptions'],formulae=[dict(label=x['title'],tex=x['formula'])],obligations=[dict(id='sharp-energy',label=x['title']),dict(id='remaining-paper',label='Remaining rotation,H1,dynamics,mixing,implementation errors and expected costs/composition')],bindings=[dict(declaration=x['decl'],cell=x['cell']['cell_id'],role='proof-edge',supports=['sharp-energy'],audit_id=x['aid'],boundary=boundary,assumption_deltas=deltas)])
    for k in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[k]=copy.deepcopy(x['cell'][k])
    unit=dict(kind='theorem',declaration=x['decl'],title=x['title'],sources=[dict(url=source['url'],label=source['anchor'],scope=boundary)],tests=['lake build Tests.ProximalBPSSharpCorrectorEnergy'],assumptions=x['assumptions'],statement=x['statement'],formula=x['formula'],boundary=boundary,steps=x['steps'],lean_statement=x['statement'],lean_proof='; '.join(z['title'] for z in x['steps']),astis_dependencies=x['cell']['proof_digestion']['existing_substrate'],mathlib_dependencies=x['apis'])
    pp=Path('website/content/publications')/(x['slug']+'.json');lp=Path('website/content/declaration_lessons')/(x['slug']+'.json');ap=Path('research-wiki/semantic-roundtrip/audits')/(x['aid']+'.json')
    w(pp,dict(schema_version=1,items=[item]));w(lp,dict(schema_version=1,units=[unit]));pub.inputs.cache_clear();pub.load.cache_clear()
    actual=Path(x['file']).read_text(encoding='utf-8');a=actual.index('theorem '+x['decl'].rsplit('.',1)[1]);b=actual.index(':= by',a);header=actual[a:b].rstrip()+'\n'
    definition='' if i==0 else (pre/'statement1.definition.lean').read_text(encoding='utf-8')
    context=['H is the stated complete real inner-product space. Bounded real-linear operators use composition as multiplication; IsSelfAdjoint means adjoint equality. All existential witnesses are conclusions, not public assumptions.']
    if i==1:context+=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualRootInverseCommutation.json')['lean']['decoder_context']+['C is the explicitly defined quadratic form on the same centered space; its pair/global estimates are conclusions. The private literal Prop is the complete statement, never a provider.']
    original=x['attribution']+'\n'+x['statement']+'\n'+source['anchor'];stmt=x['header'][x['header'].index('theorem ')+len('theorem '+x['decl'].rsplit('.',1)[1]):].rstrip('\n')
    audit=dict(id=x['aid'],state='draft',source=dict(source_id='companion-domain:'+x['slug'],anchor=source['anchor'],url=source['url'],original_text=original,text_sha256=sha(original.encode())),lean=dict(declaration=x['decl'],file=x['file'],statement=stmt,statement_sha256=sha(stmt.encode()),compiled=True,formalizer='root-samplinglib-writer',decoder_context=context,statement_representation=dict(kind='direct-header' if i==0 else 'exact-literal-private-Prop-expansion',actual_header=header,private_definition=definition,expanded_header=x['header'],source_approved_overlay=(pre/'root.header68.adoption.json').as_posix(),kernel_header_and_literal_expansion_checked=True),compiler_evidence=(fr/'receipt.json').as_posix()+f' actualPID{receipt["actual_foreground_pid"]} EXIT0 PASS{jobs}; all3 standard axioms only.'),source_review=dict(state='pending'),repairs=[],publication_binding_sha256=pub.binding_digest(item,item['bindings'][0],pub.inputs()),publication_context=pub.review_context(item,item['bindings'][0],pub.inputs()))
    w(ap,audit);packet=rt.decoder_packet(audit);w(neutral/f'packet{i}.json',packet);w(r/f'anonymous.{i}.decoder.json',packet)
    auditpaths.append(ap);pubpaths.append(pp);lessonpaths.append(lp)
w(neutral/'lease.json',dict(status='OPEN',allowed_inputs=['packet0.json','packet1.json'],source_text_visible=False,source_identity_visible=False,compiler_started=False))
(neutral/'initial-lease.raw.snapshot.json').write_bytes((neutral/'lease.json').read_bytes())
w(r/'publication-plan.json',dict(slugs=[x['slug'] for x in configs],audit_ids=[x['aid'] for x in configs],mathematical_declarations=[leaf,decl],active_cells=ids,remaining_boundary=c['truth_boundary'],actual_ASTIS_parents=cells[1]['proof_digestion']['existing_substrate'],private_providers=[],private_statement_definitions=[dict(path=files[i],definition=(pre/f'statement{i}.definition.lean').read_text(encoding='utf-8'),expanded_header=(pre/f'header{i}-expanded.lean').read_text(encoding='utf-8')) for i in [1,2]],formula_proof_steps=[5,6],source_graph_and_lean_graph_distinct=True,exact_multiline_step_Lean=True))
inputs=[Path(f) for f in files+['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','lean-toolchain','lake-manifest.json','Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']]+[fr/n for n in ['receipt.json','stdout.log','stderr.log']]+[r/n for n in ['claim.json','frozen-cell0.json','frozen-cell1.json','conceptual-mirror-audit68.json','publication-plan.json','anonymous.0.decoder.json','anonymous.1.decoder.json']]+[pre/n for n in ['root.statement-seal68.json','root.header68.adoption.json']]+[pre/f'header{i}-expanded.lean' for i in range(3)]+[pre/f'statement{i}.definition.lean' for i in [1,2]]+[Path('research-wiki/frontier-cells')/(cid+'.json') for cid in ids]+pubpaths+lessonpaths+auditpaths
inputs += [r/'compiler-diagnosis68'/n for n in ['parent-projection-route.json','atomic-existential-route.json','atomic-global-route.json','local-global-proof-route.json','redundant-ring-repair.json','diagnostics-removed.json','test-atomic-route.json','test-local-global-proof-route.json']]
w(r/'math-freeze.json',dict(schema_version=1,advance_id=c['advance_id'],checked_base_commit=receipt['checked_science_parent'],inputs=[pin(p) for p in inputs],mathematical_declarations=[leaf,decl],genuine_consumer=test,private_providers=[],actual_ASTIS_parents=cells[1]['proof_digestion']['existing_substrate'],focused_build_jobs=jobs,status='FOCUSED_COMPILED_ONLY_INDEPENDENT_MATH_DECODER_WHOLE_MODULE_SOURCE_PENDING',remaining_boundary=c['truth_boundary'],compiler_lease='All final focused checks closed; failed or stopped diagnostic runs are not proof; recovery sorryAx is not proof; original seals unchanged.'))
adv.checkpoint_advance(c['advance_id'],worker_id=c['created_by'],route_fingerprint='selfadjoint-square/block-cancellation/scalar-CS/actual-budget',progress_signature=f'{jobs}EXIT0-three-standard3-original-input-LemmaB3',mathematical_delta=c['theorem_delta'],exact_residual='Independent mathematics,source-blind decoding,whole-module source/publication review and integration remain; B21/H1/B4/full papers/cost/composition open.')
pub.check_advance([leaf,decl],reviewed=False)
print(f'PASS focused68 freeze:{jobs} jobs,all3 standard3;5+6 literal BODY steps;2 neutral decoder packets;no PROVED_LOCAL/VERIFIED.')
