from pathlib import Path
import hashlib,json,re,os,sys,datetime
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib'); O=Path(__file__).resolve().parent
C=R/'runs/20261007-companion-priority/pbps-centered-defect-preproof59/independent-elab-type-second'
B=C.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'lf_bytes':len(lf),'raw_sha256':sha(b),'lf_sha256':sha(lf)}
def put(n,v):
 p=O/n;assert not p.exists(),p;p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
manifest=[]
def freeze(p,expected=None):
 p=Path(p); a=pin(p)
 if expected:
  for k in ('bytes','lf_bytes','raw_sha256','lf_sha256'):assert a[k]==expected[k],(p,k)
 if not any(x['original']['path']==a['path'] for x in manifest):
  d=O/'inputs';d.mkdir(exist_ok=True);s=d/(f'{len(manifest):02d}-'+p.name+'.exactraw.snapshot')
  if s.exists():assert s.read_bytes()==p.read_bytes()
  else:s.write_bytes(p.read_bytes())
  manifest.append({'index':len(manifest),'original':a,'snapshot':pin(s)})
 return p.read_bytes().replace(b'\r\n',b'\n').decode('utf8')
assert not (O/'lease.json').exists()
proposal=json.loads(freeze(C/'exact-proposal.json'))
assert pin(C/'exact-proposal.json')['raw_sha256']=='c103391d43f99329d70ff4aa2dd627ecd5a3ca00ab99e4733b2f1bae206be304'
lease=json.loads(freeze(C/'lease.json'));assert lease['status'] in ('CLOSED','CLOSEDLAST')
creator=json.loads(freeze(C/'run.json'));ch=creator.pop('run_sha256');assert sha(canon(creator))==ch
assert ch=='c883cf8aa6ee244671043cdc4b553d9b920a1f2d1bc66f77fd8f0dee3c874f43'
assert sha(canon(creator['type_review_payload']))==creator['type_review_payload_sha256']
freeze(C/'receipt.json')
S=Path(proposal['complete_rfl_and_kernel_declaration_controls']['source']['path'])
source=freeze(S,proposal['complete_rfl_and_kernel_declaration_controls']['source'])
comparison=[]
for h in proposal['headers']:
 i=h['index'];a=freeze(h['parent']['path'],h['parent']);b=freeze(h['successor']['path'],h['successor'])
 line=h['deleted_let_definition'];at=a.index(line);assert a.count(line)==1 and at==h['deleted_definition_start_original_LF_character']
 stripped=a.replace(line,'');count=len(re.findall(r'\bH0\b',stripped));assert count==h['exact_kernel_inline_replacements']
 expanded=re.sub(r'\bH0\b','((innerSL ℝ q).ker)',stripped);assert expanded==b
 reverse=b.replace('((innerSL ℝ q).ker)','H0');reverse=reverse[:at]+line+reverse[at:];assert reverse==a
 assert a.encode()==Path(h['parent']['path']).read_bytes() and b.encode()==Path(h['successor']['path']).read_bytes()
 oldbinders=a.split(' :\n    let μ',1)[0];newbinders=b.split(' :\n    let μ',1)[0];assert oldbinders==newbinders
 for kind,text in [('let',a),('inline',b)]:
  expected=re.sub(r'^theorem \w+',f'def {kind}_kernel_signature{i}',text,count=1).replace(' :\n    let μ',' : Prop :=\n    let μ',1).strip()
  actual=source.split(f'def {kind}_kernel_signature{i}\n',1)[1]
  actual=f'def {kind}_kernel_signature{i}\n'+re.split(r'\n(?:def|theorem) ',actual,1)[0].rstrip()
  assert actual==expected,(i,kind,'FULL_PROP_MISMATCH')
 signature=oldbinders.split('\n',1)[1]
 expected=f'theorem kernel_signatures{i}_definitionally_equal\n'+signature+f' : let_kernel_signature{i} hα hαβ hV hH hη hβη = inline_kernel_signature{i} hα hαβ hV hH hη hβη := rfl'
 actual=source.split(f'theorem kernel_signatures{i}_definitionally_equal\n',1)[1].split('\n#print axioms',1)[0]
 assert expected==f'theorem kernel_signatures{i}_definitionally_equal\n'+actual
 # These declarations intentionally assume their complete conclusion: TYPE controls only.
 diag=source.split(f'theorem diagnostic_named_full_type{i}\n',1)[1].split('\n#print axioms',1)[0]
 prefix=signature+' (diagnostic_input :\n';assert diag.startswith(prefix)
 conclusion=b.split(' :\n',1)[1].rstrip()
 assert diag==prefix+conclusion+'\n\n) :\n'+conclusion+'\n := diagnostic_input'
 assert 'diagnostic_input' not in a+b
 comparison.append({'index':i,'parent':pin(Path(h['parent']['path'])),'successor':pin(Path(h['successor']['path'])),'exact_deleted_let':line,'deleted_at_LF_character':at,'kernel_expansions':count,'forward_exact_raw_LF':True,'reverse_exact_raw_LF':True,'all_other_bytes_unchanged':True,'full_binder_prefix_identical':True,'complete_original_and_successor_Prop_definitions_exact':True,'complete_named_rfl_exact':True,'diagnostic_control_conclusion_exact_extra_input_TYPE_ONLY':True})
