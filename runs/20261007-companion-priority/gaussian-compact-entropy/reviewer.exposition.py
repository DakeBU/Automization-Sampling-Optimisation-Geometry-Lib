from pathlib import Path
import json,hashlib,subprocess,datetime,re,html
from html.parser import HTMLParser
ROOT=Path('E:/Samplinglib'); P='runs/20261007-companion-priority/'
OUT=ROOT/(P+'gaussian-compact-entropy'); COMMIT='11d72a92db9366586f006ed22a4a78db37e7bb1c'
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=str(ROOT))
def emit(name,obj):
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();(OUT/name).open('xb').write(b);return sha(b)
assert git('rev-parse','HEAD').decode().strip()==COMMIT
inputs=[];frozen={}
def pin(path):
 if path in frozen:return frozen[path]
 b=(ROOT/path).read_bytes();i=len(inputs);raw='reviewer.exposition.input.%03d.raw.snapshot'%i;norm=raw.replace('.raw.','.lf.')
 (OUT/raw).open('xb').write(b);(OUT/norm).open('xb').write(lf(b))
 tracked=subprocess.run(['git','ls-files','--error-unmatch',path],cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode==0
 e=dict(path=path,raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b),raw_snapshot=raw,lf_snapshot=norm,tracked=tracked)
 if tracked:
  gb=git('show',COMMIT+':'+path);assert lf(gb)==lf(b),path
  e.update(Git_commit=COMMIT,Git_raw_sha256=sha(gb),Git_lf_sha256=sha(lf(gb)),working_equals_Git_LF=True)
 inputs.append(e);frozen[path]=e;return e
prod='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactEntropy.lean'
test='Tests/GaussianCompactEntropy.lean'
lesson='website/content/declaration_lessons/gaussian-compact-count-entropy.json'
pub='website/content/publications/gaussian-compact-count-entropy.json'
cell='research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-entropy.json'
audit='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianCompactEntropy.json'
companion='_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html'
modpage='_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactentropy.html'
testpage='_site/modules/tests-gaussiancompactentropy.html'
theorempage='_site/theorems/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactentropy-compact-count-gaussian-entropy-limits.html'
lessonpage='_site/lessons/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactentropy-compact-count-gaussian-entropy-limits-1cc46cd58acb.html'
graphpath='_site/data/underlying-lean-graph.json'
fixed=[prod,test,lesson,pub,cell,audit,companion,modpage,testpage,theorempage,lessonpage,graphpath,
 P+'gaussian-compact-entropy/publication-plan.json',P+'gaussian-compact-entropy/integration.json',P+'gaussian-compact-entropy/graph.0.json',P+'gaussian-compact-entropy/math-freeze.json',P+'gaussian-compact-entropy/verified.json',P+'gaussian-compact-entropy/reviewer.repository.ProofSeal.json',P+'gaussian-compact-entropy/whole-proof-review/math.review.json',P+'gaussian-compact-entropy/source.0.review.json',P+'gaussian-compact-entropy-source-graph-review/source-topology-review.repaired.json',P+'gaussian-compact-entropy/preproof/signature.prospective.txt',P+'gaussian-compact-entropy/preproof/statement-seals.accepted.json',P+'balanced-rademacher-clt/preproof/signature.prospective.txt']
for p in fixed:pin(p)
def text(p):return lf((OUT/frozen[p]['raw_snapshot']).read_bytes()).decode()
def obj(p):return json.loads(text(p))
ver=obj(P+'gaussian-compact-entropy/verified.json'); proofseal=obj(P+'gaussian-compact-entropy/reviewer.repository.ProofSeal.json')
assert ver['verified_commit']=='421496a5de7355830c0b4904ea10f33722ed3602'
assert ver['verification_status']=='passed-scoped'
assert proofseal['checked_commit']==COMMIT and proofseal['status']=='accepted-scoped'
for receipt in [ver['whole_mathematical_review_reused'],ver['source_audit']['source_receipt']]:
 e=pin(receipt['path']);assert e['raw_sha256']==receipt['raw_sha256'] and e['lf_sha256']==receipt['lf_sha256']
phase=obj(P+'gaussian-compact-entropy-source-graph-review/source-topology-review.repaired.json')
assert phase['verdict']=='accepted-scoped' and not phase['blocking']
source=obj(P+'gaussian-compact-entropy/source.0.review.json')
assert source['status']=='accepted-scoped' and source['verdict']=='equivalent-after-elaboration'
assert source['reviewer']!='gaussian_domain_preproof_reviewer_29'
freeze=obj(P+'gaussian-compact-entropy/math-freeze.json')
for p in [prod,test]:
 e=next(e for e in freeze['inputs'] if e['path']==p)
 assert frozen[p]['raw_sha256']==e['raw_sha256'] and frozen[p]['lf_sha256']==e['lf_sha256']
 assert sha(lf(git('show',ver['verified_commit']+':'+p)))==e['lf_sha256']

