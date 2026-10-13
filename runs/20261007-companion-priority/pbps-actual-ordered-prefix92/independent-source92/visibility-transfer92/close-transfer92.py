import copy, datetime, hashlib, json, pathlib, re

ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
OLD = BASE / 'independent-source92'
OUT = OLD / 'visibility-transfer92'
MATH = BASE / 'independent-visibility92'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return sha(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
def load(p): return json.loads(p.read_text(encoding='utf8'))
def bind(p):
    p = pathlib.Path(p)
    if not p.is_absolute(): p = ROOT / p
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}
def write(name, value):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())
    return bind(p)

packetpath = BASE / 'anti-anchored.review92.v3.json'
oldpacket = load(BASE / 'anti-anchored.review92.v2.json')
packet = load(packetpath)
assert canonical({k:v for k,v in packet.items() if k != 'packet_sha256'}) == packet['packet_sha256'] == '7b020b19642277b05b46fce89625db4caa215f716b30c80d119cd8389afc6e0d'
assert bind(packetpath)['raw_sha256'] == '970c06a4d10530f3b60211eab59ef922360cb8d329e37c0e26e62dafd82a94e0'
module = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean'
raw = module.read_bytes(); text = module.read_text(encoding='utf8')
oldtext = oldpacket['candidate_publication_context']['current_lean_module']
oldraw = oldtext.replace('\n', '\r\n').encode()
assert sha(oldraw) == 'd9dd0ce17df285bc73f68906589c4e5c598472eb3ba49c0c21f420e17f904277'
needle = b'\ndef actual_ordered_prefix_statement\r\n'
assert oldraw.count(needle) == 1
assert raw == oldraw.replace(needle, b'\nprivate def actual_ordered_prefix_statement\r\n')
assert sha(raw) == '4737e98180ad69da03ad8b68f72f996ebe265b1eda1fafaa0521f591b7644ead'
assert text == packet['candidate_publication_context']['current_lean_module']
assert len(raw.splitlines()) == len(oldraw.splitlines()) == 1686
for k in packet:
    if k not in ['packet_sha256', 'publication_binding_sha256', 'candidate_publication_context']:
        assert packet[k] == oldpacket[k], k
oldcontext = copy.deepcopy(oldpacket['candidate_publication_context'])
oldcontext['current_lean_module'] = text
oldcontext['file'] = sha(text.encode())
for step in oldcontext['lesson']['steps']:
    step['lean_source_region']['source_raw_sha256'] = sha(raw)
assert oldcontext == packet['candidate_publication_context']

pubpath = ROOT / 'website/content/publications/pbps-actual-ordered-prefix.json'
lessonpath = ROOT / 'website/content/declaration_lessons/pbps-actual-ordered-prefix.json'
pub = load(pubpath)['items'][0]; lesson = load(lessonpath)['units'][0]
payload = {k: pub[k] for k in ['source', 'statement', 'formulae', 'assumptions', 'obligations']}
payload.update(file=sha(text.encode()), current_lean_module=text,
    toolchain=sha((ROOT/'lean-toolchain').read_text().encode()),
    dependencies=sha((ROOT/'lake-manifest.json').read_text().encode()),
    lesson=lesson, binding={k:v for k,v in pub['bindings'][0].items() if k not in {'audit_id','legacy_audit_debt'}})
assert canonical(payload) == packet['publication_binding_sha256'] == '5562848422a38455bcdd3fd7956692c4ac67b536b4b05e45382b7f2a68b1b43f'
sealpath = BASE/'root.statement-seal92.json'
expanded = text.split('def actual_ordered_prefix_statement',1)[1].split('\n\n\nset_option',1)[0]
assert expanded == load(sealpath)['expanded_literal_Prop'].rstrip('\n')
assert expanded.replace(' : Prop :=', ' :', 1) + '\n' == packet['lean']['statement']
assert oldraw.splitlines(keepends=True)[1553:1683] == raw.splitlines(keepends=True)[1553:1683]

oldmanifest = load(OLD/'closed-RAW92.native.json')
mutable = {bind(module)['path'], bind(pubpath)['path'], bind(lessonpath)['path']}
for item in oldmanifest['inputs'] + oldmanifest['outputs']:
    if item['path'] not in mutable: assert bind(item['path']) == item, item['path']
priorreport = load(OLD/'source-review92.native.json')
assert bind(pubpath) == priorreport['publication'], 'publication metadata changed beyond declared lesson rebind'
assert len(priorreport['semantic_slots']) == 7
assert len(priorreport['six_binder_audit']) == 6 and len(priorreport['definition_audit']) == 25

for receiptname in ['kernel.receipt.native.json', 'leaf-build.receipt.native.json']:
    receipt = load(MATH/receiptname)
    assert receipt['exit_code'] == 0 and receipt['terminal_closed']
    for k in ['source','lake_manifest','stdout','stderr']:
        b = receipt[k]; actual = bind(b['path'])
        assert actual['raw_sha256'] == b['raw_sha256'] and actual['bytes'] == b['bytes']
    assert receipt['source']['raw_sha256'] == sha(raw)
