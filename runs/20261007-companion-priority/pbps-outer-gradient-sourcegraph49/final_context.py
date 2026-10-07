# -*- coding: utf-8 -*-
import pathlib,json,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49';H=lambda b:hashlib.sha256(b).hexdigest();g=json.loads((d/'source-proof-graph.json').read_text(encoding='utf-8'));inv=json.loads((d/'caller-inventory.json').read_text(encoding='utf-8'));tok=json.loads((d/'selected-token-inventory.json').read_text(encoding='utf-8'));cov=json.loads((d/'source-coverage.json').read_text(encoding='utf-8'));inp=json.loads((d/'input-bindings.json').read_text(encoding='utf-8'));ps=json.loads((d/'selected-providers.json').read_text(encoding='utf-8'))
# Pin inherited E typing contexts of the two global-variable public parent signatures.
for mod in ['GibbsAugmentation','GaussianReflection']:
 p=r/'AutoSamplingTheory/ExampleCases/ProximalBPS'/(mod+'.lean');b=p.read_bytes();m=re.search(rb'^variable \{E : Type\*\}[^\n]*\n[^\n]*',b,re.M);assert m;part=m.group();a=b[:m.start()].count(b'\n')+1;z=b[:m.end()-1].count(b'\n')+1;stem='parent-context-'+mod;(d/(stem+'.raw')).write_bytes(part);(d/(stem+'.lf')).write_bytes(part.replace(b'\r\n',b'\n'));rec=dict(id=stem,path=str(p),kind='typing-context',whole_raw_sha256=H(b),whole_lf_sha256=H(b.replace(b'\r\n',b'\n')),fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n')),fragment_bytes=len(part),snapshot=stem,physical_lines1=[a,z],selected_physical_lines1=[a,z],start_utf8_byte0=m.start(),end_utf8_byte0_exclusive=m.end());inp.append(rec);ps.append(rec)
 for line in range(a,z+1):cov['rows'].append(dict(path=str(p),physical_line1=line,classification='NODE',reason='Inherited global public producer E typing context; no proof selected',provider_ids=[stem],node_ids=['P.typing'],selected_fragment_byte_interval0=[m.start(),m.end()],physical_line_raw_sha256=H(b.splitlines(keepends=True)[line-1])))
# Bare typing-family ids are never asserted as qualified declarations.
for entry in inv['entries']+tok['entries']:
 if entry.get('resolved_node')=='P.typing':entry.pop('qualified_id',None);entry['resolved_family']='typing-contract-family'
# Remove genuinely unused AE-marker node; actual AE hypotheses remain in primitive contracts/typing inventory.
g['nodes']=[n for n in g['nodes'] if n['id']!='P.AE']
cov['rows']=sorted(cov['rows'],key=lambda v:(v['path'],v['physical_line1']));assert len(cov['rows'])==len(set((v['path'],v['physical_line1']) for v in cov['rows']))
for f,o in [('source-proof-graph.json',g),('caller-inventory.json',inv),('selected-token-inventory.json',tok),('source-coverage.json',cov),('input-bindings.json',inp),('selected-providers.json',ps)]: (d/f).write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),rows=len(cov['rows']),NODE=sum(v['classification']=='NODE' for v in cov['rows']),EXCLUDED=sum(v['classification']=='EXCLUDED' for v in cov['rows']),inputs=len(inp))))
