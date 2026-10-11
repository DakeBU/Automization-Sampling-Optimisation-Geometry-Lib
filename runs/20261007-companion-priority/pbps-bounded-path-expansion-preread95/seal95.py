"""Freeze the independently reviewed complete bounded path expansion target."""
from pathlib import Path
import json, hashlib, datetime, subprocess
root=Path.cwd(); pre=Path(__file__).parent; run94=pre.parent/'pbps-actual-prescribed-path-density94'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
manifests=[pre/'independent-header-math95/closed-RAW-manifest.native.json',pre/'independent-header-source95/closed-raw-manifest95.native.json',run94/'next-source-graph95/closed-RAW-source-graph95.native.json']
checked={}
def visit(x):
    if isinstance(x,dict):
        if 'path' in x and 'raw_sha256' in x:
            p=Path(x['path']); q=pin(p)
            assert q['raw_sha256']==x['raw_sha256'],p
            checked[q['path']]=q
        for v in x.values():visit(v)
    elif isinstance(x,list):
        for v in x:visit(v)
for p in manifests:
    visit(load(p));checked[p.as_posix()]=pin(p)
math=pre/'independent-header-math95/decision.native.json'
source=pre/'independent-header-source95/header-source-audit95.native.json'
assert load(math)['status']=='ACCEPTED_PROSPECTIVE_MATHEMATICAL_STATEMENT_NO_REQUIRED_CORRECTION'
assert load(source)['status']=='NO_SOURCE_VETO_FOR_PROSPECTIVE_SEALING'
header=pre/'Header95.lean';text=header.read_text(encoding='utf8')
assert pin(header)['raw_sha256']=='2a9d3052c353ab8aab448de05a05beeadab320def15ee31b1d353abbb063d002'
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean').exists()
for p in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json',pre/'reuse-search95/receipt.json']:
    checked[str(p).replace('\\','/')]=pin(p)
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_MATH_SOURCE_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),header=pin(header),expanded_literal_Prop=text.split('noncomputable def candidate_statement',1)[1].split('#check',1)[0],proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 (A.7), all finite counts and bounded measurable real path functionals',source_graph=load(source)['source_graph'],source_coverage=load(source)['source_coverage'],primary=load(source)['primary'],independent_math_header=pin(math),independent_source_header=pin(source),all_review_bound_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['finite-dimensional real Hilbert E; Borel measurable structure'],observable_scope=['all coordinate-product measurable real path F','every nonnegative global bound M for |F|'],EXCESS=[]),definition_audit='22 inherited literal definitions agree with93; wgt is the94 whole-path hazard and incoming-rate expression. Z is bound to raw covered arcs and uncovered z0 fallback with AE initialization; it is not an unspecified law witness.',proof_ingredients_are_dependencies=['actual finite-count joint law93','density identity94','derive each real sector integrability','derive absolute summability by probability-sector masses','derive the all-count signed identity'],alternative_routes='Mass partition route is an ASTIS completion; printed rate-cap/simplex-factorial domination remains an explicit source OR route. No cap premise added.',truth_boundary='Coordinate-product path sigma only. Covers n0,T0,rank0,zero rates,stopping and infinite waits. Fixed deterministic parameters and horizon precede AE/integration. No Skorokhod assertion, unbounded-observable or cost claim, restart/Markovness, invariance, hypocoercivity, main theorem or composition completion.',proof_search_started=False,Goal_complete=False)
out=pre/'root.statement-seal95.json';assert not out.exists()
out.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('SEALED95',pin(out)['raw_sha256'],'verified pins',len(checked))
