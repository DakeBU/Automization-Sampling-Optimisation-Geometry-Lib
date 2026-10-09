from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-bounce-rate74';OWN=R/'exact-science-verification74'
SCI='d556a7550f0395d149720da6478bfdfff98368a7';PARENT='e91f9b3acfeea172c33053b28d88b7fea6e61e9d'
ID='ASTIS-SA-20261010-PBPSActualBounceRate';ACTOR='/root/exact_science63';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounce-rate.json'
PUB=ROOT/'website/content/publications/pbps-actual-bounce-rate.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-bounce-rate.json';AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBounceRate.json';LEDGER=ROOT/'runs/substantive_advances.jsonl'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def path(s):
 p=Path(s);return p if p.is_absolute() else ROOT/p
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=path(row['path']);q=pin(p)
 for k,alts in [('RAW_bytes',['RAW_bytes','bytes','raw_bytes']),('RAW_sha256',['RAW_sha256','raw_sha256']),('LF_bytes',['LF_bytes','lf_bytes']),('LF_sha256',['LF_sha256','lf_sha256'])]:
  key=next((x for x in alts if x in row),None)
  if key:assert q[k]==row[key],(p,k,q[k],row[key])
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def state():
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 return astis_advance._replay_advances([json.loads(x) for x in LEDGER.read_bytes().splitlines() if x.strip()])[ID]
def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [z for k in sorted(set(a)|set(b)) for z in ([p+'/'+k] if k not in a or k not in b else differences(a[k],b[k],p+'/'+k))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def recheck():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 for row in read('inputs.manifest.json')['inputs']:check(row)
def freeze():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 assert git(['rev-list','--parents','-n','1',SCI]).decode().split()==[SCI,PARENT]
 names=['proved-local.json','claim.json','mathematics-freeze74.json','publication-plan.json','publication-freeze74.json','source-review.freeze74.json','source-review.packet.json','implementation-source-map74.json','root.math74.adoption.json','root.source74.adoption.json','root.decoder74.adoption.json','root.reader-metadata-overlay74.adoption.json',
 'audit.before-decoder74.exactraw.snapshot.json','audit.before-reader-context74.exactraw.snapshot.json','audit.before-source-admission74.exactraw.json','cell.before-source-admission74.exactraw.json','publication.before-source-admission74.exactraw.json',
 'reader-metadata-overlay74/proposal.json','reader-metadata-overlay74/0.before.exactraw.snapshot.json','reader-metadata-overlay74/0.proposed.exactraw.json','reader-metadata-overlay74/1.before.exactraw.snapshot.json','reader-metadata-overlay74/1.proposed.exactraw.json',
 'independent-math74/lease.final.json','independent-math74/native.manifest.json','independent-math74/run.json','independent-math74/fresh-compiler.json',
 'independent-source74/lease.final.json','independent-source74/whole-owned.manifest.json','independent-source74/source.0.run.json','independent-source74/source.0.decision.json','independent-source74/source.0.input-manifest.json','independent-source74/source.0.admission-fields.json',
 'anonymous-decoder/CLOSED_LAST.json','anonymous-decoder/run.json','independent-reader-metadata-repair74/lease.final.json','independent-reader-metadata-repair74/run.json','independent-reader-metadata-repair74/decision.json',
 'whitespace-diagnosis74/diagnosis.json','science-commit/receipt.json']
 paths=[MODULE,CELL,PUB,LESSON,AUDIT,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']+[R/n for n in names]
 paths += [ROOT/'tools'/n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_frontier_cells.py']]
 rows=[pin(p) for p in paths];assert len({x['path'] for x in rows})==len(rows)
 core=[]
 for p in paths:
  name=p.relative_to(ROOT).as_posix()
  if name==str((R/'science-commit/receipt.json').relative_to(ROOT)).replace('\\','/'):
   core.append(dict(file=pin(p),classification='POSTCOMMIT_EXTERNAL_EXECUTION_RECEIPT; causally excluded from its own SCI commit'));continue
  b=git(['show',SCI+':'+name]);raw=p.read_bytes();equal=b==raw
  assert equal or b.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n'),name
  core.append(dict(file=pin(p),Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),current_Git_RAW_equal=equal,CRLF_only_LF_qualification=not equal))
 write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='Finite RAW/LF locators; no recursive historical copies or full ledger.'))
 write('Git-inputs.json',dict(actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,files=core))
 write('lease.open.json',dict(status='OPEN_EXACT_SCI74',actual_PID=os.getpid(),actor=ACTOR,checked_commit=SCI,parent=PARENT))
 b=LEDGER.read_bytes();s=state();assert s['state']=='PROVED_LOCAL' and s['owner_id']=='companion_root_20261005' and s['publication_declarations']==[DECL]
 assert not (R/'verified.json').exists()
 write('ledger.before-prefix.json',dict(path=LEDGER.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),target_state=s,storage='Full prefix bytes remain in append-only canonical ledger; pin exact byte length and hash, no duplicate whole-history copy.'))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),checked_commit=SCI)),flush=True)
