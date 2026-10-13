from pathlib import Path

exec((Path(__file__).parent/'audit_storage101-v2.py').read_text(encoding='utf-8').split("r=put('storage-checks101.native.json'")[0])
from html.parser import HTMLParser
class Reader(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.depth=0;self.active=False;self.codes=[];self.code=None;self.details=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='section':
   if a.get('id')=='pbps-actual-prescribed-weighted-density':self.active=True;self.depth=1
   elif self.active:self.depth+=1
  if not self.active:return
  if t=='details':self.details.append(a)
  if t=='code':self.code=''
  if t=='a':self.links.append(a.get('href',''))
 def handle_endtag(self,t):
  if not self.active:return
  if t=='code' and self.code is not None:self.codes.append(self.code);self.code=None
  if t=='section':
   self.depth-=1
   if self.depth==0:self.active=False
 def handle_data(self,t):
  if self.active and self.code is not None:self.code+=t
reader=Reader();reader.feed(page.decode('utf-8'))
u=J(lesson)['units'][0];lines=blob(I,module).splitlines(keepends=True);regions=[]
for step in u['steps']:
 r=step['lean_source_region'];code=b''.join(lines[r['start_line']-1:r['end_line']]);ok=h(code)==r['exact_code_raw_sha256'];display=any(step['lean'].strip()==c.strip() for c in reader.codes)
 regions.append({'title':step['title'],'region':r,'actual_raw':h(code),'exact_raw_span_matches':ok,'generated_code_matches':display})
check('independent_generated_six_exact_regions',len(regions)==6 and all(x['exact_raw_span_matches'] and x['generated_code_matches'] for x in regions),regions)
check('independent_twelve_initially_folded',len(reader.details)==12 and all('open' not in x for x in reader.details),reader.details)
check('download_link_present',any('ActualPrescribedWeightedDensity.lean' in x for x in reader.links),reader.links)
trial=J(B+'/exact-commit-verification101/closed-trial480-manifest101.native.json');tr=[resolve(r) for r in trial['owned_artifacts']]
check('original480_trial_closed_RAW_recoverable',all(x['PASS'] for x in tr),tr)
repair=J(B+'/exact-commit-verification101/metadata-repair-admission101.native.json');orig='4808820b06e696524a9bd45b8d61f615f592999b';cp=repair['current_cell']['path']
check('original480_and_repaired471_cell_RAWs',h(blob(orig,cp))==repair['original_cell_RAW'] and h(blob(S,cp))==repair['current_cell']['raw_sha256'],repair)
repairpaths=subprocess.check_output(['git','diff','--name-only',orig,S]).decode().splitlines()
check('two_file_repair_only',len(repairpaths)==2 and cp in repairpaths and B+'/frontier-search-label-repair101.json' in repairpaths,repairpaths)
mt=J(B+'/exact-commit-verification101/metadata-transfer101-repaired.json')
check('index_and_owner_erratum_archives_recoverable',all(resolve(mt[k])['PASS'] for k in ['owner_erratum','independent_index_repair']),[resolve(mt[k]) for k in ['owner_erratum','independent_index_repair']])
check('original_science_module_lesson_audit_unchanged',all(blob(orig,p)==blob(S,p)==blob(I,p) for p in [module,lesson,pub,audit]))
# Recompute documented working-RAW source digest; this measures source, never rebuilds Lean.
paths=[Path('AutoSamplingTheory.lean'),*sorted(Path('AutoSamplingTheory').rglob('*.lean')),Path('Tests.lean'),*sorted(Path('Tests').rglob('*.lean')),Path('lakefile.lean'),Path('lean-toolchain'),Path('lake-manifest.json')]
dg=hashlib.sha256();count=0
for p in paths:
 if not p.exists():continue
 dg.update(p.as_posix().encode());dg.update(b'\0');dg.update(p.read_bytes());dg.update(b'\0');count+=1
check('current_source_digest_matches_gate_notes',dg.hexdigest()==notes['source_digest'],{'actual':dg.hexdigest(),'expected':notes['source_digest'],'files':count,'recipe':'tools/astis_site.py source_digest; path NUL exact RAW NUL'})
priorarchives=[p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',baseline]).decode().splitlines() if p.endswith('.gz') and ('100' in p or 'science100' in p or 'integration100' in p or 'delivery100' in p)]
changes=[p for p in priorarchives if blob(baseline,p)!=blob(I,p)]
check('inherited100_archives_unchanged',not changes,{'count':len(priorarchives),'changed':changes})
check('root_reader_graph_exact_parents',all(x in str(off['graph_node']) for x in ver['source_audit']['exact_four_actual_producer_parents']) and off['graph_node']['status']=='compiled',off['graph_node'])
# Keep bounded diagnostic mistakes as evidence; no input was mutated.
diag={'initial_script_read_failure':'Template numeric replacement changed date directory 20261007 to20261017; missing-path error before audit. Original audit_storage101.py retained; v2 corrects path only.','optional_parser_import':'bs4 absent; replaced with stdlib HTMLParser, no install.','bounded_search':'tools/build_site.py missing in rg multi-file query; actual tools/astis_site.py source_digest read successfully.','no_data_loss_or_mathematical_change':True}
put('diagnostics101.native.json',diag)
put('supplemental-storage101.native.json',{'kind':'independent-bounded-storage-reader-and-provenance101','science':S,'original_science':orig,'integration':I,'details':details,'errors':errors,'no_math_or_source_re_review':True})
put('supplemental-inputs101.native.json',{'inputs':list(reads.values())})
print(json.dumps({'errors':errors,'original_trial_artifacts':len(tr),'inherited100archives':len(priorarchives),'exact_verifier_artifacts':len(cl['owned_artifacts']),'sixregions':regions},ensure_ascii=True))
