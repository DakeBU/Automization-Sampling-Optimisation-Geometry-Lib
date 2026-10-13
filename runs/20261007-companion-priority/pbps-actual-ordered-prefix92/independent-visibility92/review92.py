import pathlib,json,hashlib,re,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-visibility92';O=B/'independent-private-rename92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def put(n,v):
 if (D/n).exists():
  assert json.loads((D/n).read_text(encoding='utf-8'))==v
  return
 with (D/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
src=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean';before=B/'statement-helper-visibility92/production.before.exactraw.lean';old=before.read_bytes();new=src.read_bytes()
assert bind(before)['raw_sha256']=='d9dd0ce17df285bc73f68906589c4e5c598472eb3ba49c0c21f420e17f904277'
assert bind(src)['raw_sha256']=='4737e98180ad69da03ad8b68f72f996ebe265b1eda1fafaa0521f591b7644ead'
needle=b'def actual_ordered_prefix_statement';assert old.count(needle)==1
assert new==old.replace(needle,b'private '+needle)
seal=json.loads((B/'root.statement-seal92.json').read_text(encoding='utf-8'))['expanded_literal_Prop'];statement=new.decode().split('private def actual_ordered_prefix_statement',1)[1].split('set_option maxHeartbeats',1)[0]
norm=lambda x:re.sub(r'\s+',' ',x).strip()
assert norm(statement)==norm(seal)
assert old[old.index(b'theorem actual_ordered_prefix_law'):]==new[new.index(b'theorem actual_ordered_prefix_law'):]
clean=re.sub(r'/\-[\s\S]*?\-/','',new.decode());assert not re.search(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
static=dict(before=bind(before),after=bind(src),exact_byte_transformation='Insert private and one space before the unique def actual_ordered_prefix_statement; all other bytes unchanged.',public_theorem_source_unchanged=True,helper_expanded_statement_matches_seal=True,checked_base_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),fake_closure_scan='PASS')
put('static-audit92.native.json',static)
previouscopy=(O/'FreshRenamedKernel92.lean').read_bytes();assert previouscopy.startswith(old);suffix=previouscopy[len(old):]
copy=D/'FreshPrivateStatementKernel92.lean'
if copy.exists():assert copy.read_bytes()==new+suffix
else:
 with copy.open('xb') as f:f.write(new+suffix)
lake=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'
def run(label,args):
 if (D/(label+'.receipt.native.json')).exists():
  previous=json.loads((D/(label+'.receipt.native.json')).read_text());assert previous['exit_code']==0
  return previous
 argv=[str(lake)]+args;start=time.monotonic()
 with (D/(label+'.stdout.log')).open('xb') as out,(D/(label+'.stderr.log')).open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
 receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(src),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/(label+'.stdout.log')),stderr=bind(D/(label+'.stderr.log')))
 put(label+'.receipt.native.json',receipt);print(json.dumps(receipt),flush=True);assert result.returncode==0
 return receipt
kernel=run('kernel',['env','lean',str(copy.relative_to(R))]);log=(D/'kernel.stdout.log').read_text(encoding='utf-8')
assert 'depends on axioms: [propext, Classical.choice.{u}, Quot.sound.{u}]' in norm(log)
assert not any(x in log for x in ['sorryAx','LOCAL_NO_VALUE','PROJECT_NO_VALUE','error:'])
assert 'PUBLIC_TYPE' in log and 'EXPANDED_PRIVATE_STATEMENT' in log
assert 'LOCAL_PROOF_CONSTANT_COUNT 53' in log and 'TRANSITIVE_ASTIS_CONSTANT_COUNT 121' in log
deps=[line.split(' ',1)[1] for line in log.splitlines() if line.startswith('EXTERNAL_ASTIS_DEPENDENCY AutoSamplingTheory.')]
olddeps=json.loads((O/'private-rename-review92.native.json').read_text(encoding='utf-8'))['public_dependencies'];assert deps==olddeps
public=log.split('PUBLIC_TYPE ',1)[1].split('EXPANDED_PRIVATE_STATEMENT',1)[0]
assert 'actual_ordered_prefix_statement' in public
assert re.search(r'^LOCAL_EDGE AutoSamplingTheory\..*actual_ordered_prefix_law -> _private\..*\.actual_ordered_prefix_statement$',log,re.M)
oldlog=(O/'kernel.stdout.log').read_text(encoding='utf-8');expanded=log.split('EXPANDED_PRIVATE_STATEMENT ',1)[1];oldexpanded=oldlog.split('EXPANDED_PRIVATE_STATEMENT ',1)[1]
assert norm(expanded)==norm(oldexpanded)
put('kernel-statement-transfer92.native.json',dict(private_helper_resolved_from_public_kernel_type=True,expanded_private_value_equals_previous_public_value=True,local_reachable_constants=53,transitive_ASTIS_constants=121,public_dependencies=deps,axioms=['propext','Classical.choice','Quot.sound']))
leaf=run('leaf-build',['build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix']);assert src.read_bytes()==new
report=dict(decision='ACCEPT_PRIVATE_STATEMENT_VISIBILITY_AND_TRANSFER_WHOLE_MATH_REVIEW',checked_base_HEAD=static['checked_base_HEAD'],source=bind(src),prior_delta_review=bind(O/'private-rename-review92.native.json'),prior_closed_manifest=bind(O/'closed-RAW92.native.json'),original_whole_math_review=bind(B/'independent-math92/production-math-review92.native.json'),static_audit=bind(D/'static-audit92.native.json'),kernel_statement_transfer=bind(D/'kernel-statement-transfer92.native.json'),kernel_receipt=bind(D/'kernel.receipt.native.json'),leaf_build_receipt=bind(D/'leaf-build.receipt.native.json'),findings=[
'Exactly one private modifier and following space were inserted before the transparent Prop helper definition. All preceding proof bodies, helper mathematical body, and public theorem proof bytes are unchanged.',
'The public theorem kernel type genuinely references the generated private statement constant. The checker resolves that constant from the public type and prints its value; the full expanded value equals the previous public helper value after whitespace normalization and matches the original sealed literal proposition.',
'Visibility does not add a hypothesis or hide an unproved mathematical assumption: the helper has a definition body, and the public theorem proof reaches the full actual all-n induction, geometry, history identification and measure/mass closure.',
'Fresh whole source kernel check and explicit target Lake build both passed under the fixed toolchain and unchanged manifest. Only propext, Classical.choice and Quot.sound occur as axioms. Reachable local/transitive constants and direct public ASTIS dependencies are unchanged modulo the helper private name.',
'The original complete mathematics acceptance and prior simplex-renaming delta acceptance transfer to these exact bytes. No source-theorem repair, proof-route change or mathematical delta occurred.'
],truth_boundary=['Implementation visibility repair only; source acceptance/refreeze remains separately managed.','No canonical VERIFIED, commit, publication completion or exact-commit verification performed.','All original boundaries remain: strict first-n-prefix law, not exactly-n or full A7.'])
put('visibility-review92.native.json',report)
inputs=[before,src,B/'root.statement-seal92.json',O/'private-rename-review92.native.json',O/'closed-RAW92.native.json',O/'FreshRenamedKernel92.lean',O/'kernel.stdout.log',B/'independent-math92/production-math-review92.native.json',R/'lake-manifest.json',lake]
put('closed-RAW92.native.json',dict(inputs=[bind(p) for p in inputs],outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()],closure='Native RAW inputs and outputs; manifest excludes itself. No production or canonical write.'))
print(json.dumps([bind(D/'visibility-review92.native.json'),bind(D/'closed-RAW92.native.json')],indent=2),flush=True)
