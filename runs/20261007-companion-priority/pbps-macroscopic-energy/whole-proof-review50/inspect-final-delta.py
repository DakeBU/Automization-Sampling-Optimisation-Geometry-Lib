# coding: utf-8
import pathlib,difflib,sys
sys.stdout.reconfigure(encoding='utf-8');R=pathlib.Path('.');a=(R/'runs/20261007-companion-priority/pbps-macroscopic-energy/production.2.source.raw.snapshot.lean').read_text(encoding='utf-8');b=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean').read_text(encoding='utf-8');print(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='production2snapshot',tofile='finalfrozen')))
