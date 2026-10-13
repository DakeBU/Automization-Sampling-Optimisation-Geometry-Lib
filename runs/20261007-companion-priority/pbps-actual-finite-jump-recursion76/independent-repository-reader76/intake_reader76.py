import os
import review76 as r
packet=r.final_packet_inputs('54b29a35f4d68136e744724e6fafd567f33a54a56b33d13faf6f4ba6d7b9403d')
assert len(packet['inputs'])==149
r.save('inputs.manifest.json',dict(dispatch=r.pin(r.DIS),input_count=len(packet['inputs']),inputs=packet['inputs'],actual_intake_PID=os.getpid(),current_reader_acceptance=False))
r.save('final-dispatch.exactraw.json',packet)
print(r.json.dumps(dict(status='PASS_149_FROZEN_INPUT_PINS',actual_intake_PID=os.getpid(),dispatch_RAW_sha256=r.sha(r.DIS.read_bytes()),input_count=len(packet['inputs']),PNGs=sum(x['path'].endswith('.png') for x in packet['inputs']),new_mathematical_source_or_VERIFIED_credit=False)))
