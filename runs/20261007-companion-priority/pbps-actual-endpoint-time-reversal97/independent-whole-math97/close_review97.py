from pathlib import Path
import hashlib,json,re,subprocess,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
prep=load(O/'prepared-inputs97.native.json');rc=load(O/'fresh-kernel-receipt97.native.json')
assert rc['exit_code']==0 and rc['terminal_closed']
assert (O/'fresh-kernel.stderr.log').read_bytes()==b''
for row in prep['inputs']:
 p=R/row['path'];q=R/row['snapshot'];assert p.read_bytes()==q.read_bytes() and sha(p.read_bytes())==row['raw_sha256'],row['path']
prod=R/prep['production']['path'];text=prod.read_text(encoding='utf8')
clean=re.sub(r'/\-.*?\-/','',text,flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
for p in [r'\bsorry\b',r'\badmit\b',r'^\s*axiom\b',r'Prop\s*:=\s*True\b',r':=\s*trivial\b']:
 assert not re.search(p,clean,re.M),p
out=(O/'fresh-kernel.stdout.log').read_text(encoding='utf8')
axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",out,re.S)
assert len(axioms)==2
assert all(set(re.split(r',\s*',a.strip()))=={'propext','Classical.choice','Quot.sound'} for _,a in axioms)
assert 'error:' not in out and 'sorryAx' not in out
checks=[
 {'topic':'sealed public contract','verdict':'pass','reason':'The private statement from its first E binder through its complete Prop body is text-identical to the sealed Header97 candidate and expanded_literal_Prop, after excluding only a trailing documentation comment for the next theorem. A fresh source kernel witness applies the public theorem to the original candidate definition copied verbatim from Header97. Lean must unfold both definitions to establish this type match. All six analytic binders and structural typeclasses remain exactly those sealed; no endpoint provider, measurability, symmetry, rank, positive count or positive time binder was added.'},
 {'topic':'actual producers and terminal endpoint','verdict':'pass','reason':'endpoint_data is unchanged from the accepted endpoint fragment. ActualOrderedPrefix.actual_ordered_prefix_law supplies measurable Delta. ActualFiniteCountPath.actual_finite_count_path_law supplies joint Gamma measurability and its last-index interval clause; terminal evaluation is a Borel coordinate projection. At n=0 the last grid point is 0 and 0<=T; at n+1 the final strict upper bound gives last<=T. No later Fin index exists. This yields actual Gamma(T)=terminal Phi applied to actual zAt(last). The endpoint helper uses the identical Fin.induction recursion, so hAid is definitional transport of that actual terminal identity.'},
 {'topic':'rho exact measure','verdict':'pass','reason':'The ten simplex helpers are unchanged from independent simplex acceptance. rho is T-minus-Fin.rev on the strict simplex, measurable and involutive. Ambient tuple volume is preserved by constant-family coordinate permutation and scalar complements. Restriction invariance plus injectivity of map along the measurable subtype embedding establishes preservation of the exact Measure.comap subtype.val volume. No probability normalization or quotient/replacement measure is introduced.'},
 {'topic':'finite word and actual96 discharge','verdict':'pass','reason':'The ten word helpers are unchanged from independent word acceptance. hAP uses actual96 Phi and S volume laws and S involutivity. hAI consumes actual96 S/R involutivity, RS=SR, the Phi(u) after Phi(-u) inverse direction (.2 of hPhiI), and R-Phi-R time reversal. rho values are definitionally the reversed tuple required by endpoint_reversed. The C=S composed with R cancellation has the correct Phi-gap/S factor order, and the reversed endpoint conclusion is Rz, exactly the sealed endpoint identity.'},
 {'topic':'joint measurability and involution','verdict':'pass','reason':'hAm is actual joint terminal Gamma measurability over y,r,z,t. hThetaM composes it with the fixed measurable R and pairs with rho on the time coordinate; no merely pointwise-to-joint inference occurs. Theta squared has phase R(A(R(Az,t),rho t))=R(Rz)=z and time rho(rho t)=t.'},
 {'topic':'sigma finiteness and skew product','verdict':'pass','reason':'map_comap_subtype_coe identifies map(m, subtype.val) with ambient finite-dimensional tuple volume restricted to measurable Delta. This restricted measure is sigma-finite, and SigmaFinite.of_map transports that property back to the exact m using measurable subtype inclusion. Phase ell is the product of finite-dimensional Euclidean volumes, hence sigma-finite. Mathlib skew_product requires SFinite source measures, discharged by these sigma-finite instances. On time-first coordinates the base is rho and the fiber is z -> R(A z t), whose map equality is supplied for every t by hRP.comp hAP. Pre- and post-composition by measure-preserving swap restore precisely phase-first ell.prod m and Theta.'},
 {'topic':'degenerate cases','verdict':'pass','reason':'n=0 has a singleton empty tuple simplex and one terminal harmonic arc Phi(T); no bounce is introduced by the padded word because S squared is identity. T=0 with n>0 has empty strict simplex and zero subtype measure, covered by the same restriction and skew-product theorem (which permits zero base measure); n=0,T=0 gives identity endpoint and phase reversal Theta. Rank-zero E is allowed by all finite-dimensional volume APIs. At zero reflection normal the actual totalized S from96 is identity, so no nonzero-normal condition is needed.'}
]
route=[
 'Reuse the unchanged simplex, finite-word and actual-terminal fragment proofs, checking exact declaration equality.',
 'Produce measurable Delta and joint Gamma/terminal laws from actual OrderedPrefix and FiniteCountPath under the original six binders.',
 'Construct rho on the strict simplex and retain its exact comap-volume preservation.',
 'Identify actual Gamma(T) with the generic finite-word endpoint through the actual zAt recursion.',
 'Discharge all word symmetry and volume prerequisites with actual PhaseReversalVolume; obtain endpoint reversal and fiber preservation.',
 'Combine joint endpoint measurability, rho measurability and the endpoint identity to obtain joint Theta measurability and involutivity.',
 'Derive sigma-finiteness of exact m via subtype map/restriction, apply time-first skew-product preservation, and swap back to ell.prod m.'
]
decision=dict(kind='independent-whole-mathematical-assembly-review',reviewer='/root/exact_verifier96',decision='ACCEPT_EXACT_WHOLE_MATHEMATICAL_ASSEMBLY',production=prep['production'],header=prep['header'],statement_seal=prep['statement_seal'],checked_git_head_context=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),checked_target_basis='exact RAW working-tree production, not exact-commit SAU admission',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),kernel_receipt=info(O/'fresh-kernel-receipt97.native.json'),kernel_stdout=info(O/'fresh-kernel.stdout.log'),kernel_stderr=info(O/'fresh-kernel.stderr.log'),kernel_input=prep['kernel_input'],kernel_full_fresh_production_and_sealed_header_witness=True,public_private_Prop_expansion_kernel_checked=True,axiom_results=[dict(declaration=n,axioms=re.split(r',\s*',a.strip())) for n,a in axioms],false_closure_scan='PASS: no sorry/admit/custom axiom/Prop:=True/:=trivial in comment-stripped production; fresh public theorem and exact header witness have standard axioms only',fragment_reuse=prep['unchanged_reviewed_fragment_declarations'],checks=checks,legitimate_route_at_most_seven_steps=route,defects=[],required_mathematical_repairs=[],inputs=prep['inputs'],scope_boundary='Mathematical acceptance only. No independent primary-source or publication/exposition verdict is created here; no final SAU97 VERIFIED transition, exact-commit admission, or whole-paper result is claimed. Public metadata and semantic round-trip gates remain outside this review.',preparation_note='An initial local extraction assertion included the next theorem documentation comment. The parser was corrected to exclude that comment; production and sealed Header97 were unchanged. No Lean/kernel failure occurred in this audit.')
write('whole-math-decision97.native.json',decision)
for row in prep['inputs']:
 assert sha((R/row['path']).read_bytes())==row['raw_sha256']
files=sorted(p for p in O.rglob('*') if p.is_file())
write('closed-RAW-manifest97.native.json',dict(kind='closed-independent-whole-math-raw-manifest',hash_recipe='SHA256 of original file bytes, without text or newline normalization',excludes_self=True,decision=info(O/'whole-math-decision97.native.json'),files=[info(p) for p in files],preserved_original_inputs=prep['inputs']))
print(json.dumps(dict(decision=info(O/'whole-math-decision97.native.json'),manifest=info(O/'closed-RAW-manifest97.native.json'),receipt=info(O/'fresh-kernel-receipt97.native.json')),indent=2))
