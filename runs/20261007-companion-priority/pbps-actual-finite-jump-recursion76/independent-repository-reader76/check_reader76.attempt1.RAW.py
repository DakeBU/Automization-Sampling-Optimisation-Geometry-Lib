from types import SimpleNamespace
import os, sys
import review76 as r

def native_reuse():
    results=[]
    for name,count in [('independent-math76',82),('exact-science-verification76',97),('integration76/source-communication-qualification76',18)]:
        lp=r.R/name/'lease.final.json'; lease=r.load(lp)
        assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63'
        rows=lease['all_owned_outputs_except_only_self']
        assert len(rows)+1==lease['owned_count']==count
        assert r.sha(r.can(rows))==lease['closure_logical_sha256']
        result=r.verify_finite_closed(lp,rows)
        result['kind']=name; result['whole_logical_run_sha256']=lease['whole_logical_run_sha256']
        r.check(lease['complete_named_RAW_payload'])
        if name=='independent-math76':
            assert lease['accepted_whole_mathematics'] and not lease['VERIFIED'] and not lease['source_fidelity_verdict']
        if name=='exact-science-verification76':
            assert lease['VERIFIED'] and lease['verified_commit']==r.SCI
        results.append(result)
    # The old source review is checked only as immutable native evidence. Its judgment is not self-recertified.
    lp=r.SOURCE_REVIEW/'CLOSED_LAST.json'; raw=lp.read_bytes(); lease=r.json.loads(raw)
    assert r.sha(raw)==r.SOURCE_LEASE_SHA and lease['state']=='CLOSED_LAST'
    assert len(lease['files'])==lease['file_count_before_marker']==120
    paths={item['path'] for item in lease['files']}
    assert {path.relative_to(r.SOURCE_REVIEW).as_posix() for path in r.SOURCE_REVIEW.rglob('*') if path.is_file()}==paths|{'CLOSED_LAST.json'}
    for item in lease['files']:
        b=(r.SOURCE_REVIEW/item['path']).read_bytes()
        assert len(b)==item['RAW_bytes'] and r.sha(b)==item['RAW_sha256']
        assert r.sha(b.replace(b'\r\n',b'\n'))==item['CRLF_to_LF_only_sha256']
    results.append(dict(kind='source-CLOSED121-immutable-evidence-only',lease=r.pin(lp),owned_files=121,new_source_certification=False,new_mathematics_certification=False))
    adoption=r.load(r.R/'root.decoder76.adoption.json')
    r.check(adoption['native_lease']); r.check(adoption['native_complete_payload'])
    lp=r.resolve(adoption['native_lease']['path']); lease=r.load(lp)
    assert lease['status']=='CLOSED' and lp.read_bytes()==(r.R/'anonymous-decoder/CLOSED_LAST.json').read_bytes()
    assert len(lease['bound_prior_owned_files'])==3 and lease['closed_exit_receipt']['exit_code']==0
    result=r.verify_finite_closed(lp,lease['bound_prior_owned_files']); result['kind']='strict-blind-decoder76-native-four-file-directory'; results.append(result)
    for name,keys in [('root.math76.adoption.json',['native_lease','native_complete_named']),('root.source76.adoption.json',['native_named_payload','native_report','native_lease']),('root.exact-verification76.adoption.json',['native_complete_named','native_lease','unique_VERIFIED_append']),('root.communication76.adoption.json',['native_lease','native_run','decision','addendum','canonical_audit'])]:
        adoption=r.load(r.R/name)
        for key in keys:r.check(adoption[key])
    math=r.load(r.R/'root.math76.adoption.json'); compiler=math['fresh_compiler']
    assert math['readonly_EXIT']==0 and math['mathematical_repairs']==[]
    assert compiler['fresh_source_elaboration'] and not compiler['Lake_build_cache_replay'] and compiler['terminal_EXIT']==0
    assert compiler['actual_foreground_Lean_PID']==28496 and compiler['axioms_PID']==29336 and len(compiler['standard_axioms'])==3
    for key in ['compiler_receipt','axiom_receipt']:
        r.check(compiler[key]); receipt=r.load(compiler[key]['path'])
        assert receipt['terminal_closed'] and receipt['terminal_EXIT']==0
    exact=r.load(r.R/'root.exact-verification76.adoption.json')
    assert exact['native_readonly_EXIT']==0 and exact['native_verified'] and exact['verified_commit']==r.SCI
    assert not exact['full_RAW_whitespace_PASS'] and exact['authored_complement_PASS']
    return results

