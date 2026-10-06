from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime

ROOT = Path('E:/Samplinglib')
R = Path('runs/20261007-companion-priority/smoothed-score-posterior')
C = 'f91b82a2920b40299e57ccb821583a91e0a3e188'
V = 'picard_commit_verifier_20261005'
sys.path.insert(0, str(ROOT / 'tools'))
import astis_publication as pub
import astis
import astis_advance as advance

def j(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def hashes(path):
    b = Path(path).read_bytes()
    return {'path': str(path).replace('\\', '/'), 'raw_sha256': sha(b),
            'lf_sha256': sha(b.replace(b'\r\n', b'\n')), 'bytes': len(b)}

def canon_hash(x, field):
    return pub.digest({k:v for k,v in x.items() if k != field})

def diffs(a, b, prefix=''):
    if type(a) != type(b):
        return [prefix]
    if isinstance(a, dict):
        out = []
        for key in sorted(set(a)|set(b)):
            q = prefix + '/' + key
            out.extend([q] if key not in a or key not in b else diffs(a[key], b[key], q))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [prefix]
        return [q for n,(x,y) in enumerate(zip(a,b)) for q in diffs(x,y,prefix+'/'+str(n))]
    return [] if a == b else [prefix]

assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == C
plan = j(R/'publication-plan.json')
freeze = j(R/'math-freeze.json')
math = j(R/'whole-math-review.json')
checks, paths, footprint_drift = [], set(), {}

def bind(rec, snapshot=False):
    path = rec.get('snapshot') if snapshot else rec['path']
    assert path, rec
    h = hashes(path)
    assert h['raw_sha256'] == rec['raw_sha256'], (path,'raw')
    assert h['lf_sha256'] == rec['lf_sha256'], (path,'LF')
    if 'bytes' in rec:
        assert h['bytes'] == rec['bytes'], (path,'size')
    paths.add(path)
    return h

for rec in freeze['inputs']:
    bind(rec)
for rec in math['input_bindings'] + math['actual_parent_bindings']:
    bind(rec)
    if rec.get('snapshot'):
        bind(rec,True)
    if rec.get('lf_snapshot'):
        p=rec['lf_snapshot']; assert sha(Path(p).read_bytes()) == rec['lf_sha256']; paths.add(p)
assert canon_hash(math,'review_run_sha256') == math['review_run_sha256']
checks.append({'name':'mathematical_freeze','original_inputs':len(freeze['inputs']),
               'whole_math_inputs':len(math['input_bindings']), 'actual_parents':len(math['actual_parent_bindings']),
               'independent_whole_math_reuse':'matching exact raw/LF; no repeated mathematical credit'})

data = pub.inputs()
items = {x['id']:x for x in pub.load()}
sources = []
for n,ident in enumerate(plan['audit_ids']):
    a = data['audits'][ident]
    reviewpath = R/f'source.repaired.{n}.review.json'
    packetpath = R/f'source.repaired.{n}.reviewer-packet.json'
    review, packet = j(reviewpath), j(packetpath)
    paths.update([str(reviewpath),str(packetpath),f'research-wiki/semantic-roundtrip/audits/{ident}.json'])
    assert canon_hash(review,'review_run_sha256') == review['review_run_sha256']
    assert canon_hash(packet,'packet_sha256') == packet['packet_sha256']
    assert review['reviewer_packet_sha256'] == packet['packet_sha256']
    assert review['independent_from_formalizer'] and review['independent_from_decoder']
    assert review['verdict'] == 'equivalent-after-elaboration'
    assert not review['blocking'] and not review['deltas'] and not review['repairs'] and not review['EXCESS']
    assert a['state'] == 'accepted' and a['source_review']['state'] == 'accepted'
    assert a['source_review']['review_run_sha256'] == review['review_run_sha256']
    item = items[plan['slugs'][n]]
    binding = next(b for b in item['bindings'] if b['declaration'] == plan['mathematical_declarations'][n])
    current = pub.binding_digest(item,binding,data)
    assert current == a['publication_binding_sha256'] == review['publication_binding_sha256'] == packet['publication_binding_sha256']
    ctx = pub.review_context(item,binding,data)
    assert ctx == review['review_context'], (ident,'current context')
    assert sha(packet['source']['original_text'].encode()) == packet['source']['text_sha256'] == review['source_text_sha256']
    assert sha(packet['lean']['statement'].encode()) == packet['lean']['statement_sha256'] == review['lean_statement_sha256']
    module = hashes(packet['lean']['file'])
    assert module['raw_sha256'] == review['whole_module_raw_sha256']
    assert module['lf_sha256'] == review['whole_module_lf_sha256'] == review['whole_module_file_sha256']
    assert sha(a['reconstruction']['text'].encode()) == review['reconstructed_text_sha256']
    for rec in review['input_artifacts']:
        if rec.get('snapshot'):
            bind(rec,True)
        if Path(rec['path']).exists():
            live = hashes(rec['path']);paths.add(rec['path'])
            if live['raw_sha256'] != rec['raw_sha256']:
                p=rec['path']
                assert rec.get('snapshot'), ('unpreserved source drift',p)
                if p.endswith('.json'):
                    d=diffs(j(rec['snapshot']),j(p))
                else:
                    d=['non-json-bytes']
                footprint_drift[p]={'current':live,'reviewed_raw_sha256':rec['raw_sha256'],'changed_fields':d}
    sources.append({'audit_id':ident,'current_binding_sha256':current,
                    'review_run_sha256':review['review_run_sha256'],'packet_sha256':packet['packet_sha256'],
                    'source_input_artifacts':len(review['input_artifacts']), 'module':module})
checks.append({'name':'current_source_admission','reviews':sources,'footprint_drift':footprint_drift})

overlay = j(R/'source.repair.overlay-review.json')
assert not overlay['blocking'] and overlay['all_four_production_test_raw_bytes_unchanged']
assert canon_hash(overlay,'review_run_sha256') == overlay['review_run_sha256']
paths.add(str(R/'source.repair.overlay-review.json'))
decoder_run=j(R/'anonymous-decoder/run.json')
assert canon_hash(decoder_run,'decoder_run_sha256') == decoder_run['decoder_run_sha256']
assert decoder_run['source_text_visible'] is False and decoder_run['compiler_started'] is False
for n,source in enumerate(sources):
    resultpath=R/f'anonymous-decoder/result{n}.json'; result=j(resultpath)
    assert result['decoder_run_sha256'] == decoder_run['decoder_run_sha256']
    assert result['packet_sha256'] == j(R/f'source.repaired.{n}.review.json')['decoder_packet_sha256']
    assert result['reconstructed_text_sha256'] == j(R/f'source.repaired.{n}.review.json')['reconstructed_text_sha256']
    paths.add(str(resultpath));paths.add(str(R/f'anonymous-decoder/packet{n}.json'))
paths.add(str(R/'anonymous-decoder/run.json'))

# Fresh reachable canonical ASTIS closure, not a whole-source completion assertion.
closure=set()
def visit(path):
    if path in closure:return
    closure.add(path); paths.add(path)
    text=Path(path).read_text(encoding='utf-8')
    for mod in re.findall(r'^import\s+(AutoSamplingTheory\.[\w.]+)',text,re.M):
        p=mod.replace('.','/')+'.lean'
        if Path(p).exists():visit(p)
for p in [x['path'] for x in freeze['inputs'][:4]]:visit(p)
fake=[]
for path in sorted(closure):
    clean=astis.strip_lean_comments_and_strings(Path(path).read_text(encoding='utf-8'))
    for m in astis.FORBIDDEN_REGEX.finditer(clean):fake.append({'path':path,'kind':m.group(),'offset':m.start()})
assert not fake, fake
checks.append({'name':'reachable_fakeclosure','files':len(closure),'hits':fake,'paths':sorted(closure)})

# Git objects: canonical source normalized LF; immutable run snapshots/logs raw.
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C],text=True).splitlines())
requested=sorted(p for p in paths if p in tracked)
process=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
out,_=process.communicate(('\n'.join(f'{C}:{p}' for p in requested)+'\n').encode())
assert process.returncode==0
offset=0;gitrecords=[]
for path in requested:
    end=out.index(b'\n',offset);header=out[offset:end].split();size=int(header[-1]);offset=end+1
    blob=out[offset:offset+size];offset+=size+1
    raw=Path(path).read_bytes(); mode='raw-exact' if path.startswith(str(R).replace('\\','/')+'/') else 'LF-exact'
    assert blob == raw if mode=='raw-exact' else blob.replace(b'\r\n',b'\n') == raw.replace(b'\r\n',b'\n'), (path,mode)
    gitrecords.append({'path':path,'mode':mode,'git_blob_sha256':sha(blob),**{k:v for k,v in hashes(path).items() if k!='path'}})
