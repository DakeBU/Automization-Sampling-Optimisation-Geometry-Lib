"""PREPARED ONLY. Separate exact target-cell projection. No normal transition API import or call."""
from verification_common import *
import argparse

ALLOWED=['/status','/evidence/independent_verification','/evidence/normal_V','/evidence/current_normal_stage','/phase_snapshot']

def checked_outcome():
    out=read(OWN/'normal-V-outcome.public.json')
    assert out['advance_id']==ADV and out['verifier_id']==VERIFIER and out['normal_API_calls']==1 and out['actual_exit_code']==0 and out['all_window1_postguards_passed'] and out['all_frontiers_including_target_unchanged']
    assert out['actual_math_build_identity']==MATH and file_sha(OWN/'normal-V-exact-append.jsonl')==out['exact_appended_record_sha256']
    return out

def checked_portable_refs():
    assert (REPO/VOUT_PUBLIC).read_bytes()==(OWN/'normal-V-outcome.public.json').read_bytes()
    assert (REPO/VAPP_PUBLIC).read_bytes()==(OWN/'normal-V-exact-append.jsonl').read_bytes()
    return ident(REPO/VOUT_PUBLIC),ident(REPO/VAPP_PUBLIC)

def schema_check(candidate):
    sys.path.insert(0,str(REPO));from tools import astis_frontier_cells as cells
    context=cells.load_cells();found=[c for c in context if c.get('cell_id')==candidate['cell_id']];assert len(found)==1
    probe=copy.deepcopy(candidate);probe['__path__']=found[0]['__path__']
    errors=cells.validate_cells([probe if c is found[0] else c for c in context])
    return errors

def validate_candidate(old,new,out):
    assert old['status']=='proved_locally' and old['owner_id']==OWNER and old['advance_id']==ADV
    assert new['status']=='independently_verified' and new['owner_id']==OWNER and new['advance_id']==ADV
    portable_outcome,portable_append=checked_portable_refs();ref=VOUT_PUBLIC
    assert isinstance(new['evidence']['independent_verification'],str) and new['evidence']['independent_verification']==ref
    assert new['evidence']['normal_V']['actual_normal_outcome']==portable_outcome and new['evidence']['normal_V']['actual_exact_append']==portable_append and new['evidence']['normal_V']['verifier_id']==VERIFIER and new['evidence']['normal_V']['actual_calls']==1
    stage=new['evidence']['current_normal_stage'];assert stage['advance_state']=='VERIFIED' and stage['cell_status']=='independently_verified' and stage['normal_independent_proof_VERIFIED_calls']==1 and stage['actual_math_build_identity']==MATH and stage['verified_source_carrier']==out['verified_commit']
    changed=differences(old,new);assert all(any(k==base or k.startswith(base+'/') for base in ALLOWED) for k in changed)
    # The whitelist keeps every other source, sealed statement, coverage, audit, consumer and purification field exact.
    return changed

