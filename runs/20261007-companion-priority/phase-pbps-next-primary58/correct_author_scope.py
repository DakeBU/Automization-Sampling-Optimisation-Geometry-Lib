from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-next-primary58')
p=O/'author_diagnosis.py'
s=p.read_text(encoding='utf8')
s=s.replace("'frozen_balanced_raw':pin(P/'A2.SS3.raw.html'),'D1_frozen_raw'", "'B10_balanced_raw':pin(P/'A2.E10.raw.html'),'B11_balanced_raw':pin(P/'A2.E11.raw.html'),'B15_balanced_raw':pin(P/'A2.E15.raw.html'),'B16_balanced_raw':pin(P/'A2.E16.raw.html'),'D1_frozen_raw'")
s=s.replace("'line':453,'status':'Positivity", "'line':266,'additional_lines':[462,474],'status':'Positivity")
s=s.replace("'search_scope':'Bounded pinned files", "'reuse_architecture':'A missing implementation adapter should be a reusable shared measure-pullback range leaf (generic pushforward/comap measurability, complete metrizable REAL target; no source Y StandardBorel or complete-space assumption required by Doob-Dynkin). The actual PBPS macro integration consumes it internally and retains original PBPS assumptions. No background certificate is a public PBPS premise.','search_scope':'Bounded pinned files")
assert "'B10_balanced_raw'" in s and "'line':266,'additional_lines'" in s
p.write_bytes(s.encode('utf8'))
print('UNEXECUTED_OPEN_AUTHOR_SOURCE_SCOPE_CORRECTED')
