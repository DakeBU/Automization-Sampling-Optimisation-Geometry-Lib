import pathlib
p=pathlib.Path(__file__).with_name('final-preclose-check.py')
s=p.read_text(encoding='utf-8').replace("raw=(O/a['path']).read_bytes();assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes']\nassert len(checkpoint", "raw=(O/a['name']).read_bytes();assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes']\nassert len(checkpoint")
exec(compile(s,str(p),'exec'))
