import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;repo=out.parents[3]
pre=repo/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70';old=pre/'independent-header-source70'
sha=lambda b:hashlib.sha256(b).hexdigest()
inputs=[]
paths=[(pre/'header0-proposed-expanded.lean','original-sealed-header.RAW.lean'),(pre/'root.statement-seal70.json','root.statement-seal70.RAW.json'),
 (old/'lease.final.json','prior-CLOSED83.lease.RAW.json'),(old/'owned-manifest.json','prior-CLOSED83.manifest.RAW.json'),
 (old/'independent-header-source70.decision.json','prior-CLOSED83.decision.RAW.json'),
 (old/'source-expectations70.before-header.json','prior-source-expectations.before-candidate.RAW.json'),
 (old/'finite-coverage-manifest70.json','prior-source-coverage.RAW.json'),
 (old/'parent69-retention-and-binder-audit.json','prior-binder-audit.RAW.json'),
 (old/'mean-g-source-and-internal-completion70.json','prior-mean-g-obligation.RAW.json'),
 (old/'primary419-NODE-EXCLUDED70.json','prior-primary419-inventory.RAW.json')]
for p,n in paths:
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');(out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
    inputs.append(dict(original_path=p.as_posix(),name=n,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
assert inputs[0]['RAW_sha256']=='9261f488432664370ae1b1146b098bf86c17dfd476bfe2e149d3024a77529e19'
assert inputs[2]['RAW_sha256']=='0aba415246dd79cee1429a046c6a1d61ce9924bb32de50caeef60c0a8cf2f714'
assert inputs[3]['RAW_sha256']=='875f0d90ddfc801b3bfb17928a5971f5d1fd1fb741c85196ebf782f117aa5084'
assert inputs[4]['RAW_sha256']=='3d33354176f63c435d030ec52d66f36cdb45eeb3921139f2528bc49e70fe4fa6'
expect=dict(schema='type-ascription70-source-expectations-before-overlay-v1',actual_pid=os.getpid(),candidate_overlay_not_yet_read=True,
    approved_header_RAW_sha256=inputs[0]['RAW_sha256'],approved_prior_CLOSED83_lease_RAW_sha256=inputs[2]['RAW_sha256'],
    permitted_change='Wrap the entire existing public return type in (show Prop from ...), increasing existing type-line indentation by two spaces and adding only the wrapper syntax.',
    binder_prefix='Every original public name, typeclass, type parameter and six caller conditions must remain byte-exact before return-type colon.',
    inverse_transform='Remove exactly the outer show-Prop wrapper and its one matching outer closing parenthesis, undo exactly two leading spaces on each original return-type line; the complete original sealed LF header must be recovered.',
    semantic_boundary='Prop ascription constrains the same return expression; no new witness, premise, private declaration/provider, tactic or conclusion may be introduced.',
    retained_source_obligations=['Actual SAME g=U(Pf-(f-Pf)); mean_g remains internally produced conclusion, never caller.',
       'Actual condExpL2 g constrains gP; gV=V0*Rg, exact two signed rotations and square-sum energy remain unchanged.',
       'All6 original callers,12 common witnesses,all69 old conclusions; rank0/alphaeta1/no ontoV/no68sharpenergy/no extra regularity.',
       'Original419item/7region/22node49edge primary-first coverage remains reused; no new full source/theorem/VERIFIED credit.'],
    compiler_boundary='Source representation equivalence only. A compiler diagnostic may fail; this review does not certify elaboration or fix failure.',
    no_Lean_compile_proofsearch_canonical_Git_ledger_Goal_edits=True)
(out/'expectations.before-overlay.json').write_text(json.dumps(expect,sort_keys=True,indent=2)+'\n',encoding='utf-8')
(out/'input-manifest.initial.json').write_text(json.dumps(dict(schema='type-ascription70-initial-input-manifest-v1',inputs=inputs,count=len(inputs)),sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_pid=os.getpid(),initial_inputs=len(inputs),expectations_RAW_sha256=sha((out/'expectations.before-overlay.json').read_bytes()),candidate_overlay_not_yet_read=True),sort_keys=True))
