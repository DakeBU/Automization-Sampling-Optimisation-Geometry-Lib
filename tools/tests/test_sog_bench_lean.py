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
        self.assertEqual(runtime.classify(30,{**native,'diagnostic_limit':True},state,None),'resource-limit')

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
        for kind,code in [('accepted',0),('proof-rejected',10),('resource-limit',30),('infrastructure-error',20)]:
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


if __name__=='__main__':unittest.main()
