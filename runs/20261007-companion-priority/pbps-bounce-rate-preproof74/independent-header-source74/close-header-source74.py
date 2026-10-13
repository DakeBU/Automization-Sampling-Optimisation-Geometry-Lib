from pathlib import Path
import hashlib,json,os,sys
from datetime import datetime,timezone

ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
    b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def write(n,x):
    p=OWN/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
assert OWN.relative_to(ROOT).as_posix()=='runs/20261007-companion-priority/pbps-bounce-rate-preproof74/independent-header-source74'
assert not (OWN/'lease.final.json').exists()
run=json.loads((OWN/'source-header.0.run.json').read_bytes());check=dict(run);logical=check.pop('run_sha256');assert logical==sha(canon(check))
named=json.loads((OWN/'complete-named-review-decision-input-payload.json').read_bytes());assert named==run['complete_named_review_decision_input_payload']
assert named['decision']==json.loads((OWN/'source-header.0.decision.json').read_bytes())
assert named['input_payload']==json.loads((OWN/'source-header.0.input-payload.json').read_bytes())
assert named['review']['complete_text']==(OWN/'source-header.0.review.md').read_text(encoding='utf-8')
for p in named['input_payload']['external_current_and_context_pins']:
    assert pin(ROOT/p['path'])==p
stage=json.loads((OWN/'stageA.freeze74.json').read_bytes());cc=dict(stage);slog=cc.pop('run_sha256');assert slog==sha(canon(cc))
sm=json.loads((OWN/'stageA.manifest74.json').read_bytes())
for p in sm['stageA_finite_artifacts']:assert pin(ROOT/p['path'])==p
src=json.loads((OWN/'source-inputs74.json').read_bytes())
for k in ['primary','locator_map','old_closed_lease_opaque_pin']:assert pin(ROOT/src[k]['path'])==src[k]
primary=(ROOT/src['primary']['path']).read_bytes()
for p in src['regions']+src['blocks']:
    b=primary[p['RAW_start_inclusive']:p['RAW_end_exclusive']];assert sha(b)==p['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==p['LF_sha256']
coverage=named['source_coverage_projection']
assert len(coverage['source_item_projection'])==95 and len(coverage['all70_line_classification'])==70
assert len(coverage['all26_obligations'])==26 and len(coverage['13_internal_bridges'])==13
assert named['decision']['status']=='ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY'
assert not named['decision']['required_statement_repairs'] and not named['decision']['mathematical_or_source_blocking_deltas']
summary='''Accepted: prospective HEADER74 source admission only; no statement repair or excess caller.

Exact header3537B/70lines RAW/LF d72435795cd225af382948e8da683b6eb4b9e5b05509f8e3b0d10a3ed5a5a96e. Six analytic callers match73 and private/public prefixes byte-for-byte. The six actual local definitions and all10 clauses match the source boundary, including total-division R0=I, joint Borel S, continuous rate, exact rate sign/positive-part identities and the SAME-H deterministic energy-layer cap. beta-Lipschitz remains an internally produced obligation, not a caller.

Immutable StageA freeze d5030a6377411f433ce6f92a2c6f2d1bde4c7ae3b90908d18e98a1b60fadbded predates any74 candidate/hash.15 source regions/53blocks/95items(38NODE57EXCLUDED)/21formulas/28nodes52edges/26obligations are reused unchanged and exhaustively projected. All70 header lines and13 necessary internal proof bridges are recorded.73 and74 remain sibling deterministic edges; the current imports assert no formal73 parent.

No theorem BODY/proof/implementation source-fidelity or theorem compilation is accepted. Original predicate driver52824 EXIT1 is retained; one section end insertion and53780 EXIT0 supply predicate typing only. Own GBK terminal-output failure2396 EXIT1 and its explicitly premature receipt remain intact. StageA42568/headerreview10932 plus independent read-only33984/38700 all completed EXIT0. No canonical/Git/ledger/Goal/old CLOSED write. Actual random path/hazard/PDMP/nonexplosion/invariance/terminal kernel/main/cost/fullExposition/PURIFIED/wholepaper remain open. Future reader must expose complete private literal adjacent to public signature as a specification, never a provider.
'''
(OWN/'bounded-synthesis.final74.md').write_text(summary,encoding='utf-8',newline='\n')
write('terminal.close-header-source74.receipt.json',{'actual_PID':os.getpid(),'EXIT':0,'argv':sys.argv,'completed_native_verification':{'external_header_typing_context_pins':len(named['input_payload']['external_current_and_context_pins']),'StageA_artifacts_unchanged':len(sm['stageA_finite_artifacts']),'source_regions':15,'source_blocks':53,'source_rows':95,'header_lines':70,'clauses':10,'obligations':26,'future_internal_bridges':13,'complete_named_review_decision_input_equality':True,'whole_logical_run_sha256':logical},'preclose_external_readonly':{'PID':38700,'EXIT':0},'actual_close_is_final_owned_write_sequence':True,'no_Lean_site_graph_or_canonical_write':True})
members=sorted(p for p in OWN.rglob('*') if p.is_file() and p.name not in ['manifest.final.json','lease.final.json'])
manifest={'schema':'FINITE_OWNED_NATIVE_MANIFEST_CRLF_ONLY_LF_V1','scope':OWN.relative_to(ROOT).as_posix(),'LF_recipe':'Replace CRLF byte pairs with LF only; preserve bare CR and every other byte','member_count_excluding_self_and_last_lease':len(members),'whole_owned_file_count_including_manifest_and_lease':len(members)+2,'members':[pin(p) for p in members],'original_StageA_files_byte_unchanged':True,'historical_OPEN_lease_retained_as_history_only':'lease.open.json','negative_records_retained':['terminal.negative2396.json','terminal.primary-read74.premature2396.receipt.json','read-primary74.failed2396.exactraw.py'],'external_negative_predicate_pins_retained_in_input_payload':True}
write('manifest.final.json',manifest)
lease={'schema':'ASTIS_NATIVE_CLOSED_LAST_V1','state':'CLOSED','last_owned_write':'lease.final.json','closed_utc':datetime.now(timezone.utc).isoformat(),'actual_closing_PID':os.getpid(),'actual_terminal_EXIT':0,'whole_owned_file_count':len(members)+2,'manifest':pin(OWN/'manifest.final.json'),'native_complete_named_run':pin(OWN/'source-header.0.run.json'),'native_whole_logical_run_sha256':logical,'whole_logical_hash_recipe':'Delete ONLY top-level run_sha256; UTF8 canonical JSON ensure_ascii=False sort_keys=True separators=(comma,colon).','complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload.json'),'decision':pin(OWN/'source-header.0.decision.json'),'StageA_before_header':pin(OWN/'stageA.freeze74.json'),'review_status':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY','repairs':[],'proof_implementation_or_VERIFIED_credit':False,'old_CLOSED_or_canonical_changes':False,'postclose_policy':'Only external read-only verification; zero owned writes after this lease.'}
write('lease.final.json',lease)
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'CLOSED_owned_files':len(members)+2,'manifest':pin(OWN/'manifest.final.json'),'lease':pin(OWN/'lease.final.json'),'whole_logical_run_sha256':logical,'decision':pin(OWN/'source-header.0.decision.json'),'complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload.json')},ensure_ascii=True))
