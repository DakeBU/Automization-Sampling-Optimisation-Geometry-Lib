import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,base64,datetime
O=pathlib.Path(__file__).resolve().parent
def H(b):return hashlib.sha256(b).hexdigest()
def C(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def J(n):return json.loads((O/n).read_bytes())
def save(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
packet=J('final70.official-source-review.packet.1.exactraw.json')
expect=J('stageA.source-expectations70.before-current-BODY.frozen.json')['canonical_semantic_slots_source_expectations']
blind=J('blind70.slot-decisions.json')['reconstruction_fields']
evidence={
'objects':'Primary source graph P1-P14; J/U/P/R/A0/ΓP0/Inv/B0/V0 are the SAME actual objects (literal27-124). g at125/412 is actual U(Pf-(f-Pf)); gP128/417 is actual condExp and gV130=V0*Rg. Full literal is an exact definition, not mathematical provider. Exact original header/literal and complete69 retention mechanically checked.',
'domains':'Source B1/B2/B3 and D1 real-L2 conventions; literal33-41,74-116,117-133. HP0 uses constant orthogonality, Hperp is kerP, not mean-zero ambient H. D acts on all kerP, centered inverse stays HP0. L2 integrability and AE pullback transport produced314-335; hRmicro354-356 validates inclusion identity, ambient adjoint407-411 explicit.',
'quantifiers':'Source expects fixed operators then every actual centered f. Literal45-108 introduces12 common witnesses, ∀f117, ∃fP118 and ∃gP127 follow f. Six public analytic hypotheses136-143 exactly match private19-26 and original sealed header; no operator certificate, mean_g or ontoV caller. U/T AE representative equality is per input; no common null set invented. Every-state S formula retained.',
'assumptions':'Source global hypotheses and actual law B1 match exactly hα,hαβ,hV,hH,hη,hβη. Finite-dimensional real Hilbert Borel base is coordinate-invariant representation of R^d; rank0 is explicitly disclosed extension. βη≤1 remains non-strict and legal αη=1 retained. Root positivity/inverse/kernel/mean are conclusions/dependencies, not callers. Full-body review found no new regularity, ρ/ω/c0 or sharp-energy68 premise.',
'conclusion':'Primary A2.Ex12/Ex13/Ex15 exact signs, A²+Γ²=I, real rotation; actual components first independently defined. Macro423-448 yields A0fP-ΓP0fV, micro449-455 uses inherited all-kerP negative intertwining to yield ΓP0fP+A0fV, energy456-458. Internal mean413-416 permits actual gP417. Exact69 value recovered byte-for-byte after deleting only70 tail. Source B21 corrector-change and B4 consumers remain future claims.',
'scopes':'Same common root/inverse/polar preserved through reassembly480-539. Zero-mean premise only on f, zero mean g is output. Source F#J=J plus L2 integrability and condExp integral law complete omitted internal mean adapter314-335/413-416. Into V0 and onto e distinguished. Scoped static reader51948 EXIT0 shows full private literal adjacent, closed, with correct definition/nonprovider label and8 exact BODY folds; full browser/live/Exposition/PURIFIED outside audit.',
'constant_dependencies':'γ=2sqrt(αη)/(1+αη) and centered bound1/γ are SAME parent data. Pair-energy uses only SAME A0/ΓP0 selfadjoint square sum/commutation internally366-381. Six original caller conditions; no dimension positivity, ontoV, full-space inverse, extra smoothness or 68sharpenergy/ρ/ω/c0 dependency. P16/P17/P19/P21 are real primary consumers, not invented Lean parents.'}
relations={'objects':'explicit-elaboration','domains':'explicit-elaboration','quantifiers':'equivalent','assumptions':'explicit-elaboration','conclusion':'equivalent','scopes':'explicit-elaboration','constant_dependencies':'same'}
slots={k:{'original':expect[k],'reconstructed':blind[k],'relation':relations[k],'evidence':evidence[k]} for k in expect}
delta_specs=[
('objects','Coordinate-invariant finite real Hilbert/Borel representation and normalized tilt make source R^d/probability notation explicit; rank-zero extension is disclosed.','Source P0/P1; literal19-42. No assumption of finite-dimensional L2.'),
('domains','Real L2/AE classes, measurable conditional subspace and explicit inclusion maps replace informal function/block notation.','Primary D1 and B1; literal33-41,98-111; proof326-365/407-411.'),
('quantifiers','Twelve jointly chosen common witnesses precede every centered observable; per-f and per-g conditional components remain actual existentials.','Literal45-133; exact parent69 recovery; no free operator certificate caller.'),
('assumptions','Original six analytic caller conditions are preserved; rank0 and αη=1 retained. All other source ingredients are internally produced dependency edges.','Public136-143/private19-26 exactly byte-equal to original seal; no new premise.'),
('objects','Private literal stores the exact complete sealed result; public theorem asserts it. It is not a provider.','Exact literal27-133 equals original header10-116; unfold144; reader nonprovider contract independently checked.'),
('domains','D is exactly canonical R U inclusion on the whole conditional-mean-zero microspace kerP.','Literal112-116; local310-313; inherited all-micro identity applied to actual fperp449-455.'),
('scopes','SAME nonnegative root, centered inverse and polar embedding used throughout; onto e never promoted to onto V.','Literal67-107; inverse only HP0; V*V=I, no VV*=I; proof361-365.'),
('scopes','Mean(g)=0 is an internally proved completion of source actual reflection/condExp semantics, not extra caller.','Primary F preservation S2.E14 plus B1 U/P; proof314-335/413-416.'),
('conclusion','Actual gP and gV are independently fixed by condExp and V*Rg before the coefficient equations are proved.','Literal125-133; proof417-418/423-455; not RHS-defined vectors.'),
('conclusion','Exact two-component squared-energy conservation is stated for the actual output and source signs.','Primary A2.Ex12.m1,A2.Ex15.m2,A2.SS3.p5.m20/21; proof366-381/456-458.'),
('constant_dependencies','Parent69 and actual-law reflection preservation are the real Lean dependencies; sharp-energy68 is absent.','Import1, call158-159 and law318-319; exact lesson astis_dependencies two identities.'),
('scopes','P16/P17 corrector algebra/B21, P19/B4 and P21 explicit pair-energy budget are genuine primary consumers; no completion credit inferred.','Primary A2.E20/A2.E21/A2.E27/A2.SS3.p9.m2; source graph edges and publication boundary.'),
('scopes','Current70 lesson has eight exact contiguous BODY steps. Frozen StageA reader expectation inherited a six-step count from69; current finite8-step coverage supersedes that count explicitly.','Eight spans144-539; exact code hashes/521NODE+23EXCLUDED module coverage. This is reader bookkeeping, not formula repair.')]
deltas=[{'slot':k,'severity':'informational','description':d,'evidence':e} for k,d,e in delta_specs]
base={'semantic_slots':slots,'deltas':deltas,'verdict':'equivalent-after-elaboration','repairs':[],'reviewer':'independent_primary69 / independent-source70','independent_from_formalizer':True,'independent_from_decoder':True,'review_evidence':str(O/'source.0.review.complete-RAW.txt')}
save('source.0.semantic-base.json',base)

# Two reader-only metadata changes are exact and exhaustive; packet projection unchanged.
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):
  return sum((diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))),[])
 if isinstance(a,list):
  return sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[]) if len(a)==len(b) else [p]
 return [] if a==b else [p]
