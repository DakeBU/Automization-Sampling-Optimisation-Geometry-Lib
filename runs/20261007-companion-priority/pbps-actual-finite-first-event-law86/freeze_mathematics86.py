from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_sha256=sha(b),RAW_bytes=len(b))
m=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
s=m.read_text(encoding='utf-8');seal=load(r/'root.statement-seal86.json')
prop=s.split('private def ',1)[1].split('\n\n-- Internal FTC',1)[0].rstrip()+'\n'
assert prop==seal['expanded_literal_Prop']
q=load(r/'focused-complete86.attempt1/receipt.json')
assert q['terminal_closed'] and q['exit_code']==0 and q['source_raw_sha256']==sha(m.read_bytes())
x=dict(status='FOCUSED_COMPILED_WHOLE_PUBLIC_ANCHOR_INDEPENDENT_REVIEW_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),module=pin(m),statement_seal=pin(r/'root.statement-seal86.json'),focused_final_receipt=pin(r/'focused-complete86.attempt1/receipt.json'),sealed_private_Prop_unchanged=True,internal_ingredients=['first_density_setIntegral','first_density_measure_mass','first_density_measure_Iic','finite_wait_mass','finite_wait_real_cdf'],checked_commit='8280ef700ea01a1e94c9e7a3cba05a26b4156b56 plus pinned working module',PROVED_LOCAL=False,VERIFIED=False,full_paper=False)
p=r/'mathematics-freeze86.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(x['module'])
