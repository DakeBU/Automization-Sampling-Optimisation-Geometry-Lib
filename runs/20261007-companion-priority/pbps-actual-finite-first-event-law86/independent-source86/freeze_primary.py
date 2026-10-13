from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, re

OUT = Path(__file__).resolve().parent
ROOT = Path('E:/Samplinglib')
SOURCE = ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
RAW = SOURCE.read_bytes()
assert hashlib.sha256(RAW).hexdigest() == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
HTML = RAW.decode('utf-8')
VOID = {'meta','link','img','br','hr','input','source','wbr','area','base','embed','param','col'}

class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    def text(self):
        if self.tag == 'math' and self.attrs.get('alttext'):
            return self.attrs['alttext']
        return ''.join(c if isinstance(c,str) else c.text() for c in self.children)
    def within(self, other):
        p=self
        while p:
            if p is other:return True
            p=p.parent
        return False

class Parse(HTMLParser):
    def __init__(self):
        super().__init__();self.root=Node('root',{});self.stack=[self.root];self.ids={}
    def handle_starttag(self,t,a):
        n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n)
        if n.attrs.get('id'):self.ids[n.attrs['id']]=n
        if t not in VOID:self.stack.append(n)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t:self.stack=self.stack[:i];break
    def handle_data(self,d):self.stack[-1].children.append(d)

P=Parse();P.feed(HTML);SECTION=P.ids['A1.SS1']
start=HTML.index('<section id="A1.SS1"');end=HTML.index('<section id="A1.SS2"',start)
(OUT/'primary-A1.SS1-raw.private.html').write_text(HTML[start:end],encoding='utf-8')

