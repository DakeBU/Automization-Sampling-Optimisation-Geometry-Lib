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
NAME = 'SamplingOptimisationGeometryBench compiled proof-body snapshot'
MARKER = 'SOG_COMPILED_BODY_V1 '
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
KIND = 'compiled-proof-body-constant-occurrences'


def inputs() -> tuple[dict, dict, dict]:
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
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
    return imports+'''
open Lean in
run_cmd do
  let selected : Array Name := #[
    '''+names+''']
  let env ← getEnv
  let mut rows : Array Json := #[]
  for name in selected do
    let some info := env.find? name | throwError "Selected theorem missing"
    let .thmInfo _ := info | throwError "Expected a theorem, not an axiom or definition"
    let some body := info.value? (allowOpaque := true) | throwError "Proof body missing"
    let parents := body.getUsedConstants.filter fun n => selected.contains n
    let axioms ← Lean.collectAxioms name
    rows := rows.push (Json.mkObj [
      ("id", toJson name.toString),
      ("body_parents", toJson (parents.map Name.toString)),
      ("axioms", toJson (axioms.map Name.toString))])
  logInfo m!"SOG_COMPILED_BODY_V1 {(Json.arr rows).compress}"
'''


def canonical_rows(raw: list[dict], spec: dict) -> list[dict]:
    expected=set(spec['nodes'])
    if (not isinstance(raw,list) or any(not isinstance(r,dict) or set(r)!={'id','body_parents','axioms'} for r in raw)
            or len(raw)!=len(expected) or {r['id'] for r in raw}!=expected):
        raise ValueError('Replay must return each selected theorem exactly once')
    rows=[]
    for row in raw:
        parents,axioms=row['body_parents'],row['axioms']
        if (not isinstance(parents,list) or not all(isinstance(n,str) for n in parents)
                or len(set(parents))!=len(parents) or not set(parents)<=expected or row['id'] in parents
                or not isinstance(axioms,list) or not all(isinstance(n,str) for n in axioms)
                or len(set(axioms))!=len(axioms) or not set(axioms)<=AXIOMS):
            raise ValueError('Reject unknown/circular parents or unapproved proof axioms')
        rows.append({'id':row['id'],'body_parents':sorted(parents),'axioms':sorted(axioms)})
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
           'truth_boundary':'An edge records constant occurrence in this compiled proof body, including proof-term annotations. It certifies neither mathematical necessity nor a full dependency closure. No path in an induced slice does not imply no path in the full closure.'}
    return {'schema_version':1,'name':NAME,'provenance':provenance,'rows':rows,
            'graph':graph,'graph_sha256':bench.curriculum.digest(graph)}


def recorded() -> tuple[dict,dict,dict]:
    spec,core,provenance=inputs()
    data=json.loads(SNAPSHOT.read_text(encoding='utf-8'))
    if data!=snapshot(data['rows'],spec,provenance):
        raise ValueError('Compiled proof graph is stale or malformed; replay its trusted source inspector')
    return spec,core,data


def replay() -> dict:
    spec,core,before=inputs()
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
    if inputs()[2]!=before:
        raise ValueError('Selected source/environment changed during replay')
    return snapshot(json.loads(lines[0]),spec,before)


def items() -> list[dict]:
    spec,core,data=recorded()
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
               'snapshot_sha256':bench.sha(bench.encoded(data)),
               'provenance':data['provenance']}
        adjacency={n:{b for a,b in graph['edges'] if a==n} for n in names}
        if task['operation']=='common-body-parents':
            answer=set.intersection(*(adjacency[t] for t in task['targets']))
            question='List the selected theorem constants occurring directly in every listed target proof body in this supplied induced slice. Are these necessarily indispensable mathematical premises?'
        elif task['operation']=='paths-to-interface':
            removed=task['remove']
            if removed not in names or removed in task['targets']:
                raise ValueError('Select a distinct, nontarget interface')
            def reaches(node,visited):
                return node==removed or (node not in visited and any(reaches(p,visited|{node}) for p in adjacency[node]))
            answer={t for t in task['targets'] if reaches(t,set())}
            question='List the target proofs with a directed path to the indicated normalization interface in this supplied compiled-body slice. Does such a path prove mathematical necessity? A missing path here is not a full-closure independence certificate.'
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
        gold={'nodes':sorted(answer),'entails_mathematical_necessity':False}
        rows.append({**prompt,'answer':gold,'binding_sha256':bench.curriculum.digest({'prompt':prompt,'answer':gold}),
                     'reference_status':'compiled occurrence snapshot recorded; separate replay/editorial gates apply'})
    return rows


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('refresh','check'))
    args=parser.parse_args()
    fresh=replay()
    if args.command=='refresh':
        if SNAPSHOT.is_symlink() or (SNAPSHOT.exists() and json.loads(SNAPSHOT.read_text(encoding='utf-8')).get('name')!=NAME):
            raise ValueError('Never overwrite an unrelated file as a graph snapshot')
        SNAPSHOT.write_bytes(bench.encoded(fresh))
        print('Recorded trusted compiled-body slice; no editorial verdict or mathematical necessity was created.')
    elif json.loads(SNAPSHOT.read_text(encoding='utf-8'))!=fresh:
        raise ValueError('Checked-in graph differs from fresh compiled proof-body replay')
    else:
        print('Fresh compiler replay matches the recorded graph; this is not a full closure or necessity certificate.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
