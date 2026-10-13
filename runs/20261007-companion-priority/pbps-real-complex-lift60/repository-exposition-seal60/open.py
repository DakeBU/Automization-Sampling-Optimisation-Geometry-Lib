import pathlib,json,hashlib,os,subprocess
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'repository-exposition-seal60'
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(l).hexdigest())
paths=[R/x for x in ['integration.notes.json','root.exact-verification60.adoption.json','commit-observer-split.json','visual.inspection.json','math-freeze.json','exact-science-verification/run.json','exact-science-verification/lease.json','exact-science-verification/receipt.json','exact-science-verification/before-admin-mappings.json','source-review60/run.json','source-review60/lease.json','anonymous-decoder/run.json','anonymous-decoder/input-lease.json']]
paths += [p for p in (R/'integration60').glob('*/receipt.json') if p.parent.name!='commit-integration60']
paths += list((R/'integration60/visual60').iterdir())
paths += [ROOT/('website/content/'+folder+'/'+slug+'.json') for folder in ['declaration_lessons','theorem_publications'] for slug in ['l2-real-complex-positive-lift','pbps-positive-defect-complex-lift'] if (ROOT/('website/content/'+folder+'/'+slug+'.json')).exists()]
paths += [ROOT/'research-wiki/frontier-cells'/(x+'.json') for x in ['ASTIS-SHARED-l2-real-complex-positive-lift','ASTIS-SW-PBPS-positive-defect-complex-lift']]
paths += [ROOT/'research-wiki/semantic-roundtrip/audits'/(x+'.json') for x in ['ASTIS-RT-20261008-L2PositiveComplexLift','ASTIS-RT-20261008-PBPSPositiveDefectComplexLift']]
pins=[pin(p) for p in paths if p.is_file()];q=dict(actual_PID=os.getpid(),checked_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),artifacts=pins,count=len(pins),timing='Actual qualified bytes pinned before semantic reading or image inspection in this review')
(D/'inputs.open.json').write_bytes((json.dumps(q,indent=2)+'\n').encode());(D/'lease.open.json').write_bytes((json.dumps(dict(status='OPEN',actor='/root/whole_math52/repository-exposition60',actual_opener_PID=os.getpid(),compiler='NOT_STARTED',scope='Reader-only scoped repository/exposition integration review60'),indent=2)+'\n').encode());print(json.dumps(dict(status='INPUTS_OPEN_PINNED',count=len(pins),PID=os.getpid())),flush=True)
