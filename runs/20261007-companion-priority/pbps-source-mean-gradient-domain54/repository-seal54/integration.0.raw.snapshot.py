from common import *
sys.path[:0]=[str(R),str(R/'tools'),str(R/'website/scripts')]
from tools import astis
notes=load(B/'integration.notes.json'); assert notes['registry_count']==495 and notes['root_jobs']==9157 and notes['test_jobs']==9443 and notes['proof_commit']==notes['verified_commit']==SCI
for e in notes['checks']+notes['shared_files']: assert equal(e),e['path']
assert len(notes['checks'])==24 and len(notes['shared_files'])==10
names=['tests','mandatory','pycompile','whitespace','publication','semantic','frontier','contributor','site-build','official-graph','graph','site-check']; gates=[]
for name in names:
 status=load(B/('integration.0.'+name+'.status.json')); lp=pin(B/('integration.0.'+name+'.log'))
 assert status['exit_code']==0 and status['proof_commit']==SCI and status['log_raw_sha256']==lp['raw_sha256']
 assert status['started_utc']<=status['finished_utc']; gates.append(dict(name=name,status=pin(B/('integration.0.'+name+'.status.json')),actual_status=status,actual_log=lp))
tests=path(B/'integration.0.tests.log').read_text(encoding='utf-8'); mandatory=path(B/'integration.0.mandatory.log').read_text(encoding='utf-8')
assert 'Build completed successfully (9443 jobs).' in tests and 'Build completed successfully (9157 jobs).' in mandatory and 'Build completed successfully (9443 jobs).' in mandatory and 'ASTIS check passed' in mandatory
assert 'SourceMeanGradientDomain' in tests and 'Tests.Basic' in tests and 'Tests.ProximalBPSSourceMeanGradientDomain' in tests and 'sorryAx' not in tests
lease=load(B/'root.integration.0.lease.json'); assert lease['status']==lease['read']==lease['write']==lease['Python']==lease['compiler']=='CLOSED' and lease['exit_code']==0
assert lease['opened_utc']<=lease['compiler_closed_utc']<=lease['closed_utc']
aggregator=path('AutoSamplingTheory/ExampleCases.lean').read_text(encoding='utf-8'); clean=astis.strip_lean_comments_and_strings(aggregator)
assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain' in clean
assert not re.search(r'^\s*(?:theorem|lemma|def|axiom|opaque|abbrev|instance|structure|inductive)\b',clean,re.M)
assert 'import Tests.ProximalBPSSourceMeanGradientDomain' in path('Tests.lean').read_text(encoding='utf-8')
reg=path('AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf-8'); basic=path('Tests/Basic.lean').read_text(encoding='utf-8')
assert reg.count('id := "pbps.literalSourceMean.closedGradientDomain"')==1 and TARGET in reg and 'formalizedTechnicalLemmaCount = 495' in basic
sharedpaths=[e['path'] for e in notes['shared_files']]
(O/'integration.shared.actual.diff').write_bytes(subprocess.check_output(['git','diff',SCI,HEAD,'--',*sharedpaths],cwd=R))
shared_semantics=[
 'Declaration-free ExampleCases public import and real root Tests consumer added; Registry entry actual source-specific integration and Basic native_decide495 consume it.',
 'Handoff prefix attributes original C2/two-Hessian/capped-step assumptions, actual same mu/J/nu/S, uniform core BEFORE f, every-y C1, canonical same-nu pair, rank0/PUP consumers and finite-Hilbert extension. Earlier priorities and records retained.',
 'Technical registry and non-SLT audit identify reuse of four actual public parents, not a new SLT/background duplicate. Execution changes only current checkpoint; sole original PhaseKernel STABILIZING retained.',
 'Current cell evidence pointer references unchanged independent parent verified.json/receipt; learning contracts/status unchanged, purification pending. Template aggregate53 scope and historical full_shared_integration_pending are explicit observability debts.'
]
whitespace=[]
for folder,base,end,nfind,npaths in [('whitespace-diagnosis54',git('rev-parse',SCI+'^'),SCI,737,254),('integration-whitespace54',SCI,HEAD,167,3)]:
 ws=load(B/folder/'diagnosis.json'); gz=path(ws['gzip']['path']).read_bytes(); raw=gzip.decompress(gz)
 assert sha(gz)==ws['gzip']['raw_sha256'] and sha(raw)==ws['full_negative_raw_sha256'] and int.from_bytes(gz[4:8],'little')==0 and ws['full_staged_exit']==2
 count=ws['findings'] if isinstance(ws['findings'],int) else len(ws['findings']); assert count==nfind and len(ws['immutable_raw_artifacts'])==npaths
 for e in ws['immutable_raw_artifacts']: assert equal(e)
 cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',base,end]; proc=subprocess.run(cmd,cwd=R,capture_output=True)
 assert proc.returncode==2 and proc.stdout==raw
 acmd=cmd+['--','.']+[':(exclude)'+e['path'] for e in ws['immutable_raw_artifacts']]; authored=subprocess.run(acmd,cwd=R,capture_output=True)
 assert authored.returncode==0; (O/(folder+'.authored.log')).write_bytes(authored.stdout+authored.stderr)
 whitespace.append(dict(diagnosis=pin(B/folder/'diagnosis.json'),gzip=pin(ws['gzip']['path']),findings=count,exact_immutable_paths=npaths,lossless_negative_reproduced=True,gzip_mtime=0,full_staged_exit=2,authored_command=acmd,authored_exit=0,no_blanket_folder_exclusion=True,no_full_staged_PASS=True))