pc=diff(J('current70.publication.exactraw.json'),J('final70.publication.exactraw.json'))
fc=diff(J('current70.frontier.exactraw.json'),J('final70.frontier.exactraw.json'))
assert pc==['/items/0/purification/dead_code_audit'] and fc==['/purification/dead_code_audit']
save('stageB.exact-final-reader-overlay-comparison.json',{'publication_changed_fields':pc,'cell_changed_fields':fc,'recommended_after':'One public production theorem with an exact private literal statement definition; no proof provider or wrapper Test.','only_two_fields_changed':True,'Lean_lesson_expanded_statement_blind_neutral_packet_unchanged':True,'packet0_packet1_RAW_same':True,'no_math_source_binder_BODY_repair':True})

# Complete finite exact inputs. Historical pre-overlay snapshots are retained and typed.
groups=[('stageA.complete-primary-input-manifest.frozen.json','primary-before-BODY',False),('stageB.current-input-manifest.json','official-packet0-pre-overlay',False),('stageB.supplemental-input-manifest.json','supplemental-exact',False),('stageB.blind-complete-input-manifest.json','blind-native-closure',False),('stageB.final-input-manifest.json','official-final-packet1-current',True),('stageB.terminal-and-render-input-manifest.json','actual-terminal-and-render-support',True)]
inputs=[]
for name,stage,current in groups:
 for q in J(name)['inputs']:
  row=dict(q);row['snapshot']=row.get('snapshot',row.get('RAW_snapshot'));row['original_path']=row.get('original_path',row.get('source_path'));row['stage']=stage;row['assert_original_still_current_at_finalization']=current
  b=(O/row['snapshot']).read_bytes();l=(O/row['LF_snapshot']).read_bytes();assert H(b)==row['RAW_sha256'] and len(b)==row['RAW_bytes'];assert l==b.replace(b'\r\n',b'\n') and H(l)==row['LF_sha256']
  if current:assert pathlib.Path(row['original_path']).read_bytes()==b
  inputs.append(row)
