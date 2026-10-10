from pathlib import Path
import sys,os,subprocess,json,hashlib,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent
label=sys.argv[1]
groups={
 'contributor-regressions':['-m','unittest','tools.tests.test_astis_contributor_contract','tools.tests.test_astis_publication'],
 'site-regressions':['-m','unittest',*['tools.tests.'+n for n in ['test_astis_site','test_proof_readers','test_metadata_reader','test_astis_source','test_astis_advance','test_astis_semantic_roundtrip','test_astis_publication','test_astis_process_memory','test_harness_site','test_lean_tutor','test_undergrad_guides','test_chewi_source_first_contract','test_chewi_source_first_refinement','test_samplewiki_reader_contract','test_samplewiki_companions','test_underlying_lean_graph','test_cross_domain_program','test_discrete_sampling','test_mcmc_library','test_project_authors_footer']]],
 'publication':['tools/astis_publication.py','check','--base','ea5422f595d24b528cb84ad6fe24ea5097222a2c'],
 'contributor':['tools/astis_contributor_contract.py','check','--base','ea5422f595d24b528cb84ad6fe24ea5097222a2c'],
 'semantic':['tools/astis_semantic_roundtrip.py','check'],
 'frontier':['tools/astis_frontier_cells.py','check'],
 'graph':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-finite-history-tail-law'],
 'site-check':['website/scripts/check_site.py'],
 'site-build':['website/scripts/build_site.py'],
 'canonical':['website/scripts/lean_gate.py'],
 'python-compile':['-m','py_compile','tools/astis.py'],
 'diff-check':['GIT_DIFF_CHECK'],
}
out=r/'checks87'/(sys.argv[2] if len(sys.argv)>2 else label);assert not out.exists();out.mkdir(parents=True)
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
args=['git','diff','--check'] if label=='diff-check' else [sys.executable,'-X','utf8',*groups[label]]
q=subprocess.run(args,cwd=R,env=env,capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
(out/'receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':args,'exit_code':q.returncode,'terminal_closed':True,'module_raw_sha256':hashlib.sha256((R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean').read_bytes()).hexdigest(),'scope':'Actual deterministic-depth history/tail probability bridge only; no fullA7/random-depth/physical-time-memorylessness/wholepaper/Goal credit.'},indent=2)+'\n',encoding='utf8',newline='\n')
print(q.stdout.decode(errors='replace')[-1800:]);print(q.stderr.decode(errors='replace')[-1800:]);sys.exit(q.returncode)