assert (MATH/'FreshPrivateStatementKernel92.lean').read_bytes().startswith(raw)
log = (MATH/'kernel.stdout.log').read_text(encoding='utf8')
axiom_match = re.search(r"'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law' depends on axioms: \[(.*?)\]", log, re.S)
assert axiom_match
assert [re.sub(r'\.\{[^}]+\}', '', s.strip()) for s in axiom_match.group(1).split(',')] == ['propext','Classical.choice','Quot.sound']
assert 'sorryAx' not in log
assert not re.search(r'\b(sorry|admit|axiom)\b', text)

primarypath = ROOT / priorreport['primary']['path']
primaryraw = primarypath.read_bytes()
assert sha(primaryraw) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
coverage = load(OLD/'source-proof-coverage92.native.json')
assert (coverage['node_count'],coverage['edge_count'],coverage['coverage_count']) == (29,57,46)
for row in coverage['coverage']:
    source = row['source_region']
    assert sha(primaryraw[source['byte_start']:source['byte_end_exclusive']]) == source['raw_sha256']

region_count = 0
def rebind_regions(value):
    global region_count
    if isinstance(value, dict):
        if value.get('path') == bind(module)['path'] and 'start_line' in value:
            a,b = value['start_line'],value['end_line']
            oldregion = b''.join(oldraw.splitlines(keepends=True)[a-1:b])
            newregion = b''.join(raw.splitlines(keepends=True)[a-1:b])
            assert sha(oldregion) == value['exact_code_raw_sha256']
            assert newregion == oldregion.replace(needle,b'\nprivate def actual_ordered_prefix_statement\r\n') or newregion == oldregion
            value['source_raw_sha256'] = sha(raw)
            value['exact_code_raw_sha256'] = sha(newregion)
            region_count += 1
        for x in value.values(): rebind_regions(x)
    elif isinstance(value,list):
        for x in value: rebind_regions(x)
rebind_regions(coverage)
coverage['packet_sha256'] = packet['packet_sha256']; coverage['module'] = bind(module)
coverage['record_kind'] = 'source-proof-coverage-visibility-delta-transfer'
coverage['transfer'] = {'prior_coverage':bind(OLD/'source-proof-coverage92.native.json'),
    'basis':'Exact whole-module byte substitution only adds private to the Prop abbreviation; every source region and implementation region rehashed. All 29 node dispositions, 57 edge interpretations, 46 rows, AND/OR routes and future open boundaries retained.',
    'implementation_region_occurrences_rechecked':region_count,'source_regions_rechecked':46,'topology_changed':False}
coveragebinding = write('source-proof-coverage92.v3.native.json',coverage)

exposition = load(OLD/'exposition-review92.native.json')
for i,(step,audit) in enumerate(zip(lesson['steps'],exposition['steps'])):
    region = step['lean_source_region']; a,b = region['start_line'],region['end_line']
    exact = b''.join(raw.splitlines(keepends=True)[a-1:b])
    assert sha(exact) == region['exact_code_raw_sha256'] == audit['body_region']['exact_code_raw_sha256']
    assert exact.decode().rstrip() == step['lean']
    assert sha(step['lean'].encode()) == audit['display_lean_sha256']
    assert step['formula'] == audit['formula']
    audit['body_region'] = region; audit['lesson_raw_sha256'] = bind(lessonpath)['raw_sha256']
assert len(lesson['steps']) == len(exposition['steps']) == 10
exposition.update(record_kind='exposition-visibility-delta-transfer',packet_sha256=packet['packet_sha256'],
    publication_binding_sha256=packet['publication_binding_sha256'],module=bind(module),lesson=bind(lessonpath),publication=bind(pubpath))
exposition['transfer'] = {'prior_exposition':bind(OLD/'exposition-review92.native.json'),
    'mathematical_reader_fields_unchanged':True,'ten_BODY_regions_byte_identical':True,
    'change':'Only whole-module provenance SHA changes in the ten region records. Prop abbreviation visibility is outside those ten BODY regions. Expanded public theorem, all six assumptions, 25 literal definitions and reader mathematical proof remain unchanged.',
    'source_repair_required':False,'rendered_page_inspected':False}
expositionbinding = write('exposition-review92.v3.native.json',exposition)

inputs = list(dict.fromkeys([x['path'] for x in oldmanifest['inputs']] +
    [x['path'] for x in oldmanifest['outputs']] + [bind(OLD/'closed-RAW92.native.json')['path'],bind(packetpath)['path']] +
    [bind(MATH/f)['path'] for f in ['kernel.receipt.native.json','leaf-build.receipt.native.json',
    'kernel.stdout.log','kernel.stderr.log','leaf-build.stdout.log','leaf-build.stderr.log','FreshPrivateStatementKernel92.lean','static-audit92.native.json']]))
