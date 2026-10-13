import base64,hashlib,pathlib
def sha(data):return hashlib.sha256(data).hexdigest()
def pack(path,name=None,*,binary=False):
    path=pathlib.Path(path);raw=path.read_bytes()
    item=dict(name=name or path.name,RAW_bytes=len(raw),RAW_sha256=sha(raw),RAW_base64=base64.b64encode(raw).decode('ascii'),binary=binary)
    if binary:
        item['LF_recipe']='not applicable to binary artifact; preserve exact original RAW bytes'
    else:
        raw.decode('utf-8')
        lf=raw.replace(b'\r\n',b'\n')
        item.update(LF_recipe='CRLF byte pairs to LF ONLY; preserve every other byte',LF_bytes=len(lf),LF_sha256=sha(lf),LF_base64=base64.b64encode(lf).decode('ascii'))
    return item
