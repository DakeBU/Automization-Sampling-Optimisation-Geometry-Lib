from common_v2 import *
import tarfile
pre=json.loads((OUT/'pre-invariants.json').read_bytes());assert pre['own_state']=='PROVED_LOCAL'
N=E/'native-review/ri_native_74b8'
report=json.loads((N/'report.json').read_bytes());manifest=json.loads((N/'portable-manifest.json').read_bytes());binding=json.loads((N/'relevant-input-binding.json').read_bytes())
assert sha((N/'report.json').read_bytes())=='75f6730c5d105217b3ab0d4b6c73c079fcef9b4592b2cf3d8d01ec123cc46419'
assert report['verdict']=='ACCEPT_BOUNDED_NATIVE_WHOLE_MODULE_STATIC' and report['compile_candidate_only']==CANDIDATE
assert report['source_fidelity_grant'] is False and report['ledger_transition_or_permission_grant'] is False
assert manifest['compile_candidate']==CANDIDATE and len(manifest['members'])==manifest['member_count_excluding_this_manifest']==460
assert len(manifest['receipts'])==manifest['receipt_count']==106
assert sha((N/'relevant-input-binding.json').read_bytes())==report['final_binding']['sha256']
for x in binding['tracked_relevant_input_hashes']:
 b=(ROOT/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
assert len(binding['tracked_relevant_input_hashes'])==45
binary=pathlib.Path(binding['native_binary']['path']);assert sha(binary.read_bytes())==binding['native_binary']['sha256']
assert sha((ROOT/binding['source_raw']['path']).read_bytes())==binding['source_raw']['sha256']
probe=binding['private_author_probe'];assert sha((ROOT/probe['origin']).read_bytes())==probe['sha256']
pkgmanifest=json.loads((ROOT/'lake-manifest.json').read_bytes());pkgs=[]
for p in pkgmanifest['packages']:
 d=ROOT/'.lake/packages'/p['name']
 head=subprocess.run(['git','rev-parse','HEAD'],cwd=d,check=True,capture_output=True).stdout.decode().strip()
 clean=subprocess.run(['git','status','--porcelain','--untracked-files=all'],cwd=d,check=True,capture_output=True).stdout
 assert head==p['rev'] and not clean,p['name']
 pkgs.append({'name':p['name'],'rev':head,'clean_including_untracked':True})
assert len(pkgs)==9
decisive=['receipts/build-driver.json','receipts/exact-author-probe.json','receipts/independent-literals.json','receipts/native-inspection-driver.json','receipts/native-lean-file.json','receipts/standard-applicability.json','receipts/reader-static-v2-driver.json','receipts/static-extra-driver.json']
nonzero=[];streamcount=0
with tarfile.open(N/'portable-evidence.tar.gz') as t:
 members=t.getmembers();assert len(members)==461 and all(m.isfile() for m in members)
 by={m.name:m for m in members};assert len(by)==461
 for x in manifest['members']:
  b=t.extractfile(by[x['path']]).read();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
 assert t.extractfile('portable-manifest.json').read()==(N/'portable-manifest.json').read_bytes()
 for x in manifest['receipts']:
  r=json.loads(t.extractfile(x['path']).read());assert r['exit_code']==x['exit_code']
  for k in ['stdout','stderr']:
   stream=r[k];b=t.extractfile(stream['path']).read();assert len(b)==stream['bytes'] and sha(b)==stream['sha256'];streamcount+=1
  if r['exit_code']!=0:nonzero.append({'path':x['path'],'exit_code':r['exit_code']})
 for name in decisive:assert json.loads(t.extractfile(name).read())['exit_code']==0,name
 summary=json.loads(t.extractfile('native-summary.json').read());build=json.loads(t.extractfile('native-build.json').read());fake=json.loads(t.extractfile('fake-closure-scan.json').read());static=json.loads(t.extractfile('reader-static.json').read())
 assert summary['candidate_commit']==CANDIDATE and summary['closure_module_count']==3 and summary['module_owned_total']==3
 assert summary['new_handwritten']==2 and summary['new_generated']==0
 for k in ['all_owned_reachable_from_new_roots','all_types_bodies_closed','independent_literal_kernel_applied_both','exact_author_probe_pass','probability_sigmafinite_and_physical_coordinate_map_specializations_pass']:assert summary[k] is True,k
 assert summary['only_standard_axioms']==['propext','Classical.choice','Quot.sound']
 dump_path=ROOT/'.astis/semantic-neutral-20261112/ri_native_74b8'/summary['large_full_dump']['path'];dumpb=dump_path.read_bytes();assert len(dumpb)==summary['large_full_dump']['bytes'] and sha(dumpb)==summary['large_full_dump']['sha256']
 dump=json.loads(dumpb);assert len(dump)==3
 for x in summary['declarations']:
  actual=next(d for d in dump if d['name']==x['name'])
  assert actual['type_closed'] and actual['body_closed']
  assert sha(actual['type'].encode())==x['type_sha256'] and sha(actual['body'].encode())==x['body_sha256']
  assert actual['axioms']==x['axioms'] and set(actual['axioms'])<={'propext','Classical.choice','Quot.sound'}
 assert fake['zero_hits'] and len(fake['files'])==3
 for x in fake['files']:assert not x['hits'] and sha((ROOT/x['path']).read_bytes())==x['sha256']
 assert len(build['outputs'])==3
 for x in build['outputs']:
  b=t.extractfile(x['olean']).read();assert sha(b)==x['sha256']
 assert len(static['six_steps'])==6 and all(x['exact_adjacent_formula_and_Lean'] and x['initially_closed'] for x in static['six_steps'])
 assert static['private_export_exact_81_lines'] and static['original_separator_blank_line']==60 and static['private_source_link_line']==11
assert streamcount==212 and nonzero==[{'path':'receipts/reader-static-driver.json','exit_code':1}]
gate_expected={
 'contributor':('20261112T121836654947Z-source-row-independence-final-contributor.receipt.json','bddb3e6af52303acfffa2ad90dcb3bc0f631c1a8354ddc86a1736c60d4d2ca76'),
 'frontier':('20261112T121836654948Z-source-row-independence-final-frontier.receipt.json','3939bbfef0fd99efe94a8d566cf7382fa3fb4d6dbe684e4078e1b4882fa88d8b'),
 'semantic':('20261112T121836654948Z-source-row-independence-final-semantic.receipt.json','72248f266f8d0e1e2a1086794b665ee356868e3f30875b9edc1f874e77c970b8'),
 'publication':('20261112T121836654952Z-source-row-independence-final-reviewed-publication.receipt.json','5b51cb92da68bf118c75413b03c916ae25d14f09c0aa55d21e69998707612707')}
gates=[]
for name,(file,expectedlog) in gate_expected.items():
 p=ROOT/'.astis/huanjian-resume-20261103'/file;r=json.loads(p.read_bytes());log=pathlib.Path(r['log']);b=log.read_bytes()
 assert r['exit_code']==0 and r['head_before']==HEAD and r['head_after']==HEAD
 assert r['log_sha256']==expectedlog==sha(b)
 if name in {'publication','contributor'}:assert r['command'][-2:]==['--base','6ef180f7495ef79e1f70bac7909036fc6f7f73bc']
 gates.append({'gate':name,'receipt':info(p),'log':info(log),'exit_code':0})
audit_path=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-independence.json';audit=json.loads(audit_path.read_bytes())
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
assert audit['source_review']['reviewer']==WORKER and audit['source_review']['review_run_sha256']=='51dab1d9f097c628772a2a28d6afd6422dfc1ad278f4b3474db7b8f392d9d58b'
assert audit['publication_binding_sha256']=='d90576df8ae217ca7cb9ce631cdca049780f3a706510afbe2f72a71dd1c03829'
assert audit['verdict']=='equivalent-after-elaboration' and not audit['deltas'] and not audit['repairs']
remote_states=advance._replay_advances(records(git('show',ORIGIN_MAIN+':'+LEDGER)))
remote_summary=[{'advance_id':k,'state':v.get('state'),'owner_id':v.get('owner_id'),'integration_owner':v.get('latest_evidence',{}).get('integration_owner')} for k,v in remote_states.items() if 'SlcLsiWeightedRadialMGF' in k or ('StatOT' in k and v.get('state') not in {'MERGED','QUARANTINED'})]
assert any('SlcLsiWeightedRadialMGF' in x['advance_id'] and x['state']=='STABILIZING' for x in remote_summary)
write(OUT/'acceptance-checks.json',{'accepted':True,'held_HEAD':HEAD,'native_compile_credit_only':CANDIDATE,'native_originals':[info(N/n) for n in ['report.json','portable-manifest.json','portable-evidence.tar.gz','relevant-input-binding.json','metadata-carrier-byte-comparison.json']],'native_460_file_hashes_rechecked':True,'tar_members':461,'receipt_count':106,'receipt_streams_rehashed':streamcount,'retained_native_nonzero_receipts':nonzero,'decisive_native_receipts_all_exit0':decisive,'all_3_native_owned_type_body_dump_pairs_rehashed':True,'full_native_dump_hash_only_not_exported':{'bytes':len(dumpb),'sha256':sha(dumpb)},'native_fresh_modules':3,'owned_roots':3,'new_handwritten':2,'new_generated':0,'all_45_relevant_current_inputs_match':True,'packages_rechecked':pkgs,'source_audit':info(audit_path),'four_final_gates':gates,'origin_main_ownership_summary_only':remote_summary,'scope':'Canonical actual-row full independence plus actual private local-cutoff matrix measurability and full independence. No new ambient/main-bound/browser/global delivery/integration/purification credit.','precheck_v1_failure':'IMPLEMENTATION_FAILED ref-label assertion; retained, versioned v2 passes; no API call occurred during it.'})
print(json.dumps({'accepted':True,'native_manifest_files':460,'tar_members':461,'native_receipts':106,'streams':streamcount,'decisive_native_and_four_final_gates_exit0':True,'all_45_relevant_inputs_equal':True,'packages':len(pkgs),'native_credit_only':CANDIDATE},indent=2))
