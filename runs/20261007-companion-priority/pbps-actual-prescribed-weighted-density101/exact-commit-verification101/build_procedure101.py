from context101 import *
dispatch=dict(explicit_root_dispatch=True,science_commit='4808820b06e696524a9bd45b8d61f615f592999b',baseline_commit='1dda6b4bbcdcd3b3131d86a5d90e5f9743e250b3',final_source_and_coverage_ready=True,source_native=rel(B/'final-source101/source-review101.native.json'),coverage=rel(B/'final-source101/compiled-source-coverage101.native.json'),authorizes_one_native_VERIFIED_and_only101_cell_update_after_all_PASS=True,excluded_scope='next-primary102')
assert head()==dispatch['science_commit']
save('root-freeze-dispatch101.native.json',dispatch)
old=O.parent.parent/'pbps-actual-prescribed-path-reversal100/exact-commit-verification100/verify100.py'
t=old.read_text(encoding='utf8');core=t[t.index("if __name__=='__main__':"):t.index(" dec=R/'runs/semantic-roundtrip/anonymous100/decoder-native'")]
core=core.replace('100','101')
core=core.replace("len(stage['files'])==195 and len(scoped)==196","len(stage['files'])==192 and len(scoped)==193")
core=core.replace('pbps-actual-prescribed-state-reversal99/exact-commit-verification99/closed-RAW-manifest99.json','pbps-actual-prescribed-path-reversal100/exact-commit-verification100/closed-RAW-manifest100.json')
core=core.replace('next-primary101','next-primary102')
core=core.replace('59d3131209605d2df34e74abb098f42d41338ae44f7e4f4bee4d75ac7bc0a3c8','b9c6e8ed0655b9c607eff38ecf74eb3a4555ff90184475e8dfc554bb96dcb3c0')
core=core.replace('dd6966262cfe6fde662bbbc41e9265ea72f5d542d8a7d4b6b61af8637eb2ff2b','d208b02fc4c21700d99cf69bc55af3f0b8c71cc7a440901abc2bc7a854d39343')
core=core.replace('830f6b01d3d82168085e7e081a123c3152043090ebd7f0b91410e076cb96c108','cdd05195156722be3b65c56fc09fe48971e021df81afadb48968dbab50c81d59')
core=core.replace('history_rows=[];unresolved=[]','history_rows=[];span_rows=[];unresolved=[]')
needle="    if (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)"
replacement="""    if (R/p).is_file() and 'line_start' in v and 'line_end' in v:
     rawlines=(R/p).read_bytes().splitlines(keepends=True);segment=b''.join(rawlines[v['line_start']-1:v['line_end']])
     assert sha(segment)==h,('source span RAW mismatch',v)
     exact(p);span_rows.append(v)
    elif (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)"""
assert needle in core;core=core.replace(needle,replacement)
prefix="from context101 import *\nimport gzip\ndispatch=frozen_dispatch();C=dispatch['science_commit'];BASE=dispatch['baseline_commit']\nPRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'\n"
(O/'verify101.py').write_text(prefix+core,encoding='utf8',newline='\n')
print('Prepared exact101 archive/math binding procedure; source/schema-specific checks to be appended before execution.')