visual=load(B/'visual.inspection.json'); artifacts=[]
for e in visual['artifacts']:
 p=e['portable_path']; actual=pin(p); assert actual['bytes']==e['bytes'] and actual['raw_sha256']==e['raw_sha256']; artifacts.append(dict(native=e,observed_raw_LF=actual))
assert len(artifacts)==10
captures=[]
for label,n,statusn in [('companion','cdp.capture.json','desktop54.companion'),('proof','proof.capture.json','desktop54.proof')]:
 c=load(B/'visual-inspection54'/n); assert c['ownedBrowserExit']['code']==0 and c['ownedBrowserExit']['signal'] is None and len(c['records'])==2
 st=load(B/(statusn+'.status.json')); assert st['exit_code']==0 and st['log_raw_sha256']==pin(B/(statusn+'.log'))['raw_sha256']
 for r in c['records']: assert r['bodyVisibility']=='visible' and r['bodyDisplay']=='block' and r['targetRect']['width']>0 and r['targetText']
 captures.append(dict(capture=pin(B/'visual-inspection54'/n),browser_actual_PID=c['pid'],browser_exit=c['ownedBrowserExit'],node_status=pin(B/(statusn+'.status.json')),actual_node_PID=st['owned_node_pid'],exit_code=0,log=pin(B/(statusn+'.log')),lifecycle_scope=st['scope']))
for n in ['cdp.pbps.inspect.json','cdp.branch.inspect.json','proof.proof.inspect.json','proof.proof-late.inspect.json']:
 dom=load(B/'visual-inspection54'/n); assert dom['bodyVisibility']=='visible' and dom['bodyDisplay']=='block' and dom['targetText']
pbps=load(B/'visual-inspection54/cdp.pbps.inspect.json'); assert pbps['closedLeanDetails']==10 and pbps['mathContainers']==7
vl=load(B/'root.desktop-capture54.lease.json'); assert vl['status']==vl['read']==vl['write']==vl['Python']=='CLOSED' and vl['compiler']=='NOT_STARTED_CLOSED' and vl['exit_code']==0
clar=load(B/'visual-observation-clarification54.json'); assert clar['original_visual_note_raw_sha256']==pin(B/'visual.inspection.json')['raw_sha256'] and not clar['mathematical_or_source_change']
visual_findings=[
 'Independently viewed all four current PNGs with view_image: source statement and five formula steps legible, actual SAME laws/uniform core/exact folded Lean/remaining boundaries visible. Actual compact mean domain prerequisite and all-y identity explicitly differentiated from full rough B13 and separate weak H1.',
 'The late capture shows accepted domains/scopes/conclusion informational elaborations. Original-assumptions same row is qualified by finite-Hilbert/rank0 authored extension in statement and source-review section.',
 'Actual graph focus is correct exact compiled declaration; labels explicitly distinguish solid ownership/import edges and dashed incomplete source/name references. Name-scan LogConcaveOn.prod is not a certified theorem parent; WeightedC1 adapter omitted by scanner.',
 'Repeated long heading/statement, dense inline ASCII/source anchors and narrow graph qualified-name wrapping remain presentation debts. Formulas in these four desktop captures are legible; no observed54 horizontal scrollbar/occlusion claim. Root observational correction pinned separately without changing original manifests.',
 'This is bounded desktop repository inspection; separate independent ExpositionSeal/fullreader/copy/download/mobile/main/live/PURIFIED not certified.'
]
dump('integration.checks.json',dict(status='PASS_SCOPED',checked_science=SCI,checked_integration=HEAD,all12_native_gates=gates,root_jobs=9157,Tests_jobs=9443,Registry_count=495,root_actual_CLOSED_lease=pin(B/'root.integration.0.lease.json'),root_PID_not_supplied_in_native_lease=True,shared_file_pins=[pin(p) for p in sharedpaths],shared_semantic_review=shared_semantics,public_aggregator_declaration_free=True,real_root_Test_consumer=True,whitespace=whitespace,visual_artifacts=artifacts,actual_captures=captures,all_four_PNGs_independently_viewed=True,actual_DOM_math=7,initially_closed_Lean=10,desktop_actual_CLOSED_lease=pin(B/'root.desktop-capture54.lease.json'),observational_clarification=pin(B/'visual-observation-clarification54.json'),independent_visual_findings=visual_findings,new_compiler_invocations=0,remote_boundary='Historical53 cfcc CI is not54 CI. Scientific/integration54 not pushed; main/live/PURIFIED unclaimed.',future55_reads=guard_denied))
print(json.dumps(dict(status='PASS_SCOPED',actual_gates=12,root_jobs=9157,Tests_jobs=9443,Registry=495,visual_PNGs=4,DOM=4,captures=2,all_root_leases='CLOSED0',science_whitespace=[737,254],integration_whitespace=[167,3],new_compilers=0)))
