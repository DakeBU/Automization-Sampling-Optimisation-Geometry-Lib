from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, re, html, datetime

OUT = Path(__file__).resolve().parent
SOURCE = Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
EXPECTED = 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
raw = SOURCE.read_bytes()
assert len(raw) == 1482128
assert hashlib.sha256(raw).hexdigest() == EXPECTED
text = raw.decode('utf-8')
line_starts = [0] + [m.end() for m in re.finditer('\n', text)]

class Index(HTMLParser):
    void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack=[]; self.nodes=[]
    def absolute_pos(self):
        line,col=self.getpos(); return line_starts[line-1]+col
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs); start=self.absolute_pos()
        n={'tag':tag,'attrs':attrs,'start':start,'start_line':self.getpos()[0]}
        if tag in self.void:
            n['end']=start+len(self.get_starttag_text()); self.nodes.append(n)
        else:
            self.stack.append(n)
    def handle_startendtag(self,tag,attrs):
        n={'tag':tag,'attrs':dict(attrs),'start':self.absolute_pos(),'start_line':self.getpos()[0]}
        n['end']=n['start']+len(self.get_starttag_text()); self.nodes.append(n)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:
                n=self.stack.pop(i); n['end']=text.index('>',self.absolute_pos())+1
                self.nodes.append(n); return

index=Index(); index.feed(text)
nodes={n['attrs']['id']:n for n in index.nodes if 'id' in n['attrs']}
def digest(b): return hashlib.sha256(b).hexdigest()
def render(s):
    maths=[]
    def save_math(m):
        maths.append(' $'+html.unescape(m.group(1))+'$ ')
        return ' MATHPLACEHOLDER'+str(len(maths)-1)+'END '
    s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[\s\S]*?</math>',save_math,s)
    s=re.sub(r'</(?:p|div|tr|table|h[1-6]|li|section|figcaption)>','\n',s)
    s=re.sub(r'<br\b[^>]*>','\n',s)
    s=re.sub(r'<[^>]+>','',s)
    s=html.unescape(s)
    s=re.sub(r'MATHPLACEHOLDER(\d+)END',lambda m:maths[int(m.group(1))],s)
    s='\n'.join(' '.join(line.split()) for line in s.splitlines())
    return re.sub('\n{3,}','\n\n',s).strip()+'\n'
def write_json(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

(OUT/'primary-pbps.exactraw.snapshot.html').write_bytes(raw)
fragments=[]
for node_id in ['S1','S1.p1','S2','S3.SS2','A1.SS1','S4.E5','bib.bib16']:
    n=nodes[node_id]; fragment=text[n['start']:n['end']].encode('utf-8')
    filename=node_id.replace('.','_')+'.raw.html'
    (OUT/filename).write_bytes(fragment)
    (OUT/(node_id.replace('.','_')+'.mathtext.txt')).write_text(render(fragment.decode('utf-8')),encoding='utf-8',newline='\n')
    fragments.append({'source_id':node_id,'file':filename,'start_line':n['start_line'],'end_line':text.count('\n',0,n['end'])+1,'raw_byte_start':len(text[:n['start']].encode('utf-8')),'raw_byte_end_exclusive':len(text[:n['end']].encode('utf-8')),'raw_bytes':len(fragment),'raw_sha256':digest(fragment),'crlf_to_lf_only_sha256':digest(fragment.replace(b'\r\n',b'\n'))})
selected=[]
for node_id,n in sorted(nodes.items(),key=lambda kv:kv[1]['start']):
    cl=n['attrs'].get('class','')
    inside = any(n['start']>=nodes[x]['start'] and n['end']<=nodes[x]['end'] for x in ['S1.p1','S2','S3.SS2','A1.SS1','S4.E5']) or node_id=='bib.bib16'
    if inside and (n['tag']=='table' or 'ltx_para' in cl or 'ltx_theorem' in cl or node_id in ['alg1','bib.bib16'] or re.fullmatch(r'alg1\.l\d+',node_id)):
        s=text[n['start']:n['end']]
        selected.append({'id':node_id,'tag':n['tag'],'class':cl,'start_line':n['start_line'],'end_line':text.count('\n',0,n['end'])+1,'raw_sha256':digest(s.encode('utf-8')),'mathtext':render(s)})
write_json('source-dom-index76.json',selected)
write_json('raw-manifest76.json',{'source_path':str(SOURCE),'source_raw_bytes':len(raw),'source_raw_sha256':digest(raw),'crlf_count':raw.count(b'\r\n'),'bare_lf_count':raw.count(b'\n')-raw.count(b'\r\n'),'crlf_to_lf_only_bytes':len(raw.replace(b'\r\n',b'\n')),'crlf_to_lf_only_sha256':digest(raw.replace(b'\r\n',b'\n')),'raw_copy':'primary-pbps.exactraw.snapshot.html','fragments':fragments,'normalization':'Only byte replacement CRLF -> LF. Raw bytes are preserved; mathtext is a non-authoritative reading aid.'})
write_json('source-extraction-process76.json',{'pid':os.getpid(),'parent_pid':os.getppid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'foreground':True,'script':str(Path(__file__).resolve()),'python':os.sys.executable,'argv':os.sys.argv,'candidate_lean_read':False,'old_verdicts_read':False,'extraction_completed':True,'exit_code':'not asserted inside process; see captured foreground shell completion'})
print(json.dumps({'status':'extracted','pid':os.getpid(),'raw_sha256':digest(raw),'lf_sha256':digest(raw.replace(b'\r\n',b'\n')),'indexed_blocks':len(selected),'fragments':fragments},ensure_ascii=False,indent=2))