classification=[]
assert len(creator['compiler_results'])==8
for result in creator['compiler_results']:
 assert result['compiler_status']=='CLOSED'
 log=freeze(result['stdout']['path'],result['stdout']);err=freeze(result['stderr']['path'],result['stderr']);assert not err
 if result['name'] in ('full-type-inline-kernel','consumer-inline-kernel-type'):
  code=freeze(result['source']['path'],result['source']);i=0 if result['name']=='full-type-inline-kernel' else 1
  header=Path(proposal['headers'][i]['successor']['path']).read_text(encoding='utf8').strip()
  assert header in code and 'fail "HEADER_ELABORATED_INTENTIONAL_NO_PROOF"' in code
 if result['actual_exit_code']==0:
  assert result['name']=='full-inline-definition-equality-and-kernel-controls' and 'error:' not in log
  for name in ('kernel_signatures0_definitionally_equal','kernel_signatures1_definitionally_equal','diagnostic_named_full_type0','diagnostic_named_full_type1'):
   m=re.search(re.escape('.'+name)+r"' depends on axioms: \[([^\]]+)\]",log);assert m,name
   assert set(re.findall(r'[A-Za-z_.]+',m.group(1)))=={'propext','Classical.choice','Quot.sound'}
  typ='EXIT0_COMPLETE_PROP_RFL_AND_ASSUMED_CONCLUSION_TYPE_CONTROLS';credit='Definition equality and TYPE only; no source theorem proof'
 elif 'HEADER_ELABORATED_INTENTIONAL_NO_PROOF' in log:
  assert result['actual_exit_code']==1 and log.count('error:')==1
  typ='EXIT1_INTENTIONAL_BODY_REACHED_NO_PROOF';credit='Named TYPE reached body; no proof credit'
 else:
  assert result['actual_exit_code']==1 and 'error:' in log
  typ='EXIT1_TYPE_NEGATIVE_NO_PROOF';credit='Negative diagnosis only'
 classification.append({'name':result['name'],'lake_pid':result['lake_pid'],'observed_lean_pids':[x['pid'] for x in result['observed_processes'] if x['exe']=='lean.exe'],'actual_exit_code':result['actual_exit_code'],'compiler_status':'CLOSED','classification':typ,'source':result['source'],'stdout':result['stdout'],'stderr':result['stderr'],'admitted_credit':credit})
