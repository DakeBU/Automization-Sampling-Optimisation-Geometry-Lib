from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import ctypes, hashlib, json, os, re, subprocess, sys

BASE = Path('E:/Samplinglib')
R = BASE / 'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
OWN = R / 'independent-repository-reader73'
DISPATCH = R / 'final-reader-repository-packet73.json'
COMMIT = 'd7e00a7c0e8b0f37fcc2dbe99f6b646d3a7b1de6'
DECL = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'
MODULE = BASE / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
ACTOR = '/root/header_math72'
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf8')
load = lambda p: json.loads(Path(p).read_bytes())

def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

def check(z):
    p = Path(z['path']); p = p if p.is_absolute() else BASE / p
    b = p.read_bytes()
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'] and sha(b.replace(b'\r\n', b'\n')) == z['LF_sha256'], p
    return b

def write(p, j):
    p = Path(p); assert p.is_relative_to(OWN) and not (OWN / 'lease.final.json').exists()
    p.write_text(json.dumps(j, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf8', newline='\n')

def head():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=BASE, text=True).strip()

class Node:
    def __init__(self, tag, attrs): self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self): return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)
    def nodes(self):
        yield self
        for c in self.children:
            if isinstance(c, Node): yield from c.nodes()

class Article(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.stack=[]; self.root=None
    def handle_starttag(self, tag, attrs):
        if not self.stack and not (tag == 'article' and dict(attrs).get('data-authored-declaration') == DECL): return
        n = Node(tag, attrs)
        if self.stack: self.stack[-1].children.append(n)
        else: assert self.root is None; self.root=n
        if tag not in ['br','hr','img','input','meta','link','source','wbr']: self.stack.append(n)
    def handle_endtag(self, tag):
        if self.stack:
            for i in range(len(self.stack)-1, -1, -1):
                if self.stack[i].tag == tag: del self.stack[i:]; break
    def handle_data(self, data):
        if self.stack: self.stack[-1].children.append(data)

def difference(a, b, path=''):
    if type(a) is not type(b): return [path]
    if isinstance(a, dict):
        out=[]
        for k in sorted(a.keys() | b.keys()):
            out += [path+'/'+k] if k not in a or k not in b else difference(a[k],b[k],path+'/'+k)
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [path]
        return [p for i,(x,y) in enumerate(zip(a,b)) for p in difference(x,y,path+'/'+str(i))]
    return [] if a == b else [path]

def inspect():
    assert not (OWN/'lease.final.json').exists() and head()==COMMIT
    d=load(DISPATCH); assert d['checked_science_commit']==COMMIT and len(d['inputs'])==134
    for z in d['inputs']: check(z)
    manifest=dict(dispatch=pin(DISPATCH), input_count=134, inputs=d['inputs'])
    write(OWN/'inputs.manifest.json',manifest)
    receipts=[]; logs={}
    for z in d['inputs']:
        p=Path(z['path'])
        if p.name=='receipt.json' and p.parent.name!='generator-sideeffects':
            j=load(p); label=p.parent.name
            assert j['terminal_closed'] and j['checked_parent']==COMMIT
            assert j['exit_code']==(1 if label in ['record-final','narrow-generated-scope'] else 0)
            receipts.append(dict(label=label, receipt=z, actual_foreground_PID=j['actual_foreground_PID'], EXIT=j['exit_code'], terminal_closed=True, command=j['command']))
        if p.name in ['stdout.log','stderr.log'] and p.parent.name in ['mandatory-astis-check-final','publication-final','graph-check-final','site-check-final','frontier-final','contributor-final','semantic-final','narrow-generated-scope','narrow-generated-scope-diagnostic-recheck','record-final','record-final-import-repair']:
            t=p.read_text(encoding='utf8'); logs[p.parent.name+'/'+p.name]=t if len(t)<40000 else t[-8000:]
    astis=(R/'integration73/mandatory-astis-check-final/stdout.log').read_text(encoding='utf8')
    assert all(s in astis for s in ['Build completed successfully (9184 jobs).','Build completed successfully (9484 jobs).','ASTIS check passed'])
    assert 'Publication PASS: 243 source items' in logs['publication-final/stdout.log']
    assert 'ASTIS site check passed' in logs['site-check-final/stdout.log']
    raw=MODULE.read_bytes(); source=raw.decode('utf8'); lines=source.splitlines(keepends=True)
    assert len(lines)==178 and sha(raw)=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
    assert subprocess.check_output(['git','show',COMMIT+':'+MODULE.relative_to(BASE).as_posix()],cwd=BASE)==raw
    lesson=load(BASE/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json')['units'][0]
    steps=lesson['steps']; assert len(steps)==6
    checked_steps=[]
    for i,s in enumerate(steps):
        z=s['lean_source_region']; code=''.join(lines[z['start_line']-1:z['end_line']])
        assert code==s['lean'] and sha(code.encode())==z['exact_code_raw_sha256'] and z['source_raw_sha256']==sha(raw)
        checked_steps.append(dict(ordinal=i+1,title=s['title'],formula=s['formula'],start_line=z['start_line'],end_line=z['end_line'],exact_BODY_sha256=sha(code.encode())))
    public_header=source[source.index('theorem actual_harmonic_flow_laws'):source.index(' := by',source.index('theorem actual_harmonic_flow_laws'))]
    private=source[source.index('private def actual_harmonic_flow_statement'):source.index('\ntheorem actual_harmonic_flow_laws')].rstrip()
    # The generated proof panel retains the source trailer (end/end/#print axioms).
    proof=source[source.index('theorem actual_harmonic_flow_laws'):].rstrip()
    copy=load(R/'integration73/visual73/copy-unit0-copy-and-download.inspect.json')
    assert copy['initialFolded'] and copy['copyProbeUsesIsolatedPageClipboardCallback'] and not copy['physicalOSClipboardTest']
    assert len(copy['panels'])==len(copy['downloads'])==3 and len(copy['steps'])==6
    expected=[public_header,proof,private]
    for x,e in zip(copy['panels'],expected): assert x['callbackCalled'] and x['copiedExactly'] and x['code']==e
    for x in copy['downloads']: assert x['status']==200 and x['text'].encode('utf8')==raw
    for x,s in zip(copy['steps'],steps): assert x['initiallyFolded'] and x['lean']==s['lean']
    html=(BASE/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf8')
    parser=Article(); parser.feed(html); assert parser.root
    nodes=list(parser.root.nodes()); details=[n for n in nodes if n.tag=='details']
    assert all('open' not in n.attrs for n in details)
    codes=[n.text() for n in nodes if n.tag=='code']
    assert all(e in codes for e in expected) and all(s['lean'] in codes for s in steps)
    assert private in codes and 'actual_harmonic_flow_statement' in private
    assert len(details)==12
    body=source[source.index(' := by',source.index('theorem actual_harmonic_flow_laws'))+6:source.index('\nend\n')]
    unused=['hα','hαβ','hH','hβη']; assert all(not re.search(r'(?<![\w])'+re.escape(x)+r'(?![\w])',body) for x in unused)
    assert all(x in public_header for x in ['hα :','hαβ :','hV :','hH :','hη :','hβη :'])
    assert all(x in lesson['statement'] for x in ['rank zero','two Hessian bounds','positive lower modulus','step cap','No energy positivity'])
    cell=load(BASE/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json')
    before=load(R/'integration73/cell.before-final-admin.exactraw.snapshot.json')
    assert cell['purification']['status']=='pending' and cell['learning_contract']['reader_backpressure']['exposition_seal_status']=='pending'
    graph=load(BASE/'_site/data/underlying-lean-graph.json'); target='decl:'+DECL
    gn=[x for x in graph['nodes'] if x['id']==target]; ge=[x for x in graph['edges'] if x['source']==target or x['target']==target]
    assert len(gn)==1 and len(ge)==4
    assert {x['relation'] for x in ge}=={'declares','source reference (scanner)','Lean target under audit','source correspondence; not a Lean dependency'}
    captures=[z for z in d['inputs'] if z['path'].endswith('.png')]; assert len(captures)==9
    reused=load(R/'integration73/unchanged-regression-reuse.json')
    for record in reused['records']:
        for key in ['receipt','stdout','stderr']: check(record[key])
        assert not record['fresh_for73'] and load(BASE/record['receipt']['path'])['exit_code']==0
    assert all(z['historical_RAW_hash_not_recorded'] for z in reused['current_runtime_pins'])
    for z in reused['current_runtime_pins']: check(z['current_pin'])
    generated=load(R/'integration73/generator-sideeffects/receipt.json')
    assert generated['tracked_generated_restored']==100 and generated['unused_new_generated_cards_preserved']==443 and generated['actual_PID']==26180
    assert 'AssertionError' in logs['narrow-generated-scope/stderr.log']
    assert 'unsupported": []' in logs['narrow-generated-scope-diagnostic-recheck/stdout.log']
    diagnosis=load(R/'integration73/record-final-import-diagnosis/diagnosis.json')
    assert diagnosis['failed_PID']==28464 and diagnosis['failed_EXIT']==1 and not diagnosis['canonical_math_source_or_site_changes']
    adoptions={n:load(R/n) for n in ['root.math73.adoption.json','root.decoder73.adoption.json','root.source73.adoption.json','root.exact-verification73.adoption.json']}
    assert adoptions['root.exact-verification73.adoption.json']['verified_commit']==COMMIT
    result=dict(status='PASS_BOUNDED_INSPECTION_PENDING_NAMED_READER_DECISION',actual_reader_PID=os.getpid(),checked_science_commit=COMMIT,finite_dispatch_inputs_checked=134,RAW_authority=True,LF_rule='Replace CRLF byte pairs with LF only; preserve all other bytes.',gate_receipts=receipts,gate_log_named_excerpts=logs,steps=checked_steps,initially_folded_details=12,full_private_literal_adjacent=True,original_callers=['hα','hαβ','hV','hH','hη','hβη'],unused_standing_conditions=unused,copy_callbacks=3,RAW_downloads=3,download_RAW_bytes=8519,download_legacy_bytes_field=7910,download_legacy_field_qualification='The browser bytes field is JavaScript string.length; exact UTF8 reconstruction is 8519 RAW bytes and matches source SHA256.',capture_pins=captures,graph_node=gn[0],graph_edges=ge,current_cell_admin_diff=difference(before,cell),prior_regression_reuse=reused,generated_scope=dict(failed_PID=32932,failed_EXIT=1,diagnostic_PID=26180,diagnostic_EXIT=0,restored_previously_clean_generated_paths=100,preserved_unused_new_cards=443,original_offending_path_captured=False,original_cause_established=False),recorder_diagnosis=diagnosis,adoptions=adoptions)
    write(OWN/'inspection.json',result)
    print(json.dumps(dict(status='PASS',PID=os.getpid(),inputs=134,steps=6,closed_details=12,copy_callbacks=3,RAW_downloads=3,RAW_download_bytes=8519,graph_edges=4,admin_diff=result['current_cell_admin_diff']),ensure_ascii=False))

def postclose():
    lp=OWN/'lease.final.json'; l=load(lp)
    assert l['status']=='CLOSED_LAST' and l['actor']==ACTOR and l['postclose_owned_writes_forbidden'] and l['final_owned_write']
    rows=l['files']; assert len(rows)+1==l['file_count_including_lease'] and sha(can(rows))==l['closure_logical_sha256']
    assert {p.resolve() for p in OWN.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
    for z in rows: check(z); assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
    run=load(OWN/'run.json'); assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['run_sha256']
    for k in ['decision','inputs_manifest','complete_named_RAW_payload']: check(run[k])
    m=load(run['inputs_manifest']['path']); check(m['dispatch']); dispatch=load(DISPATCH)
    assert m['inputs']==dispatch['inputs'] and m['input_count']==len(m['inputs'])==134
    for z in m['inputs']: check(z)
    d=load(run['decision']['path']); payload=load(run['complete_named_RAW_payload']['path'])
    assert payload['decision']==d and payload['inputs']==m and head()==run['checked_science_commit']==d['checked_science_commit']==COMMIT
    assert d['accepted_scoped_aggregate'] and not d['blockers'] and d['independent_of_formalizer_stabilizer']
    assert d['actor']==ACTOR and not d['new_VERIFIED_transition'] and not d['new_independent_mathematics_certification']
    assert all(not d[k] for k in ['Goal_complete','PURIFIED','full_Exposition_Seal','main','live','whole_paper'])
    kernel=ctypes.WinDLL('kernel32',use_last_error=True); kernel.OpenProcess.restype=ctypes.c_void_p
    handle=kernel.OpenProcess(0x00100000,False,l['writer_PID'])
    if handle:
        kernel.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong]; kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        assert kernel.WaitForSingleObject(handle,0)==0, 'Writer is still running'
        kernel.CloseHandle(handle)
    else: assert ctypes.get_last_error()==87, ctypes.get_last_error()
    print(json.dumps(dict(status='PASS_POSTCLOSE_READONLY',actual_external_readonly_PID=os.getpid(),writer_PID=l['writer_PID'],writer_terminated=True,owned_files=l['file_count_including_lease'],inputs=134,run_sha256=run['run_sha256'],lease=pin(lp),complete_named_RAW_payload=run['complete_named_RAW_payload'],no_owned_writes=True,terminal_EXIT_contract=0),ensure_ascii=False))

if __name__=='__main__':
    assert len(sys.argv)==2
    {'inspect':inspect,'postclose':postclose}[sys.argv[1]]()