assert len(inputs)==74
save('complete-exact-input-manifest.json',{'schema':'independent-source70-complete-exact-inputs-v1','input_count':len(inputs),'inputs':inputs,'historical_snapshot_policy':'packet0/cell/pub before reviewed two-field overlay preserved exactly; old versions never asserted current. Immutable prior sources reused read-only.','all_LF_recipe':'replace ONLY CRLF byte pairs with LF; no other normalization','full_primary_RAW_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'})
payload={'schema':'independent-source70-exact-named-RAW-LF-input-payload-v1','input_count':len(inputs),'inputs':[{**x,'RAW_base64':base64.b64encode((O/x['snapshot']).read_bytes()).decode(),'LF_base64':base64.b64encode((O/x['LF_snapshot']).read_bytes()).decode()} for x in inputs]}
save('complete-exact-RAW-LF-input-payload.json',payload)

review='''Independent primary-source fidelity review of actual projected rotation70

Verdict: equivalent-after-elaboration for the bounded current actual-input projected reflection rotation and two-component energy edge. No source mathematical/binder repair is required. This is an independent source decision, not proving-worker self-verification, SAU VERIFIED, B21 corrector-change, B4, whole-paper, full Exposition Seal, PURIFIED, merge, main or live acceptance.

Ordering and exposure: primary-first StageA was frozen before full current70 BODY or blind70 reconstruction. Reused immutable source-only22-node49-edge topology and source419 inventory are explicitly attributed; actual primary RAW/anchors and current source roles were independently checked. Prior CLOSED83 header-source and representation-only reviews were not substituted for this full-module review. Earlier opaque BODY equality exposure and tiny header-adjacent syntax exposure are disclosed in stageA.anti-anchoring-exposure70.frozen.json; no earlier mathematical reading of full70 BODY occurred. StageB read official packet then all544 current module lines, full private/public statement, all8 lesson formulas/code, blind complete reconstruction/7 canonical fields, and exact final publication/cell. No independent math verdict, prior69/68 semantic verdict, decoder reconstruction for other targets or proof-search output was used as authority.

Primary provenance: fixed PBPS arXiv2609.06905v1 full RAW1482128B SHA d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760. Seven immutable RAW slices with exact absolute offsets,419math identities and formula hashes. Source graph22nodes49edges remains a SOURCE graph, not Lean dependency certification. Exhaustive primary419 decisions175NODE244EXCLUDED and current module544 decisions521NODE23EXCLUDED are finite coverage, never automatic proof credit. All24 pre-BODY obligations have explicit current decisions.

Source and exact semantics: P12 source f in L2_0, fP=Pf,fperp=Pperpf,fV=V*fperp; P13 Kid=U(P-Pperp),g=Kidf,gP=Pg,gV=V*Pperpg; P14 matrix[A,-Γ;Γ,A] and A²+Γ²=I. The current complete literal retains the originally sealed six analytic callers and12 common original witnesses, old global-f/adjoint/norm conclusions, same U/root/centered inverse/polar/actual canonical R,D. Deleting only new70 rotation tail and restoring old terminal conjunction recovers complete parent69 literal value byte-for-byte. Literal27-133 exactly equals the original header result10-116. Public theorem keeps original six callers and asserts literal; unfold144 establishes representation only, not a provider premise.

Internal mean completion: actual F(x,y)=(x,2x-y) preserves SAME J. GaussianReflection.reflection_preserves_augmentation, measurable F and hU per-input AE plus integral_map derive integral(Uu)=integral(u). Actual condExpL2 on univ gives integral(Pu)=integral(u); L2 is integrable on probability J and Lp subtraction AE adapter is produced internally. Therefore integralg=integralPf-[integralf-integralPf]=integralf=0. This is an internally supplied omitted adapter, not mean_g caller or fresh centered output. gP is produced by the original global conditional decomposition applied to actual g with this derived mean, not chosen as RHS. gV literally V0*Rg.

BODY: 144-309 unfold and destructure complete69 parent using exactly6 callers. 310-336 canonicalD,law/probability/AE/integral/condExp adapters and selfadjointP. 337-365 actual block inclusion/orthogonality/adjoint/factorization. 366-381 same-root real energy and cross inner terms. 382-422 actual f and g conditional data, mean completion. 423-448 macro rotation by inner separation. 449-455 micro rotation using inherited ALLkerP V0*D=-A0V0*, giving PLUS A0fV. 456-539 energy cancellation and complete conclusion/witness reassembly. These are exactly8contiguous publication BODY slices covering396lines144-539, with exact UTF8 snippet equality including terminal LF and stored SHA matches. All implementation lines and source items individually enumerated in named coverage artifacts.

Domains and endpoints: HP0 is constant-orthogonal centered macroscopic subspace; Hperp=kerP, not mere global mean-zero or rangeV. D=R U inclusion acts on ALLkerP. V0*V0=I is embedding, no ontoV/VV*=I/fperp=VfV. Inverse only same HP0; full root kills constant. e is onto equivalence, distinguished from V0. Per-observable AE null sets may depend on observable; kernel law every-state quantifier retained. αη=1 and rank0 remain legal. No H1/smooth observable, extra potential derivatives, ρ/ω/c0, sharp-energy68, positive rank or independent operator certificate caller.

Consumers/boundary: P16 corrector C(u,v)=1/2(||u||²-||v||²)-<AInvu,v> and P17 actual B21 C-change remain NEXT separate source-backed edge. P19/B27 has actual comparator (Kf)P=gP+Γrρ,(Kf)V=gV-Arρ; P20/B28 adds B21. P21 primary A2.SS3.p9.m2 explicitly consumes pair energy as ||gP||²<=||gP||²+||gV||²=||fP||²+||fV||². Thus these are real paper consumers; none is a70 conclusion or invented sharp-energy68 parent. B4 errors/contraction/H1/dynamics/main/query costs/composition/full paper remain open.

Reader: bounded static current renderer/scanner test uses only3exact modules, one lesson and pinned scripts, no whole repo/site scan or browser. It resolves complete private full identity, exposes entire exact literal as adjacent nested fold with definition/nonprovider label, public signature/proof and all8 exact code folds closed initially. Full module/download context retained. Root31focused tests/pycompile receipts captured; full browser/visual/live/Exposition are not claimed. Two stale dead_code_audit process-reader prose fields contradicted private literal and were independently reviewed/adopted by root21704EXIT0; exact2-field comparison shows no other cell/pub change. Packet1 regenerated byte-identical to packet0 because these fields are outside binding/context projection; record actual same hashes. Original lesson formulas were correct: an exploratory nested-repr misreading caused false double-backslash alarm, withdrawn after direct byte inspection and scoped render. No formula change applied.

Verification boundary: owner canonical focused Lean PID9524 EXIT0/3949jobs receipt and exact RAW stdout/stderr captured and hash-checked, module03a0721... pinned. Source reviewer did not compile Lean or claim math verifier credit. Reviewer foreground receipts preserve failures and corrected runs: initial exact-code check incorrectly stripped terminal LF(47340EXIT1), nested-repr false formula check(14512EXIT1), corrected finite audit41528EXIT0, static reader51948EXIT0, exhaustive24364EXIT0, final inputs9908EXIT0, actual terminal capture34624EXIT0. Earlier StageB wrong-path capture4588EXIT1 and exploratory console GBK/unknown-key failures are explicitly retained/disclosed; unavailable exploratory child PIDs not invented. Old CLOSED bundles unchanged.

All exact RAW and CRLF-only LF inputs, named review/decision/run, fullfinite coverage and helper/failure/terminal manifest are preserved in this owned scope. Final lease will be last owned write, then read-only verification. No canonical/Git/ledger/Goal writes.
'''
review+='\nSeven semantic slots (original primary expectation; exact blind reconstruction; independent relation/evidence):\n'+json.dumps(slots,ensure_ascii=False,indent=2)+'\n\nAll typed deltas:\n'+json.dumps(deltas,ensure_ascii=False,indent=2)+'\n'
(O/'source.0.review.complete-RAW.txt').write_text(review,encoding='utf-8',newline='\n')
print(json.dumps({'actual_pid':os.getpid(),'seven_slots':7,'deltas':len(deltas),'blocking_deltas':0,'mathematical_repairs':0,'verdict':base['verdict'],'exact_inputs':len(inputs),'reader_only_changed_fields':pc+fc},ensure_ascii=False))
