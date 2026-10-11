from pathlib import Path
import json,hashlib,datetime
r=Path(__file__).parent;load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
p=r/'preintegration-diagnostics90.json';assert not p.exists()
assert load(r/'checks90/contributor/receipt.json')['exit_code']==1
assert load(r/'checks90/accepted-contributor/receipt.json')['exit_code']==0
p.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),initial_contributor=dict(classification='ADMISSION_PENDING_NOT_MATHEMATICS',reason='Ran before final source audit adoption; whole-module publication review had not yet been admitted.',negative='checks90/contributor/receipt.json',accepted_after_source_adoption='checks90/accepted-contributor/receipt.json',production_unchanged=True),browser=dict(observation='Existing bound browser.tabs.list returned [] on current root turn.',backend_reset=False,alternate_backend=False,actual_page_visual=False,fine_branch_visual=False,source_DOM_not_substitute=True),lookup_negative=dict(path='runs/20261007-companion-priority/pbps-next-history-extension-preread90/preread90.py',classification='PATH_LOOKUP',correction='Filename search locates the existing preread90.py under actual-conditional-next-wait-density89; no mathematical or canonical mutation.'),Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
for f in ['render_svg89.js','record_svg_view89.py','push_integration89.py']:
 s=(r.parent/'pbps-actual-conditional-next-wait-density89'/f).read_text(encoding='utf8').replace('89','90').replace('actual-conditional-next-wait-density','actual-finite-history-extension').replace('Integrate verified actual PBPS conditional finite next-wait density','Integrate verified actual PBPS complete finite-history extension')
 q=r/f.replace('89','90');assert not q.exists();q.write_text(s,encoding='utf8',newline='\n')
print('Typed pre-admission negative and browser limitation retained; no mathematical change.')
