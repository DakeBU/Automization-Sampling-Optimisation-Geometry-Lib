#!/usr/bin/env python3
"""Validate the proposed exact audit overlay without editing canonical files."""
from pathlib import Path
import copy,json,sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_publication as pub
proposal=json.loads((OUT/'proposed-canonical-audit.json').read_bytes())
packet=json.loads((OUT/'full-reviewer-input.raw.json.gz').read_bytes()) if False else None
import gzip
packet=json.loads(gzip.decompress((OUT/'full-reviewer-input.raw.json.gz').read_bytes()))
reg=copy.deepcopy(pub.roundtrip.load_registry())
matches=[i for i,a in enumerate(reg['audits']) if a['id']==proposal['id']]
assert len(matches)==1
reg['audits'][matches[0]]=proposal
regenerated=pub.roundtrip.semantic_reviewer_packet(proposal)
assert regenerated==packet,'Prospective audit does not regenerate the exact canonical reviewer packet'
actual_loader=pub.roundtrip.load_registry
try:
 pub.roundtrip.load_registry=lambda *args,**kwargs:reg
 pub.inputs.cache_clear();pub.load.cache_clear()
 pub.check_advance([proposal['lean']['declaration']],reviewed=True)
finally:
 pub.roundtrip.load_registry=actual_loader
 pub.inputs.cache_clear();pub.load.cache_clear()
print(json.dumps({'prospective_reviewed_publication_gate':'PASS','reviewer_packet_regenerated_exactly':True,'canonical_audit_unchanged':True,'ledger_unchanged':True,'scope':'In-memory exact target audit overlay; pub.check_advance(reviewed=True), no publication/frontier/source edits'},indent=2))
