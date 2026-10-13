import hashlib,json,os,pathlib,re
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def ck(p):assert pin(R/p['path'])==p,p['path']
m=json.loads((O/'input.manifest.json').read_bytes());rows=m['qualified_raw_LF_pairs']
for row in rows:
 for k in ['original','raw_snapshot','lf_snapshot']:ck(row[k])
def f(i):return R/rows[i]['raw_snapshot']['path']
def j(i):return json.loads(f(i).read_bytes())
cov=j(0);graph=j(1);boundary=json.loads((O/'primary-first.boundary.json').read_bytes())
assert len(cov['regions'])==23 and cov['item_count']==45 and len(graph['nodes'])==14 and len(graph['hyperedges'])==9
ck(cov['primary']);primary=(R/cov['primary']['path']).read_bytes()
for x in cov['regions']:
 a,b=x['byte_range'];assert sha(primary[a:b])==x['qualified_raw_slice']['raw_sha256']
# Finite explicitly qualified immutable decoder native outputs and parent proof support.
extra=[];lease=j(8);receipt=j(7);assert lease['status']=='CLOSED' and lease['closed_last']
for x in lease['closed_output_pins']:
 p=pathlib.Path(x['path']);b=p.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];extra.append(p)
math=O.parent/'independent-math62'
extra += [math/'mathematical-proof.review.json',math/'focused.receipt.json',math/'focused.stdout.log']
parent=j(30)
parentlog=next(x for x in parent['inputs'] if x['path'].endswith('/focused-real-defect-root-v1/stdout.log'))
p=pathlib.Path(parentlog['path']);assert sha(p.read_bytes())==parentlog['raw_sha256'];extra.append(p)
supp=[]
for i,p in enumerate(dict.fromkeys(extra)):
 b=p.read_bytes();a=O/'inputs'/f'supp-{i:02d}-{p.parent.name}-{p.name}.raw.snapshot';z=O/'inputs'/f'supp-{i:02d}-{p.parent.name}-{p.name}.LF.snapshot';a.write_bytes(b);z.write_bytes(b.replace(b'\r\n',b'\n'));supp.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z),timing='Supplement pinned before its current provenance/API/axiom semantic read; original31 primary-before-candidate chronology unchanged'))
wr('supplemental.input.manifest.json',dict(qualified_raw_LF_pairs=supp,primary31_preserved=True,explicit_historical_native_mapping=lease['closed_output_pins']))
payloadraw=f(5).read_bytes();runraw=f(6).read_bytes();decoder=j(5)
assert sha(payloadraw)==receipt['payload_raw_sha256']==lease['payload_raw_sha256']
assert sha(runraw)==receipt['decoder_run_sha256']==lease['decoder_run_sha256']
assert runraw==b'NATIVE_ANONYMOUS_DECODER_RUN\nnative_pid=9656\ninput_receipt=input-pins.before-semantic-read.json\npayload_begin; exact full payload raw bytes follow\n'+payloadraw+b'\npayload_end\npayload_raw_sha256='+sha(payloadraw).encode('ascii')+b'\nNATIVE_FOREGROUND_READBACK_COMPLETE native_pid=9656 EXIT0\n'
assert not decoder['source_text_visible'] and not decoder['source_identity_visible'] and not decoder['compiler_started']
assert len(decoder['statements'])==2 and all(x['observed_exit_code']==0 for x in lease['native_terminal_receipts'])
for ix in [12,13,14]:
 p=rows[ix]['original'];q=next(x for x in parent['inputs'] if pathlib.Path(x['path']).resolve()==(R/p['path']).resolve());assert p['raw_sha256']==q['raw_sha256'] and p['lf_sha256']==q['lf_sha256']
# Full canonical60 lift, actual61/generic61 proofs are read, not previous source verdicts.
borrowed={str(ix):f(ix).read_text(encoding='utf8') for ix in [12,13,14]}
assert 'fixed_range' in borrowed['12'] and 'conjugateOperator_positive' in borrowed['14'] and 'hrootConj' in borrowed['14']
assert 'CenteredDefectOperator.actual_centered_selfadjoint_defect' in borrowed['13']
log=pathlib.Path(parentlog['path']).read_text(encoding='utf8')
for name in ['L2RealSquareRoot.exists_positive_real_square_root','RealDefectRoot.actual_positive_real_defect_root']:
 ax=re.search(re.escape(name)+r"' depends on axioms: \[([^\]]*)\]",log).group(1);assert set(x.strip() for x in ax.split(','))=={'propext','Classical.choice','Quot.sound'}
