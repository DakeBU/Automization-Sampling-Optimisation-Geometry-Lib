"""Project exact canonical packet labels; retain physical input custody originals."""
from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
audits=[json.loads(A.read_bytes()),json.loads((W/'private-consumer-audit.reconstructed.v1.json').read_bytes())]
records=[]
for a,n in zip(audits,['anon_328a','anon_96ec']):
 root=Path('.astis/semantic-neutral-20261113')/n
 packet=json.loads((root/'input.json').read_bytes());r=json.loads((root/'result.json').read_bytes())
 physical=r['input_artifacts'];assert len(physical)==1
 assert Path(physical[0]['path']).resolve()==(root/'input.json').resolve()
 assert (physical[0].get('sha256') or physical[0].get('byte_sha256'))==sha((root/'input.json').read_bytes())
 assert packet==rt.decoder_packet(a)
 assert a['reconstruction']['input_artifacts']==physical
 a['reconstruction']['input_artifacts']=packet['input_artifacts']
 records.append({'decoder':r['decoder'],'unchanged_result_sha256':sha((root/'result.json').read_bytes()),'unchanged_decoder_run_sha256':r['decoder_run_sha256'],'physical_input_custody':physical,'canonical_input_artifacts':packet['input_artifacts'],'qualification':'Canonical schema labels projected from exact byte-verified anonymous packet; original decoder result and reconstruction unchanged. ROOT supplies no mathematical or fidelity verdict.'})
create(W/'public-reconstructed-pre-input-projection.original.json',A.read_bytes())
A.write_bytes(dump(audits[0]));create(W/'private-consumer-audit.reconstructed.v2.json',dump(audits[1]));create(W/'private-consumer-registry.reconstructed.v2.json',dump({'schema_version':1,'audits':[audits[1]]}))
create(E/'decoder-originals/input-metadata-projection.json',dump({'records':records,'tooling_qualification':'The existing CLI publication packet has no --output flag; failed argument-dispatch receipt is preserved, followed by the corrected actual call. Followup to T decoder for metadata-only custody addendum was rejected by collaboration thread limit; no repeated call or fabricated delivery. Root independently verifies both original input-file hashes above.'}))
print(json.dumps({'canonical_inputs_projected':2,'decoder_result_and_text_mutations':0,'ROOT_semantic_verdicts':0,'fresh_reviewer_packets_unchanged':all(rt.semantic_reviewer_packet(a)==json.loads((W/f'fresh-{tag}-review.v1.json').read_bytes()) for a,tag in zip(audits,['P','T']))}))
