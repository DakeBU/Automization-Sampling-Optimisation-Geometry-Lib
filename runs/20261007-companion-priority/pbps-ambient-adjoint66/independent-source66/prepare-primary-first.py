from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,re,datetime,os
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-source66');S=O.parent.parent/'pbps-ambient-adjoint-preproof66'/'independent-primary66';H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
start=datetime.datetime.now(datetime.timezone.utc).isoformat();src=Path(r'E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html');raw=src.read_bytes();assert H(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parents=[]
for n in ['lease.final.json','owned-manifest.json','source-proof-graph.json','source-coverage-inventory.json','binder-definition-contract.json','source-input-regions.json','residual-next-header.json','seven-source-semantic-slots.json','process-and-truth-boundary.json']:
 p=S/n;parents.append(pin(p));(O/('adopted-primary66.'+n)).write_bytes(p.read_bytes())
assert H((S/'source-proof-graph.json').read_bytes())=='856a36c1bfa30c15e31345e096c18f6de17ccca826b403886b8d519a37994f51'
assert H((S/'source-coverage-inventory.json').read_bytes())=='463d46dec9adb44d2c094b0ff6ab64909217ec134b5a4d4f7b4317597fea68ef'
regions=json.loads((S/'source-input-regions.json').read_bytes())['regions'];inventory=json.loads((S/'source-coverage-inventory.json').read_bytes());items=inventory['math_items'];found=[];regionpins=[]
for r in regions:
 a,b=r['source_RAW_range_end_exclusive'];chunk=raw[a:b];assert H(chunk)==r['RAW_sha256'];assert chunk==(S/(r['name']+'.raw.html')).read_bytes();(O/('source.'+r['name']+'.RAW.html')).write_bytes(chunk);(O/('source.'+r['name']+'.LF.html')).write_bytes(chunk.replace(b'\r\n',b'\n'));(O/('source.'+r['name']+'.rendered.txt')).write_bytes((S/(r['name']+'.rendered.txt')).read_bytes())
 for m in re.finditer(rb'<math\b.*?</math>',chunk,re.S):found.append((a+m.start(),a+m.end()))
 regionpins.append(dict(**r,current_RAW=pin(O/('source.'+r['name']+'.RAW.html')),current_LF=pin(O/('source.'+r['name']+'.LF.html'))))
class P(HTMLParser):
 def __init__(self):HTMLParser.__init__(self,convert_charrefs=True);self.alt=None;self.inann=False;self.ann=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='math':self.alt=d.get('alttext')
  if tag=='annotation' and d.get('encoding')=='application/x-tex':self.inann=True
 def handle_endtag(self,tag):
  if tag=='annotation':self.inann=False
 def handle_data(self,s):
  if self.inann:self.ann.append(s)
missing_alt=missing_ann=mismatch=0
for it in items:
 a,b=it['RAW_byte_range'];frag=raw[a:b];assert H(frag)==it['raw_math_sha256'];p=P();p.feed(frag.decode('utf-8'));ann=''.join(p.ann);missing_alt+=p.alt is None;missing_ann+=not ann;mismatch+=p.alt!=ann;assert p.alt==it['alttext'] and ann==it['annotation_tex']
assert len(items)==len(found)==310 and set(found)==set(tuple(x['RAW_byte_range']) for x in items)
assert missing_alt==missing_ann==mismatch==0
put('primary-first-adoption.json',dict(schema='source66-PRIMARY-FIRST-frozen-contract-adoption-v1',first_primary_read=json.loads((O/'lease.open.json').read_bytes()),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_source_read_pid=os.getpid(),source_stage_started_utc=start,whole_primary_pin=pin(src),closed_primary66_parents=parents,source_graph_frozen_before_header66=True,region_maps=regionpins,all_selected_math_items=310,all_310_literal_RAW_math_pins_rechecked=True,all_310_alttext_annotation_pairs_rechecked=True,missing_alttext=missing_alt,missing_annotation=missing_ann,annotation_mismatch=mismatch,selected_source_inventory_complete=True,whole_paper_inventory_claim=False,candidate_or_decoder_seen=False,source_graph_independent_of_Lean_topology=True))
put('source-first-reconstruction.json',dict(schema='source66-independent-primary-reconstruction-before-current-candidate-v1',candidate_seen=False,source_graph='adopted-primary66.source-proof-graph.json',contract='adopted-primary66.binder-definition-contract.json',core=['Original inputs only: finite real Euclidean/Hilbert-Borel presentation, C2 V, global Hessian sandwich 0<alpha<=beta, eta>0 and beta*eta<=1 inclusive.','P is actual conditional expectation given Y; HP=range P and Hperp=ker P is conditional centering, not mere global mean zero.','Printed B maps HP to Hperp and B* intrinsically maps Hperp to HP. Ambient B into joint L2 and ambient B* from joint L2 are inclusion/adjoint adapters.','Same inherited GammaP,Gamma0,HP0,inverse,B0,V0 must be retained; inverse only centered HP0, full root kills constants.','For every joint g, ambient B*g belongs HP0 and equals i0(B0*((I-P)g typed in kerP)); constant annihilation and duality are derived ingredients, not premises.','For every globally centered joint f, fP=Pf belongs same HP0, fperp=f-Pf belongs exact kerP, fV=V0*fperp belongs same HP0. Ambient B*fperp=i0 Gamma0 fV=GammaP(i0 fV).','Orthogonal decomposition gives norm-square budget and V0* contraction; V0 is not asserted onto Hperp.'],source_boundaries=dict(B20='Only common-HP0 domain preparation; no full corrector bound',B21=False,B17=False,H1_B13_B14_floor='No new premise or newly proved result',dynamics=False,main_theorem=False,expected_query_cost=False,composition=False,rank_zero='Inherited disclosed extension remains legal',alpha_eta_one='Legal endpoint; no strictness introduced'),proof_ingredients_are_DAG_parents_not_public_premises=True,full_Exposition=False,PURIFIED=False))
print(json.dumps(dict(source_stage_pid=os.getpid(),source_items=310,regions=6,missing_alttext=missing_alt,missing_annotation=missing_ann,annotation_mismatch=mismatch,candidate_seen=False),sort_keys=True))