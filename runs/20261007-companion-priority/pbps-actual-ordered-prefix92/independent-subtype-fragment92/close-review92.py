import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-subtype-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
source=B/'SubtypeCoordinates92.lean';assert bind(source)['raw_sha256']=='c4e7dc7915012fdb81228bb5c4cad6eeca533d977a5192e9d9a72e80d680037a'
s=source.read_text(encoding='utf-8');old=(B/'Coordinates92.lean').read_text(encoding='utf-8')
assert old[old.index('private theorem strictMono_snoc'):old.index('\nend\n')].strip()==s[s.index('private theorem strictMono_snoc'):s.index('private def snocPrefix')].strip()
clean=re.sub(r'/\-[\s\S]*?\-/','',s);assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=read(D/'kernel.receipt.json');assert receipt['exit_code']==0
log=(D/'kernel.stdout.log').read_text();assert ': error' not in log and 'depends on axioms: [propext,\n Classical.choice,\n Quot.sound]' in log
paths=[source,B/'Coordinates92.lean',B/'root.statement-seal92.json',B/'focused/subtype1-comap-tonelli/receipt.json',B/'independent-coordinate-fragments92/coordinate-fragment-review92.native.json',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Embedding.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_PRIVATE_SUBTYPE_SIMPLEX_INTEGRAL_ADAPTER',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,'source':bind(source),
 'retained_coordinate_body_exact_after_newline_normalization':True,
 'closed_boundary':'The previously open generic adapter from arbitrary measurable ENNReal simplex-subtype tests to the nested simplex/interval-subtype comap integrals is now proved. This is deterministic Lebesgue-coordinate transport, not an actual-clock probability density law.',
 'domain_audit':[
  'F has exactly the enlarged simplex subtype Delta(n+1,T) as its domain, not the ambient real vector space.',
  'The outer RHS variable has subtype Delta(n,T). The inner variable has the dependent subtype Ioo(last(cons0t),T).',
  'snocPrefix constructs the ambient vector Fin.snoc(t.val,u.val) with its enlarged simplex proof from simplex_snoc applied to t.property and u.property.',
  'LHS measure is comap of real finite-product volume along the enlarged simplex inclusion; outer RHS is the same comap on the old simplex; inner RHS is comap of real Lebesgue volume along the interval inclusion. These are the intended dimensions and domains.',
  'No subtype is replaced by Set.univ. The same original strict inequalities and ambient-to-subtype coercions survive all conversions.'
 ],
 'proof_audit':[
  {'step':'measurable extension','finding':'MeasurableEmbedding.subtype_coe hs and exists_measurable_extend provide measurable ambient G with G composed with subtype inclusion exactly F. The required Nonempty ENNReal is supplied by its ordinary instance, including when the source simplex is empty; no assumption about F values, integrability or density enters.'},
  {'step':'pointwise equality on support','finding':'congrFun hext yields G(t.val)=F(t) at every enlarged-simplex point. The first lintegral_congr replaces F by G composed with inclusion without an exceptional null set.'},
  {'step':'LHS comap conversion','finding':'lintegral_subtype_comap hs G changes the enlarged-subtype integral to the ambient integral restricted to Delta(n+1,T). This Mathlib theorem is valid for arbitrary nonnegative integrands; hG then supplies the measurability required by the coordinate Tonelli lemma.'},
  {'step':'ambient Tonelli','finding':'The retained simplex_lintegral_snoc performs measure-preserving snoc transport and nonnegative product integration. The old time vector is outer and the last absolute event time lies in its exact strict interval.'},
  {'step':'outer and inner subtype conversion','finding':'lintegral_subtype_comap hn converts the old-simplex outer restriction; for each old t, lintegral_subtype_comap measurableSet_Ioo converts the real interval restriction. The inner domain and its comap measure remain dependent on that fixed old t.'},
  {'step':'return to original F','finding':'For every t and u in those subtypes, snocPrefix is an enlarged-simplex point, so he(snocPrefix t u) replaces G(snoc(t,u)) by F(snocPrefix t u) pointwise. Arbitrary extension values outside the enlarged simplex cannot contribute.'}
 ],
 'edge_cases':[
  'n0: Delta0 is the singleton empty-vector subtype with empty-product mass1. last(cons0t)=0, so the interval is exactly (0,T). No positive n premise is used.',
  'T0,n0: Delta1(0) and the inner interval(0,0) are empty. The left integral and all inner integrals are0 even if the ambient extension has infinite values elsewhere.',
  'T0,n>0: the old and enlarged simplex subtypes are empty; both integrals are0. The measurable extension exists because ENNReal is nonempty; it does not require a point of either simplex.',
  'Infinite-valued F is allowed throughout. All operations are nonnegative lintegrals, with no subtraction or finiteness/Fubini premise.',
  'Strict endpoints remain excluded on both sides. There is no no-atom assumption or replacement by closed/half-open intervals.'
 ],
 'private_binder_boundary':'hn and hs are measurable-set ingredients produced for the literal Delta by Geometry92 at n and n+1. They are legitimate private premises and must be instantiated internally; no permission is given to add them as source-facing public binders. hF is ordinary test measurability, as in the sealed conclusion.',
 'kernel':{'receipt':bind(D/'kernel.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'snocPrefix_and_integral_types_inspected':True,'axioms':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'findings_requiring_changes':[],
 'remaining_open':'Apply this generic subtype integral adapter to the concrete history test times density; instantiate actual record/step/factor and event decomposition; complete the actual all-n probability density induction and final measure/test/mass conclusions. No full SAU or VERIFIED credit.',
 'canonical_or_production_mutation':False
}
decision=put('subtype-fragment-review92.native.json',report)
put('subtype-fragment-review92.md','''# Independent subtype-integral fragment review92

Accepted snocPrefix and subtype_simplex_lintegral_snoc in the frozen SubtypeCoordinates92.lean. The previously reviewed coordinate body is retained exactly. Fresh pinned Lean type/axiom checking passed (exit0,9.234s), with only propext, Classical.choice and Quot.sound.

The arbitrary measurable ENNReal test remains defined on the enlarged simplex subtype. Its measurable ambient extension agrees pointwise there, and the proof uses that extension only under the relevant restricted/comap measures. Every nested snocPrefix point lies in the enlarged simplex, so values outside it do not influence the result. Outer and inner subtype domains and volume dimensions are correct, including n0, T0, empty simplexes and infinite-valued tests.

This closes the generic subtype coordinate-integral adapter identified in the prior review. The private measurable-set premises must be supplied by Geometry. Concrete density/test instantiation and the actual all-n probability law remain open. No canonical or production file was changed.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('subtype-review-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned subtype-fragment review and fresh check files only. Original inputs unchanged; manifest excludes itself. No canonical or full-SA U acceptance.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
