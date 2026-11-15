"""Close all current served bytes by new explicit leaves or immutable byte reuse.
Reusing file bytes never transfers an earlier browser/math/source verdict.
"""
from pathlib import Path
import json,hashlib,tarfile,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
p=w/'reader-preview-v2';d=w/'reader-served-byte-delta-v1';assert not d.exists();d.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
oldrel='research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/reader-originals/laplace_native_61e4/v3/selected-presentation-originals.actual-v3.356.v1.tar.gz'
old=r/oldrel;raw=old.read_bytes();h=sha(raw)
assert sha(subprocess.check_output(['git','show','f1d58f14c02d638a6925cda143d5307a73aa8f9b:'+oldrel]))==h
v=json.loads((p/'preview-freeze-manifest.json').read_text());files={};resolutions=[]
with tarfile.open(old,'r:gz') as tf:
    available={x.name:x for x in tf.getmembers() if x.isfile()}
    for variant in ['original','candidate']:
        for x in v['variants'][variant]['files']:
            q=p/'fixtures'/variant/x['path'];b=q.read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes']
            member=f'input-originals/v3/fixtures/{variant}/{x["path"]}'
            z={'variant':variant,'served_path':x['path'],'bytes':len(b),'sha256':sha(b)}
            if member in available and tf.extractfile(available[member]).read()==b:
                z.update(kind='EXACT_IMMUTABLE_FILE_BYTES_ONLY',existing_public_commit='f1d58f14c02d638a6925cda143d5307a73aa8f9b',archive=oldrel,archive_sha256=h,member=member)
            else:
                rel=str(q.relative_to(w));files[rel]={'path':rel,'bytes':len(b),'sha256':sha(b)}
                z.update(kind='NEW_EXPLICIT_CURRENT_SERVED_LEAF',selected_relative_path=rel)
            resolutions.append(z)
for name in ['render_preview.py','reader_overlay.py','input-freeze-manifest.json','preview-freeze-manifest.json','helper-custody.json']:
    q=p/name;b=q.read_bytes();rel=str(q.relative_to(w));files[rel]={'path':rel,'bytes':len(b),'sha256':sha(b)}
out={'schema':'R16-explicit-current-served-byte-delta-selection-v1','scope':'Exactly new current served files and five current own render/freeze originals; unchanged served bytes resolve through exact existing public archive members. No input-snapshot/source directory recursion.',
 'source_base':str(w),'file_count':len(files),'files':list(files.values()),
 'all207_served_byte_resolutions':resolutions,'old_archive_sha256':h,
 'boundary':'Byte identity/availability only, no old mathematical/source/browser verdict transfer. Current actual389checks/36PNG and independent reader acceptance remain original R16 evidence. No physical touch/fullsite/main/production claim.'}
q=d/'served-delta.selection.v1.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selection':str(q.relative_to(r)),'sha256':sha(q.read_bytes()),'selected_new_leaves':len(files),
 'exact_existing_public_file_reuses':sum(x['kind']=='EXACT_IMMUTABLE_FILE_BYTES_ONLY' for x in resolutions),
 'all_current_served_files':len(resolutions),'no_verdict_transferred':True}))
