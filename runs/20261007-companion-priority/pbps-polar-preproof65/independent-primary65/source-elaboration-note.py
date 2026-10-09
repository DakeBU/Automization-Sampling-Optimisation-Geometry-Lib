import json,hashlib
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-primary65')
def load(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
g=load('source-proof-graph.json')
for n in g['nodes']:
 if n['id']=='typed-B0': n['content']+=' For g in Hperp, the full-HP adjoint B* g lies in HP0 because B annihilates constants, and i0(B0* g)=B* g; this compatibility must be produced internally.'
 if n['id']=='B13-B14-side-branches': n['content']+=' The macro norm-bound half of B14 is upstream provenance for B15; the lower-floor half is a separate estimate and is not needed for B16.'
write('source-proof-graph.json',g)
h=load('residual-next-header.json');h['internally_produced_inputs'] += ['full/centered adjoint compatibility: B* maps Hperp into exact HP0 since B kills constants, and i0(B0* g)=B* g','for every globally centered f, P f lies in exact HP0 by total-mean preservation and (I-P)f lies in exact Hperp'];write('residual-next-header.json',h)
p=load('primary-only-review.json');p['source_graph']=g;p['residual_next_header']=h;write('primary-only-review.json',p)
print('source-level adjoint transport and exact corrector-domain production made explicit')
