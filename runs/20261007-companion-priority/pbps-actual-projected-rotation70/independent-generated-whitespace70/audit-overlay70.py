import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,xml.etree.ElementTree as ET
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib');P=R/'integration70/generated-whitespace'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
inputs=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();inputs.append({'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))});return b
packetb=pin(R/'final-reader-repository-packet70.json');assert sha(packetb)=='4b98a34d129fcd9c0d8aa5352eb25b5b198a480585a6f37edfba2726e8cf5740';packet=json.loads(packetb)
lb=pin(R/'independent-repository-reader70/lease.final.json');assert sha(lb)=='44e6685c07f449a5f5a3ee8f697187394775ab507b707992735a105c4653e0c6';lease=json.loads(lb);assert lease['status']=='CLOSED_LAST' and lease['owned_count']==213
mb=pin(R/'independent-repository-reader70/owned-manifest.json');assert sha(mb)==lease['manifest']['RAW_sha256'];oldmanifest=json.loads(mb);assert sha(canon(oldmanifest['entries']))==oldmanifest['entries_canonical_sha256']
for q in oldmanifest['entries']:
 p=R/'independent-repository-reader70'/q['path'];bb=p.read_bytes();assert len(bb)==q['RAW_bytes'] and sha(bb)==q['RAW_sha256'] and p.stat().st_mtime_ns==q['mtime_ns_at_close']
proposalb=pin(P/'proposal.json');proposal=json.loads(proposalb);assert len(proposal['rows'])==3 and proposal['total_ASCII_bytes_removed']==6
original={q['path'].removeprefix('E:/Samplinglib/'):q for q in packet['inputs']};changes=[];expected={'docs/module-graph.svg':[313],'docs/assets/astis_lean_arsenal_module_graph.svg':[313],'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.md':[5,6]}
assert {q['path'] for q in proposal['rows']}==set(expected)
def xml_sem(e):return (e.tag,tuple(sorted(e.attrib.items())),None if e.text is None or not e.text.strip() else e.text,None if e.tail is None or not e.tail.strip() else e.tail,tuple(xml_sem(c) for c in e))
removed=0
for i,q in enumerate(proposal['rows']):
 before=pin(B/q['before_snapshot']);after=pin(B/q['after_snapshot']);current=pin(B/q['path']);assert current==after
 orig=original[q['path']];assert len(before)==orig['RAW_bytes'] and sha(before)==orig['RAW_sha256'] and sha(before.replace(b'\r\n',b'\n'))==orig['LF_sha256'];assert len(before)==q['before_RAW_bytes'] and sha(before)==q['before_RAW_sha256'];assert len(after)==q['after_RAW_bytes'] and sha(after)==q['after_RAW_sha256']
 bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True);assert len(bl)==len(al);changed=[j for j,(a,b) in enumerate(zip(bl,al),1) if a!=b];assert changed==expected[q['path']]==q['changed_lines']
 deltas=[]
 for j,(a,b) in enumerate(zip(bl,al),1):
  nl=b'\r\n' if a.endswith(b'\r\n') else (b'\n' if a.endswith(b'\n') else b'')
  body=a[:-len(nl)] if nl else a
  stripped=body.rstrip(b' ')+nl;assert b==stripped
  if a!=b:
   n=len(a)-len(b);removed+=n;deltas.append({'line':j,'ASCII_space_bytes_removed':n,'before_line_hex':a.hex(),'after_line_hex':b.hex(),'newline_hex':nl.hex()})
 if q['path'].endswith('.svg'):assert xml_sem(ET.fromstring(before))==xml_sem(ET.fromstring(after));assert deltas[0]['ASCII_space_bytes_removed']==2
 else:assert all(x['ASCII_space_bytes_removed']==1 for x in deltas)
 for name,bb in [('before',before),('after',after)]:
  f=f'pair{i}.{name}.exactraw.snapshot';(O/f).write_bytes(bb);(O/(f+'.LF')).write_bytes(bb.replace(b'\r\n',b'\n'))
 changes.append({'path':q['path'],'before_RAW_sha256':sha(before),'after_RAW_sha256':sha(after),'before_RAW_bytes':len(before),'after_RAW_bytes':len(after),'strict_line_deltas':deltas,'all_other_bytes_and_newlines_identical':True,'SVG_nonwhitespace_XML_structure_equal':True if q['path'].endswith('.svg') else None,'Markdown_single_space_EOL_removal_no_hardbreak_removed':True if q['path'].endswith('.md') else None})
assert removed==6
unchanged=[]
for q in packet['inputs']:
 rp=q['path'].removeprefix('E:/Samplinglib/')
 if rp in expected:continue
 bb=pathlib.Path(q['path']).read_bytes();assert len(bb)==q['RAW_bytes'] and sha(bb)==q['RAW_sha256'] and sha(bb.replace(b'\r\n',b'\n'))==q['LF_sha256'];unchanged.append({'path':q['path'],'RAW_sha256':q['RAW_sha256'],'LF_sha256':q['LF_sha256']})
assert len(unchanged)==137
write('input-manifest.json',{'schema':'independent-generated-whitespace70-finite-inputs-v1','count':len(inputs),'RAW_authority':True,'LF_recipe':'Only CRLF byte pairs become LF; all other bytes retained.','inputs':inputs,'other137_original_packet_inputs_checked_in_place_not_duplicated':unchanged})
decision={'schema':'independent-generated-whitespace70-decision-v1','reviewer':'/root/independent_primary69','status':'ACCEPT_EXACT_GENERATED_WHITESPACE_OVERLAY','accept_overlay':True,'preserve_scoped_aggregate_acceptance_under_exact_three_substitutions':True,'original_scoped_review':{'owned_count':213,'lease_RAW_sha256':sha(lb),'whole_logical_run_sha256':lease['whole_logical_run_sha256'],'original_packet_RAW_sha256':sha(packetb)},'proposal_RAW_sha256':sha(proposalb),'actual_independent_audit_PID':os.getpid(),'changes':changes,'ASCII_bytes_removed_total':removed,'original_CLOSED213_native_files_unchanged':True,'other_original_frozen_current_inputs_unchanged':137,'blocking_findings':[],'required_repairs':[],'scope':'Generated whitespace substitution only; no mathematical/source/VERIFIED re-adjudication or canonical/Git/ledger/Goal write.','no_replay_or_new_credit':['full library build','site/browser/graph rerun','VERIFIED transition','B21/B4/main/full Exposition/PURIFIED/wholepaper/Goal'],'root_failed_preflight_preserved':'Reported PID31552 EXIT1 is historical failed preflight, not relabeled; this review checks exact final bytes without retrying Git.','independent_review_does_not_apply_overlay':True}
write('overlay.decision.json',decision)
review='Accept the exact three generated-asset substitutions. The two SVGs each lose two ASCII spaces from otherwise blank line313. The module card loses one trailing ASCII space on each of lines5 and6; neither line had a Markdown two-space hard break. Exactly six ASCII bytes are deleted. Every other byte, every newline and the number of lines are preserved. Both SVG parsed non-whitespace XML trees, attributes, nonempty text/tails and child order are identical. Each before snapshot matches its original140 packet RAW/LF pin; each after snapshot equals current canonical RAW. The other137 original current inputs remain exact. The original CLOSED213 lease, manifest and all bound native file bytes/mtimes are unchanged. Its scoped aggregate/reader acceptance may be reused only under these three explicitly hashed substitutions. No mathematical/source review, VERIFIED transition or full-library/site/browser/graph execution was performed; no added completion credit is claimed. The root preflight31552 EXIT1 remains negative history. No canonical or Git write was made by this reviewer.\n'
(O/'overlay.full-review.RAW.md').write_bytes(review.encode());(O/'overlay.full-review.LF.md').write_bytes(review.encode().replace(b'\r\n',b'\n'))
write('tool-edit-observer-negative.json',{'operation':'apply_patch on new owned run-foreground.py schema label','status':'failed to match exact spacing; no patch applied','actual_tool_error_retained':'apply_patch verification failed: Failed to find expected lines','correction':'Read exact copied wrapper then patched exact spaced line.','terminal_PID':'Not exposed by apply_patch; no invented PID.','mathematical_or_canonical_effect':False})
print('actual_PID',os.getpid(),'PASS three exact substitutions, six ASCII spaces only; SVG semantics unchanged; other137 exact; CLOSED213 untouched; accept_overlay')
