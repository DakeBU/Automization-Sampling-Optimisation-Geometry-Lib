from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime

ROOT = Path('E:/Samplinglib')
R = Path('runs/20261007-companion-priority/smoothed-score-posterior')
C = '8056022012fc999e577d5e72a40cdeaec4a77fbc'
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
    reviewpath = R/f'source.reader-kind.{n}.review.json'
    packetpath = R/f'source.reader-kind.{n}.reviewer-packet.json'
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

overlay = j(R/'source.reader-kind.overlay-review.json')
assert not overlay['blocking'] and overlay['status']=='accepted-scoped-reader-kind-only'
assert canon_hash(overlay,'review_run_sha256') == overlay['review_run_sha256']
paths.add(str(R/'source.reader-kind.overlay-review.json'))
decoder_run=j(R/'anonymous-decoder/run.json')
assert canon_hash(decoder_run,'decoder_run_sha256') == decoder_run['decoder_run_sha256']
assert decoder_run['source_text_visible'] is False and decoder_run['compiler_started'] is False
for n,source in enumerate(sources):
    resultpath=R/f'anonymous-decoder/result{n}.json'; result=j(resultpath)
    assert result['decoder_run_sha256'] == decoder_run['decoder_run_sha256']
    assert result['packet_sha256'] == j(R/f'source.reader-kind.{n}.review.json')['decoder_packet_sha256']
    assert result['reconstructed_text_sha256'] == j(R/f'source.reader-kind.{n}.review.json')['reconstructed_text_sha256']
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


gates=j(R/'reviewer.repository.gates.json')
assert all(x['returncode']==0 for x in gates['results']),gates
P='f91b82a2920b40299e57ccb821583a91e0a3e188'
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P
verified=j(R/'verified.json')
assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped'
assert sha((R/'verified.json').read_bytes())=='2ea325d6418a50ee56a616204ad953437e42d00417e890f98a21015cd22627fc'
kind_changes=[]
for n,slug in enumerate(plan['slugs']):
    p=f'website/content/declaration_lessons/{slug}.json'
    old=subprocess.check_output(['git','show',P+':'+p])
    now=Path(p).read_bytes()
    oldjson=json.loads(old);newjson=json.loads(now)
    assert diffs(oldjson,newjson)==['/units/0/kind']
    assert oldjson['units'][0]['kind']=='proof' and newjson['units'][0]['kind']=='theorem'
    assert len(newjson['units'][0]['steps'])==[4,7][n]
    kind_changes.append({'path':p,'diff':['/units/0/kind'],'before_git_LF_sha256':sha(old),'current':hashes(p),'source_independent_acceptance':overlay['changes'][n]})
checks.append({'name':'reader_kind_overlay','overlay':hashes(R/'source.reader-kind.overlay-review.json'),'changes':kind_changes,'public_statement_or_proof_change':False})
shared_files=['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean']
expected={shared_files[0]:['import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean'],shared_files[1]:['import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior'],shared_files[2]:['import Tests.GibbsGradientMean','import Tests.SmoothedScorePosterior']}
shared_rows=[]
import difflib
for p in shared_files:
    old=subprocess.check_output(['git','show',P+':'+p]).decode('utf-8').splitlines()
    now=Path(p).read_text(encoding='utf-8').splitlines()
    added=[line[2:] for line in difflib.ndiff(old,now) if line.startswith('+ ')]
    removed=[line[2:] for line in difflib.ndiff(old,now) if line.startswith('- ')]
    if p in expected:assert added==expected[p] and not removed,(p,added,removed)
    elif p.endswith('/Registry.lean'):
        assert len(added)==10 and not removed,(p,added,removed)
        assert any(plan['mathematical_declarations'][0] in x for x in added)
        assert any('formalizedLocal' in x for x in added)
    else:
        assert removed==['example : TechnicalLemmas.formalizedTechnicalLemmaCount = 474 := by native_decide']
        assert added==['example : TechnicalLemmas.formalizedTechnicalLemmaCount = 475 := by native_decide']
    shared_rows.append({'path':p,'current':hashes(p),'added':added,'removed':removed,'raw_EOL_difference_disclosed':True})
checks.append({'name':'actual_shared_imports_registry_tests','files':shared_rows,'formalized_leaf_count':475})
integration=j(R/'integration.json')
assert integration['verified_proof_commit']==P
assert integration['aggregate_summary']=={'root_build_jobs':9135,'tests_build_jobs':9400}
for rec in integration['checks']:
    assert rec['exit_code']==0
    assert sha(Path(rec['log']).read_bytes())==rec['raw_sha256']
    assert subprocess.check_output(['git','show',C+':'+rec['log']])==Path(rec['log']).read_bytes()