def process(label,argv,accepted=(0,)):
 f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');pre=pin(MODULE);start=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 receipt=dict(label=label,actual_PID=p.pid,command=argv,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',receipt)
 assert pre==receipt['module_post'] and code in accepted,(label,code);return receipt
def gates():
 recheck();checks=[('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',PARENT]),('contributor',['tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',['tools/astis_semantic_roundtrip.py','check']),('packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-bounce-rate'])]
 rows=[process(label,[PY,'-B','-X','utf8',*args]) for label,args in checks]
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_publication;astis_publication.check_advance([DECL],reviewed=True)
 write('gates.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,diff_base=PARENT,receipts=rows,reviewed_source_gate=dict(function='astis_publication.check_advance',publication_declarations=[DECL],reviewed=True,status='PASS'),full_root_site_or_aggregate=False))
 print(json.dumps(dict(status='REQUIRED_CURRENT_GATES_PASS',actual_PID=os.getpid(),gates=len(rows))))
def native_binding():
 recheck();packages=[]
 for folder,adopter,runname,count in [('independent-math74','root.math74.adoption.json','run.json',45),('independent-source74','root.source74.adoption.json','source.0.run.json',64),('independent-reader-metadata-repair74','root.reader-metadata-overlay74.adoption.json','run.json',25)]:
  base=R/folder;a=load(R/adopter);lease=load(base/'lease.final.json');check(a['native_lease']);assert lease['status']=='CLOSED_LAST'
  if folder=='independent-math74':
   check(lease['manifest']);manifest=load(path(lease['manifest']['path']));rows=manifest['entries'];assert len(rows)==manifest['entry_count'];assert sha(canon(rows))==manifest['logical_entries_sha256']
  else:rows=lease.get('all_files_except_self',lease.get('all_owned_outputs_except_only_self'))
  for row in rows:check(row)
  assert len(list(p for p in base.rglob('*') if p.is_file()))==count
  run=load(base/runname);h=run.pop('run_sha256');assert sha(canon(run))==h==a['native_whole_logical_run_sha256']
  named=a.get('native_complete_named',a.get('native_complete_named_RAW'));check(named)
  packages.append(dict(package=folder,owned_files=count,all_manifest_rows_checked=len(rows),lease=pin(base/'lease.final.json'),run=pin(base/runname),whole_logical_run_sha256=h,complete_named_RAW=check(named)))
 math=load(R/'independent-math74/run.json')
 for row in math['input_manifest']['inputs']:check(row['original']);check(row['snapshot'])
 for row in load(R/'mathematics-freeze74.json')['inputs']:check(row)
 fresh=load(R/'independent-math74/fresh-compiler.json')
 assert fresh['fresh_source_elaboration'] and not fresh['Lake_build_cache_replay'] and fresh['terminal_EXIT']==0 and fresh['actual_foreground_Lean_PID']==19204 and fresh['axiom_audit_PID']==52720
 for key in ['compiler_receipt','output_olean','real_Lean_executable','version_output','axiom_audit_receipt','axiom_audit_driver']:check(fresh[key])
 axrec=load(path(fresh['axiom_audit_receipt']['path']));comp=load(path(fresh['compiler_receipt']['path']))
 assert axrec['exit_code']==comp['exit_code']==0
 for rec in [axrec,comp]:
  check(rec['stdout']);check(rec['stderr'])
 b=MODULE.read_bytes();assert sha(b)=='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c' and len(b)==10565 and len(b.splitlines())==211
 assert path(fresh['axiom_audit_driver']['path']).read_bytes()==b+fresh['axiom_driver_only_suffix'].encode()
 axout=path(axrec['stdout']['path']).read_text(encoding='utf-8');found=re.search(r'depends on axioms:\s*\[([^\]]+)\]',axout,re.S);assert found
 standard=[x.strip() for x in found.group(1).split(',')];assert standard==['propext','Classical.choice','Quot.sound']==fresh['standard_axioms']
 blind=load(R/'anonymous-decoder/CLOSED_LAST.json');da=load(R/'root.decoder74.adoption.json');check(da['native_lease']);check(da['native_complete_payload']);assert blind['status']=='CLOSED_LAST'
 for row in blind['prior_owned_files']:
  check(row);arch=R/'anonymous-decoder'/Path(row['path']).name;assert arch.read_bytes()==path(row['path']).read_bytes()
 check(blind['sole_input_receipt']);dr=load(R/'anonymous-decoder/run.json');assert sha(canon(dr['logical_run_payload']))==sha(dr['canonical_logical_run_utf8'].encode())==dr['decoder_run_sha256']==da['native_whole_logical_run_sha256']
 assert len(dr['canonical_logical_run_utf8'].encode())==dr['canonical_preimage_bytes'] and not any(dr[k] for k in ['proof_visible','source_identity_visible','source_text_visible'])
 assert len(list((R/'anonymous-decoder').iterdir()))==4
 packages.append(dict(package='strict-blind-decoder74',owned_files=4,archive_4_RAW_equal_original=True,lease=pin(R/'anonymous-decoder/CLOSED_LAST.json'),logical_run_sha256=dr['decoder_run_sha256'],native_recipe=dr['canonical_recipe'],not_reinterpreted_as_new_top_level_run_recipe=True))
 # Three exact post-review admission maps, with no arbitrary snapshot fallback.
 source=R/'independent-source74';si=load(source/'source.0.input-manifest.json');admit=load(source/'source.0.admission-fields.json');audit=load(AUDIT);before_a=load(R/'audit.before-source-admission74.exactraw.json')
 expected=dict(before_a);expected.update(admit['audit_fields']);assert expected==audit
 cell=load(CELL);pub=load(PUB);before_c=load(R/'cell.before-source-admission74.exactraw.json');before_p=load(R/'publication.before-source-admission74.exactraw.json')
 assert cell['source_proof_coverage']==admit['cell_source_proof_coverage'];assert pub['items'][0]['source_proof_coverage']==admit['publication_source_proof_coverage']
 cell_allowed=['/conceptual_mirror_audit/checked','/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/source_proof_coverage/coverage_report/LF_bytes','/source_proof_coverage/coverage_report/LF_sha256','/source_proof_coverage/coverage_report/RAW_bytes','/source_proof_coverage/coverage_report/RAW_sha256','/source_proof_coverage/coverage_report/path','/source_proof_coverage/coverage_status','/source_proof_coverage/source_inventory','/status']
 pub_allowed=['/items/0/source_proof_coverage/coverage_report/LF_bytes','/items/0/source_proof_coverage/coverage_report/LF_sha256','/items/0/source_proof_coverage/coverage_report/RAW_bytes','/items/0/source_proof_coverage/coverage_report/RAW_sha256','/items/0/source_proof_coverage/coverage_report/path','/items/0/source_proof_coverage/coverage_status','/items/0/source_proof_coverage/source_inventory']
 assert differences(before_c,cell)==cell_allowed and differences(before_p,pub)==pub_allowed
 assert cell['status']=='proved_locally' and cell['conceptual_mirror_audit']['checked'] and cell['evidence']['proof_review'] and cell['evidence']['source_review']
 maps={AUDIT.relative_to(ROOT).as_posix():R/'audit.before-source-admission74.exactraw.json',CELL.relative_to(ROOT).as_posix():R/'cell.before-source-admission74.exactraw.json',PUB.relative_to(ROOT).as_posix():R/'publication.before-source-admission74.exactraw.json'}
 source_maps=[]
 for row in si['final_current_inputs']:
  snap=source/row['RAW_snapshot'];assert sha(snap.read_bytes())==row['RAW_sha256']
  if row['path'] in maps:
   hist=maps[row['path']];assert hist.read_bytes()==snap.read_bytes();source_maps.append(dict(path=row['path'],resolution='EXACT_SOURCE_ADMISSION_AND_PROVED_LOCAL_FIELDS_ONLY',historical=pin(hist),current=pin(path(row['path'])),changed_pointers=differences(load(hist),load(path(row['path'])))))
  else:check(row);source_maps.append(dict(path=row['path'],resolution='CURRENT_EXACT',RAW_sha256=row['RAW_sha256']))
 for group in ['immutable_source_contract_inputs','protocol_and_freeze_inputs','repair_authority_inputs']:
  for row in si[group]:check(row)
 # Preserve the explicit draft->blind state map and the independently approved two-string overlay.
 draft=load(R/'audit.before-decoder74.exactraw.snapshot.json');blind_a=load(R/'audit.before-reader-context74.exactraw.snapshot.json');assert differences(draft,blind_a)==['/reconstruction','/state'];assert blind_a==before_a
 repair=load(R/'independent-reader-metadata-repair74/decision.json');assert repair['accepted'] and len(repair['approved_rows'])==2
 repair_maps=[]
 for row in repair['approved_rows']:
  check(row['before']);check(row['proposed']);assert differences(load(path(row['before']['path'])),load(path(row['proposed']['path'])))==[row['json_pointer']]
  before_admission=maps[row['path']];assert path(row['proposed']['path']).read_bytes()==before_admission.read_bytes()
  repair_maps.append(dict(path=row['path'],json_pointer=row['json_pointer'],before=check(row['before']),approved=check(row['proposed']),source_admission_before=pin(before_admission),current=pin(path(row['path']))))
 packet=load(R/'source-review.packet.json');review=load(source/'source.0.review.json');decision=load(source/'source.0.decision.json');sr=load(source/'source.0.run.json')
 assert decision['verdict']=='equivalent-after-elaboration' and decision['blocking_semantic_deltas']==0 and decision['mathematical_repairs']==[] and decision['repairs']==[]
 slots=['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'];assert set(decision['semantic_slots'])==set(slots)
 assert audit['semantic_slots']==decision['semantic_slots'] and audit['deltas']==decision['deltas'] and len(audit['deltas'])==13 and all(x['severity']=='informational' for x in audit['deltas'])
 assert audit['source_review']['review_run_sha256']==sr['run_sha256'] and audit['source_review']['state']=='accepted'
 assert audit['source_review']['independent_from_formalizer'] and audit['source_review']['independent_from_decoder'] and audit['source_review']['reviewer']!=ACTOR
 assert packet['packet_sha256']==decision['reviewer_packet_sha256']==audit['source_review']['reviewer_packet_sha256']==sr['official_packet_sha256']
 assert audit['publication_binding_sha256']==packet['publication_binding_sha256']==decision['publication_binding_sha256']==sr['publication_binding_sha256']=='599d4550f863962f6ef74dd0821ef433ebe7c8f5ead8d907d8a5f409fb0feeca'
 assert audit['publication_context']==packet['candidate_publication_context']
 # Full literal, same six public callers, ten groups and seven literal BODY spans.
 text=b.decode();private=text[text.index('private def actual_bounce_rate_energy_statement'):text.index('theorem actual_bounce_rate_energy_laws')]
 args,body=private.split(' : Prop :=',1)
 expanded='theorem actual_bounce_rate_energy_laws'+packet['lean']['statement']+'\n'
 assert expanded.encode()==(R/'expanded74.frozen.header.lean').read_bytes()
 reconstructed=args.replace('private def actual_bounce_rate_energy_statement','theorem actual_bounce_rate_energy_laws',1)+' :'+body
 assert reconstructed.split()==expanded.split()
 public=text[text.index('theorem actual_bounce_rate_energy_laws'):text.index(':= by',text.index('theorem actual_bounce_rate_energy_laws'))]
 publicargs=public[:public.index(' :\n    actual_bounce_rate_energy_statement')]
 assert publicargs.split()==args.replace('private def actual_bounce_rate_energy_statement','theorem actual_bounce_rate_energy_laws',1).split()
 assert 'actual_bounce_rate_energy_statement hα hαβ hV hH hη hβη' in public
 unit=load(LESSON)['units'][0];assert unit['declaration']==DECL and len(unit['steps'])==7
 body_start=text.index(':= by',text.index('theorem actual_bounce_rate_energy_laws'));line_body=text[:body_start].count('\n')+1;steps=[];lines=b.splitlines(keepends=True)
 for i,step in enumerate(unit['steps']):
  reg=step['lean_source_region'];assert reg['path']==MODULE.relative_to(ROOT).as_posix() and reg['source_raw_sha256']==sha(b) and reg['start_line']>line_body
  region=b''.join(lines[reg['start_line']-1:reg['end_line']]);assert region==step['lean'].encode() and sha(region)==reg['exact_code_raw_sha256']
  steps.append(dict(index=i+1,formula=step['formula'],region=reg,literal_BODY_match=True,RAW_span_bytes=len(region)))
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=s.strip()) for i,s in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(s)];assert not hits
 inventory=re.findall(r'^(private )?(def|theorem|lemma|axiom|opaque)\s+([^\s:]+)',stripped,re.M);assert inventory==[('private ','def','actual_bounce_rate_energy_statement'),('','theorem','actual_bounce_rate_energy_laws')]
 for field in [cell['shared_floor_audit']['searched'],cell['reuse_plan']['searched_existing']]:assert field[0].startswith('Samplinglib ') and field[1].startswith('Mathlib ')
 bodyaudit=load(R/'independent-math74/whole-body-mathematical-audit.json');assert bodyaudit['module_lines']==211 and not bodyaudit['mathematical_repair']
 write('source-math-binding-fakeclosure.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,packages=packages,math_input_count=13,source_current_finite_maps=source_maps,source_other_exact_inputs={k:len(si[k]) for k in ['immutable_source_contract_inputs','protocol_and_freeze_inputs','repair_authority_inputs']},
  draft_to_blind_map=dict(before=pin(R/'audit.before-decoder74.exactraw.snapshot.json'),after=pin(R/'audit.before-reader-context74.exactraw.snapshot.json'),changed_pointers=['/reconstruction','/state'],reader_context_refresh_no_change=True),approved_two_string_metadata_maps=repair_maps,
  actual_module=pin(MODULE),module_lines=211,source_callers=6,conclusion_groups=10,original_callers='hα hαβ hV hH hη hβη',private_literal_Prop_definitions=1,private_providers=0,full_private_literal_expansion_matches_sealed_header=True,
  native_source_slots=7,informational_deltas=13,blocking_deltas=0,mathematical_repairs=0,source_run_sha256=sr['run_sha256'],source_native_decision=pin(source/'source.0.decision.json'),publication_binding_sha256=audit['publication_binding_sha256'],reviewer_packet_sha256=packet['packet_sha256'],exact_BODY_steps=steps,
  declaration_inventory=inventory,fake_closure_hits=hits,retrieval_labels='Samplinglib and Mathlib prefixes on both recorded search fields',fresh_Lean_reused=fresh,axioms=standard,new_Lean_compilation=False,
  mathematical_boundary='Original finite real Hilbert/Borel C2 and two Hessians; strict positive alpha/order and betaeta<=1 retained even where BODY does not need them; eta>0. Zero normal, zero energy, rank0 and alphaeta=1 legal. Actual S only Borel, actual rate continuous. Same weighted SUM H layer cap, no random paths/nonexplosion/invariance/composition credit.'))
 print(json.dumps(dict(status='NATIVE_SOURCE_MATH_BINDING_SCAN_PASS',actual_PID=os.getpid(),packages=4,native_files=138,source_current_maps=8,exact_BODY_steps=7,reused_direct_Lean_PID=19204,axioms_PID=52720)))
