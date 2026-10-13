"""Snapshot only an explicit finite list, with no glob or inferred expansion."""
import hashlib,pathlib

def snapshot(out, source_path, name, role, expected_raw_sha256=None, binary=False):
    source_path=pathlib.Path(source_path)
    target=out/name
    assert target.resolve().parent==out.resolve(), 'flat owned snapshots only'
    assert not target.exists(), 'never replace an existing evidence snapshot'
    raw=source_path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if expected_raw_sha256 is not None:
        assert digest==expected_raw_sha256, str(source_path)
    target.write_bytes(raw)
    result=dict(name=name,original_path=str(source_path),role=role,RAW_bytes=len(raw),RAW_sha256=digest,
                binary=bool(binary))
    if binary:
        result.update(LF_bytes=None,LF_sha256=None,LF_recipe='not applicable; binary RAW preserved')
    else:
        raw.decode('utf-8')
        lf=raw.replace(b'\r\n',b'\n')
        (out/(name+'.LF')).write_bytes(lf)
        result.update(LF_bytes=len(lf),LF_sha256=hashlib.sha256(lf).hexdigest(),
                      LF_recipe='only CRLF-to-LF; lone CR preserved')
    return result
