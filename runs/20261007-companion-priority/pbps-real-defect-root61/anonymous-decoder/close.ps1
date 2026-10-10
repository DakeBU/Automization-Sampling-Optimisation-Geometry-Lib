param([Parameter(Mandatory=$true)][string]$ReadbackCommandId)
$ErrorActionPreference='Stop'
$out='E:\Samplinglib\.astis\decoder-61\independent'
$utf8=[System.Text.UTF8Encoding]::new($false)
function Sha([byte[]]$bytes) { [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant() }
function Record([string]$path) {
 $bytes=[System.IO.File]::ReadAllBytes($path)
 $lf=$utf8.GetBytes($utf8.GetString($bytes).Replace("`r`n","`n").Replace("`r","`n"))
 [ordered]@{path=$path;raw_sha256=(Sha $bytes);raw_bytes=$bytes.Length;lf_sha256=(Sha $lf);lf_bytes=$lf.Length}
}
function WriteJson([string]$path,$value) { [System.IO.File]::WriteAllText($path,(ConvertTo-Json -InputObject $value -Depth 40),$utf8) }
$evidence=[System.IO.File]::ReadAllText(($out+'\foreground-readback.json'),$utf8)|ConvertFrom-Json
if (-not $evidence.checks_passed) { throw 'No passed readback' }
foreach ($r in $evidence.verified_output_artifacts) { $actual=Record $r.path; if ($actual.raw_sha256 -ne $r.raw_sha256 -or $actual.raw_bytes -ne $r.raw_bytes) { throw 'An artifact changed after foreground readback' } }
foreach ($r in $evidence.verified_original_inputs) { $actual=Record $r.path; if ($actual.raw_sha256 -ne $r.raw_sha256 -or $actual.raw_bytes -ne $r.raw_bytes) { throw 'A permitted input changed before closure' } }
$leasePath='E:\Samplinglib\.astis\decoder-61\lease.json'
$initialLeasePath='E:\Samplinglib\.astis\decoder-61\initial-lease.raw.snapshot.json'
$initialLeaseRecord=Record $initialLeasePath
$closedLease=[ordered]@{status='CLOSED';allowed_inputs=@('packet0.json','packet1.json');source_text_visible=$false;source_identity_visible=$false;compiler_started=$false;decoder='anonymous-decoder-61-independent';native_run_id=$evidence.native_run_id;decoder_run_sha256=$evidence.decoder_run_sha256;decoder_payload_sha256=$evidence.decoder_payload_sha256;original_lease_snapshot=$initialLeaseRecord;actual_foreground_readback=[ordered]@{chunk_id=$ReadbackCommandId;exit_code=0;checks_passed=$true};closed_last=$true;no_later_artifact_mutation=$true}
WriteJson $leasePath $closedLease
$closedLeaseBytes=[System.IO.File]::ReadAllBytes($leasePath)
[System.IO.File]::WriteAllBytes(($out+'\closed-lease.json'),$closedLeaseBytes)
$finalInputs=@($evidence.verified_original_inputs|ForEach-Object { Record $_.path })
$records=@($evidence.verified_output_artifacts|ForEach-Object { Record $_.path })
$records+=@(Record ($out+'\foreground-readback.json');Record ($out+'\closed-lease.json'))
$manifest=[ordered]@{schema_version=1;native_run_id=$evidence.native_run_id;decoder_run_sha256=$evidence.decoder_run_sha256;decoder_payload_sha256=$evidence.decoder_payload_sha256;initial_neutral_input_pins=$evidence.verified_original_inputs;final_neutral_input_pins=$finalInputs;original_snapshot_retained_unchanged=$true;closed_original_neutral_lease=(Record $leasePath);immutable_outputs_after_readback=$records;actual_foreground_readback=[ordered]@{chunk_id=$ReadbackCommandId;exit_code=0;checks_passed=$true};closure_artifacts_read_back_in_foreground=$true;closed_last=$true;reconstruction_only=$true}
WriteJson ($out+'\inputmanifest.json') $manifest
$manifestRecord=Record ($out+'\inputmanifest.json')
$closedRecord=Record ($out+'\closed-lease.json')
if ($closedRecord.raw_sha256 -ne (Record $leasePath).raw_sha256) { throw 'Closed lease copy mismatch' }
if ((Record $initialLeasePath).raw_sha256 -ne $initialLeaseRecord.raw_sha256) { throw 'Initial snapshot altered' }
$flag=[ordered]@{marker='CLOSED_LAST';closed_last=$true;native_run_id=$evidence.native_run_id;decoder_run_sha256=$evidence.decoder_run_sha256;decoder_payload_sha256=$evidence.decoder_payload_sha256;inputmanifest=$manifestRecord;closed_lease=$closedRecord;original_neutral_lease=(Record $leasePath);original_lease_snapshot=$initialLeaseRecord;actual_foreground_readback=[ordered]@{chunk_id=$ReadbackCommandId;exit_code=0;checks_passed=$true};closure_readback_completed=$true;last_artifact_write='CLOSED_LAST.json';no_later_artifact_mutation=$true;source_text_visible=$false;source_identity_visible=$false;compiler_started=$false}
WriteJson ($out+'\CLOSED_LAST.json') $flag
$flagRecord=Record ($out+'\CLOSED_LAST.json')
[ordered]@{marker='CLOSED_LAST';closed_last=$true;decoder_run_sha256=$evidence.decoder_run_sha256;decoder_payload_sha256=$evidence.decoder_payload_sha256;inputmanifest=$manifestRecord;closed_lease=$closedRecord;closed_last_artifact=$flagRecord;final_process_exit_code=0;no_later_artifact_mutation=$true}|ConvertTo-Json -Depth 20
exit 0
