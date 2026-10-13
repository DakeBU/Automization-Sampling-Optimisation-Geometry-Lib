from pathlib import Path
import hashlib,json,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,o):(D/n).write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
bindings=[]
p=Path('runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preread43/primary.raw.snapshot.html')
raw=p.read_bytes();ls=raw.decode('utf-8').splitlines(keepends=True)
ranges=[[606,609],[612,620],[627,632],[652,661],[1289,1314]]
excerpt=''.join(''.join(ls[a-1:b]) for a,b in ranges).encode('utf-8')
(D/'primary.raw.snapshot.html').write_bytes(excerpt);(D/'primary.lf.snapshot.html').write_bytes(excerpt.replace(b'\r\n',b'\n'))
bindings.append({'id':'primary','path':str(p),'source_id':'arxiv:2609.06906v1','selected_physical_ranges':ranges,'raw_sha256':sha(excerpt),'lf_sha256':sha(excerpt.replace(b'\r\n',b'\n')),'whole_raw_sha256':sha(raw)})
if not (D/'primary-before-parent-interfaces.contract.json').exists():
    put('primary-before-parent-interfaces.contract.json',{'actor':'gaussian_noncompact_preread_42','state':'PRIMARY_READ_AND_PINNED_BEFORE_PUBLIC31_43_EXTRACTION','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'FIRST4.6/S2/normalizedstanding','leases':'actual lease.json OPEN','previous_exposure':'Prior43 prospective/sourcegraph interfaces known; no freshblind claim. Current31 public header not previously read. No43 production body/Test/review/blind/lesson read.'})
for sid,file,name in [
 ('031public','StandardizedRGOPositionFisher.lean','standardized_rgo_position_and_fisher'),
 ('043public','StandardizedRGOKLFisher.lean','standardized_rgo_unique_prox_and_kl_le_fisher')]:
    path=Path('AutoSamplingTheory/ExampleCases/SmoothedPicardHMC')/file
    data=path.read_bytes();start=data.index(('theorem '+name).encode());end=data.index(b':= by',start)
    header=data[start:end].rstrip()+b'\r\n' if b'\r\n' in data else data[start:end].rstrip()+b'\n'
    lf=header.replace(b'\r\n',b'\n')
    (D/(sid+'.raw.snapshot.txt')).write_bytes(header);(D/(sid+'.lf.snapshot.txt')).write_bytes(lf)
    bindings.append({'id':sid,'path':str(path),'name':name,'raw_sha256':sha(header),'lf_sha256':sha(lf),'raw_bytes':len(header),'lf_bytes':len(lf),'original_physical_start':data[:start].count(b'\n')+1,'original_physical_end':data[:end].count(b'\n')+1,'terminal_body_suffix_excluded':':= by','whole_file_raw_hash_only':sha(data),'body_not_exposed_or_copied':True})
    print(sid+'\n'+lf.decode('utf-8'))
put('input-bindings.json',{'inputs':bindings,'input_statement_status':'31 existing actualparent;43 root reportsPROVED_LOCAL19b569ae with verifieractive, no43VERIFIEDclaim byprereader','scope':'exactpublicheadersonly before :=by; no bodies/Tests/reviews/blind/lessons orsourcegraph'})
