# -*- coding: utf-8 -*-
from pathlib import Path
import re,sys
sys.stdout.reconfigure(encoding='utf-8');ls=Path('runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html').read_text(encoding='utf-8').splitlines()
for i in range(3340,3550):
 s=ls[i-1]
 if any(t in s for t in ['Gamma','Γ','square','positive','spectral']):print(i,re.sub('<[^>]*>',' ',s))
