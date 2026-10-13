from pathlib import Path
import sys,os,subprocess,json,hashlib,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent/'ci-reader-order-repair86'
label=sys.argv[1]
groups={
 'contributor-regressions':['-m','unittest','tools.tests.test_astis_contributor_contract','tools.tests.test_astis_publication'],
 'site-regressions':['-m','unittest',*['tools.tests.'+n for n in ['test_astis_site','test_proof_readers','test_metadata_reader','test_astis_source','test_astis_advance','test_astis_semantic_roundtrip','test_astis_publication','test_astis_process_memory','test_harness_site','test_lean_tutor','test_undergrad_guides','test_chewi_source_first_contract','test_chewi_source_first_refinement','test_samplewiki_reader_contract','test_samplewiki_companions','test_underlying_lean_graph','test_cross_domain_program','test_discrete_sampling','test_mcmc_library','test_project_authors_footer']]],
 'publication':['tools/astis_publication.py','check','--base','f62dca7500b1fa035ef7b377ac55e182ea3fd057'],
 'contributor':['tools/astis_contributor_contract.py','check','--base','f62dca7500b1fa035ef7b377ac55e182ea3fd057'],
 'semantic':['tools/astis_semantic_roundtrip.py','check'],
 'frontier':['tools/astis_frontier_cells.py','check'],
 'graph':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-finite-first-event-law'],
 'site-check':['website/scripts/check_site.py'],
 'canonical':['website/scripts/lean_gate.py'],
 'python-compile':['-m','py_compile','tools/astis.py','tools/tests/test_astis_publication.py'],
}
out=r/(sys.argv[2] if len(sys.argv)>2 else label);assert not out.exists();out.mkdir()
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
args=[sys.executable,'-X','utf8',*groups[label]]
q=subprocess.run(args,cwd=R,env=env,capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
(out/'receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':args,'exit_code':q.returncode,'terminal_closed':True,'test_raw_sha256':hashlib.sha256((R/'tools/tests/test_astis_publication.py').read_bytes()).hexdigest(),'scope':'Test-only exact repair; mathematical86/source/renderer unchanged; new87 separately exploring and uncommitted.'},indent=2)+'\n',encoding='utf-8',newline='\n')
print(q.stdout.decode(errors='replace')[-2000:]);print(q.stderr.decode(errors='replace')[-2000:]);sys.exit(q.returncode)
