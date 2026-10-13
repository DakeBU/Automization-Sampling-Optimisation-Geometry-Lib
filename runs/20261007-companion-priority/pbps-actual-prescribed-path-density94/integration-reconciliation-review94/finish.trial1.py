exec(compile((pathlib.Path(__file__).with_name('review.py')).read_text(),str(pathlib.Path(__file__).with_name('review.py')),'exec')) if False else None
import pathlib,sys,json,gzip,hashlib,subprocess,collections,re,ast
ROOT=pathlib.Path('E:/Samplinglib'); sys.path.insert(0,str(ROOT))
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94'; OUT=RUN/'integration-reconciliation-review94'
MERGE='ae17ebb1bb4cb46a47e1674373e9c317665152a1'; OURS='d39449f5b6fd6ebe05eb092f843d1b14c54623b1'; THEIRS='07fb78dd00550902ba2344edf5d6ac94d93d2044'
initial=json.loads((OUT/'checks.initial.json').read_text()); checks=initial['checks']; inputs=json.loads((OUT/'inputs.initial.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def public(b):return ('\n'.join(x.rstrip() for x in norm(b).splitlines()).rstrip()+'\n').encode()
def save(p,v):(OUT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(p):
 p=pathlib.Path(p); p=p if p.is_absolute() else ROOT/p; b=p.read_bytes(); inputs.append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)});return b
def blob(ref,p):
 b=subprocess.check_output(['git','show',ref+':'+p],cwd=ROOT);inputs.append({'path':p,'commit':ref,'raw_sha256':sha(b),'bytes':len(b)});return b
def check(name,cond,**details):checks.append({'name':name,'pass':bool(cond),**details})
def events(b):return [json.loads(x) for x in norm(b).splitlines() if x.strip()]
for c in checks:
 if c['name']=='Registry exact union no duplicates count544':
  c['superseded_by']='Registry status-aware union and formalized count'; c['test_harness_issue']='Counted two portCandidate entries as formalized. Original failed trial retained verbatim in checks.initial.json.'
 if c['name']=='normalization record pending schema inspection':c['superseded_by']='Exact normalization archive checks below'
p='AutoSamplingTheory/TechnicalLemmas/Registry.lean'
rs={r:norm(blob(r,p)) for r in [OURS,THEIRS,MERGE]}
entries={r:re.findall(r'\{\s*key\s*:=\s*"([^\"]+)"(.*?)\n\s*\}',s,re.S) for r,s in rs.items()}
maps={r:{k:v for k,v in e} for r,e in entries.items()}
expected=dict(maps[THEIRS]);expected.update(maps[OURS])
check('Registry status-aware union and formalized count',maps[MERGE]==expected and len(entries[MERGE])==len(maps[MERGE])==546 and sum('LemmaMemoryStatus.formalizedLocal' in v for v in maps[MERGE].values())==544,total_entries=len(entries[MERGE]),formalized_entries=sum('LemmaMemoryStatus.formalizedLocal' in v for v in maps[MERGE].values()),port_candidates=[k for k,v in maps[MERGE].items() if 'LemmaMemoryStatus.portCandidate' in v])
for rec in json.loads(read(RUN/'integration94/text-normalization94.json')):
 raw=gzip.decompress(blob(MERGE,rec['archive'])); output=blob(OURS,rec['path'])
 check('Exact normalization archive '+rec['path'],sha(raw)==rec['raw_sha256'] and sha(output)==rec['public_sha256'] and public(raw)==output)
 if rec['path'].endswith('.jsonl'):check('Normalization changes no ledger event',events(raw)==events(output))
rec=json.loads(read(RUN/'integration94/main-reconciliation/root-test-line-endings.json'));raw=gzip.decompress(blob(MERGE,rec['archive']));output=blob(MERGE,rec['path'])
check('Tests root CRLF-only normalization',sha(raw)==rec['raw_sha256'] and sha(output)==rec['public_sha256'] and raw.replace(b'\r\n',b'\n')==output)
acq=json.loads(read(RUN/'integration94/sole-lane-acquisition94.json'));raw=gzip.decompress(read(acq['raw_archive']));current=read('runs/substantive_advances.jsonl');merged=events(blob(MERGE,'runs/substantive_advances.jsonl'));ev=events(current)
check('Sole-lane archived RAW and public normalization',sha(raw)==acq['raw_ledger_sha256'] and sha(current)==acq['public_ledger_sha256'] and public(raw)==current)
tail=ev[len(merged):]
check('One postmerge acquisition event only',ev[:len(merged)]==merged and len(tail)==1,tail=tail)
from tools import astis_advance as advance
states=advance.current_advances();active=[k for k,v in states.items() if v.get('state')=='STABILIZING'];before=advance._replay_advances(merged);previous=[k for k,v in before.items() if v.get('state')=='STABILIZING']
save('replayed-state-summary.json',{'active':active,'previous':previous,'relevant':{k:v for k,v in states.items() if 'Affine' in k or 'PrescribedPathDensity' in k or ('SPHMC' in k and v.get('state')=='STABILIZING')}})
check('Sole stabilization lane replay',active==acq['current_active_lanes'] and previous==acq['previous_active_lanes'],current=active,previous=previous)
names=['test_reader_embeds_statement_proof_and_separate_lean','test_each_proof_keeps_its_own_assumptions_and_provenance_adjacent','test_literal_proposition_and_proof_helpers_keep_distinct_reader_positions','test_chapter_map_is_mathematical_and_keeps_the_affine_boundary']
cmd=[sys.executable,'-X','utf8','-m','unittest',*[f'tools.tests.test_astis_publication.PublicationTest.{n}' for n in names],'-v']
proc=subprocess.run(cmd,cwd=ROOT,capture_output=True);(OUT/'python-tests.stdout.log').write_bytes(proc.stdout);(OUT/'python-tests.stderr.log').write_bytes(proc.stderr);save('python-tests.receipt.json',{'command':cmd,'exit_code':proc.returncode,'no_lake':True});check('Four focused Python reader regressions',proc.returncode==0)
save('checks.final.json',{'merge':MERGE,'checks':checks});save('inputs.final.json',inputs)
print(json.dumps({'failures':[x for x in checks if not x['pass'] and not x.get('superseded_by')],'active':active,'previous':previous,'test_exit':proc.returncode},indent=2))
