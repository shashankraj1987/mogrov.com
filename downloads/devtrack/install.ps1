# Install the latest stable DevTrack release for Windows amd64.
$ErrorActionPreference = 'Stop'
$repo = 'sraj0501/Devtrack_'
$installDir = if ($env:DEVTRACK_INSTALL_DIR) { $env:DEVTRACK_INSTALL_DIR } else { Join-Path $env:LOCALAPPDATA 'DevTrack' }

try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/latest" -ErrorAction Stop
    $version = $release.tag_name
    if (-not $version) { throw 'Release tag missing' }
    $url = "https://github.com/$repo/releases/download/$version/devtrack_windows_amd64.exe"
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
    $destination = Join-Path $installDir 'devtrack.exe'
    Invoke-WebRequest -Uri $url -OutFile $destination -UseBasicParsing -ErrorAction Stop
} catch {
    Write-Error "DevTrack installation failed: $_"
    return
}

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (($userPath -split ';') -notcontains $installDir) {
    [Environment]::SetEnvironmentVariable('Path', "$userPath;$installDir", 'User')
    Write-Host 'Added installation directory to your user PATH. Restart your terminal.'
}
Write-Host "Installed DevTrack $version to $destination"
Write-Host 'Run: devtrack setup'
