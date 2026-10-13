from pathlib import Path
import os,sys,json,hashlib,traceback,re,html
from collections import Counter
from types import SimpleNamespace
sys.dont_write_bytecode=True
ROOT=Path('E:/Samplinglib'); RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'; OWN=RUN/'independent-source72'
PRIOR=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def write(n,v):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(ROOT).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'bytewise CRLF-to-LF only'}
# These dispositions are independent review judgments against the pre-BODY source
# graph. They do not reconstruct source nodes from implementation declarations.
NODE_DISPOSITIONS={
'S00':('generalized real Hilbert domain','same inherited real AE L2 / centered HP0','generic 10-11; actual 29-43,80-83'),
'S01':('outside algebra leaf; no analytic callers','six original analytic callers retained exactly','actual 20-28,143-151; parent comparison'),
'S02':('outside algebra leaf','actual conditional P and all-kerP residual R inherited','actual 35-43,103-117,122-123,129-132'),
'S03':('outside algebra leaf','same actual AE reflection U inherited','actual 53-56,127; parent call 167'),
'S04':('abstract A parameter, no actual compression claim','same centered compression A0 inherited','actual 65-70,97-102'),
'S05':('explicit same-space G/Inv primitives','same positive root and two-sided centered inverse inherited','generic 12-16; actual 72-102'),
'S06':('explicit primitive hypotheses used in algebra; hAInv/hGInv retained but unused','all seven facts internally inherited or obtained from positivity','generic 13-16,24-45; actual 314-320'),
'S07':('outside algebra leaf; no polar claim','same isometric polar V0 inherited, no onto premise','actual 107-111'),
'S08':('u,v arbitrary; no observable/components claim','actual f/g and conditional/polar components retained; mean internal','actual 119-135,321-349'),
'S09':('exact B20-shaped definition generalized to H','exact same A0(Inv u) corrector on same HP0','generic 18-19; actual 136-137'),
'S10':('arbitrary perturbation vector r on one H','arbitrary u,v,r on same HP0 inside actual branch','generic 17-21; actual 139-141,315-349'),
'S11':('established norm/cross-term algebra','consumed from generic leaf','generic 23-49; actual 315-320'),
'S12':('established real v cancellation','consumed from generic leaf','generic 46-49; actual 315-320'),
'S13':('established linear term inner(u,Inv r)','consumed from generic leaf','generic 38-45; actual 315-320'),
'S14':('established positive half norm-square term','consumed from generic leaf','generic 34-37,46-49; actual 315-320'),
'S15':('new auxiliary Hilbert leaf established, not source B21','same-space generic specialization consumed','generic 9-49; actual 314-320'),
'S16':('real PBPS integration supplied by other unit','new actual original-input same-witness consumer','actual 152-435'),
'S17':('OPEN: actual H/K producer outside theorem','OPEN: actual H/K producer not constructed','source Ex23-Ex26; no K or half-turn implementation'),
'S18':('OPEN: arbitrary r is not source r_rho','OPEN: real r/r_rho definitions not instantiated','source Ex27; actual forall r is not algorithm producer'),
'S19':('OPEN: no B27 actual output theorem','OPEN: B27 actual output adapter not produced','source B27; actual theorem changes no algorithm kernel'),
'S20':('not a proof dependency of pure algebra','inherited B21 retained with same f/g components','actual 138,167,321-349'),
'S21':('OPEN: B28 combined dynamics','OPEN: B28 requires real B27 plus retained B21','source Ex35/Ex36/B28; final universal identity insufficient'),
'S22':('OPEN: residual estimates / Young constants','OPEN: B29-B31 not established','source later B4 inequalities'),
'S23':('OPEN: full B4 and paper/main','OPEN: full B4/decay/main/errors/cost/composition not established','bounded publication boundaries; no completion credit')}

