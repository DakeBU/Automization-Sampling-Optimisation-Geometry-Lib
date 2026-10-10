from pathlib import Path
import hashlib
import json
import datetime

out = Path(__file__).resolve().parent
src = Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
raw = src.read_bytes()
lines = raw.splitlines(keepends=True)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

items = [('license-tr',257,261),('S1.p1/S1.E1',349,361),('S2.SS2.p1',613,616),('S3.E4',1486,1492),('S3.E9',1613,1619),('S3.Thmtheorem1',1639,1653),('A1.SS1.p1',2859,2887),('A1.SS1.p2/A1.E1/A1.E2',2889,2911),('A1.SS1.p3',2913,2973),('A1.SS1.SSS0.Px1.p4/A1.E7',3147,3173),('A1.SS2 joint Borel recursion paragraph',3325,3338)]
anchors = []
for identity, start, end in items:
    anchors.append(dict(id=identity, raw_line_start=start, raw_line_end=end,
        byte_start_zero_based=sum(map(len,lines[:start-1])),
        byte_end_exclusive=sum(map(len,lines[:end])),
        raw_span_sha256=hashlib.sha256(b''.join(lines[start-1:end])).hexdigest()))

manifest = dict(schema=1, kind='independent-primary-first-native-raw-manifest',
    reviewer_identity='/root/fresh_source87', source=dict(
        title='Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler',
        immutable_url='https://arxiv.org/html/2609.06905v1', version='arXiv:2609.06905v1',
        printed_date='07 Sep 2026', license='arXiv.org perpetual non-exclusive license',
        local_path=str(src), raw_sha256=hashlib.sha256(raw).hexdigest(), raw_size_bytes=len(raw)),
    anchors=anchors, candidate_exposure_before_freeze=False,
    private_source_extracts_excluded_from_publication=[str(out/'primary-a1.extracted.private.json'),str(out/'primary-context.extracted.private.json')])
manifest_path = out/'primary-source.raw-manifest.native.json'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
freeze_path = out/'source-first.freeze.native.json'
freeze = json.loads(freeze_path.read_text(encoding='utf-8'))
freeze.update(source_manifest_path=str(manifest_path),source_manifest_sha256=digest(manifest_path),
    freeze_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
freeze_path.write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (out/'chronology.native.jsonl').open('a',encoding='utf-8') as chronology:
    for event in [dict(event='primary-context-read',path=str(out/'primary-context.extracted.private.json'),sha256=digest(out/'primary-context.extracted.private.json')),
        dict(event='PRIMARY_FIRST_FREEZE_COMPLETED',freeze_path=str(freeze_path),freeze_sha256=digest(freeze_path),raw_manifest_sha256=digest(manifest_path))]:
        event.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_exposure=False)
        chronology.write(json.dumps(event)+'\n')
for path in sorted(out.iterdir()):
    print(path.name,digest(path))