class Pre(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.current=None;self.blocks=[]
 def handle_starttag(self,t,a):
  if t=='pre':self.current=[]
 def handle_endtag(self,t):
  if t=='pre' and self.current is not None:self.blocks.append(''.join(self.current));self.current=None
 def handle_data(self,d):
  if self.current is not None:self.current.append(d)
def pres(s):
 p=Pre();p.feed(s);return p.blocks
unit=obj(lesson)['units'][0];publication=obj(pub)['items'][0]
decl=unit['declaration']; short='compact_count_gaussian_entropy_limits'
s=text(companion);a=s.index('<section id="gaussian-compact-count-entropy"');z=s.index('</article>',a)+len('</article>');section=s[a:z]
plain=html.unescape(section);fold=pres(section);assert len(fold)==2
src=text(prod);start=src.index('theorem '+short);end=src.index(' := by',start)
assert fold[0].strip()==src[start:end].strip()
assert fold[1].strip()==src[start:].strip()
assert text(P+'gaussian-compact-entropy/preproof/signature.prospective.txt').strip()==fold[0].strip()
assert len(unit['steps'])==5
for step in unit['steps']:
 assert step['formula'] in plain and step['title'] in plain and step['text'] in plain
assert unit['statement'] in plain and unit['formula'] in plain
assert publication['statement']==unit['statement'] and publication['assumptions']==unit['assumptions']
assert unit['astis_dependencies']==['AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian']
assert unit['astis_dependencies'][0] in src
assert 'BernoulliLogSobolev' not in src and not any('Bernoulli' in d for d in unit['astis_dependencies'])
pages=[]
for page,sourcepath in [(modpage,prod),(testpage,test)]:
 body=text(page);loc=body.index('id="complete-module-source"');blocks=pres(body[loc:]);assert blocks[0].strip()==text(sourcepath).strip()
 pages.append(dict(page=page,source=sourcepath,complete_source_LF_matches=True,decoded_source_sha256=sha((blocks[0].strip()+'\n').encode())))
for private in ['countLaw','normalizedSum','compact_observer']:assert private in text(modpage)
for t in ['zero_mass_entropy_limit','zero_count_derivative_domain_and_value']:
 assert t in text(testpage) and t not in section
assert '../../../modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactentropy.html#complete-module-source' in section
parentlink='../../../theorems/autosamplingtheory-technicallemmas-probability-balancedrademacherclt-balanced-count-sum-tendsto-gaussian.html'
assert parentlink in section and (ROOT/'_site/theorems'/parentlink.split('/')[-1]).exists()
pin('_site/theorems/'+parentlink.split('/')[-1])
g=obj(graphpath);gid='module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy'
branch=[e for e in g['edges'] if gid in [e.get('source'),e.get('target')] or 'GaussianCompactEntropy' in str(e.get('source','')) or 'GaussianCompactEntropy' in str(e.get('target',''))]
assert any(e['source']=='module:AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT' and e['target']==gid and e['relation']=='imports' for e in branch)
assert not any('Bernoulli' in e['source'] and e['target']==gid and e['relation']=='imports' for e in branch)
assert any(e['source']==gid and e['target']=='module:Tests.GaussianCompactEntropy' and e['relation']=='imports' for e in branch)
assert any(e['relation']=='source correspondence; not a Lean dependency' for e in branch)
emit('reviewer.exposition.branch.json',dict(nodes=[n for n in g['nodes'] if 'GaussianCompactEntropy' in n.get('id','')],edges=branch,scope='Affected static branch only; no whole graph/source-topology certification or browser QA'))
checks=dict(checked_commit=COMMIT,working_HEAD=COMMIT,mathematical_files_unchanged_from_freeze_and_verified421=True,tracked_inputs_Git_LF_match=True,five_mathematical_steps_complete=True,folded_statement_matches_exact_seal=True,folded_public_body_matches_source_with_namespace_tail=True,complete_module_and_Test_pages=pages,private_contexts_visible=['countLaw','normalizedSum','compact_observer'],formal_parent35_actual_call_and_branch=True,no_fake_Bernoulli_parent=True,actual_allN_L1_and_successor_limits=True,zero_mass_continuous_tlogt=True,N0_derivative_value='fprime(0)^2, not forcedzero',Test_tails_inline=False,Test_pages_exist_complete=True,Test_page_linked_from_this_companion_section=False,source_module_links_resolve_statically=True,browser_render_or_interaction_run=False,compiler_started=False,minor_not_blocking_notes=['The prose support containment is read in the standard topological closed-support sense; exact Lean primitive uses tsupport rather than raw nonzero-set support.','The entropy step uses N as a generic asymptotic index; the exact statement/main formula use successor N+1.','Displayed N^(-1/2) is shorthand for the folded Lean totalized inverse-sqrt convention; N0 is explicitly covered by assumptions and actual Test value.','Earlier publication/source metadata labels marking later reviews pending are historical conservative boundaries, not substituted for distinct accepted receipts.'])
emit('reviewer.exposition.checks.json',checks)
gap=dict(status='OPEN',items=['Actual Test tails not inline in source-adjacent companion lesson; complete Test pages exist but this section has no Test-page link','CopyLean/source download control and download behavior not independently executed','Paper/book/chapter bundles not delivered or checked in this bounded review','Rendered browser/device formulas, fold/copy/download interactions not tested','No36 remote CI/deployment/live evidence inferred from prior34/35 remote receipts','Postmerge PURIFIED and human-facing completeness remain open'])
seal=dict(schema_version=1,verdict='ACCEPTED_SCOPED_EXPOSITION_SEAL',status='accepted-scoped',reviewer='gaussian_domain_preproof_reviewer_29',checked_commit=COMMIT,scope='Static source-adjacent36 mathematical reader and complete production/Test module pages; independent of root prose author. No sourcegraph selfvalidation, wholeproof rerun, compiler or remote/live certification.',independent_from_prose_author=True,source_graph_author_history='Reviewer authored36 source graph; source/topology truth reused ONLY from distinct phase repaired review, not selfvalidated.',mathematical_declaration=decl,mathematical_exposition='Literal card-normalized Bool law and signed inverse-sqrt sum, mean0 varianceNNReal1 Gaussian, C2 AND compact support, three genuine Gaussian L1 and allN count L1 outputs, three successor observer limits and same homogeneous entropy limit. Continuous tlogt handles zero mass. Actual N0 derivative expectation fprime(0)^2 may be nonzero. No fullflip4/LSI/T2/FIRST/main/cost claim.',formula_proof_steps=[dict(title=t['title'],formula=t['formula']) for t in unit['steps']],checks='reviewer.exposition.checks.json',graph_branch='reviewer.exposition.branch.json',blockers=[],mathematical_and_source_provenance=dict(source_topology_review=pin(P+'gaussian-compact-entropy-source-graph-review/source-topology-review.repaired.json'),actual_source_review=pin(P+'gaussian-compact-entropy/source.0.review.json'),wholeproof_review=pin(P+'gaussian-compact-entropy/whole-proof-review/math.review.json'),exact_proof_verified=pin(P+'gaussian-compact-entropy/verified.json'),current_repository_ProofSeal=pin(P+'gaussian-compact-entropy/reviewer.repository.ProofSeal.json'),boundary='Accepted receipts establish their own scoped provenance; none substitutes for this independent reader/formula/code correspondence check.'),FULL_READER_DELIVERY_GAP=gap,remaining_mathematical_boundary=['Fullflip-energy factor4','compact GaussianLSI final comparison','noncompact sqrt-RN/cutoff/W12 and finiteHilbert extension','full GaussianLSI/T2/SPHMC FIRST4.6','paper main/work/cost/composition'],input_bindings='reviewer.exposition.inputs.json',static_only=True,PURIFIED=False,human_facing_complete=False,compiler_started=False,leases=dict(read='CLOSED',write='CLOSED',compiler='CLOSED'))
emit('reviewer.exposition.inputs.json',dict(inputs=inputs,count=len(inputs),raw_LF_snapshots=True))
emit('ExpositionSeal.json',seal)
for e in inputs:
 b=(ROOT/e['path']).read_bytes();assert sha(b)==e['raw_sha256'] and sha(lf(b))==e['lf_sha256'],e['path']
assert git('rev-parse','HEAD').decode().strip()==COMMIT
outs=[]
for name in ['ExpositionSeal.json','reviewer.exposition.checks.json','reviewer.exposition.branch.json','reviewer.exposition.inputs.json','reviewer.exposition.py']:
 b=(OUT/name).read_bytes();outs.append(dict(path=P+'gaussian-compact-entropy/'+name,raw_sha256=sha(b),lf_sha256=sha(lf(b))))
runid=sha(json.dumps(dict(inputs=inputs,outputs=outs,checked_commit=COMMIT),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
emit('reviewer.exposition.run.json',dict(deterministic_run_sha256=runid,checked_commit=COMMIT,inputs_count=len(inputs),inputs=inputs,outputs=outs,all_input_raw_LF_unchanged_at_close=True,read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,lookup_diagnostics='Initial guessed Libraries/FrontierCells and website aggregate metadata paths absent; resolved exact canonical research-wiki/frontier-cells and semantic-roundtrip/audits files via filenames. No source/metadata modifications.'))
lease=json.loads((OUT/'reviewer.exposition.lease.json').read_text());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',inputs_count=len(inputs),deterministic_run_sha256=runid)
(OUT/'reviewer.exposition.lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status='CLOSED',verdict=seal['verdict'],run=runid,inputs=len(inputs),seal_sha256=sha((OUT/'ExpositionSeal.json').read_bytes()),FULL_READER_DELIVERY_GAP='OPEN')))
