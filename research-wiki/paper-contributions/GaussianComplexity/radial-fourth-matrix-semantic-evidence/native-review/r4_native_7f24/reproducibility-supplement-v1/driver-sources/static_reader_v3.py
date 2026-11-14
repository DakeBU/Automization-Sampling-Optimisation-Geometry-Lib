from bootstrap import *
wrapper=pathlib.Path(__file__).with_name('static_reader_v2.py').read_text().replace("source_lineage's",'source_lineage canonical')
wrapper=wrapper.replace("bounded-render-v2","bounded-render-v3")
exec(compile(wrapper,str(pathlib.Path(__file__)),'exec'))