def whitespace():
 recheck();rec=process('full-RAW-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI],accepted=(0,1,2))
 raw=path(rec['stdout']['path']).read_bytes();findings=[dict(path=m.group(1),line=int(m.group(2)),kind=m.group(3)) for m in re.finditer(r'^(.+):(\d+): (trailing whitespace|new blank line at EOF)\.',raw.decode(),re.M)]
 diag=load(R/'whitespace-diagnosis74/diagnosis.json');assert findings==diag['findings'] and len(findings)==20 and rec['exit_code']!=0 and not diag['full_staged_whitespace_PASS']
 rows=[]
 for row in diag['immutable_raw_paths']:
  check(row);p=path(row['path']);assert git(['show',SCI+':'+row['path']])==p.read_bytes();rows.append(dict(file=pin(p),Git_RAW_equal=True,classification='Immutable exact source or original successful/failed compiler stdout; retain every RAW byte.'))
 names=sorted({x['path'] for x in findings});authored=process('authored-complement-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI,'--','.',*[':(exclude)'+n for n in names]])
 write('whitespace.json',dict(status='AUTHORED_PASS_RAW_NEGATIVE_RETAINED',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,policy='core.whitespace=cr-at-eol',full_RAW_PASS=False,immutable_findings=20,exact_findings=findings,finite_exception_files=rows,RAW_terminal=rec,authored_complement_PASS=True,authored_terminal=authored,no_native_normalization=True))
 print(json.dumps(dict(status='WHITESPACE_QUALIFIED',actual_PID=os.getpid(),immutable_findings=20,full_RAW_PASS=False,authored_PASS=True)))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except BaseException as e:
  if not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),mode=sys.argv[1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation_by_this_observer=False))
  raise
