from pathlib import Path
import copy,hashlib,json,re,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');pre=Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68')
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
audit=copy.deepcopy(json.loads(Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSSharpCorrectorEnergy.json').read_bytes()))
audit.pop('reconstruction',None);audit.pop('publication_binding_sha256',None);audit.pop('publication_context',None)
audit.update(id='ASTIS-RT-20261009-PBPSSharpModifiedEnergyConsumer',state='draft',source_review=dict(state='pending'),repairs=[])
decl='Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence'
header=(pre/'header2-expanded.lean').read_text(encoding='utf-8');definition=(pre/'statement2.definition.lean').read_text(encoding='utf-8')
statement=header[header.index('theorem ')+len('theorem '+decl.rsplit('.',1)[1]):].rstrip('\n')
p=Path('Tests/ProximalBPSSharpCorrectorEnergy.lean');s=p.read_text(encoding='utf-8');a=s.index('theorem '+decl.rsplit('.',1)[1]);b=s.index(':= by',a)
assert definition.rstrip()+'\n'==s[s.index('private def '):a].rstrip()+'\n'
audit['source']['source_id']='companion-domain:pbps-sharp-modified-energy-consumer'
audit['source']['anchor']='PBPS2609.06905v1 Appendix B.3 Lemma B.3 and B19/B20/B23/B24: universal0<omegaWeight<=gamma modified-energy equivalence.'
audit['source']['original_text']+='\nThis standalone original-input consumer additionally proves, for every real0<omegaWeight<=gamma, L=||f||²+omegaWeight C(fP,fV), ||f||²/2<=L<=3||f||²/2 and |L-||f||²|<=omegaWeight||f||²/(2gamma)<=||f||²/2. Its complete literal proposition retains all original hypotheses/witnesses.'
audit['source']['text_sha256']=sha(audit['source']['original_text'].encode())
audit['lean'].update(declaration=decl,file=p.as_posix(),statement=statement,statement_sha256=sha(statement.encode()),statement_representation=dict(kind='exact-literal-private-Prop-expansion',actual_header=s[a:b].rstrip()+'\n',private_definition=definition,expanded_header=header,source_approved_overlay=(pre/'root.header68.adoption.json').as_posix(),kernel_header_and_literal_expansion_checked=True))
audit['lean']['decoder_context']+=['For every real omegaWeight with0<omegaWeight<=gamma, L is the explicitly defined modified squared energy. The final two-sided energy and perturbation inequalities are conclusions; omegaWeight and its stated interval are universally quantified after the actual centered f and its internally produced witnesses.']
audit['standalone_test_consumer_scope']=dict(production_source_item='pbps-sharp-corrector-energy',same_unchanged_Test=True,separate_source_review_required=True,not_a_new_production_wrapper=True)
packet=rt.decoder_packet(audit);raw=json.dumps(packet,ensure_ascii=False)
assert not re.search(r'Fan|Chewi|PBPS|arXiv|2609|Samplinglib|SharpCorrector|Chen|Zhang',raw)
write(r/'consumer.semantic-audit68.draft.json',audit);write(r/'anonymous.consumer.decoder.json',packet)
n=Path('.astis/decoder-68-consumer');n.mkdir(exist_ok=False)
write(n/'packet0.json',packet);write(n/'lease.json',dict(status='OPEN',allowed_inputs=['packet0.json'],source_text_visible=False,source_identity_visible=False,compiler_started=False))
(n/'initial-lease.raw.snapshot.json').write_bytes((n/'lease.json').read_bytes())
print('One neutral packet for unchanged full original-input Test; no source identity,code or production metadata changes.')
