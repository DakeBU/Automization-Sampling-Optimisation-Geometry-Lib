import os
import review76 as r
manifest=r.load(r.O/'inputs.manifest.json')
records=[]
for item in manifest['inputs']:
    if not item['path'].endswith('.png'): continue
    r.check(item); name=r.Path(item['path']).name
    if 'branch-' in name:
        note='Personally viewed original pixels. The selected compiled actual-finite-recursion declaration and three producer references are visible in the side card. The legend distinguishes solid module/import ownership from dashed references/correspondences. Six highlighted direct relations are shown; context labels are very dense at fit scale.'
    elif 'proof-' in name:
        number=int(name.split('proof-')[1].split('.')[0])
        note=f'Personally viewed original pixels. Numbered proof step {number} is at the viewport top, with prose, a rendered formula and an initially folded Corresponding Lean step panel. Neighbouring proof steps or the boundary/assumption table are also visible. The final zero-threshold and positive-finite-growth distinction is explicit in later captures; no global-process conclusion is rendered as proved.'
    else:
        note='Personally viewed original pixels. Attribution, source anchor, finite/stopped and deterministic-zero extension, complete ten-group statement, six analytic caller explanation and open process boundary are visible. The compact plain-text statement is dense. The displayed energy/cap/clock formula uses a horizontal scroll area. The copy screenshot is the statement viewport; callback success comes from native component evidence, not pixels alone.'
    records.append(dict(input_pin=item,actually_viewed_with='tools.view_image detail=original',independently_viewed=True,observation=note))
assert len(records)==13
r.save('independent-PNG-observations.json',dict(actor=r.ACTOR,actual_record_writer_PID=os.getpid(),independent_of_root_viewing=True,independently_viewed_PNGs=13,records=records,physical_OS_clipboard_test=False,new_mathematical_source_or_exposition_seal=False))
print(r.json.dumps(dict(status='RECORDED_13_ACTUAL_INDEPENDENT_PNG_VIEWS',actor=r.ACTOR,actual_record_writer_PID=os.getpid(),PNG_count=13,current_reader_acceptance_pending=True)))
