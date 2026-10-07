# -*- coding: utf-8 -*-
from pathlib import Path
import re,sys
sys.stdout.reconfigure(encoding='utf-8');p=Path('runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html');ls=p.read_text(encoding='utf-8').splitlines()
for i in range(3550,3714):
 s=ls[i-1]
 if any(t in s for t in ['square root','positive','Gamma','Gamma','𝛤','Gamma','B.4','B.5','B.6','B.7','B.2','B.3']):print(i,re.sub('<[^>]*>',' ',s))
