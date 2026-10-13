from pathlib import Path
import json,hashlib,datetime,shutil
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent;pre=out.parent
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p.resolve()),raw_sha256=raw(p),bytes=p.stat().st_size,hash_mode='exact-raw-file-bytes')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(n,v):
 p=out/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p
def snap(p,n):
 q=out/n;assert not q.exists();shutil.copyfile(p,q);assert raw(p)==raw(q);return q
v1=pre/'header90.proposed.lean';v2=pre/'header90.v2.proposed.lean';packet=pre/'header-review90.v2.packet.json';diagnosis=pre/'header90.scope-diagnosis.json';olddecision=out/'header90.source-decision.native.json';oldrun=out/'header90.source-run.native.json';oldmanifest=out/'closed-raw-manifest.header-source90.native.json'
assert raw(v1)=='1262c82138eb3a7cc502fe4eb6182c10e4e33168a734333ffaec580585935750'
assert raw(v2)=='5c976dcfe91fe074db71ddbf13385086735c41c273e937b0c6ef432b7dba9037'
assert raw(olddecision)=='e59dd17f33326073645406b15a0e8f236a5a7e70c9101dce7a84f98569a5115d'
assert raw(oldmanifest)=='3d2182fd184b26fe082b26cf6c1033928d246a75e721433e8589275cded4a0e4'
for section in ['inputs','outputs']:
 for e in load(oldmanifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
b1=v1.read_bytes();b2=v2.read_bytes();tail=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension\n'
assert b1.endswith(tail);assert b2==b1[:-len(tail)]+b'end\n'+tail
expression1=b1[b1.index(b'private def '):b1.rindex(b'\nend AutoSamplingTheory')]
expression2=b2[b2.index(b'private def '):b2.rindex(b'\nend\nend AutoSamplingTheory')]
assert expression1==expression2
p1=load(pre/'header-review90.packet.json');p2=load(packet)
assert {k:v for k,v in p1.items() if k!='header'}=={k:v for k,v in p2.items() if k not in ['header','scope_diagnosis']}
for k in ['header','accepted_source_graph','source_adoption','unchanged_coverage','copied_literal_definitions_from','scope_diagnosis']:
 e=p2[k];p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
receipt1=pre/'header-elaboration90/receipt.json';receipt2=pre/'header-elaboration90-v2/receipt.json';r1=load(receipt1);r2=load(receipt2)
assert r1['exit_code']==1 and r1['terminal_closed'] and r1['header']['raw_sha256']==raw(v1)
assert r2['exit_code']==0 and r2['terminal_closed'] and r2['header']['raw_sha256']==raw(v2)
for r in [r1,r2]:assert r['proof_BODY_present'] is False and r['statement_sealed'] is False
stdout1=pre/'header-elaboration90/stdout.log';stdout2=pre/'header-elaboration90-v2/stdout.log';stderr1=pre/'header-elaboration90/stderr.log';stderr2=pre/'header-elaboration90-v2/stderr.log'
log1=stdout1.read_text(encoding='utf-8');log2=stdout2.read_text(encoding='utf-8')
assert 'error:' in log1 and 'error:' not in log2
scope=write('header90.v2.scope-check.native.json',dict(schema_version=1,kind='independent exact header90 V1 to V2 syntax-only scope check',V1=pin(v1),V2=pin(v2),change='Exactly insert four bytes end followed by LF immediately before the final named namespace end. Closes the previously open noncomputable unnamed section.',private_statement_expression_byte_identical=True,private_statement_expression_raw_sha256=hashlib.sha256(expression1).hexdigest(),binders_definitions_quantifiers_conclusions_unchanged=True,packet_all_nonheader_mathematics_unchanged=True,root_diagnosis=pin(diagnosis),V1_negative_receipt=pin(receipt1),V1_negative_stdout=pin(stdout1),V1_negative_stderr=pin(stderr1),V2_header_elaboration_receipt=pin(receipt2),V2_stdout=pin(stdout2),V2_stderr=pin(stderr2),interpretation='V1 source-boundary assessment remains valid for its proposition, but V1 had a file-scope syntax error. V2 header-only elaboration succeeds. This is not a mathematical repair or a BODY proof/VERIFIED claim.',mathematical_source_verdict_unchanged=True))
snaps=[snap(v2,'header90.v2.exactraw.lean'),snap(packet,'header-review90.v2.packet.exactraw.json')]
chron=out/'chronology.header-source90.v2.native.jsonl';assert not chron.exists()
events=[dict(event='INHERIT_IMMUTABLE_PRIMARY_FIRST_EXACT_HEADER90_SOURCE_REVIEW',original_decision=pin(olddecision),original_manifest=pin(oldmanifest),original_primary_first_chronology=pin(out/'chronology.header-source90.native.jsonl')),dict(event='V2_EXACT_SCOPE_ONLY_INSERTION_AND_EXPRESSION_BYTEIDENTITY_CHECKED',scope_check=pin(scope),mathematical_statement_unchanged=True),dict(event='V2_PROSPECTIVE_SOURCE_HEADER_SUCCESSOR_CLOSED',verdict='equivalent-after-elaboration',repairs=[],no_Seal_claim_BODY_proof_VERIFIED=True)]
chron.write_text(''.join(json.dumps(dict(sequence=i+1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**e),ensure_ascii=False)+'\n' for i,e in enumerate(events)),encoding='utf-8',newline='\n')
inputs=[olddecision,oldrun,oldmanifest,out/'chronology.header-source90.native.jsonl',v1,v2,packet,diagnosis,receipt1,receipt2,stdout1,stdout2,stderr1,stderr2,pre/'source-proof-graph90.accepted-successor.json',pre/'independent-source-first90/closed-raw-manifest.source-first90.native.json']
run=write('header90.source-run.v2.native.json',dict(schema_version=1,kind='independent prospective exact-header90 V2 source-binding successor',reviewer='/root/fresh_source87',original_primary_first_source_review_run=pin(oldrun),original_closed_manifest=pin(oldmanifest),chronology=pin(chron),scope_check=pin(scope),inputs=[pin(p) for p in inputs],independent_expression_byteidentity_check=True,source_semantics_reused_unchanged=True,no_graph_creator_self_approval=True,header_elaboration_only_exit0=True,no_BODY_or_proof_acceptance=True,canonical_mutations=False,VERIFIED=False))
d=load(olddecision);d.update(header=pin(v2),packet=pin(packet),review_run_sha256=raw(run),header_version='V2',syntax_only_successor=dict(original_decision=pin(olddecision),original_manifest=pin(oldmanifest),scope_check=pin(scope),private_expression_byteidentical=True,source_boundary_decision_unchanged=True),header_elaboration=dict(receipt=pin(receipt2),exit_code=0,terminal_closed=True,proof_BODY_present=False),Lean_compilation_claimed='Header/private-definition elaboration only; no theorem BODY or mathematical closure claimed.')
decision=write('header90.source-decision.v2.native.json',d)
terminal=write('terminal-completion.header-source90.v2.native.json',dict(schema_version=1,kind='authoritative native prospective source-header90 V2 terminal completion',terminal_closed=True,status='HEADER_SOURCE_V2_AUDIT_CLOSED',decision=pin(decision),run=pin(run),chronology=pin(chron),verdict=d['verdict'],no_Seal_claim_BODY_proof_or_VERIFIED=True,canonical_mutations=False))
outputs=[Path(__file__).resolve(),scope,*snaps,chron,run,decision,terminal]
manifest=write('closed-raw-manifest.header-source90.v2.native.json',dict(schema_version=1,kind='closed exact RAW prospective source-header90 V2 successor manifest',closed=True,input_set_closed=True,output_set_closed=True,inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],inherited_primary_first_V1_header_manifest=pin(oldmanifest),all_original_inputs_outputs_RAW_reverified=True,V1_negative_and_V2_header_elaboration_preserved=True,manifest_root_excluded_from_self_hash=True,canonical_mutations=False,header_ONLY_not_BODY_or_VERIFIED=True))
for section in ['inputs','outputs']:
 for e in load(manifest)[section]:
  p=Path(e['path']);assert raw(p)==e['raw_sha256'] and p.stat().st_size==e['bytes']
print(json.dumps(dict(status='CLOSED',decision=pin(decision),run=pin(run),manifest=pin(manifest),terminal=pin(terminal),chronology=pin(chron),packet=pin(packet),verdict=d['verdict'],repairs=[],literal_defs=d['literal_definition_count'],analytic_binders=d['analytic_binder_count']),ensure_ascii=False,indent=2))
