"""Actual bounded local-import fake-closure scan; complements Lean axiom output."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess
R=Path.cwd()
E=Path(__file__).resolve().parent
seeds=['AutoSamplingTheory/ExampleCases/GaussianComplexity/MixtureDensities.lean','Tests/GaussianComplexityMixtureDensities.lean']
seen={}
queue=list(seeds)
while queue:
    name=queue.pop(0)
    if name in seen: continue
    p=R/name
    data=p.read_bytes()
    text=data.decode()
    seen[name]={'sha256':hashlib.sha256(data).hexdigest(),'lines':len(text.splitlines())}
    for mod in re.findall(r'^import\s+(AutoSamplingTheory(?:\.[A-Za-z0-9_]+)+)\s*$',text,re.M):
        q=mod.replace('.','/')+'.lean'
        if q not in seen: queue.append(q)
def code_only(s):
    out=[]; i=0; depth=0; in_string=False
    while i<len(s):
        if depth:
            if s.startswith('/-',i): depth+=1; i+=2
            elif s.startswith('-/',i): depth-=1; i+=2
            else:
                out.append('\n' if s[i]=='\n' else ' '); i+=1
        elif in_string:
            if s[i]=='\\': out.extend('  '); i+=2
            elif s[i]=='"': in_string=False; out.append(' '); i+=1
            else: out.append('\n' if s[i]=='\n' else ' '); i+=1
        elif s.startswith('/-',i): depth=1; out.extend('  '); i+=2
        elif s.startswith('--',i):
            j=s.find('\n',i); j=len(s) if j<0 else j
            out.extend(' '*(j-i)); i=j
        elif s[i]=='"': in_string=True; out.append(' '); i+=1
        else: out.append(s[i]); i+=1
    return ''.join(out)
patterns={
 'placeholder_or_unauthorized_axiom':r'\b(?:sorry|admit|axiom|constant|postulate)\b',
 'true_proposition_alias':r'\bProp\s*:=\s*True\b',
 'trivial_body':r':=\s*(?:by\s+)?trivial\b',
 'unsafe_declaration':r'^\s*(?:private\s+)?unsafe\b'}
findings=[]
for name in sorted(seen):
    code=code_only((R/name).read_text())
    for kind,pattern in patterns.items():
        for m in re.finditer(pattern,code,re.M):
            findings.append({'file':name,'line':code[:m.start()].count('\n')+1,'kind':kind,'match':m.group()})
log=E/'20261105T074909790079Z-densities-independent-review-build.log'
raw=log.read_text()
assert 'depends on axioms: [propext,' in raw and 'Classical.choice,' in raw and 'Quot.sound]' in raw
assert 'sorryAx' not in raw
report={
 'schema_version':1,'reviewer':'/root/density_fresh_source_module_review',
 'candidate_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scan_command':['/opt/anaconda3/bin/python',str(Path(__file__).relative_to(R))],
 'scanner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Target module, focused test and transitive project-local imports; Mathlib not rescanned. This is a bounded lexical supplement, not a replacement for kernel checking or semantic review.',
 'files':seen,'patterns':patterns,'comments_and_strings_removed':True,'findings':findings,
 'compiled_axiom_evidence':{'log':str(log.relative_to(R)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'observed':['propext','Classical.choice','Quot.sound'],'unauthorized_axioms_observed':False},
 'manual_semantic_closure_review':{'actual_objects_produced_internally':True,'no_public_probability_SPD_integrability_mass_or_Fubini_premise':True,'hdata_is_local_have_applied_to_both_actual_priors':True,'no_totalized_Bochner_fallback':True,'no_synthetic_density_or_law_witness':True,'no_wrapper_only_named_helper_added':True},
 'status':'pass' if not findings else 'fail',
 'limits':'No full-repository check, root build, source-completeness, lifecycle or UI acceptance is asserted.'}
(E/'fake-closure-scan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'files_scanned':len(seen),'findings':findings,'report_sha256':hashlib.sha256((E/'fake-closure-scan.json').read_bytes()).hexdigest()},indent=2))
