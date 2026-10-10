$ErrorActionPreference = 'Stop'
$out = 'E:\Samplinglib\.astis\decoder-61\independent'
$utf8 = [System.Text.UTF8Encoding]::new($false)
function Sha([byte[]]$bytes) { [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant() }
function Record([string]$path) {
 $bytes=[System.IO.File]::ReadAllBytes($path)
 $lf=$utf8.GetBytes($utf8.GetString($bytes).Replace("`r`n","`n").Replace("`r","`n"))
 [ordered]@{path=$path;raw_sha256=(Sha $bytes);raw_bytes=$bytes.Length;lf_sha256=(Sha $lf);lf_bytes=$lf.Length}
}
$pins=[System.IO.File]::ReadAllText(($out+'\input-pins.json'),$utf8)|ConvertFrom-Json
foreach ($pin in $pins) { $rec=Record $pin.path; if ($rec.raw_sha256 -ne $pin.raw_sha256 -or $rec.raw_bytes -ne $pin.raw_bytes) { throw 'Original neutral input changed before closure' } }
$run=[System.IO.File]::ReadAllText(($out+'\decoder-native-run.json'),$utf8)|ConvertFrom-Json
$payload=[System.IO.File]::ReadAllBytes(($out+'\decoder-native-run.payload.json'))
if ((Sha $payload) -ne $run.decoder_payload_sha256) { throw 'Named payload mismatch' }
$prefix=$utf8.GetBytes('ASTIS-ANONYMOUS-DECODER-NATIVE-RUN-v1'+[char]0)
$bound=[byte[]]::new($prefix.Length+$payload.Length)
[Array]::Copy($prefix,0,$bound,0,$prefix.Length)
[Array]::Copy($payload,0,$bound,$prefix.Length,$payload.Length)
if ((Sha $bound) -ne $run.decoder_run_sha256) { throw 'Native run binding mismatch' }
foreach ($index in @(0,1)) {
 $decoded=[System.IO.File]::ReadAllText(($out+'\decoded'+$index+'.json'),$utf8)|ConvertFrom-Json
 $textBytes=[System.IO.File]::ReadAllBytes(($out+'\reconstructed'+$index+'.txt'))
 $packet=[System.IO.File]::ReadAllText(('E:\Samplinglib\.astis\decoder-61\packet'+$index+'.json'),$utf8)|ConvertFrom-Json
 if ((Sha $textBytes) -ne $decoded.reconstructed_sha256 -or $decoded.reconstructed_text_sha256 -ne $decoded.reconstructed_sha256) { throw 'Reconstructed text digest mismatch' }
 if ($utf8.GetString($textBytes) -cne $decoded.reconstructed_theorem_text) { throw 'Reconstructed text body mismatch' }
 if ((Sha ($utf8.GetBytes($packet.lean.statement))) -ne $decoded.statement_sha256) { throw 'Statement binding mismatch' }
 if ($decoded.decoder_run_sha256 -ne $run.decoder_run_sha256 -or $decoded.decoder_payload_sha256 -ne $run.decoder_payload_sha256) { throw 'Decoded identity mismatch' }
}
$names=@('input-pins.json','prepare.ps1','readback.ps1','close.ps1','reconstructed0.txt','reconstructed1.txt','decoded0.json','decoded1.json','decoder-native-run.payload.json','decoder-native-run.json')
$records=@($names|ForEach-Object {Record ($out+'\'+$_)})
$evidence=[ordered]@{schema_version=1;phase='actual foreground raw-byte readback before lease closure';checks_passed=$true;native_run_id=$run.native_run_id;decoder_run_sha256=$run.decoder_run_sha256;decoder_payload_sha256=$run.decoder_payload_sha256;preparation_command=[ordered]@{chunk_id='c4f2c6';exit_code=0};verified_original_inputs=$pins;verified_output_artifacts=$records;expected_process_exit_code=0;source_text_visible=$false;source_identity_visible=$false;compiler_started=$false}
[System.IO.File]::WriteAllText(($out+'\foreground-readback.json'),(ConvertTo-Json -InputObject $evidence -Depth 30),$utf8)
[ordered]@{foreground_readback_passed=$true;outputs=$records;readback_evidence=(Record ($out+'\foreground-readback.json'));decoder_run_sha256=$run.decoder_run_sha256;decoder_payload_sha256=$run.decoder_payload_sha256}|ConvertTo-Json -Depth 30
exit 0