packets=[j(3),j(4)];units=[j(21)['units'][0],j(22)['units'][0]];pubs=[j(23)['items'][0],j(24)['items'][0]];draft=j(20);plan=j(19)
bindings=[]
for i,pkt in enumerate(packets):
 assert sha(canon({k:v for k,v in pkt.items() if k!='packet_sha256'}))==pkt['packet_sha256']
 assert not any(pkt['anti_anchoring'].values())
 assert sha(pkt['source']['original_text'].encode('utf8'))==pkt['source']['text_sha256']
 d=decoder['statements'][i];assert d['statement_sha256']==pkt['lean']['statement_sha256']
 assert d['reconstructed_theorem_text']==pkt['blind_reconstruction']['text']
 assert sha(d['reconstructed_theorem_text'].encode('utf8'))==pkt['blind_reconstruction']['text_sha256']
 assert pkt['blind_reconstruction']['decoder_run_sha256']==sha(runraw)
 module=f(9+i).read_bytes().replace(b'\r\n',b'\n').decode('utf8');h=f(15+i).read_text(encoding='utf8').strip()
 bodyheader=module.split('theorem '+pkt['lean']['declaration'].split('.')[-1],1)[1].split(':= by',1)[0].strip()
 assert h==bodyheader and pkt['lean']['statement'].strip()==h
 unit=units[i];pub=pubs[i];binding=pub['bindings'][0]
 assert unit['declaration']==pkt['lean']['declaration']==binding['declaration']==plan['mathematical_declarations'][i]
 assert unit['statement']==pub['statement']==unit['lean_statement']
 assert unit['steps']==draft['units'][i]['steps'] and unit['astis_dependencies']==plan['actual_ASTIS_parents'][i]
 digestpayload=dict(file=sha(module.encode('utf8')),current_lean_module=module,toolchain=rows[17]['original']['lf_sha256'],dependencies=rows[18]['original']['lf_sha256'],source=pub['source'],statement=pub['statement'],formulae=pub['formulae'],assumptions=pub['assumptions'],obligations=pub['obligations'],lesson=unit,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
 digest=sha(canon(digestpayload));assert digest==pkt['publication_binding_sha256'],(i,digest,pkt['publication_binding_sha256'])
 # Fresh packet context deliberately filters boundary/history and binding metadata.
 context=pkt['candidate_publication_context'];assert context['current_lean_module']==module
 assert context['lesson']=={k:v for k,v in unit.items() if k not in ['boundary','source_history_boundary']}
 assert context['binding']=={k:binding[k] for k in ['declaration','role','supports']}
 bindings.append(dict(item=i,packet=rows[3+i]['original'],reviewer_packet_sha256=pkt['packet_sha256'],publication_binding_sha256=digest,recipe='SHA256 canonical JSON of current LF module/hash, LF toolchain/manifest hashes, source/statement/formulae/assumptions/obligations, FULL authored lesson, ALL binding fields excluding only audit_id/legacy_audit_debt',publication=rows[23+i]['original'],lesson=rows[21+i]['original'],authored_assumption_deltas=binding['assumption_deltas'],fold_target=unit['declaration'],current_full_header_equal_presealed=True))
assert sum(len(x['steps']) for x in units)==7 and plan['private_providers']==[]
reasons=[
 'D1 supplies the real complete-Hilbert nonnegative unique-root background, not a printed proof of complexification. Canonical60 internally constructs positive lifts on the SAME arbitrary measure, with canonical quotient ofReal/re/im maps and norm-preserving embedding; no public map, CFC or probability certificate.',
 'Equal real operator squares apply to Rg and Qg. Complex linearity/intertwining gives Ac²g=ιA²Rg+iιA²Qg=ιB²Rg+iιB²Qg=Bc²g for every complex L2 class. This is ASTIS elaboration of background uniqueness, not B5 joint projection algebra.',
 'Both complex lifts are nonnegative; fixed Mathlib CFC.sqrt_unique identifies each with sqrt(Bc²). Instances are proof-local on COMPLEX bounded operators; restricted-real CFC on that complex algebra is not assumed on the real algebra. Positivity of BOTH A/B is necessary (I and -I otherwise have equal squares).',
 'Canonical norm preservation gives an injective real-linear isometry. Equality of lifts evaluated on ιu gives real operator equality, with no nontrivial or finite-dimensional L2 assumption. No new private helper/finite spectral basis/real CFC premise.',
 'Actual61 internally supplies original-input normalized μ,J,ν, every-y tilted S, reflected Λ disintegration and stationary marginals; same selfadjoint contractive mean-preserving per-u AE T, positive D=I-T² and positive real Γ with full scalar energy. Borrowed actual59/60/61 are dependencies, not caller hypotheses. Pointwise conjugation in61 differs from operator adjoint; full fixed-range descent is already internal61.',
 'Every positive alternative Γprime on this SAME real L2(ν), with Γprime²=this SAME D, has square equal to produced Γ². Generic uniqueness applies with BOTH positivities. The whole forall-u energy proposition is parenthesized before conjunction with forall-Γprime; no energy certificate/commutation/invertibility is assumed for alternatives.',
 'Genuine original-input Test substitutes Γprime=Γ and obtains scalar energy and contraction from energy plus nonnegative norm squares. It is a Test-only consumer, not a production dependency. No centered gap/order/inverse/polar, printed joint GammaP/B11, dynamics/main/error/cost/composition conclusion follows here.'
]
wr('formula-source.review.json',dict(status='accepted-scoped-source-content; native rendered/copy/full-exposition seal separate',current_two_full_statements_checked=True,formula_steps=[dict(index=i+1,authored_step=step,source_and_body_reason=reasons[i],accepted=True) for i,step in enumerate(units[0]['steps']+units[1]['steps'])],private_provider_count62=0,public_proof_count62=2,genuine_Test=True,bindings_checked=bindings,source_graph_vs_implementation='Literal D1/model/B1-B5/B10 topology and all excluded polar/rate/H1/main regions are independent14node9hyperedge graph; current canonical60 complexification/CFC/injective descent is the attributed selected ASTIS background implementation route, not a reconstruction of printed source edges.',source_before_current_body=boundary,coverage=cov,graph=graph,borrowed_raw_pins=[rows[i]['original'] for i in [12,13,14]],standard_axioms='Current separate independent math62 reports only propext/Classical.choice/Quot.sound for both public declarations; parent61 raw frozen compiler log checked same for generic/actual61. Compilation supplies proof evidence only.',publication_metadata_convention='Attributed background generalization and explicit rank-zero extension are retained. Remaining-paper clauses are exclusions, not proved nodes. Some purification historical scope prose mentions generic uniqueness as separate; current full statement/binding/obligations/7 steps explicitly prove scalar uniqueness only; no source assumption change is inferred from that conservative historical scope text.',repairs=[],blocking_issues=[]))
slot_names=['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']
originals=[[
 'Arbitrary measurable Ω, measure μ, bounded positive REAL A/B, multiplication composition.',
 'D1 uses real AE quotient complete L2; ASTIS attributed background generalization permits arbitrary μ, including zero and infinite L2.',
 'For all Ω/μ/A/B satisfying BOTH positivity hypotheses and same operator square, A=B.',
 'A.IsPositive, B.IsPositive, A*A=B*B; measurable structure and real L2 typing only.',
 'Equality A=B of bounded real-linear operators, not an existence or energy theorem.',
 'Attributed real-Hilbert background completion of D1, scalar antecedent only; printed B10/B11 joint/macro transport excluded.',
 'No rates/constants, η prefactor, finite/probability μ, finite L2 or Nontrivial restriction.'
 ],[
 'Original V/α/β/η define normalized μ, Gaussian joint J, ν=J.snd, reflection Λ; internally produced S/T/D/positive REAL Γ.',
 'Finite-dimensional real Hilbert Borel E/canonical volume (Euclidean adapter), explicit rank0 extension; full REAL AE quotient L2(ν) can be infinite-dimensional.',
 'Global Hessians all x/v; normalized S identity EVERY y; T action per-u ν-AE; root energy ALL u; ALL positive Γprime on same L2 whose square is SAME D, outside forall-u energy.',
 'C2 V,0<α≤β,global lower/upper Hessian bounds,η>0,βη≤1; no probability/kernel/T/root/positivity/CFC/alternative-energy/finiteL2 certificate supplied.',
 'Probability μ/J/ν,normalized Markov S and stationary disintegration, selfadjoint contractive mean-preserving AE T,positiveD,positiveΓ²=D,full energy,unconditional uniqueness among positive same-square alternatives.',
 'Actual scalar D=I-T² root from SAME genuine source kernel/T; D1 background completion only, not full printed joint GammaP/B11/ontoM/B*B, centered order/inverse/polar/H1/dynamics/main/error/querycost/composition.',
 'Exact (y+x)/2 and denominator8η with state normalization; Gaussian sqrtη;non-strictβη≤1, αη=1 legal whenα=β; noη-prefactor inΓ² orenergy, no ρ/δ/rate claims.'
 ]]
evidence=[
 ['D1 real L2 convention; header0 exact expansion and canonical60 lift.', 'LiteralD1 probability convention is background, not public finiteness; Lp2 is complete for arbitraryμ; disclosed generalization.', 'Public header0 all binders and ext proof; decoder0 reconstructed forall shape.', 'No proof-local letI appears in public header; both positive-root premises exactly required.', 'Canonical60+complexsqrt_unique+ι injectivity establish exact real equality.', 'PrimaryB10/B11, graph EXCLUDED regions and authored attribution delimit scope.', 'No scalar parameters in header0; zero/subsingleton cases need no extra witness.'],
 ['PrimaryS1/S2E6/E7/C1/B1-B5; current actual61 destructuring retains SAME objects.', 'SourceEuclidean complete real Hilbert typing adapter; finiteE separate from Lpdimension; rank0 explicitly disclosed.', 'Exactheader1 parenthesization and per-u AE action; primary C1 state density and B9 conditional action.', 'LiteralA2.Theorem1.p1 βη≤1; modelglobalC2/Hessians; actual61 internally constructs all mathematical ingredients.', 'Parent61 producesΓ, newpublic proof appliesgeneric62 to arbitrarypositiveΓprime and sharedD; genuineTest substitutes equality.', 'SourceB10 ΓP onranP; B11 defectB*B identity excluded; no macroonto/joint unit/polar rate completion.', 'LiteralC1 denominator8η, S2noise sqrtη, globalαβ inequalities and exactcap; no strictendpoint/extraenergy assumption.']]
for i,pkt in enumerate(packets):
 d=decoder['statements'][i];slots={name:dict(original=originals[i][k],reconstructed=d[name],relation='explicit-elaboration' if name in ['domains','scopes'] else 'equivalent',evidence=evidence[i][k]) for k,name in enumerate(slot_names)}
 deltas=[dict(slot='domains',classification='generalization' if i==0 else 'domain-clarification',blocking=False,description='D1 printed probability-L2 background is explicitly generalized to arbitrary-measure real L2.' if i==0 else 'Finite real Hilbert Borel volume is a source Euclidean coordinate adapter, with rank-zero extension explicitly disclosed; no finite-dimensional L2 assumption.'),dict(slot='scopes',classification='unresolved',blocking=False,description='Scalar real positive uniqueness only. Printed jointGammaP/ontoM/typedB*B/centeredorder/inverse/polar/H1/dynamics/main/error/querycost/composition remain separate, not erased source edges.')]
 decision=dict(semantic_slots=slots,deltas=deltas,verdict='equivalent-after-elaboration',repairs=[],reviewer='/root/next_primary59',independent_from_formalizer=True,independent_from_decoder=True,reviewer_packet_sha256=pkt['packet_sha256'],publication_binding_sha256=pkt['publication_binding_sha256'],publication_exposition_verdict='accepted-scoped-source-content; native rendered/copy/full-exposition seal separate',excess_count=0,blocking_issues=[],review_evidence='Primary-first literal23regions/45coverage/14node9hyperedge reconstruction before fresh packets/decoder; current complete declaration/Test and borrowed canonical60/actual61/generic61 proof comparison; independently checked exact full publication digest/7 formula steps. See formula-source.review.json and native input/readback maps.',mathematical_evidence=rows[25]['original'],native_math_run_is_distinct=True,no_state_transition=True,full_paper_completion=False,remaining_boundary=plan['remaining_boundary'])
 wr(f'source.{i}.decision.sealed.json',decision)
wr('provenance.recipe.checks.json',dict(actual_foreground_pid=os.getpid(),reviewer_packets=bindings,anonymous_native_payload=rows[5]['original'],anonymous_native_whole_run=rows[6]['original'],anonymous_CLOSEDLAST=rows[8]['original'],decoder_receipt_closure_written_false_is_preclosure_history=True,anonymous_full_raw_payload_exactly_embedded_in_whole_run=True,parent_mathfreeze_matching_sources=[rows[i]['original'] for i in [12,13,14]],source0_1_statementsha_match_originalheaders=True,formula_count=7,private_helpers62=0,no_compiler_started=True))
wr('author.receipt.json',dict(actual_foreground_pid=os.getpid(),verdicts=['equivalent-after-elaboration']*2,excess_count=0,repairs=[],source_first_pid=m['source_first_pid'],source_primary_before_current_packets_decoder=True,source_decisions_fixed=True,compiler_started=False,source_semantic_review_independent_from_previous_verdicts=True))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),status='SOURCE_DECISIONS_FIXED',verdicts=['equivalent-after-elaboration']*2,formula_steps=7,primary23coverage45=True,original_pairs=31,supplemental_pairs=len(supp),publication_digests=[x['publication_binding_sha256'] for x in bindings],compiler=False)))
