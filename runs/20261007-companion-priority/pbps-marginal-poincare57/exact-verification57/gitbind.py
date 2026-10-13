from common import *
assert git('rev-parse','HEAD')==BASE
cp=subprocess.run(['git','diff-tree','--no-commit-id','--raw','--no-abbrev','-z','-r',BASE],cwd=R,capture_output=True,check=True)
(O/'science.diff-tree.raw.log').write_bytes(cp.stdout)
t=cp.stdout.split(b'\0');i=0;entries=[]
while i<len(t) and t[i]:
 meta=t[i].decode('utf-8').split();p=t[i+1].decode('utf-8');i+=2
 assert len(meta)==5 and meta[4] in ['A','M'],(p,meta)
 assert not re.search(r'(?:pbps|preread|sourcegraph).*?(?:58|59)(?:/|$)',p),p
 entries.append(dict(path=p,old_mode=meta[0][1:],new_mode=meta[1],old_git_blob=meta[2],git_blob=meta[3],change=meta[4]))
assert entries
q=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
data,err=q.communicate(('\n'.join(x['git_blob'] for x in entries)+'\n').encode('ascii'))
assert q.returncode==0,err
pos=0
for e in entries:
 end=data.index(b'\n',pos);header=data[pos:end].decode('ascii').split();pos=end+1
 assert header[0]==e['git_blob'] and header[1]=='blob'
 n=int(header[2]);blob=data[pos:pos+n];pos+=n;assert data[pos:pos+1]==b'\n';pos+=1
 b=path(e['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert blob==b or blob==lf,e['path']
 e.update(current=pin(e['path']),git_bytes=len(blob),git_raw_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),current_binding='RAW_IDENTICAL' if blob==b else 'EXACT_CRLF_PAIRS_TO_LF_IDENTICAL')
assert pos==len(data)
result=dict(status='PASS',checked_commit=BASE,parent_commit=git('rev-parse',BASE+'^'),actual_science_entry_count=len(entries),entries=entries,cat_file_actual_PID=q.pid,cat_file_exit_code=q.returncode,cat_file_resource='CLOSED',raw_diff=pin(O/'science.diff-tree.raw.log'),future58_59_entries=0)
dump('science.gitbindings.json',result)
print(json.dumps(dict(status='PASS',checked_commit=BASE,entry_count=len(entries),whitespace_or_diagnosis_paths=[x['path'] for x in entries if any(s in x['path'].lower() for s in ['whitespace','admission.0'])],actual_cat_file_PID=q.pid)))
