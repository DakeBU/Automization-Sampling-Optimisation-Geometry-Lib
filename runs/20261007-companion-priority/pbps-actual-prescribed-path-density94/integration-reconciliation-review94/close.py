import pathlib,subprocess,json,hashlib
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
MERGE='ae17ebb1bb4cb46a47e1674373e9c317665152a1'; OURS='d39449f5b6fd6ebe05eb092f843d1b14c54623b1'; THEIRS='07fb78dd00550902ba2344edf5d6ac94d93d2044'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):(OUT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def tree(ref):
 result={}
 for row in git('ls-tree','-rz',ref).split(b'\0'):
  if row:
   meta,p=row.split(b'\t');result[p.decode()]=meta.decode()
 return result
checks=json.loads((OUT/'checks.final.json').read_text());base=json.loads((OUT/'checks.initial.json').read_text())['base'];ts={r:tree(r) for r in [base,OURS,THEIRS,MERGE]};conflicts=[];errors=[];counts={'unchanged':0,'ours_only':0,'theirs_only':0,'same_both':0,'both':0}
for p in set().union(*[set(t) for t in ts.values()]):
 b,a,c,m=[ts[r].get(p) for r in [base,OURS,THEIRS,MERGE]]
 if a==c:expect=a;kind='unchanged' if a==b else 'same_both'
 elif a==b:expect=c;kind='theirs_only'
 elif c==b:expect=a;kind='ours_only'
 else:conflicts.append(p);counts['both']+=1;continue
 counts[kind]+=1
 if expect!=m:errors.append({'path':p,'expected':expect,'actual':m})
expected_conflicts={'AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','runs/substantive_advances.jsonl','tools/tests/test_astis_publication.py','website/scripts/declaration_lessons.py'}
save('exact-tree-merge-review.json',{'merge':MERGE,'parents':[OURS,THEIRS],'merge_base':base,'counts':counts,'both_changed':sorted(conflicts),'errors':errors,'pass':not errors and set(conflicts)==expected_conflicts})
checks['checks'].append({'name':'Entire Git tree preserves all one-sided and identical changes','pass':not errors and set(conflicts)==expected_conflicts,'counts':counts})
assert all(c['pass'] or c.get('superseded_by') for c in checks['checks'])
inputs=json.loads((OUT/'inputs.final.json').read_text())
for suffix in ['independent-whole-math94/whole-math-decision94.native.json','independent-whole-math94/exposition94/exposition-decision94.native.json','independent-whole-math94/lf-transfer94/LF-transfer-decision94.native.json','exact-commit-verification94/verified.json']:
 p=OUT.parent/suffix;b=p.read_bytes();inputs.append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b),'reuse':'Unchanged mathematics, exposition, LF transfer and exact-science verification; no new mathematical review credit.'})
save('checks.closed.json',checks)
decision={'status':'ACCEPTED_INDEPENDENT_INTEGRATION_RECONCILIATION','reviewer':'/root/independent_whole_math93','checked_merge_commit':MERGE,'parents':[OURS,THEIRS],'scope':'Exact merge reconciliation and preservation only; no new mathematical, source, visual, main, purified or whole-Goal certification. No Lake builds executed.','production_raw_sha256':'60792981d3d2bac30d78a2373f7eed0002def8600e92553e9b5b0c87761599ec','findings':['All five manual resolution records match exact parent Git blobs and archived RAW inputs; Tests.lean normalized import union also checked.','Entire Git tree preserves all non-conflicting one-sided or identical parent changes. Exactly six paths changed differently on both branches; each reviewed.','Registry retains exact parent entry union: 546 entries, 544 formalizedLocal and two portCandidate. Tests count544 retained.','Both root/basic import sequences retained. All Python test methods retained; common order regression combines both branch markers. Four focused reader regressions passed.','Renderer retains source-adjacent statement disclosure and expanded literal Prop siblings before roadmap; proof helpers occur separately after mathematical proof.','Merged ledger is exact event-multiset union and contains both parent sequences in order. Current ledger adds exactly one legitimate sole-lane acquisition event. Replayed before active lanes empty; after only SAU94.','All21 collaborator native RAWs and production/lesson/publication/source audit science bytes unchanged.','Historical production logs and pre-normalization ledger resolve through exact committed gzip archives; local reconciliation archives pinned separately. No event content changed.'],'notes':['Initial review text count546 mistakenly included two portCandidate entries; status-aware check corrects the verifier test, not repository content. Original failed check retained.','First normalization resolver attempted to find newly authored Tests-root-before-LF.raw.gz in the merge commit. It is local reconciliation evidence, now explicitly locally pinned. Failed script retained.','Acquisition canonical_branch string retains codex/sphmc-standardized-rgo; current checkout is codex/sphmc-kl-fisher-integration. Acceptance binds exact merge commit and serialized lane replay, not equality of those descriptive branch labels.'],'shared_mutations_by_reviewer':False,'ledger_transition_by_reviewer':False,'Goal_complete':False}
save('decision.native.json',decision)
manifest={'status':'CLOSED_RAW','reviewer':'/root/independent_whole_math93','merge':MERGE,'inputs':inputs,'owned_evidence':[],'self_hash_intentionally_omitted':True}
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='closed-RAW-manifest.native.json':
  b=p.read_bytes();manifest['owned_evidence'].append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)})
save('closed-RAW-manifest.native.json',manifest)
print(json.dumps({p:sha((OUT/p).read_bytes()) for p in ['decision.native.json','closed-RAW-manifest.native.json']},indent=2))
