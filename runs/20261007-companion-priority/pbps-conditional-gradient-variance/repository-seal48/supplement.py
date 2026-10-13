import json,hashlib,subprocess,html,re,datetime
from pathlib import Path
r=Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance';out=run/'repository-seal48';expo=run/'exposition-seal48';commit='79efd28ca8827742e690529f8c763a7bce9b054a';prior='8d950c37e41bd5d816c4132c6a5cdde0e30dcbee'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
assert git('rev-parse','HEAD').decode().strip()==commit
old=read(run/'reviewer.exact.bindings.json');pre=read(run/'reviewer.exact.precompiler.json');locals=[]
for pin in pre['recursive_local_imports63']:
 d=bind(r/pin['path']);assert all(d[k]==pin[k] for k in ['raw_sha256','lf_sha256']);locals.append(d)
assert len(locals)==63
api=[]
for pin in old['Mathlib_API_fragments']:
 p=Path(pin['path']);b=p.read_bytes();a,z=pin['span'];fragment=b''.join(b.splitlines(keepends=True)[a-1:z]);assert H(b)==pin['whole_raw_sha256'] and H(LF(b))==pin['whole_lf_sha256'];assert H(fragment)==pin['fragment_raw_sha256'] and H(LF(fragment))==pin['fragment_lf_sha256'];api.append(pin)
assert len(api)==8
parentleases=[]
for x in old['actual_closed_parent_leases']:
 p=r/x['binding']['path'];d=bind(p);assert all(d[k]==x['binding'][k]for k in ['bytes','raw_sha256','lf_sha256']);assert read(p)['status']=='CLOSED';parentleases.append(d)
# Source-plan exact Git portability + honest original negative: each file remains its producer's raw schema.
plan=run/'four-paper-source-plan-review48';planfiles=[]
for p in plan.rglob('*'):
 if p.is_file():
  rel=str(p.relative_to(r)).replace('\\','/');b=p.read_bytes();blob=git('show',commit+':'+rel);assert blob in (b,LF(b)),rel;planfiles.append(bind(p))
oldfront= json.loads(git('show',prior+':website/content/samplewiki_companion_frontiers.json'));newfront=read(r/'website/content/samplewiki_companion_frontiers.json')
assert len(oldfront['sources'])==3 and len(newfront['sources'])==4
assert all(newfront['sources'][k]==v for k,v in oldfront['sources'].items())
assert all(x==next(y for y in newfront['cases']if y['id']==x['id'])for x in oldfront['cases'])
assert oldfront['composition']==newfront['composition'] and oldfront['setting']==newfront['setting']
newcase=next(x for x in newfront['cases']if x['id']=='ASTIS-SW-MIDPOINT-2026');assert newcase['status']=='planned'
cellp='research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-variance.json';before=json.loads(git('show',prior+':'+cellp));after=read(r/cellp);changedcell=[k for k in set(before)|set(after)if before.get(k)!=after.get(k)]
assert set(changedcell)=={'status','evidence','blocked','purification'}
assert after['status']=='independently_verified';assert 'serialized_shared_gate' in after['evidence'];serialized=after['evidence']['serialized_shared_gate']
# Static exact original companion declaration unit contains all authored six formulas and authored source/test/residual text.
lesson=read(r/'website/content/declaration_lessons/pbps-conditional-gradient-variance.json')['units'][0];decl=lesson['declaration'];page=r/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';txt=page.read_text('utf-8');start=txt.index('data-authored-declaration="'+decl+'"');end=txt.index('</article>',start);article=html.unescape(txt[start:end]);assert len(lesson['steps'])==6
for step in lesson['steps']:assert step['formula'] in article,step['title']
for f in ['formula','lean_statement','lean_proof']:assert lesson[f] in article,f
for x in lesson['sources']:assert x['url'] in article
assert 'Tests.ProximalBPSConditionalGradientVariance' in article
assert 'variance_nonneg' in article
cdp=read(run/'visual-inspection48/cdp.capture.json');pbps=next(x for x in cdp['records'] if x['label']=='pbps');branch=next(x for x in cdp['records'] if x['label']=='branch');assert pbps['closedLeanDetails']==11 and pbps['mathContainers']==8;assert cdp['ownedBrowserExit']['code']==0
observations={'actual_images_independently_viewed':['cli.overview.png','cli.pbps.png','cli.branch.png','cdp.pbps.png','cdp.branch.png'],'accepted_actual_desktop_scope':'Readable pointwise48 conditions and correct quarter-coefficient formula in controlled CDP screenshot; exact48 selected compiled declaration/source locator; overview four fixed papers/three planned routes with dashed interfaces and distinct deterministic-upper/randomized-lower lanes.','retained_negative':'Original CLI PBPS screenshot is blank despite successful capture process/rendered DOM; it contributes no visual success.','limitations':['CDP viewport shows conditions/main formula and opening roadmap, not all six proof steps as pixels; six formulas and exact full production body are statically checked.','Graph remains dense and selected sidebar wraps; no exhaustive elaborated declaration-dependency certificate.','Name-scanned LogConcavity.LogConcaveOn.prod edge is an incomplete lexical match, not claimed as an actual proof parent.','Local source-state Lean gate banner is not a current79 gate stamp; actual root9151/Tests9431 compiled scientific bytes are separately bound.','Existing lesson boundary prose still says reviews/shared admission pending; immutable original source metadata is not silently rewritten to current state.','Full inline imports/direct Test links/copy-download-bundle/browser interaction/mobile/fullreader/main-live/PURIFIED acceptance not established.'],'browser_this_reviewer':'NOT_STARTED_CLOSED; existing isolated capture lifecycle receipt reports exit0; actual image files viewed without browser process','static_six_formula_steps':6,'closed_disclosures_recorded':11,'math_containers_recorded':8,'full_standalone_source_imports_and_both_Test_theorems':'PASS_EXACT_SOURCE_BYTES_FROM_MAIN_BINDINGS','source_only_midpoint_plan':'No new Lean method kernel/invariant/complexity/transport certificate; source representation overlay only.'}
result={'checked_commit':commit,'strict_current_local63':locals,'strict_Mathlib8_actual_whole_fragment_spans':api,'actual_parent_leases_CLOSED_unchanged':parentleases,'planned_source_review_all_currentGit_rawLF':planfiles,'metadata_projection':{'frontiers':'3 existing source objects and case objects, common setting and two-source composition exactly unchanged; fourth planned source/case and authorized execution priority append.','cell_changed_top_fields':changedcell,'cell_serialized_shared_gate':serialized,'generator':'Original48 authored lesson/publication and exact production/Test unchanged; source-only fourthpaper planned reader generation reviewed separately.','historical_old_frontiers_and_generator':'Original8d Git blobs remain prior reviewed inputs; current79 source-plan projection is explicitly additional administrative/source-only scope, not unchanged-science waiver.'},'static_exposition_observations':observations}
dump(out/'supplement.bindings.json',result);dump(expo/'observations.json',observations)
print(json.dumps({'local63':len(locals),'Mathlib8':len(api),'closedparents':len(parentleases),'planGitfiles':len(planfiles),'six_formulas':'PASS','original3cases_composition_setting':'UNCHANGED','cell_admin_top_fields':changedcell,'actual_capture11details8math':'PASS'}))
