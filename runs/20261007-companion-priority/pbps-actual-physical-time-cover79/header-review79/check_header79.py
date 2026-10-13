from pathlib import Path
import re,json,hashlib,datetime,subprocess,os
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'header-review79'
S=R/'runs/20261007-companion-priority/pbps-physical-time-preread79'
H=B/'header79.proposed.lean';P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean';F=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=str(p),RAW_bytes=len(p.read_bytes()),RAW_sha256=sha(p.read_bytes()))
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(H.read_bytes())=='4b3b12a9e83195cfca5c02466b51f838b0e175fad23a9665ab32df7553968a1a'
assert sha((S/'source-freeze79.json').read_bytes())=='73511f78e36675ded6166d837477173ea06d10f3f71936055852d8219816e38b'
source=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_text(encoding='utf-8')
native=[]
for e in load(S/'source-freeze79.json')['regions']:
 a,b=e['utf8_text_character_offsets'];raw=source[a:b].encode()
 assert sha(raw)==e['exact_region_utf8_sha256']
 native.append(dict(start=e['start_native_anchor'],end=e['exclusive_end_native_anchor'],RAW_sha256=sha(raw),exact_primary_range_match=True))
save('extractor-range-readback79.json',dict(independently_read_primary_first=True,source_freeze=info(S/'source-freeze79.json'),capsule=info(S/'bounded-capsule79.json'),ranges=native))
header=H.read_text(encoding='utf-8')
def statements(p):
 s=p.read_text(encoding='utf-8');start=s.index('set_option maxHeartbeats')
 theorem=s.index('theorem ',start);body=s.index(':= by',theorem)
 return s[:start]+s[theorem:body]+':= <BODY WITHHELD>\n'
p=statements(P);f=statements(F)
for name,s in [('ActualNonaccumulation.statements-only79.txt',p),('ActualFiniteJumpRecursion.statements-only79.txt',f)]:
 q=O/name;assert not q.exists();q.write_text(s,encoding='utf-8')
def binder(s):return s[s.index('    {E : Type*}'):s.index('    let ')]
assert binder(header)==binder(p)==binder(f)
def lets(s):
 found=list(re.finditer(r'^    let (\S+)\s*:',s,re.M));d={}
 for i,m in enumerate(found):
  end=found[i+1].start() if i+1<len(found) else re.search(r'^    [\(]?∀',s[m.start():],re.M).start()+m.start()
  d[m.group(1)]=s[m.start():end]
 return d
hd=lets(header);pd=lets(p);fd=lets(f)
assert len(hd)==11 and hd==pd
common=['c','Φ','S','rate','Λ','τ','next','record','eventTime']
for k in common:assert hd[k]==fd[k],k
assert header.count('private def actual_fixed_reference_physical_time_cover_statement')==1
assert not re.search(r'^theorem ',header,re.M)
save('signature-definition-readback79.json',dict(status='PASS_PROSPECTIVE_SIGNATURE_DEFINITIONS_ONLY',header=info(H),parent78=info(P),parent76=info(F),
 six_analytic_binder_block_exact=True,all_eleven_actual_definitions_exact_parent78=True,nine_recurrence_definitions_exact_parent76=common,
 new_public_provider_premises=[],private_specification_only=True,proof_BODY_read_for_this_task=False,proof_credit=False))
q=O/'header79.exactraw.lean';assert not q.exists();q.write_bytes(H.read_bytes())
inputs=[info(x) for x in [H,P,F,R/'lean-toolchain',R/'lake-manifest.json',S/'source-freeze79.json',S/'bounded-capsule79.json']]
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
cmd=[lake,'env',lean,str(q)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,PYTHONUTF8='1');env.pop('ELAN_TOOLCHAIN',None)
with (O/'typecheck.stdout.log').open('xb') as out,(O/'typecheck.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Full private Prop foreground PID',child.pid,flush=True);code=child.wait()
save('typecheck.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,
 started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=inputs,
 stdout=info(O/'typecheck.stdout.log'),stderr=info(O/'typecheck.stderr.log'),scope='Complete named private Prop and local #check only; no theorem BODY or proof credit'))
print('FULL HEADER TYPECHECK EXIT',code,flush=True)
