from pathlib import Path
old=Path('.astis/pbps-actual-rotation70');new=Path('.astis/pbps-corrector71')
replacements=[('pbps-actual-projected-rotation70','pbps-actual-corrector-change71'),('pbps-actual-rotation70','pbps-corrector71'),('ActualProjectedRotation.actual_projected_rotation','ActualCorrectorChange.actual_corrector_change'),('ActualProjectedRotation','ActualCorrectorChange'),('actual-projected-rotation','actual-corrector-change'),('integration70','integration71'),('visual70','visual71'),('root.exact-verification70','root.exact-verification71'),('root.source70','root.source71'),('aggregate70','aggregate71'),('AGGREGATE70','AGGREGATE71'),('SCI70','SCI71'),('PASS70','PASS71'),('admin70','admin71'),('final70','final71'),('Registry518','Registry519'),('registry_count=518','registry_count=519'),('239 publication','240 publication'),('239publication','240publication'),('publication_units=239','publication_units=240')]
text=(old/'record-integration70.py').read_text(encoding='utf8')
for a,b in replacements:text=text.replace(a,b)
before="Serialized Registry519/imports/Tests and current reader/graph gates are pending\\nagainst final admin state; exact science verification is separate from these\\naggregate admissions and from remote CI."
after="Serialized Registry519/imports/Tests and current reader/graph gates are pending\\nagainst final admin state. Exact science verification is separate from aggregate,\\nreader and remote CI admission."
assert text.count(before)==1;text=text.replace(before,after)
text=text.replace('actual projected rotation/pair energy','actual same-C B21 corrector change')
text=text.replace('same-actual PBPS actual projected rotation/pair energy','same-actual PBPS B21 corrector-change')
text=text.replace('B21 corrector change,H1/B4','Actual B4 perturbation/B27/B28,H1/B4')
text=text.replace('70 integration.notes.json','71 integration.notes.json')
p=new/'record-integration71.py';assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
print('PASS prepared71 scoped aggregate/reader recorders with exact current handoff anchor,519Registry/240publication units.')
