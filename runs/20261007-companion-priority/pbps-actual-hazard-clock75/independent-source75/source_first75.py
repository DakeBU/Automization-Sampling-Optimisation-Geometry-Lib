import collections, hashlib, json, os, sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path('E:/Samplinglib')
OWN = ROOT / 'runs/20261007-companion-priority/pbps-actual-hazard-clock75/independent-source75'
BASE = ROOT / 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75'
PRIMARY = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def ref(p):
    b = p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n', b'\n').replace(b'\r', b'\n'))}

class TextMath(HTMLParser):
    def __init__(self): super().__init__(); self.out=[]; self.math=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='math': self.out.append('$'+a.get('alttext','')+'$'); self.math+=1
        if tag in ('p','tr','li','figcaption','h3','h4'): self.out.append('\n')
    def handle_endtag(self,tag):
        if tag=='math': self.math-=1
    def handle_data(self,d):
        if not self.math:self.out.append(d)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    assert not (OWN/'lease.final.json').exists(), 'closed output directory'
    raw=PRIMARY.read_bytes()
    assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
    files=['stageA.freeze75.json','source-proof-graph75.json','source-coverage-inventory75.json','exact-source-formulas75.json']
    freeze,graph,inv,form=[json.loads((BASE/f).read_text(encoding='utf-8')) for f in files]
    fixed={x['path']:x for x in freeze['core_artifacts']}
    for f in files[1:]:
        r=ref(BASE/f); assert r['RAW_sha256']==fixed[r['path']]['RAW_sha256']
    assert len(graph['nodes'])==32 and len(graph['edges'])==67
    assert len(inv['items'])==137 and collections.Counter(x['classification'] for x in inv['items'])=={'NODE':77,'EXCLUDED':60}
    assert sum(n['kind']=='ASTIS_INTERNAL_BRIDGE' for n in graph['nodes'])==13
    for item in inv['items']:
        a,b=item['RAW_range']; data=raw[a:b]
        assert sha(data)==item['RAW_sha256'] and len(data)==item['RAW_bytes'],item['item_id']
        assert item['classification'] in ('NODE','EXCLUDED') and item['reason']
        assert all(n in {x['id'] for x in graph['nodes']} for n in item['nodes'])
    for item in form['source_formulas']:
        a,b=item['RAW_range']; assert sha(raw[a:b])==item['RAW_sha256']
    for n in graph['nodes']:
        for a in n['source_anchors']:
            start,end=a['RAW_range']; assert sha(raw[start:end])==a['RAW_sha256']
    for r in inv['regions']:
        a,b=r['RAW_range']; assert sha(raw[a:b])==r['RAW']['RAW_sha256']
    expectations={
      'scope':'One fixed-reference, fixed-start actual PBPS harmonic-flow segment and its first integrated-hazard clock only.',
      'source_assumptions':'Finite real Hilbert/Borel realization of R^d, including rank zero; V C2; 0<alpha<=beta; Hessian quadratic bounds; eta>0 and beta*eta<=1. These are the source standing hypotheses, not separately supplied rate/flow estimates.',
      'literal_formula':'c=y-eta gradV(xRef), h=gradV(x)-gradV(xRef), q(s)=sqrt(eta) max(0,<P_s,h(X_s)>), Lambda(t)=integral_0^t q(s) ds, tau(e)=inf{u>=0:Lambda(u)>=e}, with empty set infinity.',
      'closed_inf':'Time is continuous and nonnegative; closed threshold crossing must attain its nonempty infimum. IVT/continuity must justify equality at finite crossing; no discrete-time stopping API.',
      'threshold_and_infinity':'e>=0 including e=0; tau(0)=0; e>0 implies tau>0 possibly infinity; tau=inf empty=top; tau<=t iff e<=Lambda(t).',
      'measurability':'Joint Borel first-clock map from parameters/start/threshold; no assertion of continuity of the clock or bounce.',
      'actual_probability':'Use actual normalized Exp(1) pushforward; strict survival P(tau>t)=exp(-Lambda(t)), with infinity included in event. No caller-provided survival/support/zero-atom theorem.',
      'cap':'Use C=sqrt(eta) beta sqrt(2H(z))(sqrt(2eta H(z))+norm(c-xRef)); H is actual weighted SUM energy. Establish original-energy cap along flow and Lambda(t)<=Ct internally.',
      'lower_wait':'For C>0, tau>=e/C in extended nonnegative order; for C=0, positive threshold gives infinity while e=0 gives zero.',
      'rank0_H0':'These remain legal specializations of general statements; do not invent a new theorem claim or a positive-dimension/energy/nonzero-normal restriction.',
      'outside_scope':['recursive postbounce paths','global path energy propagation','iid sequence/SLLN/nonexplosion','Markov memorylessness','reversal/invariance/semigroup','terminal kernel','hypocoercivity/main','errors/caps','expected-query costs','actual-input composition','full exposition','PURIFIED','live','Goal completion'],
      'graph_contract':'32 nodes / 67 edges is source topology; 137 inventory items =77 NODE+60 EXCLUDED. Thirteen internal bridge nodes require implementation or explicit retired route, not source theorem credit.'
    }
    rec={'schema':'pbps75-independent-source-only-freeze/v1','actor':'/root/independent_source75','phase':'SOURCE_ONLY_BEFORE_CURRENT_LEAN','actual_PID':os.getpid(),'source_primary':ref(PRIMARY),'baseline_inputs':[ref(BASE/f) for f in files],'counts':{'nodes':32,'edges':67,'items':137,'NODE':77,'EXCLUDED':60,'internal_bridges':13,'exact_formulas':len(form['source_formulas'])},'all_RAW_ranges_rechecked':True,'every_classification_preserved':True,'expectations':expectations,'current_module_or_packet_read':False}
    rec['freeze_sha256']=sha(canonical(rec))
    (OWN/'source-only.freeze75.json').write_bytes((json.dumps(rec,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
    print(json.dumps({'status':'SOURCE_ONLY_FREEZE_PASS','PID':os.getpid(),'freeze':ref(OWN/'source-only.freeze75.json'),'counts':rec['counts']}))
    for r in inv['regions']:
        a,b=r['RAW_range']; p=TextMath();p.feed(raw[a:b].decode('utf-8'))
        print('\nSOURCE REGION '+r['region_id']+'\n'+''.join(p.out))
    print('\nSOURCE GRAPH NODES')
    for n in graph['nodes']:print(n['id']+' '+n['kind']+' '+n['label']+' | '+n['meaning'])
    print('\nSOURCE GRAPH EDGES')
    for e in graph['edges']: print(json.dumps(e,ensure_ascii=False,separators=(',',':')))

if __name__=='__main__':main()
