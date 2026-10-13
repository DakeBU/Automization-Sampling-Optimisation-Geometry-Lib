import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;repo=out.parents[3]
pre=repo/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70';old=pre/'independent-header-source70'
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=[(pre/'header0-proposed-expanded.lean','original-sealed-header.RAW.lean'),(pre/'root.statement-seal70.json','root.statement-seal70.RAW.json'),
 (old/'lease.final.json','prior-CLOSED83.lease.RAW.json'),(old/'owned-manifest.json','prior-CLOSED83.manifest.RAW.json'),
 (old/'independent-header-source70.decision.json','prior-CLOSED83.decision.RAW.json'),
 (old/'source-expectations70.before-header.json','prior-source-expectations.before-candidate.RAW.json'),
 (old/'finite-coverage-manifest70.json','prior-source-coverage.RAW.json'),
 (old/'parent69-retention-and-binder-audit.json','prior-binder-audit.RAW.json'),
 (old/'mean-g-source-and-internal-completion70.json','prior-mean-g-obligation.RAW.json'),
 (old/'primary419-NODE-EXCLUDED70.json','prior-primary419-inventory.RAW.json')]
inputs=[]
for p,n in paths:
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
    inputs.append(dict(original_path=p.as_posix(),name=n,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
assert inputs[0]['RAW_sha256']=='9261f488432664370ae1b1146b098bf86c17dfd476bfe2e149d3024a77529e19'
expect=dict(schema='named-literal70-source-expectations-before-overlay-v1',actual_pid=os.getpid(),candidate_overlay_not_yet_read=True,
    approved_header_RAW_sha256=inputs[0]['RAW_sha256'],original_source_CLOSED83_lease_RAW_sha256=inputs[2]['RAW_sha256'],
    literal_value='The private def must have declared type Prop and its complete value must be the exact original sealed return expression, with no changed logical token, quantifier, witness, domain, formula or binder.',
    literal_parameters='Only the same original type parameters, typeclass parameters and six analytic conditions. These parameterize a proposition record, not an extra mathematical premise/provider.',
    public_header='Retain the exact original public theorem name and all original caller binders; conclude the private literal instantiated with exactly those same type/data parameters and six hypotheses.',
    proof_boundary='Permitted BODY representation delta is only unfold of the literal before the same existing BODY. Do not inspect or review the rest of BODY or claim it compiled.',
    reader_requirement='Public signature alone abbreviates the full statement. Reader must expose the complete exact private literal in an adjacent initially folded Lean panel with complete module link; this review does not establish that future rendering exists.',
    original_primary_first_coverage_reused=dict(math_items=419,regions=7,nodes=22,edges=49,NODE=173,EXCLUDED=246),
    obligations=['SAME actual g=U(Pf-(f-Pf)),mean_g internally produced,actual condExpL2 gP and gV=V0*Rg.',
        'Both exact rotation signs and square-sum energy;all6 callers/12commonwitnesses/all69oldconclusions retained.',
        'Rank0/alphaeta1/no ontoV/no68sharpenergy/no extra regularity; B21 corrector/B4/main/composition remain outside.',
        'Named literal is an exact proposition representation, never a proof ingredient/provider or caller certificate.'],
    no_Lean_compile_proofsearch_canonical_old_native_Git_ledger_Goal_edits=True,no_new_full_theorem_source_VERIFIED_credit=True)
(out/'expectations.before-overlay.json').write_text(json.dumps(expect,sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'input-manifest.initial.json').write_text(json.dumps(dict(schema='named-literal70-initial-input-manifest-v1',count=len(inputs),inputs=inputs),sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_pid=os.getpid(),candidate_overlay_not_yet_read=True,initial_inputs=len(inputs),
    expectations_RAW_sha256=sha((out/'expectations.before-overlay.json').read_bytes())),sort_keys=True))
