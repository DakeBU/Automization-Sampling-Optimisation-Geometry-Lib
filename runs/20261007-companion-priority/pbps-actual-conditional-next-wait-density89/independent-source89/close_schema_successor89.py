from pathlib import Path
import json, hashlib, datetime
out=Path(__file__).resolve().parent
root=Path('E:/Samplinglib')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size,hash_mode='exact-raw-file-bytes')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(n,v):
 p=out/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p
olddecision=out/'source-review89.decision.native.json';oldrun=out/'source-review89.run.native.json';oldmanifest=out/'closed-raw-manifest.source-review89.native.json'
assert raw(olddecision)=='5e5ac9def30513303a4233f70942990da9867642b245ea54034b29c1420454cd'
assert raw(oldmanifest)=='453ef2bc945661b5956d4bac8fb24a69afc89b0751655d96d0b4263e47ff99a1'
for section in ['inputs','outputs']:
 for e in load(oldmanifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
d=load(olddecision)
slotmap={'D89-1':'conclusion','D89-2':'domains','D89-3':'objects','D89-4':'scopes','D89-5':'quantifiers','D89-6':'conclusion','D89-7':'scopes','D89-8':'scopes'}
negative=write('source-review89.native-format-observations.json',dict(kind='retained reviewer-local serialization/check observations',source_verdict_unchanged=True,canonical_changes=False,observations=[
 dict(kind='failed-local-diff-check',script=pin(out/'close_source_review89.attempt1.py'),terminal_exit_code=1,error="AssertionError: ['/steps/1/formula']",explanation='Initial audit script expected the separately reviewed one-field overlay to be text. Exact recursive diff showed it was formula. Independently read original/current formula; successor removes premature kernel mass bound from step2. Corrected local assertion to formula before the native source decision closed. Source/Lean/prose was not changed.'),
 dict(kind='native-semantic-slot-serialization',original=pin(olddecision),explanation='All seven reconstructed fields originally retained structured native decoder objects/lists. Canonical semantic schema requires nonempty strings. The successor serializes those exact values as JSON strings and also preserves the untouched structured values explicitly; no semantic content, verdict, boundary or original native output is changed.'),
 dict(kind='native-delta-description-fields',explanation='Successor adds canonical slot/description/evidence/severity fields derived verbatim from existing source/lean/reason/classification/blocking fields; all original fields remain.')]))
native_structured={}
for k,row in d['semantic_slots'].items():
 native_structured[k]=row['reconstructed']
 row['reconstructed']=json.dumps(row['reconstructed'],ensure_ascii=False,sort_keys=True,indent=2)
for delta in d['deltas']:
 delta.update(slot=slotmap[delta['id']],description=delta['source']+' → '+delta['lean']+'. '+delta['reason'],evidence='Independent source review classification: '+delta['classification']+'; nonblocking. '+delta['reason'],severity='informational')
d['native_structured_reconstruction']=native_structured
d['delta_slots']=slotmap
d['format_successor']=dict(original_decision=pin(olddecision),original_run=pin(oldrun),original_manifest=pin(oldmanifest),change='Schema serialization and canonical delta fields only; source verdict, all mathematics and publication binding unchanged.',original_outputs_immutable=True)
schema=root/'tools/astis_semantic_roundtrip_core.py'
assert 'for field in ("original", "reconstructed", "evidence"):' in schema.read_text(encoding='utf-8')
for row in d['semantic_slots'].values():
 for k in ['original','reconstructed','evidence']:assert isinstance(row[k],str) and row[k].strip()
 assert row['relation'] in ['equivalent','explicit-elaboration','same']
for x in d['deltas']:
 assert x['slot'] in d['semantic_slots'] and x['description'] and x['evidence'] and not x['blocking']
assert d['verdict']=='equivalent-after-elaboration' and not d['repairs'] and len(d['literal_definition_audit'])==23 and len(d['analytic_binder_audit'])==6 and len(d['body_audit'])==6
chron=out/'chronology.source-review89.v2.native.jsonl';assert not chron.exists()
events=[dict(event='INHERIT_CLOSED_SOURCE_REVIEW_UNCHANGED',original_manifest=pin(oldmanifest),old_chronology=pin(out/'chronology.source-review89.native.jsonl')),dict(event='CANONICAL_SCHEMA_READ_AND_NATIVE_SERIALIZATION_SUCCESSOR_CHECKED',schema=pin(schema),native_observations=pin(negative),source_verdict_unchanged=True),dict(event='SCHEMA_COMPATIBLE_SOURCE_REVIEW89_V2_CLOSED',verdict=d['verdict'],target=d['accepted_truth_boundary']['target'],canonical_mutations=False,VERIFIED=False)]
chron.write_text(''.join(json.dumps(dict(sequence=i+1,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**e),ensure_ascii=False)+'\n' for i,e in enumerate(events)),encoding='utf-8',newline='\n')
run=write('source-review89.run.v2.native.json',dict(schema_version=1,kind='independent source89 exact native schema serialization successor',reviewer='/root/fresh_source87',original_source_review_run=pin(oldrun),original_source_review_decision=pin(olddecision),original_closed_manifest=pin(oldmanifest),chronology=pin(chron),native_observations=pin(negative),schema_input=pin(schema),inputs_reused_unchanged=True,seven_semantic_slots_string_fields=True,all_original_native_decoder_uncertainties_unchanged=True,all_original_deltas_retained=True,source_fidelity_verdict_unchanged=True,canonical_mutations=False,VERIFIED=False))
d['review_run_sha256']=raw(run)
decision=write('source-review89.decision.v2.native.json',d)
terminal=write('terminal-completion.source-review89.v2.native.json',dict(schema_version=1,kind='authoritative schema-compatible native source89 terminal completion',terminal_closed=True,status='source-review-closed',decision=pin(decision),run=pin(run),chronology=pin(chron),verdict=d['verdict'],accepted_target=d['accepted_truth_boundary']['target'],canonical_mutations=False,VERIFIED=False))
inputs=[olddecision,oldrun,oldmanifest,schema,out/'source-review89.decision.native.json',out/'chronology.source-review89.native.jsonl']
outputs=[Path(__file__).resolve(),negative,chron,run,decision,terminal]
manifest=write('closed-raw-manifest.source-review89.v2.native.json',dict(schema_version=1,kind='closed exact RAW schema-compatible independent source89 successor manifest',closed=True,input_set_closed=True,output_set_closed=True,inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],inherited_full_source_review_manifest=pin(oldmanifest),transitive_input_output_closure='Every original manifest input/output descriptor RAW-reverified before successor; predecessor immutable and retained.',manifest_root_excluded_from_self_hash=True,canonical_mutations=False,VERIFIED=False))
for section in ['inputs','outputs']:
 for e in load(manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
print(json.dumps(dict(status='CLOSED',decision=pin(decision),run=pin(run),manifest=pin(manifest),terminal=pin(terminal),chronology=pin(chron),verdict=d['verdict'],accepted_target=d['accepted_truth_boundary']['target'],delta_slots=slotmap),ensure_ascii=False,indent=2))
