"""Independent whole-source mathematical audit compiler evidence; no production edits."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78'
OUT=BASE/'independent-math78'
OUT.mkdir(parents=True,exist_ok=True)
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'
PARENT=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
PRODUCT=ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation'
os.environ['PYTHONUTF8']='1'
sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
    b=Path(p).read_bytes();return {'path':str(p),'RAW_bytes':len(b),'RAW_sha256':sha(b)}
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
seal=load(BASE/'root.statement-seal78.json')
for k in ['header','source_first_freeze','source_graph_overlay','header_math','source_topology_review','syntax_overlay_review','private_overlay_review','typecheck','toolchain','lake_manifest']:
    a=seal[k];assert sha((ROOT/a['path']).read_bytes())==a['RAW_sha256'],k
for a in seal['dag_parents']:assert sha((ROOT/a['path']).read_bytes())==a['RAW_sha256']
focused=load(BASE/'focused78-attempt2/receipt.json')
assert focused['exit_code']==0 and focused['terminal_closed']
assert info(MODULE)['RAW_sha256']==focused['source_RAW_sha256']=='e6d71cb969b30f6ac8e6be65e5cd067166b4f29213d9328ed9edc0971fd026fc'
source=MODULE.read_text(encoding='utf-8')
header=(ROOT/seal['header']['path']).read_text(encoding='utf-8')
private=source[source.index('private def '):source.index('\n\n\nset_option maxHeartbeats')]
sealed_private=header[header.index('private def '):header.index('\n\nend\n')]
assert private==sealed_private
before_body=source[:source.index(' := by\n')]
assert before_body.count('\ntheorem ')==1 and before_body.count('\nprivate def ')==1
binder=private[private.index('    {E : Type*}'):private.index('    let P :')].removesuffix(' : Prop :=\n')
public=before_body[before_body.index('\ntheorem '):]
pub_binder=public[public.index('    {E : Type*}'):public.index(' :\n    actual_fixed_reference')]
assert binder==pub_binder
parent=PARENT.read_text(encoding='utf-8');parent_private=parent[:parent.index('\nset_option maxHeartbeats')]
def lets(s,indent,stop):
    patt=r'^'+(' '*indent)+r'let (\S+)\s*:';matches=list(re.finditer(patt,s,re.M));r={}
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else s.index(stop,m.start())
        r[m.group(1)]=s[m.start():end]
    return r
headlets=lets(private,4,'    ∀ y')
parentlets=lets(parent_private,4,'    (∀ y')
for name in ['c','Φ','S','rate','Λ','τ','next','record','eventTime']:assert headlets[name]==parentlets[name],name
assert len(headlets)==11
body=source[source.index(' := by\n')+7:]
bodylets=lets(body[:body.index('  -- Reuse')],2,'  change')
for name in ['c','Φ','S','rate','H','C','Λ','τ','next','record','eventTime']:
    assert '\n'.join(line[2:] for line in parentlets[name].splitlines())=='\n'.join(bodylets[name].splitlines()),name
from tools import astis
stripped=astis.strip_lean_comments_and_strings(source)
module_hits=[{'line':n,'text':s.strip()} for n,s in enumerate(stripped.splitlines(),1) if astis.FORBIDDEN_REGEX.search(s)]
assert not module_hits
save('statement-and-definition-audit78.json',{'status':'PASS','reviewer':'/root/exact_verify77','module':info(MODULE),
    'statement_seal':info(BASE/'root.statement-seal78.json'),'private_Prop_exact_to_sealed_header':True,
    'public_binders_exact_to_private_Prop':True,'source_analytic_premises':6,'new_public_provider_premises':0,
    'literal_statement_objects':11,'exact_parent_recurrence_objects':['c','Φ','S','rate','Λ','τ','next','record','eventTime'],
    'body_internal_H_C_and_parent_definitions_exact':True,'whole_module_fake_closure_hits':module_hits,
    'focused_receipt_reused_as_supplement':info(BASE/'focused78-attempt2/receipt.json'),
    'not_source_blind_decoder':True,'not_final_source_review':True})
snapshot=OUT/'module78.exactraw.lean';snapshot.write_bytes(MODULE.read_bytes())
probe=OUT/'FreshWholeModuleAxioms78.lean'
probe.write_bytes(MODULE.read_bytes()+ ('\n/- Independent fresh full-source elaboration and axiom readback only. -/\n#print axioms '+DECL+'\n#check '+DECL+'\n').encode('utf-8'))
frozen=[info(p) for p in [MODULE,PARENT,PRODUCT,BASE/'root.statement-seal78.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json',probe]]
save('input-freeze78.json',{'inputs':frozen,'head_at_freeze':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True).stdout.decode().strip(),
    'scope':'Independent mathematics and fresh source elaboration only; not exact-science-commit admission.'})
lake=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
cmd=[lake,'env',lean,str(probe)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'fresh-whole-module-axioms.stdout.log').open('wb') as so,(OUT/'fresh-whole-module-axioms.stderr.log').open('wb') as se:
    child=subprocess.Popen(cmd,cwd=ROOT,stdout=so,stderr=se,env=os.environ.copy());code=child.wait()
save('fresh-whole-module-axioms.receipt.json',{'command':cmd,'cwd':str(ROOT),'started_utc':start,
    'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_foreground_PID':child.pid,
    'exit_code':code,'terminal_closed':True,'inputs':frozen,'stdout':info(OUT/'fresh-whole-module-axioms.stdout.log'),
    'stderr':info(OUT/'fresh-whole-module-axioms.stderr.log'),'full_source_prefix_exact':True,
    'canonical_olean_written':False,'native_reasoning_trajectory_claimed':False})
print('FRESH COMPLETE SOURCE EXIT',code,flush=True)
assert code==0
text=(OUT/'fresh-whole-module-axioms.stdout.log').read_text(encoding='utf-8')
ax=re.search(r'depends on axioms: \[([^\]]+)\]',text)
assert ax and set(a.strip() for a in ax.group(1).split(','))=={'propext','Classical.choice','Quot.sound'}
assert info(MODULE)==frozen[0]
save('fresh-compiler-summary78.json',{'status':'PASS_FULL_SOURCE_STANDARD_THREE','module':info(MODULE),
    'axioms':['propext','Classical.choice','Quot.sound'],'receipt':info(OUT/'fresh-whole-module-axioms.receipt.json'),
    'statement_definition_audit':info(OUT/'statement-and-definition-audit78.json'),'proof_reviewer':'/root/exact_verify77',
    'source_review':False,'VERIFIED':False,'Goal_complete':False})
print('FRESH WHOLE-SOURCE MATHEMATICS EVIDENCE READY',flush=True)
