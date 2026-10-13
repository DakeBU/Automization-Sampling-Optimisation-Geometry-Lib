"""Distinct exact metadata-only overlay review. Writes only this new owned directory."""
from __future__ import annotations
import copy, ctypes, datetime, hashlib, json, os, re, subprocess, sys, traceback
from pathlib import Path
from types import SimpleNamespace

ROOT = Path('E:/Samplinglib')
OWN = Path(__file__).resolve().parent
R73 = ROOT / 'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
PROPOSAL = R73 / 'independent-source73/reader-metadata-overlay73/proposal.json'
EXPECTED = '252a9ce488ada4e979db0c845466046cc1a8c22eada30a10b212ccabcd117a6e'
DECL = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'
MODULE = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
LESSON = 'website/content/declaration_lessons/pbps-actual-harmonic-flow.json'
AUDIT = 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json'
REVIEWER = '/root/header_math72'
RECIPE = 'Remove ONLY top-level run_sha256; JSON ensure_ascii=False, sort_keys=True, separators=(comma,colon), allow_nan=False; UTF-8 without BOM/newline; SHA256. Every other field, including nested hash fields, remains.'
LF_RECIPE = 'Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
def logical(v): return sha(canonical({k:x for k,x in v.items() if k != 'run_sha256'}))
def no_duplicates(pairs):
    d = {}
    for k,v in pairs:
        assert k not in d, ('duplicate JSON key', k)
        d[k] = v
    return d
def decode(b): return json.loads(b.decode('utf-8'), object_pairs_hook=no_duplicates)
def read(p): return decode(Path(p).read_bytes())
def pin(p):
    p = Path(p); b = p.read_bytes(); lf = b.replace(b'\r\n', b'\n')
    return {'path':p.as_posix(), 'RAW_bytes':len(b), 'RAW_sha256':sha(b), 'LF_bytes':len(lf), 'LF_sha256':sha(lf), 'LF_recipe':LF_RECIPE}
