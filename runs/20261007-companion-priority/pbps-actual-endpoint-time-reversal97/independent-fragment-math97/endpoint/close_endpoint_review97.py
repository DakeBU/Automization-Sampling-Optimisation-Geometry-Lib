from pathlib import Path
import hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parents[1];P=B.parent/'pbps-endpoint-time-reversal-preread97';F=B/'focused97/endpoint2-explicit-terminal-type'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes());norm=lambda t:re.sub(r'\s+',' ',t).strip()
def rel(p):return p.relative_to(R).as_posix()
def info(p):return dict(path=rel(p),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
src=B/'ActualEndpoint97.lean';raw=src.read_bytes();assert sha(raw)=='2d35c29f19523b9f43a53aaef00e70ab74c38605d7e96b87c945bf50f651cb75'
assert (F/'input.exactraw.lean').read_bytes()==raw
rc=load(F/'receipt.json');assert rc['input_raw_sha256']==sha(raw) and rc['exit_code']==0 and rc['terminal_closed'] and not rc['complete_SAU']
assert not (F/'stderr.log').read_bytes()
stdout=(F/'stdout.log').read_text(encoding='utf8');assert "'PBPSEndpointDataWork97.endpoint_data' depends on axioms: [propext, Classical.choice, Quot.sound]" in stdout
text=raw.decode();header=(P/'Header97.lean').read_text(encoding='utf8');statement=text.split('theorem endpoint_data',1)[0];theorem=text.split('theorem endpoint_data',1)[1]
assert norm(statement[statement.index('{E : Type*}'):statement.index(': Prop := by')])==norm(header[header.index('{E : Type*}'):header.index(': Prop := by')])
assert norm(theorem[theorem.index('{E : Type*}'):theorem.index(': statement')])==norm(header[header.index('{E : Type*}'):header.index(': Prop := by')])
def block(t,name):
 s=re.search(r'^    let '+re.escape(name)+r'(?=\s|:)',t,re.M);assert s,name
 e=re.search(r'^    (?:let |∀ |∃ )',t[s.end():],re.M);assert e,name
 return t[s.start():s.end()+e.start()]
names=['c','Φ','S','Rec','Hist','Δ','Prefix','m','zAt','K','Path','Ψ','Γ']
for name in names:assert norm(block(statement,name))==norm(block(header,name)),name
scan={p:bool(re.search(p,text)) for p in [r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'\bunsafe\b',r'\bnative_decide\b',r'Prop\s*:=\s*True',r':=\s*trivial']};assert not any(scan.values())
paths=[src,F/'input.exactraw.lean',F/'receipt.json',F/'stdout.log',F/'stderr.log',B/'focused_check97.py',P/'Header97.lean',P/'root.statement-seal97.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean',R/'lean-toolchain',R/'lake-manifest.json']
snap=O/'inputs';snap.mkdir(exist_ok=False);inputs=[]
for i,p in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=rel(q)))
v=dict(kind='independent-compiled-mathematical-fragment-review',reviewer='/root/exact_verifier96',decision='ACCEPT_EXACT_COMPILED_ACTUAL_ENDPOINT_DATA_FRAGMENT',fragment=info(src),inputs=inputs,required_repairs=[],observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
statement_audit=dict(six_original_analytic_binders_preserved=True,ambient_instances_preserved=True,private_Prop_and_theorem_binders_match_seal=True,literal_definitions_matched_to_header=names,additional_provider_hypotheses=[],conclusions=['MeasurableSet exact strict Delta','joint actual Gamma measurability at fixed n,T','joint actual Gamma terminal evaluation measurability','pointwise exact final harmonic arc identity for every initial state and strict tuple']),
mathematical_audit=[
 dict(region='exact carriers',finding='All 13 inherited local definitions in the private statement match Header97 after whitespace normalization. The displayed endpoint is literally Gamma evaluated at the subtype terminal time, not an unlinked surrogate word. Standard Hilbert/Borel structures and all six analytic assumptions are retained.'),
 dict(region='actual OrderedPrefix producer',finding='actual_ordered_prefix_law is applied with exactly hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta. Its n,T first projection gives MeasurableSet Delta. This is the missing local ingredient for Simplex97.rho_volume, discharged as a compiled dependency rather than added to the public source statement.'),
 dict(region='actual93 joint Gamma projection',finding='actual_finite_count_path_law returns a process Z and hdata. At n,T, hdata consists of Psi measurability, Gamma measurability, rho-density measurability and the pointwise history/path package. (hdata n T).2.1 selects exactly joint Gamma. Extracting the process existential only to access this property adds no assumed process provider.'),
 dict(region='terminal coordinate evaluation',finding='The terminal coordinate is explicitly typed as {s:NNReal // s<=T}. measurable_pi_apply at this fixed index, composed with joint Gamma, proves exactly joint endpoint measurability for ((y,r),z,t). It does not require continuity at bounce zero normals and does not assert measurability in a varying dependent T.'),
 dict(region='last-time inequality n=0',finding='Fin.last 0 is the only grid index and cons0 evaluates to zero. T.coe_nonneg proves last grid time<=T, including T=0. No dummy nonempty event index is introduced.'),
 dict(region='last-time inequality n>0',finding='After n=succ k, the final cons-grid coordinate is t(Fin.last k). The original strict simplex upper-bound field gives t(last)<T, then <=T. This supports conversion to the real elapsed terminal gap without changing NNReal subtraction conventions.'),
 dict(region='pointwise final interval identification',finding='For fixed y,r,z, hd=(hdata n T).2.2.2 y r z has four leading measurability fields followed by the deterministic interval clause. hd.2.2.2.2.1 applies at actual t, s=T, j=Fin.last n. hlast supplies the lower-bound condition. The later-grid condition is vacuous because every k<=Fin.last n, so k>last is contradictory. This yields the exact formula at all states/tuples, without AE/no-event-at-T assumptions.'),
 dict(region='degenerate and zero-normal coverage',finding='At n=0 the formula identifies Gamma(T)=Phi_T zAt0; it remains valid at T=0. With n>0,T=0 there is no strict tuple, so the universal endpoint statement is vacuous but all measurability claims are well-typed. No rank, nonzero-normal or rate restriction appears; actual93 supplies the totalized definitions and Borel behavior.'),
 dict(region='dependency and fragment boundary',finding='This is a concrete reusable adapter connecting actual93 path output and actualOrderedPrefix to the sealed endpoint and simplex inputs. It does not reclassify the remaining endpoint inverse/phase-volume/skew-product obligations as proved. ActualOrderedPrefix must be recorded as a real direct proof parent when integrated.')],
kernel=dict(kind='Source-bound focused run reused; no duplicate full-library build.',receipt=info(F/'receipt.json'),input_snapshot=info(F/'input.exactraw.lean'),exit_code=0,standard_axioms=['propext','Classical.choice','Quot.sound'],independent_duplicate_compile=False,warnings='Unused named proof binders in private Prop and an unnecessary-simpa style warning. These do not alter the theorem; original source hypotheses are intentionally retained.'),fake_closure_scan=scan,
remaining_truth_boundary='Only exact strict-simplex measurability, actual Gamma/endpoint joint Borel maps and deterministic final-arc identification are certified as this compiled fragment. The reversed finite-word identity, actual phase fibers, product Theta preservation, final sealed production theorem, semantic roundtrip/publication and complete SAU97 remain open.',source_fidelity_verdict=False,complete_SAU=False,VERIFIED_transition=False,production_edit=False,shared_edit=False)
write('endpoint-math-decision97.native.json',v)
for x in inputs:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
write('closed-RAW-endpoint97.native.json',dict(kind='closed-independent-fragment-review',reviewer='/root/exact_verifier96',self_excluded=True,fragment_raw_sha256=sha(raw),all_inputs_rehashed=True,files=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],complete_SAU=False,shared_edits=False,ledger_transitions=False))
for n in ['endpoint-math-decision97.native.json','closed-RAW-endpoint97.native.json']:print(json.dumps(info(O/n)),flush=True)
