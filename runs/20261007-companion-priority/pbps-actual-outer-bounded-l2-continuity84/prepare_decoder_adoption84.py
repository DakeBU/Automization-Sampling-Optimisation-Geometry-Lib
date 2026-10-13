from pathlib import Path
r=Path(__file__).parent
s=Path('runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83/adopt_decoder83.py').read_text(encoding='utf8')
for a,b in [
 ('decoder83','decoder84'),('source-review83','source-review84'),
 ('ASTIS-RT-20261010-PBPSActualBoundedTestContinuity','ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity'),
 ('a7b714040aae3ac14959d216022bfd4161c818d9ef35b53264d6563465bda169','9d2944e2cfa4a4b2729f7e56560f18e0cbed5f35ed3d5e57130dc06d51ebb77a'),
 ('c9dbecd18a8c8a681b6c77515071c85a2d432e007564c6e10c9522e6ffb5d85e','72a7e8a9cc62ba5f9a36a21217419910e7c2606a13ae8c24c93b899d9e28212e'),
 ('5956517d891aa559fe71cad0303c89fd9f61ed2a00b6dcb169057dfce33d64ed','6cf8ec9203b11da9ad27531ee8b6f94c66d6ffaef31261e745e42c68089ce8d5'),
 ("['inputs','outputs']","['input_artifacts','output_artifacts']")]:
 assert a in s,a;s=s.replace(a,b)
p=r/'adopt_decoder84.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
