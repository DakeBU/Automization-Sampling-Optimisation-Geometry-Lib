from pathlib import Path
import json,sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(ROOT))
from tools import astis_publication as publication
from tools import astis_semantic_roundtrip as roundtrip
name='AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query'
publication.check_advance([name],reviewed=True)
audit=next(a for a in roundtrip.load_registry()['audits'] if a['id']=='ASTIS-RT-20261107-HuanjianFirstOrderQuery')
packet=roundtrip.semantic_reviewer_packet(audit)
assert packet['packet_sha256']=='1a1b7d8c5ce75da07ba11554e311dafcbff27eb84792fa4b66560efbec1696ea'
assert audit['source_review']['reviewer']=='/root/reader_570298'
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
print(json.dumps({'gate':'PASS real publication.check_advance(reviewed=True) including full semantic registry validation',
 'declaration':name,'audit_state':audit['state'],'source_review':audit['source_review']['state'],
 'reviewer_packet_sha256':packet['packet_sha256'],
 'scope':'Independent source-V admission only; not canonical root or integration gate.'},indent=2))
