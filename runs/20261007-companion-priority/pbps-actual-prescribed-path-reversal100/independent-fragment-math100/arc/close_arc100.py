from pathlib import Path
import hashlib, json, re, difflib
ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
BASE='runs/20261007-companion-priority/'
RUN=BASE+'pbps-actual-prescribed-path-reversal100/'
PRE=BASE+'pbps-finite-path-reversal-preread100/'
def raw(p):
 b=(ROOT/p).read_bytes()
 return dict(path=p,raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(name,x):
 p=OWN/name
 assert not p.exists()
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 return raw(p.relative_to(ROOT).as_posix())
fragment=raw(RUN+'ArcReversal100.lean')
assert fragment['raw_sha256']=='f41c9907b77abe7f17c7c94bd78bfe86176dcdc9effb379fd08d0ab27a59be5d'
seal=raw(PRE+'root.statement-seal100.json')
assert seal['raw_sha256']=='830f6b01d3d82168085e7e081a123c3152043090ebd7f0b91410e076cb96c108'
text=(ROOT/fragment['path']).read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit|axiom|sorryAx)\b|Prop\s*:=\s*True|:=\s*trivial',text)
kernel=load((OWN/'kernel-receipt100.native.json').relative_to(ROOT).as_posix())
assert kernel['exit_code']==0 and kernel['fragment_raw_sha256']==fragment['raw_sha256']
out=(OWN/'kernel.stdout.log').read_text(encoding='utf-8')
assert out.count('[propext, Classical.choice, Quot.sound]')==2 and 'sorryAx' not in out
old=(ROOT/(RUN+'focused100/arc1-closed-horizon/input.exactraw.lean')).read_text(encoding='utf-8')
diff=''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='retained arc1',tofile='reviewed arc2'))
save('trial-delta100.native.json',dict(kind='retained-first-trial-comparison',negative_trial=raw(RUN+'focused100/arc1-closed-horizon/receipt.json'),negative_snapshot=raw(RUN+'focused100/arc1-closed-horizon/input.exactraw.lean'),accepted_fragment=fragment,diff=diff,interpretation='Two elaboration corrections: implicit Fin.castSucc_lt_succ use and explicit involution rewrite via hRR. The first trial sorryAx arose from failed elaboration and is retained as negative evidence; it supplies no accepted proof evidence.'))
decision={
 'kind':'independent-mathematical-fragment-review100',
 'reviewer':'/root/exact_verifier96',
 'decision':'ACCEPT_GENERIC_ACTIVE_ARC_AND_OFF_EVENT_PATH_REVERSAL_FRAGMENT',
 'fragment':fragment,
 'declarations':['PBPSArcReversal100.active_arc','PBPSArcReversal100.path_reversal'],
 'scope':'Generic private-proof ingredients only. No public actual-path theorem, full SAU, source completion or VERIFIED credit.',
 'active_arc_audit':'The filter contains zero because a(0)=0<=s. Its greatest index j satisfies a(j)<=s. Any later k with a(k)<=s would belong to the same filter and contradict maximality. Monotonicity is unnecessary for this selection lemma.',
 'path_reversal_audit':[
  'Select the greatest active reverse index j. If j is last, s<=T=b(last) bounds the next endpoint. Otherwise maximality gives the strict next-start bound, using the castSucc/succ index identity.',
  'The complement equation for b(j.succ) converts the next-endpoint bound to a(j.rev.castSucc)<=T-s.',
  'For every k>j.rev, j=0 is impossible because j.rev is last. For j=i.succ, the off-event assumption excludes s=b(j.castSucc), turning the active lower bound into a strict inequality. Monotonicity of a and j.rev.succ<=k.castSucc then gives T-s<a(k.castSucc).',
  'The path laws identify g(s) and f(T-s) on the selected arcs. The same reflected j indexes the stated barPost identity; no second reversal map or arbitrary state replacement enters.',
  'R involutive and R(Phi_u(Rx))=Phi_-u(x) imply Phi_u(Rx)=R(Phi_-u(x)). Combining this with Phi_(u+v)=Phi_u composed with Phi_v yields the required operator order.',
  'The remaining real identity is -(s-b(j.castSucc)) + (a(j.rev.succ)-a(j.rev.castSucc)) = T-s-a(j.rev.castSucc), exactly by the left complement equation.'
 ],
 'endpoint_and_degenerate_audit':{
  'endpoints':'The proof covers the entire closed interval whenever the stated off-event condition holds; no step assumes s is strictly between zero and T. In the actual strict-simplex discharge all event times lie strictly inside, so both endpoints satisfy that condition.',
  'n_zero':'Fin(n+1) has one arc; later-index requirements and event exclusion are vacuous. Complement equations recover the endpoint bounds, and the same flow algebra applies.',
  'T_zero':'For actual inputs with n=0 the argument covers the single point. With positive n, strict Prefix is empty. The generic lemma itself handles any supplied arrays and laws satisfying its premises.',
  'negative_T':'No unspoken T>=0 premise: the generic conclusion has no s satisfying 0<=s<=T when T<0; actual T is NNReal.',
  'rank_norm_rate':'X is arbitrary. No dimension, nonzero-normal, positive-rate or division hypothesis occurs. Those zero cases are not removed.',
  'non_strict_grids':'Monotone a is sufficient; repeated grid values do not invalidate maximum selection. Event coincidences are excluded where necessary by the explicit hne premise.'
 },
 'actual_discharge_obligations':[
  'a and b must be the literal original/reversed Fin.cons/Fin.snoc grids, with monotone a derived from the strict simplex, and b endpoints by reduction.',
  'hbl and hbr must be derived from the actual99 rho coordinate projection sharing its witness with the state-pair projection; no private99 helper call or independent provider premise.',
  'Phi and R must be the literal actual definitions; actual harmonic flow supplies hgroup and actual96 supplies hR/hrev.',
  'post and barPost must be literal zAt arrays. The first actual99 state-pair projection supplies hstate.',
  'f and g must be the two clamped actual Gamma paths. Actual93 live-arc identification plus the clamp identity on Icc must supply hf/hg. Their generic appearance in this helper is not authorization to export arbitrary-path or path-law hypotheses.',
  'The final theorem must independently discharge interval integrability and time-substitution equality; this fragment establishes neither.'
 ],
 'kernel':{'fresh_independent_exact_prefix_compile':'PASS','axioms_both_declarations':['propext','Classical.choice','Quot.sound'],'fake_closure_scan':'PASS exact fragment lexical scan','warning':'Only unnecessarySimpa linter warning at j=0 impossible branch'},
 'source_alignment':'Matches the accepted base-plus-overlay100 off-event Icc scope. Right-continuous jump points remain explicitly excluded; no all-time reversal assertion is introduced.',
 'defects_found':[],
 'no_shared_edits':True,'no_VERIFIED_transition':True,'no_public_provider_hypothesis_approved':True
}
save('arc-math-decision100.native.json',decision)
paths=[fragment['path'],PRE+'Header100.lean',seal['path'],PRE+'independent-header-math100/header-math-decision100.native.json',PRE+'independent-header-math100/topology-overlay100/source-topology-admission100.native.json',PRE+'independent-header-math100/topology-overlay100/closed-RAW-topology-admission100.native.json']
for trial in ['arc1-closed-horizon','arc2-explicit-involution']:
 for name in ['receipt.json','input.exactraw.lean','stdout.log','stderr.log']:
  paths.append(RUN+'focused100/'+trial+'/'+name)
files=[raw(p.relative_to(ROOT).as_posix()) for p in sorted(OWN.iterdir()) if p.is_file()]
manifest=save('closed-RAW-arc100.native.json',dict(kind='closed-independent-fragment-review100',inputs=[raw(p) for p in paths],files=files,closed=True,hash_algorithm='SHA256 exact raw bytes',self_hash_intentionally_omitted=True))
print(json.dumps({'decision':raw((OWN/'arc-math-decision100.native.json').relative_to(ROOT).as_posix()),'manifest':manifest},indent=2))