checks.append({'name':'exact_git_objects','checked_commit':C,'files':len(gitrecords),'inputs':gitrecords,
               'external_mathlib_files':sorted(p for p in paths if p.startswith('.lake/packages/mathlib/'))})
publication=pub.check_advance(plan['mathematical_declarations'],reviewed=True)
checks.append({'name':'reviewed_publication_admission','result':publication})

gates=j(R/'reviewer.exact.retry.gates.json')
assert all(x['returncode']==0 for x in gates['results'])
A='ASTIS-SA-20261007-SmoothedScorePosterior'
state=advance.current_advances()[A]
assert state['state']=='PROVED_LOCAL'
assert set(state['publication_declarations'])==set(plan['mathematical_declarations'])
assert state['owner_id']!=V
oldC='7641ee07454a47c7a3d6a7818b8f833c7cd00045'
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==oldC
repair=j(R/'cell-reuse-repair.json')
repair_rows=[]
for n,cid in enumerate(plan['active_cells']):
    before=repair['before'][n];after=repair['after'][n]
    assert before['path']==after['path']
    old=Path(before['snapshot']).read_bytes()
    assert sha(old)==before['raw_sha256']
    assert sha(old.replace(b'\r\n',b'\n'))==before['lf_sha256']
    assert old.replace(b'\r\n',b'\n')==subprocess.check_output(['git','show',oldC+':'+before['path']]).replace(b'\r\n',b'\n')
    live=bind(after)
    original=j(before['snapshot']);current=j(before['path'])
    changed=diffs(original,current)
    assert changed==['/reuse_plan/reused_declarations'],changed
    lesson=j(Path('website/content/declaration_lessons')/(plan['slugs'][n]+'.json'))['units'][0]
    parents=current['reuse_plan']['reused_declarations']
    assert parents==lesson['astis_dependencies']==repair['actual_parent_lists'][cid]
    assert len(parents)==[4,8][n]
    repair_rows.append({'cell':cid,'before':before,'after':live,'changed_fields':changed,'canonical_parent_ids':parents})
