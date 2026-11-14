from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
BASE = ROOT / '.astis/semantic-neutral-20261112/ri_src_5ab9'
OUT = BASE / 'phase4_review'
EVIDENCE = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence'
DEST = EVIDENCE / 'source-review/ri_src_5ab9'
ACTOR = '/root/row_indep_fresh_source_5ab9'
COMMIT = '66e0bb9b748d68816a8443d60696656c9340222f'

def rel(path):
    return str(path.relative_to(ROOT))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canonical(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def info(path):
    b = path.read_bytes()
    return {'path': rel(path), 'bytes': len(b), 'sha256': sha(b)}

def write_json(path, value):
    b = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    if path.exists():
        assert path.read_bytes() == b, f'Would overwrite non-identical output: {path}'
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b)

packet_path = EVIDENCE / 'anti-anchored-reviewer-packet.json'
packet = json.loads(packet_path.read_bytes())
assert info(packet_path)['sha256'] == 'a6e3f3842a3ec25ab8d94eefb4b90701f68e70f95715e9c94ac294f815dd168a'
assert canonical({k:v for k,v in packet.items() if k != 'packet_sha256'}) == packet['packet_sha256'] == '51f818cce1189763710d937ce87ef07808c728984c5f93f7da4279054b037210'
assert packet['publication_binding_sha256'] == 'd90576df8ae217ca7cb9ce631cdca049780f3a706510afbe2f72a71dd1c03829'

source_map_path = EVIDENCE / 'source-lean-map.draft.json'
assert info(source_map_path)['sha256'] == '6d4aea4726db237433e458bc5c31252da88f4724013c9b50570a26dbfd2ceeb0'
source_map = json.loads(source_map_path.read_bytes())
lesson_path = ROOT / 'website/content/declaration_lessons/huanjian-gaussian-source-row-independence.json'
publication_path = ROOT / 'website/content/publications/huanjian-gaussian-source-row-independence.json'
lesson = json.loads(lesson_path.read_bytes())['units'][0]
item = json.loads(publication_path.read_bytes())['items'][0]
code_manifest_path = BASE / 'phase3-code-only-inputs-v1/input-manifest.json'
code_manifest = json.loads(code_manifest_path.read_bytes())
assert info(code_manifest_path)['sha256'] == '7278908beb43ab9963a69deb4510baf4aee49d752d1c09073ae4d1ae3876e3d5'
code = {}
for entry in code_manifest['inputs']:
    path = ROOT / entry['copy']
    b = path.read_bytes()
    assert len(b) == entry['bytes'] and sha(b) == entry['sha256']
    code[entry['source']] = b

prior_manifests = [
    (BASE / 'freeze_bundle_manifest.json', 'aaf7e9ecaf12d8c63141a169b1c9771308f0adc87cc4162431d57ebc5666c51e', 'artifact_hashes'),
    (BASE / 'phase2_type_only/freeze_bundle_manifest.json', '11d664970528fd2f3d100f5e584005e5aca7079f6e03cbb81086c8a4efab4875', 'artifacts'),
    (BASE / 'phase3_code_only/freeze_bundle_manifest.json', 'd600052e9402c59c132c0ac71c4e01187f0e0c239443d9094c32fe37c52d0712', 'artifacts'),
]
verified_prior = []
for path, expected, key in prior_manifests:
    assert info(path)['sha256'] == expected
    value = json.loads(path.read_bytes())
    for entry in value[key]:
        p = ROOT / entry['path']
        assert str(p).startswith(str(BASE) + '/')
        assert info(p)['sha256'] == entry['sha256']
        verified_prior.append(info(p))
    verified_prior.append(info(path))

raw_exposure = json.loads((BASE / 'input_exposure_manifest.json').read_bytes())
for entry in raw_exposure['required_instruction_inputs']:
    assert info(ROOT / entry['path'])['sha256'] == entry['sha256']
raw_path = ROOT / raw_exposure['raw_source_input']['path']
raw = raw_path.read_bytes()
assert sha(raw) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'

decoder_dir = EVIDENCE / 'decoder-originals/n_decode_9e31'
decoder_expect = {
    'input.json': '6dea1b9d1fc2f203c16642cffd76ff0df8a29813121e51f157554dab3abf500a',
    'run_transcript.json': 'f5946852ce343bfd40c2c44aaf93a282cbcc29f68bc2c11f175b4d75212718fb',
    'reconstruction.md': '608361f0c4c0832a2724c49b2febc2733e87050dca19b18746a1b6012b7a2a8c',
}
for name, expected in decoder_expect.items():
    assert info(decoder_dir / name)['sha256'] == expected
