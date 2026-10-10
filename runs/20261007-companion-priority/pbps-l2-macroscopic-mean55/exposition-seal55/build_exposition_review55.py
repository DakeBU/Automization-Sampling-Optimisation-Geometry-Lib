from pathlib import Path
import json,hashlib,datetime,subprocess,struct
root=Path(r'E:\Samplinglib');stage=Path(__file__).parent
head='aa34b6a4ff0f9b24c497472d25ce072ecb8d091a';science='4f71a36d56500fda7f86e8080f695a514913950a'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):
 with path.open('rb') as handle:return handle.read()
def record(path):
 data=read(path);lf=data.replace(b'\r\n',b'\n')
 return {'path':str(path.resolve()),'raw_bytes':len(data),'raw_sha256':sha(data),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def save(name,obj):
 with (stage/name).open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(root)).decode().strip();assert actual==head
pin_paths=['AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','Tests/ProximalBPSL2MacroscopicMean.lean','website/content/declaration_lessons/pbps-l2-macroscopic-mean.json','website/content/publications/pbps-l2-macroscopic-mean.json']
pins={}
for relative in pin_paths:
 data=read(root/relative);gitdata=subprocess.check_output(['git','show',head+':'+relative],cwd=str(root));assert data.replace(b'\r\n',b'\n')==gitdata.replace(b'\r\n',b'\n')
 item=record(root/relative);item['HEAD_git_blob_LF_sha256']=sha(gitdata.replace(b'\r\n',b'\n'));item['physical_lines']=len(data.decode('utf-8').splitlines())
 if relative.endswith('.lean'):
  scientific=subprocess.check_output(['git','show',science+':'+relative],cwd=str(root));assert scientific.replace(b'\r\n',b'\n')==data.replace(b'\r\n',b'\n');item['science_git_blob_LF_sha256']=sha(scientific.replace(b'\r\n',b'\n'))
 pins[relative]=item
