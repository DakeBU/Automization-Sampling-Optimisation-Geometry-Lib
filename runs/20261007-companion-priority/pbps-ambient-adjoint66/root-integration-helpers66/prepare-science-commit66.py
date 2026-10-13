from pathlib import Path
s=Path('.astis/pbps-polar65/commit-proof65.py').read_text(encoding='utf-8')
changes={
"pbps-polar65":"pbps-ambient-adjoint66",
"parent='0aef19ca2711159eeaec86d42c9be142a94fa402'":"parent='31ce36e7ca01b203696918672c33d29a337550c3'",
"['independent-math65','independent-source65']":"['independent-math66','independent-source66']",
"root-science-helpers65":"root-science-helpers66",
"['pbps-ambient-adjoint66','pbps-polar-preproof65']":"['pbps-ambient-adjoint66','pbps-ambient-adjoint-preproof66']",
"late64":"late65",
"pbps-centered-root64":"pbps-polar65",
"or 'preproof66' in p":"or 'pbps-polar-preproof65' in p",
"whitespace-diagnosis65":"whitespace-diagnosis66",
"Prove actual PBPS centered polar isometry and typed adjoint corrector":"Prove actual PBPS ambient adjoint and globally centered corrector",
"PASS65 science commit":"PASS66 science commit",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
old="for p in Path('.astis/pbps-ambient-adjoint66').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())"
assert old in s
s=s.replace(old,old+"\npreproof_helpers=export/'preproof-origin65';preproof_helpers.mkdir()\nfor p in Path('.astis/pbps-polar65').glob('*66*.py'):(preproof_helpers/p.name).write_bytes(p.read_bytes())\npost65_helpers=export/'post65';post65_helpers.mkdir()\nfor name in ['adopt-ci65.py']:\n p=Path('.astis/pbps-polar65')/name;(post65_helpers/name).write_bytes(p.read_bytes())")
target=Path('.astis/pbps-ambient-adjoint66/commit-proof66.py');assert not target.exists()
target.write_text(s,encoding='utf-8',newline='\n')
print('Prepared guarded SCI66 commit helper; no staging/commit or canonical state change.')
