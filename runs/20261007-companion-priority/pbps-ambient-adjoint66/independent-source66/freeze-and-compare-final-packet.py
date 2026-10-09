from pathlib import Path
import json,hashlib,os,datetime
O=Path(__file__).parent;R=O.parent;ROOT=Path('E:/Samplinglib')
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
def freeze(p,n):
 b=p.read_bytes();(O/(n+'.RAW.json')).write_bytes(b);(O/(n+'.LF.json')).write_bytes(b.replace(b'\r\n',b'\n'));return dict(original=pin(p),RAW_snapshot=n+'.RAW.json',LF_snapshot=n+'.LF.json')
stage=dict(schema='source66-finite-original-to-approved-current-inputs-v1',actual_pid=os.getpid(),read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=[])
stage['inputs'].append(freeze(R/'presentation-overlay66/applied.json','overlay.applied'))
stage['inputs'].append(freeze(R/'math-freeze1.metadata-overlay.json','math-freeze1.metadata-overlay'))
mapping=json.loads((R/'math-freeze1.metadata-overlay.json').read_bytes());applied=json.loads((R/'presentation-overlay66/applied.json').read_bytes())
assert H((O/'metadata-overlay.verdict.json').read_bytes())==applied['separate_independent_overlay_verdict']['raw_sha256']
assert H((O/'overlay.proposal.RAW.json').read_bytes())==applied['proposal']['raw_sha256']
for i,row in enumerate(mapping['explicit_old_to_approved_current_maps']):
 p=ROOT/row['canonical'];old=(O/('overlay.%d.before.RAW.json'%i)).read_bytes();proposed=(O/('overlay.%d.proposed.RAW.json'%i)).read_bytes()
 assert H(old)==row['before']['raw_sha256'];assert old==(ROOT/row['before_snapshot']['path']).read_bytes()
 assert H(proposed)==row['proposed']['raw_sha256'];assert proposed==p.read_bytes();assert proposed==(ROOT/row['proposed']['path']).read_bytes()
 stage['inputs'].append(freeze(p,'current.approved.%d'%i))
for i,row in enumerate(mapping['current_inputs'][4:]):
 p=ROOT/row['path'];assert H(p.read_bytes())==row['raw_sha256'];stage['inputs'].append(freeze(p,['audit.current','reviewer-packet.final'][i]))
for i,row in enumerate(mapping['compiled_inputs_unchanged']):
 p=ROOT/row['path'];assert H(p.read_bytes())==row['raw_sha256'];assert p.read_bytes()==(O/('%03d.RAW.snapshot'%i)).read_bytes()