checks.append({'name':'root_integration_raw_receipts','integration':hashes(R/'integration.json'),'checks':integration['checks'],'existing_status_working_HEAD_is_proof_parent':'Root ran prospective shared edits before committing; independently fresh current exact-HEAD aggregate replaces any inference from that label.'})
import publication_reader
sitegraph=Path('_site/data/underlying-lean-graph.json');graph=j(sitegraph)
assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest(),(graph.get('publication_inputs_sha256'),publication_reader.graph_input_digest())
assert len(graph['nodes'])>0 and len(graph['edges'])>0
for dec in plan['mathematical_declarations']:
    assert any(n['id']=='decl:'+dec for n in graph['nodes'])
# Snapshot exact generated graph input, without regeneration or shared mutation.
(R/'reviewer.repository.graph.raw.snapshot.json').write_bytes(sitegraph.read_bytes())
checks.append({'name':'current_official_graph','path':str(sitegraph),'raw_sha256':sha(sitegraph.read_bytes()),'publication_inputs_sha256':graph['publication_inputs_sha256'],'nodes':len(graph['nodes']),'edges':len(graph['edges']),'formal_candidate_boundary':graph.get('reference_contract'),'snapshot':str(R/'reviewer.repository.graph.raw.snapshot.json')})
assert not astis.forbidden_pattern_hits()
checks.append({'name':'whole_repository_fakeclosure','Lean_files':len(astis.lean_source_files()),'hits':[],'scope':'Canonical ASTIS scan; comments and strings stripped; no conceptual edges promoted.'})
# Explicitly retain the historical exact proof receipt and every committed raw evidence file.
raw_evidence=[]
runpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',str(R)],text=True).splitlines()
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
rawout,_=proc.communicate(('\n'.join(C+':'+p for p in runpaths)+'\n').encode());assert proc.returncode==0
off=0
for p in runpaths:
    e=rawout.index(b'\n',off);size=int(rawout[off:e].split()[-1]);off=e+1
    blob=rawout[off:off+size];off+=size+1;b=Path(p).read_bytes()
    assert b==blob,('raw immutable run receipt differs from Git',p)
    raw_evidence.append(hashes(p))
checks.append({'name':'all_current_packet_committed_run_raw_artifacts','count':len(raw_evidence),'inputs':raw_evidence})
states=advance.current_advances()
assert states['ASTIS-SA-20261007-SmoothedScorePosterior']['state']=='VERIFIED'
assert [a for a,x in states.items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
cell_evidence=[]
for cid in plan['active_cells']:
    c=data['cells'][cid]
    assert c['status']=='independently_verified'
    assert c['evidence']['independent_verification']==str(R/'verified.json').replace('\\','/')
    cell_evidence.append({'cell':cid,'status':c['status'],'independent_verification':c['evidence']['independent_verification'],'verified_proof_commit':P})
checks.append({'name':'canonical_verifier_projection_and_single_stabilization','cells':cell_evidence,'original_sole_stabilization':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel','no_new_transition':True})
report={'schema_version':1,'artifact_kind':'independent-repository-ProofSeal','verification_status':'passed-scoped','status':'accepted-scoped','checked_repository_commit':C,'verified_proof_commit':P,'reviewer':V,'Lean':'leanprover/lean4:v4.33.0','Mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d','checks':checks,'fresh_repository_gates':gates,'scope':'Existing independently VERIFIED generic Gibbs mean-zero and actual source score/posterior same p/r/rho for all eta>0, now actual shared-root imports/Registry475/Tests consumer coverage. Proof is not repeated and no new mathematical credit.','source_boundary':integration['truth_boundary'],'ProofSeal':{'status':'repository-accepted-scoped','root':9135,'Tests':9400,'Registry':475,'source_review_current_bindings':True,'reachable_fakeclosure':len(closure),'whole_fakeclosure_hits':[]},'remaining_boundary':['FIRST4.6 W2/LSI/T2/bias/fullLemma4.2/algorithm/work/main/composition remain OPEN.','ExpositionSeal and postmerge purification are separate; no full-paper/PURIFIED badge or rendered interaction/Copy/Download/live acceptance.','Own exact published-head remote CI, merge/main admission and live deployment remain unclaimed. Prior-head success is not current CI.'],'no_state_or_shared_mutation':True,'read_lease':'CLOSED','write_lease':'CLOSED','compiler_lease':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=R/'reviewer.repository.ProofSeal.json';out.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
(R/'reviewer.repository.lease.json').write_bytes((json.dumps({'reviewer':V,'checked_commit':C,'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','compiler_lease':'CLOSED','receipt':out.as_posix(),'receipt_raw_sha256':sha(out.read_bytes()),'no_state_or_canonical_inputs_changed':True},indent=2)+'\n').encode())
print(json.dumps({'checked_commit':C,'status':'accepted-scoped','receipt':out.as_posix(),'raw_sha256':sha(out.read_bytes()),'git_source_inputs':len(gitrecords),'committed_raw_run_artifacts':len(raw_evidence),'graph_nodes':len(graph['nodes']),'graph_edges':len(graph['edges']),'leases':'CLOSED'},ensure_ascii=False))
