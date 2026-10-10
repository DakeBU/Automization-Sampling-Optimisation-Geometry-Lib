from pathlib import Path
import hashlib,json,os,re,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74/integration74');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
baseline=load(r/'before-generator-state.json');keep=set(baseline['keep']);pre=set(baseline['preexisting_tracked_changes']);tracked=set(subprocess.check_output(['git','ls-files'],text=True).splitlines())
log=(r/'module-graph-refresh/stdout.log').read_text(encoding='utf8').replace('\\','/')
names=sorted({m.group(1).strip() for m in re.finditer(r'^(?:wrote |\- )(.+)$',log,re.M)}&tracked-keep-pre)
out=r/'generator-line-ending-diagnosis';assert (out/'diagnosis.json').is_file();rows=[]
for p in names:
 current=Path(p).read_bytes();old=subprocess.check_output(['git','show',baseline['head']+':'+p])
 if current==old:continue
 assert current.replace(b'\r\n',b'\n')==old.replace(b'\r\n',b'\n'),p
 i=len(rows);a=out/f'cache-remaining-{i}.generated.exactraw.snapshot';b=out/f'cache-remaining-{i}.HEAD.exactraw.snapshot';assert not a.exists() and not b.exists();a.write_bytes(current);b.write_bytes(old)
 rows.append(dict(path=p,generated_backup=a.as_posix(),HEAD_backup=b.as_posix(),generated_RAW_sha256=sha(current),HEAD_RAW_sha256=sha(old),LF_sha256=sha(old.replace(b'\r\n',b'\n')),only_CRLF_pairs_differ=True,explicit_generator_stdout=True,preexisting_tracked_change=False))
for z in rows:
 p=Path(z['path']);assert sha(p.read_bytes())==z['generated_RAW_sha256'];p.write_bytes(Path(z['HEAD_backup']).read_bytes())
q=out/'remaining-RAW-diagnosis.json';assert not q.exists();q.write_text(json.dumps(dict(status='EXPLICIT_GENERATOR_RAW_BYTE_RECONCILIATION',actual_PID=os.getpid(),scanned_clean_tracked_generator_paths=len(names),remaining_CRLF_only_count=len(rows),rows=rows,source_Lean_and_publication_unchanged=True,canonical_collaborator_files_preserved=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 explicit generator RAW reconciliation; additional CRLF-only clean files restored:',len(rows))
