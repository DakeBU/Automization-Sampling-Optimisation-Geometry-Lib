import copy, hashlib, json, os, sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75/independent-source75'
PRO=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75/review-input-metadata-overlay75/proposal.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def ref(p):
    b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))}
def put(n,v):
    p=OWN/n;p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());return ref(p)
def get(o,p):
    for k in p.strip('/').split('/'):o=o[int(k)] if isinstance(o,list) else o[k]
    return o
def setp(o,p,v):
    keys=p.strip('/').split('/')
    for k in keys[:-1]:o=o[int(k)] if isinstance(o,list) else o[k]
    if isinstance(o,list):o[int(keys[-1])]=v
    else:o[keys[-1]]=v
def diffs(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append(p+'/'+k)
            else:out.extend(diffs(a[k],b[k],p+'/'+k))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [p]
        return sum((diffs(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
    return [] if a==b else [p]
def scan(o,p=''):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k in {'semantic_slots','deltas','verdict','review_run_sha256'}:out.append(p+'/'+k)
            out+=scan(v,p+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):out+=scan(v,p+'/'+str(i))
    return out
def main():
    assert not (OWN/'lease.final.json').exists()
    proposal=load(PRO)
    allowed={
      'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json':['/statement_seal/binder_audit','/source_detail_audit/consulted/0/expanded_binder_audit'],
      'website/content/publications/pbps-actual-hazard-clock.json':['/items/0/statement_seal/binder_audit']
    }
    assert len(proposal['rows'])==2 and proposal['field_count']==3
    (OWN/'overlay-inputs').mkdir(exist_ok=True)
    snaps=[]
    def snapshot(name,p):
        dest=OWN/'overlay-inputs'/(name+'.RAW');dest.write_bytes(p.read_bytes())
        lf=OWN/'overlay-inputs'/(name+'.LF');lf.write_bytes(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n'))
        snaps.append({'name':name,'origin':ref(p),'RAW_snapshot':ref(dest),'LF_snapshot':ref(lf)})
    snapshot('proposal',PRO)
    common=None;rows=[]
    for i,row in enumerate(proposal['rows']):
        path=row['path'];assert path in allowed
        beforep=ROOT/row['before']['path'];afterp=ROOT/row['proposed']['path'];current=ROOT/path
        for p,expected in [(beforep,row['before']),(afterp,row['proposed']),(current,row['current'])]:
            r=ref(p);assert all(r[k]==expected[k] for k in ['RAW_bytes','RAW_sha256','LF_sha256'])
        assert current.read_bytes()==beforep.read_bytes()
        before=load(beforep);after=load(afterp);masked=copy.deepcopy(before)
        assert sorted(c['json_pointer'] for c in row['changes'])==sorted(allowed[path])
        for change in row['changes']:
            pointer=change['json_pointer'];old=get(before,pointer);new=get(after,pointer)
            assert old==change['old'] and new==change['new']
            if common is None:common=new
            assert new==common
            assert new['kind']=='expanded-binder-inventory-only'
            assert len(new['ambient_typing'])==5 and len(new['source_hypotheses'])==6
            assert new['definitions']==8 and new['conclusion_groups']==10
            assert new['extra_public_proof_or_law_providers']==[] and new['unexplained_binders']==[]
            assert [(h['name'],h['classification']) for h in new['source_hypotheses']]==[(x,'SOURCE') for x in ['hα','hαβ','hV','hH','hη','hβη']]
            setp(masked,pointer,new)
        assert masked==after, diffs(masked,after)
        assert not scan(after),scan(after)
        rows.append({'path':path,'before':ref(beforep),'proposed':ref(afterp),'current_equals_before_RAW':True,'exact_changed_fields':allowed[path],'all_other_JSON_equal':True,'complete_recursive_semantic_diff_paths':diffs(before,after),'prior_review_keys_remaining':scan(after),'neutral_inventory_exact':common})
        snapshot(str(i)+'.before',beforep);snapshot(str(i)+'.proposed',afterp)
    checks=[]
    for name,key in [('module','frozen_Lean'),('sealed-header','frozen_header'),('original-official-packet','source_packet_before')]:
        expected=proposal[key];p=ROOT/expected['path'];r=ref(p)
        assert all(r[k]==expected[k] for k in ['RAW_bytes','RAW_sha256','LF_sha256'])
        snapshot(name,p);checks.append({'name':name,'exact_pin':r,'unchanged':True})
    s=load(OWN/'build-state75.json')
    for name,key in [('source-graph','source_graph'),('source-inventory','source_inventory'),('lesson','lesson')]:
        expected=s[key];p=ROOT/expected['path'];assert ref(p)==expected
        checks.append({'name':name,'exact_pin':ref(p),'unchanged':True})
    # Scientific and proof data are outside the three replaced metadata fields.
    pubrow=next(x for x in proposal['rows'] if x['path'].startswith('website/'))
    pb=load(ROOT/pubrow['before']['path'])['items'][0];pa=load(ROOT/pubrow['proposed']['path'])['items'][0]
    protected=['source','statement','assumptions','formulae','obligations','bindings','source_proof_coverage','proof_digestion','purification']
    assert all(pb[k]==pa[k] for k in protected)
    manifest=put('overlay75.input-manifest.json',{'schema':'pbps75-exact-metadata-overlay-inputs/v1','inputs':snaps,'count':len(snaps),'complete_proposal_RAW':ref(PRO)})
    result={'schema':'pbps75-independent-exact-metadata-overlay-review/v1','status':'ACCEPTED_EXACT_THREE_FIELD_METADATA_OVERLAY_ONLY','reviewer':'/root/independent_source75','role':'independent-exact-metadata-overlay-reviewer','actual_PID':os.getpid(),'author':'root-samplinglib-writer','independent_from_proposal_author':True,'authorization':'Parent explicitly authorized independent exact proposal review only, no canonical application. This is separate from the supplemental source review.','proposal_RAW':ref(PRO),'proposal_canonical_sha256':sha(canon(proposal)),'input_manifest':manifest,'field_count':3,'files':2,'rows':rows,'exact_pins':checks,'protected_publication_fields_unchanged':protected,'same_neutral_inventory_in_all_three_fields':True,'Lean_statement_source_formulas_source_topology_coverage_unchanged':True,'canonical_applied_by_reviewer':False,'source_admission_granted':False,'fresh_anti_anchored_source_reviewer_required':True,'mathematical_repair':False,'source_repair':False,'VERIFIED':False,'PROVED_LOCAL':False,'Goal_complete':False,'blocking_deltas':[],'truth_boundary':'Accept only the exact proposed metadata replacement at these pins. This repairs review input exposure, supplies no mathematical theorem or source-fidelity admission, and cannot validate the already exposed supplemental reviewer as anti-anchored.'}
    result['decision_sha256']=sha(canon(result))
    decision=put('overlay75.decision.json',result)
    run={'schema':'pbps75-independent-exact-overlay-native-run/v1','actor':'/root/independent_source75','actual_PID':os.getpid(),'activity':'exact-three-field-metadata-review','decision':decision,'input_manifest':manifest,'observed_assertions_PASS':True,'terminal_exit_must_be_observed_separately':True,'no_canonical_mutations':True}
    run['run_sha256']=sha(canon(run));runref=put('overlay75.run.json',run)
    print(json.dumps({'status':result['status'],'actual_PID':os.getpid(),'decision':decision,'run':runref,'native_run_sha256':run['run_sha256'],'proposal_RAW':result['proposal_RAW'],'field_count':3,'files':2},ensure_ascii=False))
if __name__=='__main__':main()