old=json.loads(read(stage/'lease.open.json').decode('utf-8'))
for key in ['lesson','publication']:assert record(Path(old['inputs'][key]['path']))['raw_sha256']==old['inputs'][key]['raw_sha256']
dom=json.loads(read(stage/'actual-native-dom-checks55.json').decode('utf-8'))
assert len(dom['details'])==11 and all(x['initially_closed'] for x in dom['details'])
assert dom['details'][7]['exact_statement_match'] and dom['details'][8]['exact_whole_declaration_match']
assert dom['details'][7]['statement_terminal_LF_sha256']=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
visual=root/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55/visual-inspection55'
images={}
for name in ['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png']:
 data=read(visual/name);assert data[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',data[16:24]);assert(width,height)==(1440,1800)
 images[name]={**record(visual/name),'width':width,'height':height,'independently_viewed':True,'tool_display_resize':'view_image supplied1408x1760 display; original1440x1800 bytes preserved and dimension-checked.'}
capture_lease=root/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55/root.desktop-capture55.lease.json';lease=json.loads(read(capture_lease).decode('utf-8'));assert lease['status']=='CLOSED' and lease['exit_code']==0
captures={name:record(visual/name) for name in ['cdp.capture.json','proof.capture.json','cdp.pbps.inspect.json','cdp.branch.inspect.json','proof.proof.inspect.json','proof.proof-late.inspect.json']}
pbpsdom=json.loads(read(visual/'cdp.pbps.inspect.json').decode('utf-8'));assert pbpsdom['closedLeanDetails']==11 and pbpsdom['mathContainers']==8
lesson=json.loads(read(root/'website/content/declaration_lessons/pbps-l2-macroscopic-mean.json').decode('utf-8'))['units'][0];assert len(lesson['steps'])==6
findings=[
 {'slot':'assumptions','status':'ACCEPTED_SCOPED','evidence':'Complete statement/assumptions keep C2, both global positive alpha<=beta Hessian bounds, positive capped eta, genuine same laws and arbitrary uncentered L2 input; finite Hilbert/Borel including rank0 is explicit source-presentation extension.'},
 {'slot':'quantifiers_and_objects','status':'ACCEPTED_SCOPED','evidence':'One S/U/M/T chosen before everyu; M true snd pullback and T actual conditional mean under SAME nu. Every-y S law distinguished from only AE rough means and first/squared fiber integrability.'},
 {'slot':'formula_steps','status':'ACCEPTED_SCOPED','evidence':'Six connected steps: true M pullback, compact-density/closedrange coherence, closedrange inverse T, actual posterior/sourceS and AE fibers, Fubini/orthogonal defect, actual rough-difference/rank0 tests. No missing centering or extra rough moment premise is implied.'},
 {'slot':'rendering','status':'ACCEPTED_SCOPED_WITH_DEBT','evidence':'Four independent image inspections plus actual MJX8 DOM show correct forall,nu,Lambda,norms/Fubini symbols. Initial parsed double-backslash concern is resolved for actual captured renderer; canonical fields untouched. Main equation and step6 require horizontal scroll; steps1-5 are readable, no blanket formula overflow claim.'},
 {'slot':'exact_adjacent_Lean','status':'ACCEPTED_SCOPED','evidence':'Native source section40356bytes has11 initiallyclosed details. Statement fold exactly productionLF statement2525 trimmed bytes and2526withterminalLF. Proof fold is exact full production theorem plus namespace-end13519bytes, not an abbreviated proof. Six substep folds provide named Lean correspondence; executable complete proof remains at adjacent final proof fold.'},
 {'slot':'remaining_boundary','status':'ACCEPTED_SCOPED','evidence':'Visible assumption table/source attribution/boundary preserve B.13 roughgradient/weakH1/Gamma/main/error/cost/composition OPEN. No paper or fullreader completion badge inferred.'},
 {'slot':'graph_truth_separation','status':'ACCEPTED_SCOPED_WITH_DEBT','evidence':'Exact55 declaration focused and COMPILED badge visible. Intro states solid imports/moduleownership are not theoremimplications; dashed references name scans INCOMPLETE. Incidental LogConcaveOn.prod scan visible and labeled; no claim of exhaustive real proof DAG.'}]
debts=[{'id':'main-equation-horizontal-scroll','evidence':'cdp.pbps.png','scope':'Main long equation extends beyond visible content width; horizontal scrollbar present.'},{'id':'step6-horizontal-scroll','evidence':'proof.proof-late.png','scope':'Step6 final constant/variance part clipped at initial right boundary with scrollbar.'},{'id':'dense-prose-and-repeat','evidence':'cdp.pbps.png; proof.proof-late.png','scope':'Long ASCII-heavy complete statement, repeated title/restatement, abbreviations and capitalization slow reading.'},{'id':'very-long-companion-page','evidence':'cdp.pbps.inspect.json','scope':'bodyHeight312366px; this bounded section requires deep scroll/navigation.'},{'id':'graph-incomplete-incidental-scan','evidence':'cdp.branch.png','scope':'Name scan includes incidental LogConcaveOn.prod; explicitly incomplete and dashed reference semantics, not full proof relevance.'},{'id':'stationarity-notation','evidence':'proof.proof.png step4','scope':'S∘nu denotes kernel action on the measure in context; nuS=nu or an explicit convention would make the stationarity formula easier to read.'}]
report={'schema_version':1,'kind':'SCOPED_EXPOSITION_SEAL55','reviewer':'/root/sourcegraph_creator56','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT','review_independence':'Reviewer did not author55 Lean/math/lesson/publication; not source-blind or identity-blind; separate from56 source graph creation and not self-validating56.','integration_HEAD':head,'science_commit':science,'pins':pins,'images':images,'actual_capture_DOM':captures,'capture_closed_lease':record(capture_lease),'actual_native_html_display':record(stage/'actual-native-dom-checks55.json'),'findings':findings,'presentation_debts':debts,'lossless_source_Lean_binding':{'source_ids':['PBPS2609.06905v1 B.1','PBPS2609.06905v1 B.9'],'lean_declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean.actual_macroscopic_l2_mean','source_hypotheses':'Source C2/two Hessian/positive capped eta preserved; finite Hilbert/Borel/rank0 explicitly advertised extension; no caller normalization/operator/kernel/domain certificates.','source_obligations':'Actual uniform fullL2 M/T and AE conditional variance norm defect only.','remaining_boundary':'Roughgradient/weakH1/fullB13/Gamma/dynamics/main/errors/unboundedcost/composition OPEN'},'excluded_claims':['fullreader acceptance','mobile or physical-device acceptance','live deployment','main-branch publication','PURIFIED','whole-mathematics re-verification','full PBPS/SPHMC or four-paper completion','source topology56 admission'],'diagnosed_comparison_history':'Before-EOL and before-namespace-display check JSON retained. Initial rawtext mismatches came from CRLF vs LF and proof fold includes theorem+namespace closure; corrected exact comparisons use explicit LF/outer-whitespace recipe. Not a hidden display repair.','compiler':'NOT_STARTED_CLOSED','canonical_mutations':False,'immutable56_artifacts':'Not modified by this55 review.'}
save('exposition-seal55.json',report)
save('readback55.json',{'schema_version':1,'status':'PASS_PRE_CLOSURE','exact_HEAD':actual,'pin_alignment':'PASS_HEAD_AND_SCIENCE','initial_lesson_publication_raw_alignment':'PASS','four_images_dimension':'1440x1800','11closed_8MJX':'PASS','exact_statement_2526_terminalLF':'PASS','exact_full_proof_display':'PASS','capture_CLOSED_EXIT0':'PASS','verdict':'ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT','scope_exclusions':report['excluded_claims'],'compiler':'NOT_STARTED_CLOSED'})
print(json.dumps({'verdict':report['verdict'],'HEAD':head,'science':science,'source_lines':pins[pin_paths[0]]['physical_lines'],'test_lines':pins[pin_paths[1]]['physical_lines'],'images':4,'closed_folds':11,'mjx':8,'debts':len(debts),'readback':'PASS'}))
