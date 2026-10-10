"""Tiny distinct exact two-field metadata review; native binding functions only."""
from __future__ import annotations
import ctypes, hashlib, json, os, subprocess, sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path('E:/Samplinglib'); OWN=Path(__file__).resolve().parent; R73=OWN.parent
P=R73/'frontier-label-overlay73/proposal.json'
SHA='53a145fb79a389164ad6a9f47b8f963b07f145f30553288f5c6ab61c6c82a4fd'
LF='Replace CRLF byte pairs with LF only; retain bare CR and every other byte.'
RECIPE='Delete ONLY top-level run_sha256; json.dumps ensure_ascii=False, sort_keys=True, separators=(comma,colon), allow_nan=False; SHA256 UTF-8 without BOM/newline. Preserve every other and nested field.'
def sha(b): return hashlib.sha256(b).hexdigest()
def cj(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def logical(v): return sha(cj({k:x for k,x in v.items() if k!='run_sha256'}))
def pairs(rows):
    d={}
    for k,v in rows: assert k not in d,('duplicate key',k); d[k]=v
    return d
def read(p): return json.loads(Path(p).read_bytes().decode('utf-8'),object_pairs_hook=pairs)
def pin(p):
    p=Path(p); b=p.read_bytes(); l=b.replace(b'\r\n',b'\n'); return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l),'LF_recipe':LF}
def save(n,v):
    assert not (OWN/'lease.final.json').exists(); p=OWN/n; assert OWN in p.resolve().parents
    p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8'))
def guard(rows):
    for r in rows: assert pin(r['path'])==r,('drift',r['path'])
def diff(a,b,p=''):
    if type(a) is not type(b): return [{'pointer':p,'before':a,'after':b}]
    if isinstance(a,dict):
        assert set(a)==set(b),('keyset change',p)
        return [r for k in sorted(a) for r in diff(a[k],b[k],p+'/'+k.replace('~','~0').replace('/','~1'))]
    if isinstance(a,list):
        assert len(a)==len(b),('list length change',p)
        return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [{'pointer':p,'before':a,'after':b}]

REVIEW='''# Distinct exact frontier search-label repair73 review

ACCEPT exact proposal RAW4298 SHA53a145fb79a389164ad6a9f47b8f963b07f145f30553288f5c6ab61c6c82a4fd, as metadata wording only. Reviewer /root/header_math72 differs from proposer/canonical writer /root and the source reviewer /root/independent_primary69. No new SCI, source, mathematics or VERIFIED credit is given.

I read both complete before/proposed RAW JSONs with duplicate-key rejection. Actual frontier schema is schema_version3; current canonical bytes equal the exact before bytes. Exhaustive recursive comparison finds exactly /shared_floor_audit/searched/0 and /reuse_plan/searched_existing/0. Both old strings are "Exact source-first finite retrieval: runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json". Both new strings are "Samplinglib exact source-first finite retrieval: runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json". Each change adds the Samplinglib label AND changes initial Exact to lowercase exact. Thus this is exactly two string replacements, not literally prefix insertion with every old string byte retained. Replacing precisely those two complete JSON string tokens reconstructs the entire proposed RAW, including formatting/endings; no other field or byte changes. Approved before SHA8bf5034754d7932caeee43d6dacb73357c1727681cc2d7fa37288dfd8ab0b4af, after SHAea6da105f453a8af3feb5fd1547e4142db816ab744df8143c3db1dfb8557446c.

The existing exact api.retrieval.json SHAe55254a15e18f338c942b54ee8382ba7ee31dd14872e0a17ad0e720ed908fc58 establishes the label's truth. Native queries schema has five rows. local_dynamics_inventory explicitly searched AutoSamplingTheory/TechnicalLemmas and AutoSamplingTheory/ExampleCases/ProximalBPS: PID38848 terminal EXIT1 means no match in that finite historical query, with empty stderr, not a failed proof or absence everywhere. existing_local_adapters searched named actual Samplinglib files and returned existing local declarations: PID15364 terminal EXIT0. chosen_mathlib_interfaces PID20056 EXIT0 separately records Mathlib retrieval; the existing Mathlib label remains unchanged. All stored query stdout/stderr UTF-8 hashes are independently recomputed. These are historical bounded retrieval receipts, not new current-source search or proof certificates.

I recomputed native tools/astis_publication.py binding_payload, binding_digest and review_context with exact current publication/lesson/module and before/current/proposed cell data. The payloads are exactly equal in all three cases. Frontier metadata is not consumed by these functions. Publication binding remains627cae79b09fa7c73f90020fcc85081a9ba134ac778d47871f3a10f4a18250ea; canonical review-context SHA remains1722badb9a3f7ec13118dcb9017be0a02276777610ce582769f436bee2bd0370. The context equals the existing source audit publication_context and source packet candidate_publication_context. Native semantic_reviewer_packet exactly regenerates the existing full source packet and its logical SHA5ebea0f0e8a0d5b355a86655e0ccb8cf121dee5624ffce51d5b2290d6ff54cbf. All proposal unchanged pins for actual Lean, publication, lesson, audit and source packet are exact; statement, formulas, six callers, assumptions, source evidence and prior source decision remain unchanged.

Only the root writer may apply the approved exact overlay after the failed SCI run is closed, then create the required metadata-only science child and obtain fresh independent verification. This review does not perform or replace those actions. No Lean/frontier/publication/semantic/site/contributor gate is run, no canonical/Git/ledger change is made, and no SCI/VERIFIED/PURIFIED/Exposition/Goal admission is produced. All actual stochastic H_y/kernel/K/r_rho/B27/B28, nonexplosion, invariance, full-paper, cost/composition boundaries remain open. Finite native RAW/LF pins, complete named decision/input payload and CLOSED_LAST cover only this new review directory.
'''