code=0
try:
 assert not (OWN/'lease.final.json').exists()
 priorpins=load(OWN/'preparation.inputs.json')['inputs']
 for r in priorpins:
  p=ROOT/r['path'];assert sha(p.read_bytes())==r['raw_sha256'];assert sha(p.read_bytes().replace(b'\r\n',b'\n'))==r['lf_sha256']
 primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes()
 assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 cov=load(PRIOR/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json');graph=load(PRIOR/'stageA.source-proof-graph72.before-header.frozen.json')
 assert len(graph['nodes'])==24 and len(graph['edges'])==53 and set(NODE_DISPOSITIONS)=={n['id'] for n in graph['nodes']}
 rows=[]
 for region,items in [('primary255',cov['primary_entries']),('supplemental106',cov['supplemental_entries'])]:
  for i,r in enumerate(items):
   a,b=r['RAW_start'],r['RAW_end_exclusive'];assert sha(raw[a:b])==r['RAW_sha256'],r['math_id']
   ds=[{'node':s,'generic':NODE_DISPOSITIONS[s][0],'actual':NODE_DISPOSITIONS[s][1],'evidence':NODE_DISPOSITIONS[s][2]} for s in r['source_graph_nodes']]
   rows.append({'inventory':region,'inventory_index':i,'math_id':r['math_id'],'RAW_start':a,'RAW_end_exclusive':b,'RAW_sha256':r['RAW_sha256'],'frozen_classification':r['classification'],'frozen_reason':r['reason'],'StageB_node_dispositions':ds,'source_hash_verified':True,'EXCLUDED_credit':'outside frozen target; no proof/completion credit' if r['classification']=='EXCLUDED' else None})
 assert len(rows)==361
 write('StageB.source361.coverage.json',{'schema':'source72-immutable-source-inventory-current-dispositions-v1','source_inventory_raw_sha256':sha((PRIOR/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json').read_bytes()),'primary':pin(primary),'counts':dict(Counter(r['frozen_classification'] for r in rows)),'source_count':361,'unclassified':0,'rows':rows,'source_graph_unchanged':True,'NODE_means':'source-relevant, never all nodes proved; OPEN dispositions remain explicit','raw_range_recipe':'zero-based half-open exact fixed primary RAW offsets'})
 write('StageB.source-graph24-node-dispositions.json',{'source_graph':pin(PRIOR/'stageA.source-proof-graph72.before-header.frozen.json'),'nodes':[{'id':n['id'],'source_label':n['label'],'generic':NODE_DISPOSITIONS[n['id']][0],'actual':NODE_DISPOSITIONS[n['id']][1],'evidence':NODE_DISPOSITIONS[n['id']][2]} for n in graph['nodes']],'edge_count_unchanged':53,'implementation_graph':'Separate: actual -> compiled parent71 and generic; generic -> Mathlib only. No Lean edge from B21 to generic algebra.'})
 forms=load(PRIOR/'stageA.target20-exact-RAW-formulas72.frozen.json')['entries'];frows=[]
 for r in forms:
  assert sha(raw[r['RAW_start']:r['RAW_end_exclusive']])==r['RAW_sha256']
  mid=r['math_id'];num=re.search(r'Ex(\d+)',mid);k=int(num[1]) if num else None
  if mid=='A2.E20.m1':j=('exact definition','generic 18-19; actual 136-137','same half/minus/A Inv order')
  elif k is not None and 28<=k<=34:j=('established auxiliary algebra, specialized in actual','generic 23-49; actual 314-320','source actual Kf components must still be supplied externally; this algebra uses arbitrary u v r')
  elif k in [23,24,25,26,27] or mid=='A2.E27.m1':j=('OPEN actual producer/adapter','source S17/S18/S19','no arbitrary r is identified with real residual; no actual K output claim')
  else:j=('OPEN combined B28 dynamics','source S21','retained B21 plus generic identity does not construct K or source r_rho')
  frows.append({'math_id':mid,'RAW_start':r['RAW_start'],'RAW_end_exclusive':r['RAW_end_exclusive'],'RAW_sha256':r['RAW_sha256'],'exact_source_formula':r['alttext'],'disposition':j[0],'candidate_or_source_evidence':j[1],'boundary':j[2]})
 assert len(frows)==20
 write('StageB.source20-formula-coverage.json',{'count':20,'entries':frows})

 # Capture only new final current inputs and relevant exact local API/reader code.
 freeze=load(RUN/'source-review.freeze72.v3.json');extras=[RUN/'source-review.freeze72.v3.json',RUN/'root.reader-status-overlay72.adoption.json',ROOT/'tools/astis_publication.py',ROOT/'tools/astis_site.py',ROOT/'website/scripts/inline_lean.py',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean']
 finalpins=[]
 for i,e in enumerate(freeze['inputs']+[{'path':p.relative_to(ROOT).as_posix()} for p in extras]):
  p=ROOT/e['path'];b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
  if 'RAW_sha256' in e:assert sha(b)==e['RAW_sha256'] and len(b)==e['RAW_bytes']
  if 'LF_sha256' in e:assert sha(lf)==e['LF_sha256']
  rd=OWN/f'final-inputs/{i:02d}.exactraw.snapshot';ld=OWN/f'final-inputs/{i:02d}.LF.snapshot';rd.parent.mkdir(exist_ok=True);rd.write_bytes(b);ld.write_bytes(lf)
  r=pin(p);r.update(raw_snapshot=rd.relative_to(OWN).as_posix(),lf_snapshot=ld.relative_to(OWN).as_posix(),semantic_read='opaque identity only' if 'semantic-roundtrip/audits/' in p.as_posix() else 'authorized current input');finalpins.append(r)
 write('StageB.final-current-inputs.manifest.json',{'schema':'source72-final-current-finite-inputs-v1','inputs':finalpins,'input_count':len(finalpins),'initial_inputs_retained':'StageB.current-inputs.manifest.json','prior_inputs_reference_only':'preparation.inputs.json','primary_reference_only':pin(primary),'versions':'official0/1 initial; unapplied status v1/v2; approved v3 -> final official2/3; no math change'})
 packets=[load(RUN/f'source-review.packet.{i}.json') for i in [2,3]]
 modules=[ROOT/p['lean']['file'] for p in packets]; texts=[p.read_text(encoding='utf-8') for p in modules]
 parent=(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_text(encoding='utf-8')
 a=texts[1].split('private def actual_corrector_perturbation_statement',1)[1].split('\ntheorem ',1)[0]
 old=parent.split('private def actual_corrector_change_statement',1)[1].split('\ntheorem ',1)[0]
 addition=' ∧\n                                (∀ u v r : HP0,\n                                  C (u+ΓP0 r) (v-A0 r)-C u v=\n                                    inner ℝ u (Inv r)+‖r‖^2/2))'
 assert a.count(addition)==1;stripped=a.replace(addition,')');assert stripped==old
 pubsig=texts[1].split('theorem actual_corrector_perturbation',1)[1].split(' := by',1)[0]
 oldsig=parent.split('theorem actual_corrector_change',1)[1].split(' := by',1)[0]
 assert pubsig.replace('actual_corrector_perturbation_statement','actual_corrector_change_statement')==oldsig
 all_existentials=re.findall(r'∃ (\w+) :',a);witnesses=all_existentials[:12];assert witnesses==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'];assert all_existentials[12:]==['fP','gP']
 write('StageB.parent-retention.exact-check.json',{'parent_module':pin(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'),'actual_module':pin(modules[1]),'private_literal_parent_after_delete_exact_append_equal':True,'exact_deleted_append_LF':addition,'parent_literal_suffix_LF_sha256':sha(old.encode()),'six_public_callers_exact_equal_after_name_reversal':True,'twelve_witnesses_in_literal_order':witnesses,'all_old_clauses_and_order_retained':True,'no_extra_caller_or_provider':True})

 sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'))
 import astis_site as site
 import astis_publication as publication
 import inline_lean
 site.project_lean_paths=lambda:modules
 mods,decls=site.scan_project_sources();byname={d.full_name:d for d in decls};site._SOURCE_BY_NAME=byname
 # Only local-preview fold shape is evaluated; no Git status/published/live credit.
 site._ACTIVE_GIT=SimpleNamespace(web_root=None)
 line_rows=[];step_rows=[];bindings=[];reader=[]
 ranges=[[(1,8,'module context',[]),(9,21,'complete public auxiliary statement',['S00','S06','S09','S10']),(22,22,'proof assignment',[]),(23,26,'unfold and inner transport',['S11']),(27,33,'inverse and square-sum evaluation',['S06']),(34,37,'quadratic energy',['S14']),(38,42,'linear operator identity',['S13']),(43,45,'mixed linear term',['S13']),(46,49,'norm expansion and v cancellation',['S11','S12','S14']),(50,54,'namespace/axiom-query context',[])],[(1,19,'imports/source/module context',[]),(20,28,'six analytic callers in literal',['S01']),(29,118,'same definitions and twelve global witnesses',['S00','S02','S03','S04','S05','S06','S07']),(119,138,'retained actual f/g/components/mean/rotation/B21',['S08','S09','S20']),(139,141,'new same-HP0 universal perturbation conclusion',['S10','S16']),(142,142,'separator',[]),(143,151,'public six callers and literal return type',['S01']),(152,167,'unfold same literal and invoke exact parent71',['S16','S20']),(168,290,'extract parent witnesses and every old clause',['S00','S02','S03','S04','S05','S06','S07','S08','S20']),(291,313,'restore same centered types/definitions/D',['S00','S04','S05','S07']),(314,320,'internal positive-root selfadjointness; consume generic leaf',['S06','S15','S16']),(321,349,'same actual observable branch plus universal identity',['S08','S09','S10','S16','S20']),(350,435,'complete original witness and old-clause reassembly',['S16','S20']),(436,440,'namespace/axiom-query context',[])]]
 slugs=['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation']
 for n,(packet,path,text) in enumerate(zip(packets,modules,texts)):
  logical=dict(packet);logical.pop('packet_sha256');assert sha(canon(logical))==packet['packet_sha256']
  assert text==packet['candidate_publication_context']['current_lean_module']
  assert sha(path.read_bytes())==packet['candidate_publication_context']['file']
  lesson=load(ROOT/f'website/content/declaration_lessons/{slugs[n]}.json')['units'][0]
  item=load(ROOT/f'website/content/publications/{slugs[n]}.json')['items'][0];binding=item['bindings'][0]
  data={'declarations':byname,'lessons':{lesson['declaration']:lesson}}
  assert publication.review_context(item,binding,data)==packet['candidate_publication_context']
  assert publication.binding_digest(item,binding,data)==packet['publication_binding_sha256']
  linebytes=path.read_bytes().splitlines(keepends=True);lines=text.splitlines();seen=set();bodyseen=set()
  for j,s in enumerate(lesson['steps']):
   r=s['lean_source_region'];lo,hi=r['start_line'],r['end_line'];b=b''.join(linebytes[lo-1:hi]);lf=b.replace(b'\r\n',b'\n')
   assert r['path']==path.relative_to(ROOT).as_posix() and r['source_raw_sha256']==sha(path.read_bytes())
   assert sha(b)==r['exact_code_raw_sha256'];assert lf.decode()==s['lean']
   assert not bodyseen.intersection(range(lo,hi+1));bodyseen.update(range(lo,hi+1))
   step_rows.append({'unit':n,'step':j+1,'title':s['title'],'start_line':lo,'end_line':hi,'exact_BODY_RAW_sha256':sha(b),'exact_BODY_LF_sha256':sha(lf),'exact_formula':s['formula'],'exact_authored_text':s['text'],'code_equals_raw_span_and_LF_lesson':True,'formula_source_fidelity':'independently checked exact signs/constants/domain/operator order; formulas describe complete contiguous span with preceding context retained'})
  expectedbody=set(range(23,50)) if n==0 else set(range(152,436));assert bodyseen==expectedbody
  for lo,hi,role,nodes in ranges[n]:
   for line in range(lo,hi+1):
    assert line not in seen;seen.add(line)
    line_rows.append({'unit':n,'line':line,'line_RAW_sha256':sha(linebytes[line-1]),'role':role,'source_nodes':nodes,'in_exposition_BODY_span':line in bodyseen,'reviewed':True})
  assert seen==set(range(1,len(lines)+1))
  name=packet['lean']['declaration'];helper=lesson.get('helpers',[])
  if n==1:
   assert helper==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation_statement']
   d=byname[helper[0]];assert d.kind=='def' and d.source_line==20 and not d.has_placeholder
   signature,value=inline_lean.split_statement(d.source_text);assert signature.endswith(': Prop') and value.startswith(':=')
   assert value[2:].strip()==a.split(': Prop :=',1)[1].strip()
  else:assert helper==[]
  rendered=inline_lean.disclosure(name,role='proof',explanation='Exact local proof context.',page='teaching/local.html',helpers=tuple(helper))
  assert '<details ' in rendered and not re.search(r'<details[^>]*\sopen(?:\s|>)',rendered)
  if n==1:assert 'Full Lean proposition (definition)' in rendered and 'It supplies no mathematical proof or additional hypothesis' in rendered and html.escape(byname[helper[0]].source_text) in rendered
  (OWN/f'StageB.unit.{n}.bounded-adjacent-fold.html').write_text(rendered,encoding='utf-8',newline='\n')
  reader.append({'unit':n,'full_scanner_identity':name,'helper_identities':helper,'private_literal_full_exact_value_exposed':n==1,'initially_folded':True,'literal_nonprovider_label_correct':n==1,'method':'production scanner limited to exactly two modules; production disclosure against this bounded declaration cache, local-preview links only','browser_fullExposition_aggregate_live_credit':False})
  bindings.append({'unit':n,'final_official_packet_index':n+2,'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':sha((RUN/f'source-review.packet.{n+2}.json').read_bytes()),'publication_binding_sha256':packet['publication_binding_sha256'],'candidate_publication_context_sha256':sha(canon(packet['candidate_publication_context'])),'recomputed_from_exact_current_inputs':True})
 assert len(line_rows)==494 and len(step_rows)==10
 write('StageB.whole494-line-coverage.json',{'count':494,'modules':[pin(p) for p in modules],'unreviewed':0,'rows':line_rows,'proof_boundaries':{'generic':[23,49],'actual':[152,435]},'source_graph_not_inferred_from_code':True})
 write('StageB.exact10-BODY-formula-coverage.json',{'count':10,'generic_steps':6,'actual_steps':4,'BODY_lines':27+284,'complete_BODY_no_gap_no_overlap':True,'entries':step_rows})
 write('StageB.final-binding-checks.json',{'units':bindings,'source_graph_vs_Lean_graph_separate':True,'reader_checks':reader,'scope':'whole code/source/formula/statement and bounded fold evidence only, no aggregate reader/browser acceptance'})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'source_items':361,'nodes':24,'edges':53,'formulas':20,'lines':494,'steps':10,'parent_literal_exact':True,'final_bindings':bindings},indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:
 write('StageB.coverage.v2.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'writes_scope':OWN.relative_to(ROOT).as_posix()})
sys.exit(code)
