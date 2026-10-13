# -*- coding: utf-8 -*-
from pathlib import Path
import sys,re
sys.stdout.reconfigure(encoding='utf-8');p=Path('runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html');ls=p.read_text(encoding='utf-8').splitlines()
for i,s in enumerate(ls,1):
 if 'Gamma' in s or 'Γ' in s or 'square root' in s:
  print(i,re.sub('<[^>]*>',' ',s)[:1800])
