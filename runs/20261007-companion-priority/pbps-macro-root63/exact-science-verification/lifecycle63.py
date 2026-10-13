from verify63 import *

BOUNDARY=['second B.5 identity beyond this new root target','centered lower root order/coercivity','centered root inverse and polar factor','weak H1 domains and regularity/boundary adapters','event dynamics/nonexplosion/invariance/hypocoercivity','full paper mixing/error results','actual-input expected-query costs and PBPS/SPHMC composition','Gaussian Cloud and midpoint results','serialized aggregate/repository/CI acceptance','rendered Exposition Seal, merge, deployment and PURIFIED reader completion']

def decision():
    assert_frozen()
    build=read(OUT/'focused.result.json');bindings=read(OUT/'bindings.result.json');gates=read(OUT/'gates.result.json')
    assert build['status']==bindings['status']=='PASS'
    assert read(OUT/'publication.reviewed.result.json')['status']=='PASS' and read(OUT/'fakeclosure.result.json')['status']=='PASS'
    for name in ['publication.packet','publication.diff','contributor.diff','semantic']:assert read(OUT/(name+'.receipt.json'))['exit_code']==0
    assert read(OUT/'frontier.metadata.receipt.json')['exit_code']==1
    audit=read(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot.json')
    review=read(RUN/'independent-source63/review.payload.json')
    assert audit['state']=='accepted' and review['verdict']=='equivalent-after-elaboration' and review['binder_audit']['EXCESS_count']==0 and not review['repairs']
    assert review['independent_from_formalizer'] and review['independent_from_decoder']
    assert len(review['semantic_slots'])==7
    debt={'classification':'IMPLEMENTATION_FAILED integration metadata','exact_commit':SCI,'frontier_check_exit_code':1,'defects':['learning_contract.failure_class=API_INSTANCE_ALIGNMENT is not an allowed enum','non-success failure lacks required=true/completed explicit salvage audit'],'mathematical_statement_or_proof_changed':False,'full_repository_acceptance':False,'repair_owner':'root sole serialized stabilization lane','scientific_VERIFIED_scope':'Exact original-input main/Test Lean truth, current reviewed publication and source fidelity, fakeclosure cleanliness only; no aggregate or rendered reader acceptance'}
    late=[]
    for sub in ['remote-science63-site-failure-log','remote-formal63-failure-log']:
        d=RUN/sub
        if d.exists():
            for p in sorted(d.rglob('*')):
                if p.is_file():
                    row=pin(p);dest=OUT/'late-repository-debt-inputs'/sub/p.relative_to(d);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());row['exact_raw_snapshot']=dest.as_posix();late.append(row)
    reasons=[
        {'step':1,'source':['1.1','2.6','2.7','B.4','C.1 density'],'argument':'The actual centered-defect producer receives only C2, the two global Hessian bounds and capped positive eta. Its probability, normalized every-y S, stationary disintegration, reflection and T are outputs. M0 is identified with the displayed canonical M by per-observable AE equality and Lp extensionality; no alternative model is supplied.'},
        {'step':2,'source':['B.1','B.2'],'argument':'P is HP.starProjection. Projection range/fixed-point laws identify ran(P)=HP. The actual range producer identifies ran(M)=ran(P); restricting M and composing its equivRange with ofEq yields onto e with inclusion(eu)=Mu. The product/comap Fact and closed-subspace structures are derived internally.'},
        {'step':3,'source':['B.3','B.4 compression paragraph'],'argument':'Evaluate actual MT=PUPM on e.symm f. Canonical inclusion compatibility and P fixing HP imply A=eTe^-1. Isometric conjugation gives selfadjointness and all-HP contraction. The scalar and HP endomorphisms stay distinct, and no positivity of A is asserted.'},
        {'step':4,'source':['B.5 first identity'],'argument':'Idempotence gives PB=0. The second reflected witness U2 has exactly the same per-observable AE action as U, so Lp extensionality aligns it. The existing full-joint Gram is B0*B0=P-AJ^2. It is not I_joint-AJ^2.'},
        {'step':5,'source':['B.5','B.10','D.1'],'argument':'The real root producer consumes internally derived positivity of I_scalar-T^2. Transport the SAME Gamma through e to positive GammaP. Multiplicative conjugation yields GammaP^2=I_HP-A^2. Typed adjoint composition gives B*B=i*(P-AJ^2)i; P fixes HP and AJ intertwines inclusion A, so the restriction is precisely I_HP-A^2.'},
        {'step':6,'source':['B.11','D.1 adjoint and norm conventions'],'argument':'Scalar root energy at e.symm f plus the actual defect identity and isometry norm preservation proves the all-HP energy. Gram and root selfadjointness equate squared leakage/root norms; their nonnegativity permits unsquaring.'},
        {'step':7,'source':['B.10','D.1 unique nonnegative root convention'],'argument':'For every positive G on HP with G^2=I_HP-A^2, pull back by e.symm. The resulting positive marginal G0 squares to I_scalar-T^2. Generic compiled positive-root uniqueness identifies G0=Gamma, and conjugation back gives G=GammaP. The universal G conjunct is outside every-f energy and supplies no alternative energy, CFC or commutation premise.'},
        {'step':8,'source':['B.11 energy consequence'],'argument':'The genuine Test retains exactly the original inputs and all theorem witnesses. Energy and norm(Af)^2>=0 imply norm(GammaP f)<=norm(f) by nonnegative-square arithmetic; no energy/certificate/root premise is supplied to the theorem.'}
    ]
    payload={'schema_version':1,'result':'ACCEPTED_SCOPED_EXACT_SCIENCE63_WITH_EXPLICIT_INTEGRATION_METADATA_DEBT','verifier_id':ACTOR,'actual_author_pid':os.getpid(),'authored_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'verified_commit':SCI,'actual_git_parent':PARENT,'independent_from_formalizer':True,'independent_from_blind_decoder':True,'independent_from_source_reviewer':True,'no_production_or_canonical_metadata_edits':True,'whole_main_and_genuine_Test_read':True,'input_contract_audit':{'C2':True,'two_global_Hessian_bounds':True,'positive_alpha_ordered_beta':True,'eta_positive_beta_eta_le_one':True,'rank_zero_permitted':True,'alpha_eta_equal_one_permitted':True,'extra_public_binders':[],'supplied_probability_range_root_CFC_energy_premises':[],'EXCESS':0},'operator_domain_audit':{'canonical_M_onto_exact_HP':True,'HP':'lpMeas for comap snd = ran(P), closed macro subspace','same_e_U_T_Gamma':True,'A':'HP -> HP','B':'HP -> joint L2, with PB=0','B_adjoint':'joint L2 -> HP','full_joint_Gram':'P - AJ^2','macro_Gram':'I_HP - A^2 = GammaP^2','alternative_positive_G_quantifier_outside_every_f':True,'alternative_energy_premise':False,'AE_order':'per observable; no simultaneous exceptional-set claim','S_density_order':'every y; normalized tilted volume law'},'eight_formula_proof_arguments':reasons,'current_literal_headers_and_code_bindings':bindings,'focused_current_Lean':build,'current_gates':gates,'reviewed_publication':read(OUT/'publication.reviewed.result.json'),'fakeclosure_scan':read(OUT/'fakeclosure.result.json'),'independent_source_audit':{'audit_id':audit['id'],'audit_state':audit['state'],'verdict':review['verdict'],'source_reviewer':review['reviewer'],'publication_binding_sha256':audit['publication_binding_sha256'],'semantic_slots':review['semantic_slots'],'source_coverage_region_count':24,'source_assumption_repair':False,'mechanical_presentation_repair':'Only step3 exact line region/indentation binding changed after math closure; current all8 literal spans separately source reviewed.'},'source_vs_Lean_graph_distinction':'Source-first raw regions/consumer topology remain source correspondence. Scalar-root conjugation and typed restriction are explicit ASTIS implementation adapters; imports/source names/conceptual mirrors do not create theorem implication.','conceptual_mirror_audit':read(RUN/'conceptual-mirror-audit63.json'),'integration_metadata_debt':debt,'late_authoritative_repository_failure_inputs':late,'remaining_boundary':BOUNDARY,'full_ASTIS_gate_run':False,'global_site_rebuild_run':False,'MERGED':False,'PURIFIED':False,'full_paper_complete':False,'whole_Goal_complete':False,'own_typed_diagnostic_corrections':[{'class':'IMPLEMENTATION_FAILED','issue':'Initial freeze collector followed overly broad historical path strings, including a Windows alternate-stream-like prose suffix; completed fresh restricted v2 manifest before the only compiler run. Old partial snapshots remain retained, not mathematical inputs.'},{'class':'IMPLEMENTATION_FAILED','issue':'Gate helper import path omitted tools; restored the import path and completed only the pending scanner/reviewed gate without rerunning passed gates.'},{'class':'IMPLEMENTATION_FAILED','issue':'Initial header extractor included the single space belonging to the Test theorem/body delimiter. Excluded that delimiter byte exactly; statement bytes then match sealed header1 without token/assumption normalization.'}]}
    write('named-verification.payload.json',payload)
    write('verification.decision.json',{'result':payload['result'],'actor':ACTOR,'exact_commit':SCI,'named_complete_RAW_payload':pin(OUT/'named-verification.payload.json'),'required_scoped_gates_passed':True,'integration_metadata_debt':debt,'remaining_boundary':BOUNDARY,'canonical_VERIFIED_transition_pending':True})
    print('Independent exact-science63 decision authored; required scoped gates PASS, integration metadata debt retained')

def transition():
    assert_frozen()
    decision=read(OUT/'verification.decision.json');assert decision['required_scoped_gates_passed']
    sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
    from tools import astis_advance as adv
    item=adv.current_advances()[ADV];assert item['state']=='PROVED_LOCAL' and item['owner_id']!=ACTOR
    ledger=ROOT/'runs/substantive_advances.jsonl';before=ledger.read_bytes();(OUT/'ledger.before-own-VERIFIED.exactraw.snapshot').write_bytes(before)
    evidence={'verifier_id':ACTOR,'verified_commit':SCI,'gate':{'focused_current_build':pin(OUT/'focused.receipt.json'),'focused_result':pin(OUT/'focused.result.json'),'publication_diff_current_parent':pin(OUT/'publication.diff.receipt.json'),'contributor_diff_current_parent':pin(OUT/'contributor.diff.receipt.json'),'semantic_current':pin(OUT/'semantic.receipt.json'),'reviewed_publication':pin(OUT/'publication.reviewed.result.json'),'scope':'exact bounded science; aggregate/repository/reader acceptance remains open'},'source_audit':{'canonical_audit':'ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot','native_source_run_sha256':'32b39c9148d59120ba67a632e836ea203a7d8c8477703c27a9c774886857b2e5','all_current_qualified_bindings':pin(OUT/'bindings.result.json'),'independent_scientific_payload':pin(OUT/'named-verification.payload.json'),'source_fidelity_verdict':'equivalent-after-elaboration','EXCESS':0,'source_assumption_repairs':0},'fake_closure_scan':pin(OUT/'fakeclosure.result.json'),'publication_declarations':[DECL],'independent_verification_decision':pin(OUT/'verification.decision.json'),'integration_metadata_debt':decision['integration_metadata_debt'],'remaining_boundary':BOUNDARY,'full_repository_gate_pass':False,'rendered_Exposition_Seal':False}
    adv.transition_advance(ADV,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-science-verification'],evidence=evidence)
    after=ledger.read_bytes();assert after.startswith(before)
    tail=after[len(before):];rows=[json.loads(line) for line in tail.splitlines() if line.strip()];assert len(rows)==1
    current=adv.current_advances()[ADV];assert current['state']=='VERIFIED' and current['latest_evidence']['verifier_id']==ACTOR
    (OUT/'ledger.after-own-VERIFIED.exactraw.snapshot').write_bytes(after)
    write('transition.result.json',{'status':'OWN_INDEPENDENT_APPROVED_VERIFIED_APPEND','advance_id':ADV,'worker_id':ACTOR,'verified_commit':SCI,'actual_pid':os.getpid(),'owner_before':item['owner_id'],'state_before':'PROVED_LOCAL','state_after':'VERIFIED','before_ledger_pin':pin(OUT/'ledger.before-own-VERIFIED.exactraw.snapshot'),'after_ledger_pin':pin(ledger),'after_snapshot':pin(OUT/'ledger.after-own-VERIFIED.exactraw.snapshot'),'before_raw_prefix_preserved':True,'appended_records':rows,'append_count':1,'canonical_frontier_or_audit_mutated':False})
    print('VERIFIED independently appended for exact SCI63; root self-verification absent; repository metadata debt retained')

def finalize():
    assert_frozen();tr=read(OUT/'transition.result.json');assert tr['status']=='OWN_INDEPENDENT_APPROVED_VERIFIED_APPEND'
    payload=read(OUT/'named-verification.payload.json');ph=sha((OUT/'named-verification.payload.json').read_bytes())
    artifacts=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['lease.json','run.json','run.logical.sha256','native.receipt.json','output.manifest.json','proposed-lease.closed.json','finalizer.stdout.log','finalizer.stderr.log','finalizer.process.receipt.json','readback.stdout.log','readback.stderr.log','readback.process.receipt.json','terminal.readback.json']]
    x={'schema_version':1,'kind':'independent-exact-science63-verification','actor':ACTOR,'actual_finalizer_pid':os.getpid(),'verified_commit':SCI,'actual_parent':PARENT,'whole_input_manifest':read(OUT/'input.manifest.json'),'complete_named_verification_payload':payload,'complete_named_RAW_payload_sha256':ph,'approved_independent_ledger_transition':tr,'artifacts_before_native_finalization':artifacts,'whole_run_hash_recipe':'SHA256 sorted compact ensure_ascii=False UTF-8 JSON of WHOLE run.json except ONLY top-level run_sha256','named_payload_hash_recipe':'SHA256 COMPLETE exact RAW named-verification.payload.json bytes, distinct from whole logical run hash','final_boundary':BOUNDARY,'repository_acceptance':False,'full_Goal_complete':False}
    x['run_sha256']=sha(compact(x));assert x['run_sha256']!=ph;write('run.json',x)
    (OUT/'run.logical.sha256').write_text(x['run_sha256']+'\n',encoding='utf-8')
    write('native.receipt.json',{'status':'FOREGROUND_FINALIZER_OUTPUTS_WRITTEN','actual_finalizer_pid':os.getpid(),'verifier_id':ACTOR,'verified_commit':SCI,'whole_run_sha256':x['run_sha256'],'run_RAW':pin(OUT/'run.json'),'distinct_complete_named_RAW_payload_sha256':ph,'named_payload':pin(OUT/'named-verification.payload.json'),'independent_transition':pin(OUT/'transition.result.json'),'full_repository_acceptance':False,'integration_metadata_debt':payload['integration_metadata_debt'],'closed_lease_written':False})
    print(json.dumps({'status':'NATIVE_FINALIZER_SUCCESS','actual_finalizer_pid':os.getpid(),'whole_run_sha256':x['run_sha256'],'distinct_named_RAW_payload_sha256':ph}),flush=True)

def capturechild(label,action):
    start=time.time()
    with (OUT/(label+'.stdout.log')).open('wb') as out,(OUT/(label+'.stderr.log')).open('wb') as err:
        p=subprocess.Popen([PY,'-B','-X','utf8',str(OUT/'lifecycle63.py'),action],cwd=ROOT,stdout=out,stderr=err);pid=p.pid;rc=p.wait()
    write(label+'.process.receipt.json',{'status':'FOREGROUND_TERMINAL_CLOSED','parent_pid':os.getpid(),'actual_child_pid':pid,'argv':[PY,'-B','-X','utf8',str(OUT/'lifecycle63.py'),action],'exit_code':rc,'elapsed_seconds':time.time()-start,'stdout':pin(OUT/(label+'.stdout.log')),'stderr':pin(OUT/(label+'.stderr.log'))})
    assert rc==0
    print((OUT/(label+'.stdout.log')).read_text(encoding='utf-8'))

def prepareclose():
    assert_frozen();x=read(OUT/'run.json');rcpt=read(OUT/'native.receipt.json');proc=read(OUT/'finalizer.process.receipt.json');assert proc['exit_code']==0 and proc['actual_child_pid']==rcpt['actual_finalizer_pid']
    write('terminal.readback.json',{'status':'ACTUAL_FOREGROUND_FINALIZER_READBACK','actual_reader_pid':os.getpid(),'finalizer_actual_pid':proc['actual_child_pid'],'observed_exit_code':proc['exit_code'],'stdout':pin(OUT/'finalizer.stdout.log'),'stderr':pin(OUT/'finalizer.stderr.log'),'native_receipt':pin(OUT/'native.receipt.json'),'whole_run_sha256':x['run_sha256'],'distinct_complete_named_RAW_payload_sha256':rcpt['distinct_complete_named_RAW_payload_sha256']})
    exclusions=['output.manifest.json','proposed-lease.closed.json','lease.json','readback.stdout.log','readback.stderr.log','readback.process.receipt.json']
    rows=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in exclusions]
    write('output.manifest.json',{'status':'COMPLETE_OWNED_OUTPUT_MANIFEST_BEFORE_CLOSED_CANDIDATE_READBACK','artifacts':rows,'layer_exclusions':exclusions,'closure_rule':'CLOSED lease includes candidate readback process/log pins, manifest pin and all remaining outputs; proposed lease and lease identical'})
    write('proposed-lease.closed.json',{'status':'CLOSED_LAST','verifier_id':ACTOR,'verified_commit':SCI,'prepared_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'whole_run_sha256':x['run_sha256'],'distinct_complete_named_RAW_payload_sha256':rcpt['distinct_complete_named_RAW_payload_sha256'],'native_receipt':pin(OUT/'native.receipt.json'),'output_manifest':pin(OUT/'output.manifest.json'),'terminal_readback':pin(OUT/'terminal.readback.json'),'self_layer_exclusions':['lease.json','proposed-lease.closed.json'],'final_write_rule':'After actual foreground read-only candidate binding check exits0, close writes only lease.json as final owned write. No owned writes afterwards.','approved_independent_VERIFIED_transition':pin(OUT/'transition.result.json'),'integration_metadata_debt':read(OUT/'verification.decision.json')['integration_metadata_debt']})
    print('Prepared exact CLOSED candidate and output manifest')

def readback():
    assert_frozen();x=read(OUT/'run.json');h=x.pop('run_sha256');assert sha(compact(x))==h
    ph=sha((OUT/'named-verification.payload.json').read_bytes());assert ph==x['complete_named_RAW_payload_sha256'] and ph!=h
    for row in read(OUT/'output.manifest.json')['artifacts']:assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
    c=read(OUT/'proposed-lease.closed.json');assert c['whole_run_sha256']==h and c['distinct_complete_named_RAW_payload_sha256']==ph
    assert read(OUT/'transition.result.json')['state_after']=='VERIFIED'
    print(json.dumps({'status':'READ_ONLY_CLOSED_CANDIDATE_BINDING_PASS','actual_reader_pid':os.getpid(),'owned_manifest_artifacts':len(read(OUT/'output.manifest.json')['artifacts']),'whole_run_sha256':h,'distinct_named_RAW_payload_sha256':ph}),flush=True)

def close():
    proc=read(OUT/'readback.process.receipt.json');assert proc['exit_code']==0
    c=read(OUT/'proposed-lease.closed.json');c['actual_foreground_candidate_readback']=proc
    # Layer these process outputs after their actual terminal completion, then read them
    # back in this same foreground final closure process before the one final write.
    c['actual_final_closure_pid']=os.getpid()
    c['complete_owned_output_manifest_after_readback']=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['lease.json','proposed-lease.closed.json']]
    write('proposed-lease.closed.json',c)
    readback()
    for row in c['complete_owned_output_manifest_after_readback']:assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
    assert read(OUT/'finalizer.process.receipt.json')['exit_code']==0
    (OUT/'lease.json').write_bytes((OUT/'proposed-lease.closed.json').read_bytes())
    print(json.dumps({'status':'CLOSED_LAST_FINAL_WRITE_COMPLETED','actual_closure_pid':os.getpid(),'lease_RAW_sha256':sha((OUT/'lease.json').read_bytes()),'whole_run_sha256':c['whole_run_sha256'],'distinct_named_RAW_payload_sha256':c['distinct_complete_named_RAW_payload_sha256']}),flush=True)

def checkclosed():
    c=read(OUT/'lease.json');assert c['status']=='CLOSED_LAST';assert (OUT/'lease.json').read_bytes()==(OUT/'proposed-lease.closed.json').read_bytes()
    for row in c['complete_owned_output_manifest_after_readback']:assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
    print(json.dumps({'status':'FINAL_READ_ONLY_CLOSED_PASS','whole_run_sha256':c['whole_run_sha256'],'distinct_named_RAW_payload_sha256':c['distinct_complete_named_RAW_payload_sha256'],'owned_files':len(c['complete_owned_output_manifest_after_readback'])+2,'lease_RAW_sha256':sha((OUT/'lease.json').read_bytes())}),flush=True)

if __name__=='__main__':
    {'decision':decision,'transition':transition,'finalize':finalize,'capture-finalize':lambda:capturechild('finalizer','finalize'),'prepare-close':prepareclose,'readback':readback,'capture-readback':lambda:capturechild('readback','readback'),'close':close,'check-closed':checkclosed}[sys.argv[1]]()