neutral = json.loads((decoder_dir / 'input.json').read_bytes())
run = json.loads((decoder_dir / 'run_transcript.json').read_bytes())
assert canonical({k:v for k,v in neutral.items() if k != 'packet_sha256'}) == neutral['packet_sha256']
assert (decoder_dir / 'reconstruction.md').read_text() == packet['blind_reconstruction']['text']
assert run['output_contract']['reconstructed_text_sha256'] == decoder_expect['reconstruction.md']
assert run['output_contract']['reconstructed_theorem_text'] != packet['blind_reconstruction']['text']
assert run['source_text_visible'] is False
assert packet['roles']['blind_decoder'] != ACTOR != packet['roles']['formalizer']

producer_path = ROOT / code_manifest['inputs'][0]['source']
consumer_path = ROOT / code_manifest['inputs'][1]['source']
candidate_paths = [producer_path, consumer_path, lesson_path, publication_path, packet_path, source_map_path]
for path in candidate_paths:
    fixed = subprocess.run(['git', 'show', COMMIT + ':' + rel(path)], check=True, capture_output=True, cwd=ROOT).stdout
    assert path.read_bytes() == fixed
assert producer_path.read_bytes() == code[rel(producer_path)]
assert consumer_path.read_bytes() == code[rel(consumer_path)]

c = packet['candidate_publication_context']
assert all(lesson[k] == v for k,v in c['lesson'].items())
assert set(lesson) - set(c['lesson']) == {'boundary'}
assert sha(c['current_lean_module'].encode()) == c['file'] == sha(producer_path.read_bytes())
full_binding = {k:v for k,v in c.items() if k != 'candidate_assumptions'}
full_binding['lesson'] = lesson
full_binding['binding'] = {k:v for k,v in item['bindings'][0].items() if k not in {'audit_id','legacy_audit_debt'}}
assert canonical(full_binding) == packet['publication_binding_sha256']
for key in ['source', 'statement', 'formulae', 'assumptions', 'obligations']:
    assert c[key] == item[key]
for name, key in [('lean-toolchain', 'toolchain'), ('lake-manifest.json', 'dependencies')]:
    assert sha((ROOT/name).read_text().encode()) == c[key]

pl = producer_path.read_text().splitlines(keepends=True)
tl = consumer_path.read_text().splitlines(keepends=True)
step_ranges = [(21,57),(59,77),(78,86),(88,96)]
steps = []
for n,(a,z) in enumerate(step_ranges):
    assert lesson['steps'][n]['lean'] == ''.join(pl[a-1:z])
    steps.append({'step':n+1, 'source':rel(producer_path), 'lines_1based_inclusive':[a,z], 'sha256':sha(lesson['steps'][n]['lean'].encode())})
assert lesson['steps'][4]['lean'] == ''.join(tl[:59])
assert lesson['steps'][5]['lean'] == ''.join(tl[60:81])
assert tl[59] == '\n'
assert lesson['steps'][4]['lean'] + tl[59] + lesson['steps'][5]['lean'] == consumer_path.read_text()
assert len(tl) == 81 and lesson['sources'][1]['line'] == 11 and lesson['sources'][1]['path'] == rel(consumer_path)
steps += [{'step':5,'source':rel(consumer_path),'lines_1based_inclusive':[1,59],'sha256':sha(lesson['steps'][4]['lean'].encode())},
          {'step':6,'source':rel(consumer_path),'lines_1based_inclusive':[61,81],'sha256':sha(lesson['steps'][5]['lean'].encode())}]

counts = {'source_spans':0, 'code_spans':0}
def spans(value):
    if isinstance(value, dict):
        if 'raw_utf8_start' in value:
            a,z=value['raw_utf8_start'],value['raw_utf8_end']
            ca,cz=value['char_start'],value['char_end']
            assert raw[a:z] == raw.decode()[ca:cz].encode()
            assert sha(raw[a:z]) == value['span_sha256']
            assert raw[:a].count(b'\n')+1 == value['lf_line_start']
            assert raw[:z-1].count(b'\n')+1 == value['lf_line_end']
            counts['source_spans'] += 1
        if 'raw_UTF8_byte_span' in value:
            b=code[value['path']];a,z=value['raw_UTF8_byte_span'];ca,cz=value['decoded_char_span']
            assert sha(b) == value['file_sha256']
            assert b[a:z] == b.decode()[ca:cz].encode()
            assert sha(b[a:z]) == value['span_sha256']
            assert b[:a].count(b'\n')+1 == value['LF_lines_1based'][0]
            assert b[:z-1].count(b'\n')+1 == value['LF_lines_1based'][1]
            counts['code_spans'] += 1
        for x in value.values(): spans(x)
    elif isinstance(value,list):
        for x in value: spans(x)
