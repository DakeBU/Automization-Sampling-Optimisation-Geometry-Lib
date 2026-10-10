import base64, datetime, hashlib, html, json, os, pathlib, re
from html.parser import HTMLParser

out=pathlib.Path(__file__).resolve().parent
prior=pathlib.Path(r'E:\Samplinglib\runs\20261007-companion-priority\pbps-first-corrector-energy-preproof67\independent-primary67')
def sha(b): return hashlib.sha256(b).hexdigest()
def put(name,d): (out/name).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def pin(name,b): return dict(name=name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
regions=json.loads((prior/'source-input-regions.json').read_bytes())
payload_bytes=(prior/'RAW-input-payload.json').read_bytes()
payload=json.loads(payload_bytes)
inventory=json.loads((prior/'source-coverage-inventory.json').read_bytes())
lease_bytes=(prior/'lease.final.json').read_bytes()
lease=json.loads(lease_bytes)
manifest_bytes=(prior/'owned-manifest.json').read_bytes()
manifest=json.loads(manifest_bytes)
assert sha(manifest_bytes)==lease['manifest_RAW_sha256']
assert sha(payload_bytes)==lease['SEPARATE_COMPLETE_RAW_INPUT']['RAW_sha256']
assert lease['status']=='CLOSED_LAST' and lease['owned_file_count']==59 and lease['postclose_writes_permitted'] is False
opaque=[]
for x in manifest['regular_file_entries']:
    b=(prior/x['name']).read_bytes()
    assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256'],x['name']
    opaque.append(dict(name=x['name'],RAW_sha256=sha(b),verified=True,content_reviewed=False))
assert len(opaque)==57
assert len([p for p in prior.iterdir() if p.is_file()])==59
logical_bytes=(prior/'review-run.json').read_bytes()
logical=json.loads(logical_bytes)
assert 'run_sha256' in logical
prior_embedded=logical.pop('run_sha256')
logical_hash=sha(json.dumps(logical,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
assert logical_hash==lease['whole_logical_run_sha256']==prior_embedded
whole_path=pathlib.Path(regions['whole_primary']['path'])
whole=whole_path.read_bytes()
assert len(whole)==1482128 and sha(whole)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'

class Render(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]; self.math=0
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='math':
            self.math+=1
            self.parts.append(' ['+a.get('id','')+': '+a.get('alttext','')+'] ')
        elif not self.math and t in ('p','div','h2','h3','h4','table','tr'): self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='math': self.math-=1
        elif not self.math and t in ('p','div','h2','h3','h4','table','tr'): self.parts.append('\n')
    def handle_data(self,d):
        if not self.math: self.parts.append(d)

source_inputs=[]; items=[]; region_records=[]
old_by_id={x['id']:x for x in inventory['math_items']}
for r in regions['regions']:
    name='source.'+r['name']+'.RAW.html'
    b=(prior/name).read_bytes()
    a,z=r['source_RAW_range_end_exclusive']
    assert whole[a:z]==b and sha(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes']
    supplied=[x for x in payload['inputs'] if x.get('pin',{}).get('name')==name]
    assert len(supplied)==1 and base64.b64decode(supplied[0]['complete_RAW_bytes_base64'])==b
    (out/name).write_bytes(b)
    lf=b.replace(b'\r\n',b'\n')
    (out/name.replace('.RAW.','.LF.')).write_bytes(lf)
    source_inputs.extend([pin(name,b),pin(name.replace('.RAW.','.LF.'),lf)])
    parser=Render(); parser.feed(b.decode('utf-8'))
    rendered='\n'.join(s.strip() for s in ''.join(parser.parts).splitlines() if s.strip())+'\n'
    (out/('source.'+r['name']+'.rendered.txt')).write_text(rendered,encoding='utf-8')
    count=0
    for m in re.finditer(rb'<math\b[^>]*>.*?</math>',b,re.S):
        raw=m.group(); tag=raw[:raw.index(b'>')+1]
        attrs={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([\w:-]+)="([^"]*)"',tag)}
        ident=attrs.get('id'); alt=attrs.get('alttext')
        annotation=re.search(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',raw,re.S)
        tex=html.unescape(annotation.group(1).decode('utf-8')) if annotation else None
        assert ident and alt is not None and tex==alt
        old=old_by_id[ident]
        assert old['RAW_sha256']==sha(raw) and old['source_RAW_range_end_exclusive']==[a+m.start(),a+m.end()]
        items.append(dict(id=ident,region=r['name'],alttext=alt,annotation_tex=tex,
            RAW_bytes=len(raw),RAW_sha256=sha(raw),source_RAW_range_end_exclusive=[a+m.start(),a+m.end()],
            region_RAW_range_end_exclusive=[m.start(),m.end()],source_role='pending-independent-classification'))
        count+=1
    assert count==r['math_count']
    region_records.append(dict(r,independently_reparsed_math_count=count,bytes_exact=True))
assert len(items)==344 and len(old_by_id)==344
metadata=[]
for name in ['source-input-regions.json','RAW-input-payload.json','source-coverage-inventory.json','lease.final.json','owned-manifest.json']:
    b=(prior/name).read_bytes()
    local='upstream-primary67.'+name
    (out/local).write_bytes(b)
    metadata.append(pin(local,b))
put('source-input-regions.json',dict(schema='primary69-exact-six-region-RAW-LF-map-v1',regions=region_records,
    regions_end_exclusive=True,whole_primary=pin(str(whole_path),whole),source_before_candidate=True))
put('source-coverage-inventory.json',dict(schema='primary69-source-only-reparsed-six-regions-v1',count=len(items),
    complete_finite_selection=True,whole_paper_inventory_claim=False,prior_classifications_used=False,
    math_items=items,source_before_candidate=True,missing_math_ids=0,annotation_mismatch=0))
put('prior-CLOSED59-source-provenance-verification.json',dict(schema='primary69-opaque-prior-closure-check-v1',
    actual_pid=os.getpid(),expected_status='CLOSED_LAST',owned_count=59,regular_entries_verified=57,
    manifest=pin('upstream-primary67.owned-manifest.json',manifest_bytes),lease=pin('upstream-primary67.lease.final.json',lease_bytes),
    complete_input_hash_verified=True,whole_logical_hash_verified=logical_hash,deleted_only_top_level_run_sha256=True,
    opaque_content_not_reviewed=True,opaque_checks=opaque,
    source_verification=dict(regions=6,math_elements=344,all_match_fixed_primary=True,all_match_supplied_payload=True),
    whole_primary=pin(str(whole_path),whole)))
put('source-read-process.json',dict(schema='primary69-first-source-process-v1',actual_pid=os.getpid(),
    start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_before_candidate=True,
    candidate_or_Lean_content_reviewed=False,upstream_non_HTML_payload_entries_not_decoded=True,
    predecessor_verdicts_not_reviewed=True,exact_source_inputs=source_inputs,exact_metadata_inputs=metadata))
print(json.dumps(dict(pid=os.getpid(),source_regions=6,math_elements=len(items),all_344_exact=True,
    prior_CLOSED59_verified=True,whole_primary_RAW_bytes=len(whole),whole_primary_RAW_sha256=sha(whole)),sort_keys=True))
