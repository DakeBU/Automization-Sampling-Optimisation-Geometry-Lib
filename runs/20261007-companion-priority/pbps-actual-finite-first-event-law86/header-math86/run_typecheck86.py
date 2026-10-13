from pathlib import Path
import datetime,hashlib,json,re,subprocess,time
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(n,d):
    with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
p=B/'header86.proposed.lean';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='51e925d7a7874083c0802682e7157fcaa2adf6961c2f1ba711d1646ab35e32d8'
marker=b'\nend\r\nend ' if b'\r\n' in raw else b'\nend\nend '
# Append local #check inside the original namespace. Original full Prop bytes retained.
needle=b'\r\nend\r\nend ' if b'\r\n' in raw else b'\nend\nend '
assert raw.count(needle)==1
local=raw.replace(needle,(b'\r\n#check actual_finite_first_event_law_statement\r\n' if b'\r\n' in raw else b'\n#check actual_finite_first_event_law_statement\n')+needle)
copy=O/'header86.full-private-prop.local-check.lean'
with copy.open('xb') as f:f.write(local)
parents=[R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
def prop_only(p):
    s=p.read_text('utf8');a=s.index('private def ')
    stops=[m.start() for m in re.finditer(r'(?m)^(?:set_option |(?:private )?theorem |/--)',s) if m.start()>a]
    return s[a:min(stops)].rstrip()
def lets(s):
    matches=list(re.finditer(r'(?m)^    let (\S+)\s*:',s));out={}
    for i,m in enumerate(matches):
        z=matches[i+1].start() if i+1<len(matches) else (s.index('\n    ∀',m.start()) if '\n    ∀' in s[m.start():] else len(s))
        out[m.group(1)]=s[m.start():z].rstrip()
    return out
header=raw.decode('utf8').replace('\r\n','\n');blocks=lets(header)
parent85=prop_only(parents[0]);prefix=lets(parent85)
same={n:blocks[n]==prefix[n] for n in ['P','ε','c','Φ','S','rate','Λ','τ']}
save('definition-readback86.json',dict(created_utc=now(),header=pin(p),parent85=pin(parents[0]),eight_definitions_exact_byte_text_after_newline_normalization=same,all_eight_identical=all(same.values()),literal_blocks={n:blocks[n] for n in blocks},parent_statement_readbacks=[dict(file=pin(q),private_prop=prop_only(q),implementation_BODY_not_displayed=True) for q in parents],binder_names=re.findall(r'\((h\S+)\s*:',header[:header.index(': Prop :=')]),scope='Whole header and exact parent private Props only; no86BODY exists. Previous separate source-only review visibility deviation remains disclosed there.'))
assert all(same.values())
tool=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'
cmd=[str(tool),'env','lean',str(copy)]
inputs=[p,B/'header86.preparation.json',R/'lean-toolchain',R/'lake-manifest.json',*parents]
save('typecheck-inputs86.json',dict(created_utc=now(),inputs=[pin(q) for q in inputs],local_copy=pin(copy),local_overlay='Only local #check inside namespace; exact complete original private Prop unchanged. No theorem/body/axiom/sorry placeholder.',compiler=str(tool),command=cmd))
t=time.perf_counter();start=now()
with (O/'whole-header86.stdout.log').open('xb') as out,(O/'whole-header86.stderr.log').open('xb') as err:
    result=subprocess.run(cmd,cwd=R,stdout=out,stderr=err)
save('typecheck-receipt86.json',dict(command=cmd,cwd=str(R),started_utc=start,finished_utc=now(),wall_seconds=time.perf_counter()-t,terminal_exit_code=result.returncode,foreground=True,input_header=pin(p),compiled_copy=pin(copy),stdout=pin(O/'whole-header86.stdout.log'),stderr=pin(O/'whole-header86.stderr.log'),toolchain=pin(R/'lean-toolchain'),lake_manifest=pin(R/'lake-manifest.json'),no_Lean_theorem_proof_credit=True))
print(json.dumps(dict(terminal_exit_code=result.returncode,receipt=pin(O/'typecheck-receipt86.json'),definition_identity=same)))
print((O/'whole-header86.stdout.log').read_text('utf8')[-2200:])
print((O/'whole-header86.stderr.log').read_text('utf8')[-1000:])
