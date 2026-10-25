$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\marti\Documents\MEX-Ontologi'
$taskConfig = Get-Content -LiteralPath (Join-Path $taskRoot 'scripts/studio-gemini.json') -Raw | ConvertFrom-Json
$taskExe = [IO.Path]::GetFullPath($taskConfig.executable)
$taskAppDir = Split-Path $taskExe
$taskProcesses = @(Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $taskExe })
if ($taskProcesses.Count -ne 1) { throw 'Se esperaba una única instancia conocida de Studio.' }
$taskPid = $taskProcesses[0].ProcessId
$taskChildren = @(Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $taskPid -and $_.ExecutablePath -eq (Join-Path $taskAppDir 'open-ontologies.exe') })
$taskStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$taskBackup = Join-Path $taskRoot ('data/backups/studio-antes-activar-gemma-' + $taskStamp + '.ttl')
$taskBefore = Invoke-RestMethod -Uri 'http://127.0.0.1:8137/api/stats'
$taskBody = @{ path=$taskBackup; format='turtle' } | ConvertTo-Json
$taskSaved = Invoke-RestMethod -Uri 'http://127.0.0.1:8137/api/save' -Method Post -ContentType 'application/json' -Body $taskBody
if ($taskSaved.error -or -not (Test-Path -LiteralPath $taskBackup -PathType Leaf)) { throw 'No se pudo respaldar el grafo; no cerrar Studio.' }
if ((Get-Item -LiteralPath $taskBackup).Length -lt 1000000) { throw 'Respaldo inesperadamente pequeño; no cerrar Studio.' }
$taskHash = (Get-FileHash -LiteralPath $taskBackup -Algorithm SHA256).Hash.ToLowerInvariant()
Stop-Process -Id $taskPid
foreach ($taskChild in $taskChildren) {
    $taskStill = Get-CimInstance Win32_Process -Filter "ProcessId = $($taskChild.ProcessId)"
    if ($taskStill -and $taskStill.ExecutablePath -eq (Join-Path $taskAppDir 'open-ontologies.exe')) { Stop-Process -Id $taskChild.ProcessId }
}
$taskCanonical = Join-Path $taskRoot 'data/catalogo/studio-live.ttl'
Copy-Item -LiteralPath $taskBackup -Destination $taskCanonical -Force
if ((Get-FileHash -LiteralPath $taskCanonical -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskHash) { throw 'La copia canónica no coincide; conservar respaldo y no reiniciar.' }
& (Join-Path $taskRoot 'scripts/abrir_studio_gemini.ps1')
$taskReceipt = @{ antes_pid=$taskPid; antes_stats=$taskBefore; respaldo=$taskBackup; respaldo_sha256=$taskHash; copia_canonica_verificada=$true; iniciado_utc=[DateTime]::UtcNow.ToString('o'); modelo_solicitado='gemma-4-31b-it'; limite='Reinicio con configuración vigente; comprobar handshake y grafo después.' }
[IO.File]::WriteAllText((Join-Path $taskRoot 'propuestas/pendientes-muse-r6/reinicio-studio.json'), ($taskReceipt | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
Write-Output 'Reinicio solicitado con respaldo y copia canónica verificados.'
