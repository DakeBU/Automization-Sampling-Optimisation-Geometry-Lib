from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a/phase1'
H = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda name, obj: (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

exposure = {
 'phase':'PHASE1_RAW_SOURCE_COGNITION',
 'reviewer':'src_4e8f6a',
 'ambient_exposure_nonzero':True,
 'zero_exposure_claim':False,
 'independence_claim_scope':'No current candidate Lean statement, target declaration, author proof, proposed acceptance conclusion, blind reconstruction, old source audit or peer private rationale was supplied to or opened by this reviewer during Phase 1. This is a bounded process report, not a claim that ambient labels cannot anchor cognition.',
 'source_visibility':True,
 'source_identity_visibility':True,
 'ambient_labels_visible':[
  'Task assigned source arXiv 2610.20492v1, title shown by original HTML, known exact source hash and bytes, required §2/§4/C.4 reading.',
  'Task explicitly named semantic axes statement/calculus/normalizer/affine/oracle, full O versus same O, local versus main-theorem parameters, precision versus covariance and deterministic cap versus undefined expected cost.',
  'Current repository path/name ASTIS-GC, role/task path src_4e8f6a, output path semantic-neutral-20261108, and parent role boundaries.',
  'Inherited developer approval-prefix metadata contains historical Gaussian-affinity, first-order-query, fixed-spectrum-query, determinant, admissibility, normalizer, browser/final-reader/integration labels and older exercise identifiers. The list is partially truncated in the inherited context. None of its named files was opened.',
  'Mandatory AGENTS.md names PBPS, SPHMC, Gaussian Cloud, midpoint, older Bench and PR/commit history, frontier/site/registry paths, technical-lemma examples and ATLAS-related policy. These mandatory ambient contents were read but their referenced mathematical/history files were not opened.',
  'Mandatory protocols contain worked mathematical/process examples and historical fixed allowlists. These were read as process material, not evidence for this source or a proposed candidate.',
  'Platform tooling, permissions, skill catalog and workspace metadata reveal available capabilities and permitted filesystem roots; these are exposure, not a zero-exposure certificate.'
 ],
 'handling':'Read the whole required source slice before forming the claim inventory. No candidate was inferred or selected from historical labels. All claims and scope qualifications were reconstructed from the pinned paper; standard bridges are explicitly labelled. Topic steering and nonzero ambient labels remain recorded as limitations of anti-anchoring.',
 'files_actually_read_for_content':[
  {'path':'AGENTS.md','scope':'entire mandatory guide'},
  {'path':'.agents/skills/astis-semantic-roundtrip/SKILL.md','scope':'entire'},
  {'path':'docs/proof-digestion-protocol.md','scope':'entire; output truncation was followed by bounded rereads covering the rest'},
  {'path':'docs/theorem-publication-protocol.md','scope':'entire; bounded rereads covered portions affected by initial combined-output truncation'},
  {'path':'docs/evidence-routed-memory-protocol.md','scope':'entire'},
  {'path':'.astis/huanjian-resume-20261103/2610.20492v1.html','scope':'entire file read programmatically for byte/hash verification, copying and parsing; semantically read S1 context, all S2, all S4 and all A3.SS4; original C.4 and Lemma 4.6 HTML also inspected directly'},
  {'path':'.astis/semantic-neutral-20261108/src_4e8f6a/phase1/','scope':'only self-created source snapshots, extracts, claim inventory, summaries, scripts and validation outputs'}
 ],
 'source_nonprimary_exposure':[
  'The original HTML title, first 2600 bytes of header/scripts/metadata and first math alttext κ were shown.',
  'A structural parser showed section/subsection IDs across the original HTML (S1–S5, appendices, bibliography) and the first math tag; it did not display substantive unassigned sections.',
  'Entire S1 was read for context, so its literature comparisons and the informal other-result statement were visible. Section 3 and referenced external papers were not read. Only bounded relevant context enters CTX clauses; no claim about Section 3 proof is made.'
 ],
 'existence_only_probes':[
  '/AGENTS.md','/Users/AGENTS.md','/Users/zhouhuanjian/AGENTS.md',
  '.agents/AGENTS.md','.agents/skills/AGENTS.md','.agents/skills/astis-semantic-roundtrip/AGENTS.md',
  'docs/AGENTS.md','.astis/AGENTS.md','.astis/huanjian-resume-20261103/AGENTS.md',
  '.astis/semantic-neutral-20261108/AGENTS.md',
  '.astis/semantic-neutral-20261108/src_4e8f6a/AGENTS.md',
  '.astis/semantic-neutral-20261108/src_4e8f6a/phase1/AGENTS.md'
 ],
 'not_performed':[
  'No candidate/frontier/paper-contribution/implementation/Lean/API lookup.',
  'No old review/evidence/sourceaudit/preproof graph/peer private file opened.',
  'No .atlas-upstream access, no registry/ledger/shared publication/site/README/model/remote writes.',
  'No git tree/status/history lookup, no network/source search, no external paper lookup.',
  'No new Goal, background/detached ASTIS process, Lean invocation or source-admission check.',
  'No subagent spawned by this reviewer.'
 ],
 'writes_scope':str(OUT),
 'future_phase_gate':'Await anonymous Lean plus an independent source-blind reconstruction only after this freeze. Perform bounded selective comparison first; whole-module/reader/fresh-Lean context only later if separately supplied.'
}
dump('ambient_exposure_record.json', exposure)

extra = {
 'S2.Ex1':['P2-03'], 'S2.E1':['P2-04'], 'S2.Ex2':['P2-07'], 'S2.E2':['P2-08'],
 'S4.Ex9':['H4-01'], 'S4.E11':['H4-02'], 'S4.Ex10':['H4-06'],
 'S4.Ex11':['H4-07'], 'S4.Ex12':['H4-09','H4-10'], 'S4.Ex13':['H4-09'],
 'S4.Ex14':['H4-09'], 'S4.Ex15':['H4-11'], 'S4.EGx1':['H4-12'],
 'S4.Ex17':['H4-14'], 'S4.EGx2':['T4-02'], 'S4.Ex20':['T4-04'],
 'S4.Ex21':['T4-05'], 'S4.Ex22':['T4-05'], 'S4.Ex23':['T4-06'],
 'S4.Ex24':['T4-07'], 'S4.Ex25':['T4-08'], 'S4.Ex26':['T4-09'],
 'S4.Ex27':['T4-10'], 'S4.Ex28':['L4-02'], 'S4.Ex29':['L4-03'],
 'S4.Ex30':['L4-04'], 'A3.Ex160':['C4-05','C4-06'],
 'S2.SS0.SSS0.Px1.p1.2':['P2-04'],
 'S2.SS0.SSS0.Px4.p1.2':['P2-08','P2-09'],
 'S4.SS2.SSS0.Px1.p1':['H4-07','H4-08'],
 'S4.Thmtheorem2':['H4-04','H4-05'],
 'S4.SS2.SSS0.Px3.p1':['H4-12','H4-13','H4-14'],
 'S4.SS2.SSS0.Px4.p1':['H4-16','C4-01'],
 'S4.SS3.p1':['T4-01','T4-10'],
}
payload = json.loads((OUT/'source_claims_seven_slots.json').read_text())
claims = payload['claims']
expected_slots = {'objects','quantifiers','domain','assumptions','conclusion','use','failure_boundary'}
assert len(claims)==50
assert len({c['claim_id'] for c in claims})==50
assert all(set(c['seven_slots'])==expected_slots and all(c['seven_slots'].values()) for c in claims)

# This is a reading inventory, deliberately not NODE/EXCLUDED proof topology.
reading = []
unmapped = []
heading_ids = {
 'S2','S2.SS0.SSS0.Px1','S2.SS0.SSS0.Px2','S2.SS0.SSS0.Px3','S2.SS0.SSS0.Px4',
 'S4','S4.SS1','S4.SS2','S4.SS2.SSS0.Px1','S4.SS2.SSS0.Px2','S4.SS2.SSS0.Px3',
 'S4.SS2.SSS0.Px4','S4.SS3','S4.SS3.2','S4.SS3.SSS0.Px1','S4.SS3.SSS0.Px2',
 'S4.SS3.SSS0.Px3','S4.SS4','S4.SS4.SSS0.Px1','S4.SS4.SSS0.Px2','A3.SS4','A3.SS4.2'
}
for sec in ['S2','S4','A3.SS4']:
    text = (OUT/'extracted'/(sec+'.txt')).read_text()
    for ident, line in re.findall(r'^\[([^;\n]+); HTML line (\d+)\]$', text, re.M):
        if ident in heading_ids:
            reading.append({'source_region':ident,'html_line':int(line),'reading_status':'read-in-full','region_kind':'structural-heading-or-proof-container','claim_ids':[]})
            continue
        ids = set()
        for c in claims:
            for anchor in c['source_anchors']:
                if ident==anchor or ident.startswith(anchor+'.'):
                    ids.add(c['claim_id'])
        for anchor, mapped in extra.items():
            if ident==anchor or ident.startswith(anchor+'.'):
                ids.update(mapped)
        if not ids:
            unmapped.append(ident)
        reading.append({'source_region':ident,'html_line':int(line),'reading_status':'read-in-full','region_kind':'substantive-source-region','claim_ids':sorted(ids)})
assert not unmapped, unmapped
dump('primary_reading_coverage.json',{
 'purpose':'Reading/claim coverage only; not a Source Proof Graph, topology extraction, graph approval, proof certificate or source admission.',
 'primary_sections':['S2','S4','A3.SS4'],
 'context_section':'S1',
 'source_regions':reading,
 'unmapped_substantive_regions':unmapped,
 'source_claim_count':50,
 'coverage_limit':'Mechanical anchor mapping only checks that every displayed primary reading region is assigned to at least one source-cognition clause or a structural heading. The reviewer read each primary extract completely; this file does not independently certify mathematical proof coverage.',
 'deferred_or_unchecked':[
  'C.1–C.3 proofs and reference [22] are named and described by §4 but not inspected.',
  'Lemma 4.7 is stated in the assigned slice without its proof.',
  'Fact C.6 Bernstein calculation is cited by §4.4 but not inspected.',
  'Gaussian integration and other standard algebra/calculus/measure bridges are interpreted but not independently formalized.',
  'Stronger lower bounds from the same fixed-spectrum family are explicitly open.'
 ]})

source = ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html'
raw = source.read_bytes()
assert len(raw)==951991 and H(raw)=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
for entry in json.loads((OUT/'inputs_manifest.json').read_text()):
    b=(OUT/entry['snapshot']).read_bytes()
    assert len(b)==entry['bytes'] and H(b)==entry['sha256']
    assert (ROOT/Path(entry['original_path']).relative_to(ROOT)).read_bytes()==b
assert H((OUT/'inputs/2610.20492v1.html').read_bytes())==H(raw)
dump('validation_receipt.json',{
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'kind':'file-and-inventory consistency only; no mathematical admission or formal proof check',
 'checks':[
  'Original source length 951991 and pinned SHA-256 matched.',
  'All six original source/protocol/guide snapshots matched their recorded bytes and hashes and remained byte-identical to source files.',
  '50 distinct source claims have all seven nonempty requested slots.',
  'Every extracted primary region is mapped to claims or explicitly classified as a structural heading.',
  'No primary substantive region is left unmapped.',
  'All generated artifacts are within the assigned phase1 directory.'
 ],
 'claim_count':50, 'primary_region_count':len(reading),
 'formal_check_run':False,'source_admission_run':False,'candidate_comparison_run':False
})

excluded = {'freeze_manifest.json','freeze_manifest.sha256'}
entries=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.relative_to(OUT).as_posix() not in excluded:
        b=p.read_bytes()
        entries.append({'path':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':H(b)})
manifest = {
 'schema':'phase1-source-cognition-freeze-v1',
 'phase':'PHASE1_RAW_SOURCE_COGNITION',
 'status':'FROZEN_AWAITING_SEPARATE_ANONYMOUS_COMPARISON_INPUTS',
 'frozen_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':'src_4e8f6a',
 'source':{'original_path':str(source),'bytes':len(raw),'sha256':H(raw),'title':'On Complexity of Gaussian Sampling','version':'2610.20492v1'},
 'primary_reading':['S2','S4','A3.SS4'],
 'context_reading':['S1'],
 'source_clause_count':50,
 'exposure':'ambient_exposure_record.json; explicitly nonzero ambient exposure',
 'cognition':'source_cognition.md',
 'seven_slots':'source_claims_seven_slots.json',
 'interfaces':'interfaces_and_scope.md',
 'reading_coverage':'primary_reading_coverage.json',
 'inputs':'inputs_manifest.json',
 'protocol_summary':'protocol_summary.md',
 'validation':'validation_receipt.json',
 'claim_boundary':'Independent source-only cognition, not Lean truth, source admission, graph authorship, topology approval, decoder reconstruction or repair acceptance.',
 'next_phase_gate':'Await anonymous Lean and independent blind reconstruction; then selective seven-slot comparison; whole-module/reader/fresh-Lean only afterward.',
 'artifacts':entries
}
dump('freeze_manifest.json',manifest)
manifest_bytes=(OUT/'freeze_manifest.json').read_bytes()
(OUT/'freeze_manifest.sha256').write_text(H(manifest_bytes)+'  freeze_manifest.json\n')
print(json.dumps({'status':manifest['status'],'source_bytes':len(raw),'source_sha256':H(raw),'claims':50,'primary_regions':len(reading),'artifacts':len(entries),'freeze_manifest_sha256':H(manifest_bytes)},indent=2))
