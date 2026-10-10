from pathlib import Path
import subprocess,json,hashlib,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent/'ci-reader-order-repair86';r.mkdir(exist_ok=True)
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
observations=[]
for label,args in [('list',['gh','run','list','--branch','codex/sphmc-standardized-rgo','--limit','8','--json','databaseId,headSha,name,status,conclusion,url']),('contributor',['gh','run','view','38082954355','--log-failed']),('site',['gh','run','view','38082954327','--log-failed']),('lean',['gh','run','view','38082954278','--log-failed'])]:
 q=subprocess.run(args,cwd=R,capture_output=True)
 p=r/(label+'.remote.stdout.log');p.write_bytes(q.stdout);e=r/(label+'.remote.stderr.log');e.write_bytes(q.stderr)
 observations.append({'argv':args,'exit_code':q.returncode,'stdout':pin(p),'stderr':pin(e)});assert q.returncode==0
p=R/'tools/tests/test_astis_publication.py';before=p.read_bytes();(r/'test.before.exactraw.snapshot').write_bytes(before)
s=before.decode('utf-8')
old="markers = ['Mathematical proof', 'Lean statement ·', 'Lean proof ·',"
replacement="markers = ['Lean statement ·', 'Proof roadmap',\n                       'Full assumptions and notation', 'Mathematical proof', 'Lean proof ·',"
assert s.count(old)==1;s=s.replace(old,replacement)
marker='    def test_new_default_harness_schema_requires_publication(self):'
test='''    def test_literal_proposition_and_proof_helpers_keep_distinct_reader_positions(self):
        import declaration_lessons as lessons
        import inline_lean
        import re
        name = ('AutoSamplingTheory.ExampleCases.ProximalBPS.'
                'ActualFiniteFirstEventLaw.actual_finite_first_event_law')
        unit = next(u for u in lessons.load_units() if u['declaration'] == name)
        text = lessons.render_unit(unit, lessons.lesson_path(name))
        statement = f'class="inline-lean inline-lean-statement" data-inline-lean="{name}"'
        proof = f'class="inline-lean inline-lean-proof" data-inline-lean="{name}"'
        literal = name + '_statement'
        literal_panel = f'class="inline-lean inline-lean-proof" data-inline-lean="{literal}"'
        positions = [text.index(statement), text.index(literal_panel),
                     text.index('Proof roadmap'), text.index('Mathematical proof'),
                     text.index(proof)]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('Full Lean proposition (definition)', text)
        # The full proposition is a sibling of the signature, so it is
        # independently reachable before the roadmap, without opening a proof.
        signature_end = text.index('</details>', text.index(statement))
        self.assertLess(signature_end, text.index(literal_panel))
        self.assertEqual(text.count(literal_panel), 1)
        for helper in unit['helpers']:
            panel = f'class="inline-lean inline-lean-proof" data-inline-lean="{helper}"'
            self.assertEqual(text.count(panel), 1)
            if helper != literal:
                self.assertGreater(text.index(panel), text.index(proof))
        self.assertEqual(text.count('<summary>Corresponding Lean step</summary>'),
                         len(unit['steps']))
        self.assertNotRegex(text, r'<details\\b[^>]*\\bopen(?:\\s|=|>)')

'''
assert s.count(marker)==1;s=s.replace(marker,test+marker)
out=r/'test.proposed.exactraw.snapshot';out.write_bytes(s.encode('utf-8'))
new(r/'proposal86.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_commit':'f62dca7500b1fa035ef7b377ac55e182ea3fd057','before':pin(r/'test.before.exactraw.snapshot'),'proposed':pin(out),'remote_observations':observations,'diagnosis':'All three exact-head remote workflows fail the same outdated order assertion after independently reviewed V4 renderer intentionally moved Lean signature and full literal Prop before proof roadmap. Lean source and reviewed mathematics unchanged. Remote Lean did not reach a theorem build success claim.','repair':'Align the existing order test with statement→roadmap→assumptions→mathematical proof→Lean proof; retain comparison/provenance checks, and add actual86 regression for full Prop sibling, all five proof helpers exactly once, all eleven step disclosures and initially folded panels. No renderer/math/metadata/evidence status change.','requires_independent_repair_review_before_apply':True,'canonical_shared_files_changed':False})
print(json.dumps(pin(out)))