def prepare_proposal(carrier):
    # Read-only preparation after real window1; cannot be used before its actual outcome exists.
    out=checked_outcome();assert out['verified_commit']==carrier
    assert sha((REPO/ADVPATH).read_bytes())==out['post_advance_ledger_sha256'] and sha((REPO/DISCPATH).read_bytes())==out['post_discovery_ledger_sha256']
    portable_outcome,portable_append=checked_portable_refs()
    oldraw=(REPO/CELL).read_bytes();old=json.loads(oldraw);new=copy.deepcopy(old);new['status']='independently_verified';e=new['evidence']
    e['independent_verification']=VOUT_PUBLIC
    e['normal_V']={'state':'VERIFIED','actual_calls':1,'actual_normal_outcome':portable_outcome,'actual_exact_append':portable_append,'verifier_id':VERIFIER,'verified_source_carrier':carrier}
    e.setdefault('current_normal_stage',{}).update({'advance_state':'VERIFIED','cell_status':'independently_verified','theorem_VERIFIED':True,'normal_independent_proof_VERIFIED_calls':1,'verifier_id':VERIFIER,'verified_source_carrier':carrier,'actual_math_build_identity':MATH})
    new['phase_snapshot']='One normal PL and one independent normal proof V by '+VERIFIER+' at source/evidence carrier '+carrier+'. Current reader is independently accepted within its preserved bounded report. Actual native build remains immutablea8bb; no new build/reader/source review. API window preserved all frontiers; this cell is proposed for a separate authorized projection. Main/production, stabilization, purification and full-paper/whole-Goal completion remain pending. Earlier process snapshots and mathematical/source fields are retained.'
    changed=validate_candidate(old,new,out);errors=schema_check(new)
    private_dir(PRIVATE/'projection-preparation');write(PRIVATE/'projection-preparation/schema-errors.private.json',errors)
    assert not errors
    raw=(json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode();exact(OWN/'target-cell-proposal.exact.json',raw)
    write(OWN/'target-cell-proposal.public.json',{'status':'READONLY_EXACT_PROPOSAL_NOT_APPLIED','advance_id':ADV,'before_cell_sha256':sha(oldraw),'proposed_cell_sha256':sha(raw),'changed_field_paths':changed,'canonical_full_context_schema_errors':0,'normal_API_calls':0,'normal_V_outcome':ident(OWN/'normal-V-outcome.public.json'),'expected_advance_ledger_sha256':out['post_advance_ledger_sha256'],'expected_discovery_ledger_sha256':out['post_discovery_ledger_sha256'],'separate_ROOT_window2_authorization_required':True})
    print(json.dumps({'status':'READONLY_EXACT_PROPOSAL_NOT_APPLIED','proposed_cell_sha256':sha(raw),'changed_field_paths':changed}))
    return 0

def cell_window(a,authpath):
    marker=PRIVATE/'target-cell-attempted.once.json';assert not marker.exists();out=checked_outcome()
    assert out['verified_commit']==a['carrier_commit'] and a['window1_outcome']['file']==VOUT_PUBLIC and pin_bytes(a['window1_outcome'])==(OWN/'normal-V-outcome.public.json').read_bytes()
    before=snapshot('window2-before',a);pl=read(OWN/'PROVED_LOCAL-original25.exact.json');inspect_target(before,pl,'VERIFIED')
    assert sha(before['araw'])==a['expected_advance_ledger_sha256']==out['post_advance_ledger_sha256'] and sha(before['draw'])==a['expected_discovery_ledger_sha256']==out['post_discovery_ledger_sha256']
    assert {n.decode() for n in git('window2-worktree','diff','--name-only','HEAD','-z').split(b'\0') if n}=={ADVPATH}
    assert not git('window2-index','diff','--cached','--name-only','-z')
    oldraw=(REPO/CELL).read_bytes();assert sha(oldraw)==a['expected_target_cell_sha256'];old=json.loads(oldraw)
    raw=pin_bytes(a['projection_candidate']);assert sha(raw)==a['expected_projected_cell_sha256'];new=json.loads(raw)
    changed=validate_candidate(old,new,out);errors=schema_check(new);write(PRIVATE/'window2-schema-errors.private.json',errors)
    write(OWN/'window2-schema-precheck.public.json',{'candidate_sha256':sha(raw),'canonical_full_context_schema_error_count':len(errors),'errors_original_private':True,'before_attempt_marker':True})
    assert not errors
    exact(PRIVATE/'window2-target.before.exact.json',oldraw);exact(PRIVATE/'window2-target.proposed.exact.json',raw)
    assert (REPO/CELL).read_bytes()==oldraw
    write(marker,{'local_private_do_not_publish':True,'advance_id':ADV,'authorization_sha256':file_sha(authpath),'about_to_write_only_exact_target_cell_once':True,'before_sha256':sha(oldraw),'after_sha256':sha(raw),'normal_API_calls':0})
    with (REPO/CELL).open('r+b') as f:f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())
    after=snapshot('window2-after',a);g=postguards(before,after,a,{CELL},cell_exception=CELL)
    assert g['only_changed_tracked_paths']==[CELL] and before['araw']==after['araw'] and before['draw']==after['draw'] and (REPO/CELL).read_bytes()==raw
    write(OWN/'window2-postguards.public.json',{'advance_id':ADV,'all_postguards_passed':True,'target_status':'independently_verified','only_target_cell_projected':True,'before_cell_sha256':sha(oldraw),'after_cell_sha256':sha(raw),'changed_field_paths':changed,'normal_API_calls':0,'additional_V_calls':0,'both_ledgers_exact':True,'all_other_tracked_frontiers_modes_HEAD_branch_index_unchanged':True,'all_other_target_fields_source_seals_audits_consumers_purification_unchanged':True,'normal_V_outcome':ident(OWN/'normal-V-outcome.public.json'),'guards':g})

def main():
    os.umask(0o077);p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare-only',action='store_true');p.add_argument('--carrier');p.add_argument('--authorization',type=Path);p.add_argument('--authorization-sha256');p.add_argument('--child',action='store_true');args=p.parse_args()
    if args.prepare_only:
        assert args.carrier and not args.authorization and not args.child
        return prepare_proposal(args.carrier)
    assert args.authorization and args.authorization_sha256 and not args.carrier
    return run_captured(args,'TARGET_CELL_PROJECTION_ONCE',cell_window)
if __name__=='__main__':sys.exit(main())