assert (R/'math-freeze.json').read_bytes()==(O/'frozen.math-freeze.json').read_bytes()
p=json.loads((O/'reviewer-packet.final.RAW.json').read_bytes());old=json.loads((O/'reviewer-packet.initial.RAW.json').read_bytes());core=dict(p);del core['packet_sha256'];assert C(core)==p['packet_sha256']
assert p['source']==old['source'] and p['lean']==old['lean'] and p['blind_reconstruction']==old['blind_reconstruction']
assert all(v is False for v in p['anti_anchoring'].values());assert p['blind_reconstruction']['source_text_visible'] is False
assert p['roles']['formalizer']!='/root/independent_source64' and p['roles']['blind_decoder']!='/root/independent_source64'
for text,sha in [(p['lean']['statement'],p['lean']['statement_sha256']),(p['source']['original_text'],p['source']['text_sha256']),(p['blind_reconstruction']['text'],p['blind_reconstruction']['text_sha256'])]:assert H(text.encode())==sha
expanded=(O/'current.expanded-header0.RAW.lean').read_text(encoding='utf-8');assert expanded[expanded.index('\n'):].rstrip('\n')==p['lean']['statement']
item=json.loads((ROOT/'website/content/publications/pbps-ambient-adjoint-corrector.json').read_bytes())['items'][0]
lesson=json.loads((ROOT/'website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json').read_bytes())['units'][0];binding=item['bindings'][0]
module=(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean').read_text(encoding='utf-8')
payload=dict(file=H(module.encode()),current_lean_module=module,toolchain=H((ROOT/'lean-toolchain').read_text(encoding='utf-8').encode()),dependencies=H((ROOT/'lake-manifest.json').read_text(encoding='utf-8').encode()),source=item['source'],statement=item['statement'],formulae=item['formulae'],assumptions=item['assumptions'],obligations=item['obligations'],lesson=lesson,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
context=dict(payload);context['binding']={k:payload['binding'][k] for k in ['declaration','role','supports']};context['lesson']={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']};context['candidate_assumptions']=[{k:row[k] for k in ['source','lean']} for row in binding['assumption_deltas']]
assert C(payload)==p['publication_binding_sha256']==applied['current_binding'];assert context==p['candidate_publication_context'];assert C(context)==applied['current_context_sha256']
put('publication-binding.final.recomputed.json',dict(schema='source66-final-publication-binding-recomputation-v1',actual_pid=os.getpid(),algorithm='Entire finite tools/astis_publication.py binding_payload/review_context; no selective projection beyond the defined context algorithm',publication_binding_sha256=C(payload),publication_context_sha256=C(context),publication_binding_payload=payload,publication_context=context,current_publication=pin(ROOT/'website/content/publications/pbps-ambient-adjoint-corrector.json'),current_lesson=pin(ROOT/'website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json')))
excerpts=json.loads((O/'literal-BODY-excerpt-audit.json').read_bytes())
for i,step in enumerate(lesson['steps']):
 r=step['lean_source_region'];raw=(ROOT/r['path']).read_bytes();lines=raw.splitlines(keepends=True);chunk=b''.join(lines[r['start_line']-1:r['end_line']]);assert H(raw)==r['source_raw_sha256'];assert H(chunk)==r['exact_code_raw_sha256'];assert chunk==(O/('literal-BODY-step%d.RAW.lean'%i)).read_bytes();assert chunk.decode()==step['lean']
assert item['formulae']==json.loads((O/'overlay.0.before.RAW.json').read_bytes())['items'][0]['formulae']
beforelesson=json.loads((O/'overlay.1.before.RAW.json').read_bytes())['units'][0];assert lesson['formula']==beforelesson['formula'];assert lesson['steps']==beforelesson['steps']
strings=[lesson['formula']]+[s['formula'] for s in lesson['steps']]+[f['tex'] for f in item['formulae']]
assert all('\\\\' not in s for s in strings)
put('final-reviewer-packet-binding-check.json',dict(schema='source66-final-packet-canonical-binding-check-v1',actual_pid=os.getpid(),reviewer_packet_sha256=p['packet_sha256'],reviewer_packet_RAW_pin=pin(O/'reviewer-packet.final.RAW.json'),initial_packet_retained=pin(O/'reviewer-packet.initial.RAW.json'),source_reconstruction_expanded_Lean_unchanged=True,canonical_packet_hash_checked=True,exact_current_context_equal=True,publication_binding_sha256=C(payload),publication_context_sha256=C(context),all6_literal_BODY_regions_unchanged=True,original_and_current_input_stages_explicit=True,anti_anchoring_and_role_independence_checked=True,all4_current_files_exact_reviewed_proposed_bytes=True,formula_changes=0,source_mathematical_repair=False))
stage.update(original_freeze_immutable=True,original_inputs_not_assumed_equal_to_changed_current_metadata=True,all4_current_exact_proposed=True,compiled_inputs_unchanged=True,finite_history_only=True,root_application_actual_pid=applied['actual_root_pid'],source_mathematical_repair=False)
put('candidate-inputs.final.json',stage)
print(json.dumps(dict(actual_pid=os.getpid(),packet_sha256=p['packet_sha256'],packet_RAW_sha256=H((O/'reviewer-packet.final.RAW.json').read_bytes()),binding=C(payload),context=C(context),current_files_exact_approved=True,unchanged_BODY_regions=6,source_math_repair=False),sort_keys=True))
