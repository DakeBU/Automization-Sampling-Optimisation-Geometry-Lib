from common import *
adoption=J(R/'root.exact-verification61.adoption.json'); maps=[]
for m in adoption['exact_historical_resolutions']:
 matches(m['original'],m['exact_raw_snapshot']['path']);matches(m['exact_raw_snapshot']);maps.append(m)
science=J(R/'exact-science-verification/science.entries.json');assert science['count']==691 and science['checked_commit']==SCI
p=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE);data,_=p.communicate(('\n'.join(x['git_blob'] for x in science['entries'])+'\n').encode());assert p.returncode==0;pos=0
for e in science['entries']:
 end=data.index(b'\n',pos);size=int(data[pos:end].split()[2]);b=data[end+1:end+1+size];pos=end+size+2;assert H(b)==e['git_raw_sha256'] and H(b.replace(b'\r\n',b'\n'))==e['git_lf_sha256']
 if e['repository_path'] in ['research-wiki/frontier-cells/ASTIS-SHARED-l2-positive-real-square-root.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-real-defect-root.json']:
  dst=P/('science-cell-'+H(e['repository_path'].encode())+'.exactraw.snapshot.json');dst.write_bytes(b);matches(e['current'],dst);maps.append(dict(original=e['current'],exact_raw_snapshot=pin(dst),authority='Original SCI current raw pin equals exact SCI Git blob raw, before root independent-verification/integration administration'))
p2=J(P/'phase2.inputs.json'); ledger=next(x for x in p2['qualified_original_snapshot_pairs'] if path(x['original']['path'])==ROOT/'runs/substantive_advances.jsonl');matches(ledger['original'],ledger['exact_raw_snapshot']['path']);maps.append(dict(**ledger,authority='PHASE2 exact integration ledger byte snapshot taken before future62 append; reviewed61 integration scope only'))
dl=J(R/'anonymous-decoder/closed-lease.json');assert dl['status']=='CLOSED' and dl['closed_last'] and dl['actual_foreground_readback']['exit_code']==0 and dl['source_identity_visible'] is False and dl['source_text_visible'] is False
W(P/'native.history.json',dict(status='PASS',actual_PID=os.getpid(),actual_git_catfile_PID=p.pid,exit_code=p.returncode,science_entries_checked=691,finite_qualified_history_mappings=maps,exact2SCI_cell_mappings=True,exact4_original_native_adoption_mappings=True,exact1_pre_future_claim_integration_ledger_map=True,decoder_native_closed_lease=pin(R/'anonymous-decoder/closed-lease.json'),source_identity_exposure='Native decoder source-text=false/identity=false; source review separately explicitly source-exposed. Neither role substitutes for the other.'))
print('NATIVE_HISTORY_PASS',len(maps),'qualified maps',691,'SCI blobs')
