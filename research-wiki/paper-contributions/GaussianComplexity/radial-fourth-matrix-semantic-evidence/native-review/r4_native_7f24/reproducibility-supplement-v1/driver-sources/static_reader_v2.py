from bootstrap import *
source=pathlib.Path(__file__).with_name('static_reader_v1.py').read_text()
source=source.replace("out=ROOT/'bounded-render'", "out=ROOT/'bounded-render-v2'\n(out/'textbook').mkdir(parents=True,exist_ok=True)\n(out/'textbook/index.html').write_text(site.page('Bounded theme carrier','textbook/index.html','',extra_head='<link rel=\"stylesheet\" href=\"../assets/information-architecture.css\">'))")
source=source.replace("No whole-site or browser claim.", "A production base-page theme carrier supplies source_lineage's canonical-theme precondition; it is not a built textbook/source index. No whole-site, CSS-layout or browser claim.")
exec(compile(source, str(pathlib.Path(__file__)), 'exec'))
