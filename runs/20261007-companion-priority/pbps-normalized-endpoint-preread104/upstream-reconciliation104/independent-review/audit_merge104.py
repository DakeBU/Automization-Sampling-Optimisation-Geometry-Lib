from pathlib import Path
import hashlib,json,subprocess,ast,sys,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
OURS='68b21db4010afe302dbdca732c9e86ef41cb2609';THEIRS='4aded42f2fcf72a79b3e761a108cdab6d248adaf'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
pre=load(B/'premerge.json');resolution=load(B/'resolution104.json');mr=load(B/'merge-result.json')
assert git('rev-parse','HEAD').decode().strip()==OURS and git('rev-parse','MERGE_HEAD').decode().strip()==THEIRS
base=git('merge-base',OURS,THEIRS).decode().strip();assert base==pre['merge_base'] and pre['head']==OURS and pre['upstream']==THEIRS
assert not git('ls-files','-u').strip()
incoming=git('diff','--name-only',base,THEIRS).decode().splitlines();changed=git('diff','--cached','--name-only').decode().splitlines();assert set(incoming)==set(pre['incoming'])==set(changed) and len(changed)==34
conflicts={x['path'] for x in resolution['conflicts']};assert conflicts==set(mr['unmerged'].splitlines()) and len(conflicts)==5
assert not pre['staged'] and not pre['untracked_intersection']
assert not conflicts&{x['path'] for x in pre['dirty_raw']} and not set(incoming)&{x['path'] for x in pre['dirty_raw']}
for x in pre['dirty_raw']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
workrows=[];idx={};views={};snapshotdir=O/'parent-blobs';snapshotdir.mkdir(exist_ok=True)
for i,path in enumerate(changed):
 ib=git('show',':'+path);idx[path]=ib;wb=(R/path).read_bytes();assert wb.replace(b'\r\n',b'\n')==ib,path
 for mark,ref in [('ours',OURS),('base',base),('theirs',THEIRS)]:
  p=subprocess.run(['git','show',ref+':'+path],cwd=R,capture_output=True);bb=p.stdout if p.returncode==0 else b''
  views[(path,mark)]=bb;(snapshotdir/f'{i:02d}.{mark}.snapshot').write_bytes(bb)
 assert not re.search(rb'^(<<<<<<< |=======\r?$|>>>>>>> )',ib,re.M),path
 row=dict(path=path,index_sha256=sha(ib),working_raw_sha256=sha(wb),ours_sha256=sha(views[(path,'ours')]),base_sha256=sha(views[(path,'base')]),theirs_sha256=sha(views[(path,'theirs')]))
 if path not in conflicts:
  ob,bb,tb=[views[(path,k)] for k in ['ours','base','theirs']]
  if ob==bb:expected=tb;method='ours unchanged from common base; exact upstream bytes'
  elif tb==bb:expected=ob;method='upstream unchanged from common base; exact ours bytes'
  elif ob==tb:expected=ob;method='parents identical'
  else:
   cmd=['git','merge-file','-p',str(snapshotdir/f'{i:02d}.ours.snapshot'),str(snapshotdir/f'{i:02d}.base.snapshot'),str(snapshotdir/f'{i:02d}.theirs.snapshot')]
   p=subprocess.run(cmd,cwd=R,capture_output=True);assert p.returncode==0,(path,p.stderr.decode());expected=p.stdout;method='independently replayed clean three-way text merge'
  assert ib==expected,path;row['clean_merge_verification']=method
 workrows.append(row)
