from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime
sys.path.insert(0,'tools')
import astis_publication as pub
import astis
import astis_advance as advance
R=Path('runs/20261007-companion-priority/gaussian-sqrt-density-domain')
C='fbafcea29c4e3d4a90e6401d20edc989c3df9d7a'
P='1de412105042ebcfe147d50a3d1022fb0514faad'
V='picard_commit_verifier_20261005'
A='ASTIS-SA-20261007-GaussianSqrtDensityDomain'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(p):
    b=Path(p).read_bytes()
    return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def canon(d,k):return pub.digest({key:v for key,v in d.items() if key!=k})
def diffs(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):return [q for k in sorted(set(a)|set(b)) for q in ([p+'/'+k] if k not in a or k not in b else diffs(a[k],b[k],p+'/'+k))]
    if isinstance(a,list):
        if len(a)!=len(b):return [p]
        return [q for n,(x,y) in enumerate(zip(a,b)) for q in diffs(x,y,p+'/'+str(n))]
    return [] if a==b else [p]
paths=set();checks=[]
def bind(rec,snapshot=False):
    p=Path(rec['snapshot'] if snapshot else rec['path'])
    if not p.exists() and snapshot:p=R/p
    h=desc(p)
    assert h['raw_sha256']==rec['raw_sha256'],(p,'raw hash')
    assert h['lf_sha256']==rec['lf_sha256'],(p,'LF hash')
    if 'bytes' in rec:assert h['bytes']==rec['bytes'],(p,'bytes')
    paths.add(p.as_posix());return h
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
plan=j(R/'publication-plan.json');freeze=j(R/'math-freeze.json');math=j(R/'reviewer.math.review.json')
assert sha((R/'reviewer.math.review.json').read_bytes())=='bca3dc672771978affbdb8e2ab5ff948497f4fd0c0e8d7713f39cb97b7bc979a'
assert math['verdict']=='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF' and not math['blockers']
for rec in freeze['inputs']:bind(rec)
mathinputs=j(R/math['input_binding_receipt'])
assert len(mathinputs['inputs'])==math['input_count']==56
for rec in mathinputs['inputs']:bind(rec);bind(rec,True)
mathrun=j(R/'reviewer.math.run.json')
assert pub.digest(mathrun['artifacts'])==mathrun['run_sha256']
for rec in mathrun['artifacts']:
    r=dict(rec);r['path']=(R/rec['path']).as_posix();bind(r)
for sig in j(R/'preproof/statement-seals.accepted.json')['signatures']:
    actual=Path(sig['file']).read_text(encoding='utf-8')
    text=sig['signature_text']
    start=actual.index('theorem '+sig['full_declaration'].split('.')[-1]+'\n')
    end=actual.index(' := by',start)
    extracted=actual[start:end]+'\n'
    assert text==extracted and sha(extracted.encode())==sig['signature_lf_sha256']
