from common import *
import re
q=J(P/'inputs.before.json');[matches(x) for x in q['mathematical_freeze']];assert path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0';assert next(x for x in J(ROOT/'lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
env=os.environ.copy();inherited=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PYTHONDONTWRITEBYTECODE']='1'
lake='C:/Users/admin/.elan/bin/lake.EXE';version=invoke('toolchain-version',[lake,'env','lean','--version'],env);assert version['exit_code']==0 and '4.33.0' in path(version['stdout']['path']).read_text()
pre=[pin(x['path']) for x in q['mathematical_freeze']];actual=invoke('compiler',[lake,'build','Tests.ProximalBPSRealDefectRootUnique'],env);assert actual['exit_code']==0
text=path(actual['stdout']['path']).read_text(encoding='utf8');assert 'Build completed successfully (3918 jobs).' in text
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",text);assert len(axioms)>=2,axioms
for n,a in axioms:assert {x.strip() for x in a.split(',')}=={'propext','Classical.choice','Quot.sound'},(n,a)
assert 'sorryAx' not in text
post=[matches(x) for x in pre];W(P/'compiler.json',dict(checked_commit=SCI,actual_foreground_compiler=actual,toolchain_version=version,ELAN_TOOLCHAIN_inherited_removed=inherited is not None,ELAN_TOOLCHAIN_child_unset=True,environment=dict(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'),repo_pinned_mathlib='db584cd6d46c92f209a44c0f1c829460d327499d',before=pre,after=post,focused_jobs=3918,focused_invocations=1,forced_rebuild=False,standard3_prints=[dict(declaration=n,actual_axioms=[x.strip() for x in a.split(',')]) for n,a in axioms],anonymous_Test='Actual complete original-input consumer compiled in this focused build; no separate anonymous-example axiom print invented',resources='Actual compiler/version children EXIT0/CLOSED; no other compiler started'))
print('COMPILER_CLOSED',actual['actual_PID'],'EXIT0','3918 jobs','standard3',len(axioms))