# Every mathematical paragraph and display receives a disposition. Structural
# wrappers and repeated MathML children inherit their enclosing item.
groups = [
 ('fixed-rate', ['A1.SS1.p1.1','A1.Ex1'], 'Fixed y and reference; actual residual-gradient rate'),
 ('flow-bounce', ['A1.SS1.p1.2','A1.Ex2','A1.Ex3'], 'Explicit harmonic flow and actual reflection, R_0=I'),
 ('zero-normal', ['A1.SS1.p1.3'], 'Involution; vanishing rate removes zero-normal event ambiguity'),
 ('clock-recursion', ['A1.SS1.p2.1','A1.E1','A1.E2'], 'Independent Exp(1) threshold, integrated hazard, recursion and post-jump state'),
 ('infinite-wait', ['A1.SS1.p2.2'], 'Empty threshold set means infinity and stopped recursion; between-event flow'),
 ('energy', ['A1.SS1.p3.1','A1.Ex4'], 'Shifted harmonic energy'),
 ('energy-conservation', ['A1.SS1.p3.2','A1.Ex5'], 'Flow/bounce energy conservation and phase-space bounds'),
 ('rate-bound', ['A1.SS1.p3.3','A1.Ex6'], 'Lipschitz residual-gradient bound and energy-local rate cap'),
 ('hazard-bound', ['A1.SS1.p3.4','A1.Ex7'], 'Rate cap integrated on the arc'),
 ('wait-lower-bound', ['A1.SS1.p3.5','A1.Ex8'], 'Zero-cap no-jump case; otherwise finite wait at least clock/cap'),
 ('clock-sum', ['A1.SS1.p3.6','A1.Ex9'], 'Jump time lower bound by sum of consumed exponential clocks'),
 ('wellposed-markov', ['A1.SS1.p3.7'], 'SLLN, nonaccumulation, all-time uniqueness, exponential memoryless Markov property and Davis Section 2 citation'),
 ('momentum-reversal', ['A1.SS1.p4.1','A1.Ex10'], 'State reversal and pullback'),
 ('phase-density', ['A1.SS1.p4.2','A1.Ex11'], 'Conditional target times Gaussian momentum density'),
 ('operator-theorem', ['A1.Thmtheorem1.p1.1','A1.E3','A1.Thmtheorem1.p1.2','A1.I1.i1.p1.1','A1.I1.i2.p1.1','A1.I1.i3.p1.1'], 'Adjoint reversal, invariance, strong continuity/contraction and averaged self-adjoint Markov contraction'),
 ('heuristic-generator', ['A1.SS1.SSS0.Px1.p1.1','A1.Ex12','A1.Ex13'], 'Heuristic drift and jump operator decomposition'),
 ('heuristic-log-density', ['A1.SS1.SSS0.Px1.p1.2','A1.Ex14'], 'Reversal of flow and derivative of log density'),
 ('heuristic-adjoint-drift', ['A1.SS1.SSS0.Px1.p1.3','A1.Ex15'], 'Formal integration by parts'),
 ('heuristic-adjoint-jump', ['A1.SS1.SSS0.Px1.p1.4','A1.Ex16'], 'Formal reflection change of variables'),
 ('heuristic-adjoint-sum', ['A1.SS1.SSS0.Px1.p1.5','A1.Ex17'], 'Formal generator adjoint identity'),
 ('heuristic-exponentiation', ['A1.SS1.SSS0.Px1.p1.6'], 'Formal exponentiation and Gaussian averaging'),
 ('heuristic-limit', ['A1.SS1.SSS0.Px1.p2.1'], 'Explicit warning: discontinuous bounce prevents directly treating formal calculation as rigorous'),
 ('arc-density-identity', ['A1.SS1.SSS0.Px1.p3.1','A1.E4'], 'Log-density derivative along exact harmonic arc'),
 ('reverse-flow', ['A1.SS1.SSS0.Px1.p3.2','A1.Ex18'], 'Reverse harmonic flow and commuting bounce/reversal'),
 ('jump-rate-match', ['A1.SS1.SSS0.Px1.p3.3','A1.E5'], 'Positive nontrivial jump matches reversed rate'),
 ('bounce-measure', ['A1.SS1.SSS0.Px1.p3.4','A1.E6'], 'Flow/reversal Lebesgue preservation; bounce Fubini plus orthogonality'),
 ('simplex', ['A1.SS1.SSS0.Px1.p4.1','A1.Ex19'], 'Ordered strictly interior n-event times'),
 ('full-path-law', ['A1.SS1.SSS0.Px1.p4.2','A1.E7'], 'Prescribed-time paths and iterated exponential-clock expansion for bounded measurable path functionals'),
 ('series-reversal', ['A1.SS1.SSS0.Px1.p4.3','A1.E8'], 'Simplex-volume absolute convergence and reversal of path/time vector'),
 ('borel-change', ['A1.SS1.SSS0.Px1.p4.4'], 'Finite composition of Borel preserving bijections; inverse via reversal and time determinant one'),
 ('survival-density-match', ['A1.SS1.SSS0.Px1.p5.1','A1.Ex20'], 'Integrate arc density identity and reflection density preservation'),
 ('termwise-duality', ['A1.SS1.SSS0.Px1.p5.2','A1.Ex21'], 'Match rate factors; Tonelli for nonnegative terms, signed decomposition, bounded-observable duality'),
 ('invariance-extension', ['A1.SS1.SSS0.Px1.p5.3'], 'Set first observable to one and extend adjoint identity by L2 density'),
 ('contractivity-continuity', ['A1.SS1.SSS0.Px1.p6.1','A1.Ex22'], 'Jensen contraction, deterministic continuity and first-event survival limit on compactly supported observables'),
 ('dense-extension', ['A1.SS1.SSS0.Px1.p6.2'], 'Dominated convergence and dense-subspace extension'),
 ('gaussian-average', ['A1.SS1.SSS0.Px1.p7.1','A1.Ex23'], 'Momentum-average reversal cancellation and self-adjointness'),
 ('average-properties', ['A1.SS1.SSS0.Px1.p7.2'], 'Averaged Markov/contraction properties'),
]
inventory=[];seen=set()
for name,ids,desc in groups:
    for anchor in ids:
        assert anchor in P.ids,anchor
        seen.add(anchor)
        inventory.append({'anchor':anchor,'disposition':'NODE','node':'primary:'+name,'kind':'substantive-proof-paragraph' if P.ids[anchor].tag=='p' else 'reused-display','paraphrase':desc})
atomic=[k for k,n in P.ids.items() if n.within(SECTION) and (n.tag=='p' or ('ltx_equation' in n.attrs.get('class','').split() and n.tag in ['table','tbody']))]
missing=[k for k in atomic if k not in seen]
assert not missing,missing
private_nodes={k: {'tag':P.ids[k].tag,'text':P.ids[k].text()} for k in seen}
(OUT/'primary-atomic-items.private.json').write_text(json.dumps(private_nodes,ensure_ascii=False,indent=2),encoding='utf-8')

