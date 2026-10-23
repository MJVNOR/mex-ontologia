[CmdletBinding()]
param([switch]$Comprobar, [switch]$Validar)

$ErrorActionPreference = 'Stop'
$config = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'studio-gemini.json') -Raw | ConvertFrom-Json
$envPath = Join-Path (Split-Path $PSScriptRoot) '.env'
$settings = @{}
$allowed = @('ONTO_PROVIDER', 'ONTO_LLM_BASE_URL', 'ONTO_LLM_MODEL', 'ONTO_LLM_API_KEY')

try {
    if (-not (Test-Path -LiteralPath $config.executable -PathType Leaf)) {
        throw 'No se encuentra Studio. Revisa scripts/studio-gemini.json.'
    }
    if (-not (Test-Path -LiteralPath $config.node -PathType Leaf)) {
        throw 'No se encuentra Node. Revisa scripts/studio-gemini.json.'
    }
    if (-not (Test-Path -LiteralPath $envPath -PathType Leaf)) {
        throw 'Falta .env en la carpeta del proyecto. Usa .env.example como plantilla.'
    }
    # Parse values as data; never evaluate .env contents as PowerShell code.
    foreach ($line in [IO.File]::ReadLines($envPath)) {
        if ($line -match '^\s*(ONTO_[A-Z_]+)\s*=(.*)$' -and $Matches[1] -in $allowed) {
            $settings[$Matches[1]] = $Matches[2].Trim().Trim('"').Trim("'")
        }
    }
    foreach ($name in $allowed) {
        if ([string]::IsNullOrWhiteSpace($settings[$name])) { throw "Falta $name en .env." }
    }
    $baseUrl = 'https://generativelanguage.googleapis.com/v1beta/openai'
    if ($settings.ONTO_LLM_BASE_URL.TrimEnd('/') -ne $baseUrl) {
        throw 'Este acceso directo requiere el endpoint oficial de Gemini.'
    }
    if ($Comprobar) {
        [pscustomobject]@{
            Modelo = $settings.ONTO_LLM_MODEL
            Endpoint = $baseUrl
            ClaveConfigurada = $true
            Ejecutable = $config.executable
        }
        return
    }
    # Read-only API check; no graph data or chat messages are sent here.
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    try {
        $models = Invoke-RestMethod -Uri ($baseUrl + '/models') -Headers @{Authorization = 'Bearer ' + $settings.ONTO_LLM_API_KEY} -TimeoutSec 20
    } catch {
        $status = 'sin respuesta'
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
        throw "No se pudo validar Gemini (HTTP $status). Revisa la clave de .env y la conexion."
    }
    if (-not ($models.data | Where-Object { ($_.id -replace '^models/', '') -eq $settings.ONTO_LLM_MODEL })) {
        throw "El modelo $($settings.ONTO_LLM_MODEL) no aparece en tu API. Cambia ONTO_LLM_MODEL en .env."
    }
    if ($Validar) {
        Write-Host "Gemini conectado. Modelo disponible: $($settings.ONTO_LLM_MODEL)."
        return
    }
    if (Get-Process -Name 'open-ontologies-studio' -ErrorAction SilentlyContinue) {
        throw 'Guarda tu trabajo y cierra Studio antes de abrirlo con Gemini.'
    }
    $savedEnv = @{}
    $settings['ONTO_NODE_BINARY'] = $config.node
    try {
        foreach ($name in $settings.Keys) {
            $savedEnv[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
            [Environment]::SetEnvironmentVariable($name, $settings[$name], 'Process')
        }
        $logFolder = Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'MEX-Ontologi'
        New-Item -ItemType Directory -Path $logFolder -Force | Out-Null
        [IO.File]::WriteAllText((Join-Path (Split-Path $config.executable) 'agent-env-path.txt'), $envPath, [Text.UTF8Encoding]::new($false))
        Start-Process -FilePath $config.executable -WorkingDirectory (Split-Path $config.executable) -WindowStyle Normal -RedirectStandardError (Join-Path $logFolder 'studio-startup.log')
        Write-Host "Studio abierto con Gemini ($($settings.ONTO_LLM_MODEL))."
    } finally {
        foreach ($name in $savedEnv.Keys) {
            [Environment]::SetEnvironmentVariable($name, $savedEnv[$name], 'Process')
        }
    }
} catch {
    if ($Comprobar -or $Validar) { throw $_.Exception.Message }
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host 'Pulsa Enter para cerrar' | Out-Null
    exit 1
} finally {
    $settings.Clear()
}
