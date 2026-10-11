import pathlib,json,hashlib,re,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-private-rename92';O=B/'independent-math92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def put(n,v):
 with (D/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
src=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean';before=B/'private-name-inventory92/production.before.exactraw.lean'
old=before.read_bytes();new=src.read_bytes()
assert bind(before)['raw_sha256']=='46c637205d601786472e789bf4706a77b18ea6dad423ab33d1ac39491e71e111'
assert bind(src)['raw_sha256']=='d9dd0ce17df285bc73f68906589c4e5c598472eb3ba49c0c21f420e17f904277'
start=old.index('private def Δ'.encode());end=old.index(b'private def state',start);segment=old[start:end]
assert segment.count('Δ'.encode())==22
assert new==old[:start]+segment.replace('Δ'.encode(),b'orderedSimplex')+old[end:]
assert old[old.index(b'def actual_ordered_prefix_statement'):]==new[new.index(b'def actual_ordered_prefix_statement'):]
assert b'orderedSimplex' not in old
seal=json.loads((B/'root.statement-seal92.json').read_text(encoding='utf-8'))['expanded_literal_Prop']
statement=new.decode().split('def actual_ordered_prefix_statement',1)[1].split('set_option maxHeartbeats',1)[0]
norm=lambda x:re.sub(r'\s+',' ',x).strip()
assert norm(statement)==norm(seal)
clean=re.sub(r'/\-[\s\S]*?\-/','',new.decode());assert not re.search(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
static=dict(before=bind(before),after=bind(src),exact_byte_transformation='Only 22 UTF-8 Delta identifiers replaced by orderedSimplex between private def Delta and private def state.',replacement_count=22,new_name_absent_before=True,public_definition_and_theorem_bytes_unchanged=True,sealed_expanded_statement_equal=True,fake_closure_scan='PASS',checked_base_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip())
put('static-audit92.native.json',static)
previouscopy=(O/'FreshWholeSourceKernel92.lean').read_bytes();assert previouscopy.startswith(old);suffix=previouscopy[len(old):]
copy=D/'FreshRenamedKernel92.lean'
with copy.open('xb') as f:f.write(new+suffix)
lake=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'
def run(label,args):
 argv=[str(lake)]+args;start=time.monotonic()
 with (D/(label+'.stdout.log')).open('xb') as out,(D/(label+'.stderr.log')).open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
 receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(src),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/(label+'.stdout.log')),stderr=bind(D/(label+'.stderr.log')))
 put(label+'.receipt.native.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True);assert result.returncode==0
 return receipt
kernel=run('kernel',['env','lean',str(copy.relative_to(R))])
log=(D/'kernel.stdout.log').read_text(encoding='utf-8');assert 'depends on axioms: [propext, Classical.choice.{u}, Quot.sound.{u}]' in norm(log)
assert not any(x in log for x in ['sorryAx','LOCAL_NO_VALUE','PROJECT_NO_VALUE','error:'])
assert 'PUBLIC_TYPE' in log and 'EXPANDED_PRIVATE_STATEMENT' in log
assert 'LOCAL_PROOF_CONSTANT_COUNT 53' in log and 'TRANSITIVE_ASTIS_CONSTANT_COUNT 121' in log
deps=[line.split(' ',1)[1] for line in log.splitlines() if line.startswith('EXTERNAL_ASTIS_DEPENDENCY AutoSamplingTheory.')]
olddeps=json.loads((O/'dependencies92.native.json').read_text(encoding='utf-8'))['public_external_ASTIS_dependencies'];assert deps==olddeps
leaf=run('leaf-build',['build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix'])
assert src.read_bytes()==new
report=dict(decision='ACCEPT_PRIVATE_ALPHA_RENAME_AND_TRANSFER_WHOLE_MATH_REVIEW',checked_base_HEAD=static['checked_base_HEAD'],source=bind(src),original_review=bind(O/'production-math-review92.native.json'),original_closed_manifest=bind(O/'closed-RAW92.native.json'),static_audit=bind(D/'static-audit92.native.json'),kernel=bind(D/'kernel.receipt.native.json'),leaf_build=bind(D/'leaf-build.receipt.native.json'),findings=[
'Exact byte reconstruction proves the sole change is 22 occurrences of the private simplex name Delta to orderedSimplex in its bounded definition/use segment. The replacement name did not occur before, so no capture or collision is introduced.',
'Every byte from the public actual_ordered_prefix_statement through the final theorem and namespace close is unchanged. Its full literal expansion still matches the original Statement Seal after whitespace normalization.',
'No premise, definition body, mathematical route, event support, density factor, measure, test domain, recurrence, or conclusion changed. This is an implementation inventory naming repair, not a source statement repair.',
'Fresh whole source elaboration plus kernel public type/expanded statement, axioms and dependency traversal passed. The same 53 local and 121 transitive ASTIS constants and five direct public dependencies remain, modulo the renamed private simplex.',
'Fresh explicit fixed-toolchain leaf Lake build passed, providing separate target-build acceptance. All six original analytic hypotheses and prior strict-prefix, n=0/T=0, stopped/top/zero-clock, rank-zero and arbitrary ENNReal-test conclusions transfer from the frozen whole mathematical review.'
],axioms=['propext','Classical.choice','Quot.sound'],public_dependencies=deps,limitations=['No canonical VERIFIED transition, commit, source-roundtrip acceptance or publication-completion claim.','Existing result is strict first-n-prefix law, not exactly-n or full A7; every original truth boundary remains.'],owned_writes_only=D.as_posix())
put('private-rename-review92.native.json',report)
inputs=[before,src,B/'root.statement-seal92.json',B/'private-name-inventory92/rename.json',O/'production-math-review92.native.json',O/'closed-RAW92.native.json',O/'dependencies92.native.json',O/'FreshWholeSourceKernel92.lean',R/'lake-manifest.json',lake]
put('closed-RAW92.native.json',dict(inputs=[bind(p) for p in inputs],outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()],closure='Native RAW inputs and outputs; manifest excludes itself. No production or canonical write.'))
print(json.dumps([bind(D/'private-rename-review92.native.json'),bind(D/'closed-RAW92.native.json')],indent=2),flush=True)