def inspect():
    assert not (OWN/'decision.json').exists(); proposal=read(P); assert len(P.read_bytes())==4298 and sha(P.read_bytes())==SHA
    assert proposal['schema']=='astis-independent-frontier-search-label-overlay73/v1' and proposal['proposer']=='/root'
    bp=ROOT/proposal['before']['path']; ap=ROOT/proposal['after']['path']; cp=ROOT/proposal['canonical_path']; b0=bp.read_bytes(); b1=ap.read_bytes()
    for name,p in [('before',bp),('after',ap),('current',cp),('existing_search_evidence',ROOT/proposal['existing_search_evidence']['path'])]:
        for k in ['RAW_bytes','RAW_sha256','LF_sha256']: assert pin(p)[k]==proposal[name][k]
    assert cp.read_bytes()==b0; before=read(bp); after=read(ap); assert before['schema_version']==after['schema_version']==3
    expected=[{'pointer':x['JSON_pointer'],'before':x['before'],'after':x['after']} for x in proposal['changes']]
    assert len(expected)==2 and {x['pointer'] for x in expected}=={'/shared_floor_audit/searched/0','/reuse_plan/searched_existing/0'}
    assert diff(before,after)==sorted(expected,key=lambda x:x['pointer'])
    old=proposal['changes'][0]['before']; new=proposal['changes'][0]['after']; assert all(x['before']==old and x['after']==new for x in proposal['changes'])
    assert new=='Samplinglib '+old[0].lower()+old[1:] and new!='Samplinglib '+old
    oldtoken=json.dumps(old,ensure_ascii=False).encode(); newtoken=json.dumps(new,ensure_ascii=False).encode(); assert b0.count(oldtoken)==2 and b0.replace(oldtoken,newtoken)==b1
    evidence=ROOT/proposal['existing_search_evidence']['path']; retrieval=read(evidence); assert retrieval['query_count']==len(retrieval['queries'])==5
    for row in retrieval['queries']:
        assert row['terminal_closed']
        for stream in ['stdout','stderr']: assert sha(row[stream+'_utf8'].encode('utf-8'))==row[stream+'_raw_sha256']
    by={x['label']:x for x in retrieval['queries']}; local=by['local_dynamics_inventory']; adapter=by['existing_local_adapters']
    assert local['pid']==38848 and local['exit_code']==1 and local['stderr_utf8']==''
    assert {'AutoSamplingTheory/TechnicalLemmas','AutoSamplingTheory/ExampleCases/ProximalBPS'}<=set(local['command'])
    assert adapter['pid']==15364 and adapter['exit_code']==0 and 'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean' in adapter['command'] and adapter['stdout_utf8']
    assert before['shared_floor_audit']['searched'][1:]==after['shared_floor_audit']['searched'][1:] and 'Mathlib' in before['shared_floor_audit']['searched'][1]
    paths=[P,bp,ap,cp,evidence]
    for row in proposal['unchanged']:
        p=ROOT/row['path']; paths.append(p)
        for k in ['RAW_bytes','RAW_sha256','LF_sha256']: assert pin(p)[k]==row[k]
    pub=read(ROOT/'website/content/publications/pbps-actual-harmonic-flow.json'); assert pub['schema_version']==1 and len(pub['items'])==1
    item=pub['items'][0]; binding=item['bindings'][0]; name=binding['declaration']; lessonraw=read(ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json'); lesson=next(x for x in lessonraw['units'] if x['declaration']==name)
    audit=read(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json'); packet=read(R73/'source-review.packet.json')
    sys.path.insert(0,str(ROOT/'tools')); import astis_publication as publication; import astis_semantic_roundtrip as rt
    payloads=[]; contexts=[]; computations=[]
    for label,cell in [('before',before),('current',read(cp)),('proposed',after)]:
        data={'declarations':{name:SimpleNamespace(source_file=audit['lean']['file'])},'lessons':{name:lesson},'cells':{cell['cell_id']:cell},'audits':{audit['id']:audit}}
        payload=publication.binding_payload(item,binding,data); context=publication.review_context(item,binding,data); bd=publication.binding_digest(item,binding,data); cd=publication.digest(context)
        assert bd==proposal['binding_sha256']==audit['publication_binding_sha256']==packet['publication_binding_sha256'] and cd==proposal['context_sha256']
        assert context==audit['publication_context']==packet['candidate_publication_context']; payloads.append(payload); contexts.append(context); computations.append({'version':label,'binding_sha256':bd,'context_sha256':cd})
    assert payloads[0]==payloads[1]==payloads[2] and contexts[0]==contexts[1]==contexts[2]
    assert rt.semantic_reviewer_packet(audit)==packet and packet['packet_sha256']==proposal['source_packet_sha256']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
    paths += [ROOT/'tools/astis_publication.py',ROOT/'tools/astis_semantic_roundtrip.py',ROOT/'tools/astis_semantic_roundtrip_core.py',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
    pins=[pin(p) for p in dict.fromkeys(paths)]; guard(pins)
    decision={'schema':'astis-independent-frontier-label-repair73-review/v1','verdict':'ACCEPT_EXACT_TWO_STRING_METADATA_REPLACEMENTS','reviewer':'/root/header_math72','proposer':'/root','proposal':pin(P),'canonical_path':proposal['canonical_path'],'approved_before':pin(bp),'approved_after':pin(ap),'current_equals_before_RAW':True,'exhaustive_changes':expected,'exact_RAW_only_two_string_tokens':True,'additional_case_change_disclosed':'Exact -> exact in each string; not byte-prefix-only.','historical_search_evidence':pin(evidence),'historical_local_inventory_PID_EXIT':[38848,1],'historical_local_adapters_PID_EXIT':[15364,0],'native_binding_context':computations,'native_payloads_equal':True,'native_source_packet_exact':True,'source_packet_sha256':packet['packet_sha256'],'actual_reader_PID':os.getpid(),'checked_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'canonical_ledger_Git_writes':False,'Lean_gate_reruns':False,'new_SCI_source_math_VERIFIED_credit':False,'application_precondition':'Root first closes failed exact SCI run; subsequent metadata-only child and fresh independent verification remain required.','inputs':pins,'review_failures':[]}
    save('decision.json',decision); save('finite.inputs.json',{'inputs':pins,'LF_recipe':LF})
    save('full.exact-overlay-inputs.json',{'proposal':proposal,'before_full_exact_RAW_UTF8':b0.decode(),'proposed_full_exact_RAW_UTF8':b1.decode(),'historical_existing_search_rows':[local,adapter]})
    (OWN/'named.review.utf8.md').write_bytes(REVIEW.encode('utf-8'))
    print(json.dumps({'actual_reader_PID':os.getpid(),'verdict':decision['verdict'],'finite_inputs':len(pins),'exact_string_fields':2,'no_gate_rerun':True,'EXIT':0},ensure_ascii=False))
def launch():
    assert not (OWN/'reader.terminal.json').exists(); command=[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'inspect']
    with (OWN/'reader.stdout.txt').open('wb') as out,(OWN/'reader.stderr.txt').open('wb') as err:
        p=subprocess.Popen(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=out,stderr=err); code=p.wait()
    save('reader.terminal.json',{'actual_foreground_PID':p.pid,'terminal_EXIT':code,'observer_PID':os.getpid(),'command':command,'stdout':pin(OWN/'reader.stdout.txt'),'stderr':pin(OWN/'reader.stderr.txt')}); print(json.dumps(read(OWN/'reader.terminal.json'))); return code
def close():
    d=read(OWN/'decision.json'); terminal=read(OWN/'reader.terminal.json'); assert terminal['terminal_EXIT']==0 and terminal['actual_foreground_PID']==d['actual_reader_PID']; guard(d['inputs'])
    save('complete-named-review-decision-input-payload.json',{'named_review':REVIEW,'named_decision_and_input_payload':d,'full_exact_overlay':read(OWN/'full.exact-overlay-inputs.json'),'terminal_receipt':terminal,'writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE})
    run={'schema':'astis-independent-frontier-label-repair73-run/v1','inputs':d['inputs'],'decision':pin(OWN/'decision.json'),'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'reader_terminal':terminal,'final_writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE,'no_new_truth_or_canonical_write':True}; run['run_sha256']=logical(run); save('run.json',run)
    owned=[pin(p) for p in sorted(OWN.iterdir()) if p.is_file() and p.name not in ['native.manifest.json','lease.final.json']]
    save('native.manifest.json',{'owned_files':owned,'exclusions':['native.manifest.json self-reference','lease.final.json final write'],'LF_recipe':LF,'run_sha256':run['run_sha256'],'wholelogicalrun_recipe':RECIPE})
    lease={'status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),'owned_files':len(owned)+2,'run_sha256':run['run_sha256'],'manifest':pin(OWN/'native.manifest.json'),'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'decision':pin(OWN/'decision.json'),'last_write_contract':'This lease is the final owned write; no write after CLOSED; external readonly only.','writer_terminal_EXIT_contract':'Exit0 immediately; actual terminal observed externally.','metadata_only_no_SCI_VERIFIED_credit':True}; save('lease.final.json',lease); print(json.dumps({'writer_PID':os.getpid(),'owned_files':lease['owned_files'],'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json'),'EXIT':0}))
def readonly():
    lease=read(OWN/'lease.final.json'); assert lease['status']=='CLOSED_LAST'
    for n,k in [('native.manifest.json','manifest'),('complete-named-review-decision-input-payload.json','complete_named'),('decision.json','decision')]: assert pin(OWN/n)==lease[k]
    m=read(OWN/'native.manifest.json'); guard(m['owned_files']); actual={p.as_posix() for p in OWN.iterdir() if p.is_file()}; expected={r['path'] for r in m['owned_files']}|{(OWN/'native.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}; assert actual==expected and len(actual)==lease['owned_files']
    latest=(OWN/'lease.final.json').stat().st_mtime_ns; assert all(Path(p).stat().st_mtime_ns<=latest for p in actual)
    run=read(OWN/'run.json'); guard(run['inputs']); assert logical(run)==run['run_sha256']==lease['run_sha256']==m['run_sha256']
    k=ctypes.windll.kernel32; handle=k.OpenProcess(0x1000,False,lease['actual_last_writer_PID']); gone=not bool(handle)
    if handle:
        code=ctypes.c_ulong(); assert k.GetExitCodeProcess(handle,ctypes.byref(code)); k.CloseHandle(handle); gone=code.value!=259
    assert gone; print(json.dumps({'external_readonly_PID':os.getpid(),'terminal_EXIT':0,'writer_PID':lease['actual_last_writer_PID'],'writer_exited':gone,'owned_files':len(actual),'finite_inputs':len(run['inputs']),'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json')}))
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='inspect': inspect()
    elif mode=='launch': raise SystemExit(launch())
    elif mode=='close': close()
    elif mode=='readonly': readonly()
    else: raise ValueError(mode)
