from pathlib import Path
import json,subprocess,datetime
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');out=r/'integration81'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head==json.loads((out/'commit-observed81.json').read_bytes())['commit']
admin=json.loads((out/'final-admin.json').read_bytes());note=json.loads((r/'integration.notes.json').read_bytes())
assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
p=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
(out/'push81.stdout.log').write_bytes(p.stdout);(out/'push81.stderr.log').write_bytes(p.stderr)
assert p.returncode==0,p.stderr.decode('utf8',errors='replace')
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo'],text=True).strip();assert remote.split()[0]==head
(out/'push-observed81.json').write_text(json.dumps(dict(local_commit=head,remote_observed=remote,exit_code=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),force=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
body=Path('.astis/pr315-sau81.md')
body.write_text(f'''Construct the ideal PBPS half-turn returned-position probability kernel H_y from the actual jointly Borel physical-time phase at pi. The exact conditional reference q_y is normalized internally using the existing Gibbs and Gaussian conditional-kernel parents. The input law is the explicit independent product ((reference, standard Gaussian momentum), actual mean-one exponential clock stream). This is the ideal exact-reference law; the implemented approximate-reference sampler remains an independent obligation.

The measurable full origin/terminal live-arc event is established before product Fubini. Consequently the actual independent input law supports physical initialization and a genuine live harmonic arc at pi; its phase0 pushforward is dirac(x) x standard Gaussian. The previously verified joint phase and fixed-parameter common-AE all-finite-time properties are retained, including last-live infinite waits and explicit exceptional fallback. All six original analytic conditions are unchanged. No phase, normalization, measurability or law certificate is supplied as an extra public premise.

Independent mathematics, blind reconstruction and source-first review checked the exact module, all 65 source items, a 15-node/29-edge proof graph and ten contiguous formula/BODY regions. Science {note['science_commit']} is independently VERIFIED with the standard three axioms and actual dependencies checked. Serialized local integration {head} passed root{admin['root_jobs']}/Tests{admin['test_jobs']}, Registry{admin['registry_count']}, canonical astis.py check including ATLAS/fake-closure scans, contributor/publication/semantic/frontier, affected graph/site build/site checks, py_compile and diff check. The complete attributed statement and stepwise formula proof sit beside initially folded exact Lean.

Random-input all-time/version uniqueness, process Markov/semigroup/invariance/reversibility, hypocoercivity/mixing, implemented-reference errors/oracle costs and actual-input PBPS-SPHMC composition remain OPEN. Probability fibers alone imply none of these. TV proximity does not transfer unbounded expected costs. The existing sole stabilization lane carries this independently VERIFIED child. The affected coarse SVG was actually viewed and generated HTML content/folding checked; actual browser page/interactive branch visual acceptance remains pending because the bound browser surface has no inspectable tab. Main merge, full Exposition Seal/PURIFIED, live deployment, paper-main completion and the existing four-paper Goal remain separate.

Remote CI is separate: the science-head Lean job38057308993 failed before compiler invocation while downloading pinned Lean4.33.0 due to SSL/TLS error35. The toolchain remains fixed; local acceptance does not represent a remote CI pass. Preserve prior collaborator work, source versions, routes, cycles and memory.
''',encoding='utf8',newline='\n')
subprocess.run(['gh','pr','edit','315','--repo','DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','--title','Construct ideal PBPS half-turn kernel with actual product initialization','--body-file',str(body)],check=True)
(out/'pr315-observed81.json').write_bytes(subprocess.check_output(['gh','pr','view','315','--repo','DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','--json','url,state,headRefOid,statusCheckRollup']))
print('Normal push and existing PR315 updated',head)
