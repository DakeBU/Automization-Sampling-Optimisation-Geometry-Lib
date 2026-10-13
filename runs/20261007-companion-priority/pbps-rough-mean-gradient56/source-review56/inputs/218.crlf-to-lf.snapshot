from pathlib import Path
import re, json, hashlib
task = Path(__file__).parent
root = Path(r'E:\Samplinglib')
def sha(b): return hashlib.sha256(b).hexdigest()
def snapshot_header(rel, name):
    path = root / rel
    with path.open('rb') as handle: raw = handle.read()
    text = raw.decode('utf-8')
    start = re.search(r'^theorem ' + re.escape(name) + r'\b', text, re.M).start()
    match = re.search(r'\s*:=\s*by\b', text[start:])
    assert match is not None
    end = start + match.start()
    contract = text[start:end]
    context = '\n'.join(line for line in text[:start].splitlines() if re.match(r'^(import|namespace|section|noncomputable section|variable|open)\b', line)) + '\n'
    header_bytes = contract.encode('utf-8')
    for suffix, b in [('raw', header_bytes), ('lf', header_bytes.replace(b'\r\n', b'\n'))]:
        with (task / (name + '.' + suffix + '.contract.lean')).open('wb') as handle: handle.write(b)
    record = {'declaration': name, 'physical_path': str(path), 'line_start': text.count('\n', 0, start)+1, 'line_end': text.count('\n', 0, end)+1, 'whole_file_raw_sha256': sha(raw), 'whole_file_raw_bytes': len(raw), 'whole_file_lf_sha256': sha(raw.replace(b'\r\n',b'\n')), 'whole_file_lf_bytes': len(raw.replace(b'\r\n',b'\n')), 'header_raw_sha256': sha(header_bytes), 'header_raw_bytes': len(header_bytes), 'header_lf_sha256': sha(header_bytes.replace(b'\r\n',b'\n')), 'header_lf_bytes': len(header_bytes.replace(b'\r\n',b'\n')), 'typing_context': context, 'proof_body_emitted': False}
    print(json.dumps(record,ensure_ascii=False));print(contract)
    return record
records = []
for file, decl in [('SourceMeanGradientDomain.lean','literal_source_mean_in_closed_gradient'), ('L2MacroscopicMean.lean','actual_macroscopic_l2_mean'), ('MacroscopicEnergy.lean','actual_macroscopic_gradient_energy_blocks')]:
    records.append(snapshot_header('AutoSamplingTheory/ExampleCases/ProximalBPS/'+file,decl))
with (task/'provider-contract-snapshots.json').open('w',encoding='utf-8',newline='\n') as handle: json.dump(records,handle,indent=2);handle.write('\n')
proposal = root/'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof56/root.statement-proposal.json'
with proposal.open('r',encoding='utf-8') as handle: print('ROOT PROPOSAL', handle.read())
statement = root/'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof56/prospective-statement.txt'
with statement.open('rb') as handle: candidate = handle.read()
print('TARGET',len(candidate),sha(candidate),len(candidate.replace(b'\r\n',b'\n')),sha(candidate.replace(b'\r\n',b'\n')));print(candidate.decode('utf-8'))
with (task/'prospective-statement.target.raw.snapshot.txt').open('wb') as handle: handle.write(candidate)
with (task/'prospective-statement.target.lf.snapshot.txt').open('wb') as handle: handle.write(candidate.replace(b'\r\n',b'\n'))