assert [x['classification'] for x in classification].count('EXIT1_TYPE_NEGATIVE_NO_PROOF')==4
assert [x['classification'] for x in classification].count('EXIT1_INTENTIONAL_BODY_REACHED_NO_PROOF')==3
# Reuse immutable source/binder review and graph ONLY as historical support, never as this overlay's acceptance.
reused=[]
for rel in ('independent-source-topology59/source-statement.preproof-review.json','independent-source-topology59/source-proof-graph.json','independent-source-topology59/source-coverage.manifest.json','independent-source-topology59/lease.json','elaboration-overlay-source-review/source-overlay-review.json','elaboration-overlay-source-review/lease.json'):
 p=B/rel;freeze(p);reused.append(pin(p))
put('exact-comparison.json',{'headers':comparison,'compiler_results_independent_classification':classification,'creator_native_run_hash':ch,'creator_named_payload_hash':creator['type_review_payload_sha256']})
review={'actor':'/root/next_primary59','creator':'/root/whole_math52','verdict':'ACCEPT_EXACT_V2_TO_V3_KERNEL_SYNTAX_OVERLAY','proposal':pin(C/'exact-proposal.json'),'independence':'Exact complete headers, reconstruction and rfl correspondence checked anew; creator and prior verdicts are not acceptance substitutes. No compiler started by reviewer.','exact_delta':'Delete one local dependent let H0 per header; replace exactly 13/12 occurrences by ((innerSL ℝ q).ker). Typed identity annotations retained.','EXCESS':0,'source_hypothesis_changes':0,'source_graph_changes':0,'source_coverage_changes':0,'binder_and_definition_fidelity':'All other bytes identical, including E dimensions, real scalar, measures, internally produced probabilities/Markov/disintegration, actual SAME U/M/T, mean preservation/qAE1, whole centered kernel, full/centered defects, sharp rho/delta and centered IsUnit. Thus constants, t=1 and rank0/subsingleton scope unchanged. No caller CFC, probability, selfadjointness, finite L2 or Nontrivial premise added.','complete_rfl_evidence':'Exact complete parent/successor Prop definitions and complete original binders in both named rfl equalities correspond byte-for-byte to the proposed headers; creator terminal EXIT0 log lists standard three axioms.','compiler_classification_counts':{'TYPE_negative_EXIT1':4,'intentional_body_reached_EXIT1_NO_PROOF':3,'complete_rfl_and_assumed_conclusion_controls_EXIT0':1},'diagnostic_input':'Only in diagnostic_named_full_type0/1 controls, each assumes its exact conclusion. Supports TYPE checks only. Absent from both proposed public headers; zero source proof credit.','remaining_boundary':'Actual producer and Test sharp consumer theorem bodies, independent postproof source/math gates and publication remain open. Gamma/root/weakH1/dynamics/cost/mixing/full-paper/Goal completion not admitted.','reused_immutable_source_support':reused,'original_closed_audits_untouched':True,'compiler_by_reviewer':'NOT_STARTED','review_foreground_python_pid':os.getpid(),'read_only_inspection_negative':'Prior console metadata print EXIT1 gbk UnicodeEncodeError; corrected ASCII metadata print EXIT0. No mathematical diagnostic affected.'}
put('source-overlay-review.json',review)
put('input.manifest.json',{'qualified_indexed_immutable_inputs':manifest,'count':len(manifest),'copy_policy':'Only bounded exact artifacts; no recursive evidence copies, no new primary extraction.'})
payload={'verdict':review['verdict'],'review':pin(O/'source-overlay-review.json'),'comparison':pin(O/'exact-comparison.json'),'inputs':pin(O/'input.manifest.json'),'proposal':pin(C/'exact-proposal.json'),'headers':comparison,'EXCESS':0,'proof_completion_admitted':False,'new_compilers':0}
put('named-kernel-overlay-source.payload.json',payload)
put('review-author.receipt.json',{'python_pid':os.getpid(),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':review['verdict'],'inputs':len(manifest),'payload_sha256':sha(canon(payload)),'compiler_by_reviewer':'NOT_STARTED'})
print(json.dumps({'verdict':review['verdict'],'inputs':len(manifest),'header_expansions':[13,12],'EXCESS':0,'reviewer_pid':os.getpid(),'creator_native_hash_checked':ch,'compiler_classification_counts':review['compiler_classification_counts']}))