def save(name,v):
    assert not (OWN/'lease.final.json').exists(), 'CLOSED directory is immutable'
    p = OWN / name; p.parent.mkdir(parents=True, exist_ok=True)
    assert OWN in p.resolve().parents, p
    p.write_bytes((json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode('utf-8'))
def save_text(name,s):
    assert not (OWN/'lease.final.json').exists(), 'CLOSED directory is immutable'
    p=OWN/name; assert OWN in p.resolve().parents
    p.write_bytes(s.encode('utf-8'))
def diff(a,b,p=''):
    if type(a) is not type(b): return [{'pointer':p, 'before':a, 'after':b}]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            q=p+'/'+k.replace('~','~0').replace('/','~1')
            if k not in a or k not in b: out.append({'pointer':q,'key_presence_change':True})
            else: out += diff(a[k], b[k], q)
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [{'pointer':p,'array_length_change':True}]
        return [row for i,(x,y) in enumerate(zip(a,b)) for row in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [{'pointer':p,'before':a,'after':b}]
def value_at(v,p):
    for k in p.split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~'); v=v[int(k)] if isinstance(v,list) else v[k]
    return v
def guard(rows):
    for x in rows: assert pin(x['path'])==x, ('input drift',x['path'])

def check():
    assert not (OWN/'checks.result.json').exists(), 'Do not overwrite prior check evidence'
    assert pin(PROPOSAL)['RAW_sha256']==EXPECTED
    proposal=read(PROPOSAL)
    assert proposal['schema']=='astis-independent-reader-process-metadata-proposal73/v1'
    assert proposal['author']!=REVIEWER and proposal['author']=='/root/independent_primary69'
    assert proposal['status']=='PROPOSED_AWAITING_DISTINCT_REPAIR_REVIEW'
    assert proposal['exact_field_count']==proposal['exact_file_count']==len(proposal['changes'])==2
    paths=[PROPOSAL]; rows=[]; full_inputs={}; versions=[]
    expected_paths=[('website/content/publications/pbps-actual-harmonic-flow.json','/items/0/purification/dead_code_audit'),('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json','/purification/dead_code_audit')]
    for n,(change,(canonical_path,pointer)) in enumerate(zip(proposal['changes'],expected_paths)):
        assert change['canonical_path']==canonical_path and change['JSON_pointer']==pointer
        before=ROOT/change['before']['path']; proposed=ROOT/change['proposed']['path']; current=ROOT/canonical_path
        paths += [before,proposed,current]
        b0,b1,bc=before.read_bytes(),proposed.read_bytes(),current.read_bytes()
        for tag,p in [('before',before),('proposed',proposed)]:
            pp=pin(p); expected=change[tag]
            for k in ('RAW_bytes','RAW_sha256','LF_sha256'): assert pp[k]==expected[k],(n,tag,k)
        assert b0==bc, ('canonical current not exact approved-before',canonical_path)
        j0,j1=decode(b0),decode(b1)
        changes=diff(j0,j1)
        expected_diff=[{'pointer':pointer,'before':change['old_value'],'after':change['proposed_value']}]
        assert changes==expected_diff,(canonical_path,changes)
        assert value_at(j0,pointer)==change['old_value'] and value_at(j1,pointer)==change['proposed_value']
        old=json.dumps(change['old_value'],ensure_ascii=False).encode('utf-8')
        new=json.dumps(change['proposed_value'],ensure_ascii=False).encode('utf-8')
        assert b0.count(old)==1 and b0.replace(old,new,1)==b1, 'RAW changes beyond one exact JSON string token'
        assert change['old_value']=='Pending implementation; one actual deterministic theorem.'
        assert j0['items'][0]['purification']['status']==j1['items'][0]['purification']['status']=='pending' if n==0 else j0['purification']['status']==j1['purification']['status']=='pending'
        rows.append({'canonical_path':canonical_path,'JSON_pointer':pointer,'before':pin(before),'after':pin(proposed),'canonical_current':pin(current),'exhaustive_JSON_diff':changes,'exact_RAW_single_string_token_replacement':True,'other_RAW_bytes_unchanged':True})
        versions.append((j0,j1,decode(bc)))
        full_inputs[before.as_posix()]=b0.decode('utf-8'); full_inputs[proposed.as_posix()]=b1.decode('utf-8')
    pub_before,pub_proposed,pub_current=versions[0]
    cell_before,cell_proposed,cell_current=versions[1]
    assert pub_before['schema_version']==pub_proposed['schema_version']==1
    assert len(pub_before['items'])==len(pub_proposed['items'])==1
    assert cell_before['schema_version']==cell_proposed['schema_version']==3
    item=pub_current['items'][0]; binding=item['bindings'][0]
    assert len(item['bindings'])==1 and binding['declaration']==DECL
    lesson_json=read(ROOT/LESSON); units=lesson_json['units']
    lesson=[x for x in units if x['declaration']==DECL]
    assert lesson_json['schema_version']==1 and len(lesson)==1
    audit=read(ROOT/AUDIT); anonymous=read(R73/'anonymous-decoder/parent-packet.json'); source_packet=read(R73/'source-review.packet.json')
    assert audit['lean']['declaration']==DECL and audit['lean']['file']==MODULE
    assert source_packet['roles']['formalizer']!=REVIEWER and source_packet['roles']['blind_decoder']!=REVIEWER
    paths += [ROOT/MODULE,ROOT/LESSON,ROOT/AUDIT,R73/'anonymous-decoder/parent-packet.json',R73/'source-review.packet.json',R73/'anonymous.lean-context73.json',R73/'anonymous.decoder.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
    m=R73/'independent-math73'; closed=read(m/'lease.final.json'); md=read(m/'decision.json'); mr=read(m/'run.json')
    assert closed['status']=='CLOSED_LAST' and closed['owned_files']==39
    assert logical(mr)==mr['run_sha256']==closed['run_sha256']
    assert md['verdict']=='ACCEPTED_MATHEMATICS_ONLY' and md['compiled_independently'] and md['fresh_Lean_terminal_EXIT']==0
    assert md['candidate_module']['RAW_sha256']==pin(ROOT/MODULE)['RAW_sha256']=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
    assert pin(m/'decision.json')['RAW_sha256']==closed['decision']['RAW_sha256']
    assert pin(m/'native.manifest.json')['RAW_sha256']==closed['manifest']['RAW_sha256']
    module_text=(ROOT/MODULE).read_text(encoding='utf-8')
    declarations=re.findall(r'(?m)^(private\s+)?(def|theorem|lemma|axiom)\s+(\w+)',module_text)
    assert declarations==[('private ','def','actual_harmonic_flow_statement'),('','theorem','actual_harmonic_flow_laws')]
    assert len(module_text.splitlines())==178
    paths += [m/'decision.json',m/'lease.final.json',m/'run.json',m/'native.manifest.json']
    sys.path.insert(0,str(ROOT/'tools'))
    import astis_publication as publication
    import astis_semantic_roundtrip as roundtrip
    assert Path(publication.__file__).resolve()==(ROOT/'tools/astis_publication.py').resolve()
    data={'declarations':{DECL:SimpleNamespace(source_file=MODULE)},'lessons':{DECL:lesson[0]},'cells':{cell_current['cell_id']:cell_current},'audits':{audit['id']:audit}}
    all_payloads=[]; all_contexts=[]; computations=[]
    for name,pub,cell in [('before',pub_before,cell_before),('current',pub_current,cell_current),('proposed',pub_proposed,cell_proposed)]:
        d=dict(data); d['cells']={cell['cell_id']:cell}; i=pub['items'][0]; b=i['bindings'][0]
        payload=publication.binding_payload(i,b,d); context=publication.review_context(i,b,d)
        bd=publication.binding_digest(i,b,d); cd=publication.digest(context)
        assert bd==sha(canonical(payload)) and cd==sha(canonical(context))
        assert bd==proposal['publication_binding_sha256_unchanged']==audit['publication_binding_sha256']==source_packet['publication_binding_sha256']
        assert cd==proposal['review_context_canonical_sha256_unchanged']
        assert context==audit['publication_context']==source_packet['candidate_publication_context']
        all_payloads.append(payload); all_contexts.append(context)
        computations.append({'version':name,'publication_binding_sha256':bd,'review_context_canonical_sha256':cd})
    assert all_payloads[0]==all_payloads[1]==all_payloads[2] and all_contexts[0]==all_contexts[1]==all_contexts[2]
    assert roundtrip.semantic_reviewer_packet(audit)==source_packet
    assert roundtrip.decoder_packet(audit)==anonymous
    source_core={k:v for k,v in source_packet.items() if k!='packet_sha256'}
    anonymous_core={k:v for k,v in anonymous.items() if k!='packet_sha256'}
    assert roundtrip.sha256_json(source_core)==source_packet['packet_sha256']
    assert roundtrip.sha256_json(anonymous_core)==anonymous['packet_sha256']
    paths += [ROOT/'tools/astis_publication.py',ROOT/'tools/astis_semantic_roundtrip.py',ROOT/'tools/astis_semantic_roundtrip_core.py',ROOT/'tools/astis_frontier_cells.py',Path(sys.modules['astis_site'].__file__).resolve(),ROOT/'docs/theorem-publication-protocol.md',ROOT/'docs/proof-digestion-protocol.md']
    pins=[pin(p) for p in dict.fromkeys(paths)]
    guard(pins)
    result={'schema':'astis-independent-exact-reader-metadata-repair73/v1','verdict':'ACCEPT_EXACT_METADATA_ONLY_PROPOSAL','reviewer':REVIEWER,'proposer':proposal['author'],'distinct_from_proposer_and_source_reviewer':True,'proposal':pin(PROPOSAL),'approved_rows':rows,'exact_changed_fields':2,'exact_changed_files':2,'bindings':computations,'native_binding_payload_equal':True,'native_review_context_equal':True,'native_semantic_reviewer_packet_exact':True,'native_anonymous_packet_exact':True,'source_packet_sha256':source_packet['packet_sha256'],'anonymous_packet_sha256':anonymous['packet_sha256'],'publication_purification_status':'pending','cell_purification_status':'pending','prior_math_CLOSED39_preserved':pin(m/'lease.final.json'),'prior_math_compile_reused_not_rerun':{'actual_Lean_PID':md['fresh_foreground_Lean_PID'],'terminal_EXIT':md['fresh_Lean_terminal_EXIT'],'module':pin(ROOT/MODULE)},'declaration_inventory':declarations,'checked_parent':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'actual_check_PID':os.getpid(),'mathematical_repair':False,'new_mathematics_credit':False,'new_source_fidelity_credit':False,'PURIFIED':False,'ExpositionSeal':False,'VERIFIED':False,'canonical_Git_ledger_writes':False,'Lean_or_fullgates_rerun':False,'inputs':pins,'failure_evidence':[]}
    result['failure_evidence']=[{'kind':'VERIFIER_SETUP_PATH_ERROR_NOT_MATHEMATICS','actual_foreground_PID':48776,'terminal_EXIT':1,'reason':'After native diff/binding/packet assertions succeeded, input pin enumeration used nonexistent website/scripts/astis_site.py; corrected to actual imported module __file__.','receipt':pin(OWN/'check.terminal.json'),'stderr':pin(OWN/'check.stderr.txt'),'exact_script':pin(OWN/'review73.setup-path-negative.py')}]
    save('checks.result.json',result)
    save('finite.inputs.json',{'LF_recipe':LF_RECIPE,'inputs':pins})
    save('reviewed.full-input-and-native-payload.json',{'proposal':proposal,'full_before_and_proposed_RAW_UTF8':full_inputs,'native_binding_payload_common_to_before_current_proposed':all_payloads[0],'native_review_context_common_to_before_current_proposed':all_contexts[0]})
    print(json.dumps({'actual_check_PID':os.getpid(),'verdict':result['verdict'],'changed_fields':2,'input_files':len(pins),'binding':computations[0]['publication_binding_sha256'],'context':computations[0]['review_context_canonical_sha256'],'EXIT':0},ensure_ascii=False))

def launch():
    assert not (OWN/'lease.final.json').exists()
    assert not (OWN/'check2.terminal.json').exists(), 'Do not overwrite a previous terminal receipt'
    command=[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'check']
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    with (OWN/'check2.stdout.txt').open('wb') as out,(OWN/'check2.stderr.txt').open('wb') as err:
        p=subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err)
        code=p.wait()
    save('check2.terminal.json',{'command':command,'actual_foreground_PID':p.pid,'terminal_EXIT':code,'observer_PID':os.getpid(),'stdout':pin(OWN/'check2.stdout.txt'),'stderr':pin(OWN/'check2.stderr.txt')})
    print(json.dumps(read(OWN/'check2.terminal.json'),ensure_ascii=False))
    return code

REVIEW = '''# Independent exact reader-metadata repair73 review

Decision: ACCEPT the exact proposal RAW SHA256 252a9ce488ada4e979db0c845466046cc1a8c22eada30a10b212ccabcd117a6e, for the two specified process metadata strings only. Reviewer /root/header_math72 differs from proposer/source reviewer /root/independent_primary69 and from the canonical proving writer. This is a metadata repair review; it gives no new mathematics, source fidelity, PURIFIED, Exposition Seal or VERIFIED credit.

I read all full before/proposed UTF-8 RAWs with duplicate-key rejection. The actual publication schema is schema_version1 with one items element and one binding; the frontier cell is schema_version3. Current canonical bytes equal the exact approved-before bytes. Exhaustive recursive JSON comparison finds precisely /items/0/purification/dead_code_audit in website/content/publications/pbps-actual-harmonic-flow.json and /purification/dead_code_audit in research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json. No key, array, type, number, boolean or other string changes. Independently, replacing the one JSON-quoted old string token in each complete before RAW gives the complete proposed RAW byte for byte, including formatting, line endings and final newline.

Both old values are "Pending implementation; one actual deterministic theorem." Both new values are "One public deterministic theorem uses the complete private literal proposition definition; the literal is a specification, not a mathematical provider. The six original callers are retained. No retired candidate declaration occurs in this178-line module. This scoped audit grants neither an Exposition Seal nor PURIFIED admission."

This removes stale pending-implementation wording after the already CLOSED39 independent mathematics review. That unchanged review freshly compiled the exact module SHA506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c (Lean PID39960 EXIT0); I do not rerun its mathematics or compiler. The present exact text inventory has only the private literal Prop and the public deterministic theorem in178 lines. The full six original caller binders, private literal and proof are exact unchanged module bytes. The proposed words claim no new scope or theorem.

I called the native tools/astis_publication.py binding_payload, binding_digest and review_context directly, supplying the exact module declaration, exact authored lesson and actual current/before/proposed publication and cell data. No broad scan, publication validation, source review, Lean build or site aggregate ran. Both native payloads are exactly equal for before/current/proposed, beyond merely equal digests. Binding SHA256 remains627cae79b09fa7c73f90020fcc85081a9ba134ac778d47871f3a10f4a18250ea; review-context canonical SHA256 remains1722badb9a3f7ec13118dcb9017be0a02276777610ce582769f436bee2bd0370. Native binding code includes module, toolchain, lake manifest, source, statement, formulae, assumptions, obligations, exact lesson and binding fields. Publication purification is absent; frontier cell metadata is not consumed. Review context additionally removes prior assumption-delta classifications and lesson boundary fields as specified by native code. Only the two excluded process metadata strings change.

The recomputed context equals the existing audit publication_context and source packet candidate_publication_context. Native semantic_reviewer_packet reproduces the current full source packet; native decoder_packet reproduces the current full anonymous packet. Both logical packet hashes are recomputed. Exact RAW/LF pins bind the source audit, anonymous approved context, decoder artifact, packets, module, lesson, assumptions in the unchanged JSON objects, native tools, protocols and prior CLOSED39 lease/decision/run/manifest. No audit/source decision is rewritten or re-decided. No source acquisition or source mathematics review is performed here.

Both purification.status values stay pending. Source graph/coverage, statement seal, original assumptions, all six exact lesson BODY spans/formulas, source text, blind reconstruction, publication binding/context and every boundary remain unchanged. Actual stochastic H_y, terminal kernel, actual K/r_rho, B27/B28, invariance, nonexplosion, full PBPS/SPHMC results, errors/caps, costs, composition, global Goal, integration and live publication are not admitted. Only the root canonical writer may adopt this separately reviewed exact overlay later.

The first setup check PID48776 exited1 only because input pin enumeration named a nonexistent website/scripts/astis_site.py after the diff/binding/packet assertions had passed. Its exact script, terminal receipt and stderr are retained. The pin now uses the actual imported module path. This is a verifier setup-path failure, not negative mathematical or proposal evidence. No math or fullgate was repeated.

The complete named payload carries this review, the decision, exact input list, all four full before/proposed RAW UTF-8 texts, common native binding/context payloads and the actual terminal check receipt. The finite manifest separately pins every owned output. The canonical whole-logical-run recipe removes only the top-level run_sha256; nested hashes and all other fields remain. lease.final.json is the final owned write, CLOSED_LAST; a later process performs read-only verification and reports terminal EXIT0 externally.
'''

def close():
    assert not (OWN/'lease.final.json').exists()
    result=read(OWN/'checks.result.json'); terminal=read(OWN/'check2.terminal.json')
    assert terminal['terminal_EXIT']==0 and terminal['actual_foreground_PID']==result['actual_check_PID']
    assert (OWN/'check2.stderr.txt').read_bytes()==b''
    guard(result['inputs'])
    decision={k:v for k,v in result.items() if k!='inputs'}
    decision['minimum_repair']=None
    decision['scope']='Approve only exact two metadata strings. Adoption remains the canonical writer action.'
    save('decision.json',decision); save_text('independent-reader-metadata-repair73.utf8.md',REVIEW)
    complete={'schema':'astis-complete-named-reader-metadata-repair73/v1','named_review':REVIEW,'named_decision':decision,'complete_finite_input_payload':read(OWN/'finite.inputs.json'),'full_reviewed_RAW_and_native_binding_payload':read(OWN/'reviewed.full-input-and-native-payload.json'),'terminal_receipt':terminal,'closure_writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE}
    save('complete-named-review-decision-input-payload.json',complete)
    run={'schema':'astis-independent-reader-metadata-repair73-run/v1','reviewer':REVIEWER,'proposal':pin(PROPOSAL),'inputs':result['inputs'],'decision':pin(OWN/'decision.json'),'named_review':pin(OWN/'independent-reader-metadata-repair73.utf8.md'),'complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload.json'),'checks_terminal':terminal,'writer_PID':os.getpid(),'wholelogicalrun_recipe':RECIPE,'canonical_writes':False,'new_math_source_PURIFIED_ExpositionSeal_VERIFIED_credit':False,'failure_evidence':result['failure_evidence']}
    run['run_sha256']=logical(run); save('run.json',run)
    owned=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ('native.manifest.json','lease.final.json')]
    manifest={'schema':'astis-finite-owned-RAW-LF-manifest/v1','owned_root':OWN.as_posix(),'LF_recipe':LF_RECIPE,'owned_files':owned,'exclusions':['native.manifest.json (self-reference)','lease.final.json (final write)'],'wholelogicalrun_recipe':RECIPE,'run_sha256':run['run_sha256']}
    save('native.manifest.json',manifest)
    lease={'status':'CLOSED_LAST','reviewer':REVIEWER,'actual_last_writer_PID':os.getpid(),'writer_terminal_EXIT_contract':'exit0 immediately; external tool observes actual terminal EXIT','last_write_contract':'lease.final.json is the final owned write; no writes after CLOSED; external read-only verification only.','owned_files':len(owned)+2,'run_sha256':run['run_sha256'],'manifest':pin(OWN/'native.manifest.json'),'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'decision':pin(OWN/'decision.json'),'proposal':pin(PROPOSAL),'new_math_source_PURIFIED_ExpositionSeal_VERIFIED_credit':False,'canonical_Git_ledger_writes':False}
    save('lease.final.json',lease)
    print(json.dumps({'actual_writer_PID':os.getpid(),'terminal_EXIT_contract':0,'owned_files':lease['owned_files'],'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json')},ensure_ascii=False))

def readonly():
    lease=read(OWN/'lease.final.json'); assert lease['status']=='CLOSED_LAST'
    assert pin(OWN/'native.manifest.json')==lease['manifest']
    assert pin(OWN/'complete-named-review-decision-input-payload.json')==lease['complete_named']
    assert pin(OWN/'decision.json')==lease['decision']
    manifest=read(OWN/'native.manifest.json')
    for row in manifest['owned_files']: assert pin(row['path'])==row, ('owned hash mismatch',row['path'])
    actual={p.as_posix() for p in OWN.rglob('*') if p.is_file()}
    expected={x['path'] for x in manifest['owned_files']}|{(OWN/'native.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}
    assert actual==expected and len(actual)==lease['owned_files']
    latest=(OWN/'lease.final.json').stat().st_mtime_ns
    assert all(Path(p).stat().st_mtime_ns<=latest for p in actual)
    run=read(OWN/'run.json'); assert logical(run)==run['run_sha256']==lease['run_sha256']==manifest['run_sha256']
    guard(run['inputs']); assert pin(PROPOSAL)==lease['proposal']
    handle=ctypes.windll.kernel32.OpenProcess(0x1000,False,lease['actual_last_writer_PID'])
    writer_exited=not bool(handle)
    if handle:
        code=ctypes.c_ulong(); assert ctypes.windll.kernel32.GetExitCodeProcess(handle,ctypes.byref(code)); ctypes.windll.kernel32.CloseHandle(handle)
        writer_exited=code.value!=259
    assert writer_exited, 'final writer still running'
    print(json.dumps({'actual_external_readonly_PID':os.getpid(),'external_readonly':True,'writer_PID':lease['actual_last_writer_PID'],'writer_exited':writer_exited,'owned_files':len(actual),'finite_inputs':len(run['inputs']),'wholelogicalrun_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json'),'terminal_EXIT':0},ensure_ascii=False))

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='check': check()
    elif mode=='launch': raise SystemExit(launch())
    elif mode=='close': close()
    elif mode=='readonly': readonly()
    else: raise ValueError(mode)
