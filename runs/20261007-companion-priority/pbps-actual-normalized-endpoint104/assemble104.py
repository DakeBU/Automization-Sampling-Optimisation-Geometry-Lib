from pathlib import Path
r=Path(__file__).resolve().parent
h=(r.parent/'pbps-normalized-endpoint-preread104/Header104.lean').read_text(encoding='utf8')
prefix=h.split('#check candidate')[0]
params=h.split('def candidate',1)[1].split(' : Prop := by',1)[0]
s=prefix+'\nset_option maxHeartbeats 1600000\nset_option maxRecDepth 10000\ntheorem assembly'+params+' : candidate hα hαβ hV hH hη hβη := by\n'+(r/'Body104.txt').read_text(encoding='utf8')+'\n#print axioms assembly\nend\nend PBPSNormalizedEndpointCandidate104\n'
(r/'Assembly104.lean').write_text(s,encoding='utf8',newline='\n')
