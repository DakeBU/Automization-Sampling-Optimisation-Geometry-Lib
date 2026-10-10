from common import *
import shutil
assert head()==SCI
env=os.environ.copy(); inherited=env.pop('ELAN_TOOLCHAIN',None); env['LEAN_NUM_THREADS']='2'; env['PYTHONUTF8']='1'; env['PYTHONDONTWRITEBYTECODE']='1'
W(P/'compiler.inputs.before.json',dict(actual_wrapper_PID=os.getpid(),checked_commit=head(),ELAN_TOOLCHAIN_removed=inherited is not None,LEAN_NUM_THREADS='2',PYTHONUTF8='1',source_inputs=[matches(x) for x in J(R/'math-freeze.json')['inputs']],source_input_timing='All actual27 original raw/LF immediately before child invocation'))
tool=invoke('toolchain',[shutil.which('lake'),'env','lean','--version'],env); assert tool['exit_code']==0
assert '4.33.0' in (P/'toolchain.stdout.log').read_text()
manifest=J(ROOT/'lake-manifest.json'); mathlib=next(x for x in manifest['packages'] if x['name']=='mathlib'); assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
W(P/'toolchain.pin.json',dict(toolchain=pin(ROOT/'lean-toolchain'),manifest=pin(ROOT/'lake-manifest.json'),mathlib=mathlib,observed_toolchain_status=pin(P/'toolchain.status.json')))
build=invoke('focused',['C:/Users/admin/.elan/bin/lake.exe','build','Tests.ProximalBPSRealDefectRoot'],env)
post=[matches(x) for x in J(R/'math-freeze.json')['inputs']]; W(P/'compiler.inputs.after.json',dict(checked_commit=head(),inputs=post,build=build))
assert build['exit_code']==0; log=(P/'focused.stdout.log').read_text(encoding='utf8'); assert 'sorryAx' not in log
axioms=[l for l in log.splitlines() if 'depends on axioms' in l]; assert len(axioms)==2 and all('[propext, Classical.choice, Quot.sound]' in l for l in axioms),axioms
W(P/'compiler.json',dict(status='PASS',checked_commit=SCI,focused=build,source_pre=pin(P/'compiler.inputs.before.json'),source_post=pin(P/'compiler.inputs.after.json'),toolchain=pin(P/'toolchain.pin.json'),axiom_lines=axioms,compiler='CLOSED_EXIT0',one_nonforced_invocation=True,scope='Focused target only; full mandatory root and aggregate deferred to serialized integration'))
print('FOCUSED_CLOSED',build['actual_PID'],build['exit_code'],axioms)
