from pathlib import Path
import json, hashlib
root=Path(r'E:\Samplinglib'); task=Path(__file__).parent
specs=[
 ('variance','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',[(20,29)]),
 ('tilted','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',[(25,43)]),
 ('stdGaussian','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',[(50,68)]),
 ('gradient','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',[(50,84)]),
 ('Lp','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',[(89,91),(102,108)]),
 ('partial-linear-graph','.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean',[(40,49),(731,744)]),
 ('closed-gradient','.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean',[(48,71),(95,98),(107,109),(128,129)]),
 ('disintegration','.lake/packages/mathlib/Mathlib/Probability/Kernel/Disintegration/Basic.lean',[(39,59)]),
 ('bounded-extension','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Extend.lean',[(178,190),(194,196),(201,203)]),
]
records=[]
for label,relative,ranges in specs:
    path=root/relative
    with path.open('rb') as handle: raw=handle.read()
    lines=raw.decode('utf-8').splitlines(keepends=True)
    context=[]
    for a,b in ranges:
        fragment=''.join(lines[a-1:b])
        if label != 'Lp': fragment=fragment.split(':= by')[0]
        snapshot=label+'.'+str(a)+'-'+str(b)+'.raw.context.lean'
        data=fragment.encode('utf-8')
        with (task/snapshot).open('wb') as handle:handle.write(data)
        with (task/snapshot.replace('.raw.','.lf.')).open('wb') as handle:handle.write(data.replace(b'\r\n',b'\n'))
        context.append({'line_start':a,'requested_line_end':b,'snapshot':snapshot,'raw_sha256':hashlib.sha256(data).hexdigest(),'raw_bytes':len(data),'lf_sha256':hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest(),'lf_bytes':len(data.replace(b'\r\n',b'\n')),'proof_delimiter_truncated':':= by' in ''.join(lines[a-1:b])})
        print(label,a,b,fragment)
    records.append({'label':label,'physical_path':str(path),'whole_file_raw_sha256':hashlib.sha256(raw).hexdigest(),'whole_file_raw_bytes':len(raw),'ranges':context,'status':'LEXICAL_DEFINITION_OR_OPAQUE_EXTERNAL_CONTRACT_NOT_IMPLEMENTATION_REVIEW'})
with (task/'external-semantic-context-snapshots.json').open('w',encoding='utf-8',newline='\n') as handle:json.dump(records,handle,indent=2);handle.write('\n')
