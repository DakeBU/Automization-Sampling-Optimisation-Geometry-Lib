from pathlib import Path
import hashlib,json
r=Path(__file__).parent;d=Path('.astis/decoder83');d.mkdir(exist_ok=False);raw=(r/'anonymous.decoder83.json').read_bytes();(d/'packet.json').write_bytes(raw)
print('Anonymous packet RAW',hashlib.sha256(raw).hexdigest(),'canonical',json.loads(raw)['packet_sha256'])