spans(source_map)
assert counts == {'source_spans':12, 'code_spans':29}

slots = {
    'objects': {
        'original':'Actual source coordinate rows gamma_i=((g_a)_i)_a of the r=q+1 independent standard d-Gaussian columns on their fixed canonical product experiment.',
        'reconstructed':'R_i(omega) collects physical coordinate i from every actual sampled column omega(a), wrapped without changing coordinates into real (q+1)-Euclidean space.',
        'relation':'equivalent',
        'evidence':'Own pre-type raw freeze A3.Ex85/A3.SS2.p1; exact P14-19 and full blind reconstruction Objects. Actual rows and same experiment are retained, without resampling or an equal-in-law surrogate.'},
    'domains': {
        'original':'Natural d,q with 2q+1<d; r=q+1; q=0 included; real finite-dimensional source column and row spaces; physical source indices 1..d and 1..r.',
        'reconstructed':'Nonnegative integer d,q with the same strict bound; D and E have their Euclidean/Borel structures; Fin d and Fin(q+1) give zero-based finite coordinates on the fixed product measurable space.',
        'relation':'explicit-elaboration',
        'evidence':'Source S4.Thmtheorem4.p1.1 and own raw freeze; full reconstruction Domains; source index translation i.val+1/a.val+1 preserves all coordinates, including q=0.'},
    'quantifiers': {
        'original':'Universal natural parameters subject to the source range, then full joint independence of all actual rows: every finite row selection and every family of Borel row events.',
        'reconstructed':'Universal d,q,hq followed by defined spaces/measure/maps; factorization for every subset S of Fin d and every corresponding Borel event family, including the entire finite family and the empty selection.',
        'relation':'equivalent',
        'evidence':'Exact P12-20, expanded iIndepFun definition and Basic654-660/860-883 inspected in the code freeze; full reconstruction Quantifiers. No pairwise-only or selected-event weakening.'},
    'assumptions': {
        'original':'Independent standard d-Gaussian columns realized on their canonical column product; natural range 2q+1<d. Gaussian/product data are the fixed experiment, not extra proof certificates.',
        'reconstructed':'Only hq is a logical hypothesis; D,E,Omega,mu and row are literal local definitions. Standard Gaussian Borel probability/product meanings elaborate the concrete experiment.',
        'relation':'explicit-elaboration',
        'evidence':'Raw source standing input and assigned canonical scope; exact P/T types and complete modules checked before this packet. No row-independence, row-law, matrix-measurability, tau/kappa/Gram/norm/moment/tail caller premise.'},
    'conclusion': {
        'original':'The scoped public subclaim is full independence of the actual row family. Raw p1 also states Gaussian marginal laws, assigned to the same existing canonical row-law node rather than this new producer.',
        'reconstructed':'The sole producer output is iIndepFun R mu, with full event factorization and no separate row law, identical-law, Measurable, or AEMeasurable output.',
        'relation':'same',
        'evidence':'Fresh scoped source.original_text, own raw/type/code freezes, exact P20 and full reconstruction Conclusion agree. The actual private matrix conjunction was independently checked in T32/T76-79 and the publication, without adding it to decoder output.'},
    'scopes': {
        'original':'Actual rows on the same fixed canonical column-product experiment; the binding is only this independence component, with arbitrary enlarged-ambient transfer and the remainder of the raw p1/main theorem outside scope.',
        'reconstructed':'All definitions occur within the d,q,hq scope and independence is under this particular mu; generated-sigma-algebra factorization is full mutual independence. No arbitrary measure/ambient transfer or further output is asserted.',
        'relation':'equivalent',
        'evidence':'Own raw scope freeze, full reconstruction Scopes, supplied kernel expansion and current publication boundary. Dirac-on-Unit notation introduces no conditioning law. Actual private F_i may vary with i, with no iid-matrix claim.'},
    'constant_dependencies': {
        'original':'Only d,q, r=q+1, strict 2q+1<d, unit Gaussian covariance and fixed Euclidean exponent are relevant to the scoped public target; no quantitative estimate or unspecified constant.',
        'reconstructed':'Exactly d,q and fixed numerals 2,1, Euclidean exponent2, and identity-covariance Gaussian factors. No tolerance/tail/error/asymptotic constant or quantitative conclusion.',
        'relation':'same',
        'evidence':'Exact P signature and full reconstruction Constant dependencies. T separately retains theta_i=(i.val+1-1/2)pi/d, feature0=1, sqrt2 cosine frequencies, inverse-d, L=2(q+1)+3log(1000d), and local closed cutoff exactly as raw source.'},
}
report_path = OUT / 'review-report.md'
report_hash = info(report_path)['sha256']
overlay = {
    'state':'source-reviewed',
    'semantic_slots':slots,
    'deltas':[],
    'verdict':'equivalent-after-elaboration',
    'source_review':{
        'state':'accepted',
        'reviewer':ACTOR,
        'independent_from_formalizer':True,
        'independent_from_decoder':True,
        'evidence':'Independent pre-type raw-source, sealed-type, full-code and fresh anti-anchored reconstruction/publication review. Accepted only for the canonical actual-row independence component and the material private measurable/independent Ex107 consumer; all six formulas/Lean slices and exact source-map spans checked. Full raw report: '+rel(DEST/'phase4_review/review-report.md')+'. No Harness VERIFIED, proof-seal, integration, rendered-reader or permission grant.',
        'review_run_sha256':report_hash,
        'reviewer_packet_sha256':packet['packet_sha256'],
        'reviewer_packet_raw_sha256':info(packet_path)['sha256'],
        'publication_binding_sha256':packet['publication_binding_sha256'],
        'run_artifact':rel(DEST/'phase4_review/review-report.md'),
        'original_run_artifact':rel(report_path),
        'checked_candidate':COMMIT,
    },
    'repairs':[],
}
assert set(overlay) == {'state','semantic_slots','deltas','verdict','source_review','repairs'}
overlay_path = OUT / 'canonical-overlay.json'
write_json(overlay_path,overlay)

