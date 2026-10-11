from pathlib import Path
import json,hashlib,copy,sys
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-weighted-density-preread101'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return info(p)
before=B/'pbps-actual-prescribed-weighted-density.before-index-clarification101.exactraw.snapshot.json'
after=R/'website/content/declaration_lessons/pbps-actual-prescribed-weighted-density.json'
authored=B/'authored-statement101.json';publication=R/'website/content/publications/pbps-actual-prescribed-weighted-density.json'
old=load(before);new=load(after);statement=load(authored)
oldtext=old['units'][0]['steps'][0]['text'];newtext=new['units'][0]['steps'][0]['text']
assert newtext=='Using zero-based Fin n coordinates (i=0,...,n-1), '+oldtext[0].lower()+oldtext[1:]
comparison=copy.deepcopy(new);comparison['units'][0]['steps'][0]['text']=oldtext;assert comparison==old
assert old['units'][0]['statement']==new['units'][0]['statement']==statement['statement']
assert '(rho(t))_i=T-t_(n+1-i) in one-based coordinates' in statement['statement']
assert new['units'][0]['steps'][0]['formula']=='\\rho(t)_i=T-t_{n-1-i},\\quad\\rho_{99}=\\rho_{100}.'
freeze=load(B/'publication-freeze101.json');packet=R/freeze['packet']['path'];assert info(packet)==freeze['packet']
assert info(before)['raw_sha256']==next(x['raw_sha256'] for x in freeze['inputs'] if x['path']==info(after)['path'])
prep=load(B/'independent-whole-math101/prepared-inputs101.native.json')
for key in ['production','header','seal']:assert info(R/prep[key]['path'])==prep[key]
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=load(publication)['items'][0];binding=pub.binding_digest(item,item['bindings'][0]);assert binding=='53fd5e8723d4680bad200242460cc94ef8cb5c17e07e751ba646eadc10ecd3b1'
inputs=[before,after,authored,publication,B/'publication-freeze101.json',packet,B/'independent-whole-math101/prepared-inputs101.native.json',B/'independent-whole-math101/whole-math-decision101.native.json']+[R/prep[k]['path'] for k in ['production','header','seal']]
decision=save('index-clarification-decision101.native.json',dict(kind='independent-narrow-exposition-index-clarification-review',reviewer='/root/exact_verifier96',decision='ACCEPT_INDEX_CONVENTION_CLARIFICATION',scope='Only this notation clarification; no overall source-fidelity, publication, decoder or VERIFIED verdict.',before=info(before),after=info(after),changed_json_paths=['units[0].steps[0].text'],before_text=oldtext,after_text=newtext,all_other_parsed_JSON_fields_identical=True,full_authored_statement_unchanged=True,index_equivalence={'zero_based':'For i in Fin n, i.rev has value n-1-i; reversed zero-based coordinate is T-t_zero[n-1-i].','one_based':'Write j=i+1 and t_zero[k]=t_one[k+1]. Then n-1-i=n-j, so T-t_zero[n-j]=T-t_one[n+1-j]. This is exactly the full statement formula for j=1,...,n.','n_zero':'There is no legal Fin0 coordinate; both coordinate assertions are vacuous, so the displayed n-1-i is never evaluated as an out-of-range index.','n_one':'i=0 maps to0; j=1 maps to1.','sufficiency':'The new text explicitly switches to zero-based Fin n coordinates immediately before the unchanged formula. The full statement explicitly uses one-based coordinates. Both now have local convention labels, resolving the ambiguity without altering the mathematics.'},repair_does_not_change=['step1 formula','adjacent exact Lean','complete authored mathematical statement','production proof','sealed Header101','anonymous decoder input'],unchanged_production=prep['production'],unchanged_header=prep['header'],unchanged_seal=prep['seal'],unchanged_decoder_input=info(packet),current_publication_binding_sha256=binding,compile_replayed=False,compile_reason='Prose-only clarification; unchanged fresh whole-production/sealed-header evidence retained.',defects_found=[],no_shared_mutations=True,no_overall_source_verdict=True))
closed=save('closed-RAW-index-clarification101.native.json',dict(kind='closed-independent-narrow-index-review101',inputs=[info(p) for p in inputs],files=[info(p) for p in sorted(O.iterdir()) if p.is_file()],closed=True,hash_algorithm='SHA256 exact RAW bytes',self_hash_intentionally_omitted=True))
print(json.dumps(dict(decision=decision,manifest=closed),indent=2))
