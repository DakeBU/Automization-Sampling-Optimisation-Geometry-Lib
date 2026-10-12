from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent
base='d42d05408676ef3573e325940a1e09c0fdca176e'
checks={
 'publication-main':['tools/astis_publication.py','check','--base','origin/main'],
 'publication':['tools/astis_publication.py','check','--base',base],
 'contributor':['tools/astis_contributor_contract.py','check','--base',base],
 'semantic':['tools/astis_semantic_roundtrip.py','check'],
 'frontier':['tools/astis_frontier_cells.py','check'],
 'graph':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-normalized-endpoint-sector'],
 'python-compile':['-m','py_compile','tools/astis.py'],
 'contributor-regressions':['-m','unittest','tools.tests.test_astis_contributor_contract','tools.tests.test_astis_publication'],
 'site-build':['website/scripts/build_site.py'],
 'site-check':['website/scripts/check_site.py'],
 'site-regressions':['-m','unittest',*['tools.tests.'+n for n in ['test_astis_site','test_proof_readers','test_metadata_reader','test_astis_source','test_astis_advance','test_astis_semantic_roundtrip','test_astis_publication','test_astis_process_memory','test_harness_site','test_lean_tutor','test_undergrad_guides','test_chewi_source_first_contract','test_chewi_source_first_refinement','test_samplewiki_reader_contract','test_samplewiki_companions','test_underlying_lean_graph','test_cross_domain_program','test_discrete_sampling','test_mcmc_library','test_project_authors_footer']]],
 'astis':['tools/astis.py','check'],
 'process-memory':['tools/astis_process_memory.py','check'],
 'harness':['tools/astis.py','harness-test'],
 'canonical':['website/scripts/lean_gate.py'],
 'underlying-graph':['website/scripts/underlying_lean_graph.py'],
}
label=sys.argv[1];out=r/'checks104'/(sys.argv[2] if len(sys.argv)>2 else label);out.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
if label=='diff-check':cmd=['git','diff','--check']
elif label=='focused-build':cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector']
elif label=='tests':cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'build','Tests']
else:cmd=[sys.executable,'-X','utf8',*checks[label]]
q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
data=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,exit_code=q.returncode,terminal_closed=True,
    module_raw_sha256=hashlib.sha256((R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean').read_bytes()).hexdigest())
(out/'receipt.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
print(q.stdout.decode(errors='replace')[-1800:]);print(q.stderr.decode(errors='replace')[-1400:]);print(json.dumps(data))
sys.exit(q.returncode)
