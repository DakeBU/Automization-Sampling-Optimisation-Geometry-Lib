from pathlib import Path
R=Path('E:/Samplinglib');r=Path(__file__).parent;pre=r.parent/'pbps-conditional-next-wait-preread88'
s=(pre/'header88.proposed.lean').read_text(encoding='utf8')
s=s.replace('/-! Prospective header88:', '/-! Actual conditional survival:')
prop=s.split('private def actual_conditional_next_wait_survival_statement',1)[1].split('\n#check',1)[0]
binders=prop.split(' : Prop :=',1)[0]
lets=prop.split(' : Prop :=\n',1)[1].split('    ∀ y xRef',1)[0]
target='    ∀ y xRef'+prop.split('    ∀ y xRef',1)[1]
theorem='''
set_option maxHeartbeats 1000000 in
/-- Conditional next-wait survival for the actual finite stopped history.
The duration is a Borel function of that entire history. No normalization or
strict positivity of the history event is required. -/
theorem actual_conditional_next_wait_survival'''+binders+''' :
    actual_conditional_next_wait_survival_statement hα hαβ hV hH hη hβη := by
  classical
'''+''.join(line[2:]+'\n' for line in lets.rstrip().splitlines())+'  change\n'+''.join(line[2:]+'\n' for line in target.rstrip().splitlines())+'\n'
body=r/'proof88.body.txt'
out=s.split('\n#check',1)[0]+'\n'+theorem+body.read_text(encoding='utf8')+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival\n'
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean'
p.write_text(out,encoding='utf8',newline='\n')
print(p,len(out.encode()))
