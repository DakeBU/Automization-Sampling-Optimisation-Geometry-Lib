from __future__ import annotations
import json
import base64
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import sog_bench_lean as runtime
import sog_bench_lean_native as native
import sog_bench_lean_workspace as workspace


def core():
    return {'id':'sogb-001','family':'fixture','split':'public-dev','binding_sha256':'binding',
        'imports':['Mathlib.Data.Nat.Basic'],'source_file':'AutoSamplingTheory/Fixture.lean',
        'lean_task':'import Mathlib.Data.Nat.Basic\nexample : 1 = 1 := by\n  -- Replace this comment with your proof.\n',
        'lean_reference':'import Mathlib.Data.Nat.Basic\nexample : 1 = 1 := by\n  rfl\n'}


class LeanRuntimeTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform=='linux','POSIX cache modes require Linux')
    def test_private_mode_public_cache_is_copied_without_changing_original_inode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.write_bytes(b'public trace');source.chmod(0o600)
            target=root/'copy';native.public_cache_file(source,target)
            self.assertEqual(source.stat().st_mode & 0o777,0o600)
            self.assertEqual(target.stat().st_mode & 0o777,0o644)
            self.assertNotEqual(source.stat().st_ino,target.stat().st_ino)
            source.chmod(0o644);linked=root/'linked';native.public_cache_file(source,linked)
            self.assertEqual(source.stat().st_ino,linked.stat().st_ino)

    def test_policy_keeps_project_version_and_standard_axioms(self):
        p=runtime.policy()
        self.assertEqual(p['lean_toolchain'],'leanprover/lean4:v4.33.0')
        self.assertEqual(p['minimum_landlock_abi'],6)
        self.assertTrue(p['base_image'].startswith('ubuntu:24.04@sha256:'))

    def test_offline_locations_preserve_the_exact_package_graph(self):
        original=json.loads((ROOT/'lake-manifest.json').read_text())
        offline=runtime.offline_manifest()
        self.assertEqual(len(original['packages']),len(offline['packages']))
        for before,after in zip(original['packages'],offline['packages']):
            self.assertEqual(after['type'],'path')
            self.assertEqual(after['dir'],'/deps/packages/'+before['name'])
            for key in ('name','scope','inherited','configFile','manifestFile'):
                self.assertEqual(before[key],after[key])
        config=runtime.offline_lakefile()
        self.assertIn('require mathlib from "/deps/packages/mathlib"',config)
        self.assertIn('lean_lib Challenge',config)
        self.assertNotIn('require mathlib from git',config)

    def test_owned_cache_includes_required_c_outputs_without_other_modules(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(runtime,'ROOT',Path(tmp)):
            lib=Path(tmp)/'.lake/build/lib/lean/AutoSamplingTheory/Ancestor'
            ir=Path(tmp)/'.lake/build/ir/AutoSamplingTheory/Ancestor'
            lib.parent.mkdir(parents=True);ir.parent.mkdir(parents=True)
            for ext in ('.olean','.ilean','.trace'):
                lib.with_suffix(ext).write_bytes(b'Unexecuted artifact fixture')
            with self.assertRaises(ValueError):runtime.owned_artifacts(['AutoSamplingTheory.Ancestor'])
            ir.with_suffix('.c').write_bytes(b'C artifact fixture, not compiled')
            ir.with_suffix('.setup.json').write_bytes(b'{}')
            ir.parent.joinpath('Unrelated.c').write_bytes(b'must not be included')
            artifacts=runtime.owned_artifacts(['AutoSamplingTheory.Ancestor'])
            self.assertIn('ir/AutoSamplingTheory/Ancestor.c',artifacts)
            self.assertIn('ir/AutoSamplingTheory/Ancestor.setup.json',artifacts)
            self.assertFalse(any('Unrelated' in p for p in artifacts))

    def packet(self,c=None):
        with patch.object(runtime.bench,'prompts',return_value=[{'track':'lean','question':'fixed prompt'}]),\
             patch.object(runtime.bench,'environment_digest',return_value='context'):
            return runtime.packet(c or core())

    def test_three_views_separate_statement_baseline_from_oracle(self):
        files=self.packet()
        self.assertIn(b'theorem sogBenchTarget : 1 = 1',files['verifier/Challenge.lean'])
        self.assertIn(b'sorry',files['verifier/Challenge.lean'])
        self.assertNotIn(b'rfl',files['verifier/Challenge.lean'])
        self.assertNotIn(b'sorry',files['oracle/Solution.lean.txt'])
        self.assertNotIn(b'rfl',files['agent/Solution.lean.txt'])
        cfg=json.loads(files['verifier/config.json'])
        self.assertEqual(cfg['definition_names'],[])
        self.assertNotIn('sorryAx',cfg['permitted_axioms'])
        desc=json.loads(files['operator.json'])
        self.assertEqual(files['agent/LICENSE'],(ROOT/'LICENSE').read_bytes())
        for path,digest in desc['files'].items():
            self.assertEqual(runtime.bench.sha(files[path]),digest)

    def test_non_aligned_or_ambiguous_or_changed_slot_rejected(self):
        for key,value in [('lean_enabled',False),('lean_task','example : True := by trivial'),
                          ('lean_reference','example : True := by trivial\nexample : True := by trivial')]:
            c=core();c[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.packet(c)

    def test_full_source_is_data_not_an_executed_host_command(self):
        c=core();c['lean_reference'] += '\n-- test string; no runner executes it here\n'
        with patch.object(runtime.subprocess,'run',side_effect=AssertionError('No execution')):
            self.assertIn('operator.json',self.packet(c))

    def test_export_projects_actual_editorial_schema_and_excludes_pending(self):
        c=core()
        with tempfile.TemporaryDirectory() as tmp,\
             patch.object(runtime.bench,'materialize',return_value=[c]),\
             patch.object(runtime,'packet',return_value={'agent/prompt.json':b'{}'}),\
             patch.object(runtime.bench,'editorial_review',return_value={'items':{c['id']:{'editorial':'accepted'}}}):
            out=Path(tmp)/'fresh'
            self.assertEqual(runtime.export(out),['sogb-001'])
            self.assertEqual((out/'sogb-001/agent/prompt.json').read_bytes(),b'{}')
            with self.assertRaises(ValueError):runtime.export(out)
        with tempfile.TemporaryDirectory() as tmp,\
             patch.object(runtime.bench,'materialize',return_value=[c]),\
             patch.object(runtime.bench,'editorial_review',return_value={'items':{c['id']:{'editorial':'pending'}}}):
            with self.assertRaises(ValueError):runtime.export(Path(tmp)/'new',['sogb-001'])

    def test_unsupported_host_is_rejected_before_any_submission_execution(self):
        with patch.object(runtime.sys,'platform','win32'),\
             patch.object(runtime.subprocess,'Popen',side_effect=AssertionError('Must not execute')):
            with self.assertRaises(RuntimeError):runtime.run_submission(
                task=Path('no'),stage_dir=Path('no'),submission=Path('no'),runtime=Path('no'),output=Path('no'))

    def test_invalid_input_is_bounded_and_never_evaluated(self):
        with tempfile.TemporaryDirectory() as tmp,\
             patch.object(runtime.subprocess,'Popen',side_effect=AssertionError('No submitted host execution')):
            root=Path(tmp);source=root/'input.txt'
            self.assertEqual(runtime.read_submission(source,4),(None,'missing-file'))
            source.write_bytes(b'12345')
            self.assertEqual(runtime.read_submission(source,4),(None,'too-large'))
            source.write_bytes(b'\xff')
            self.assertEqual(runtime.read_submission(source,4),(None,'invalid-utf8'))
            source.write_bytes(b'1234')
            self.assertEqual(runtime.read_submission(source,4),(b'1234',None))
            source.write_bytes(b'')
            self.assertEqual(runtime.read_submission(source,4),(b'',None))

    @unittest.skipUnless(sys.platform=='linux','Actual symlink/FIFO behavior requires POSIX')
    def test_fifo_and_symlink_are_rejected_without_blocking_or_following(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'regular';source.write_bytes(b'not Lean')
            link=root/'link';link.symlink_to(source)
            self.assertEqual(runtime.read_submission(link,65536),(None,'symlink'))
            fifo=root/'fifo';os.mkfifo(fifo)
            self.assertEqual(runtime.read_submission(fifo,65536),(None,'not-regular'))

    def test_invalid_selected_attempt_gets_evidence_before_any_docker_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);task=root/'task';stage=root/'stage';prepared=root/'runtime'
            task.mkdir();stage.mkdir();prepared.mkdir();(task/'verifier').mkdir()
            (task/'operator.json').write_text('{}');(prepared/'preparation.json').write_text('{}')
            for name in ('Challenge.lean','config.json'):
                (task/'verifier'/name).write_bytes(b'Unexecuted unit fixture')
                (stage/name).write_bytes(b'Unexecuted unit fixture')
            (stage/'stage.json').write_bytes(runtime.bench.encoded({
                'id':core()['id'],'binding_sha256':'binding','files':{}}))
            with patch.object(runtime.sys,'platform','linux'),\
                 patch.object(runtime.shutil,'which',return_value='docker'),\
                 patch.object(runtime,'check_runtime'),patch.object(runtime,'checked_packet',return_value=core()),\
                 patch.object(runtime.subprocess,'Popen',side_effect=AssertionError('No process for invalid input')):
                output=root/'evidence'
                result=runtime.run_submission(task=task,stage_dir=stage,submission=root/'missing',runtime=prepared,output=output)
                self.assertEqual(result['kind'],'invalid-submission')
                self.assertEqual(result['reason'],'missing-file')
                self.assertIsNone(result['submission_sha256'])
                self.assertFalse(result['container_started'])
                self.assertEqual(json.loads((output/'result.json').read_text()),result)

    def test_hostile_sources_are_only_data_and_expect_real_markers_and_reasons(self):
        with patch.object(runtime.subprocess,'run',side_effect=AssertionError('Never run hostile fixture here')):
            sources=native.hostile_sources('theorem sogBenchTarget : True := by trivial\n')
        self.assertEqual(len(sources),4)
        self.assertIn('Std.Internal.UV.TCP',sources['denied-network'][0])
        self.assertIn('socket.connect',sources['denied-network'][0])
        self.assertEqual(sources['denied-trusted-write'][1],'accepted')
        self.assertEqual(sources['wall-limit'][1],'resource-limit')
        self.assertEqual(sources['diagnostic-limit'][1],'resource-limit')

    def test_verdict_requires_consistent_exit_and_started_container_evidence(self):
        state={'StartedAt':'2026-11-05T00:00:00Z','ExitCode':0,'OOMKilled':False}
        native={'kind':'fixed-target-comparator','accepted':True,'comparator_exit':0}
        self.assertEqual(runtime.classify(0,native,state,None),'accepted')
        self.assertEqual(runtime.classify(10,{**native,'accepted':False,'comparator_exit':1},
            {**state,'ExitCode':10},None),'proof-rejected')
        for code,value,observed,reason in [
            (0,native,None,None),(0,native,{**state,'StartedAt':'0001-01-01T00:00:00Z'},None),
            (0,{'accepted':True},state,None),(0,{**native,'comparator_exit':1},state,None),
            (10,{},state,None),(10,{**native,'comparator_exit':None},state,None)]:
            with self.subTest(code=code,value=value):
                self.assertEqual(runtime.classify(code,value,observed,reason),'infrastructure-error')
        self.assertEqual(runtime.classify(137,None,{**state,'OOMKilled':True},None,'verifying-solution'),'resource-limit')
        self.assertEqual(runtime.classify(137,None,state,'wall-time-limit','verifying-solution'),'resource-limit')
        self.assertEqual(runtime.classify(137,None,state,'wall-time-limit','challenge-preflight'),'infrastructure-error')
        self.assertEqual(runtime.classify(30,{**native,'diagnostic_limit':True},
            {**state,'ExitCode':30},None),'resource-limit')
        self.assertEqual(runtime.classify(30,{**native,'diagnostic_limit':True},state,None),'infrastructure-error')

    def test_control_framing_keeps_stdout_data_and_preflight_distinct(self):
        phases=[{'kind':'runtime-phase','phase':'challenge-preflight'},
                {'kind':'runtime-phase','phase':'verifying-solution'}]
        native={'kind':'fixed-target-comparator','accepted':False,'comparator_exit':1,
                'diagnostic':'{"accepted":true}\nYour solution is okay!'}
        raw=b'\n'.join(json.dumps(x).encode() for x in [*phases,native])
        self.assertEqual(runtime.parse_control(raw),(native,'verifying-solution'))
        partial=b'\n'.join(json.dumps(x).encode() for x in phases)+b'\n{"broken":'
        self.assertEqual(runtime.parse_control(partial),(None,'verifying-solution'))
        self.assertIsNone(runtime.parse_control(json.dumps(native).encode())[0])
        error={'kind':'infrastructure-error','accepted':False,'error':'trusted challenge failed'}
        self.assertEqual(runtime.parse_control(json.dumps(error).encode()),(error,None))

    def test_live_diagnostics_survive_timeout_as_data_not_control_or_a_verdict(self):
        raw_data=b'{"accepted":true}\nYour solution is okay!\n'
        frames=[{'kind':'runtime-phase','phase':'challenge-preflight'},
            {'kind':'runtime-diagnostic','phase':'challenge-preflight',
             'chunk_b64':base64.b64encode(raw_data).decode()}]
        raw=b'\n'.join(json.dumps(x).encode() for x in frames)+b'\n{"partial":'
        chunks=[];native,phase=runtime.parse_control(raw,diagnostic_chunks=chunks)
        self.assertIsNone(native);self.assertEqual(phase,'challenge-preflight')
        self.assertEqual(b''.join(chunks),raw_data)
        wrong=[frames[0],{**frames[1],'phase':'verifying-solution'},
               {'kind':'fixed-target-comparator','accepted':True}]
        self.assertIsNone(runtime.parse_control(b'\n'.join(json.dumps(x).encode() for x in wrong))[0])

    def test_cli_exposes_nonzero_rejection_and_infrastructure_status(self):
        for kind,code in runtime.EXIT_CODES.items():
            with self.subTest(kind=kind),\
                 patch.object(runtime.sys,'argv',['tool','run','--task','t','--stage','s','--runtime','r','--submission','f','--output','o']),\
                 patch.object(runtime,'run_submission',return_value={'kind':kind}),\
                 redirect_stdout(io.StringIO()),self.assertRaises(SystemExit) as error:
                runtime.main()
            self.assertEqual(error.exception.code,code)

    def test_runtime_receipt_rejects_tool_or_source_drift_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);(path/'tools').mkdir()
            for name in ('container.py','landrun-env','policy.json'):
                (path/'tools'/name).write_bytes((runtime.RUNTIME/name).read_bytes())
            (path/'tools/bench_bounded_io.py').write_bytes((ROOT/'benchmarks/samplingoptimisationgeometrybench/harbor/bench_bounded_io.py').read_bytes())
            for name in ('comparator','lean4export','landrun'):
                (path/'tools'/name).write_bytes(b'Unexecuted unit-test fixture, not a real runtime binary')
            image='sha256:'+'a'*64;(path/'image-id').write_text(image)
            receipt={'policy':runtime.policy(),'image_id':image,
                'tools':{p.name:runtime.bench.sha(p.read_bytes()) for p in (path/'tools').iterdir()}}
            (path/'preparation.json').write_bytes(runtime.bench.encoded(receipt))
            self.assertEqual(runtime.check_runtime(path),receipt)
            (path/'tools/container.py').write_text('changed')
            with self.assertRaises(ValueError):runtime.check_runtime(path)

    def test_runtime_receipt_cannot_omit_tools_or_smuggle_an_unlisted_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);(path/'tools').mkdir()
            image='sha256:'+'a'*64;(path/'image-id').write_text(image)
            (path/'preparation.json').write_bytes(runtime.bench.encoded({
                'policy':runtime.policy(),'image_id':image,'tools':{}}))
            with self.assertRaisesRegex(ValueError,'inventory'):runtime.check_runtime(path)
            for name in runtime.RUNTIME_TOOLS:(path/'tools'/name).write_bytes(b'fixture')
            (path/'tools/unlisted.py').write_bytes(b'not executed')
            (path/'preparation.json').write_bytes(runtime.bench.encoded({
                'policy':runtime.policy(),'image_id':image,
                'tools':{name:runtime.bench.sha(b'fixture') for name in runtime.RUNTIME_TOOLS}}))
            with self.assertRaisesRegex(ValueError,'inventory'):runtime.check_runtime(path)

    def test_docker_argv_has_only_readonly_binds_and_declared_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            argv=runtime.docker_command(image='sha256:'+'a'*64,name='sog-lean-fixture',
                stage_dir=path,submission=path,packages=path,toolchain=path,tools_dir=path)
            self.assertIn('--network=none',argv);self.assertIn('--read-only',argv)
            self.assertIn('--user=1000:1000',argv);self.assertIn('--cap-drop=ALL',argv)
            self.assertIn('--security-opt=no-new-privileges:true',argv)
            self.assertIn('--log-driver=none',argv);self.assertIn('--pids-limit=128',argv)
            env=[argv[i+1] for i,a in enumerate(argv) if a=='--env']
            self.assertEqual(set(env),{v+'=' for v in runtime.PROXY_VARIABLES})
            mounts=[argv[i+1] for i,a in enumerate(argv) if a=='--mount']
            self.assertEqual(len(mounts),5)
            self.assertTrue(all(m.endswith(',readonly') for m in mounts))
            self.assertFalse(any('docker.sock' in m for m in mounts))
        recipe=(runtime.RUNTIME/'Dockerfile').read_text()
        self.assertNotIn('useradd',recipe)
        self.assertIn('USER 1000:1000',recipe)

    def test_mutable_image_and_unowned_container_name_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for image,name in [('ubuntu:latest','sog-lean-fixture'),('sha256:'+'a'*64,'somebody-elses-container')]:
                with self.subTest(image=image,name=name),self.assertRaises(ValueError):
                    runtime.docker_command(image=image,name=name,stage_dir=Path(tmp),submission=Path(tmp),
                        packages=Path(tmp),toolchain=Path(tmp),tools_dir=Path(tmp))


