"""Replay a tiny allowlisted proof-body occurrence graph with pinned Lean.

This compiles trusted project imports and an environment inspector, never model
submissions. The induced public-theorem slice omits other constants, including
private auxiliaries. It certifies neither a full closure nor mathematical necessity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

import sog_bench as bench
import sog_bench_review as review

SPEC = bench.DATA.parent/'compiled_graph_tasks.json'
SNAPSHOT = bench.DATA.parent/'compiled-transport-graph.json'
FLOW_SPEC = bench.DATA.parent/'compiled_flow_graph_tasks.json'
FLOW_SNAPSHOT = bench.DATA.parent/'compiled-flow-graph.json'
NAME = 'SamplingOptimisationGeometryBench compiled proof-body snapshot'
MARKER = 'SOG_COMPILED_BODY_V1 '
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
KIND = 'compiled-proof-body-constant-occurrences'
# Direct constants in the elaborated, unexpanded statement; not inferred
# hypotheses, a type dependency closure, or evidence of logical necessity.
STATEMENT_CONSTANTS = {'CompleteSpace', 'HasGradientAt', 'HasDerivAt',
                       'HasDerivWithinAt', 'Differentiable'}


def inputs(spec_path: Path | None = None) -> tuple[dict, dict, dict]:
    spec = json.loads((spec_path or SPEC).read_text(encoding='utf-8'))
    if (spec.get('schema_version')!=1 or not isinstance(spec.get('source_files'),list)
            or not isinstance(spec.get('nodes'),dict) or not isinstance(spec.get('tasks'),list)):
        raise ValueError('Invalid bounded compiler-graph selection')
    # Resolve source names once per process; source fingerprints below are never cached.
    known = bench.astis_site._SOURCE_BY_NAME
    if not known:
        known={d.full_name:d for d in bench.astis_site.scan_project_sources()[1]}
        bench.astis_site._SOURCE_BY_NAME=known
    core = next((c for c in bench.materialize() if c['id']==spec.get('core_id')),None)
    if core is None or not bench.has_lean(core):
        raise ValueError('Select an existing aligned mathematical core')
    sources = {}
    for rel in spec['source_files']:
        if (not isinstance(rel,str) or '\\' in rel or '..' in Path(rel).parts
                or not rel.startswith('AutoSamplingTheory/TechnicalLemmas/') or not rel.endswith('.lean')):
            raise ValueError('Only explicitly eligible project-original technical sources may be selected')
        text=(bench.ROOT/rel).read_text(encoding='utf-8')
        if 'atlas' in text.lower():
            raise ValueError('Restricted-source references are not eligible for this ML slice')
        sources[rel]=bench.text_hash(bench.ROOT/rel)
    if len(sources)!=len(spec['source_files']) or not sources or not spec['nodes'] or len(spec['nodes'])>64:
        raise ValueError('Use a nonempty bounded nonduplicate source/theorem selection')
    for name,label in spec['nodes'].items():
        if (not re.fullmatch(r'AutoSamplingTheory\.TechnicalLemmas\.[A-Za-z0-9_.]+',name)
                or name not in known or known[name].source_file not in sources
                or known[name].kind not in {'theorem','lemma'} or known[name].has_placeholder
                or not isinstance(label,str) or not label.strip()):
            raise ValueError('Every selected node must resolve to an eligible completed local theorem')
    selection={'core_id':core['id'],'source_files':sorted(sources),'nodes':spec['nodes']}
    provenance={'core_id':core['id'],'core_binding_sha256':core['binding_sha256'],
                'context_sha256':review.context_binding(core), 'source_sha256_lf':sources,
                'selection_sha256':bench.sha(bench.encoded(selection)),
                'generator_sha256_lf':bench.text_hash(Path(__file__)),
                'toolchain':(bench.ROOT/'lean-toolchain').read_text().strip(),
                'mathlib_manifest_sha256_lf':bench.text_hash(bench.ROOT/'lake-manifest.json'),
                'lakefile_sha256_lf':bench.text_hash(bench.ROOT/'lakefile.lean')}
    if provenance['toolchain']!='leanprover/lean4:v4.33.0':
        raise ValueError('Compiled graph requires the pinned Lean 4.33.0')
    return spec,core,provenance


def probe_source(spec: dict) -> str:
    imports=''.join('import '+rel.removesuffix('.lean').replace('/','.')+'\n' for rel in sorted(spec['source_files']))
    names=',\n    '.join('`'+name for name in sorted(spec['nodes']))
    statements=', '.join('`'+name for name in sorted(STATEMENT_CONSTANTS))
    required={name for task in spec['tasks'] for name in task.get('required_statement_constants',[])}
    if not required<=STATEMENT_CONSTANTS:
        raise ValueError('Unknown requested statement-profile selector')
    required_names=', '.join('`'+name for name in sorted(required))
    return imports+'''
open Lean in
run_cmd do
  let selected : Array Name := #[
    '''+names+''']
  let env ← getEnv
  let statementConstants : Array Name := #['''+statements+''']
  let requiredStatementConstants : Array Name := #['''+required_names+''']
  for tag in requiredStatementConstants do
    if (env.find? tag).isNone then
      throwError m!"Requested statement-profile selector is absent from this environment: {tag}"
  let mut rows : Array Json := #[]
  for name in selected do
    let some info := env.find? name | throwError "Selected theorem missing"
    let .thmInfo _ := info | throwError "Expected a theorem, not an axiom or definition"
    let some body := info.value? (allowOpaque := true) | throwError "Proof body missing"
    let parents := body.getUsedConstants.filter fun n => selected.contains n
    let profile := info.type.getUsedConstants.filter fun n => statementConstants.contains n
    let axioms ← Lean.collectAxioms name
    rows := rows.push (Json.mkObj [
      ("id", toJson name.toString),
      ("body_parents", toJson (parents.map Name.toString)),
      ("statement_constants", toJson (profile.map Name.toString)),
      ("axioms", toJson (axioms.map Name.toString))])
  logInfo m!"SOG_COMPILED_BODY_V1 {(Json.arr rows).compress}"
'''


def canonical_rows(raw: list[dict], spec: dict) -> list[dict]:
    expected=set(spec['nodes'])
    if (not isinstance(raw,list) or any(not isinstance(r,dict) or set(r)!={'id','body_parents','axioms','statement_constants'} for r in raw)
            or len(raw)!=len(expected) or {r['id'] for r in raw}!=expected):
        raise ValueError('Replay must return each selected theorem exactly once')
    rows=[]
    for row in raw:
        parents,axioms,profile=row['body_parents'],row['axioms'],row['statement_constants']
        if (not isinstance(parents,list) or not all(isinstance(n,str) for n in parents)
                or len(set(parents))!=len(parents) or not set(parents)<=expected or row['id'] in parents
                or not isinstance(axioms,list) or not all(isinstance(n,str) for n in axioms)
                or len(set(axioms))!=len(axioms) or not set(axioms)<=AXIOMS
                or not isinstance(profile,list) or not all(isinstance(n,str) for n in profile)
                or len(set(profile))!=len(profile) or not set(profile)<=STATEMENT_CONSTANTS):
            raise ValueError('Reject unknown/circular parents or unapproved proof axioms')
        rows.append({'id':row['id'],'body_parents':sorted(parents),'axioms':sorted(axioms),
                     'statement_constants':sorted(profile)})
    # A theorem-body slice should be acyclic, not merely self-loop-free.
    adjacency={r['id']:r['body_parents'] for r in rows}
    def visit(node,active,done):
        if node in active:
            raise ValueError('Cyclic theorem-body occurrence graph')
        if node not in done:
            for parent in adjacency[node]:
                visit(parent,active|{node},done)
            done.add(node)
    done=set()
    for node in adjacency:
        visit(node,set(),done)
    return sorted(rows,key=lambda r:r['id'])


def snapshot(rows: list[dict], spec: dict, provenance: dict) -> dict:
    rows=canonical_rows(rows,spec)
    graph={'kind':KIND,'direction':'theorem-to-selected-constant-in-compiled-proof-body',
           'scope':'induced public-theorem slice; unselected constants, private auxiliaries and Mathlib parents are omitted',
           'nodes':sorted(spec['nodes']),
           'edges':sorted([r['id'],p] for r in rows for p in r['body_parents']),
           'node_labels':spec['nodes'], 'source_sha256_lf':provenance['source_sha256_lf'],
           'statement_constant_whitelist':sorted(STATEMENT_CONSTANTS),
           'statement_profiles':{r['id']:r['statement_constants'] for r in rows},
           'statement_profile_scope':'Direct constant occurrences in the unexpanded elaborated statement; not a binder-role analysis, inferred hypothesis list or full type dependency closure.',
           'truth_boundary':'An edge records constant occurrence in this compiled proof body, including proof-term annotations. Statement profiles record only whitelisted direct type-constant occurrences, not logical requirements. Neither certifies mathematical necessity or a full dependency closure. No path in an induced slice does not imply no path in the full closure.'}
    return {'schema_version':1,'name':NAME,'provenance':provenance,'rows':rows,
            'graph':graph,'graph_sha256':bench.curriculum.digest(graph)}


def recorded(spec_path: Path | None = None, snapshot_path: Path | None = None) -> tuple[dict,dict,dict]:
    spec,core,provenance=inputs(spec_path)
    data=json.loads((snapshot_path or SNAPSHOT).read_text(encoding='utf-8'))
    if data!=snapshot(data['rows'],spec,provenance):
        raise ValueError('Compiled proof graph is stale or malformed; replay its trusted source inspector')
    return spec,core,data


def replay(spec_path: Path | None = None) -> dict:
    spec,core,before=inputs(spec_path)
    def run(command):
        result=subprocess.run(command,cwd=bench.ROOT,text=True,encoding='utf-8',errors='replace',
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        if result.returncode:
            raise ValueError('Trusted compiler replay failed: '+' '.join(command)+'\n'+result.stdout[-6000:])
        return result.stdout
    version=run(['lake','env','lean','--version'])
    if not re.search(r'version 4\.33\.0(?:[, )])',version):
        raise ValueError('Effective compiler is not Lean 4.33.0')
    manifest=json.loads((bench.ROOT/'lake-manifest.json').read_text(encoding='utf-8'))
    pinned=next(p['rev'] for p in manifest['packages'] if p['name']=='mathlib')
    if run(['git','-C','.lake/packages/mathlib','rev-parse','HEAD']).strip()!=pinned:
        raise ValueError('Actual Mathlib checkout differs from its pinned revision')
    if run(['git','-C','.lake/packages/mathlib','status','--porcelain']).strip():
        raise ValueError('Compiler replay requires an unmodified Mathlib checkout')
    modules=[rel.removesuffix('.lean').replace('/','.') for rel in sorted(spec['source_files'])]
    run(['lake','build',*modules])
    directory=bench.ROOT/'.astis/sog-bench'
    directory.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='compiled-graph-',dir=directory) as tmp:
        path=Path(tmp)/'Inspect.lean'
        path.write_text(probe_source(spec),encoding='utf-8',newline='\n')
        output=run(['lake','env','lean',path.relative_to(bench.ROOT).as_posix()])
    lines=[line.split(MARKER,1)[1] for line in output.splitlines() if MARKER in line]
    if len(lines)!=1:
        raise ValueError('Expected exactly one structured compiler graph response')
    if inputs(spec_path)[2]!=before:
        raise ValueError('Selected source/environment changed during replay')
    return snapshot(json.loads(lines[0]),spec,before)


def items(spec_path: Path | None = None, snapshot_path: Path | None = None) -> list[dict]:
    spec,core,data=recorded(spec_path,snapshot_path)
    rows=[]
    for task in spec['tasks']:
        names=set(task['view_nodes'])
        if (len(names)!=len(task['view_nodes']) or not names<=set(data['graph']['nodes'])
                or not task['targets'] or len(set(task['targets']))!=len(task['targets'])
                or not set(task['targets'])<=names):
            raise ValueError('Question must select distinct existing graph nodes and targets')
        graph={**data['graph'],'nodes':sorted(names),
               'edges':[e for e in data['graph']['edges'] if set(e)<=names],
               'node_labels':{n:spec['nodes'][n] for n in sorted(names)},
               'statement_profiles':{n:data['graph']['statement_profiles'][n] for n in sorted(names)},
               'snapshot_sha256':bench.sha(bench.encoded(data)),
               'provenance':data['provenance']}
        adjacency={n:{b for a,b in graph['edges'] if a==n} for n in names}
        if task['operation']=='common-body-parents':
            answer=set.intersection(*(adjacency[t] for t in task['targets']))
            question='List the selected theorem constants occurring directly in every listed target proof body in this supplied induced slice. Are these necessarily indispensable mathematical premises?'
        elif task['operation'] in {'paths-to-interface','typed-paths-to-interface'}:
            removed=task['remove']
            if removed not in names or removed in task['targets']:
                raise ValueError('Select a distinct, nontarget interface')
            def reaches(node,visited):
                return node==removed or (node not in visited and any(reaches(p,visited|{node}) for p in adjacency[node]))
            answer={t for t in task['targets'] if reaches(t,set())}
            question='List the target proofs with a directed path to the indicated interface in this supplied compiled-body slice. Does such a path prove mathematical necessity? A missing path here is not a full-closure independence certificate.'
            if task['operation']=='typed-paths-to-interface':
                required=task['required_statement_constants']
                if (not required or len(set(required))!=len(required) or not set(required)<=STATEMENT_CONSTANTS):
                    raise ValueError('Select distinct constants from the emitted statement-profile whitelist')
                answer={t for t in answer if set(required)<=set(graph['statement_profiles'][t])}
                question='List only targets that BOTH have a directed path to the indicated interface AND contain every requested constant in their supplied unexpanded-statement profile. This is a structural/type-occurrence filter, not proof of necessary hypotheses or that other targets lack a genuine gradient.'
        else:
            raise ValueError('Unknown compiled graph question operation')
        bench.curriculum.classify({'library_domains':core['library_domains'],'skills':['graph-reading','semantic-boundary'],
            'track_levels':{'natural-language':task['level']},'lean_enabled':False,
            'difficulty_reason':'Local structural comparison, not mathematical proof length or graph distance.'},bench.curriculum.curriculum())
        prompt={'id':task['id'],'core_id':core['id'],'family':core['family'],'title':task['title'],
                'library_domains':core['library_domains'],'track':'graph-json','level':task['level'],'split':core['split'],
                'skills':['graph-reading','semantic-boundary'],'targets':task['targets'],'question':question,
                'context':graph,'graph_sha256':bench.curriculum.digest(graph),
                'answer_schema':{'nodes':'list of distinct declaration ids; order ignored by scorer',
                                 'entails_mathematical_necessity':'boolean; whether this evidence certifies mathematical necessity'}}
        if 'remove' in task:
            prompt['remove']=task['remove']
        if task['operation']=='typed-paths-to-interface':
            prompt['required_statement_constants']=required
        gold={'nodes':sorted(answer),'entails_mathematical_necessity':False}
        rows.append({**prompt,'answer':gold,'binding_sha256':bench.curriculum.digest({'prompt':prompt,'answer':gold}),
                     'reference_status':'compiled occurrence snapshot recorded; separate replay/editorial gates apply'})
    return rows


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('refresh','check'))
    parser.add_argument('--slice', choices=('all','transport','convex-flow'), default='all')
    args=parser.parse_args()
    for label,spec_path,snapshot_path in (('transport',SPEC,SNAPSHOT),('convex-flow',FLOW_SPEC,FLOW_SNAPSHOT)):
        if args.slice not in {'all',label}:
            continue
        fresh=replay(spec_path)
        if args.command=='refresh':
            if snapshot_path.is_symlink() or (snapshot_path.exists() and json.loads(snapshot_path.read_text(encoding='utf-8')).get('name')!=NAME):
                raise ValueError('Never overwrite an unrelated file as a graph snapshot')
            snapshot_path.write_bytes(bench.encoded(fresh))
            print(label+': recorded trusted body/statement occurrences; no editorial verdict or necessity created.')
        elif json.loads(snapshot_path.read_text(encoding='utf-8'))!=fresh:
            raise ValueError(label+': graph differs from fresh compiled replay')
        else:
            print(label+': fresh compiler replay matches; not a full closure or necessity certificate.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
