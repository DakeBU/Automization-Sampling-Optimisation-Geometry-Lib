import pathlib
p=pathlib.Path(__file__).with_name('stageB-finite-audit.py')
s=p.read_text(encoding='utf-8').replace("s['lean'].encode()==raw.rstrip(b'\\n')", "s['lean'].encode()==raw")
exec(compile(s,str(p),'exec'))