edges=[
 ('flow-bounce','energy-conservation','Actual harmonic and reflection norm identities'),
 ('energy','energy-conservation','Initial energy controls each later state'),
 ('energy-conservation','rate-bound','State bounds inserted into residual gradient estimate'),
 ('fixed-rate','rate-bound','Beta-Lipschitz gradient plus Cauchy-Schwarz'),
 ('rate-bound','hazard-bound','Integrate along each deterministic arc'),
 ('hazard-bound','wait-lower-bound','Combine threshold definition, continuity and positive exponential clock'),
 ('clock-recursion','wait-lower-bound','Integrated hazard threshold'),
 ('wait-lower-bound','clock-sum','Sum finite waits'),
 ('clock-sum','wellposed-markov','SLLN and no finite accumulation'),
 ('infinite-wait','wellposed-markov','Terminated recursion remains deterministic forever'),
 ('clock-recursion','wellposed-markov','Unused independent clocks and exponential memoryless property'),
 ('phase-density','arc-density-identity','Differentiate density along the flow'),
 ('flow-bounce','reverse-flow','Exact flow and reflection formulas'),
 ('zero-normal','jump-rate-match','Positive rate implies nonzero residual normal'),
 ('flow-bounce','jump-rate-match','Reflection reverses normal momentum'),
 ('flow-bounce','bounce-measure','Pointwise orthogonality, Fubini, Borel measurability'),
 ('clock-recursion','full-path-law','First-event law iterated using conditionally unused independent clock tail'),
 ('infinite-wait','full-path-law','Survival branch includes infinite next waiting times'),
 ('wellposed-markov','full-path-law','No omitted finite-horizon infinite-event trajectories'),
 ('simplex','full-path-law','Ordered event-time integration domain'),
 ('rate-bound','series-reversal','Energy-local rate bound on every prescribed path'),
 ('full-path-law','series-reversal','Bounded functional and n-event density product'),
 ('bounce-measure','borel-change','Each endpoint factor preserves Lebesgue measure'),
 ('reverse-flow','borel-change','Construct reversed inverse'),
 ('arc-density-identity','survival-density-match','Integrate over deterministic arcs'),
 ('flow-bounce','survival-density-match','Bounce preserves phase density'),
 ('survival-density-match','termwise-duality','Initial density times survival matches reversed factors'),
 ('jump-rate-match','termwise-duality','Each jump factor matches'),
 ('borel-change','termwise-duality','Legitimate full-space and simplex change of variables'),
 ('full-path-law','termwise-duality','All n-event terms represented'),
 ('termwise-duality','invariance-extension','Bounded-observable adjoint equality; take F=1'),
 ('invariance-extension','contractivity-continuity','Invariance plus Jensen'),
 ('clock-recursion','contractivity-continuity','First-event survival tends to one'),
 ('contractivity-continuity','dense-extension','Bounded compactly supported functions, dominated convergence'),
 ('dense-extension','operator-theorem','L2 density and contractivity'),
 ('invariance-extension','gaussian-average','Adjoint reversal plus momentum-average identities'),
 ('gaussian-average','average-properties','Composition of Markov contractions'),
 ('average-properties','operator-theorem','Final averaged operator conclusion'),
]

