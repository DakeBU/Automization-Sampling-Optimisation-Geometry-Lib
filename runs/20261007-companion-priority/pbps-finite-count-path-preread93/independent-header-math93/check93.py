from pathlib import Path
import json,hashlib,re,subprocess,time
from datetime import datetime,timezone
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-finite-count-path-preread93';O=B/'independent-header-math93';S=B/'Header93.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
raw=S.read_bytes();assert info(S)['raw_sha256']=='90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
old=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/root.statement-seal92.json';seal=json.loads(old.read_bytes())['expanded_literal_Prop'];text=raw.decode();norm=lambda x:re.sub(r'\s+',' ',x).strip()
newprefix=text[text.index('    let c :'):text.index('    let eventTime :')];oldprefix=seal[seal.index('    let c :'):seal.index('    ∀ n :')];assert norm(newprefix)==norm(oldprefix)
assert len(re.findall(r'\b(?:sorry|admit|axiom)\b',text))==0
save('static-check93.native.json',dict(source=info(S),prefix92_seal=info(old),all22_literal_prefix92_definitions_unchanged=True,new_public_provider_binders=False,analytic_binders=['hα','hαβ','hV','hH','hη','hβη'],observed_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),scope='Prospective Prop elaboration and mathematical statement review only; no inhabiting proof exists.'))
copy=O/'FreshHeader93.lean';suffix=b'\nset_option pp.universes true\nset_option pp.proofs false\nset_option pp.deepTerms true\nset_option pp.maxSteps 1000000\n#print Candidate93.candidate_finite_count_path_statement\n#print axioms Candidate93.candidate_finite_count_path_statement\n'
with copy.open('xb') as f:f.write(raw+suffix)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))];start=time.monotonic()
with (O/'kernel.stdout.log').open('xb') as out,(O/'kernel.stderr.log').open('xb') as err:p=subprocess.run(cmd,cwd=R,stdout=out,stderr=err)
save('kernel.receipt.native.json',dict(command=cmd,exit_code=p.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=info(S),copy=info(copy),lake_manifest=info(R/'lake-manifest.json'),stdout=info(O/'kernel.stdout.log'),stderr=info(O/'kernel.stderr.log'),scope='Definition of a prospective proposition only; not a proof of it.'));assert p.returncode==0
print(json.dumps(info(O/'kernel.receipt.native.json')),flush=True)
