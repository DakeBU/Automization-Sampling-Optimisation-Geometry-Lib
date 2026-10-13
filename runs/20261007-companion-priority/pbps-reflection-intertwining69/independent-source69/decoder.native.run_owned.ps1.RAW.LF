$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$taskRoot = 'E:\Samplinglib\.astis\decoder-69\independent'
$taskUtf8 = [System.Text.UTF8Encoding]::new($false)
function Save-TaskJson([string]$path, $value) {
    $body = ($value | ConvertTo-Json -Depth 100) + "`n"
    [System.IO.File]::WriteAllText($path, $body, $taskUtf8)
}
function Get-TaskSha([string]$path) {
    return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$taskBuildOutput = @(& python (Join-Path $taskRoot 'build_reconstruction.py') $PID 2>&1)
$taskBuildExit = $LASTEXITCODE
$taskBuildOutput | ForEach-Object { Write-Output $_ }
if ($taskBuildExit -ne 0) { exit $taskBuildExit }
$taskReceiptPath = Join-Path $taskRoot 'terminal-receipts.json'
$taskReceipts = Get-Content -LiteralPath $taskReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$taskReceipts.receipts[1].real_exit_code = $taskBuildExit
$taskReceipts.receipts[1].exit_record_status = 'actual subprocess exit observed by foreground shell after completion'
$taskReceipts.receipts[1] | Add-Member -NotePropertyName stdout -NotePropertyValue ($taskBuildOutput -join "`n")
$taskReceipts.receipts += [pscustomobject]@{
    phase = 'artifact-authoring-tool'
    tool = 'apply_patch'
    result = 'two successful apply_patch calls; created only owned reconstruction and three scripts'
    pid = $null
    exit_code = $null
    exit_semantics = 'in-process tool reports successful completion; no operating-system process exit exposed'
}
Save-TaskJson $taskReceiptPath $taskReceipts

$taskFinalOutput = @(& python (Join-Path $taskRoot 'finalize_reconstruction.py') $PID 2>&1)
$taskFinalExit = $LASTEXITCODE
$taskFinalOutput | ForEach-Object { Write-Output $_ }
if ($taskFinalExit -ne 0) { exit $taskFinalExit }
$taskFinalPid = (($taskFinalOutput -join '') | ConvertFrom-Json).foreground_python_pid
$taskReceipts.receipts += [pscustomobject]@{
    phase = 'finalization'
    foreground_python_pid = $taskFinalPid
    parent_foreground_shell_pid = $PID
    real_exit_code = $taskFinalExit
    exit_record_status = 'actual subprocess exit observed by foreground shell after completion'
    stdout = ($taskFinalOutput -join "`n")
}
$taskReceipts.receipts += [pscustomobject]@{
    phase = 'closure-shell'
    foreground_shell_pid = $PID
    real_exit_code = $null
    exit_record_status = 'foreground shell real exit is observed externally by exec_command after CLOSED_LAST; it cannot be written into the already-closed owned tree'
}
Save-TaskJson $taskReceiptPath $taskReceipts

$taskExpected = @(
    'anonymous_reconstruction_69.json', 'build_reconstruction.py', 'finalize_reconstruction.py', 'run_owned.ps1',
    'inputs/packet0.raw.json', 'inputs/packet0.lf.json',
    'inputs/lean-statement.raw.txt', 'inputs/lean-statement.lf.txt',
    'inputs/approved-definition-context.raw.json', 'inputs/approved-definition-context.lf.json',
    'negative-checks.json', 'terminal-receipts.json', 'build-state.json',
    'review-run.json', 'decoded0.json', 'manifest.json', 'lease.json'
)
$taskFiles = @(Get-ChildItem -LiteralPath $taskRoot -Recurse -File)
$taskEntries = @()
foreach ($taskFile in $taskFiles) {
    $taskRelative = $taskFile.FullName.Substring($taskRoot.Length + 1).Replace('\', '/')
    if ($taskRelative -notin $taskExpected) { throw "Unexpected owned artifact: $taskRelative" }
    if ($taskRelative -in @('manifest.json', 'lease.json')) { continue }
    $taskEntries += [pscustomobject]@{ path = $taskRelative; raw_sha256 = (Get-TaskSha $taskFile.FullName); raw_bytes = $taskFile.Length }
}
if ($taskEntries.Count -ne 15) { throw "Expected 15 payload files before manifest and lease, found $($taskEntries.Count)" }
$taskManifest = [pscustomobject]@{
    schema_version = 1
    schema_name = 'finite-owned-reconstruction-manifest'
    owner = '/root/anonymous_decoder69'
    owned_root = $taskRoot.Replace('\', '/')
    owned_regular_file_count = 17
    hashed_payload_file_count = 15
    entries = @($taskEntries | Sort-Object path)
    all_owned_files = $taskExpected
    self_and_closure_policy = @(
        [pscustomobject]@{ path = 'manifest.json'; hash_policy = 'RAW hash reported by read-only postclose observer; no recursive self hash' },
        [pscustomobject]@{ path = 'lease.json'; hash_policy = 'written last as CLOSED_LAST; RAW hash reported by read-only postclose observer' }
    )
    lf_recipe = 'CRLF to LF ONLY; no isolated CR conversion and no trailing-whitespace normalization'
    terminal_policy = 'all owned scripts, input payloads, negative checks, run payloads, and terminal receipts are enumerated; subprocess actual EXIT values precede closure; shell and observer actual EXIT values remain external terminal evidence'
}
Save-TaskJson (Join-Path $taskRoot 'manifest.json') $taskManifest
$taskRun = Get-Content -LiteralPath (Join-Path $taskRoot 'review-run.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskLease = [pscustomobject]@{
    schema_version = 1
    owner = '/root/anonymous_decoder69'
    status = 'CLOSED_LAST'
    owned_root = $taskRoot.Replace('\', '/')
    owned_regular_file_count = 17
    closure_foreground_shell_pid = $PID
    generation_real_exit_code = $taskBuildExit
    finalization_real_exit_code = $taskFinalExit
    last_owned_write = 'lease.json'
    subsequent_owned_actions = 'read-only postclose validation and externally reported terminal EXIT only'
    manifest_raw_sha256 = Get-TaskSha (Join-Path $taskRoot 'manifest.json')
    whole_logical_sha256 = $taskRun.run_sha256
    boundary = 'independent source-blind reconstruction only; no source-facing acceptance'
}
# The following call is deliberately the last owned filesystem write.
Save-TaskJson (Join-Path $taskRoot 'lease.json') $taskLease
Write-Output ('CLOSED_LAST foreground_shell_pid=' + $PID)
exit 0