boundary={
 'source_id':'arXiv:2609.06905v1',
 'source_raw_sha256':hashlib.sha256(RAW).hexdigest(),
 'scope':'First actual-clock finite-density and marked-law boundary extracted from A1.E1/A1.E2 and the unnamed clock iteration at A1.E7, with exhaustive surrounding A1.SS1 topology',
 'source_standing_hypotheses':[
  'Potential on Euclidean R^d; source global Hessian contract alpha I <= Hess V <= beta I (S1.E1); fixed positive eta in the proximal-scale setting eta <= 1/beta (Section 2.2).',
  'Fixed arbitrary y, reference x_tilde, and initial phase state zeta=(x,p); reference need not be a random conditional draw for this fixed-reference first-event statement.',
  'Independent Exp(1) clocks for recursive process. For the first deterministic state only one unit exponential law is needed.',
  'Actual harmonic center c=y-eta grad V(x_tilde), residual h(x)=grad V(x)-grad V(x_tilde), and rate lambda=sqrt(eta)*max(<p,h(x)>,0).',
  'Actual reflection R_h=I-2hh^T/||h||^2 when h!=0, R_0=I; position is unchanged by the bounce.'
 ],
 'proof_ingredients_not_new_source_binders':[
  'Continuity, nonnegativity and local integrability of the actual arc rate q(t)=lambda(Phi_t zeta).',
  'A(t)=integral_0^t q(s)ds is continuous, differentiable where needed, nondecreasing, and zero at zero.',
  'Actual flow measurability/continuity, actual reflection Borel measurability, cumulative-hazard generalized-inverse measurability, and threshold crossing facts.',
  'Derivative of exponential survival; finite-measure uniqueness or generalized-inverse pushforward substitution; mark-map pushforward.',
  'Energy conservation and finite pathwise rate cap are derived facts, not assumptions to be promoted to public source binders.',
  'Recursive conditional independence, terminal survival, nonexplosion and all-event-time density iteration are additional ingredients for A7, not conclusions of a first finite event theorem.'
 ],
 'first_clock_reconstruction':{
  'definitions':'q(t)=lambda(Phi_t zeta); A(t)=integral_0^t q(s) ds; S=inf{u>=0:A(u)>=E}, with S=infinity when the set is empty; E~Exp(1).',
  'survival':'For finite t>=0, P(S>t)=exp(-A(t)). Equal-threshold issues at E=0 or limiting cumulative hazard are null events handled explicitly; deterministic e=0 may yield S=0.',
  'finite_density':'The positive finite part has measure P(S in B, 0<S<infinity)=integral_(B intersect (0,infinity)) q(t)*exp(-A(t)) dt for Borel B. It is generally a subprobability measure.',
  'infinite_mass':'P(S=infinity)=exp(-lim_(t->infinity) A(t)), with exp(-infinity)=0. Neither finite event nor strictly positive rate at every t is a source assumption.',
  'marks':'On the positive finite branch the mark is (S, Phi_S zeta, actualBounce(Phi_S zeta)); its measure is the pushforward of q(t)exp(-A(t))dt by the deterministic actual mark map.',
  'default_zero':'A total real-valued finite-clock representative may assign 0 to an infinite or nonpositive branch only as an implementation encoding whose theorems restrict to positive times/finite branch. It is not the source waiting-time semantics and never creates an actual t=0 event.',
  'zero_normal':'The actual bounce is defined for zero normal by identity. Nonzero-normal assumptions cannot replace that global definition. Zero-rate times carry zero finite-event-density mass.',
  'source_status':'These are source-faithful local consequences of A1.E1/A1.E2 and the implicit iteration invoked at A1.E7, not separately numbered claims explicitly printed by the authors.'
 },
 'alternative_density_routes':{
  'logic':'OR between sufficient routes; common actual-clock definitions and measurability form shared parents. Do not require both derivations as a false AND.',
  'route_cdf':'Threshold equivalence + exponential survival AND FTC/derivative of exp(-A) AND Borel finite-measure uniqueness imply finite density.',
  'route_pushforward':'Exponential-clock density AND monotone cumulative-hazard generalized inverse with correct plateaus/finite branch AND pushforward/substitution identity imply finite density.',
  'source_provenance':'Paper specifies integrated hazard construction and iterates it; it does not explicitly prescribe either expanded density proof. These routes are reviewer reconstructions of omitted bookkeeping.'
 },
 'A7_forward_OPEN':[
  'Conditional unused-tail law: after each consumed clock and reached state, remaining Exp(1) clocks retain their product law conditional on generated history; deterministic-state first-event law alone does not establish this.',
  'Iterate conditional marked transition laws through arbitrary n, with measurable state-dependent kernels and strict ordered-time simplex bookkeeping.',
  'Include final no-event survival through the horizon, including infinite next wait; boundary event times at 0 and t have zero mass but need proof/handling.',
  'All finite-horizon paths are represented by a finite event count using source nonexplosion; sum of exact-count laws equals the entire path law.',
  'Path-functional measurability, prescribed-time path construction and terminal survival factor; zero-event term uses empty product and deterministic path.',
  'Absolute convergence pointwise in initial state from energy-local cap and simplex volume; do not silently infer integrability of exp(cap*t) under the phase law. Probability normalization and Tonelli supply the appropriate integrated control.',
  'Complete path reversal still requires A4, A5, A6, full A7, Borel endpoint/time change, survival-density matching, and termwise integration; first marked law does not establish stationarity or operator results.'
 ],
 'full_topology':{'nodes':[{'id':'primary:'+n,'description':d,'anchors':a} for n,a,d in groups], 'edges':[{'parent':'primary:'+a,'consumer':'primary:'+b,'consumer_use':c,'logic':'AND within this pathwise route'} for a,b,c in edges], 'heuristic_branch':'Formal generator argument is explicitly heuristic; it is not a complete alternative proof of A3 without the missing analytic domain hypotheses. Rigorous source route is pathwise.'},
 'inventory':inventory,
 'inventory_accounting':{'atomic_paragraphs_and_displays':len(atomic),'accounted':len(set(atomic)&seen),'missing':missing,'structural_exclusions':'HTML wrappers, headings, equationgroup tables, MathML/annotation duplicate children and proof-end glyph are subordinate to the inventoried paragraph/display; no independent substantive mathematical item excluded.'},
 'external_inputs':[{'anchor':'A1.SS1.p3.7','input':'Strong law for iid unit exponential clocks; exponential memorylessness; Davis [12, Section 2] integrated-hazard construction','status':'Source cited/used, not local Lean truth inferred here'},{'anchor':'A1.SS1.SSS0.Px1.p3.4','input':'Fubini and orthogonality','status':'Source proof ingredient'},{'anchor':'A1.SS1.SSS0.Px1.p5.2','input':'Tonelli and signed decomposition','status':'Source proof ingredient'},{'anchor':'A1.SS1.SSS0.Px1.p6.1','input':'Jensen, dominated convergence and C_c density in L2','status':'Source proof ingredient'}],
 'review_status':'SOURCE_FIRST_FROZEN; canonical anti-anchored packet unseen; no implementation verdict, repair proposal, formal verification, ledger transition or completion claim',
 'independence':'Independent primary-source reviewer; not formalizer, decoder, mathematical verifier or repair proposer. No prior reviews/registry/decision/manifest/native decoder/adoption files read.',
 'license':{'primary':'arXiv.org perpetual non-exclusive license','public_policy':'Hashes, identifiers, faithful paraphrases and mathematical formulas only; exact long extracts restricted to private evidence files','exclude_from_public':['primary-A1.SS1-extraction.private.json','primary-standing-source-context.private.json','primary-A1.SS1-raw.private.html','primary-atomic-items.private.json']},
 'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
(OUT/'primary-first-freeze.json').write_text(json.dumps(boundary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
chronology={
 'events':[
  {'order':1,'action':'Read .agents/skills/astis-semantic-roundtrip/SKILL.md, then docs/proof-digestion-protocol.md'},
  {'order':2,'action':'Read pinned primary bytes; verify RAW hash; inspect anchor positions; diagnose GBK print failure'},
  {'order':3,'action':'Read full A1.SS1 source text, inventory and topology from primary only; save long source extracts privately'},
  {'order':4,'action':'Read primary S2/S3 standing context and S1.E1 plus primary license label'},
  {'order':5,'action':'Freeze source-only first-clock boundary and exhaustive A1.SS1 graph before all implementation/decoder/packet access'},
 ],
 'last_utc':boundary['frozen_utc'],
 'canonical_reviewer_packet_seen':False,
 'implementation_seen':False,
 'decoder_outputs_seen':False,
 'earlier_verdicts_seen':False,
}
(OUT/'primary-first-chronology.json').write_text(json.dumps(chronology,indent=2)+'\n',encoding='utf-8')
outputs=[]
for f in sorted(OUT.iterdir()):
 if f.is_file() and f.name!='primary-first-RAW-manifest.json':
  b=f.read_bytes();outputs.append({'path':str(f.relative_to(ROOT)),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'public_excluded':'.private.' in f.name})
manifest={'utc':boundary['frozen_utc'],'inputs':[{'path':str(f.relative_to(ROOT)),'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in [ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md',ROOT/'docs/proof-digestion-protocol.md',SOURCE]],'outputs':outputs,'diagnostics':['Initial anchor probe exited 1 only because terminal GBK could not encode U+220E; RAW primary hash had already matched. Later commands explicitly set PYTHONIOENCODING=utf-8.','All source atom coverage assertions passed; no network access or package installation.']}
(OUT/'primary-first-RAW-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'freeze':str(OUT/'primary-first-freeze.json'),'sha256':hashlib.sha256((OUT/'primary-first-freeze.json').read_bytes()).hexdigest(),'inventory':boundary['inventory_accounting'],'manifest_sha256':hashlib.sha256((OUT/'primary-first-RAW-manifest.json').read_bytes()).hexdigest()},indent=2))
