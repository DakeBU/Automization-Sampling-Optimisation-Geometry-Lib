"""Distinct exact three-formula exposition repair, no final source verdict."""
from pathlib import Path
import copy,datetime,hashlib,json,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def read(p):return json.loads(p.read_bytes())
def put(n,j):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
skill=R/'.agents/skills/astis-semantic-roundtrip/SKILL.md'
module=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
lesson=R/'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json'
publication=R/'website/content/publications/pbps-actual-finite-first-event-law.json'
proposal=O.parent/'independent-math86/proposed-exposition-overlay86.v2.json'
expected={module:'cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5',lesson:'b1e33e24fdf5bc182fc16edce0e8821fb4c08855d0fdaafc0b1aa2ad436b7d4b',publication:'f1408d45a5bfe5aa5875b73786460296e451da94074a40335aad2d75a5392bb1',proposal:'89944d1cf3edd59938dea6acd1f1ca761e14d83f2f33487f59f24f640784f3b4'}
for q,h in expected.items():assert pin(q)['raw_sha256']==h,q
p=read(proposal);l=read(lesson);pub=read(publication);lines=module.read_text(encoding='utf8').splitlines();u=l['units'][0]
assert len(p['changes'])==3 and len(u['steps'])==11
assert [c['path'] for c in p['changes']]==['units[0].steps[5].formula','units[0].steps[7].formula','units[0].steps[8].formula']
after=copy.deepcopy(l);checks=[]
assessments={
 5:'BODY205-271 retains actual definitions, consumes hazard/flow/bounce/unitExp interfaces and installs P probability. Replacing the prematurely displayed survival law by literal product P is correct. Actual U law and survival are derived only at295-309 in step7. ell is a definitional shorthand for the displayed actual rate along flow, not a premature derived law.',
 7:'BODY317-348 establishes hmap, the entire unmarked waiting-time density equality through left-half-line CDFs. hmarked is not established until350-353. Keeping only F_*(P|A)=rho here matches this exact region.',
 8:'BODY349-367 derives finite rho, hmarked at350-353 and mass/real-mass/bound at354-366. Adding the marked-law equality here and retaining the mass formula matches all claims at their actual producer step.'}
for c in p['changes']:
 k=int(re.search(r'steps\[(\d+)\]',c['path']).group(1));assert u['steps'][k]['formula']==c['before']
 assert c['before']!=c['after'];after['units'][0]['steps'][k]['formula']=c['after']
 assert all(len(run)==1 for run in re.findall(r'\\+',c['after']))
 checks.append({'path':c['path'],'exact_before':c['before'],'exact_after':c['after'],'before_exact_match':True,'decoded_TeX_backslashes':'single','decision':'ACCEPT_EXACT_EXPOSITION_OPERATION','BODY_sequence_reason':assessments[k]})
