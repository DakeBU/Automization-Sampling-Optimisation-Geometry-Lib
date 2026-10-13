from verify import *
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from tools import astis,astis_advance
claim=load(R/'proved-local.json')
names=['L2PullbackRange','PBPSMacroscopicCenteredRange','PBPSCenteredMacroDefectGap']
native=['source0-verdict-addendum58/source.0.verdict-addendum.review.json','source-review58/source.1.review.json','source-complete-review58/source.2.complete.review.json']
reviews=[]
for n,f,d in zip(names,native,claim['lean_declarations']):
 q=load(R/f);a=load(ROOT/f'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-{n}.json')
 assert q['verdict']=='equivalent-after-elaboration' and not q['repairs'] and not q['mathematical_blockers'] and not q['publication_blockers']
 assert len(q['semantic_slots'])==7 and a['source_review']['state']=='accepted' and a['verdict']==q['verdict']
 assert a['source_review']['review_run_sha256']==q['review_run_sha256'] and a['source_review']['run_artifact']==str((R/f).relative_to(ROOT)).replace('\\','/')
 assert a['publication_binding_sha256']==q['publication_binding_sha256']
 assert q['source_text_visible_to_decoder'] is False and q['source_identity_visible_to_decoder'] is False
 reviews.append(dict(declaration=d,canonical_audit=pin(ROOT/f'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-{n}.json'),native_review=pin(R/f),verdict=q['verdict'],whole_run_sha256=q['review_run_sha256'],named_source_payload_sha256=q['source_review_payload_sha256'],semantic_slots=7,repairs=0,blockers=0))
orig=load(R/'source-review58/source.0.review.json');add=load(R/native[0]);assert orig['semantic_slots']==add['semantic_slots'] and orig['verdict']=='exact'
dec=load(R/'anonymous-decoder/run.json');assert dec['status']=='CLOSED' and dec['source_text_visible'] is False and dec['source_identity_visible'] is False
math=load(R/'whole-math58/receipt.json');assert math['verdict']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER'
fake=[]
for f in claim['lean_files']+['AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','Tests/GaussianMarginalPoincare.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean']:
 code=astis.strip_lean_comments_and_strings((ROOT/f).read_text(encoding='utf8'));hits=[i for i,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;fake.append(dict(input=pin(ROOT/f),findings=hits))
log=(D/'focused.log').read_text(encoding='utf8'); closures=[dict(declaration=n,axioms=[s.strip() for s in a.split(',')]) for n,a in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log,re.S) if n in claim['lean_declarations']]
assert len(closures)==3 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in closures) and 'sorryAx' not in log
state=astis_advance.current_advances();assert state['ASTIS-SA-20261008-PBPSMacroscopicCenteredRange']['state']=='PROVED_LOCAL'
stab=[k for k,v in state.items() if v['state']=='STABILIZING'];assert stab==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
write(D/'scoped-checks.json',dict(status='PASS',checked_commit=SCI,actual_PID=os.getpid(),source_reviews=reviews,source0_classification_only_seven_slots_unchanged=True,anonymous_decoder_source_text_blind=True,anonymous_decoder_source_identity_blind=True,decoder_run=pin(R/'anonymous-decoder/run.json'),original_complete_math=pin(R/'whole-math58/receipt.json'),whole_math_reused_without_reproof=True,standard_axiom_closures=closures,fake_closure_scan=fake,source_math_repairs=0,sole_STABILIZING=stab,remaining_boundary=claim['truth_boundary'],source_scope='Generic attributed background real L2 pullback range; actual PBPS B.1-B.5/C.3-C.4 mean/centered onto and all-centered macro sharp contraction/squared B defect precursor. Finite real Hilbert/Borel/rank0 extension explicitly disclosed. No Gamma/full weakH1/dynamics/main/cost/composition/full reader/live/PURIFIED credit.'))
print('PASS complete unchanged math / accepted sources3 / exact closures3 / fake scan7 / sole STABILIZING',os.getpid())
