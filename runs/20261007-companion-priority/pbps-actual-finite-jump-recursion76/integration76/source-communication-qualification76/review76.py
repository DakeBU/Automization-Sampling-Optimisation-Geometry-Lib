from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76';S=ROOT/'runs/20261007-companion-priority/pbps-recursive-preproof76/fresh-compiled-source76';OWN=R/'integration76/source-communication-qualification76'
ACTOR='/root/exact_science63';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';SCI='e1f1d85d34426954829a97a46b563ea8e1dab8f1'
NOTICE='根只读采纳独立数学已完成，源码候选及15inputs保持冻结。关于 neutral binder 的 header_RAW_range：请在原生审查里明确保留坐标过期的非数学 metadata 问题，以你从当前 frozen expanded header/完整模块独立重定位的坐标作为证据；若你认为必须修复，返回单独精确 metadata overlay 供独立审查，不要重写 frozen输入。不要读取或引用其他审查 verdict。最终两份coverage projection 应基于你 source-only 冻结的独立 source graph，保留未覆盖 whole-paper 边界。'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def write(n,x):
 p=OWN/n;p.write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def check(row):
 q=pin(ROOT/row['path']);assert q==row;return q

def review():
 print(json.dumps(dict(status='REVIEW_STARTED',actual_PID=os.getpid())),flush=True)
 write('lease.open.json',dict(status='OPEN_PROVENANCE_QUALIFICATION_ONLY',actor=ACTOR,actual_PID=os.getpid(),new_math_or_source_verdict=False,new_VERIFIED=False))
 (OWN/'communication-notice.exactraw.txt').write_bytes(NOTICE.encode())
 paths=[ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md',S/'source-only.freeze76.json',S/'source-proof-graph76.json',S/'source-coverage76.json',S/'candidate-intake76.json',S/'candidate-dispatch.freeze76.raw.json',S/'review-logical-run76.raw.json',S/'compiled-source-review76.json',S/'candidate-checks76.json',S/'CLOSED_LAST.json',R/'source-review.clean.packet.json',R/'expanded76.frozen.header.lean',R/'neutral-expanded-binders76.json',R/'root.math76.adoption.json',R/'root.source76.adoption.json',R/'exact-science-verification76/lease.final.json',R/'exact-science-verification76/run.json',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean']
 rows=[pin(p) for p in paths];write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='Bounded exact references to immutable source-only/candidate/native authorities; no recursive payload copies or chat/session-store access.',communication_notice=pin(OWN/'communication-notice.exactraw.txt'),communication_source='Exact text disclosed by root in this task; not independently exported from private chat storage. No notice timestamp invented.'))
 first=load(S/'source-only.freeze76.json');intake=load(S/'candidate-intake76.json');dispatch=load(S/'candidate-dispatch.freeze76.raw.json');native=load(S/'review-logical-run76.raw.json');report=load(S/'compiled-source-review76.json');lease=load(S/'CLOSED_LAST.json');packet=load(R/'source-review.clean.packet.json')
 assert first['created_utc']<intake['utc'] and first['anti_anchoring']['source_first_extraction'] and all(v is False for k,v in first['anti_anchoring'].items() if k!='source_first_extraction')
 assert intake['source_only_freeze_sha256']==native['source_first_freeze_sha256']==sha((S/'source-only.freeze76.json').read_bytes())
 assert lease['state']=='CLOSED_LAST' and lease['review_run_sha256']==report['review_run_sha256']==sha((S/'review-logical-run76.raw.json').read_bytes())
 assert native['prior_verdicts_or_other_reviewer_outcomes_seen'] is False and dispatch['no_prior_source_or_math_verdicts_supplied'] is True
 assert len(dispatch['inputs'])==dispatch['input_count']==len(intake['readable_inputs'])==15
 assert packet['anti_anchoring']==dict(prior_semantic_slots_included=False,prior_deltas_included=False,prior_verdict_included=False,prior_repairs_included=False)
 assert packet['packet_sha256']==native['packet_sha256']==report['packet_sha256'] and packet['publication_binding_sha256']==native['publication_binding_sha256']
 assert not {'semantic_slots','deltas','verdict','repairs','source_review'}&set(packet)
 permitted=[]
 for row in native['readable_input_manifest']:
  b=(S/row['own_raw_copy']).read_bytes();assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256'];permitted.append(dict(original_locator=row['path'],frozen_native_snapshot=pin(S/row['own_raw_copy'])))
 assert len(permitted)==15 and not any('adoption' in x['original_locator'] or 'independent-math76' in x['original_locator'] or 'source.0.decision' in x['original_locator'] for x in permitted)
 checks=load(S/'candidate-checks76.json');neutral=load(R/'neutral-expanded-binders76.json');header=(R/'expanded76.frozen.header.lean').read_bytes();index={q['id']:q for k in ['callers','literal_definitions','conclusion_groups'] for q in neutral[k]};coordinate=[]
 for row in checks['neutral_binder_fresh_coordinates']:
  item=index[row['id']];literal=item.get('header_literal',item.get('literal')).encode();a,z=row['current_expanded_header_RAW_range'];old_a,old_z=row['provided_neutral_header_RAW_range'];assert header[a:z]==literal and header[old_a:old_z]!=literal and row['provided_neutral_header_RAW_range']==item['header_RAW_range'];coordinate.append(dict(id=row['id'],group=row['group'],current_RAW_range=[a,z],literal_RAW_sha256=sha(literal),independently_rechecked=True,old_stale=True))
 assert len(coordinate)==checks['neutral_stale_coordinate_count']==27
 text=(ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md').read_text(encoding='utf-8');rule='The packet contains source and reconstruction but omits all earlier semantic slots, deltas, verdicts, and repairs.';assert rule in text
 evidence=dict(status='CHECKED_BOUNDED_RECORD',actual_PID=os.getpid(),source_only_freeze_utc=first['created_utc'],candidate_intake_utc=intake['utc'],source_first_before_candidate_native_evidence=True,source_first_before_notice='Root disclosed the notice as candidate-stage; no independent chat timestamp available.',skill_rule=rule,skill_one_based_line=next(i+1 for i,x in enumerate(text.splitlines()) if rule in x),skill=pin(ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md'),native_retained_broad_flag=dict(path=pin(S/'review-logical-run76.raw.json'),field='prior_verdicts_or_other_reviewer_outcomes_seen',value=False),dispatch_retained_broad_flag=dict(path=pin(S/'candidate-dispatch.freeze76.raw.json'),field='no_prior_source_or_math_verdicts_supplied',value=True),native_source_lease=pin(S/'CLOSED_LAST.json'),whitelisted15_frozen_inputs=permitted,packet_anti_anchoring=packet['anti_anchoring'],excluded_inputs=dispatch['excluded_inputs'],independently_rechecked_coordinate_rows=coordinate,earlier_semantic_payload_check='The disclosed message contains no earlier seven-slot contents, semantic deltas, fidelity verdict or repair payload. The 15-file candidate whitelist excludes old review outcomes. This is not an exhaustive audit of undisclosed communications.')
 write('evidence.json',evidence)
 qualification=dict(schema='source-communication-qualification76/addendum-v1',status='APPEND_ONLY_PROPOSED_QUALIFICATION_NO_NATIVE_REWRITE',actor=ACTOR,source_native_run=pin(S/'review-logical-run76.raw.json'),source_native_lease=pin(S/'CLOSED_LAST.json'),exact_disclosed_notice=pin(OWN/'communication-notice.exactraw.txt'),mathematics_status_notice_received=True,earlier_mathematical_review_payload_received=False,earlier_semantic_source_verdict_payload_received=False,coordinate_metadata_notice_received=True,coordinate_notice_scope='Root identified stale auxiliary byte coordinates and called them nonmathematical metadata; this candidate-specific cue is disclosed, not erased. It supplied neither replacement byte coordinates nor a source theorem equivalence conclusion. The reviewer independently recomputed all27 literals/ranges, rechecked here.',native_broad_false_flag_retained=True,native_broad_false_flag_accurate_as_universal_no_outcomes_claim=False,interpretation='Do not interpret native false as never having learned any review status. It omits this status-only communication. Read the native record only together with this append-only qualification; do not retroactively rewrite its meaning or bytes.',whitelist_scope='No old source/semantic/math review payload was a readable candidate input. A status notice is nevertheless communication exposure and is recorded separately.',required_adoption_condition='Any future provenance claim must link this exact qualification and preserve the original native flag/RAW. No unconditional all-outcomes-hidden claim is authorized.',new_semantic_verdict=False,new_VERIFIED=False)
 write('qualification.addendum.proposed.json',qualification)
 decision=dict(schema='source-communication-qualification76/decision-v1',status='ACCEPTED_QUALIFIED_SOURCE_COMMUNICATION_PROVENANCE',actor=ACTOR,actual_PID=os.getpid(),accepted=True,source_fidelity_admission_invalidated_by_disclosed_notice=False,fresh_source_review_required=False,append_only_qualification_required=True,mathematics_status_notice_received=True,earlier_semantic_source_verdict_payload_received=False,coordinate_metadata_notice_received=True,native_false_flag_overbroad=True,native_bytes_must_remain_unchanged=True,reason='The rule hides earlier source/semantic slots, deltas, fidelity verdicts and repairs, rather than every status communication. Source-only expectations/topology were frozen before candidate access. The disclosed message reveals mathematics acceptance status and a coordinate-metadata cue, but no old source-fidelity payload or mathematical proof content. Independent source comparison remains supported by the fixed source-first graph, exact15-file whitelist and independently recomputed current coordinates; compiler acceptance is not used as source fidelity evidence. The broad native no-outcomes flag is not accurate for the full known communication record and requires the linked additive qualification.',bias_limit='Learning mathematics acceptance may create a favourable expectation; that exposure is explicitly retained. The coordinate classification was suggested by root; its checkable byte-content facts were independently recomputed, rather than accepted on that suggestion alone.',strict_reaudit_trigger='If additional communication supplied earlier semantic slots/deltas/fidelity verdicts/repairs, or source expectations were changed after exposure to those payloads, reassess anti-anchoring and require a genuinely fresh independent source review. No such payload is present in the bounded disclosed record.',reviewer_exposure='This actor previously reviewed mathematics/exact SCI76 and is not blind to its acceptance. This is an independent communication/protocol review, distinct from root/message author and fresh source reviewer; it is not a new source-fidelity or mathematical certification.',evidence=pin(OWN/'evidence.json'),proposed_append_only_qualification=pin(OWN/'qualification.addendum.proposed.json'),limitations='Exact notice supplied by root; no private chat/session-store audit or undisclosed-message absence proof. No precise notice timestamp claimed.',canonical_or_ledger_Git_writes=False,Lean_recompiled=False,new_VERIFIED=False,aggregate=False,reader=False,PURIFIED=False,whole_paper=False,Goal_complete=False)
 write('decision.json',decision)
 payload=dict(payload_name='COMPLETE_SOURCE_COMMUNICATION_QUALIFICATION76',decision=decision,qualification=qualification,evidence=evidence,input_manifest=load(OWN/'inputs.manifest.json'),exact_notice_UTF8=NOTICE)
 write('complete-named-review.payload.json',payload)
 run=dict(schema='source-communication-qualification76/run-v1',status=decision['status'],actor=ACTOR,checked_existing_SCI=SCI,decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-review.payload.json'),wholelogical_recipe='Canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; remove ONLY top-level run_sha256.',source_fidelity_admission_invalidated=False,fresh_source_review_required=False,append_only_qualification_required=True,new_VERIFIED=False,canonical_Git_ledger_writes=False)
 run['run_sha256']=sha(canon(run));write('run.json',run)
 print(json.dumps(dict(status='QUALIFIED_PROVENANCE_ACCEPTED',actual_PID=os.getpid(),input_count=len(rows),literal_coordinate_checks=27,whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],no_new_VERIFIED=True)),flush=True)

def readback():
 run=load(OWN/'run.json');h=run.pop('run_sha256');assert sha(canon(run))==h
 for field in ['decision','inputs_manifest','complete_named_RAW_payload']:check(run[field])
 for row in load(OWN/'inputs.manifest.json')['inputs']:check(row)
 assert (OWN/'communication-notice.exactraw.txt').read_bytes()==NOTICE.encode()
 print(json.dumps(dict(status='READONLY_READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=h)),flush=True)

def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(Path(__file__).read_bytes());argv=[PY,'-B','-X','utf8',str(Path(__file__)),'_child',action]
 with (OWN/(action+'.stdout.RAW')).open('wb') as out,(OWN/(action+'.stderr.RAW')).open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='FOREGROUND_RUNNING',action=action,actual_PID=p.pid,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.RAW')),stderr=pin(OWN/(action+'.stderr.RAW')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',action=action,actual_PID=p.pid,exit_code=code)),flush=True);return code

def close():
 assert not (OWN/'lease.final.json').exists();readback();assert launch('readback')==0
 rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file()];run=load(OWN/'run.json');write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),closed_utc=now(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload'],all_child_sessions_closed=True,closing_process_exit='Must be observed by external foreground terminal; no postclose owned receipt write.',postclose_owned_writes=False,canonical_Git_ledger_writes=False,new_VERIFIED=False))
 print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))),flush=True)

def postclose():
 l=load(OWN/'lease.final.json');rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name!='lease.final.json'];assert rows==l['all_owned_outputs_except_only_self'] and sha(canon(rows))==l['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'),closure_logical_sha256=l['closure_logical_sha256'],owned_writes=False)),flush=True)

if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  if action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),error=repr(e),traceback=traceback.format_exc(),canonical_mutation=False))
  raise