# The root committed original verifier failures without modifying their raw bytes.
prior=j(R/'reviewer.exact.failed-admission.json')
assert sha((R/'reviewer.exact.failed-admission.json').read_bytes())==repair['failed_admission']['raw_sha256']
for g in prior['gates']['results']:
    bind(g)
checks.append({'name':'bounded_metadata_only_repair','old_rejected_commit':oldC,'current_commit':C,'two_exact_fields':repair_rows,'source_lessons_reviewed_and_unchanged':True,'prior_failed_receipt_preserved_raw':repair['failed_admission']})
# Check that previously reviewed mathematical evidence is honestly reusable at this new head.
focused=j(R/'reviewer.exact.gates.json')['results'][0]
bind(focused)
log=Path(focused['path']).read_text(encoding='utf-8')
axioms=[]
for name,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
    values={x.strip() for x in a.split(',')}
    assert values=={'propext','Classical.choice','Quot.sound'},(name,values)
    axioms.append({'declaration':name,'axioms':sorted(values)})
assert len(axioms)==5
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
mathlib=next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')
assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
checks.append({'name':'focused_evidence_reuse','prior_checked_commit':oldC,'current_four_math_files_raw_unchanged':True,'focused':focused,'jobs':3751,'printed_axioms':axioms,'clean_build_claim':False,'Lean':'leanprover/lean4:v4.33.0','Mathlib':mathlib['rev']})
report={'schema_version':1,'artifact_kind':'independent-exact-commit-retry-checks','reviewer':V,'verified_commit':C,'verification_status':'passed-scoped','checks':checks,'gates':gates,'cells_changed':False,'source_boundaries_preserved':True,'compiler_lease':'CLOSED','write_lease':'OPEN until separate VERIFIED publication and close','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.exact.retry.checks.json'
dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'checked_commit':C,'receipt':dest.as_posix(),'raw_sha256':sha(dest.read_bytes()),'checks':len(checks),'git_inputs':len(gitrecords),'closure_files':len(closure),'axiom_declarations':len(axioms),'status':'passed-scoped'},ensure_ascii=False))
