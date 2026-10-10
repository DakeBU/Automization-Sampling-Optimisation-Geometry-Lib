from pathlib import Path
h=Path('.astis/pbps-sharp-energy68');s=(h/'record-integration68.py').read_text(encoding='utf-8')
for a,b in [('runs/20261007-companion-priority/pbps-sharp-energy68','runs/20261007-companion-priority/pbps-reflection-intertwining69'),('integration68','integration69'),('verification68','verification69'),('visual68','visual69'),('Registry516','Registry517'),('registry_count=516','registry_count=517'),('publication_units=237','publication_units=238'),('237publication','238publication'),('516Registry','517Registry'),('AGGREGATE68','AGGREGATE69'),('admin68','admin69'),('aggregate68','aggregate69'),('final admin68','final admin69'),('PASS68','PASS69'),('root-science68','root-science69')]:s=s.replace(a,b)
s=s.replace("'semantic', 'frontier',", "'semantic-cli', 'frontier-cli',")
s=s.replace("len(capture['records']) == 14", "len(capture['records']) == 8")
s=s.replace("len(probe['panels']) == len(probe['downloads']) == 2", "len(probe['panels']) == len(probe['downloads']) == 3")
s=s.replace("[5, 6][i]",'6').replace('panels=2','panels=3').replace('downloads=2','downloads=3')
s=s.replace("'graph-check-shared-final', ", '')
s=s.replace('Two full literal private Prop representations preserve the statement; this is not a full Exposition Seal.','The complete literal private Prop is also present in the existing adjacent proof helper fold; it remains a representation, not a proof provider or full Exposition Seal.')
s=s.replace('Two complete attributed statements, all eleven formula/BODY proof steps and exact actual branch inspected.','One complete attributed statement, all six formula/BODY proof steps, complete private-Prop helper and exact actual branch inspected.')
s=s.replace('four copy callbacks and four RAW production source downloads exact.','three copy callbacks and three RAW production source downloads exact.')
s=s.replace('Exact corrected SCI68B and serialized local aggregate only','Exact SCI69 and serialized local aggregate only')
s=s.replace('Focused and independent math/decoder/source/exact-commit, reviewed metadata and local aggregate accepted within sharp corrector energy scope.','Focused and independent math/decoder/source/exact-commit, reviewed metadata and local aggregate accepted within full-micro intertwining scope.')
start=s.index("    anchor = 'Serialized Registry517");end=s.index("    p.write_bytes(text.replace",start)
replacement="""    anchor = 'Serialized Registry517/imports/Tests and current reader/graph gates are pending\\nagainst final admin state; exact science verification is separate from these\\naggregate admissions and from remote CI.'
    assert text.count(anchor) == 1
    text = text.replace(anchor, f'Serialized local aggregate69: root{jobs[0]}, Tests{jobs[1]}, Registry517;238 publication units.\\nOne complete statement, six formula/BODY steps, full private-Prop helper and actual\\nbranch inspected; three isolated copy callbacks and three RAW downloads exact.\\nCurrent graph regeneration follows these final cell writes; final gates are recorded\\nin existing69 integration.notes.json. Python296 evidence is reused from INT64 against\\nunchanged tools/site scripts. Independent repository/reader, remoteCI/main/live and\\nfull Exposition/PURIFIED remain separate.')
"""
s=s[:start]+replacement+s[end:]
s=s.replace('One generic sharp Hilbert quadratic leaf, the same-actual PBPS sharp corrector theorem and genuine modified-energy Test consumer; one evidenced PBPS route, exact compiled edges and two cards only. No conceptual formal edge.','One same-actual PBPS full-micro intertwining production theorem, one literal proposition representation and one module card; real existing parents with same-U adapter, no invented Test consumer or conceptual formal edge.')
s=s.replace("remaining=visual['debts']+['B21/H1/B4 dynamics/invariance/nonexplosion/main/errors/caps/expectedquerycost/actual-input composition remain open.']", "remaining=visual['debts']+['Actual projected rotation/mean preservation and B21 corrector change,H1/B4 dynamics/invariance/nonexplosion/main/errors/caps/expectedquerycost/actual-input composition remain open.']")
s=s.replace("current_graph=pin('_site/data/underlying-lean-graph.json'),", "current_graph=pin('_site/data/underlying-lean-graph.json'), retired_root_CLI_attempts=['integration69/semantic PID47776 EXIT2: wrong astis.py subcommand; corrected semantic-cli PID33732 EXIT0','integration69/frontier PID46100 EXIT2: wrong astis.py subcommand; corrected frontier-cli PID49036 EXIT0'],")
dest=h/'record-integration69.py';assert not dest.exists();dest.write_text(s,encoding='utf-8',newline='\n')
s=(h/'contact-reader68.py').read_text(encoding='utf-8').replace('visual68','visual69').replace("==14",'==8').replace('==11','==6').replace('range(0,11,4)','range(0,6,4)').replace('min(i+4,11)','min(i+4,6)').replace('all11_steps','all6_steps').replace('fourteen captures/eleven rendered proof steps','eight captures/six rendered proof steps')
dest=h/'contact-reader69.py';assert not dest.exists();dest.write_text(s,encoding='utf-8',newline='\n')
print('Prepared69 root integration/visual record helpers; no canonical metadata, gate or acceptance written.')
