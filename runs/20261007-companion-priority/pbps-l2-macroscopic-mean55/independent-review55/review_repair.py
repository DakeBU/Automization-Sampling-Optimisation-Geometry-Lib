import copy, hashlib, json, pathlib, datetime

ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55'
OUT = BASE / 'independent-review55'
REPAIR = BASE / 'source-metadata-repair55'
ACTOR = 'phase_source_reviewer_20261005'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canon(d):
    return json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def logical(d, field):
    return sha(canon({k:v for k,v in d.items() if k != field}))

def loc(s):
    p = pathlib.Path(s)
    return p if p.is_absolute() else ROOT / p

def read(p):
    return json.loads(pathlib.Path(p).read_bytes())

def pin(p, label=None):
    p = pathlib.Path(p); b=p.read_bytes()
    try:
        b.decode('utf-8'); lf=sha(b.replace(b'\r\n', b'\n'))
    except UnicodeDecodeError:
        lf=None
    return {'path':label or p.relative_to(ROOT).as_posix(), 'bytes':len(b), 'raw_sha256':sha(b), 'lf_sha256':lf}

def verify(d, override=None):
    actual=pin(loc(override or d['path']), d['path'])
    for k in ('bytes','raw_sha256','lf_sha256'):
        if k in d:
            assert actual[k] == d[k], (d['path'], override, k, d[k], actual[k])
    return actual