checks.append({'name':'whole_math_and_signature_freeze','mathematical_review':desc(R/'reviewer.math.review.json'),'freeze_inputs':len(freeze['inputs']),'whole_math_inputs':56,'math_artifacts':len(mathrun['artifacts']),'math_run':mathrun['run_sha256'],'complete_body_reuse':'All seven generic private helpers, generic public assembly, real source consumer and three actual Test proofs independently reviewed by distinct mathematical reviewer; this exact verifier inspected current full production/Test bodies and matched frozen bytes. No duplicate completion credit.'})
data=pub.inputs();items={x['id']:x for x in pub.load()}
sources=[];drifts={}
decoder_run=j(R/'anonymous-decoder/run.json');decoder_run_raw=sha((R/'anonymous-decoder/run.json').read_bytes())
assert not decoder_run['source_text_visible'] and not decoder_run['compiler_started'] and not decoder_run['implementation_visible']
paths.add((R/'anonymous-decoder/run.json').as_posix())
for n,aid in enumerate(plan['audit_ids']):
    a=data['audits'][aid];review=j(R/f'source.{n}.review.json');packet=j(R/f'source.{n}.reviewer-packet.json')
    assert a['state']=='accepted' and a['source_review']['state']=='accepted'
    assert canon(review,'review_run_sha256')==review['review_run_sha256']==a['source_review']['review_run_sha256']
    assert canon(packet,'packet_sha256')==packet['packet_sha256']==review['reviewer_packet_sha256']
    assert review['verdict']=='equivalent-after-elaboration' and not review['blocking'] and not review['deltas'] and not review['repairs'] and not review['EXCESS']
    assert review['independent_from_formalizer'] and review['independent_from_decoder']
    assert set(review['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
    item=items[plan['slugs'][n]];binding=next(b for b in item['bindings'] if b['declaration']==plan['mathematical_declarations'][n])
    current=pub.binding_digest(item,binding,data)
    assert current==a['publication_binding_sha256']==review['publication_binding_sha256']==packet['publication_binding_sha256']
    assert pub.review_context(item,binding,data)==review['review_context']
    assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']==review['source_text_sha256']
    assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']==review['lean_statement_sha256']
    h=desc(packet['lean']['file'])
    assert h['raw_sha256']==review['whole_module_raw_sha256']
    assert h['lf_sha256']==review['whole_module_lf_sha256']==review['whole_module_file_sha256']
    assert review['whole_module_review']['entire_proof_and_private_helpers_read']
    result=j(R/f'anonymous-decoder/result{n}.json');blind=j(R/f'anonymous-decoder/packet{n}.json')
    assert result['decoder_run_sha256']==decoder_run_raw==review['decoder_run_sha256']
    assert result['packet_sha256']==blind['packet_sha256']==review['decoder_packet_sha256']
    assert result['packet_raw_sha256']==sha((R/f'anonymous-decoder/packet{n}.json').read_bytes())
    assert sha(result['reconstructed_theorem_text'].encode())==result['reconstructed_text_sha256']==review['reconstructed_text_sha256']==sha(a['reconstruction']['text'].encode())
    assert result['statement_sha256']==review['lean_statement_sha256']
    source_primary=review['source_read_evidence'];assert sha(Path(source_primary['path']).read_bytes())==source_primary['raw_sha256']
    paths.update([(R/f'source.{n}.review.json').as_posix(),(R/f'source.{n}.reviewer-packet.json').as_posix(),(R/f'anonymous-decoder/result{n}.json').as_posix(),(R/f'anonymous-decoder/packet{n}.json').as_posix(),source_primary['path'],f'research-wiki/semantic-roundtrip/audits/{aid}.json'])
    for rec in review['input_artifacts']:
        bind(rec,True)
        hnow=desc(rec['path']);paths.add(rec['path'])
        if hnow['raw_sha256']!=rec['raw_sha256']:
            changed=diffs(j(rec['snapshot']),j(rec['path']))
            if rec['path'].startswith('research-wiki/semantic-roundtrip/audits/'):
                allowed={'state','semantic_slots','deltas','verdict','source_review'}
                assert all(x.split('/')[1] in allowed for x in changed),changed
            elif rec['path'] in [f'research-wiki/frontier-cells/{cid}.json' for cid in plan['active_cells']]:
                allowed={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review'}
                assert all(any(x==q or x.startswith(q+'/') for q in allowed) for x in changed),changed
                current_cell=j(rec['path'])
                assert current_cell['status']=='independently_verified'
                assert current_cell['evidence']['proof_review'] and current_cell['evidence']['source_review']
            else:
                raise AssertionError(('unexpected source footprint drift',rec['path'],changed))
            drifts[rec['path']]={'reviewed_raw_sha256':rec['raw_sha256'],'current':hnow,'administrative_fields':changed}
    c=data['cells'][plan['active_cells'][n]];parents=c['reuse_plan']['reused_declarations']
    assert parents==data['lessons'][plan['mathematical_declarations'][n]]['astis_dependencies']==plan['actual_ASTIS_parents'][n]
    assert len(parents)==[5,2][n]
    sources.append({'audit':aid,'review':desc(R/f'source.{n}.review.json'),'review_run_sha256':review['review_run_sha256'],'packet_sha256':packet['packet_sha256'],'binding_sha256':current,'seven_slots':list(review['semantic_slots']),'whole_module':review['whole_module_review'],'input_artifacts':len(review['input_artifacts']),'source_primary':source_primary,'canonical_parent_ids':parents})
checks.append({'name':'current_source_decoder_publication','sources':sources,'decoder_run_raw_sha256':decoder_run_raw,'administrative_source_admission_only':drifts})
closure=set()
def visit(p):
    if p in closure:return
    closure.add(p);paths.add(p)
    for mod in re.findall(r'^import\s+((?:AutoSamplingTheory|Tests)\.[\w.]+)',Path(p).read_text(encoding='utf-8'),re.M):
        child=mod.replace('.','/')+'.lean'
        if Path(child).exists():visit(child)
for p in [r['path'] for r in math['frozen_production_files']]:visit(p)
fake=[]
for p in sorted(closure):
    clean=astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf-8'))
    for i,line in enumerate(clean.splitlines(),1):
        if astis.FORBIDDEN_REGEX.search(line):fake.append({'path':p,'line':i,'text':line.strip()})
assert not fake
assert not astis.forbidden_pattern_hits()
checks.append({'name':'fresh_fakeclosure','reachable_modules':len(closure),'module_inputs':[desc(p) for p in sorted(closure)],'reachable_hits':[],'full_canonical_files':len(astis.lean_source_files()),'full_hits':[]})

def gitbytes(commit,p):return subprocess.check_output(['git','show',commit+':'+p])
integration=j(R/'integration.json')
assert integration['verified_proof_commit']==P
assert integration['cell_metadata_preceded_graph_generation'] is True
rootlogs=[]
for row in integration['checks']:
    assert row['exit_code']==0
    h=desc(row['log']);assert h['raw_sha256']==row['raw_sha256']
    paths.add(row['log']);rootlogs.append(h)
verified=j(R/'verified.json')
assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped'
assert desc(R/'verified.json')['raw_sha256']=='d7a4744bd152b7b97ae3780bf48c5416859a4dfa1d35357a6dc73b4447cd8418'
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean']
changed=subprocess.check_output(['git','diff','--name-only',P,C,'--','*.lean'],text=True).splitlines()
assert set(changed)==set(shared),changed
import_adds={shared[0]:['import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity'],shared[1]:['import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain'],shared[2]:['import Tests.GaussianSqrtDensityDomain','import Tests.StandardizedRGOSqrtDensity']}
import difflib
shared_rows=[]
for p in shared:
    old=gitbytes(P,p).replace(b'\r\n',b'\n').decode();now=Path(p).read_bytes().replace(b'\r\n',b'\n').decode()
    changes=[x for x in difflib.ndiff(old.splitlines(),now.splitlines()) if x.startswith(('+ ','- '))]
    if p in import_adds:assert changes==['+ '+x for x in import_adds[p]],(p,changes)
    elif p.endswith('Tests/Basic.lean'):assert changes==['- example : formalizedTechnicalLemmaCount = 475 := by native_decide','+ example : formalizedTechnicalLemmaCount = 476 := by native_decide'],changes
    else:
        assert len(changes)==10 and all(x.startswith('+ ') for x in changes),changes
        assert any('localDecl := "'+plan['mathematical_declarations'][0]+'"' in x for x in changes)
        assert any('status := LemmaMemoryStatus.formalizedLocal' in x for x in changes)
    paths.add(p);shared_rows.append({'path':p,'old_git_raw_sha256':sha(gitbytes(P,p)),'current':desc(p),'normalized_changes':changes})
for cid in plan['active_cells']:
    p='research-wiki/frontier-cells/'+cid+'.json';old=json.loads(gitbytes(P,p));now=j(p)
    changed=diffs(old,now)
    allowed=['/status','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review']
    assert all(any(x==a or x.startswith(a+'/') for a in allowed) for x in changed),changed
    assert now['status']=='independently_verified'
    assert now['evidence']['independent_verification']==(R/'verified.json').as_posix()
    assert now['evidence']['integration_receipt']==(R/'integration.json').as_posix()
    for label,b in [('proof-before',gitbytes(P,p)),('shared-current',Path(p).read_bytes())]:
        dest=R/('reviewer.repository.'+cid+'.'+label+'.raw.snapshot.json');dest.write_bytes(b)
    checks.append({'name':'bounded_cell_independent_integration_admin','cell':cid,'fields':changed,'current':desc(p)})
for p in [x['path'] for x in math['frozen_production_files']]:
    assert gitbytes(P,p).replace(b'\r\n',b'\n')==gitbytes(C,p).replace(b'\r\n',b'\n'),p
for slug in plan['slugs']:
    for folder in ['publications','declaration_lessons']:
        p='website/content/'+folder+'/'+slug+'.json'
        assert gitbytes(P,p).replace(b'\r\n',b'\n')==gitbytes(C,p).replace(b'\r\n',b'\n'),p
        paths.add(p)
sys.path.insert(0,'website/scripts')
import publication_reader as reader
graphpath=Path('_site/data/underlying-lean-graph.json');graph=j(graphpath)
assert graph['publication_inputs_sha256']==reader.graph_input_digest()
ids={x['id'] for x in graph['nodes']}
assert all('decl:'+d in ids for d in plan['mathematical_declarations'])
assert all(e in graph['edges'] for edges in integration['structural_branches'].values() for e in edges)
snapshot=R/'reviewer.repository.underlying-lean-graph.raw.snapshot.json';snapshot.write_bytes(graphpath.read_bytes())
sitepath=Path('_site/data/site-data.json');site=j(sitepath);stamp=site['git']
assert stamp['commit']==P and stamp['dirty_files'] and stamp['commit_published'] is False
site_snap=R/'reviewer.repository.site-data.raw.snapshot.json';site_snap.write_bytes(sitepath.read_bytes())
checks.append({'name':'shared_root_Registry_actual_consumer','normalized_Lean_delta':shared_rows,'Registry_count':476,'four_new_imports_actual':True})
checks.append({'name':'independent_root_integration_evidence','receipt':desc(R/'integration.json'),'root_logs':rootlogs,'source_proof_parent':P,'root_prospective_tree_at_gate':True,'fresh_current_commit_gate_supersedes_prospective_stamp':True})
checks.append({'name':'current_official_graph_and_static_reader','graph':desc(graphpath),'snapshot':desc(snapshot),'publication_input_digest':graph['publication_inputs_sha256'],'node_count':len(graph['nodes']),'edge_count':len(graph['edges']),'two_target_nodes_and_actual_import_edges':True,'site_snapshot':desc(site_snap),'generated_site_git_commit':stamp['commit'],'generated_site_dirty_file_count':len(stamp['dirty_files']),'commit_published':False,'site_scope':'Root static site build/check reused with exact log hashes and current graph freshness. Precommit proof-parent plus dirty prospective tree, not a clean shared-head/public/live stamp. Untracked future33 paths in stamp are observability only, excluded from packet32 proof. No rendered or Copy/Download interaction QA.'})
paths.update(p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
paths.add((R/'integration.json').as_posix());paths.add((R/'verified.json').as_posix())

tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C],text=True).splitlines())
requested=sorted(paths & tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
out,_=proc.communicate(('\n'.join(C+':'+p for p in requested)+'\n').encode());assert proc.returncode==0
off=0;gitrows=[]
for p in requested:
    end=out.index(b'\n',off);size=int(out[off:end].split()[-1]);off=end+1;blob=out[off:off+size];off+=size+1;raw=Path(p).read_bytes()
    immutable=p.startswith(R.as_posix()+'/') or '.snapshot.' in p or '.raw.snapshot' in p
    if immutable:assert blob==raw,(p,'raw Git freeze')
    else:assert blob.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n'),(p,'LF Git freeze')
    gitrows.append({**desc(p),'git_blob_sha256':sha(blob),'mode':'raw-exact' if immutable else 'LF-exact'})
checks.append({'name':'current_Git_raw_LF_union','checked_commit':C,'count':len(gitrows),'inputs':gitrows,'external_Mathlib_pins':[desc(p) for p in sorted(paths) if p.startswith('.lake/packages/mathlib/')]})
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
pub.check_advance(plan['mathematical_declarations'],reviewed=True)
gates=j(R/'reviewer.repository.gates.json');assert gates['checked_commit']==C;assert all(x['returncode']==0 for x in gates['results'])
log=(R/'reviewer.exact.focused.log').read_text(encoding='utf-8');axioms=[]
for name,values in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
    a={x.strip() for x in values.split(',')};assert a=={'propext','Classical.choice','Quot.sound'};axioms.append({'declaration':name,'axioms':sorted(a)})
assert len(axioms)==5
assert advance.current_advances()[A]['state']=='VERIFIED'
for row in gates['results']:assert desc(row['path'])['raw_sha256']==row['raw_sha256']
aggregate=(R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8');assert 'ASTIS check passed' in aggregate and '9137 jobs' in aggregate and '9404 jobs' in aggregate
report={'schema_version':1,'artifact_kind':'independent-repository-ProofSeal-checks','verifier_id':V,'verified_commit':C,'verification_status':'passed-scoped','checks':checks,'gates':gates,'reachable_axioms':axioms,'scope':'Only actual positive Gaussian relative density, C2/L2 square-root and entropy/log-gradient/Fisher-quarter domains; genuine same-p standardized RGO for all positive variable eta. No weak Sobolev/KL representative, LSI/T2, FIRST4.6/W2/bias/main/cost/composition.','read_lease':'OPEN until repository receipt and CLOSED lease; no state transition','compiler_lease':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.repository.checks.json';dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'verified_commit':C,'verification_status':'passed-scoped','receipt':dest.as_posix(),'raw_sha256':sha(dest.read_bytes()),'Git_input_count':len(gitrows),'source_inputs':[x['input_artifacts'] for x in sources],'closure_modules':len(closure),'whole_fake_scan_files':len(astis.lean_source_files()),'standard_axiom_declarations':len(axioms)},ensure_ascii=False))
