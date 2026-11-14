from pathlib import Path
import json,hashlib
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/r9-full-consumer-source-review-v3a';I=B/'inputs'
def h(a):return hashlib.sha256(a).hexdigest()
u=json.loads((I/'4-huanjian-gaussian-source-matrix-variance.json').read_bytes())['units'][0]
mods=['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean','Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean'];folds=[]
for start,end,p in [(0,4,mods[0]),(4,7,mods[1])]:
 a=''.join(s['lean'] for s in u['steps'][start:end]).encode();raw=(R/p).read_bytes();assert a==raw,p;folds.append({'module':p,'step_range':[start+1,end],'full_module_bytes_equal':True,'lines':len(raw.splitlines()),'bytes':len(raw),'sha256':h(raw)})
m=json.loads((I/'3-source-lean-map.full-consumer-v3a.draft.json').read_bytes());out=[];coverage=set()
for i,row in enumerate(m['mappings'],1):
 for kind in ['source','lean']:
  for item in row[kind]:
   p=item.get('file',item.get('path'));raw=(R/p).read_bytes();assert h(raw)==item['file_sha256'],p
   lo,hi=([item['raw_utf8_start'],item['raw_utf8_end']] if kind=='source' else item['raw_UTF8_byte_span']);piece=raw[lo:hi];assert h(piece)==item['span_sha256'],(i,p)
   text=raw.decode();clo,chi=([item['char_start'],item['char_end']] if kind=='source' else item['decoded_char_span']);assert text[clo:chi].encode()==piece
   if kind=='lean':
    l,hline=item['LF_lines_1based'];assert ''.join(text.splitlines(True)[l-1:hline]).encode()==piece;coverage.update(range(l,hline+1))
   else:
    assert text.count('\n',0,clo)+1==item['lf_line_start']
   out.append({'mapping':i,'kind':kind,'file':p,'raw_span':[lo,hi],'sha256':h(piece),'exact':True})
lines=(R/mods[1]).read_text().splitlines();missing=[{'line':i,'text':line} for i,line in enumerate(lines,1) if i not in coverage and line.strip()]
r={'folds':folds,'map_exact_spans':out,'unmapped_nonblank_T_lines':missing,'map_alone_full_code_coverage':not missing,'all7_folds_full_code_coverage':True,'scope':'code bytes same as separately frozen full-code reviews; exact hashes do not substitute for semantic reading'}
(B/'span-and-fold-checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'folds':folds,'exact_map_spans':len(out),'unmapped_nonblank_T_lines':missing},indent=2))
