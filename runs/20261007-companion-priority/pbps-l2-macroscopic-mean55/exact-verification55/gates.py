from common import *
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis,astis_publication as pub,astis_advance as advance
assert git('rev-parse','HEAD')==SCI
data=pub.inputs();item=next(x for x in pub.load() if any(z['declaration']==TARGET for z in x['bindings']));binding=next(z for z in item['bindings'] if z['declaration']==TARGET)
payload=pub.binding_payload(item,binding,data);expected='3429f3b54edb1b9e40456d5f25677a1a54b4984f8d62aae273ce650e3b6ce862'
assert pub.digest(payload)==logical(payload)==expected and payload==load(B/'reviewer.source.binding-payload.json')
audit=load(AUDIT);source=load(B/'independent-review55/source.1.review.json')
assert audit['state']=='accepted' and audit['source_review']['state']=='accepted' and audit['source_review']['review_run_sha256']==source['review_run_sha256'] and audit['source_review']['run_artifact']==pin(B/'independent-review55/source.1.review.json')['path'] and audit['publication_binding_sha256']==expected
assert audit['publication_context']==pub.review_context(item,binding,data)
pub.check_advance([TARGET],reviewed=True)
dump('publication-binding-payload.json',payload)
body='AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean';test='Tests/ProximalBPSL2MacroscopicMean.lean';checks=load(B/'whole-math55/checks.json')
scan=[]
for row in checks['fake_closure_scan']:
 p=row['input']['path'];assert equal(row['input']);clean=astis.strip_lean_comments_and_strings(path(p).read_text(encoding='utf-8'));hits=[n for n,l in enumerate(clean.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;scan.append(dict(input=pin(p),hits=hits))
b=path(body).read_bytes().replace(b'\r\n',b'\n');start=b.index(b'theorem actual_macroscopic_l2_mean');end=b.index(b' := by',start);header=b[start:end]+b'\n';assert len(header)==2526 and sha(header)=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
(O/'statement.exact.LF.lean').write_bytes(header)
log=path(O/'focused.log').read_text(encoding='utf-8');prints=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log);assert len(prints)==3 and all(set(re.findall(r'[A-Za-z_.]+',a))=={'propext','Classical.choice','Quot.sound'} for n,a in prints) and 'sorryAx' not in log and 'Build completed successfully (3894 jobs).' in log
# Native blind complete self and three distinct named payloads; actor-object adapter preserved.
dn=[]
for f,n,nh in [('result0.json','decoder_payload','decoder_payload_sha256'),('run.json','run_payload','run_payload_sha256'),('lease.json','closure_payload','closure_payload_sha256')]:
 d=load(B/'anonymous-decoder'/f);dn.append(selfcheck(B/'anonymous-decoder'/f,'logical_sha256'));assert logical(d[n])==d[nh]
db=load(B/'anonymous-decoder/binding-receipt.json');dr=load(B/'anonymous-decoder/result0.json');dl=load(B/'anonymous-decoder/lease.json');du=load(B/'anonymous-decoder/run.json')
assert isinstance(dr['decoder'],dict) and isinstance(db['decoder'],str) and db['native_decoder_object']==dr['decoder'] and db['canonical_actor_mapping']['native_value_type']=='object' and not db['canonical_actor_mapping']['mutation_of_native_result']
assert db['exposure']['source_text_blind'] and not db['exposure']['strict_identity_blind'] and not dr['source_fidelity_self_admission'] and dl['status']=='CLOSED'
for e in db['output_artifacts']:assert equal(e)
for name,e in du['run_payload']['authorized_input_receipts'].items():
 p=B/'anonymous-decoder'/('initial-lease.raw.snapshot.json' if name=='lease.json' else name);assert equal(dict(e,path=str(p)));assert logical(load(p))==e['logical_sha256']
# Immutable full-whitespace negative and exact diagnostic exclusions. Recheck authored complement at the exact commit.
wd=load(B/'whitespace-diagnosis55/diagnosis.json');gz=path(wd['gzip']['path']).read_bytes();negative=gzip.decompress(gz);assert sha(gz)==wd['gzip']['raw_sha256'] and sha(negative)==wd['full_negative_raw_sha256'] and int.from_bytes(gz[4:8],'little')==0 and wd['findings']==1014 and len(wd['immutable_raw_artifacts'])==594 and wd['full_staged_exit']==2
immutable={e['path'] for e in wd['immutable_raw_artifacts']};diagnostic={m.group(1) for m in re.finditer(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF)\.?$',negative.decode('utf-8'),re.M)};assert diagnostic==immutable,(len(diagnostic),len(immutable))
paths=[e['path'] for e in load(O/'committed-inputs.json')['bindings']];authored=[p for p in paths if p not in immutable];batch=[]
with (O/'authored-whitespace.log').open('wb') as out:
 for i in range(0,len(authored),64):
  cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',BASE,SCI,'--']+authored[i:i+64];r=subprocess.run(cmd,cwd=R,capture_output=True);out.write(r.stdout+r.stderr);assert r.returncode==0,(i,r.stdout);batch.append(dict(start=i,count=len(authored[i:i+64]),exit_code=r.returncode))
state=advance.current_advances();a=state[ADV];assert a['state']=='PROVED_LOCAL' and a['owner_id']!=ACTOR
lanes=[k for k,v in state.items() if v['state']=='STABILIZING'];assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'],lanes
dump('gates.json',dict(status='PASS',checked_commit=SCI,actual_python_PID=os.getpid(),production=pin(body),Tests=pin(test),exact_statement=pin(O/'statement.exact.LF.lean'),whole_math_unchanged=pin(B/'whole-math55/receipt.json'),reuse_complete_whole_math=True,source0_preserved_metadata_negative=pin(B/'source.0.review.json'),source1_accepted=pin(B/'independent-review55/source.1.review.json'),source_review_logical_sha256=source['review_run_sha256'],source_audit=pin(AUDIT),reviewed_publication_gate='tools.astis_publication.check_advance([TARGET], reviewed=True) ACTUALLY PASS',publication_binding_sha256=expected,publication_payload=pin(O/'publication-binding-payload.json'),helper_whole=pin('tools/astis_publication.py'),helper_binding_lines=[47,115],fake_closure_scan=scan,axiom_closures=[dict(declaration=n,axioms=sorted(re.findall(r'[A-Za-z_.]+',a))) for n,a in prints],decoder_native_full_runs=dn,decoder_object_canonical_actor_string_adapter=True,source_text_blind=True,strict_identity_blind=False,full_whitespace_negative=dict(findings=1014,exact_immutable_paths=594,gzip_mtime=0,negative=pin(wd['gzip']['path']),full_staged_PASS=False),authored_complement=dict(count=len(authored),batch_size=64,batches=batch,exit_code=0,log=pin(O/'authored-whitespace.log')),Win206_retired_negative=pin(B/'science-stage-argument.0.diagnosis.json'),advance_before_state=a['state'],owner_id=a['owner_id'],verifier_id=ACTOR,sole_STABILIZING=lanes))
print(json.dumps(dict(status='PASS',reviewed_publication=True,binding=expected,fake_hits=0,standard3=3,decoder_native_complete=True,whitespace_authored=len(authored),immutable_negative_paths=594,STABILIZING=lanes)))
