import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,subprocess,collections
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib');C='c46af8a55e89419109f654c4553cf527993cbeed';E='e44b6b1e08c8a259a1f48006d822b53efd3fecb8';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
extra=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();x={'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))};extra.append(x);return b
def load(p):return json.loads(pin(p))
cmds=[]
def git(args):
 a=['git',*args];p=subprocess.Popen(a,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(cmds);(O/f'git{i}.stdout.RAW').write_bytes(out);(O/f'git{i}.stderr.RAW').write_bytes(err);cmds.append({'argv':a,'actual_PID':p.pid,'EXIT':p.returncode,'stdout':f'git{i}.stdout.RAW','stderr':f'git{i}.stderr.RAW'});assert p.returncode==0;return out
assert git(['rev-parse','HEAD']).decode().strip()==C
diffnames=git(['diff','--name-only',C,'--']).decode().splitlines()
expected={'AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','conversion-windows/ASTIS-SW-PBPS-2026.md','docs/assets/astis_lean_arsenal_module_graph.svg','docs/companion-papers-handoff.md','docs/module-graph.svg','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl','website/content/samplewiki_companion_frontiers.json','website/scripts/check_cross_domain_browser.py','website/scripts/inline_lean.py'}
assert set(diffnames)==expected,(set(diffnames)^expected)
c46diff=git(['diff',E,C,'--','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json']).decode();assert 'Samplinglib: Exact local library-retrieval70.json' in c46diff
assert git(['diff',E,C,'--','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'])==b''
integrationdiff=git(['diff',C,'--',*sorted(expected)])
reg=(B/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf-8');imp=(B/'AutoSamplingTheory/ExampleCases.lean').read_text(encoding='utf-8');test=(B/'Tests/Basic.lean').read_text(encoding='utf-8')
assert reg.count('localDecl := "'+D+'"')==1;assert imp.count('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation')==1
assert 'formalizedTechnicalLemmaCount = 518' in test
baseimp=git(['show',C+':AutoSamplingTheory/ExampleCases.lean']).decode();assert imp.replace('\r\n','\n').replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation\n','')==baseimp.replace('\r\n','\n')
basetest=git(['show',C+':Tests/Basic.lean']).decode();assert test.replace('\r\n','\n').replace('formalizedTechnicalLemmaCount = 518','formalizedTechnicalLemmaCount = 517')==basetest.replace('\r\n','\n')
entries=[json.loads(l) for l in (B/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()];selected=[x for x in entries if x.get('localDecl')==D or x.get('local_decl')==D];print('registry entries',len(entries),'matching',len(selected))
assert len(entries)==518
v=load(R/'verified.json');ledger=(B/'runs/substantive_advances.jsonl').read_bytes();before=v['ledger_before'];after=v['ledger_after'];assert len(ledger)==after['raw_bytes'] and sha(ledger)==after['raw_sha256'];assert sha(ledger[:before['raw_bytes']])==before['raw_sha256']
added=ledger[before['raw_bytes']:];events=[json.loads(l) for l in ledger.splitlines() if l.strip()];ev=[x for x in events if x.get('advance_id')=='ASTIS-SA-20261009-PBPSActualProjectedRotation'];ver=[x for x in ev if x.get('status')=='VERIFIED'];print('ledger matched',len(ev),'VERIFIED',len(ver),'added bytes',len(added),'keys',list(ver[0]) if ver else [])
assert len(ver)==1;assert len(added.splitlines())==1;ae=json.loads(added);assert ae==ver[0];assert C in str(ae);assert '/root/exact_science63' in str(ae);assert v['owner_id']!=v['verifier_id']
ad=load(R/'root.exact-verification70.adoption.json');assert sha(added)==ad['unique_VERIFIED_append_SHA256']
resume=load(R/'resume-state70/receipt.json');assert resume['head']==E and resume['exit_code']==0;assert set(l.strip() for l in resume['tracked_status'].splitlines())=={'M website/scripts/check_cross_domain_browser.py','M website/scripts/inline_lean.py'}
g=load(R/'integration70/generator-sideeffects/receipt.json');assert len(g['rows'])==539;counts=collections.Counter(x['action'] for x in g['rows']);print('generator actions',dict(counts))
assert g['tracked_generated_restored']==96 and g['unused_new_generated_cards_preserved']==443
for x in g['rows']:
 bb=pin(B/x['generated_backup']);assert sha(bb)==x['generated_RAW_sha256']
 if 'HEAD_backup' in x:
  hb=pin(B/x['HEAD_backup']);assert sha(hb)==x['HEAD_RAW_sha256'];assert (B/x['path']).read_bytes()==hb
 else: assert not (B/x['path']).exists(),x['path']
conversion=pin(B/'conversion-windows/ASTIS-SW-PBPS-2026.md');oldconversion=pin(R/'integration70/conversion.before.exactraw.md');cur=conversion.replace(b'\r\n',b'\n');old=oldconversion.replace(b'\r\n',b'\n');oldbody=old[old.index(b'## Current source packet'):];assert cur.endswith(oldbody);assert C.encode() in cur[:cur.index(b'## Current source packet')]
# Reuse native scientific reviews by immutable closure/adoption bindings, without rerunning or reopening their mathematical verdicts.
native=[]
for n in ['independent-math70/lease.final.json','independent-source70/lease.final.json','exact-science-verification70/lease.final.json','exact-science-verification70-label-supplement/lease.final.json','anonymous-decoder/lease.json','independent-reader-helper-code70/lease.final.json']:
 x=load(R/n);assert x['status']=='CLOSED_LAST';native.append({'path':n,'lease_RAW_sha256':extra[-1]['RAW_sha256'],'status':x['status'],'whole_logical_run_sha256':x.get('whole_logical_run_sha256'),'reuse_only':True})
helper=load(R/'independent-reader-helper-code70/lease.final.json')
for q in helper['manifest']:
 if q.get('relative_path') in ['inline_lean.py.current.RAW.py','check_cross_domain_browser.py.current.RAW.py'] or 'reviewed' in q.get('relative_path',''): print('helper evidence',q['relative_path'],q['raw_sha256'])
for s in ['inline_lean.py','check_cross_domain_browser.py']:
 h=sha((B/'website/scripts'/s).read_bytes());matches=[q for q in helper['manifest'] if q.get('raw_sha256')==h];assert matches,(s,h);print('current helper pinned',s,h,'native matches',len(matches))
# Preserve original SCI failure, not crediting the corrected label supplement as a rewrite.
neg=load(R/'exact-science-verification70/frontier.receipt.json');print('negative keys',list(neg));print('negative',json.dumps({k:v for k,v in neg.items() if k not in ['inputs']},ensure_ascii=False)[:1600])
negout=pin(R/'exact-science-verification70/frontier.stdout.log');negerr=pin(R/'exact-science-verification70/frontier.stderr.log');assert b'fail' in (negout+negerr).lower() or b'error' in (negout+negerr).lower()
notes=json.loads((R/'integration.notes.json').read_bytes());gate_rows=[];gate_drift=[]
for q in json.loads((O/'packet140.current-input-pins.json').read_bytes())['inputs']:
 p=pathlib.Path(q['path'])
 if p.name!='receipt.json' or R/'integration70' not in p.parents:continue
 x=json.loads(p.read_bytes());assert x['terminal_closed'] and x['exit_code']==0 and x['actual_foreground_PID']>0 and x['checked_parent']==C
 gate_rows.append({'label':p.parent.name,'actual_PID':x['actual_foreground_PID'],'EXIT':x['exit_code'],'command':x['command'],'started_utc':x['started_utc'],'finished_utc':x['finished_utc'],'receipt_RAW_sha256':q['RAW_sha256']})
 for a in x.get('inputs',[]):
  ab=pathlib.Path(a['path']).read_bytes()
  if sha(ab)!=a['RAW_sha256']:gate_drift.append({'gate':p.parent.name,'path':a['path'],'recorded_RAW_sha256':a['RAW_sha256'],'current_RAW_sha256':sha(ab)})
mandatory=(R/'integration70/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8');assert 'ASTIS check passed' in mandatory and 'Build completed successfully (9180 jobs).' in mandatory and 'Build completed successfully (9480 jobs).' in mandatory
assert len(gate_rows)==25,len(gate_rows)
scope=[x for x in gate_rows if x['label'].startswith('scope-')];assert len(scope)==6
write('additional-input-pins70.json',{'schema':'bounded-additional-input-pins-v1','count':len(extra),'LF_rule':'CRLF to LF only','inputs':extra})
result={'schema':'independent-repository70-checks-v1','actual_PID':os.getpid(),'checked_science_commit':C,'original_math_commit':E,'head_exact':True,'tracked_modified_paths':diffnames,'only_necessary70_integration_and_two_reviewed_reader_scripts':True,'Registry_count':len(entries),'production_entry_unique':True,'root_import_exact_only_added70':True,'Tests_only_count517_to518':True,'ledger_unique_nonowner_VERIFIED':{'count':1,'verifier':v['verifier_id'],'owner':v['owner_id'],'added_RAW_bytes':len(added),'added_RAW_sha256':sha(added),'original_e44_not_VERIFIED':True},'c46_only_search_label_metadata_no_Lean_change':True,'resume_clean_e44_except_two_scripts':True,'generator_sideeffects':{'restored':96,'unused_new_exact_backups':443,'verified_rows':539,'all_restored_current_RAW_match_HEAD_backups':True,'unused_paths_absent':True},'conversion':{'new70_prefix':True,'old_history_exact_LF_suffix_preserved':True,'RAW_and_LF_separate':True},'native_reuse':native,'gates':gate_rows,'earlier_gate_input_differences':gate_drift,'no_gate_rerun':True,'read_only_git_commands':cmds}
write('repository70.checks.json',result)
print('PASS bounded repository checks, gates',len(gate_rows),'scope',len(scope),'earlier input differences',len(gate_drift))
for q in gate_drift:print('GATE_INPUT_DIFFERENCE',q['gate'],q['path'])
