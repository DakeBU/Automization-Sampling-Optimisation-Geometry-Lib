import copy,datetime,hashlib,html,json,os,pathlib,re,sys
out=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path(r'E:\Samplinglib')
sys.dont_write_bytecode=True
sys.path[:0]=[str(repo/'tools'),str(repo/'website/scripts')]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
manifest=json.loads((out/'current-input-manifest.json').read_bytes())
input_list=manifest['inputs']
def pin(n,p,role):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 (out/n).write_bytes(b);(out/(n+'.LF')).write_bytes(lf)
 input_list.append(dict(name=n,original_path=str(p),role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf)))
 return b
scanner=pin('renderer.astis_site.RAW.py',repo/'tools/astis_site.py','bounded-single-module-scanner; no-full-project-scan')
api=pin('api.Adjoint.RAW.lean',repo/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','API-definition-only; no-proof-reuse-or-claim')
import astis_site as base
import inline_lean
module=repo/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean'
assert sha(module.read_bytes())=='7bbaae1abd67305749d385153019061eb055a7968a707f919e7d9ac9fc21846d'
base.project_lean_paths=lambda:[module]
modules,declarations=base.scan_project_sources()
known={d.full_name:d for d in declarations}
assert len(modules)==1 and len(declarations)==2
base._SOURCE_BY_NAME=known
base._ACTIVE_GIT=base.GitContext(commit='',ref='bounded-preview',remote_url='',web_root='',commit_published=False,public_source_links=False,dirty_files=set())
public='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining'
private=public+'_statement'
assert private in known and known[private].kind=='def' and known[private].source_line==17
exact=(out/'sealed.statement0.definition.lean').read_text(encoding='utf-8').strip()
assert known[private].source_text.strip()==exact
assert not known[private].has_placeholder and known[private].source_text.startswith('private def ')
rendered=inline_lean.disclosure(public,role='proof',explanation='Bounded metadata feasibility preview.',page='declarations/bounded-source69.html',helpers=(private,),trim_following_docstring=True)
(out/'reader-overlay.helper-fold.preview.html').write_text(rendered,encoding='utf-8')
assert 'data-inline-lean="'+private+'"' in rendered
assert html.escape(exact) in rendered
assert 'Exact module and namespace context' in rendered
assert rendered.index('data-inline-lean="'+public+'"')<rendered.index('data-inline-lean="'+private+'"')
api_lines=api.decode('utf-8').splitlines()
assert 'theorem _root_.isSelfAdjoint_starProjection' in api_lines[390]
assert 'hPself : IsSelfAdjoint P := isSelfAdjoint_starProjection HP' in module.read_text(encoding='utf-8')
original=json.loads((out/'current.lesson.RAW.json').read_bytes())
unit=original['units'][0]
assert 'helpers' not in unit
assert unit['mathlib_dependencies'][-1]=='Submodule.isSelfAdjoint_starProjection'
updated=copy.deepcopy(original)
updated['units'][0]['helpers']=[private]
updated['units'][0]['mathlib_dependencies'][-1]='isSelfAdjoint_starProjection'
restored=copy.deepcopy(updated);del restored['units'][0]['helpers'];restored['units'][0]['mathlib_dependencies'][-1]='Submodule.isSelfAdjoint_starProjection'
assert restored==original
proposal=dict(schema='source69-reader-api-metadata-overlay-v1',classification='reader-and-API-metadata-only; no-mathematical-repair',target='website/content/declaration_lessons/pbps-actual-reflection-intertwining.json',base_RAW_sha256=sha((out/'current.lesson.RAW.json').read_bytes()),operations=[dict(op='add',path='/units/0/helpers',value=[private]),dict(op='replace',path='/units/0/mathlib_dependencies/6',old='Submodule.isSelfAdjoint_starProjection',value='isSelfAdjoint_starProjection')],unchanged=['Lean module','private literal Prop','six public analytic conditions','all witnesses and conclusions','six BODY spans and formulas','blind neutral packet'],application_by='root-only-after-bounded-independent-decision')
put('reader-api-metadata-overlay.proposal.json',proposal)
decision=dict(schema='source69-reader-api-metadata-overlay-decision-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision='APPROVE_EXACT_TWO_METADATA_FIELDS',proposal_RAW_sha256=sha((out/'reader-api-metadata-overlay.proposal.json').read_bytes()),mathematical_repair=False,source_verdict=False,canonical_writes=False,scanner=dict(scanned_module_count=1,declaration_count=2,private_full_identity=private,source_line=17,complete_literal_Prop_matches_sealed_definition=True),rendering=dict(preview='reader-overlay.helper-fold.preview.html',scope='Existing inline_lean.disclosure only; no full-site build or browser rendering.',complete_private_Prop_in_adjacent_proof_fold=True,public_signature_fold_preserved_by_unchanged_renderer=True,exact_module_context_link_retained=True,limitation='Supporting proof called by the result above is the renderer fixed label; this private def is a proposition record, not a mathematical provider.'),API=dict(source='.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',line=391,declared_name='_root_.isSelfAdjoint_starProjection',call_spelling='isSelfAdjoint_starProjection',old_spelling='Submodule.isSelfAdjoint_starProjection',correction_is_reference_metadata_only=True),exact_two_fields_only=True,all_other_lesson_fields_equal=True)
put('reader-api-metadata-overlay.decision.json',decision)
put('current-input-manifest.json',manifest)
print(json.dumps(dict(decision=decision['decision'],proposal_sha256=decision['proposal_RAW_sha256'],decision_sha256=sha((out/'reader-api-metadata-overlay.decision.json').read_bytes()),private_full_identity=private,source_line=17,actual_pid=os.getpid()),sort_keys=True))
