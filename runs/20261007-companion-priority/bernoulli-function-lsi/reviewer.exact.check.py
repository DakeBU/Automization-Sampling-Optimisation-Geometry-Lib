from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime
sys.path.insert(0, 'tools')
import astis_publication as pub, astis, astis_advance as advance
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi')
C='a83ce789bd4f3ce22c3757129282c9ad488c2ccf'
V='picard_commit_verifier_20261005'
def j(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def desc(p):
    b=Path(p).read_bytes()
    return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def diff(a,b,p=''):
    if type(a)!=type(b): return [p]
    if isinstance(a,dict): return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
    if isinstance(a,list): return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [p]
paths=set(); checks=[]; admin=[]
def bind(row,p=None):
    actual=desc(p or row['path'])
    assert actual['raw_sha256']==row['raw_sha256'],actual['path']
    assert actual['lf_sha256']==row['lf_sha256'],actual['path']
    if 'bytes' in row: assert actual['bytes']==row['bytes'],actual['path']
    paths.add(actual['path']); return actual
def frozen(rows,admin_allowed=False):
    for row in rows:
        if 'raw_snapshot' in row: bind(row,row['raw_snapshot'])
        if 'lf_snapshot' in row:
            assert sha(Path(row['lf_snapshot']).read_bytes())==row['lf_sha256']; paths.add(row['lf_snapshot'])
        if desc(row['path'])['raw_sha256']==row['raw_sha256']: bind(row); continue
        assert admin_allowed and 'raw_snapshot' in row, row['path']
        fields=diff(j(row['raw_snapshot']),j(row['path']))
        if '/semantic-roundtrip/audits/' in row['path']: allowed=['/state','/semantic_slots','/deltas','/verdict','/source_review']
        elif '/frontier-cells/' in row['path']: allowed=['/status','/evidence/execution_boundary','/evidence/metadata_overlay_review','/evidence/proof_review','/evidence/source_review']
        else: raise AssertionError(('unexpected footprint drift',row['path'],fields))
        assert all(any(f==a or f.startswith(a+'/') for a in allowed) for f in fields),fields
        paths.add(row['path']);admin.append({'path':row['path'],'before_snapshot':row['raw_snapshot'],'before_raw_sha256':row['raw_sha256'],'current':desc(row['path']),'allowed_admin_fields':fields})
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
claim=j(R/'claim.json');A=claim['advance_id'];plan=j(R/'publication-plan.json');proved=j(R/'proved-local.json')
decls=plan['mathematical_declarations']
assert decls==proved['lean_declarations']==proved['publication_declarations'] and len(decls)==2
freeze=j(R/'math-freeze.json'); frozen(freeze['inputs']);assert len(freeze['inputs'])==14
whole=j(R/'whole-proof-review/reviewer.math.review.json')
assert whole['independent_from_proof_writer'] and whole['verdict']=='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF' and not whole['blockers'] and whole['standard3_only']
counts={}
for name in ['inputs.frozen.json','api-inputs.frozen.json','direct-parent-inputs.frozen.json']:
    rows=j(R/'whole-proof-review'/name)['inputs'];frozen(rows);counts[name]=len(rows)
for name,review in [('whole-proof-review/reviewer.math.run.json','whole-proof-review/reviewer.math.review.json'),('dependency-metadata-overlay1/reviewer.overlay1.run.json','dependency-metadata-overlay1/overlay1.review.json')]:
    run=j(R/name)
    assert pub.digest({k:v for k,v in run.items() if k not in {'hash_recipe','deterministic_run_sha256'}})==run['deterministic_run_sha256']
    assert desc(R/review)['raw_sha256']==run['review_raw_sha256']
    for row in run['artifacts']:bind(row)
overlay=j(R/'dependency-metadata-overlay1/overlay1.review.json')
assert overlay['whole_math_review_still_valid'] and overlay['independent_from_overlay_author'] and overlay['independent_from_repair_requester'] and not overlay['blockers'] and not overlay['blocking']
frozen(j(R/'dependency-metadata-overlay1/reviewer.overlay1.inputs.json')['inputs'],True)
for slug in plan['slugs']:
    before=R/'dependency-metadata-overlay1'/(slug+'.before.raw.snapshot.json')
    after=Path('website/content/declaration_lessons')/(slug+'.json')
    assert diff(j(before),j(after))==['/units/0/mathlib_dependencies']
for seal in j(R/'preproof/statement-seals.accepted.json')['signatures']:
    bind(seal['portable_signature'])
    text=Path(seal['file']).read_text(encoding='utf-8')
    assert seal['signature_text'].rstrip()+' := by' in text
    assert sha(seal['signature_text'].encode())==seal['signature_lf_sha256']
checks.append({'name':'exact_whole_math_and_signature_chain','math_freeze_inputs':14,'whole_review_inputs':counts,'whole_math_review':desc(R/'whole-proof-review/reviewer.math.review.json'),'metadata_only_overlay':desc(R/'dependency-metadata-overlay1/overlay1.review.json'),'two_public_signed_scalar_and_actual_cube_proofs':'Original complete all-body mathematical review reused only after exact raw/LF files, pinned APIs and proof/signature identity. Local independent examination checks zero branches, signed difference, true finite measure/full flip, RMS induction, exact half and genuine test consumers. No Han dependency supplied.'})
data=pub.inputs();items={x['id']:x for x in pub.load()};sources=[]
blindrun=j(R/'anonymous-decoder/run.json')
assert pub.digest(blindrun['deterministic_run_basis'])==blindrun['decoder_run_sha256']
assert not blindrun['compiler_started'] and not blindrun['source_text_visible'] and blindrun['status']=='CLOSED'
for row in blindrun['input_artifacts']+blindrun['result_artifacts']: bind(row,R/'anonymous-decoder'/Path(row['path']).name)
mapping=[]
for i,decl in enumerate(decls):
    aid=plan['audit_ids'][i];a=data['audits'][aid];item=items[plan['slugs'][i]]
    binding=next(b for b in item['bindings'] if b['declaration']==decl)
    packet=j(R/f'source.{i}.reviewer-packet.overlay1.json');review=j(R/f'source.{i}.review.overlay1.json')
    assert pub.digest({k:v for k,v in review.items() if k!='review_run_sha256'})==review['review_run_sha256']==a['source_review']['review_run_sha256']
    assert pub.digest({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==review['reviewer_packet_sha256']==a['source_review']['reviewer_packet_sha256']
    assert a['state']=='accepted' and a['source_review']['state']=='accepted'
    assert review['verdict']=='equivalent-after-elaboration' and not review['blocking'] and not review['deltas'] and not review['repairs'] and not review['source_assumption_delta'] and review['source_excess']==0
    assert review['independent_from_formalizer'] and review['independent_from_decoder'] and review['reviewer']!=V
    assert set(review['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
    assert pub.binding_digest(item,binding,data)==a['publication_binding_sha256']==packet['publication_binding_sha256']==review['publication_binding_sha256']
    assert pub.review_context(item,binding,data)==packet['candidate_publication_context']
    assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']==review['source_text_sha256']
    assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']==review['lean_statement_sha256']
    module=desc(packet['lean']['file'])
    assert module['raw_sha256']==review['whole_module_raw_sha256'] and module['lf_sha256']==review['whole_module_lf_sha256']==review['whole_module_file_sha256']
    assert review['whole_module_covered'] and review['all_private_helpers_covered']
    blind=j(R/f'anonymous-decoder/result{i}.json');bp=j(R/f'anonymous-decoder/packet{i}.json')
    assert blind['source_text_visible'] is False and bp['packet_sha256']==review['decoder_packet_sha256']==packet['blind_reconstruction']['decoder_packet_sha256']
    assert blind['decoder_run_sha256']==blindrun['decoder_run_sha256']==review['decoder_run_sha256']==a['reconstruction']['decoder_run_sha256']
    assert sha(blind['reconstructed_theorem_text'].encode())==blind['reconstructed_text_sha256']==review['reconstructed_text_sha256']==packet['blind_reconstruction']['text_sha256']==a['reconstruction']['text_sha256']
    assert blind['reconstructed_theorem_text']==packet['blind_reconstruction']['text']==a['reconstruction']['text']
    original=j(review['original_full_review']['path']);assert original['status']=='BLOCKED' and original['blocking']
    assert desc(review['original_full_review']['path'])['raw_sha256']==review['original_full_review']['raw_lf_sha256']
    assert pub.digest({k:v for k,v in original.items() if k!='review_run_sha256'})==original['review_run_sha256']==review['original_full_review']['review_run_sha256']
    rows=[]
    for k,row in enumerate(review['input_artifacts']):
        row=dict(row);row['raw_snapshot']=(R/'source.overlay1.review.inputs'/f'{k:03}.raw.snapshot').as_posix();rows.append(row)
    frozen(rows,True)
    cells=[c for c in data['cells'].values() if c['cell_id'] in plan['active_cells'] and c['shared_floor_audit']['canonical_declaration']==decl]
    assert len(cells)==1 and cells[0]['status']=='proved_locally'
    mapping.append({'declaration':decl,'cell_id':cells[0]['cell_id'],'audit_id':aid,'binding':packet['publication_binding_sha256']})
    sources.append({'review':desc(R/f'source.{i}.review.overlay1.json'),'review_run_sha256':review['review_run_sha256'],'packet':desc(R/f'source.{i}.reviewer-packet.overlay1.json'),'packet_sha256':packet['packet_sha256'],'binding_sha256':packet['publication_binding_sha256'],'source_input_count':len(rows),'whole_module_lines':review['whole_module_lines'],'private_helpers':len(review['private_declarations']),'lesson_steps':review['lesson_step_count'],'original_BLOCKED_preserved':desc(review['original_full_review']['path'])})
pub.check_advance(decls,reviewed=True)
checks.append({'name':'current_source_and_fresh_portable_blind','sources':sources,'cell_mapping_by_canonical_declaration':mapping,'decoder_run_sha256':blindrun['decoder_run_sha256'],'publication_reviewed':True,'administrative_only_drifts':admin})
TP=Path('runs/20261007-companion-priority/bernoulli-lsi-source-graph-review/source-topology-review.json')
MP=TP.with_name('conceptual-mirror-review.json')
top=j(TP);mirror=j(MP)
for obj in [top,mirror]:
    assert pub.digest({k:v for k,v in obj.items() if k!='review_run_sha256'})==obj['review_run_sha256']
    assert obj['independent_from_formalizer'] and not obj['blocking'] and not obj['deltas'] and not obj['repairs']
assert top['independent_from_graph_author'] and top['source_only'] and top['verdict']=='accepted-scoped'
assert desc(top['review_target'])['raw_sha256']==top['review_target_raw_sha256'];paths.add(top['review_target'])
assert mirror['independent_from_creator'] and mirror['verdict']=='accepted-scoped-conceptual-only'
discovery=advance.current_discoveries()['ASTIS-DISC-20261007-BernoulliGaussianEntropyEnergyMirror']
assert discovery['status']=='validated' and discovery['latest_actor']==mirror['reviewer'] and discovery['created_by']!=mirror['reviewer']
checks.append({'name':'independent_source_topology_and_conceptual_only_admission','topology_review':desc(TP),'coverage':top['coverage'],'mirror_review':desc(MP),'discovery_id':discovery['discovery_id'],'discovery_status':discovery['status'],'no_formal_transport_edge':True})
paths.update([TP.as_posix(),MP.as_posix()])
closure=set()
def visit(p):
    if p in closure:return
    closure.add(p);paths.add(p)
    for n in re.findall(r'^import\s+((?:AutoSamplingTheory|Tests)\.[\w.]+)',Path(p).read_text(encoding='utf-8'),re.M):
        q=n.replace('.','/')+'.lean'
        if Path(q).exists():visit(q)
for p in proved['lean_files']:visit(p)
fake=[]
for p in sorted(closure):
    for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf-8')).splitlines(),1):
        if astis.FORBIDDEN_REGEX.search(line):fake.append({'path':p,'line':n,'text':line.strip()})
assert not fake and not astis.forbidden_pattern_hits()
checks.append({'name':'fresh_fake_closure','reachable_modules':len(closure),'reachable_hits':fake,'canonical_files':len(astis.lean_source_files()),'canonical_hits':[],'reachable_inputs':[desc(p) for p in sorted(closure)]})
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
paths.update(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C],text=True).splitlines());selected=sorted(paths&tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
out,_=proc.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert proc.returncode==0
offset=0;gitrows=[]
for p in selected:
    end=out.index(b'\n',offset);size=int(out[offset:end].split()[-1]);offset=end+1;blob=out[offset:offset+size];offset+=size+1;live=Path(p).read_bytes()
    raw=p.startswith('runs/') or '.snapshot' in p
    assert (blob==live if raw else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),(p,'Git mismatch')
    gitrows.append({**desc(p),'git_blob_sha256':sha(blob),'mode':'raw-exact' if raw else 'LF-exact'})
checks.append({'name':'exact_Git_current_raw_LF','checked_commit':C,'count':len(gitrows),'inputs':gitrows})
gates=j(R/'reviewer.exact.gates.json');assert len(gates['results'])==8 and gates['checked_commit']==C
for row in gates['results']:bind(row)
assert [(r['name'],r['returncode']) for r in gates['results'] if r['returncode']]==[('contributor',1)]
failure=(R/'reviewer.exact.contributor.log').read_text(encoding='utf-8')
assert failure.count('functor none-found must match conceptual_mirror_audit')==2
axioms=[]
for name,vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(encoding='utf-8'),re.S):
    values={x.strip() for x in vals.split(',')};assert values=={'propext','Classical.choice','Quot.sound'};axioms.append({'declaration':name,'axioms':sorted(values)})
assert len(axioms)==6
assert advance.current_advances()[A]['state']=='PROVED_LOCAL'
report={'schema_version':1,'verification_status':'rejected-metadata-admission','checked_commit':C,'advance_id':A,'verifier_id':V,'checks':checks,'gates':gates,'axioms':axioms,'focused_jobs':2653,'existing_root_aggregate_jobs':[9138,9406],'new34_shared_imports_not_claimed':True,'typed_blocker':{'class':'contributor-cell-conceptual-mirror-metadata-inconsistency','exact_diagnostic':'Both graph_contribution.functor_view are none-found while conceptual_mirror_audit.status is candidates-published with an independently validated conceptual mirror. Contributor --base origin/main rejects both declarations.','cells':plan['active_cells'],'canonical_inputs_not_repaired_by_verifier':True},'VERIFIED_transition_published':False,'preserved_original_BLOCKED_source_receipts':True,'remaining_boundary':['Genuine signed two-point and actual finite Boolean function LSI only, exact coefficient one half, all n including zero.','Gaussian CLT law, actual entropy/full-flip energy limits, Gaussian LSI/noncompact/finite-dimensional adapters and T2/FIRST4.6/W2/bias/paper main/work/composition remain open.','Shared integration/repository ProofSeal/ExpositionSeal/current remote CI remain separate.'],'leases':{'compiler':'CLOSED','Python':'CLOSED','read':'CLOSED','write':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.exact.failed-admission.json';assert not dest.exists();dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
closed={'status':'CLOSED','checked_commit':C,'verifier_id':V,'compiler':'CLOSED','Python':'CLOSED','read':'CLOSED','write':'CLOSED','receipt':desc(dest),'no_VERIFIED_transition':True,'canonical_mutations':[]}
(R/'reviewer.exact.lease.closed.json').write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'receipt':desc(dest),'Git_inputs':len(gitrows),'source_inputs':[len(j(R/f'source.{i}.review.overlay1.json')['input_artifacts']) for i in range(2)],'closure_modules':len(closure),'canonical_fake_files':len(astis.lean_source_files()),'leases':'CLOSED','status':report['verification_status']}))
