from pathlib import Path
import hashlib,json,textwrap
p=Path('Tests/ProximalBPSSharpCorrectorEnergy.lean');b=p.read_bytes();s=b.decode('utf-8')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
snapshot=d/'test.before-local-global-proof.raw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
definition=s[s.index('private def '):s.index('\ntheorem ')]
tail=textwrap.dedent(definition[definition.index('                          (∀ f : Lp ℝ 2 J,'):]).strip()
assert tail.startswith('(∀ f :') and tail.endswith('))')
lines=tail[1:-1].splitlines()
signature='  have hFinal : '+lines[0]+'\n'+'\n'.join('    '+line for line in lines[1:])+' := by\n'
a=s.index('  intro f hf\n');z=s.index('\n\n\nend\nend ',a);proof=s[a:z]
s=s[:a]+'  exact hFinal'+s[z:]
insert=s.index('  unfold genuine_actual_modified_energy_equivalence_statement\n')
local=signature+''.join('  '+line if line.strip() else line for line in proof.splitlines(keepends=True))+'\n'
s=s[:insert]+local+s[insert:]
p.write_text(s,encoding='utf-8',newline='\n')
(d/'test-local-global-proof-route.json').write_text(json.dumps(dict(route='Use the unchanged final literal Test tail as the explicit type of a local have, prove it before outer witness reconstruction, then return this same proof. Reuse the diagnosed compact actual-input elaboration context.',exact_statement_tail=tail,public_statement_unchanged=True,new_declarations=False,proof_ingredients_unchanged=True,before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),compiler_credit=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Test final energy proof localized at exact unchanged statement tail; compiler pending.')
