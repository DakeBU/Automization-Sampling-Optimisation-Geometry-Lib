import hashlib, json, os, subprocess, sys
from pathlib import Path

OUT = Path('E:/Samplinglib/.astis/decoder-60/independent')
BASE = OUT.parent
def canonical(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def sha(v): return hashlib.sha256(v).hexdigest()
def load(name): return json.loads((OUT/name).read_bytes())
def write(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def readback(args):
    result = subprocess.run([sys.executable, '-X', 'utf8', str(OUT/'readback.py')] + args, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Readback failed, lease remains OPEN')
    return {'exit_code':result.returncode, 'stdout':json.loads(result.stdout), 'stderr':result.stderr, 'exit_capture':'subprocess.run.returncode; child PID reported by os.getpid in the child itself'}

first = readback([])
run = {
    'schema_version':1,
    'decoder':'/root/anonymous_decoder60',
    'synthesis_first_verdict':'PASS for independent reconstruction from the anonymous propositions and approved definitions. Reconstruction evidence only; no source fidelity judgment was attempted or supported.',
    'source_text_visible':False,
    'source_identity_visible':False,
    'compiler_started':False,
    'repo_bodies_history_audits_or_memory_read':False,
    'foreground_only':True,
    'actual_input_manifest':load('input-manifest.json'),
    'payload_sha256':load('decoder-payload.json')['payload_sha256'],
    'payload_sha256_recipe':load('decoder-payload.json')['payload_sha256_recipe'],
    'run_sha256_recipe':'SHA256(UTF8(JSON sorted keys, compact separators, ensure_ascii=false) of this entire native run object minus ONLY its top-level run_sha256 field)',
    'generation_pid':load('generation-record.json')['pid'],
    'generation_exit_code':0,
    'generation_exit_evidence':'Foreground exec_command returned exit_code=0 for generate.py; PID is the generator own os.getpid value.',
    'first_readback':first,
    'finalizer_pid':os.getpid(),
    'outputs':[{'filename':n,'raw_sha256':sha((OUT/n).read_bytes())} for n in ['decoded0.json','decoded1.json','input-manifest.json','initial-lease.json','decoder-payload.json','generation-record.json']],
    'boundaries':['No source text, identities, implementation bodies, history, previous audits, compiler, memory or other chats were inspected.','All operator/kernel properties are reconstructed at the exact displayed existential/universal and AE/every-state scope.','No source fidelity or theorem completion claim.']
}
run['run_sha256'] = sha(canonical(run))
write(OUT/'run.json',run)
final = readback(['--final'])
readback_record = {'decoder':'/root/anonymous_decoder60','final_readback':final,'first_readback_pid':first['stdout']['pid'],'first_readback_exit_code':first['exit_code'],'run_sha256':run['run_sha256'],'source_text_visible':False,'source_identity_visible':False}
write(OUT/'final-readback.json',readback_record)
assert load('final-readback.json') == readback_record
assert sha(canonical({k:v for k,v in load('run.json').items() if k!='run_sha256'})) == run['run_sha256']
lease = json.loads((OUT/'initial-lease.json').read_bytes())
lease.update({'status':'CLOSED','decoder':'/root/anonymous_decoder60','result':'Independent reconstruction complete; source fidelity unassessed','run_path':str(OUT/'run.json'),'run_sha256':run['run_sha256'],'final_readback_path':str(OUT/'final-readback.json'),'final_readback_raw_sha256':sha((OUT/'final-readback.json').read_bytes()),'final_readback_pid':final['stdout']['pid'],'final_readback_exit_code':final['exit_code'],'first_readback_pid':first['stdout']['pid'],'first_readback_exit_code':first['exit_code'],'closed_by_pid':os.getpid(),'source_text_visible':False,'source_identity_visible':False,'compiler_started':False})
# Last filesystem mutation: close the neutral lease only after successful readback and captured process exit.
write(BASE/'lease.json',lease)
print(json.dumps({'run_sha256':run['run_sha256'],'first_readback_pid':first['stdout']['pid'],'first_readback_exit_code':first['exit_code'],'final_readback_pid':final['stdout']['pid'],'final_readback_exit_code':final['exit_code'],'lease_status':'CLOSED','decoder':'/root/anonymous_decoder60'},ensure_ascii=False))