for x in resolution['conflicts']:assert info(x['path'])['raw_sha256']==x['resolved_RAW_sha256'],x['path']
# Exact conflict resolutions, each bounded relative to ours.
p='AutoSamplingTheory/TechnicalLemmas/Registry.lean';ours=views[(p,'ours')];up=views[(p,'theirs')].replace(b'\r\n',b'\n')
key=b'    key := "geometry.curve-extension-independence",';pos=up.index(key);start=up.rfind(b'  {\n',0,pos);end=up.index(b'  },\n',pos)+len(b'  },\n');entry=up[start:end]
expected=b'import AutoSamplingTheory.TechnicalLemmas.Geometry.CurveExtension\n'+ours.replace(b'def geometryMemory : List LemmaMemoryEntry := [\n',b'def geometryMemory : List LemmaMemoryEntry := [\n'+entry)
assert idx[p]==expected and idx[p].count(key)==1
p='Tests.lean';assert idx[p]==b'import Tests.Shared.CurveExtension\n'+views[(p,'ours')]
p='Tests/Basic.lean';assert idx[p]==views[(p,'ours')].replace(b'formalizedTechnicalLemmaCount = 553',b'formalizedTechnicalLemmaCount = 554')
assert idx[p].count(b'formalizedTechnicalLemmaCount = 554')==1
p='tools/tests/test_astis_publication.py'
def functions(b):
 return {n.name:ast.get_source_segment(b.decode().replace('\r\n','\n'),n) for n in ast.walk(ast.parse(b.decode())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
of=functions(views[(p,'ours')]);tf=functions(views[(p,'theirs')]);cf=functions(idx[p]);oldname='test_chapter_map_is_mathematical_and_keeps_the_affine_boundary';newname='test_chapter_map_keeps_curve_progress_and_full_source_boundaries';literal='test_literal_proposition_and_proof_helpers_keep_distinct_reader_positions'
assert cf[literal]==of[literal] and cf[newname]==tf[newname] and oldname not in cf
expected=views[(p,'ours')].decode().replace(of[oldname],tf[newname]);assert idx[p].decode()==expected
# The source-authoritative reader auto-merge must preserve our literal-proposition behavior.
reader='website/scripts/publication_reader.py';assert idx[reader]==views[(reader,'theirs')]
# Ledger ours contains legitimate inserted earlier events; test event subsequences, not a false prefix.
p='runs/substantive_advances.jsonl';lb=views[(p,'base')];lo=views[(p,'ours')];lt=views[(p,'theirs')];lm=idx[p]
assert lt.startswith(lb);tail=lt[len(lb):];assert len(tail.splitlines())==8 and lm==lo+tail
def subsequence(a,b):
 it=iter(b);return all(any(x==y for y in it) for x in a)
assert subsequence(lb.splitlines(),lo.splitlines()) and subsequence(lo.splitlines(),lm.splitlines()) and subsequence(lt.splitlines(),lm.splitlines())
events=[json.loads(x) for x in tail.splitlines()];assert {x['advance_id'] for x in events}=={'ANDI-SA-20261012-CurveExtension'}
def states(raw):
 out={}
 for line in raw.splitlines():
  x=json.loads(line);id=x.get('advance_id')
  if not id:continue
  if x.get('event')=='proposal':out[id]=x.get('state')
  elif x.get('event')=='transition':out[id]=x.get('to_state',x.get('to',x.get('state')))
 return out
os=states(lo);ms=states(lm);assert all(ms.get(k)==v for k,v in os.items())
assert 'ASTIS-SA-20261012-PBPSActualPhaseNormalization' in os
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import current_advances
now=current_advances();lane={k:v['owner_id'] for k,v in now.items() if v['state']=='STABILIZING'}
assert lane=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity':'companion_root_20261005'}
assert now['ASTIS-SA-20261012-PBPSActualPhaseNormalization']['state']=='VERIFIED'
# All PBPS103 production/reader/source/decoder paths are unchanged in the merge index.
science103='runs/20261007-companion-priority/pbps-actual-phase-normalization103'
proofpaths=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-normalization.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPhaseNormalization.json','website/content/publications/pbps-actual-phase-normalization.json','website/content/declaration_lessons/pbps-actual-phase-normalization.json']
proofpaths+=git('ls-tree','-r','--name-only',OURS,'--',science103,'runs/semantic-roundtrip/anonymous103','runs/20261007-companion-priority/pbps-phase-normalization-preread103').decode().splitlines()
for p in proofpaths:assert git('rev-parse',OURS+':'+p).strip()==git('rev-parse',':'+p).strip(),p
prepared=load(R/science103/'independent-whole-math103/prepared-inputs103.native.json')
for x in prepared['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
closed=load(R/science103/'exact-commit-verification103/closed-RAW-manifest103.json');collab=closed['preserved_collaborator_inputs'];assert len(collab)==21
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256']
for x in pre['dirty_raw']:assert info(x['path'])['raw_sha256']==x['raw_sha256']
assert git('rev-parse','HEAD').decode().strip()==OURS and git('rev-parse','MERGE_HEAD').decode().strip()==THEIRS and not git('ls-files','-u').strip()
save('merge-resolution-review104.native.json',dict(decision='ACCEPT_BOUNDED_UNCOMMITTED_MERGE_RESOLUTION',reviewer='/root/exact_verifier96',checked_parents=dict(ours=OURS,upstream=THEIRS,common_base=base),checked_index_tree=git('write-tree').decode().strip(),root_inputs=[info(B/n) for n in ['premerge.json','merge-result.json','resolution104.json']],staged_files=workrows,conflict_resolution=dict(registry='Exactly one upstream curve import plus exact upstream entry inserted into ours; every prior PBPS entry retained.',tests='Exactly one upstream CurveExtension test import prepended to ours.',count='Ours553 plus one curve registration equals554; only this literal changed.',publication_tests='Exact ours file with only the old affine-only chapter-map test replaced by upstream updated curve test. Literal-proposition/helper positioning test and full assumptions marker retained byte-for-byte.',ledger='Exact ours Git ledger followed by exact upstream8-event tail; base is a subsequence of ours, both parents are subsequences of result. No prior event overwritten.'),clean_merges=29,source_authoritative_publication_reader='Exact upstream publication_reader.py; explicit source_order sorting incorporated. No generated reader patch used.',all47_prior_dirty_RAWs_preserved=True,dirty_inputs=pre['dirty_raw'],recorded_premerge_untracked_intersection_empty=True,prior_untracked_inventory_not_reconstructed=True,all21_collaborator_RAWs_preserved=True,preserved_collaborator_inputs=collab,PBPS103_index_paths_unchanged=len(proofpaths),PBPS103_kernel_proof_inputs_RAW_unchanged=True,PBPS103_state='VERIFIED',sole_stabilization_lane=lane,upstream_event_count=8,upstream_advance_ids=['ANDI-SA-20261012-CurveExtension'],remaining=['Root aggregate postmerge gates and eventual merge commit','PBPS browser/visual acceptance, main merge and postmerge purification retain their separate status'],no_mathematical_reproof=True,no_shared_edit=True,no_commit=True,no_SAU_transition=True,no_false_PBPS_main_merge_or_purification_claim=True))
save('closed-RAW-review104.native.json',dict(status='CLOSED_INDEPENDENT_BOUNDED_MERGE_RESOLUTION_ACCEPTED',checked_parents=dict(ours=OURS,upstream=THEIRS,common_base=base),inputs=[info(B/n) for n in ['premerge.json','merge-result.json','resolution104.json']],artifacts=[info(p) for p in sorted(O.rglob('*')) if p.is_file()],self_hash_intentionally_omitted=True,no_shared_write_or_commit=True))
for n in ['merge-resolution-review104.native.json','closed-RAW-review104.native.json']:print(json.dumps(info(O/n)),flush=True)
