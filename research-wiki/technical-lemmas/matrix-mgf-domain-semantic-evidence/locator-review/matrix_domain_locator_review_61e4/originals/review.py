"""Exact-proposal line-custody review only; applies two JSON fields in memory and never writes canonical data."""
import copy,datetime as dt,hashlib,json,os
from pathlib import Path
import subprocess,sys,time,traceback
OWN=Path(__file__).resolve().parent;REPO=OWN.parents[2]
COMMIT='a8bb8ea5b4474be5214bd83ae380a612e2cecb78'
MAP='research-wiki/technical-lemmas/matrix-mgf-domain-semantic-evidence/source-to-lean.correspondence.authored-v1.json'
OVERLAY='.astis/semantic-neutral-20261115/matrix_domain_fresh_source_53d8/source-correspondence-locator-only.proposed-v1.json'
P='AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveDefIntegral.lean';T='Tests/GaussianComplexityMatrixMgfDomain.lean'
SG='.astis/semantic-neutral-20261115/matrix_domain_sg_48bc/source-graph.v1.json';BR='.astis/semantic-neutral-20261115/matrix_domain_sg_48bc/author-derived-bridges.v1.json'
LESSON='website/content/declaration_lessons/huanjian-matrix-mgf-domain.json';PUB='website/content/publications/huanjian-matrix-mgf-domain.json'
EXPECTED={MAP:'2b9873f8340135308fdcd7499076794d09095a101704fc5ca45f6e5c30c1a33d',OVERLAY:'44707d2a450a5fc09d749a9ee5196be05d025a603c77e2508a0c9c0044a50725',P:'d3c6e5a194fecf1ae1abe45c70310f4f47d66e903b098019c326ee0d3018b024',T:'60e9f7b928ebc1b8a0d9efad93f39f1b172fe0a871893d67eb1015582c5d5c61',SG:'884f7970347129bf75f3a15feb6bcbcb4c0c427a2cdefbf3a5cc90abef75cf09',BR:'3a66bd5bef0858fe57a01e15231851808f0c54da196cba918e012db7283dd9c1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def h(p):return sha(Path(p).read_bytes())
def dump(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def exact(p,b):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def differences(a,b,path=''):
    if type(a) is not type(b):return [path]
    if isinstance(a,dict):return sum((differences(a[k],b[k],path+'/'+k) if k in a and k in b else [path+'/'+k] for k in sorted(set(a)|set(b))),[])
    if isinstance(a,list):return [] if a==b else [path]
    return [] if a==b else [path]
def run(label,argv):
    d=OWN/'command-receipts';d.mkdir(exist_ok=True);out=d/(label+'.stdout.raw');err=d/(label+'.stderr.raw');start=time.monotonic();utc=dt.datetime.now(dt.timezone.utc).isoformat()
    with out.open('xb') as o,err.open('xb') as e:r=subprocess.run(argv,cwd=REPO,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0'},stdin=subprocess.DEVNULL,stdout=o,stderr=e)
    dump(d/(label+'.receipt.json'),{'argv':argv,'cwd':str(REPO),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':h(out),'stderr_sha256':h(err),'scope':'read-only immutable explicit object lookup'})
    assert r.returncode==0;return out.read_bytes()
def main():
    inputs={p:(REPO/p).read_bytes() for p in [MAP,OVERLAY,P,T,SG,BR,LESSON,PUB]};before={p:sha(b) for p,b in inputs.items()}
    assert all(before[p]==v for p,v in EXPECTED.items())
    for raw,b in inputs.items():exact(OWN/'input-originals'/raw,b)
    assert run('exact-commit',['/usr/bin/git','--no-optional-locks','rev-parse',COMMIT]).decode().strip()==COMMIT
    for label,raw in [('P',P),('T',T)]:
        b=run('exact-'+label+'-source',['/usr/bin/git','--no-optional-locks','cat-file','blob',COMMIT+':'+raw]);assert b==inputs[raw]
    original=json.loads(inputs[MAP]);proposal=json.loads(inputs[OVERLAY]);sg=json.loads(inputs[SG]);bridge=json.loads(inputs[BR])
    assert proposal['original_file']==MAP and proposal['original_file_sha256']==EXPECTED[MAP] and proposal['candidate_commit']==original['candidate_commit']==COMMIT
    assert proposal['code_file']==T and proposal['code_file_sha256']==EXPECTED[T] and len(proposal['operations'])==2
    expected_ops={
      '/SOURCE_GAP_author_implementation_map/GAP-FINITE-MATRIX-INTEGRATION':([T,176,183],[[T,57,87],[T,95,137],[T,145,183],[T,187,190]]),
      '/SOURCE_GAP_author_implementation_map/GAP-FOUR-MGF-ENVELOPE':([T,191,209],[[T,103,137],[T,138,186],[T,187,210]])}
    assert {x['json_pointer'] for x in proposal['operations']}==set(expected_ops)
    projected=copy.deepcopy(original);witness=[];lines=inputs[T].splitlines(keepends=True)
    requirements={
      'GAP-FINITE-MATRIX-INTEGRATION':[(57,82,'full-law dimensions/Gaussian probability data, Y/actual means/Z, weights/global signs/S'),(83,87,'Borel and probability instances'),(95,102,'actual Structure call and extracted measurability/Hermiticity'),(103,114,'actual Radius call and derived centered radius'),(115,137,'weight/sign/sum norm bound and S measurability/Hermiticity'),(145,175,'same-matrix exponential identification and spectral/pointwise G facts'),(176,183,'exponential continuity, measurable G and actual matrix Bochner integrability'),(187,190,'continuous linear trace, actual integral commutation and scalar trace integrability')],
      'GAP-FOUR-MGF-ENVELOPE':[(103,137,'Radius call, Z/S norm bounds, actual four weight/sign parameters and sum structure'),(138,144,'all-real parameter/case introduction and actual G/MX/B domain target'),(145,183,'same-matrix exp, pointwise PD and norm envelope, G measurability/integrability'),(184,186,'actual new canonical P call giving true mean PD'),(187,192,'trace commutation/integrability and exact r² cardinality'),(193,209,'actual R16 trace-envelope call, pointwise cap and probability integration'),(210,210,'final strict-trace conjunct hMX.trace_pos, not only upper-cap end line')]}
    sg_nodes={n['id']:n for n in sg['nodes']}
    for op in proposal['operations']:
        pointer=op['json_pointer'];old,new=expected_ops[pointer];assert op['old_exact_value']==old and op['new_exact_value']==new
        key=pointer.rsplit('/',1)[1];assert original['SOURCE_GAP_author_implementation_map'][key]==old
        projected['SOURCE_GAP_author_implementation_map'][key]=copy.deepcopy(new)
        assert sg_nodes[key]['kind']=='SOURCE_GAP'
        coverage={i for raw,a,b in new for i in range(a,b+1)};checks=[];spans=[]
        for raw,a,b in new:
            assert raw==T and 1<=a<=b<=len(lines)
            body=b''.join(lines[a-1:b]);spans.append({'file':raw,'first_line':a,'last_line':b,'exact_LF_body_sha256':sha(body),'first_line_text':lines[a-1].decode().rstrip('\n'),'last_line_text':lines[b-1].decode().rstrip('\n')})
        for a,b,why in requirements[key]:assert set(range(a,b+1))<=coverage;checks.append({'lines':[a,b],'local_implementation_component':why,'covered':True})
        witness.append({'json_pointer':pointer,'old_exact':old,'new_exact':new,'source_gap_statement':sg_nodes[key]['statement'],'range_witnesses':spans,'coverage_checks':checks})
    changed=differences(original,projected);assert set(changed)==set(expected_ops) and len(changed)==2
    assert original['mapping']==projected['mapping'] and original['unchanged_truth_boundary']==projected['unchanged_truth_boundary'] and original['gap_status']==projected['gap_status'] and original['no_extra_public_T_node']==projected['no_extra_public_T_node']
    assert proposal['mathematical_source_repairs']==[] and proposal['Lean_changes']==proposal['P_or_T_statement_changes']==proposal['lesson_or_publication_changes']==proposal['new_public_nodes_or_proof_credit']==0
    projected_bytes=(json.dumps(projected,ensure_ascii=False,indent=2)+'\n').encode();exact(OWN/'in-memory-locator-map.PROPOSED_NOT_APPLIED.json',projected_bytes)
    dump(OWN/'exact-range-coverage-witnesses.json',{'scope':'Local line custody/support locations only; producer call sites are dependencies, not a reproduction or new proof credit for those producers.','witnesses':witness,'finite_integration_context_note':'The first revised gap deliberately omits strict-mean-PD call184–186, whose separate GAP-STRICT-MEAN-PD map is unchanged. Its pure G/MX/B binder restatement138–144 remains available through the unchanged T-G-DOMAIN-PD-MEAN mapping138–186 and full exact module. The listed local ranges cover the claimed law/S/domain/integration computations, not every binder/context line.','no_source_fidelity_or_exhaustive_source_coverage_verdict':True})
    after={p:h(REPO/p) for p in inputs};assert after==before
    dump(OWN/'locator-only-review-result.json',{'schema':'astis.distinct-exact-locator-only-review.v1','status':'ACCEPT_EXACT_TWO_LOCATOR_REPLACEMENTS_ONLY','reviewer':'matrix_domain_locator_review_61e4','proposal_creator':'/root/matrix_domain_fresh_source_53d8','reviewer_distinct_from_proposer_and_original_map_author':True,'original_map':{'file':MAP,'sha256':EXPECTED[MAP]},'exact_proposal':{'file':OVERLAY,'sha256':EXPECTED[OVERLAY]},'immutable_source_commit':COMMIT,'P_sha256':EXPECTED[P],'T_sha256':EXPECTED[T],'SG_sha256':EXPECTED[SG],'author_derived_bridges_sha256':EXPECTED[BR],'actual_structural_changes_if_applied_in_memory':changed,'all_other_fields_structurally_identical':True,'proposed_map_not_applied_sha256':sha(projected_bytes),'findings':['Finite-integration range now reaches full Gaussian law and actual Y/means/Z/S definitions, probability/Borel instances, Structure/Radius use sites, sum measurability/Hermiticity/norm, actual exp identification/norm/measurability/integrability and trace CLM commutation. It is no longer restricted to final G-continuity/integrability lines.','Four-family envelope now includes the sum/radius/case/domain chain103–186 and trace/cardinality/cap/final strict trace187–210. The final hMX.trace_pos at210 is explicitly included.','Discontiguous/overlapping support locations do not create extra public nodes or producer proof credit. Other GAP maps, all five mapping entries, source-graph/bridge statuses and authored historical truth-boundary/status fields remain unchanged.'],'blocking_findings':[],'original_input_hashes_before':before,'original_input_hashes_after':after,'originals_P_T_lesson_pub_source_graph_bridge_map_overlay_unchanged_during_review':True,'mathematical_statement_code_lesson_publication_source_credit_changes':0,'canonical_map_writes':0,'Lean_browser_source_fidelity_normal_API_V_ledger_Git_mutations':0,'scope':'Exact line-custody/correspondence locator overlay review only. Not acceptance of a printed source theorem, proof repair, added lemma, full source coverage/source fidelity, semantic binding successor, or normal verification. Acceptance applies only to proposal44707 and originalmap2b987 at exact a8bb/current matching P/T bytes.'})
    print(json.dumps({'status':'ACCEPT_EXACT_TWO_LOCATOR_REPLACEMENTS_ONLY','canonical_map_writes':0,'source_or_API_changes':0,'review_result_sha256':h(OWN/'locator-only-review-result.json'),'coverage_witness_sha256':h(OWN/'exact-range-coverage-witnesses.json'),'in_memory_only_map_sha256':sha(projected_bytes)}))
if __name__=='__main__':
    d=OWN/'review-OS-process';d.mkdir(exist_ok=False);out=d/'stdout.raw';err=d/'stderr.raw';start=time.monotonic();utc=dt.datetime.now(dt.timezone.utc).isoformat();code=0
    for fd,p in [(1,out),(2,err)]:
        f=p.open('xb',buffering=0);os.dup2(f.fileno(),fd);f.close()
    try:main()
    except BaseException:traceback.print_exc();code=1
    sys.stdout.flush();sys.stderr.flush();dump(d/'receipt.json',{'schema':'actual-locator-only-readonly-review-OS-receipt-v1','argv':[sys.executable,*sys.argv],'cwd':str(REPO),'pid':os.getpid(),'started_utc':utc,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'actual_exit_code':code,'stdout_sha256':h(out),'stderr_sha256':h(err),'script_sha256':h(__file__),'scope':'Read-only explicit inputs and in-memory proposal only; all outputs under own new reviewer directory.'});sys.exit(code)