def qualification(audit,packet):
    directory=r.R/'integration76/source-communication-qualification76'
    lease=r.load(directory/'lease.final.json'); decision=r.load(directory/'decision.json')
    proposal=r.load(directory/'qualification.addendum.proposed.json'); run=r.load(directory/'run.json')
    assert lease['owned_count']==18 and lease['actor']==decision['actor']==proposal['actor']=='/root/exact_science63'
    assert proposal['actor']!=r.ACTOR and proposal['actor']!='companion_root_20261005'
    assert r.sha(r.can({key:value for key,value in run.items() if key!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']
    assert run['run_sha256']=='f0bcdae9864810e4271fcc74533099f78bfe86208d15017f21d38719f486c75a'
    for key in ['decision','inputs_manifest','complete_named_RAW_payload']:r.check(run[key])
    assert decision['accepted'] and decision['append_only_qualification_required']
    assert decision['native_false_flag_overbroad'] and decision['native_bytes_must_remain_unchanged']
    assert decision['mathematics_status_notice_received'] and decision['coordinate_metadata_notice_received']
    assert not decision['earlier_semantic_source_verdict_payload_received']
    assert not decision['source_fidelity_admission_invalidated_by_disclosed_notice'] and not decision['fresh_source_review_required']
    assert not decision['new_VERIFIED'] and not decision['Lean_recompiled'] and not decision['aggregate'] and not decision['reader']
    assert proposal['native_broad_false_flag_retained'] and not proposal['native_broad_false_flag_accurate_as_universal_no_outcomes_claim']
    assert not proposal['new_semantic_verdict'] and not proposal['new_VERIFIED']
    notice=r.check(proposal['exact_disclosed_notice']).decode('utf-8')
    assert '根只读采纳独立数学已完成' in notice and '坐标过期的非数学 metadata 问题' in notice
    assert '不要读取或引用其他审查 verdict' in notice
    for key in ['source_native_lease','source_native_run']:r.check(proposal[key])
    # Retain the exact old broad flag, interpreted only together with the independently reviewed addendum.
    native=r.load(r.SOURCE_REVIEW/'review-logical-run76.json')
    assert native['prior_verdicts_or_other_reviewer_outcomes_seen'] is False
    link=audit['source_review']['communication_provenance_qualification']
    for key,filename in [('addendum','qualification.addendum.proposed.json'),('decision','decision.json'),('native_closed_lease','lease.final.json')]:
        r.check(link[key]); assert r.resolve(link[key]['path']).resolve()==(directory/filename).resolve()
    assert link['whole_logical_run_sha256']==run['run_sha256']
    assert link['mathematics_status_notice_received'] and link['coordinate_metadata_notice_received']
    assert link['native_broad_false_flag_not_a_universal_no_communication_claim'] and link['native_source_RAW_preserved'] and not link['new_VERIFIED']
    assert link['scope']==decision['limitations'] and link['reaudit_trigger']==decision['strict_reaudit_trigger']
    adoption=r.load(r.R/'root.communication76.adoption.json')
    assert adoption['independent_actor']==proposal['actor'] and adoption['packet_and_binding_unchanged'] and adoption['native_closed_files_unchanged']
    assert not adoption['new_VERIFIED'] and not adoption['new_math_or_source_verdict']
    assert audit['publication_binding_sha256']==packet['publication_binding_sha256']=='ef7ddf32173166e15704713b04a186c1ae19f324f9d555083a416ed5af930c11'
    assert audit['source_review']['reviewer_packet_sha256']==packet['packet_sha256']=='1a72e794cd4e22dd03762b4a58d82419d1c49372cd8252f8611ba8335b37580d'
    return dict(status='PASS_INDEPENDENT_QUALIFICATION_BINDING_AND_DISCLOSURE_ONLY',independent_actor=proposal['actor'],native_closed_owned_files=18,whole_logical_run_sha256=run['run_sha256'],canonical_link=link,decision=r.pin(directory/'decision.json'),addendum=r.pin(directory/'qualification.addendum.proposed.json'),lease=r.pin(directory/'lease.final.json'),mathematics_status_and_coordinate_notice_disclosed=True,old_broad_false_preserved_but_not_universal_claim=True,additional_undisclosed_messages_not_audited=True,no_private_session_store_audit=True,new_source_or_math_verdict=False,new_VERIFIED=False,self_validation_of_old_source_verdict=False)

def main():
    im=r.load(r.O/'inputs.manifest.json'); dispatch=r.final_packet_inputs('54b29a35f4d68136e744724e6fafd567f33a54a56b33d13faf6f4ba6d7b9403d')
    assert im['inputs']==dispatch['inputs'] and im['input_count']==149
    for item in im['inputs']:r.check(item)
    src=(r.ROOT/r.MOD).read_bytes(); assert r.sha(src)==r.SOURCE and len(src)==22655
    lines=src.splitlines(keepends=True); assert len(lines)==412
    lesson=r.load('website/content/declaration_lessons/pbps-actual-finite-jump-recursion.json')['units'][0]
    pub=r.load('website/content/publications/pbps-actual-finite-jump-recursion.json')['items'][0]
    audit=r.load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualFiniteJumpRecursion.json')
    cell=r.load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-jump-recursion.json')
    packet=r.load(r.R/'source-review.clean.packet.json')
    assert lesson['declaration']==r.DECL and pub['bindings'][0]['declaration']==r.DECL and len(lesson['steps'])==10
    spans=[]; previous=192
    for index,step in enumerate(lesson['steps'],1):
        region=step['lean_source_region']; a,b=region['start_line'],region['end_line']
        code=b''.join(lines[a-1:b])
        assert a==previous+1 and code.decode()==step['lean'] and r.sha(code)==region['exact_code_raw_sha256']
        assert region['source_raw_sha256']==r.SOURCE and region['path']==r.MOD and step['formula'] and step['text']
        spans.append(dict(step=index,title=step['title'],start_line=a,end_line=b,exact_BODY_RAW_sha256=r.sha(code))); previous=b
    assert previous==409
    for word in ['rank zero','C²','0<α≤β','βη≤1','η>0','phase-free stopped','including zeros','fixed y,xRef','No iid realization','Markov law','cost theorem']:
        assert word in lesson['statement'],word
    assert 'six original analytic callers' in ' '.join(lesson['assumptions'])
    assert 'never supplied as callers' in ' '.join(lesson['assumptions'])
    for caller in ['hα','hαβ','hV','hH','hη','hβη']:assert '('+caller+' :' in src.decode()
    sys.path.insert(0,str(r.ROOT/'tools')); import astis_publication as ap
    data=dict(declarations={r.DECL:SimpleNamespace(source_file=r.MOD)},lessons={r.DECL:lesson})
    binding=ap.binding_digest(pub,pub['bindings'][0],data); context=ap.review_context(pub,pub['bindings'][0],data)
    assert binding==audit['publication_binding_sha256'] and context==audit['publication_context']
    assert audit['state']=='accepted' and audit['verdict']=='equivalent-after-elaboration'
    native_report=r.load(r.SOURCE_REVIEW/'compiled-source-review76.json')
    # Literal adoption integrity only; no fresh source judgment from the original source reviewer.
    for key in ['semantic_slots','verdict','repairs']:assert audit[key]==native_report['audit_fields'][key]
    for key,value in native_report['source_review'].items():assert audit['source_review'][key]==value,key
    assert audit['source_review']['reviewer']==r.ACTOR and audit['source_review']['independent_from_decoder']
    assert len(audit['deltas'])==len(native_report['audit_fields']['deltas'])==4
    for original,adapted in zip(native_report['audit_fields']['deltas'],audit['deltas']):
        assert all(adapted[key]==value for key,value in original.items()) and adapted['severity']=='informational' and adapted['description']
    qual=qualification(audit,packet)
    html=(r.ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8')
    start=html.index('<section id="pbps-actual-finite-jump-recursion"'); end=html.find('<section id=',start+1)
    tree=r.Tree(); tree.feed(html[start:end if end!=-1 else None])
    article=next(node for node in tree.root.all('article') if node.attrs.get('data-authored-declaration')==r.DECL)
    details=article.all('details'); codes=[node.text() for node in article.all('code') if 'language-lean' in node.attrs.get('class','')]
    assert len(details)==16 and all('open' not in node.attrs for node in details)
    assert len(codes)==13 and lesson['statement'] in article.text()
    for step in lesson['steps']:assert step['lean'] in codes and step['formula'] in article.text() and step['text'] in article.text()
    assert 'private def actual_fixed_reference_finite_jump_recursion_statement' in article.text()
    visual=r.R/'integration76/visual76'; copy=r.load(visual/'copy-unit0-copy-and-download.inspect.json')
    assert copy['initialFolded'] and copy['copyProbeUsesIsolatedPageClipboardCallback'] and not copy['physicalOSClipboardTest']
    assert copy['closedLeanDetails']==16 and len(copy['panels'])==len(copy['downloads'])==3 and len(copy['steps'])==10
    copied=[]
    for panel in copy['panels']:
        assert panel['callbackCalled'] and panel['copiedExactly'] and panel['status']=='Copied'
        assert panel['code'] in codes and panel['code'] in src.decode()
        copied.append(dict(code_UTF8_RAW_bytes=len(panel['code'].encode()),code_RAW_sha256=r.sha(panel['code'].encode()),exact_continuous_module_fragment=True,callbackCalled=True,copiedExactly=True))
    assert len({item['code_RAW_sha256'] for item in copied})==3
    for download in copy['downloads']:
        assert download['status']==200 and download['text'].encode()==src and download['bytes']==len(download['text'])
    for step,observed in zip(lesson['steps'],copy['steps']):assert step['lean']==observed['lean'] and observed['initiallyFolded']
    render=r.load(visual/'render-capture.json'); cc=r.load(visual/'copy-capture.json')
    assert render['ownedBrowserExit']['code']==cc['ownedBrowserExit']['code']==0 and len(render['records'])==12 and len(cc['records'])==1
    pngs=[item for item in im['inputs'] if item['path'].endswith('.png')]; views=r.load(r.O/'independent-PNG-observations.json')
    assert len(pngs)==views['independently_viewed_PNGs']==13 and [x['input_pin'] for x in views['records']]==pngs
    assert views['actor']==r.ACTOR and views['independent_of_root_viewing']
    sys.path.insert(0,str(r.ROOT/'website/scripts')); import publication_reader
    graph=r.load('_site/data/underlying-lean-graph.json')
    assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
    mid='module:'+r.DECL.rsplit('.',1)[0]; did='decl:'+r.DECL; nodes={node['id']:node for node in graph['nodes']}
    assert nodes[mid]['status']==nodes[did]['status']=='compiled'
    direct=[edge for edge in graph['edges'] if did in [edge['source'],edge['target']]]
    assert len(direct)==6 and sum(x['relation']=='source reference (scanner)' for x in direct)==3
    for relation in ['declares','Lean target under audit','source correspondence; not a Lean dependency']:assert sum(x['relation']==relation for x in direct)==1
    for parent in ['ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']:
        assert any(edge['source']=='module:AutoSamplingTheory.ExampleCases.ProximalBPS.'+parent and edge['target']==mid and edge['relation']=='imports' for edge in graph['edges'])
    assert cell['status']=='independently_verified'
    gates=[]
    for item in im['inputs']:
        if item['path'].endswith('/receipt.json') and '/integration76/' in item['path']:
            receipt=r.load(item['path'])
            if 'exit_code' not in receipt:continue
            assert receipt['terminal_closed'] and receipt['exit_code']==0 and receipt['checked_parent']==r.SCI
            for stream in ['stdout','stderr']:r.check(receipt[stream])
            gates.append(dict(label=r.Path(item['path']).parent.name,actual_foreground_PID=receipt['actual_foreground_PID'],terminal_EXIT=0,terminal_closed=True,receipt=item))
    assert len(gates)==18
    logs=lambda name:(r.R/'integration76'/name/'stdout.log').read_text(encoding='utf-8')
    assert all(text in logs('mandatory-astis-check-final') for text in ['ASTIS check passed','Build completed successfully (9187 jobs).','Build completed successfully (9487 jobs).'])
    assert '246 source items' in logs('publication-final') and '525 compiled local leaves' in logs('website-ci-build')
    assert 'ASTIS site check passed' in logs('site-check-final') and '"omitted_connections": 0' in logs('graph-check-final')
    for name in ['reader-render-current','reader-copy-download']:assert 'CLOSED' in logs(name)
    notes=r.load(r.R/'integration.notes.json'); assert notes['proof_commit']==r.SCI and notes['registry_count']==525 and notes['publication_units']==246 and notes['root_jobs']==9187 and notes['test_jobs']==9487 and len(notes['checks'])==17
    assert notes['publication_inputs_sha256']==graph['publication_inputs_sha256'];r.check(notes['current_graph'])
    affected=r.load(r.R/'integration76/affected-module-graph/affected-graph.receipt.json')
    assert len(affected['outputs'])==5 and not affected['canonical_tool_source_changed'] and not affected['official_whole_module_graph_refresh_command_run']
    assert affected['unrelated_cards_external_indexes_leaf_docs_and_manifest_untouched']
    before=r.load(r.R/'integration76/before-generator-state.json')
    protected={r.resolve(path).resolve() for path in before['preexisting_tracked_changes']+before['untracked_cards']}
    changed=set()
    for item in affected['outputs']:r.check(item);changed.add(r.resolve(item['path']).resolve())
    assert not changed&protected and changed<={r.resolve(path).resolve() for path in before['keep']}
    reuse=r.load(r.R/'integration76/unchanged-regression-reuse.json')
    assert reuse['unchanged_Git_and_workspace'] and not reuse['fresh_full_suite_or_full_browser_for76'] and 'Historical executable RAW hashes were not recorded' in reuse['runtime_qualification']
    prior=[]
    for item in reuse['records']:
        for key in ['receipt','stdout','stderr']:r.check(item[key])
        receipt=r.load(item['receipt']['path']); assert receipt['exit_code']==0 and receipt['terminal_closed'] and not item['fresh_for76']
        prior.append(dict(label=item['label'],receipt=item['receipt'],actual_foreground_PID=receipt['actual_foreground_PID'],terminal_EXIT=0,fresh_for76=False))
    for item in reuse['current_runtime_pins']:r.check(item['current_pin']);assert item['mtime_predates_reused_runs'] and item['historical_RAW_hash_not_recorded']
    vf=r.load(r.R/'verified.json')
    assert vf['status']=='VERIFIED' and vf['verifier_id']=='/root/exact_science63' and vf['owner_id']!=vf['verifier_id'] and vf['verified_commit']==r.SCI and vf['transition_count']==1 and not vf['aggregate'] and not vf['current_reader']
    assert vf['event']['from_state']=='PROVED_LOCAL' and vf['event']['to_state']=='VERIFIED' and vf['event']['worker_id']==vf['verifier_id']
    append=r.check(vf['exact_append']); assert r.json.loads(append)==vf['event']
    ledger=(r.ROOT/'runs/substantive_advances.jsonl').read_bytes(); before_n=vf['ledger_before']['RAW_bytes'];after_n=vf['ledger_after']['RAW_bytes']
    assert r.sha(ledger[:before_n])==vf['ledger_before']['RAW_sha256'] and r.sha(ledger[:after_n])==vf['ledger_after']['RAW_sha256'] and ledger[before_n:after_n]==append
    transitions=[j for b in ledger.splitlines() if b.strip() for j in [r.json.loads(b)] if j.get('advance_id')==vf['advance_id'] and j.get('to_state')=='VERIFIED']
    assert len(transitions)==1 and transitions[0]==vf['event']
    native=native_reuse()
    result=dict(status='PASS_SCOPED_CURRENT_READER76_FINITE_CHECKS',actual_foreground_PID=os.getpid(),actor=r.ACTOR,checked_science_commit=r.SCI,all_dispatch_RAW_LF_pins=149,source_module=r.pin(r.ROOT/r.MOD),complete_module_lines=412,formula_BODY_spans=spans,initially_closed_details=16,exact_Lean_code_panels=13,copy_panel_fragments=copied,copy_callbacks=3,RAW_downloads=3,download_UTF8_RAW_bytes=len(src),download_Javascript_character_count=len(src.decode()),publication_binding_sha256=binding,publication_context_exact=True,source_binding_reused_unchanged=True,native_reviews_reused=native,communication_qualification=qual,current_gate_receipts=gates,current_graph_digest=graph['publication_inputs_sha256'],direct_graph_connections=direct,three_actual_parent_module_imports=True,graph_labels_dense=True,graph_not_theorem_implication=True,affected_generator_outputs=affected['outputs'],no_preexisting_or_untracked_collaborator_path_overwritten=True,prior_full_regressions_reused=prior,runtime_qualification=reuse['runtime_qualification'],physical_OS_clipboard_test=False,prior_unique_VERIFIED_transition_reused_only=True,new_VERIFIED_transition=False,new_independent_mathematics_certification=False,new_source_fidelity_certification=False,old_source_reviewer_actor_disclosed=r.ACTOR,reader_independent_of_formalizer_stabilizer=True)
    print(r.json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
