from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import sog_bench_lean as runtime


def core():
    return {'id':'sogb-001','family':'fixture','split':'public-dev','binding_sha256':'binding',
        'imports':['Mathlib.Data.Nat.Basic'],'source_file':'AutoSamplingTheory/Fixture.lean',
        'lean_task':'import Mathlib.Data.Nat.Basic\nexample : 1 = 1 := by\n  -- Replace this comment with your proof.\n',
        'lean_reference':'import Mathlib.Data.Nat.Basic\nexample : 1 = 1 := by\n  rfl\n'}


class LeanRuntimeTests(unittest.TestCase):
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