spec = importlib.util.spec_from_file_location('bounded_roundtrip_schema',ROOT/'tools/astis_semantic_roundtrip_core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
audit = {'id':item['bindings'][0]['audit_id'], **copy.deepcopy(overlay),
         'source':copy.deepcopy(packet['source']),
         'lean':{**copy.deepcopy(packet['lean']),'formalizer':packet['roles']['formalizer'],'decoder_context':neutral['lean']['approved_definition_context']},
         'reconstruction':{**copy.deepcopy(packet['blind_reconstruction']), 'lean_statement_sha256':packet['lean']['statement_sha256'], 'input_artifacts':neutral['input_artifacts']},
         'publication_binding_sha256':packet['publication_binding_sha256'],
         'publication_context':packet['candidate_publication_context']}
protocol = {k:'required' for k in ['decoder_blindness','decoder_context_content_scan','independent_source_review','source_review_packet_binding','independent_repair_review','repair_review_packet_binding']}
protocol['semantic_slots']=list(core.SEMANTIC_SLOTS)
protocol['decoder_allowed_inputs']=list(core.DECODER_INPUT_ARTIFACTS)
assert core.semantic_reviewer_packet(audit) == packet
assert core.decoder_packet(audit) == neutral
errors = core.validate_registry({'schema_version':1,'protocol':protocol,'audits':[audit]})
assert not errors, errors
write_json(OUT/'schema-validation.json',{
    'scope':'One in-memory audit assembled from this fresh packet, exact anonymous decoder input, and this six-key overlay; no registry/audit loading or control-plane call.',
    'overlay':info(overlay_path), 'raw_report':info(report_path),
    'reviewer_packet_canonical_sha256':packet['packet_sha256'],
    'publication_binding_sha256':packet['publication_binding_sha256'],
    'six_top_level_keys_exact':True, 'canonical_reviewer_packet_exact_equality':True,
    'canonical_decoder_packet_exact_equality':True,
    'core_validate_registry_errors':errors, 'result':'passed',
    'not_a_compiler_or_Harness_VERIFIED_or_publication_gate':True})

schema_ranges = {
    'tools/astis_semantic_roundtrip_core.py':[(1,116),(263,363),(439,645),(718,723)],
    'tools/astis_semantic_roundtrip.py':[(95,119)],
    'tools/astis_publication.py':[(71,78),(108,141)],
}
schema_excerpt_items=[]
for name,ranges in schema_ranges.items():
    path=ROOT/name;b=path.read_bytes();lines=b.splitlines(keepends=True)
    for a,z in ranges:
        excerpt=b''.join(lines[a-1:z])
        schema_excerpt_items.append({'original_source':name,'original_full_file_sha256':sha(b),'lines_1based_inclusive':[a,z],
                                     'exact_excerpt_utf8':excerpt.decode(),'exact_excerpt_sha256':sha(excerpt)})
write_json(OUT/'schema-reference-excerpts.json',{'scope':'Narrow exact process-schema/binding excerpts only; no full control snapshot, registry contents, old verdicts, or theorem proof evidence.','excerpts':schema_excerpt_items})

write_json(OUT/'integrity-checks.json',{
    'candidate':COMMIT,'six_exact_candidate_paths_matched':[info(p) for p in candidate_paths],
    'reviewer_packet':info(packet_path),'canonical_packet_sha256':packet['packet_sha256'],
    'complete_publication_binding_recomputed':packet['publication_binding_sha256'],
    'source_lean_map':info(source_map_path),'verified_span_instances':counts,
    'six_exact_lesson_code_slices':steps,
    'private_original_blank_line60':{'bytes':1,'sha256':sha(b'\n')},
    'step5_plus_original_blank60_plus_step6_is_full_consumer':True,
    'full_private_source_lines':81,'source_export_declaration_line':11,
    'decoder_exact_originals':[info(decoder_dir/n) for n in decoder_expect],
    'full_original_reconstruction_equals_fresh_packet_text':True,
    'original_run_abridgment_preserved_separate_from_full_file_hash':True,
    'no_target_compiler_receipt_or_log_opened':True,
    'all_prior_raw_type_code_freezes_and_inputs_unchanged':True})

phase4_inputs=[packet_path,source_map_path,lesson_path,publication_path,EVIDENCE/'publication-draft-record.json',
               decoder_dir/'input.json',decoder_dir/'run_transcript.json',decoder_dir/'reconstruction.md',
               EVIDENCE/'decoder-original-custody.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
write_json(OUT/'input-exposure-manifest.json',{
    'reviewer':ACTOR,'phase':'FRESH_ANTI_ANCHORED_SOURCE_AND_PUBLICATION_REVIEW_FROZEN',
    'exact_candidate':COMMIT,'fresh_file_inputs':[info(p) for p in phase4_inputs],
    'prior_own_frozen_artifacts_preserved':verified_prior,
    'prior_full_eight_code_inputs_preserved':code_manifest['inputs'],
    'process_schema_reference_files':[info(ROOT/p) for p in schema_ranges],
    'process_schema_export_policy':'Only the narrow exact schema-reference-excerpts.json is exported, not full control implementation snapshots.',
    'actual_exposure':['Fresh packet source/scoped statement/full reconstruction/current whole module/candidate lesson projection.','Exact current lesson and publication, including current assumption classifications; independently judged against own source freeze rather than treated as verdicts.','Root-authored draft source/Lean map; all stated byte/character/LF locators checked against original source and eight code copies.','Publication draft record compiler/custody/step fields, receipt paths/hashes; its source_review value was deliberately omitted from displayed fields and not used.','Original neutral decoder input, raw run transcript and its original full reconstruction; original custody explanation.','Narrow schema/serialization code solely to form and validate the requested canonical overlay.','Read-only git show of six exact candidate paths; no Git writes.'],
    'not_read':['Other-agent source/native verdicts or graphs','Old semantic slots, deltas, repairs or canonical registry contents','Underlying build/kernel receipt or log bodies','Rendered website/UI or integration/global graph acceptance evidence','Foreign broad/control snapshots or ATLAS'],
    'allowed_output_roots':[rel(OUT),rel(DEST)],
    'only_requested_review_and_exact_copy_outputs_written':True,
    'no_ledger_frontier_registry_goal_Git_or_Harness_status_mutation':True,
    'source_review_state_meaning':'Requested semantic-only source-reviewed/accepted review; no normal independent VERIFIED or later gate grant.'})

entries=[]
def add(source,destination):
    assert destination == DEST or DEST in destination.parents
    b=source.read_bytes()
    entries.append({'source':rel(source),'destination':rel(destination),'bytes':len(b),'sha256':sha(b)})

add(raw_path,DEST/'raw-source/2610.20492v1.html')
for entry in raw_exposure['required_instruction_inputs']:
    p=ROOT/entry['path'];add(p,DEST/'protocols'/entry['path'])
raw_bundle=json.loads((BASE/'freeze_bundle_manifest.json').read_bytes())
for entry in raw_bundle['artifact_hashes']:
    p=ROOT/entry['path'];add(p,DEST/'raw_phase'/p.name)
add(BASE/'freeze_bundle_manifest.json',DEST/'raw_phase/freeze_bundle_manifest.json')
for name in ['type_only_judgment.md','input_selective_type_definition_packet.json','input_exposure_manifest.json','freeze_bundle_manifest.json']:
    add(BASE/'phase2_type_only'/name,DEST/'type_phase'/name)
original_type=ROOT/'.astis/huanjian-gc-source-row-independence-20261112/selective-type-definition-packet.json'
assert original_type.read_bytes()==(BASE/'phase2_type_only/input_selective_type_definition_packet.json').read_bytes()
add(original_type,DEST/'type_phase/original-selective-type-definition-packet.json')
for entry in code_manifest['inputs']:
    p=ROOT/entry['copy'];add(p,DEST/'code_inputs'/p.name)
add(code_manifest_path,DEST/'code_inputs/input-manifest.json')
for name in ['code_only_judgment.md','input_exposure_manifest.json','freeze_bundle_manifest.json']:
    add(BASE/'phase3_code_only'/name,DEST/'code_phase'/name)
phase4_destnames={
    packet_path:'anti-anchored-reviewer-packet.json',source_map_path:'source-lean-map.draft.json',
    lesson_path:'declaration-lesson.json',publication_path:'publication.json',
    EVIDENCE/'publication-draft-record.json':'publication-draft-record.json',
    decoder_dir/'input.json':'decoder-originals/n_decode_9e31/input.json',
    decoder_dir/'run_transcript.json':'decoder-originals/n_decode_9e31/run_transcript.json',
    decoder_dir/'reconstruction.md':'decoder-originals/n_decode_9e31/reconstruction.md',
    EVIDENCE/'decoder-original-custody.json':'decoder-original-custody.json',
    ROOT/'lean-toolchain':'lean-toolchain',ROOT/'lake-manifest.json':'lake-manifest.json'}
for source,name in phase4_destnames.items():add(source,DEST/'phase4_inputs'/name)
for name in ['review-report.md','canonical-overlay.json','schema-validation.json','schema-reference-excerpts.json','integrity-checks.json','input-exposure-manifest.json','prepare_phase4_review.py']:
    add(OUT/name,DEST/'phase4_review'/name)
assert len(entries)==59
assert len({e['destination'] for e in entries})==len(entries)
for entry in entries:
    source=ROOT/entry['source'];destination=ROOT/entry['destination'];b=source.read_bytes()
    if destination.exists():
        assert destination.read_bytes()==b, f'Existing portable destination differs: {destination}'
    else:
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(b)
    assert info(destination)['bytes']==entry['bytes'] and info(destination)['sha256']==entry['sha256']

manifest={'schema_version':1,'reviewer':ACTOR,'exact_candidate':COMMIT,
          'exact_count':len(entries),'manifest_destination':rel(DEST/'portable-manifest.json'),
          'manifest_self_entry_policy':'The manifest destination is separate from entries to avoid circular self-hashing. The original and destination manifest bytes are identical; hash is reported externally.',
          'entry_fields':'source and destination are repository-relative; bytes/SHA-256 bind both exact files. Existing destinations may only be verified byte-identical, never overwritten.',
          'entries':entries}
write_json(OUT/'portable-manifest.json',manifest)
write_json(DEST/'portable-manifest.json',manifest)
assert (OUT/'portable-manifest.json').read_bytes()==(DEST/'portable-manifest.json').read_bytes()
for p in [report_path,overlay_path,OUT/'portable-manifest.json']:
    print(json.dumps(info(p)))
print(json.dumps({'exact_count':len(entries),'manifest_destination':rel(DEST/'portable-manifest.json'),'portable_manifest_sha256':info(DEST/'portable-manifest.json')['sha256'],'in_memory_schema_result':'passed'}))
