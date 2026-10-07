from pathlib import Path
import hashlib,json,copy
scratch=Path('.astis/gaussian-entropy33')
run=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy');pre=run/'preproof'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):
 p=Path(p);assert not p.exists(),p
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def bind(p):
 p=Path(p);b=p.read_bytes()
 return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),bytes=len(b))
lease=read(scratch/'reviewer.statement.preliminary.lease.json')
assert all(lease[k]=='CLOSED'for k in ['status','read_lease','write_lease','compiler_lease'])
review=read(scratch/'reviewer.statement.preliminary.review.json')
assert review['verdict']=='PRELIMINARY_NO_MATHEMATICAL_OR_SOURCE_ASSUMPTION_BLOCKER'and not review.get('blockers',[])
typecheck=read(scratch/'root.statement-typecheck.0.json');assert typecheck['exit_code']==0
for x in lease['inputs']:
 assert all(bind(x['path'])[k]==x[k]for k in ['raw_sha256','lf_sha256']),x['path']
 assert all(bind(scratch/x['snapshot'])[k]==x[k]for k in ['raw_sha256','lf_sha256']),x['snapshot']
pre.mkdir(parents=True,exist_ok=False);historical=pre/'historical-scratch';historical.mkdir()
for p in scratch.iterdir():
 if p.is_file():(historical/p.name).write_bytes(p.read_bytes())
for f in ['source.signature.txt','S3.E2.raw.snapshot.html','S4.Ex3.raw.snapshot.html']:
 (pre/f).write_bytes((scratch/f).read_bytes())
for original,portable in [('root.statement-typecheck.0.json','root.statement-typecheck.original.raw.json'),('root.statement-typecheck.0.log','root.statement-typecheck.original.raw.log'),('StatementTypeProbe.lean','root.statement-typeprobe.lean'),('reviewer.statement.preliminary.review.json','reviewer.statement.preliminary.original.raw.json'),('reviewer.statement.preliminary.lease.json','reviewer.statement.preliminary.original.raw.lease.json')]:
 (pre/portable).write_bytes((scratch/original).read_bytes())
prop=read(scratch/'root.statement-proposal.json');old=copy.deepcopy(prop)
prop['targets'][0]['signature']=bind(pre/'source.signature.txt')
prop['additional_primary_spans']=[dict(anchor=x['anchor'],**bind(pre/Path(x['path']).name))for x in prop['additional_primary_spans']]
prop['portability_scope']='Only stable candidate/source/signature paths and explicit metadata fields. Original rootproposal and preliminary receipts/rawsnapshots preserved; exact mathematical signature bytes unchanged.'
prop['definition_audit']=dict(mu='Literal canonical normalized Gibbs volume tilt by -V.',R='True RGO posterior, second quadratic tilt with exact1/(2eta).',p='One internally produced measurable stationarypoint from current32; uniqueness conclusion derived from unchanged curvature, not assumed.',r='Actual affine true RGO pushforward with SAME p and square-root scale.',gamma='Actual centered covarianceI stdGaussian E, includingE0.',Z='Actual positive Gaussian-relative partition from current32, not supplied.',q='Literal positive exp(-rho)/Z. RN/logratio equality remainsAE only, never used for pointwise derivatives.',KL='Pinned canonical ENNReal InformationTheory.klDiv with !=top output; both laws internally probabilities, so masscorrection cancels.',entropy='True qlogqL1gamma/logqL1r/rhoL1r, exact canonicalKL realvalue and -Erho-logZ formula. No canonicalRN smooth-Fisher witness or weakSobolev/LSI/T2/W2 claim.')
prop['typecheck_receipt']=(pre/'typecheck.portable.json').as_posix()
prop['dependency_admission']='Require current32 independent VERIFIED exactcommit before any newSAU claim or implementation. Statement-only preproof can be reviewed before that state transition.'
write(pre/'root.statement-proposal.json',prop)
write(pre/'typecheck.portable.json',dict(schema_version=1,status='type-elaboration-pass',exit_code=0,original_receipt=bind(pre/'root.statement-typecheck.original.raw.json'),original_log=bind(pre/'root.statement-typecheck.original.raw.log'),portable_probe=bind(pre/'root.statement-typeprobe.lean'),signature=bind(pre/'source.signature.txt'),transformation=typecheck['transformation'],theorem_bodies_or_proof_search=False,production_edits=False,compiler_lease='CLOSED'))
write(pre/'portability.proposal.json',dict(schema_version=1,status='metadata-path-only-pending-independent-final-StatementSeal',original_root_proposal=bind(historical/'root.statement-proposal.json'),portable_root_proposal=bind(pre/'root.statement-proposal.json'),exact_signature_unchanged=old['targets'][0]['signature']['raw_sha256']==prop['targets'][0]['signature']['raw_sha256'],historical_scratch=historical.as_posix(),type_only_receipt=(pre/'typecheck.portable.json').as_posix(),new_definition_audit='Explicit roles only; no statement or assumptions changed',no_new_SAU_claim_or_proof_body=True))
print('Portable exactsource candidate and type-only evidence frozen; no claim/proofsearch. Final independentStatementSeal requested next.')
