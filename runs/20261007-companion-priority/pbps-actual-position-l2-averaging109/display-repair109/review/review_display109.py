from pathlib import Path
import copy
import gzip
import hashlib
import json

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-position-l2-averaging109'
OUT = RUN / 'display-repair109/review'


def h(b):
    return hashlib.sha256(b).hexdigest()


def ref(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), raw_sha256=h(b), bytes=len(b))


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def write(name, data):
    p = OUT / name
    assert not p.exists()
    p.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


old_decision_path = RUN / 'final-source109/source-review109.native.json'
old_run_path = RUN / 'final-source109/reviewer-run109.native.json'
old_packet_path = RUN / 'reviewer109.input.json'
packet_path = RUN / 'display-repair109/reviewer.input.json'
before_path = RUN / 'display-repair109/before-pbps-actual-position-l2-averaging.json'
lesson_path = ROOT / 'website/content/declaration_lessons/pbps-actual-position-l2-averaging.json'
production_path = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPositionL2Averaging.lean'
scope_path = RUN / 'display-repair109/scope.json'
old_decision, old_run = read(old_decision_path), read(old_run_path)
old_packet, packet = read(old_packet_path), read(packet_path)
before, lesson = read(before_path), read(lesson_path)
scope = read(scope_path)
assert ref(production_path)['raw_sha256'] == scope['Lean_RAW'] == '21c6b4e95b729b41f555eecf6a42185ab2f63bff7bcab3f6dc2ab82da171e85e'
assert packet['publication_binding_sha256'] == scope['new_binding']
assert old_packet['publication_binding_sha256'] == scope['old_binding']
calc = copy.deepcopy(packet)
calc.pop('packet_sha256')
assert h(json.dumps(calc, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()) == packet['packet_sha256']
old_text = before['units'][0]['steps'][6]['text']
new_text = lesson['units'][0]['steps'][6]['text']
assert old_text.count('B**=B') == 1
assert new_text == old_text.replace('B**=B', 'the double-adjoint identity for B')
test = copy.deepcopy(before)
test['units'][0]['steps'][6]['text'] = new_text
assert test == lesson
test_packet = copy.deepcopy(old_packet)
test_packet['candidate_publication_context']['lesson']['steps'][6]['text'] = new_text
test_packet['publication_binding_sha256'] = packet['publication_binding_sha256']
test_packet['packet_sha256'] = packet['packet_sha256']
assert test_packet == packet
assert len(lesson['units'][0]['steps']) == 8
reused = [old_run[k] for k in ['primary_first', 'native_decoder', 'native_decoder_manifest', 'compiled_coverage', 'exposition', 'whole_math_kernel_evidence_only']]
for item in reused:
    assert ref(ROOT / item['path']) == item
limits = dict(actual_browser_acceptance=False, fullExpositionSeal=False, merged_to_main=False, stabilized=False, purified=False, full_paper_complete=False)
admission = write('display-admission109.native.json', dict(
    verdict='ACCEPT_PRESENTATION_ONLY_DOUBLE_ADJOINT_WORDING', reviewer='/root/source_final96', independent_from_author=True,
    scope=ref(scope_path), before_lesson=ref(before_path), current_lesson=ref(lesson_path),
    changed_json_pointer='/units/0/steps/6/text', before=old_text, after=new_text,
    exact_change='Replace exactly one B**=B prose token with the double-adjoint identity for B.',
    mathematical_meaning='The prose denotes (B*)*=B in both versions. Production317 invokes ContinuousLinearMap.adjoint_adjoint on the same canonical position lift. The replacement removes Markdown-bold delimiter characters without changing mathematical content.',
    checks=dict(only_one_lesson_text_field_changed=True, all_eight_lean_regions_identical=True, all_formulae_identical=True, literal_statement_identical=True, assumptions_identical=True, production_raw_unchanged=True, decoder_packet_and_reconstruction_identical=True, source_graph_and_compiled_coverage_unchanged=True),
    prior_source_validity='The original source review remains valid for its exact original publication binding. This separate independent admission transfers it to the new text-only publication binding after checking the precise delta.',
    source_theorem_repairs=[], limitations=limits,
))
evidence = 'Independent bounded presentation review: exactly one step7 prose token B**=B becomes the double-adjoint identity for B. Both denote the actual adjoint_adjoint rewrite at production317. All eight code/formula regions, literal statement, source assumptions, production RAW and anonymous reconstruction are identical. Prior source/math/decoder/coverage evidence is explicitly reused by exact RAW, not claimed freshly repeated. No new mathematical source delta.'
run = copy.deepcopy(old_run)
run.update(kind='Independent109 presentation-delta source-review transfer', prior_involvement='Authored original independent primary-first final109 review; this task explicitly reuses that closed review and independently checks only the new presentation delta.',
    primary_first_repeated_this_run=False, prior_semantic_verdict_slots_deltas_repairs_used=True, reuse_authorization='Parent requested exact unchanged mathematics/source/decoder reuse for one prose-token repair.',
    reviewer_packet=ref(packet_path), reviewer_packet_sha256=packet['packet_sha256'], publication_binding_sha256=packet['publication_binding_sha256'],
    source_evidence=evidence, prior_source_review=ref(old_decision_path), prior_source_run=ref(old_run_path), independently_accepted_display_delta=admission,
    owned_scope=OUT.relative_to(ROOT).as_posix(), limitations=limits)
runref = write('reviewer-run109.native.json', run)
decision = copy.deepcopy(old_decision)
decision.update(reviewer_packet_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],review_run_sha256=runref['raw_sha256'],review_evidence=evidence,
    prior_source_review=ref(old_decision_path), independently_accepted_display_delta=admission, limitations=limits)
decision['source_review'].update(reviewer_packet_sha256=packet['packet_sha256'],review_run_sha256=runref['raw_sha256'],run_artifact=runref['path'],evidence=evidence,
    prior_semantic_verdict_slots_deltas_repairs_used=True, review_mode='Explicitly authorized unchanged-source reuse plus independent presentation-delta admission', independently_accepted_display_delta=admission, limitations=limits)
decision['deltas'].append(dict(slot='scopes',severity='informational',description='One display-only prose token spells out the double-adjoint identity; source theorem and proof unchanged.',source='Gaussian momentum averaging adjoint composition.',lean='ContinuousLinearMap.adjoint_adjoint at production317; unchanged.',evidence=admission['path'],blocking=False))
assert decision['repairs'] == []
decisionref = write('source-review109.native.json', decision)
inputs = [old_decision_path,old_run_path,old_packet_path,packet_path,before_path,lesson_path,production_path,scope_path,RUN/'display-repair109/before-ASTIS-RT-20261012-PBPSActualPositionL2Averaging.json']
inputs += [ROOT/item['path'] for item in reused]
outputs = sorted(p for p in OUT.iterdir() if p.is_file())
archives = []
archive_dir = OUT/'raw-archives'
archive_dir.mkdir()
for p in outputs:
    b=p.read_bytes();a=archive_dir/(p.name+'.raw.gz');a.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(a.read_bytes())==b
    archives.append(dict(original=ref(p),archive=ref(a)))
closure=write('closed-RAW-display-review109.native.json',dict(kind='Closed independent presentation-only109 review',inputs=[ref(p) for p in inputs],artifacts=[ref(p) for p in outputs],archives=archives,decision=decisionref,run=runref,admission=admission,no_shared_mutation=True,limitations=limits))
print(json.dumps(dict(decision=decisionref,run=runref,admission=admission,closure=closure),indent=2))
