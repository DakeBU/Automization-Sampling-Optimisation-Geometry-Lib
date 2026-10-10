from common import *
import re
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==INT
assert subprocess.check_output(['git','rev-parse',INT+'^'],cwd=ROOT).decode().strip()==SCI
W(P/'lease.open.json',dict(status='OPEN',actor=ACTOR,actual_opener_PID=os.getpid(),checked_science=SCI,checked_integration=INT,compiler='NOT_STARTED',owns='Only new repository-exposition-seal62 reviewer files.'))
delta=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',INT],cwd=ROOT).decode().splitlines();assert len(delta)==1875,len(delta)
tree=subprocess.check_output(['git','ls-tree','-r',INT],cwd=ROOT).decode().splitlines();mapping={s.split('\t',1)[1]:s.split()[2] for s in tree}
objects=[mapping[p] for p in delta];child=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);raw,err=child.communicate(('\n'.join(objects)+'\n').encode());assert child.returncode==0 and not err
offset=0;entries=[]
for relative,oid in zip(delta,objects):
 end=raw.index(b'\n',offset);hdr=raw[offset:end].decode().split();size=int(hdr[2]);data=raw[end+1:end+1+size];offset=end+size+2;assert hdr[0]==oid
 q=pin(relative);assert H(data.replace(b'\r\n',b'\n'))==q['lf_sha256'],relative
 entries.append(dict(repository_path=relative,git_blob=oid,git_raw_sha256=H(data),git_bytes=len(data),git_LF_sha256=H(data.replace(b'\r\n',b'\n')),opening_current=q))
W(P/'integration.git.entries.json',dict(checked_commit=INT,parent=SCI,count=len(entries),actual_catfile_PID=child.pid,exit_code=0,entries=entries))
W(P/'integration.tree.index.json',dict(checked_commit=INT,files=mapping,production_module_count=sum(p.startswith('AutoSamplingTheory/') and p.endswith('.lean') for p in mapping),no_production63=not any('MacroDefectRoot' in p for p in mapping)))
selected=[R/'integration.notes.json',R/'root.exact-verification62.adoption.json',R/'visual.inspection.json',ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html',ROOT/'_site/lean-foundations.html']
selected.extend(q for q in (R/'integration62/visual62').iterdir() if q.is_file())
# Keep exact current generated assets before new production files can exist.
for h in selected[:]:
 if h.suffix=='.html':
  for name in re.findall(r'(?:src|href|data-graph-source)=[\"\']([^\"\']+)[\"\']',h.read_text(encoding='utf8')):
   if name.startswith('/assets/') and (ROOT/'_site'/name.lstrip('/')).is_file():selected.append(ROOT/'_site'/name.lstrip('/'))
selected.extend(ROOT/p for p in delta if p.startswith(('research-wiki/frontier-cells/','website/content/','Libraries/','AutoSamplingTheory/','Tests/')) or p in ['AutoSamplingTheory.lean','Tests.lean','runs/substantive_advances.jsonl','docs/companion-papers-handoff.md'])
selected.extend([ROOT/'tools/astis_site.py',ROOT/'website/scripts/underlying_lean_graph.py',ROOT/'website/scripts/publication_reader.py'])
snaps=[];seen=set()
for source in selected:
 source=source.resolve()
 if source in seen:continue
 seen.add(source);q=pin(source);dest=P/(f'input-{len(snaps):04d}-'+H(source.as_posix().encode())[:24]+'.exactraw.snapshot');dest.write_bytes(source.read_bytes());matches(q,dest);snaps.append(dict(original=q,exact_raw_snapshot=pin(dest)))
W(P/'opening.inputs.json',dict(status='FROZEN',checked_science=SCI,checked_integration=INT,actual_opener_PID=os.getpid(),integration_entries=1875,qualified_snapshots=len(snaps),snapshot_pairs=snaps,source63='Claimed-only/preproof63 tracked integration records provide planning evidence, never compiled proof credit. Future production63 untracked/new paths excluded from exact integration tree.',memory_registry_context='MEMORY.md552-554 only: source/repository boundaries remain scoped; all factual results independently current.'))
print('OPENING62_FROZEN',len(entries),'Git entries',len(snaps),'qualified snapshots',os.getpid())