def write(p,d):
    pathlib.Path(p).write_bytes(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8')+b'\n')

def differences(a,b,path=''):
    if type(a) != type(b): return [path]
    if isinstance(a,dict):
        if set(a)!=set(b): return [path+'/<keys>']
        return [q for k in a for q in differences(a[k],b[k],path+'/'+k)]
    if isinstance(a,list):
        if len(a)!=len(b): return [path+'/<length>']
        return [q for i in range(len(a)) for q in differences(a[i],b[i],path+'/'+str(i))]
    return [] if a==b else [path]

old = read(BASE/'source.0.review.json')
assert logical(old,'review_run_sha256') == old['review_run_sha256']
overlay = read(REPAIR/'overlay.json')
lease = read(REPAIR/'source.repair.review.lease.json')
assert lease['status']=='OPEN' and lease['compiler_lease']=='NOT_STARTED_CLOSED'
lease_bytes = (REPAIR/'source.repair.review.lease.json').read_bytes()
(OUT/'provided-opening.lease.raw.snapshot.json').write_bytes(lease_bytes)
packet = read(REPAIR/'source.1.reviewer-packet.json')
assert (REPAIR/'source.1.reviewer-packet.json').read_bytes() == (BASE/'source.0.reviewer-packet.json').read_bytes()
assert logical(packet,'packet_sha256') == packet['packet_sha256'] == lease['reviewer_packet_sha256']
current = [verify(d) for d in lease['input_artifacts']]
assert len(current)==321
assert len(old['input_artifacts'])==297
mapping = overlay['original_source_input_snapshot_mapping']
assert set(mapping) == {x['file'] for x in overlay['operations']}
historical = [verify(d,mapping.get(d['path'])) for d in old['input_artifacts']]
opchecks=[]
for i,op in enumerate(overlay['operations']):
    before=loc(op['before_pin']['path']); after=loc(op['after_pin']['path']); live=loc(op['file'])
    verify(op['before_pin']); verify(op['after_pin']); verify(op['current_pin'])
    bb=before.read_bytes(); ab=after.read_bytes()
    assert bb.count(op['before'].encode())==1
    assert bb.replace(op['before'].encode(),op['after'].encode(),1)==ab==live.read_bytes()
    assert differences(read(before),read(after))==[op['json_pointer']]
    assert mapping[op['file']]==op['before_pin']['path']
    saved=BASE/f'reviewer.source.input.{i+3:02}.raw.snapshot'
    assert saved.read_bytes()==bb
    other=loc(overlay['operations'][1-i]['before_pin']['path'])
    assert other.read_bytes()!=bb
    original=[d for d in old['input_artifacts'] if d['path']==op['file']]
    assert len(original)==1
    assert pin(other)['raw_sha256']!=original[0]['raw_sha256']
    assert not loc(op['before']).exists() and loc(op['after']).is_file()
    opchecks.append({'file':op['file'],'json_pointer':op['json_pointer'],
      'before':op['before'],'after':op['after'],'exact_literal_replacement':True,
      'exact_single_pointer':True,'mapping_matches_original_descriptor_and_owned_snapshot':True,
      'swapped_wrong_before_mapping_rejected':True,'current_after_bytes_match':True,
      'successor_inventory':pin(loc(op['after']))})

for k in ('negative','native_negative_run','native_negative_own_closed_lease','native_negative_provided_closed_lease'):
    verify(overlay[k])

pub = read(ROOT/'website/content/publications/pbps-l2-macroscopic-mean.json')['items'][0]
binding=pub['bindings'][0]
unit=read(ROOT/'website/content/declaration_lessons/pbps-l2-macroscopic-mean.json')['units'][0]
module=ROOT/packet['lean']['file']
fd=lambda p:sha(loc(p).read_text(encoding='utf-8').encode('utf-8'))
payload={'file':fd(module),'current_lean_module':module.read_text(encoding='utf-8'),
  'toolchain':fd('lean-toolchain'),'dependencies':fd('lake-manifest.json'),
  **{k:pub[k] for k in ('source','statement','formulae','assumptions','obligations')},
  'lesson':unit,'binding':{k:v for k,v in binding.items() if k not in {'audit_id','legacy_audit_debt'}}}
assert payload==read(BASE/'reviewer.source.binding-payload.json')
bh=sha(canon(payload))
assert bh==overlay['publication_binding_before']==overlay['publication_binding_after']==packet['publication_binding_sha256']
audit=read(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSL2MacroscopicMean.json')
assert audit['publication_binding_sha256']==bh
context=copy.deepcopy(payload)
context['binding']={k:context['binding'][k] for k in ('declaration','role','supports')}
context['lesson']={k:v for k,v in context['lesson'].items() if k not in {'boundary','source_history_boundary'}}
context['candidate_assumptions']=[{k:row[k] for k in ('source','lean')} for row in binding.get('assumption_deltas',[])]
assert context==packet['candidate_publication_context']==audit['publication_context']
assert packet['blind_reconstruction']==read(BASE/'source.0.reviewer-packet.json')['blind_reconstruction']
helper=ROOT/'tools/astis_publication.py'
helperpin=[d for d in old['input_artifacts'] if pathlib.Path(d['path']).name=='astis_publication.py']
assert len(helperpin)==1; verify(helperpin[0])
helperlines=helper.read_text(encoding='utf-8').splitlines()
(OUT/'helper47-115.raw.snapshot.py.txt').write_bytes(('\n'.join(helperlines[46:115])+'\n').encode('utf-8'))
write(OUT/'binding-payload.json',payload)
checks={'status':'PASSED_SCOPED_METADATA_ONLY','original297_all_verified':True,
  'historical_pin_count':len(historical),'unchanged_live_historical_pin_count':295,
  'current321_all_verified':True,'current_pin_count':len(current),'operations':opchecks,
  'original_negative_and_native_run_and_closed_leases_immutable':True,
  'packet_raw_bytes_unchanged':True,'native_blind_and_all_original_nonmetadata_pins_unchanged':True,
  'full_binding_payload_exact_original':True,'publication_binding_sha256':bh,
  'publication_context_and_audit_unchanged':True,'helper_scope':'physical47-115 only; no import/execution',
  'path_discovery':'Provided repair lease and source.1 packet reside in source-metadata-repair55/. Earlier assumed parent lease path yielded FileNotFoundError before source acceptance; no root files modified.',
  'source_or_math_change':False,'compiler_started':False,'whole_math_verdict_read':False,
  'historical_inputs_with_exact_before_mapping':historical,'current_inputs':current}
write(OUT/'checks.json',checks)
slots=copy.deepcopy(old['semantic_slots'])
slots['scopes']['evidence']='The original complete 248-line production, 107-line Tests and six-formula review is reused after all297 historical pins are matched (only publication/cell interpreted via exact immutable before snapshots). The two locator pointers now resolve the already admitted caller-inventory.after.json. This is separately reviewed metadata repair; no source/topology/mathematical route or boundary is changed.'
evidence='Independent metadata repair55 review: both JSON-pointer differences and exact literal path byte replacements checked against original descriptors/owned snapshots; swapped wrong-before mapping rejected. All297 historical and321 current strict raw/LF/byte pins verified. Original full seven-slot, complete-production/Test and six-formula source assessment reused only after unchanged scientific bytes/native blind/current packet comparison. Full canonical publication binding independently recomputed from authorized helper47-115 and equals3429f3b54edb1b9e40456d5f25677a1a54b4984f8d62aae273ce650e3b6ce862. Source0 metadata-only negative and native run/closed leases remain immutable. No compiler or whole-math verdict read; no new proof, decoder, topology, paper-completion or self-verification credit.'
receipt={'schema_version':1,'reviewer':ACTOR,'status':'ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_REPAIR',
  'verdict':'equivalent-after-elaboration','blocking':False,'source_or_math_change':False,
  'source_or_math_blocker':False,'source_excess':0,'semantic_slots':slots,'deltas':[],'repairs':[],
  'metadata_repair_status':'accepted-scoped-metadata-only','metadata_operations':opchecks,
  'reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':bh,
  'independent_from_formalizer':True,'independent_from_decoder':True,
  'review_evidence':evidence,'input_artifacts':current,
  'original_negative':pin(BASE/'source.0.review.json'),'original_negative_run':pin(BASE/'reviewer.source.run.json'),
  'root_authored_metadata_overlay':pin(REPAIR/'overlay.json'),'provided_opening_lease':pin(OUT/'provided-opening.lease.raw.snapshot.json'),
  'checks':pin(OUT/'checks.json'),'binding_payload':pin(OUT/'binding-payload.json'),
  'source_primary':old['source_primary'],'source_primary_logical_sha256':old['source_primary_logical_sha256'],
  'prior_topology_negative':old['prior_topology_negative'],'independent_repaired_topology':old['independent_repaired_topology'],
  'remaining_boundaries':old['remaining_boundaries'],
  'honest_exposure':'Earlier independently closed primary-before-candidate55, exact typed statement, original/repaired topology and complete source0 implementation/decoder/lesson review are explicit reuse. This distinct stage examines root-authored metadata repair, not historically blind reconstruction. No whole-math55 verdict read.',
  'hash_recipe':'review_run_sha256 = SHA256 UTF8 entire receipt minus review_run_sha256; ensure_ascii=False sort_keys=True separators=(comma,colon) allow_nan=False, no terminal newline.',
  'completed_utc':now()}
receipt['review_run_sha256']=logical(receipt,'review_run_sha256')
write(OUT/'source.1.review.json',receipt)
assert logical(read(OUT/'source.1.review.json'),'review_run_sha256')==receipt['review_run_sha256']
print(json.dumps({'receipt':pin(OUT/'source.1.review.json'),'review_run_sha256':receipt['review_run_sha256'],'binding':bh,'historical':297,'current':321,'own_and_provided_leases':'still OPEN until final immutable post-check and closure'},ensure_ascii=False))
