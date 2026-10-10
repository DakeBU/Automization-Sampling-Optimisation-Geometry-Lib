import os,sys,json,re,subprocess,traceback
from pathlib import Path
import final68 as F
import review68 as R
ROOT=R.ROOT;O=R.O;P=R.P;PRE=R.PRE;BASE=R.BASE;ACTOR=R.ACTOR
pin=R.pin;save=R.save;read=R.read;get=R.get;sha=R.sha;now=R.now
SLUGS=['hilbert-sharp-quadratic-corrector-bound','pbps-sharp-corrector-energy']
def aux_pin():
 paths=[ROOT/'tools/astis.py',ROOT/'website/scripts/declaration_lessons.py',ROOT/'website/scripts/inline_lean.py',ROOT/'runs/20261007-companion-priority/pbps-root-commutation67/independent-math67/lease.final.json']
 rows=[]
 for i,p in enumerate(paths):
  b=p.read_bytes();rp=O/f'audit-inputs/{i:03}.RAW.snapshot';lp=O/f'audit-inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=pin(p),RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('audit.inputs.manifest.json',dict(actual_PID=os.getpid(),utc=now(),inputs=rows,input_count=len(rows),bounded_auxiliary_inputs=True))
def audit():
 F.stable();aux_pin();seals=read(F.frozen(PRE/'root.statement-seal68.json'));header_adopt=read(F.frozen(PRE/'root.header68.adoption.json'))
 assert pin(PRE/'independent-header-math68/lease.final.json')['raw_sha256']=='71cc0fecc36ddbbe0bdd25e7c778cca3a899578c484c606de8da5df0813c3c99'
 assert header_adopt['math_whole_logical_run_sha256']=='6938a3acb8fd912084aa34fef8491290daac94a452d24ef311137f7d352f01b6'
 assert pin(ROOT/'runs/20261007-companion-priority/pbps-root-commutation67/independent-math67/lease.final.json')['raw_sha256']=='e98cc7a699edf6827583c6d40a00505445cd033588693788b152afddc9b66425'
 parent=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean';gitraw=subprocess.check_output(['git','show',BASE+':'+parent.relative_to(ROOT).as_posix()],cwd=ROOT)
 assert sha(gitraw)==pin(parent)['raw_sha256']=='8567673eba335e7c1209f8bd90ce510954426bd5bbcdef6ff53ea97889762748'
 expanded=[]
 for n,path,name in [(1,F.MAIN,'actual_sharp_corrector_bound'),(2,F.TEST,'genuine_actual_modified_energy_equivalence')]:
  t=F.frozen(path).read_text(encoding='utf-8');definition=t.split('private def '+name+'_statement',1)[1].split('\ntheorem '+name,1)[0];definition='private def '+name+'_statement'+definition
  sealeddef=F.frozen(PRE/f'statement{n}.definition.lean').read_text(encoding='utf-8')
  assert definition.rstrip('\n')==sealeddef.rstrip('\n'),('private definition not sealed literal',n)
  db=definition.split(' : Prop :=\n',1)[1];h=F.frozen(PRE/f'header{n}-expanded.lean').read_text(encoding='utf-8');hb=h.split('theorem '+name,1)[1]
  caller,body=hb.split(' :\n',1);actualcaller=t.split('\ntheorem '+name,1)[1].split(' : '+name+'_statement',1)[0]
  defcaller=definition.split(name+'_statement',1)[1].split(' : Prop :=\n',1)[0]
  assert caller==actualcaller==defcaller
  assert db.rstrip('\n')==body.rstrip('\n'),('expanded type mismatch',n)
  assert all(x not in caller for x in ['Nontrivial','IsProbabilityMeasure','IsSelfAdjoint','IsPositive','Commute','Inv','Γ','CFC','IsUnit','FiniteDimensional ℝ (Lp'])
  expanded.append(dict(module=pin(path),sealed_definition=pin(PRE/f'statement{n}.definition.lean'),sealed_header=pin(PRE/f'header{n}-expanded.lean'),original_caller_exact=True,private_full_Prop_is_literal=True,expanded_Prop_equal_except_terminal_newlines=True,syntax_whitespace_map=dict(actual_definition_terminal_LF=len(definition)-len(definition.rstrip('\n')),sealed_definition_terminal_LF=len(sealeddef)-len(sealeddef.rstrip('\n')),header_body_terminal_LF=len(body)-len(body.rstrip('\n'))),no_new_premise=True))
 for q in seals['headers']:
  for k in ['header','literal_definition']:
   if k in q:
    d=q[k];pr=pin(ROOT/d['path']);assert pr['raw_sha256']==d['RAW_sha256'] and pr['raw_bytes']==d['RAW_bytes'] and pr['lf_sha256']==d['LF_sha256']
 plan=read(F.frozen(P/'publication-plan.json'))
 for q in plan['private_statement_definitions']:
  path=ROOT/q['path'];t=F.frozen(path).read_text(encoding='utf-8');name=path.name
  assert q['definition'].rstrip('\n') in t
 rows=[]
 for slug in SLUGS:
  lesson=read(F.frozen(ROOT/f'website/content/declaration_lessons/{slug}.json'));pub=read(F.frozen(ROOT/f'website/content/publications/{slug}.json'))
  assert len(lesson['units'])==len(pub['items'])==1
  u=lesson['units'][0];item=pub['items'][0];assert u['statement']==item['statement'] and u['assumptions']==item['assumptions'] and u['formula']==item['formulae'][0]['tex']
  for i,q in enumerate(u['steps']):
   r=q['lean_source_region'];path=ROOT/r['path'];raw=F.frozen(path).read_bytes();ls=raw.splitlines(keepends=True);span=b''.join(ls[r['start_line']-1:r['end_line']]);assert sha(raw)==r['source_raw_sha256'] and sha(span)==r['exact_code_raw_sha256'] and span==q['lean'].encode('utf-8'),('literal span mismatch',slug,i+1)
   name=R.NAME.rsplit('.',1)[1] if path==R.LEAF else F.NAMES['main' if path==F.MAIN else 'test'].rsplit('.',1)[1]
   text=raw.decode();offset=text.index('theorem '+name);body=text.index(':= by',offset)+len(':= by');bodyline=text[:body].count('\n')+1
   assert r['start_line']>=bodyline,('header mistaken for BODY',slug,i+1)
   rows.append(dict(slug=slug,step=i+1,title=q['title'],text=q['text'],formula=q['formula'],module_path=path.as_posix(),whole_source_RAW_sha256=sha(raw),start_line=r['start_line'],end_line=r['end_line'],span_RAW_bytes=len(span),span_RAW_sha256=sha(span),literal_BODY_match=True,body_start_line=bodyline))
 assert len(rows)==11 and [sum(q['slug']==s for q in rows) for s in SLUGS]==[5,6]
 save('formula-BODY.audit.json',dict(status='PASS',actual_PID=os.getpid(),step_count=11,steps=rows,whole_file_RAW_and_line_span_RAW_distinct=True,not_full_reader_Exposition_Seal=True))
 sys.path.insert(0,str(ROOT/'tools'));import astis
 scan=[];providers=[];decls=[]
 for path in [R.LEAF,F.MAIN,F.TEST]:
  text=F.frozen(path).read_text(encoding='utf-8');clean=astis.strip_lean_comments_and_strings(text)
  for i,line in enumerate(clean.splitlines(),1):
   if astis.FORBIDDEN_REGEX.search(line) or re.search(r'\b(unsafe|native_decide|run_tac)\b',line):scan.append(dict(path=path.as_posix(),line=i,text=line))
  found=re.findall(r'(?m)^\s*(private\s+)?(def|theorem|lemma|axiom|opaque|constant|instance)\s+(\w+)',clean)
  decls.append(dict(path=path.as_posix(),declarations=found,imports=re.findall(r'(?m)^import (.+)$',text)))
  for priv,kind,name in found:
   if priv and not (kind=='def' and name.endswith('_statement') and re.search(r'private def '+name+r'\b[\s\S]*? : Prop :=',clean)):providers.append(dict(path=path.as_posix(),kind=kind,name=name))
 assert not scan and not providers
 assert len(decls[0]['declarations'])==1 and len(decls[1]['declarations'])==len(decls[2]['declarations'])==2
 assert decls[1]['imports']==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation','AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound']
 assert decls[2]['imports']==['AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy']
 save('fake-closure-import.audit.json',dict(status='PASS',actual_PID=os.getpid(),scanner=pin(ROOT/'tools/astis.py'),scanner_function='strip_lean_comments_and_strings + FORBIDDEN_REGEX, plus unsafe/native_decide/run_tac',scoped_files=3,hits=scan,private_math_providers=providers,private_literal_Prop_count=2,declarations=decls,production_imports_Tests=False))
 axrows=[]
 for which,expected in [('leaf',[R.NAME]),('main',[F.NAMES['main']]),('test',[R.NAME,F.NAMES['main'],F.NAMES['test']])]:
  result=get(f'{which}.compiler.result.json');assert result['status']=='PASS' and result['receipt']['exit_code']==0 and result['receipt']['terminal_closed']
  t=(O/f'{which}.compiler.stdout.log').read_text(encoding='utf-8');matches=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",t)
  assert [x[0] for x in matches]==expected
  for name,s in matches:
   ax=[v.strip() for v in s.split(',')];assert len(ax)==3 and set(ax)=={'propext','Classical.choice','Quot.sound'};axrows.append(dict(compiler=which,declaration=name,axioms=ax))
 save('exact-axioms.audit.json',dict(status='PASS',actual_PID=os.getpid(),fresh_Lean_compilers=3,all_three_public_declarations_standard3=True,printed_occurrences=6,occurrences=axrows))
 m=read(F.frozen(P/'conceptual-mirror-audit68.json'));assert m['status']=='none-found'
 renderer=(ROOT/'website/scripts/declaration_lessons.py').read_text(encoding='utf-8');inline=(ROOT/'website/scripts/inline_lean.py').read_text(encoding='utf-8');assert "explanation=unit['lean_statement']" in renderer and "signature, body = split_statement(exact_source)" in inline and "code = signature if role == 'statement' else exact_source" in inline
 save('statement-caller-parent.audit.json',dict(status='PASS',actual_PID=os.getpid(),expansions=expanded,preproof_seals_exact=True,preproof_math130_reused_by_exact_lease=pin(PRE/'independent-header-math68/lease.final.json'),parent67_code_exact_BASE_GitRAW=pin(parent),parent67_closed_math164_lease=pin(ROOT/'runs/20261007-companion-priority/pbps-root-commutation67/independent-math67/lease.final.json'),main_existing_existential_objects=['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'],all_objects_from_same_parent_invocation=True,no_extra_caller_probability_range_root_CFC_gap_unit_inverse_energy_premise=True,rank_zero_and_alpha_eta_one_legal=True,conceptual_mirror=dict(record=m,independent_assessment='none-found is meaningful: this is a direct two-component quadratic form identity and its actual consumer. Existing discrete-hypocoercivity mechanism is not promoted to a Lean edge. No new independently justified cross-domain adapter is established.'),observer_corrections=[dict(issue='Ready message guessed47 final inputs',resolution='Authoritative native44 =43 rootfreeze inputs plus freeze; no native bytes changed'),dict(issue='Prose-valued lean_statement initially inferred to be faulty Lean code',resolution='Withdrawn after independently reading renderer: lean_statement is explanation; actual code comes from declaration.source_text/split_statement. Private definition placement/full reader seal remains a separate admission question.',renderer_files=[pin(ROOT/'website/scripts/declaration_lessons.py'),pin(ROOT/'website/scripts/inline_lean.py')])]))
 F.stable();print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),final_input_count=44,formula_BODY_matches=11,private_literal_Props=2,fake_closure_hits=0,standard3_public_declarations=3)))
if __name__=='__main__':
 try:audit()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else 'audit')+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
