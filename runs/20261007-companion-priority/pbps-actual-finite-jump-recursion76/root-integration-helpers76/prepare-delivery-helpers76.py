from pathlib import Path
import ast,re
old=Path('.astis/pbps-clock75');new=Path('.astis/pbps-recursion76')
def adapt(s):
 for a,b in [('pbps-actual-hazard-clock75','pbps-actual-finite-jump-recursion76'),('pbps-clock75','pbps-recursion76'),('ActualHazardClock','ActualFiniteJumpRecursion'),('actual-hazard-clock','actual-finite-jump-recursion')]:s=s.replace(a,b)
 return re.sub(r'75(?![0-9a-f])','76',s)
s=adapt((old/'record-integration75.py').read_text(encoding='utf8'))
s=s.replace("len(capture['records'])==11","len(capture['records'])==12").replace("len(probe['panels'])==len(probe['downloads'])==4","len(probe['panels'])==len(probe['downloads'])==3").replace("len(lesson['steps'])==9","len(lesson['steps'])==10").replace("len(viewed['images'])==12","len(viewed['images'])==13")
s=s.replace('formula_BODY_steps=9,copy_callbacks=4,RAW_downloads=4','formula_BODY_steps=10,copy_callbacks=3,RAW_downloads=3').replace('registry_count=524','registry_count=525').replace('publication_units=245','publication_units=246').replace('Registry524','Registry525').replace(';245 publication units',';246 publication units').replace('nine formula/BODY','ten formula/BODY').replace('four isolated copy callbacks and four RAW','three isolated copy callbacks and three RAW')
s=s.replace('Actual first-hazard clock laws','Actual finite stopped recursion and original-energy spacing').replace('Actual recursive PDMP/invariance/nonexplosion remain open.','iid thresholds/nonaccumulation/global PDMP/invariance remain open.').replace('One actual integrated-hazard/first-clock theorem with actual flow and bounce/rate formal parents, internal primitive/closed-hitting/Exp pushforward APIs. No conceptual formal edge, full recursive path or invariance claim.','One actual finite stopped recursion theorem with actual flow/bounce/first-clock formal parents, original-energy inheritance and uniform waiting increments. No conceptual formal edge, global path/nonaccumulation/invariance claim.')
ast.parse(s);p=new/'record-integration76.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
s=adapt((old/'freeze-final-reader75.py').read_text(encoding='utf8'))
s=s.replace(",'root.review-input-metadata76.adoption.json'",'').replace(",'implementation-source-map76.json'",'')
s=s.replace('registry_count=524','registry_count=525').replace('publication_units=245','publication_units=246').replace('formula_BODY_steps=9,module_lines=396,actual_captures=12,copy_callbacks=4,RAW_downloads=4','formula_BODY_steps=10,module_lines=412,actual_captures=13,copy_callbacks=3,RAW_downloads=3')
ast.parse(s);p=new/'freeze-final-reader76.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared bounded76 reader record/freeze helpers only; expected current two-declaration panels3, proof steps10, capture13 require actual checks.')