def changes(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  assert a.keys()==b.keys();return sum((changes(a[k],b[k],path+'.'+k if path else k) for k in a),[])
 if isinstance(a,list):
  assert len(a)==len(b);return sum((changes(a[k],b[k],path+f'[{k}]') for k in range(len(a))),[])
 return [] if a==b else [path]
diff=changes(l,after);assert diff==[c['path'] for c in p['changes']]
assert u['formula']==after['units'][0]['formula'] and ord(u['formula'][0])==92 and ord(u['formula'][1])!=92
assert all(len(run)==1 for run in re.findall(r'\\+',u['formula']))
regions=[]
for k,step in enumerate(u['steps']):
 reg=step['lean_source_region'];a,b=reg['start_line'],reg['end_line'];code='\n'.join(lines[a-1:b])+'\n'
 assert reg['source_raw_sha256']==expected[module] and sha(code.encode())==reg['exact_code_raw_sha256']
 # Authored adjacent Lean equals exact region, allowing only the conventional terminal newline.
 assert step['lean'].rstrip('\n')==code.rstrip('\n'),k
 regions.append({'step':k+1,'title':step['title'],'start_line':a,'end_line':b,'exact_code_raw_sha256':reg['exact_code_raw_sha256'],'source_raw_sha256':expected[module],'adjacent_Lean_exact_match':True,'formula_changed':k in [5,7,8],'formula_BODY_sequence_after_patch':'MATCH','kind':'internal-helper' if k<5 else 'main-BODY'})
main=regions[5:];assert main[0]['start_line']==205 and main[-1]['end_line']==400
assert all(a['end_line']+1==b['start_line'] for a,b in zip(main,main[1:]))
helpers=regions[:5]
assert [(q['start_line'],q['end_line']) for q in helpers]==[(86,106),(108,124),(126,136),(138,158),(160,192)]
for a,b in zip(helpers,helpers[1:]):assert all(not s.strip() for s in lines[a['end_line']:b['start_line']-1])
assert pub['items'][0]['statement']==u['statement']==u['lean_statement']
assert pub['items'][0]['assumptions']==u['assumptions']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
e=put('exposition-repair.run-evidence86.json',{
 'schema':'astis.distinct-exact-exposition-repair-run86.v1','status':'closed','created_utc':now,'reviewer':'/root/fresh_source78','proposer':'/root/exact_verify77','exact_proposal':pin(proposal),
 'module':pin(module),'lesson':pin(lesson),'publication':pin(publication),'skill':pin(skill),
 'scope':'Exactly three sequencing formula fields; final primary-source/canonical-blind/BODY semantic verdict is not issued here.',
 'independence':{'distinct_from_proposer':True,'distinct_from_formalizer':True,'no_peer_math_decision_or_closed_manifest_read':True,'no_earlier_verdicts_or_canonical_audit_or_decoder_source_packets_read':True,'only_allowed_skill_module_lesson_publication_exact_proposal_inputs':True},
 'observed_checks':['Exact RAW hashes verified before inspection.','Entire current module read with line numbers; previously truncated display supplemented by lines300-405.','All11 authored formula/text/adjacent Lean/source regions inspected, including five helper lemmas and six main regions.','Decoded unit formula starts codepoints92,105: one backslash then i; no escape edit necessary.','Exact three before values matched; in-memory patch has exactly those three leaf diffs.','All11 region LF-terminated code hashes and adjacent Lean verified. Six main regions cover205-400 continuously; helper regions cover all five internal proofs with only blank separators.'],
 'public_statement_and_conditions':'Publication and lesson attributed full statement and assumption lists match and are unchanged by the three formula edits. Six analytic hypotheses, literal inputs, positive finite restriction, missing mass, bounded Borel tests and OPEN global boundaries are retained.',
 'licensing_hygiene':'No primary HTML or long verbatim primary extraction read or copied in this repair run. Output contains publication formulas, paraphrased sequencing reasons and exact RAW hashes only.',
 'no_compile_or_production_shared_state_write':True})
d=put('exposition-repair.decision86.json',{
 'schema':'astis.distinct-exact-exposition-repair-decision86.v1','status':'closed','created_utc':now,'verdict':'ACCEPT_EXACT_THREE_FORMULA_EXPOSITION_OVERLAY_ONLY','review_run_sha256':e['raw_sha256'],'proposal_raw_sha256':expected[proposal],
 'per_operation':checks,'exact_in_memory_leaf_diff':diff,'operations_expected':3,'operations_reviewed':3,'no_unit_formula_escape_edit':True,
 'authored_step_coverage':{'expected_steps':11,'reviewed_steps':11,'helpers_expected':5,'helpers_reviewed':5,'main_steps_expected':6,'main_steps_reviewed':6,'regions':regions,'gaps':[],'overlaps':[],'main_BODY_contiguous':True,'formula_BODY_exact_sequence_matches_after_overlay':True},
 'unchanged':{'module_RAW':expected[module],'header_statement_and_proof':True,'all_Lean_adjacent_fields':True,'all_step_text_titles_details_regions':True,'unit_formula':True,'full_public_statement_conditions_assumptions':True,'publication_RAW':expected[publication],'no_mathematical_or_source_binder_change':True},
 'minimality':'Only move survival/marked-law conclusions to the steps actually deriving them; retain global theorem formulas and all mathematical text. No escape transformation, assumption, definition or Lean proof repair.',
 'required_additional_repairs':[],'final_source_fidelity_verdict':'NOT_PERFORMED_PENDING_SEPARATE_CANONICAL_PACKET_REVIEW','truth_boundary':'Distinct exact exposition-only overlay acceptance; root alone may materialize it. No source theorem completion, compiled recheck, proof state transition, Seal/VERIFIED or whole-paper credit.'})
m=put('exposition-repair.run-manifest86.json',{'schema':'astis.exact-exposition-repair-raw-manifest86.v1','status':'closed','created_utc':now,'raw_inputs':[pin(q) for q in [skill,module,lesson,publication,proposal]],'raw_outputs':[pin(q) for q in sorted(O.iterdir()) if q.is_file() and q.name!='exposition-repair.run-manifest86.json'],'manifest_self_hash_omitted':True,'noncircular':'Evidence binds exact input RAWs; decision binds evidence RAW; manifest binds all outputs except itself.','owned_outputs_only':True,'no_originals_mutated':True,'private_primary_bulk_outputs':[]})
for q in [O/'exposition-repair.decision86.json',O/'exposition-repair.run-evidence86.json',O/'exposition-repair.run-manifest86.json']:print(json.dumps(pin(q)))
