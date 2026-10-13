from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
freeze=json.loads((O/'input-freeze90.json').read_text('utf8'))
kernel=json.loads((O/'kernel-dependency90.json').read_text('utf8'))
for d in freeze['actual_inputs']+kernel['ASTIS_source_files']:
 assert pin(R/d['path'])==d
names=['reread_primary90.py','.private.primary90.reread-A1-A2.json','primary-reread90.chronology.json',
 'prepare_and_compile90.py','module90.exactraw.lean','input-freeze90.json','collaborator-preservation90.initial.json',
 'historical-probe-filename-lookup90.negative.json','FreshWholeSourceKernelClosure90.lean','instrumentation-origin90.json',
 'fresh-focused-build.stdout.log','fresh-focused-build.stderr.log','fresh-focused-build.receipt.json',
 'fresh-whole-source-kernel.stdout.log','fresh-whole-source-kernel.stderr.log','fresh-whole-source-kernel.receipt.json',
 'analyze_kernel_and_math90.py','kernel-dependency90.json','fake-closure90.json','whole-mathematics90.pre-exposition.json','close_kernel_work90.py']
with (O/'kernel-work90.closed-RAW-manifest.json').open('x',encoding='utf8',newline='\n') as f:
 json.dump({'status':'CLOSED_KERNEL_AND_PREREAD_SUBPACKET_ONLY_EXPOSITION_FINAL_REVIEW_PENDING',
 'reviewer_id':'/root/exact_verify77','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'frozen_inputs':freeze['actual_inputs'],'actual_transitive_ASTIS_source_files':kernel['ASTIS_source_files'],
 'owned_artifacts':[pin(O/n) for n in names],'whole_module_focused_and_fresh_source_exit0':True,
 'standard_axioms_only':kernel['axioms'],'no_VERIFIED_or_final_whole_review_claim':True,
 'privacy':'Long source extracts .private.* remain local and excluded from public packet/archive.',
 'self_digest_external_not_embedded':True},f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(pin(O/'kernel-work90.closed-RAW-manifest.json'),indent=2))