transfer = {'only_source_change':'line1458: def actual_ordered_prefix_statement -> private def actual_ordered_prefix_statement',
    'old_module_sha256':sha(oldraw),'new_module_sha256':sha(raw),'whole_raw_substitution_verified':True,
    'public_theorem_raw_bytes_unchanged':True,'sealed_expanded_Prop_identical':True,
    'six_original_assumptions_identical':True,'all25_literal_definitions_identical':True,
    'anonymous_packet_and_reconstruction_identical':True,'all_mathematical_proof_expressions_identical':True,
    'all_natural_mathematical_exposition_identical':True,'source_graph_topology_unchanged':True,
    'source_repair_required':False,'new_mathematical_claim':False}
run = write('review-run92.v3.native.json',{'record_kind':'independent-source-exposition-visibility-transfer-run',
    'reviewer':'/root/primary_source91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'canonical_packet_sha256':packet['packet_sha256'],'packet_raw_sha256':bind(packetpath)['raw_sha256'],
    'publication_binding_sha256':packet['publication_binding_sha256'],'inputs':[bind(p) for p in inputs],
    'prior_run':bind(OLD/'review-run92.native.json'),
    'chronology':'Fresh primary-first92 freeze and independent v2 whole-source/decoder/exposition audit remain immutable. This v3 run independently verifies exact visibility-only change and transfers that established mathematical review; it is not a new blind reconstruction or a new primary-first claim.',
    'independence':'Distinct from formalizer and decoder. Kernel/leaf receipts checked directly; another reviewer verdict is not used as source authority.',
    'compiler_scope':'Fresh kernel exact production prefix, closed exit0 kernel and leaf receipts, standard axiom list and source token scan checked. No compile rerun or whole-project gate claimed.',
    'transfer':transfer,'preclosure_script_diagnostic':'First local validation stopped before emitting outputs because the axiom parser did not strip printed universe suffixes .{u}; parser corrected. Exact normalized axiom set is unchanged.', 'no_canonical_mutation':True})

report = copy.deepcopy(priorreport)
report.update(record_kind='independent-anti-anchored-source-exposition-visibility-transfer',
    reviewer_packet_sha256=packet['packet_sha256'],reviewer_packet_raw_sha256=bind(packetpath)['raw_sha256'],
    publication_binding_sha256=packet['publication_binding_sha256'],review_run_sha256=run['raw_sha256'],review_run_binding=run,
    module=bind(module),publication=bind(pubpath),lesson=bind(lessonpath),source_proof_coverage=coveragebinding,exposition_audit=expositionbinding)
for slot in report['semantic_slots'].values():
    assert all(slot.get(k) for k in ['original','reconstructed','relation','evidence'])
    slot['evidence'] += ' V3 transfer: exact public theorem/expanded Prop, original six binders, all literal definitions and full anonymous reconstruction unchanged; independently byte-checked against v2.'
report['actual_proof_audit']['scope'] = 'Whole mathematical source review transferred from immutable v2 after independent exact full-module visibility-only byte comparison; all bound source/proof regions rehashed.'
report['actual_proof_audit']['kernel_receipt'] = bind(MATH/'kernel.receipt.native.json')
report['actual_proof_audit']['kernel_log'] = bind(MATH/'kernel.stdout.log')
report['actual_proof_audit']['leaf_receipt'] = bind(MATH/'leaf-build.receipt.native.json')
report['visibility_transfer'] = transfer
report['prior_source_review'] = bind(OLD/'source-review92.native.json')
report['review_evidence'].append('V3 exact command-visibility-only substitution; immutable v2 reasoning transferred with new packet/publication/RAW/compiler bindings.')
assert report['repairs'] == []
reportbinding = write('source-review92.v3.native.json',report)
manifest = write('closed-RAW92.v3.native.json',{'record_kind':'closed-RAW-independent-source-exposition-visibility-transfer',
    'reviewer':'/root/primary_source91','canonical_packet_sha256':packet['packet_sha256'],
    'publication_binding_sha256':packet['publication_binding_sha256'],'inputs':[bind(p) for p in inputs],
    'outputs':[coveragebinding,expositionbinding,run,reportbinding,bind(OUT/'close-transfer92.py')],
    'closure':'Every listed current input and output rehashed after emission. All old owned files preserved; old production and lesson provenance remains in immutable v2 receipts/packet. This transfer changes no source topology or canonical status. Manifest self-hash reported externally.'})
for item in load(OUT/'closed-RAW92.v3.native.json')['inputs']+load(OUT/'closed-RAW92.v3.native.json')['outputs']:
    assert bind(item['path']) == item
print(json.dumps({'report':reportbinding,'run':run,'coverage':coveragebinding,'exposition':expositionbinding,'closed_manifest':manifest},indent=2))
