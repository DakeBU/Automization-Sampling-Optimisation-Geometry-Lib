from pathlib import Path
p=Path('.astis/pbps-polar65/adopt-decoder65.py')
s=p.read_text(encoding='utf-8')
replacements={
"'1740d084b5a9c69f9c6dcd3ff967004aef4065cc80c49fa1d2824b051a9806b2'":'expected_whole',
"'bbc16712419f26afd4495208deaf21d889228b00e6f212cf81774d9f0d7c3892'":'expected_named',
'==13916':'==int(expected_readback)',
'==43476':'==int(expected_close)',
'PBPSActualPolarIsometry':'PBPSAmbientAdjointCorrector',
'pbps-actual-polar-isometry':'pbps-ambient-adjoint-corrector',
'FOCUSED_COMPILED_ONLY_INDEPENDENT_MATH_DECODER_SOURCE_PUBLICATION_PENDING':'FOCUSED_COMPILED_ONLY_INDEPENDENT_MATH_DECODER_WHOLE_MODULE_SOURCE_PENDING',
}
for old,new in replacements.items():
    assert old in s,old
    s=s.replace(old,new)
s=s.replace('65','66')
s=s.replace('pbps-polar66','pbps-ambient-adjoint66')
needle="load=lambda p:json.loads(Path(p).read_bytes());"
assert needle in s
s=s.replace(needle,"expected_whole,expected_named,expected_readback,expected_close=sys.argv[1:]\n"+needle)
target=Path('.astis/pbps-ambient-adjoint66/adopt-decoder66.py')
assert not target.exists()
target.write_text(s,encoding='utf-8',newline='\n')
print('Prepared guarded decoder66 adopter; no native/canonical audit state changed.')
