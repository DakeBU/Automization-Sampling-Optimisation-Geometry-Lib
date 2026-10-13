from pathlib import Path
import json,hashlib,os,datetime,re
ROOT=Path('E:/Samplinglib'); OWN=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68/independent-header-source68'; PRE=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68'; OLD=ROOT/'runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/independent-primary67'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def write(n,o):(OWN/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
files=[PRE/f for f in ['draft68.json','header0-expanded.lean','header1-expanded.lean','header2-expanded.lean','statement1.definition.lean','statement2.definition.lean']]
files += sorted((PRE/'alpha-renaming-weight68').iterdir())
entries=[]
for i,p in enumerate(files):
 assert p.is_file();b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');r=f'inputs/header{i:02d}.RAW.snapshot';l=f'inputs/header{i:02d}.LF.snapshot';(OWN/r).write_bytes(b);(OWN/l).write_bytes(lf)
 entries.append({'path':p.relative_to(ROOT).as_posix(),'raw_snapshot':r,'raw_bytes':len(b),'raw_sha256':sha(b),'lf_snapshot':l,'lf_bytes':len(lf),'lf_sha256':sha(lf)})
write('header-inputs.manifest.json',{'schema':1,'phase':'candidate-after-source-first-freeze','pid':os.getpid(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entries':entries})
lease=json.loads((OLD/'lease.final.json').read_text());manifest=json.loads((OLD/'owned-manifest.json').read_text());oldrun=json.loads((OLD/'review-run.json').read_text());logical={k:v for k,v in oldrun.items() if k!='run_sha256'}
assert lease['status']=='CLOSED_LAST';assert len(list(OLD.rglob('*')))>0
for e in manifest['regular_file_entries']:
 b=(OLD/e['name']).read_bytes(); assert len(b)==e['RAW_bytes']; assert sha(b)==e['RAW_sha256']; assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==e['LF_sha256']
assert sha((OLD/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']; assert len([p for p in OLD.rglob('*') if p.is_file()])==lease['owned_file_count']==59
assert sha(canon(logical))==oldrun['run_sha256']==lease['whole_logical_run_sha256']
assert all(p.stat().st_mtime_ns <= (OLD/'lease.final.json').stat().st_mtime_ns for p in OLD.rglob('*') if p.is_file())
primary=(ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();regions=json.loads((OLD/'source-input-regions.json').read_text())
for e in regions['regions']:
 a,z=e['source_RAW_range_end_exclusive'];b=primary[a:z];assert len(b)==e['RAW_bytes'];assert sha(b)==e['RAW_sha256']
coverage=json.loads((OLD/'source-coverage-inventory.json').read_text());assert coverage['count']==len(coverage['math_items'])==344;assert coverage['all_classified'];assert coverage['missing_items']==[];assert coverage['missing_alttext']==coverage['missing_annotation']==coverage['annotation_mismatch']==0
write('reused-primary67.closed-validation.json',{'status':'EXACT_CLOSED59_SOURCE_GRAPH_AND344_ITEM_COVERAGE_REUSED','pid':os.getpid(),'closed_owned_count':59,'whole_logical_run_sha256':oldrun['run_sha256'],'complete_raw_source_decision_sha256':sha((OLD/'primary-source-decision.json').read_bytes()),'whole_primary_raw_sha256':sha(primary),'six_primary_regions_independently_RAW_verified':True,'exact_coverage_count':344,'math_items_added_or_removed':False,'whole_paper_source_coverage_claim':False,'source_graph_before_candidate67':True,'candidate67_final_source_verdict_read':False})
comparisons=[]
for n in [1,2]:
 h=(PRE/f'header{n}-expanded.lean').read_text(encoding='utf8');d=(PRE/f'statement{n}.definition.lean').read_text(encoding='utf8');hb=h.split('    let μ :=',1)[1];db=d.split('    let μ :=',1)[1]
 hp=h.split('theorem ',1)[1].split('\n',1)[1].split('    let μ :=',1)[0];dp=d.split('private def ',1)[1].split('\n',1)[1].split('    let μ :=',1)[0]
 assert hp.rstrip().endswith(':');hp=hp.rstrip()[:-1]; assert dp.rstrip().endswith(': Prop :=');dp=dp.rstrip()[:-len(': Prop :=')]
 assert re.sub(r'\s+','',hp)==re.sub(r'\s+','',dp);assert hb.rstrip()==db.rstrip()
 comparisons.append({'header':f'header{n}-expanded.lean','definition':f'statement{n}.definition.lean','binder_token_equality_ignoring_whitespace':True,'complete_literal_proposition_body_equality_after_trailing_whitespace':True,'raw_body_equal':hb==db,'header_trailing_newline_count':len(hb)-len(hb.rstrip('\n')),'definition_trailing_newline_count':len(db)-len(db.rstrip('\n')),'definition_kind':'literal-full-Prop-value','public_premises_added':False,'provider_proof_credit':False,'fallback_or_default_semantics':False})
alpha=json.loads((PRE/'alpha-renaming-weight68/applied.json').read_text());am=[]
for e in alpha['maps']:
 b=(PRE/'alpha-renaming-weight68'/e['before_snapshot']).read_bytes();a=(PRE/'alpha-renaming-weight68'/e['after_snapshot']).read_bytes();assert sha(b)==e['before_raw_sha256'];assert sha(a)==e['after_raw_sha256'];assert a==(ROOT/e['path']).read_bytes();assert b.count('ω'.encode())==6;assert a==b.replace('ω'.encode(),b'omegaWeight');am.append({'path':e['path'],'before_raw_sha256':sha(b),'after_raw_sha256':sha(a),'exact_six_identifier_replacements_only':True,'source_mathematical_repair':False})
write('definition-and-alpha-map.audit.json',{'status':'EXACT_LITERAL_PROP_AND_ALPHA_RENAMING_ACCEPTED_FOR_HEADER_ONLY','pid':os.getpid(),'literal_definitions':comparisons,'finite_alpha_maps':am,'draft68_initial_header2_hash_is_historical_not_current':True,'statement2_extra_final_empty_line_only_is_semantically_inert':True,'fresh_compilation_claimed':False})
print('FREEZE_AND_SOURCE_VALIDATION_EXIT_0',os.getpid(),len(entries));print(json.dumps(comparisons,ensure_ascii=False,indent=2));print('oldrun',oldrun['run_sha256']);print('coverage_schema',coverage['schema']);print('coverage_first',json.dumps(coverage['math_items'][0],ensure_ascii=False)[:1200]);print('region_counts',[(e['name'],e['math_count']) for e in regions['regions']])
