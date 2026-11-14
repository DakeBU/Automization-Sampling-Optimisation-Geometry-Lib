"""Preserve first verifier failures; repair only verifier compatibility checks."""
from run import ROOT,sha
import json
old=ROOT/'scratch/InspectAll.lean'
src=old.read_text();(ROOT/'scratch/InspectAll.v1.original.lean').write_text(src)
(ROOT/'scratch/InspectAllV2.lean').write_text(src.replace('set_option pp.maxDepth 100000\n','').replace('native-all-bodies.json','native-all-bodies-v2.json'))
s=(ROOT/'check_native.py').read_text().replace("('inspect-all','InspectAll.lean')","('inspect-all-v2','InspectAllV2.lean')").replace("('independent-literal-kernel','IndependentLiteralCheck.lean')","('independent-literal-kernel-v2','IndependentLiteralCheck.lean')").replace('native-all-bodies.json','native-all-bodies-v2.json')
(ROOT/'check_native_v2.py').write_text(s)
s=(ROOT/'reader_static.py').read_text()
s=s.replace("assert div.children[0].text()==s['text'] and div.children[1].text()=='\\\\['+s['formula']+'\\\\]'", "assert div.children[0].text()==html.unescape(lessons.inline_text(s['text'])) and div.children[1].text()=='\\\\['+s['formula']+'\\\\]'")
(ROOT/'reader_static_v2.py').write_text(s)
failures=[{'original':'receipts/inspect-all.json','class':'IMPLEMENTATION_FAILED','scope':'Verifier script, no theorem failure','diagnosis':'Lean4.33 rejects obsolete pp.maxDepth option inherited from scaffold; command continued and exported data but nonzero exit remains rejected. V2 omits only this option.'},
{'original':'receipts/reader-static-driver.json','class':'IMPLEMENTATION_FAILED','scope':'Static checker assertion, no renderer defect','diagnosis':'Production inline_text intentionally converts prose ASCII >= into ≥; V1 compared raw authored prose. V2 compares exact production-escaped prose after entity decoding, while formulas and Lean remain byte exact.'}]
(ROOT/'verifier-failures.json').write_text(json.dumps(failures,indent=2)+'\n')
print('Preserved original failing scripts/receipts/streams; created changed verifier V2 checks.')