class LeanWorkspaceTests(unittest.TestCase):
    def create(self,root,max_checks=1):
        task=root/'task';stage=root/'stage';prepared=root/'runtime'
        task.mkdir();stage.mkdir();prepared.mkdir();(task/'agent').mkdir()
        (task/'agent/prompt.json').write_text('{"question":"test prompt, no gold"}')
        (task/'oracle').mkdir();(task/'oracle/gold.txt').write_text('must not enter agent view')
        (task/'operator.json').write_text('{}');(prepared/'preparation.json').write_text('{}')
        (stage/'stage.json').write_bytes(runtime.bench.encoded({'id':'sogb-001','binding_sha256':'binding'}))
        output=root/'workspace'
        with patch.object(workspace.sys,'platform','linux'),patch.object(workspace.shutil,'which',return_value='docker'),\
             patch.object(runtime,'checked_packet',return_value=core()),patch.object(runtime,'check_runtime'):
            workspace.start(task=task,stage=stage,prepared=prepared,output=output,
                provenance={'kind':'controlled-software-fixture','name':'unexecuted unit fixture'},max_checks=max_checks)
        return output

    @staticmethod
    def fake_verifier(**kwargs):
        # Test only the recorder state machine, NOT Lean or native isolation.
        output=kwargs['output'];output.mkdir()
        result={'kind':'accepted','model_measurement':False}
        workspace.write_new(output/'result.json',result)
        (output/'compiler-diagnostic.bin').write_bytes(b'Unexecuted unit fixture; not real compiler feedback')
        return result

    def test_agent_view_never_copies_operator_or_oracle(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=self.create(Path(tmp))
            self.assertEqual([p.name for p in (output/'agent').iterdir()],['prompt.json'])
            self.assertFalse((output/'oracle').exists())
            manifest,events=workspace.history(output)
            self.assertEqual(manifest['denominator'],1);self.assertEqual(events,[])

    def test_check_acceptance_without_final_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(runtime,'run_submission',side_effect=self.fake_verifier):
            output=self.create(Path(tmp))
            feedback=workspace.act(output,{'action':'check','source':'not executed by unit test'})
            self.assertEqual(feedback['kind'],'accepted');self.assertFalse(feedback['final'])
            result=workspace.close(output)
            self.assertEqual(result['final_outcome'],'no-final-submission')
            self.assertEqual(result['denominator'],1);self.assertFalse(result['final_accepted'])

    def test_bounded_tools_then_first_final_is_immutable(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(runtime,'run_submission',side_effect=self.fake_verifier):
            output=self.create(Path(tmp))
            workspace.act(output,{'action':'check','source':'check source'})
            with self.assertRaisesRegex(ValueError,'budget'):workspace.act(output,{'action':'check','source':'second check'})
            workspace.act(output,{'action':'submit','source':'final source'})
            for action in ('check','submit'):
                with self.assertRaisesRegex(ValueError,'final'):workspace.act(output,{'action':action,'source':'replacement'})
            result=workspace.close(output)
            self.assertTrue(result['final_accepted']);self.assertEqual(result['check_calls'],1)
            self.assertEqual(result['final_submissions'],1);self.assertFalse(result['model_measurement'])
            with self.assertRaises(FileExistsError):workspace.close(output)

    def test_invalid_final_stays_selected_and_is_not_executed(self):
        for source,reason in [(None,'missing-or-nontext-source'),('x'*65537,'too-large'),('\ud800','invalid-utf8')]:
            with self.subTest(reason=reason),tempfile.TemporaryDirectory() as tmp,\
                 patch.object(runtime,'run_submission',side_effect=AssertionError('No execution of invalid source')):
                output=self.create(Path(tmp));feedback=workspace.act(output,{'action':'submit','source':source})
                self.assertEqual(feedback['kind'],'invalid-submission');self.assertEqual(feedback['reason'],reason)
                result=workspace.close(output)
                self.assertEqual(result['denominator'],1);self.assertEqual(result['final_outcome'],'invalid-submission')

    def test_interrupted_final_cannot_be_silently_retried_or_counted_as_proof_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=self.create(Path(tmp))
            with patch.object(runtime,'run_submission',side_effect=RuntimeError('simulated operator interruption')):
                with self.assertRaises(RuntimeError):workspace.act(output,{'action':'submit','source':'reserved final'})
            with self.assertRaises(ValueError):workspace.act(output,{'action':'submit','source':'retry'})
            result=workspace.close(output)
            self.assertEqual(result['final_outcome'],'infrastructure-error');self.assertTrue(result['interrupted'])
            self.assertEqual(result['denominator'],1)

    def test_sequential_lock_rejects_concurrent_call_without_removing_foreign_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=self.create(Path(tmp));lock=output/'operation.lock';lock.write_bytes(b'existing owner')
            with self.assertRaises(FileExistsError):workspace.act(output,{'action':'submit','source':'unused'})
            self.assertEqual(lock.read_bytes(),b'existing owner')

    def test_fixed_protocol_rejects_command_target_and_path_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=self.create(Path(tmp))
            for request in [{'action':'shell','source':'do not run'},
                    {'action':'check','source':'unused','command':'do not run'},
                    {'action':'submit','source':'unused','task':'other-task'},
                    {'action':'submit','path':'C:/not-an-agent-file'}]:
                with self.subTest(request=request),self.assertRaises(ValueError):workspace.act(output,request)
            self.assertEqual(workspace.history(output)[1],[])

    def test_request_envelope_is_bounded_and_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'request.json'
            source.write_bytes(b'{"action":"check","action":"submit"}')
            with self.assertRaisesRegex(ValueError,'Duplicate'):workspace.read_request(source)
            source.write_bytes(b'x'*(workspace.REQUEST_BYTES+1))
            with self.assertRaisesRegex(ValueError,'too-large'):workspace.read_request(source)

    def test_source_and_result_drift_are_detected(self):
        for changed in ('source.txt','verification/result.json'):
            with self.subTest(changed=changed),tempfile.TemporaryDirectory() as tmp,\
                 patch.object(runtime,'run_submission',side_effect=self.fake_verifier):
                output=self.create(Path(tmp));workspace.act(output,{'action':'submit','source':'recorded source'})
                (output/'actions/0001'/changed).write_text('changed')
                with self.assertRaises(ValueError):workspace.history(output)


if __name__=='__main__':unittest.main()
