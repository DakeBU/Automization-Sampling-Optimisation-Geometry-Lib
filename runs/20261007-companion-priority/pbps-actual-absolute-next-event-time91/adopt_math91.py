from pathlib import Path
import hashlib,json,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'independent-math91'
sys.path.insert(0,str(R/'tools'))
import astis_semantic_roundtrip as rt
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
expected={'decision91.native.json':'335138e5ae1b59eff3f46bcc607ca3f5464a42e8d805848f6cd0785fd321ff79',
          'closeout91.native.json':'2fb4d1fde24a0e85df508a7e676435b6527b7df123d52949ccd77aa5bd83ae42',
          'closed-manifest91.native.json':'0aa64d0bf60f8b067eb32633274c20e85a972f01dbae239780cb07529b57569f',
          'leaf-build.receipt.native.json':'f9d9664642918ad30386649f8facc20769781d69da5d95b2eb9a548518626055'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h
checked=[]
def verify(x):
    p=Path(x['path']);b=p.read_bytes();assert sha(b)==x['raw_sha256'],p
    if 'bytes' in x:assert len(b)==x['bytes'],p
    checked.append(str(p))
for x in load(d/'closed-manifest91.native.json')['files']:verify(x)
n=load(d/'decision91.native.json');close=load(d/'closeout91.native.json')
assert n['reviewer']=='/root/independent_math91' and n['decision']=='ACCEPT_LOCAL_MATHEMATICS_KERNEL_AND_EXPOSITION'
assert n['kernel_exit_code']==0 and not n['excess_binders'] and not n['provider_assumptions'] and not n['counterexamples_found']
assert n['axioms']==['propext','Classical.choice','Quot.sound'] and n['kernel_expansion_complete']
assert n['statement_seal_exact_35_let_Prop_match'] and not n['missing_value_constants']
for x in [n['production'],n['statement_seal'],*n['parent_compiled_artifacts'],*n['reviewed_exposition'],close['target_olean']]:verify(x)
assert load(d/'leaf-build.receipt.native.json')['exit_code']==0
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime.json'
a=load(ap);before=rt.semantic_reviewer_packet(a)
(r/'audit.before-kernel-confirmation91.json').write_bytes(ap.read_bytes())
a['lean']['statement_representation']['kernel_header_and_literal_expansion_checked']=True
a['lean']['independent_kernel_evidence']=(d/'decision91.native.json').relative_to(R).as_posix()
assert rt.semantic_reviewer_packet(a)==before==load(r/'anti-anchored.review91.json')
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=r/'root.math91.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',native_hashes=expected,checked_RAW_descriptors=len(checked),
    reviewer=n['reviewer'],module=n['production'],exposition_accepted=True,canonical_source_packet_unchanged=True,VERIFIED=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Whole mathematics/kernel/leaf/exposition adopted;',len(checked),'RAW descriptors; source packet unchanged; no VERIFIED.')
