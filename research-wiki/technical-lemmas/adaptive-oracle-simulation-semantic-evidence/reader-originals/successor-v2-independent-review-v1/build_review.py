"""Independent review of completed artifacts only. Never launches browser/server/API/Git."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import ast
import datetime as dt
import hashlib
import json
import re
import struct

OWN=Path(__file__).resolve().parent
ACTOR=OWN.parent
RUN=ACTOR/'successor-v2-runtime'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def dump(p,v):
    Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

r=load(RUN/'actual-result.json')
a=load(RUN/'execution-assignment.ROOT.actual-v2.json')
assert sha(RUN/'actual-result.json')=='da29a2e155e55e9c198bbf6f33013489283ab6668b8b5d82c1e9ec8157a4392e'
assert sha(RUN/'execution-assignment.ROOT.actual-v2.json')=='a291b00199047560b54dd2f1480d1d94cc30f748770c2d418a4be99d67d0e2f9'
preview=Path(a['preview_root']);fixture=preview/'fixtures/candidate';snapshot=preview/'input-snapshot'
by={c['name']:c['detail'] for c in r['checks']}
review=[]
def check(name,ok,detail=None):
    review.append({'name':name,'pass':bool(ok),'detail':detail})

receipt=load(RUN/'runtime-process/receipt.json')
check('real-OS-process-bound-exit0',receipt['actual_exit_code']==0 and receipt['exception'] is None and receipt['actual_OS_fd1_fd2_until_exit'] and receipt['actual_result_sha256']==sha(RUN/'actual-result.json') and receipt['assignment_sha256']==sha(RUN/'execution-assignment.ROOT.actual-v2.json'))
for name in ['stdout','stderr']:
    p=RUN/receipt[name]['path']
    check('actual-OS-'+name+'-bytes-and-hash',p.stat().st_size==receipt[name]['bytes'] and sha(p)==receipt[name]['sha256'])
check('exact-stdout165-stderr0',receipt['stdout']['bytes']==165 and receipt['stdout']['sha256']=='b41926bf509c5e09e3e41c9c1ec6e745f2c09fb0e6e5d1286f762a6edbc0a22f' and receipt['stderr']['bytes']==0)
old=load(ACTOR/'actual-result.json')
check('original485-check-names-all-retained',not(Counter(c['name'] for c in old['checks'])-Counter(c['name'] for c in r['checks'])),{'original':len(old['checks']),'new':len(r['checks'])})
check('original-FAIL-preserved',old['status']=='FAIL' and sha(ACTOR/'actual-result.json')=='f7e3488bdca1e854664f1eb2e91f48169e554293964ed5019915a792ceb01578')
check('runtime514-records-no-false',len(r['checks'])==514 and not [c for c in r['checks'] if not c['pass']])
check('all24-frozen-inputs-still-exact',len(a['frozen_inputs'])==24 and all(sha(row['path'])==row['sha256'] for row in a['frozen_inputs']))
m=load(preview/'preview-freeze-manifest.json')
check('actual104-fixture-bytes-still-exact',len(m['variants']['candidate']['files'])==104 and all(sha(fixture/x['path'])==x['sha256'] for x in m['variants']['candidate']['files']))
freeze=load(preview/'input-freeze-manifest.json')
check('all118-input-snapshot-hashes-still-exact',len(freeze['files'])==118 and all(sha(snapshot/x['path'])==x['sha256'] for x in freeze['files']))

# Reuse only the static HTML parser classes, never its checks, writes or verdict.
tree=ast.parse((ACTOR/'preflight.py').read_text())
ns={'HTMLParser':HTMLParser,'Path':Path}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name in ['Node','Document']],type_ignores=[]),'static-parser-classes','exec'),ns)
Document=ns['Document']
item='huanjian-adaptive-oracle-simulation'
PFILE='AutoSamplingTheory/TechnicalLemmas/Probability/AdaptiveOracleSimulation.lean'
TFILE='Tests/GaussianComplexityAdaptiveFirstOrderSimulation.lean'
P='AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation.measurable_simulation_joint_law_and_cost'
T='AutoSamplingTheory.Tests.GaussianComplexityAdaptiveFirstOrderSimulation.actual_fixed_spectrum_first_order_matvec_joint_laws_and_costs'
RUNDECL='AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle.run'
FO='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query'
sources=[('P',PFILE,P,93,170),('T',TFILE,T,21,118),('RUN','AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularizationOracle.lean',RUNDECL,18,62),('FO','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumFirstOrder.lean',FO,30,92)]
unit=load(snapshot/'website/content/declaration_lessons'/f'{item}.json')['units'][0]
for raw in [m['variants']['candidate']['proof_path'],m['variants']['candidate']['lesson_path']]:
    doc=Document(fixture/raw);article=doc.root.descendants('article','proof-reader')[0]
    steps=article.descendants('details','proof-reader-step')
    codes=[s.descendants('pre','code-block')[0].descendants('code')[0].text for s in steps]
    check('static-current-five-exact-spans:'+raw,len(codes)==5 and codes==[s['lean'] for s in unit['steps']] and ''.join(codes[:4]).encode()==(snapshot/PFILE).read_bytes() and codes[4].encode()==(snapshot/TFILE).read_bytes())
    check('static-current-initial-folds-and-formula:'+raw,all('open' not in d.attrs for d in article.descendants('details')) and unit['formula'] in article.descendants(cls='reader-main-equation')[0].text)
download_paths=[]
for tag,raw,decl,anchor,nlines in sources:
    exact=(snapshot/raw).read_bytes();doc=Document(fixture/'data/lesson-sources'/f'{raw}.html')
    pre=doc.root.descendants('pre')[0]
    check('static-four-whole-source-pages:'+tag,pre.text.encode()==exact and len(pre.descendants('span'))==nlines and doc.ids['L'+str(anchor)].text.strip().startswith(('private theorem ' if tag=='T' else 'def ' if tag=='RUN' else 'theorem ')+decl.split('.')[-1]))
    check('served-four-whole-source-downloads:'+tag,(fixture/'downloads/lean'/raw).read_bytes()==exact)
for label in ['desktop','mobile']:
    pairs=[(f'{label}-step{i+1}-whole-module.lean',s['lean_source_path']) for i,s in enumerate(unit['steps'])]
    pairs += [(f'{label}-source-{tag}-whole-module.lean',raw) for tag,raw,_,_,_ in sources]
    pairs += [(f'{label}-private-T-module-context-download.lean',TFILE)]
    for name,raw in pairs:
        p=RUN/'runtime-output'/name;download_paths.append(p)
        check('actual-download-byte-recompute:'+name,p.read_bytes()==(snapshot/raw).read_bytes(),{'sha256':sha(p)})

anchors=[]
for t in r['natural_source_anchor_stability_traces']:
    samples=t['samples'];tail=samples[-4:]
    def sig(s):
        g=s['geometry'];p=s['pre_scroll'] or {'left':0,'top':0}
        return [s['window_scroll']['x'],s['window_scroll']['y'],p['left'],p['top'],*[g[k] for k in ['left','right','top','bottom']],g['header'],*[g['clip'][k] for k in ['left','right','top','bottom']]]
    maximum=max(max(z)-min(z) for z in zip(*(sig(s) for s in tail)))
    g=samples[-1]['geometry'];stable=len(tail)==4 and samples[-1]['elapsed_ms']>=500 and maximum<=.25
    iw=max(0,min(g['right'],g['clip']['right'])-max(g['left'],g['clip']['left']))
    ih=max(0,min(g['bottom'],g['clip']['bottom'])-max(g['top'],g['clip']['top']))
    visible=iw>0 and ih>0 and g['top']>=g['header']-1
    check('raw-anchor:'+t['case'],stable and visible)
    anchors.append({'case':t['case'],'samples':len(samples),'elapsed_ms':samples[-1]['elapsed_ms'],'tail_max_delta_css_px':maximum,'settled_top':g['top'],'header':g['header'],'strict_recomputed':stable and visible})
check('all18-natural-anchor-traces-retained',len(anchors)==18)

glyphs=[];graph_measurements=[];layouts=[]
for c in r['checks']:
    name=c['name'];g=c['detail']
    if name.endswith(('widest-line-final-full-codepoint-visible','bottom-full-codepoint-visible')):
        box=g['glyph'];clip=g['actualVisibleClip']
        ok=box['width']>0 and box['height']>0 and box['left']>=clip['left']-1 and box['right']<=clip['right']+1 and box['top']>=clip['top'] and box['bottom']<=clip['bottom']
        tag=name.split('-')[1];raw=next(x[1] for x in sources if x[0]==tag)
        line=(snapshot/raw).read_text().splitlines()[int(g['lineId'][1:])-1].rstrip()
        exact_glyph=bool(line) and line[-1]==g['selectedGlyph'] and [ord(ch) for ch in g['selectedGlyph']]==g['codePoints']
        check('raw-source-glyph:'+name,ok and exact_glyph and g['lineVisible'])
        glyphs.append({'name':name,'line_id':g['lineId'],'glyph':g['selectedGlyph'],'range':box,'clip':clip,'full_codepoint_and_geometry_recomputed':ok and exact_glyph})
    if name.endswith('all-source-lines-have-real-layout'):
        tag=name.split('-')[1];expected=next(x[4] for x in sources if x[0]==tag)
        check('raw-line-layout:'+name,len(g)==expected and all(x['lineHeight']>0 for x in g))
    if name.endswith('readable-node-core-label-inside-real-SVG-clip'):
        q=g['after_native_UI'];ok=q['positiveSVGClippedIntersection'] and q['intersectionFraction']>=.98 and q['labelVisibleFraction']>=.95 and q['effectiveFontPx']>=12 and q['labelIntersection']['width']>=min(80,q['labelRect']['width']) and q['labelIntersection']['height']>=min(12,q['labelRect']['height'])
        pointer=any('native_pointer' in x for x in g['interactions']);wheel=any('native_wheel' in x for x in g['interactions'])
        check('raw-graph-clipped-font:'+name,ok and pointer and wheel)
        graph_measurements.append({'name':name,'node_fraction':q['intersectionFraction'],'label_fraction':q['labelVisibleFraction'],'effective_font_px':q['effectiveFontPx'],'native_pointer_and_wheel':pointer and wheel,'recomputed':ok})
    if name.endswith('formal-solid-reference-dashed-arrows'):
        check('raw-graph-solid-dashed-arrows:'+name,len(g)==9 and sum(x['formal'] and x['dash']=='none' for x in g)==6 and sum(x['overlay'] and x['dash']!='none' for x in g)==3 and all(x['arrow'] for x in g))
    if name.endswith('exact-neighbor-directions'):
        check('raw-graph-neighbor-directions:'+name,sorted(g['actual'])==sorted(g['expected']))
    if name.endswith(('right-reachable-if-overflow','source-table-right-reachable')):
        check('raw-local-right-reach:'+name,g['max']<=1 or (g['actual']>=g['max']-1 and g['overflow'] in ['auto','scroll']))
    if name.endswith('document-horizontal-containment'):
        check('raw-layout:'+name,g['html']<=g['viewport']+1 and g['body']<=g['viewport']+1)
        layouts.append({'name':name,**g})
check('16-source-glyphs-and8-graph-focuses',len(glyphs)==16 and len(graph_measurements)==8)

graph=load(fixture/'data/underlying-lean-graph.json');modules=[s[1][:-5].replace('/','.') for s in sources]
node_ids={'module:'+x for x in modules}|{'decl:'+sources[i][2] for i in [0,2,3]}
edges={('module:'+modules[2],'module:'+modules[0],'imports')}|{('module:'+modules[i],'module:'+modules[1],'imports') for i in [0,3]}|{('module:'+modules[i],'decl:'+sources[i][2],'declares') for i in [0,2,3]}|{('decl:'+RUNDECL,'decl:'+P,'source reference (scanner)')}|{('decl:'+sources[i][2],'module:'+modules[1],'source reference (scanner)') for i in [0,3]}
check('independent-exact7nodes9edges-private-T-not-public',len(graph['nodes'])==7 and {n['id'] for n in graph['nodes']}==node_ids and len(graph['edges'])==9 and {(e['source'],e['target'],e['relation']) for e in graph['edges']}==edges and not any(T in n['id'] for n in graph['nodes']))

inline=[]
for label in ['desktop','mobile']:
    prefix=label+'-inline-regression-'
    before=by[prefix+'parent-content-bound'];after=by[prefix+'all-visible-glyphs-vertical-containment-after-scroll']
    def vertical(x):
        return len(x['visibleGlyphBoxes'])==31 and all(g['rect']['top']>=g['geometry']['clip']['top'] and g['rect']['bottom']<=g['geometry']['clip']['bottom'] for g in x['visibleGlyphBoxes'])
    check('raw-inline-both-states-all31-visible-glyphs-vertical:'+label,vertical(before) and vertical(after))
    check('raw-inline-visible-glyph-sequence-retained:'+label,[g['className'] for g in before['visibleGlyphBoxes']]==[g['className'] for g in after['visibleGlyphBoxes']])
    tail=after['lastVisibleGlyph'];b=tail['rect'];clip=tail['geometry']['clip']
    tail_ok='mjx-c22A4' in tail['className'] and b['width']>0 and b['height']>0 and b['left']>=clip['left']-1 and b['right']<=clip['right']+1 and b['top']>=clip['top'] and b['bottom']<=clip['bottom']
    check('raw-inline-final-visible-transpose-in-clip:'+label,tail_ok)
    check('raw-inline-local-scroll-actually-reached-max:'+label,after['maxScrollLeft']>1 and after['scrollLeft']>0 and abs(after['scrollLeft']-after['maxScrollLeft'])<=1)
    check('raw-inline-owned-parent-content-bound:'+label,before['rect']['left']>=before['parent']['contentLeft']-1 and before['rect']['right']<=before['parent']['contentRight']+1 and before['rect']['width']<=before['parent']['contentWidth']+1)
    font=float(before['computed']['fontSize'].removesuffix('px'));parent_font=float(before['parent']['fontSize'].removesuffix('px'))
    check('raw-inline-original-font-preserved:'+label,abs(font-parent_font*1.089)<=.001 and font>=17.424-.001 and after['computed']['fontSize']==before['computed']['fontSize'])
    initial_rows=by[prefix+'exact-matrix-formula-unique']['native_formulas']
    final_data=by[prefix+'all-assumption-native-MathML-retained-and-available'];final_rows=final_data['all_root_native_math_audits']
    semantic_ok=bool(final_rows) and len(final_rows)==len(initial_rows) and [[z['text'] for z in row] for row in final_rows]==[[z['text'] for z in row] for row in initial_rows]
    semantic_ok=semantic_ok and all(row and all(z['text'].strip() and z['namespace']=='http://www.w3.org/1998/Math/MathML' and all(q['display']!='none' and q['visibility']!='hidden' and q['ariaHidden']!='true' for q in z['ancestry']) for z in row) for row in final_rows)
    check('raw-all-assumption-MathML-text-namespace-availability:'+label,semantic_ok)
    check('raw-target-MathML-before-after-exact:'+label,[z['text'] for z in before['nativeMathML']]==[z['text'] for z in after['nativeMathML']] and bool(before['nativeMathML']))
    inline.append({'viewport':label,'clientWidth':after['clientWidth'],'scrollWidth':after['scrollWidth'],'actual_scrollLeft':after['scrollLeft'],'max_scrollLeft':after['maxScrollLeft'],'font_px':font,'parent_font_px':parent_font,'normalizedFormula':after['normalizedFormula'],'all31_visible_glyphs_vertically_inside_clip':vertical(before) and vertical(after),'final_visible_transpose':tail,'native_MathML_assumption_roots':len(final_rows),'native_MathML_instances':sum(len(x) for x in final_rows),'all_native_MathML_text_and_availability_recomputed':semantic_ok})
check('mobile-expanded-body390',by['mobile-proof-expanded-document-horizontal-containment']=={'viewport':390,'html':390,'body':390} and by['mobile-inline-regression-expanded-document-horizontal-containment']=={'viewport':390,'html':390,'body':390})

network={'requests':len(r['requests']),'responses':len(r['responses']),'origins':sorted(set(x['url'].split('/')[2] for x in r['requests'] if x['url'].startswith('http'))),'HTTP_errors':[x for x in r['responses'] if x['status']>=400],'console_errors':[x for x in r['console'] if x['type']=='error'],'page_errors':r['page_errors'],'blocked_external_requests':r['blocked_external_requests']}
check('raw-network-errors-zero-and-local-only',len(network['origins'])==1 and network['origins'][0].startswith('127.0.0.1:') and not any(network[k] for k in ['HTTP_errors','console_errors','page_errors','blocked_external_requests']))

screens=[]
for row in r['screenshots']:
    p=RUN/row['path'];raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
    w,h=struct.unpack('>II',raw[16:24]);check('PNG-exact-hash:'+p.name,sha(p)==row['sha256'])
    name=p.stem
    if 'inline-regression' in name:
        note='Actually viewed in this run: formula stays in its assumption row; local before/right-end views expose the complete transpose endpoint after scroll, with legible original-sized symbols and no visible vertical cut.'
    elif 'initial-folded' in name:
        note='Actually viewed in this run: concise rendered main formula and clear statement/proof hierarchy; conditions, proof steps and adjacent Lean closed initially; narrow layout has formula-scroll cue.'
    elif 'representative-step' in name:
        note='Actually viewed in this run: mathematical step prose/formula and adjacent Lean disclosure are clear; mobile code remains in its own bounded panel.'
    elif 'assumption-comparison' in name:
        note='Actually viewed in this run: comparison columns are legible; mobile shot intentionally shows the right side after internal table scroll, within its container.'
    elif 'module-full-source-context' in name:
        note='Actually viewed in this run: complete-module entrance and bounded code panel are legible; viewport shows part of the full source, whose entirety is separately byte-checked.'
    elif 'widest-right-glyph' in name:
        note='Actually viewed in this run: retained internal source scroll exposes the widest line ending; blank space on shorter lines is expected at this scroll position.'
    elif 'source-T-bottom' in name:
        note='Actually viewed in this run: final namespace/source ending is visible above the footer.'
    elif '-source-' in name and '-anchor' in name:
        note='Actually viewed in this run: correct declaration beginning is naturally below the header; source stays within its horizontal source region.'
    elif 'source-index' in name:
        note='Actually viewed in this run: all four exact source identities wrap legibly; associated private T explicitly has no public-node credit.'
    elif 'parent-context' in name:
        note='Actually viewed in this run: public run parent and the private two-direction application are distinct; source-reference limitation is readable.'
    elif 'actual-node-viewport' in name:
        note='Actually viewed in this run: selected core label and directed solid/dashed connections are legible within actual SVG clip; long labels remain ellipsized as disclosed.'
    elif 'full-ID-detail' in name:
        note='Actually viewed in this run: exact full identity wraps legibly in detail with context entrance and directed-neighbor cards.'
    else:
        raise RuntimeError(name)
    screens.append({**row,'actor_relative_path':str(p.relative_to(ACTOR)),'width':w,'height':h,'independently_viewed_this_actual_run':True,'observation':note})
check('all50-PNGs-independently-viewed-and-bound',len(screens)==50 and sum(x['path'].startswith('runtime-output/desktop') for x in screens)==23 and sum(x['path'].startswith('runtime-output/mobile') for x in screens)==27)
measurement={'schema':'r18-v2-independent-reader-measurements-v1','actual_result_sha256':sha(RUN/'actual-result.json'),'checks':review,'anchor_traces':anchors,'source_glyphs':glyphs,'graph_measurements':graph_measurements,'inline_regression':inline,'document_layouts':layouts,'network':network,'screenshots':screens,'interaction_evidence_scope':'All retained geometry and saved downloads were independently recomputed. Clipboard and some navigation/DOM equality checks retain runner assertions rather than captured clipboard/DOM text; exact reviewed runner, frozen fixture bytes, actual artifacts and actual screenshots were inspected together. No new browser run was made.','remaining_reader_residuals':[]}
dump(OWN/'measurements.v1.json',measurement)
failures=[c for c in review if not c['pass']]
summary={'independent_checks':len(review),'false':failures,'actual_PNGs_viewed':len(screens),'raw_anchor_traces':len(anchors),'source_glyphs':len(glyphs),'graph_focuses':len(graph_measurements),'inline_regression':[{k:v for k,v in x.items() if k!='final_visible_transpose'} for x in inline],'network':network,'measurements_sha256':sha(OWN/'measurements.v1.json')}
dump(OWN/'recompute-summary.v1.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
