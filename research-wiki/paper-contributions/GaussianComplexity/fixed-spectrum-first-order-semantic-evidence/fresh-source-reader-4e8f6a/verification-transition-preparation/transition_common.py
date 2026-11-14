from pathlib import Path
import copy,hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a'
PREP=BASE/'verification-transition-preparation'
PUBLIC=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-first-order.json'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
DISCOVERY=ROOT/'runs/substantive_discoveries.jsonl'
HEAD='9d306d837fbddf1518b0035494baaf5c21c24488'
AUDIT_BEFORE='ff19477ff58f2bedfb7790b6edd006d05b0386185011e6d21a9fa47f28651e4e'
ACTOR='/root/source_reader_4e8f6a'
OWNER='huanjian_gc_20261108_fixed_spectrum_first_order'
ADVANCE='ASTIS-SA-20261108-GaussianComplexityFixedSpectrumFirstOrder'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query'
AUDIT_ID='ASTIS-RT-20261108-HuanjianFixedSpectrumFirstOrder'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'website/scripts'))
from tools import astis_advance as advance
import astis_semantic_roundtrip as rt
import astis_publication as publication
import astis_frontier_cells as frontier

def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def readjson(p):return json.loads(Path(p).read_text())
def writejson(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def state():
 return advance._replay_advances([json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()])
def foreign_state_digest(s):
 return sha(canonical({k:v for k,v in s.items() if k!=ADVANCE}))
def foreign_audit_digest(reg):
 return sha(canonical({k:v for k,v in reg.items() if k!='audits'}|{'audits':[a for a in reg['audits'] if a.get('id')!=AUDIT_ID]}))
def frontier_hashes():
 # Preservation covers all 444 JSON artifacts, including three underscore
 # examples excluded by the validator's 441 actual-cell inventory.
 return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted(frontier.DEFAULT_CELL_ROOT.rglob('*.json'))}
def tracked_changes():
 return sorted(x for x in git('diff','--name-only',HEAD).decode().splitlines() if x)
def prospective(proposal):
 reg=rt.load_registry()
 matches=[i for i,a in enumerate(reg['audits']) if a.get('id')==AUDIT_ID]
 assert len(matches)==1,matches
 reg=copy.deepcopy(reg);reg['audits'][matches[0]]=copy.deepcopy(proposal)
 schema_errors=rt.validate_registry(reg)
 data=publication.inputs()
 data={**data,'audits':{**data['audits'],AUDIT_ID:proposal}}
 pub_errors=publication.validate(publication.load(),data,strict_names={DECL})
 known={b['declaration'] for i in publication.load() for b in i['bindings']}
 if DECL not in known:pub_errors.append('Own declaration missing publication record')
 ownitem=next(i for i in publication.load() if i['id']=='huanjian-fixed-spectrum-first-order')
 ownbinding=next(b for b in ownitem['bindings'] if b['declaration']==DECL)
 digest=publication.binding_digest(ownitem,ownbinding,data)
 assert digest==proposal['publication_binding_sha256']
 assert publication.review_context(ownitem,ownbinding,data)==proposal['publication_context']
 assert rt.semantic_reviewer_packet(proposal)['packet_sha256']=='9f6bb17d32f9661f999fb0de7aa20c2ea15d2971ef78c9e30165d0bca0b80524'
 return {'schema_errors':schema_errors,'publication_errors':pub_errors,
   'registry_schema_version':reg['schema_version'],'registry_protocol_preserved':reg['protocol']==rt.load_registry()['protocol'],
   'merged_audit_count':len(reg['audits']),'publication_binding_sha256':digest,
   'method':'Actual rt.load_registry() top-level schema/protocol and all merged audits, replacing exactly own fragment in memory; actual publication.validate with prospective own audit only. No canonical writes or normal transition API.'}

def assert_protected(baseline, *, after=False):
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 assert sha(git('ls-files','-s','-z'))==baseline['git_index_entries_sha256']
 wanted=sorted([AUDIT.relative_to(ROOT).as_posix(),LEDGER.relative_to(ROOT).as_posix()]) if after else []
 assert tracked_changes()==wanted,(tracked_changes(),wanted)
 assert sha(DISCOVERY.read_bytes())==baseline['discovery_sha256']
 assert frontier_hashes()==baseline['frontier_hashes']
 for rel,h in baseline['frozen_review_and_provenance_files'].items():
  assert sha((ROOT/rel).read_bytes())==h,rel
 current=state()
 assert len(current)==285 and foreign_state_digest(current)==baseline['foreign_sau_state_sha256']
 assert current[ADVANCE]['owner_id']==OWNER and current[ADVANCE]['created_by']==OWNER
 assert foreign_audit_digest(rt.load_registry())==baseline['foreign_audits_and_protocol_sha256']
 return current
