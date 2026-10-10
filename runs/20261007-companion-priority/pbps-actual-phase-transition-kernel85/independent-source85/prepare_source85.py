"""Source-first preparation ONLY. Does not open final implementation/publication/decoder packet."""
from pathlib import Path
from html.parser import HTMLParser
import ast,datetime,hashlib,json
ROOT=Path('E:/Samplinglib');PRE=ROOT/'runs/20261007-companion-priority/pbps-transition-kernel-preread85';OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parser_source=PRE/'freeze_preread85.py';cl=next(n for n in ast.parse(parser_source.read_text(encoding='utf-8')).body if isinstance(n,ast.ClassDef) and n.name=='SourceHTML')
ns={'HTMLParser':HTMLParser};exec(compile(ast.Module(body=[cl],type_ignores=[]),str(parser_source),'exec'),ns)
h=ns['SourceHTML']();h.feed(primary.read_text(encoding='utf-8'))
expected={
 'source-first-notes85.json':'9e9e3737db6cc73e351ffe7daa8ad7dbb124e546f1378a25372ae0dab36fa1c1',
 'source-first-seal85.json':'be71b20e9f50107ce24dc4ecb21f326352046482081c16d95554400487704b47',
 'source-first-run-manifest85.json':'e2685c8e1b1ebf4ab292367526da053471100107dd60c32afc418125202d6ef0',
 'source-inventory85.json':'b22c1c1cb9c6f2ff86d7182b6821f003058ca101684507ad97873c3a63d50730',
 'source-proof-graph85.json':'cff28b7b0581c3b5b0219063e422d7b3b70e738ded0e673b035dd73ac32a81be',
 'source-inventory85.reviewed-effective.json':'bfb2c488d895ef1b3ff488d2f9e51e06e47ea5df9fcf3d4124ab225ffc0e52ee',
 'source-proof-graph85.reviewed-effective.json':'2e075d018bd310a9ecb0068e5d98bdaf01d5cf8e623e986a9b071e82b59f1f04',
 'candidate-recommendation85.json':'90182e93f3ab3dec8fafab021d02db490020fc0e92af55d922748ed5e2a8ff53',
 'independent-topology85/proposed-minimal-topology-overlay85.json':'0d4911d3f7f495bc7b1a8f9c944eaaf64032a0ddc3c62b57266440a13e8441d9'
}
for p,v in expected.items():assert pin(PRE/p)['raw_sha256']==v,p
oi=read(PRE/'source-inventory85.json');i=read(PRE/'source-inventory85.reviewed-effective.json');g=read(PRE/'source-proof-graph85.reviewed-effective.json')
original_anchors=oi['anchors']+oi['additional_anchor_pins'];effective_anchors=i['anchors']+i['additional_anchor_pins']
for a in effective_anchors:assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256'],a['source_id']
assert len(original_anchors)==28 and len(effective_anchors)==31
assert len(i['items'])==16 and len(g['nodes'])==21 and len(g['edges'])==29
assert sum(e['dependency_edge'] for e in g['edges'])==26
future=[e['id'] for e in g['edges'] if e['classification']=='FUTURE_OPEN'];excluded=[e['id'] for e in g['edges'] if not e['dependency_edge']]
assert len(future)==6 and len(excluded)==3
obj={'schema':'astis.source-first-prepacket-preparation85.v1','status':'SOURCE_FIRST_READY_WAITING_FOR_CANONICAL_PACKET','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/fresh_source78','primary_raw':pin(primary),'raw_inputs':[pin(primary),pin(parser_source),*[pin(PRE/p) for p in expected]],'source_first_chronology':'Primary raw was reread and authenticated before any final implementation/publication/reconstruction packet. Original independent preread85 bytes and reviewed-effective topology were rechecked. This is only preparation; no final semantic verdict is issued.','primary_anchors_original':28,'primary_anchors_effective':31,'anchor_count_explanation':'The original freeze has25 main+3 additional pins=28. The exact distinct-reviewed overlay adds A1.E7/A1.E8/p5.1, so reviewed-effective inventory contains31 independently checked unique pins; p4.4 was already among original28.','anchor_verification':[dict(a,independently_reparsed_exact_match=True) for a in effective_anchors],'coverage_counts':{'inventory':16,'nodes':21,'relations':29,'dependencies':26,'future_OPEN_dependencies':6,'excluded_associations':3},'future_OPEN_edges':future,'excluded_associations':excluded,'independent_source_expectations':[
 'Original six analytic assumptions and eleven literal definitions; same actual joint Z and actual iidExp1 P must bind every kernel law and test integral.',
 'Finite-time jointly indexed full-phase kernel, exact actual map/event laws, fixed-parameter AE init implies Dirac0, bounded Borel test integrability and clock expectation transfer. No arbitrary supplied process/law/measurability premise.',
 'Source terminal-pi failed-limit0 and total all-finite uncovered-initial-phase fallback are distinct conventions; only per-fixed-parameter AE law compatibility. Rank0, zero waits on exceptional inputs, infinite last-live arc and stopped dummy auxiliary branch remain explicit.',
 'IsMarkovKernel means probability fibers, not process Markov/restart/Chapman-Kolmogorov. K is optional representation of future invariance, not necessary invariance premise.',
 'Selected id×const/map AND ingredients are route-local; direct parameter integral remains unselected alternative. All path-law/reversal/invariance/AE-safe Jensen/fullL2 independent density/main/cost obligations stay OPEN.',
 'Final packet-bound review must compare all seven semantic slots, full exact module, all six authored formula/BODY regions, full attributed statement/nine conditions/four formulae and every16/21/29 source entry.'
 ],'final_packet_read':False,'final_implementation_or_publication_read':False,'anonymous_decoder_files_read':False,'other_math_verdicts_or_root_adoption_reports_read':False,'final_review_verdict':None,'no_shared_or_production_writes':True,'originals_unchanged':True,'extraction_author_role_disclosed':True,'self_approval_of_original_graph':False}
p=OUT/'prepacket-preparation85.json';assert not p.exists();p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
for name,v in expected.items():assert pin(PRE/name)['raw_sha256']==v
print(json.dumps({'preparation':pin(p),'script':pin(Path(__file__)),'counts':obj['coverage_counts'],'original_anchor_count':28,'effective_anchor_count':31,'status':obj['status']},indent=2))
