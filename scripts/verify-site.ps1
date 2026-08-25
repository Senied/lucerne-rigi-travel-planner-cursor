$ErrorActionPreference = "Stop"

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

$siteRoot = Split-Path -Parent $PSScriptRoot
Push-Location $siteRoot
try {
    node --check app.js
    Assert-True ($LASTEXITCODE -eq 0) "app.js syntax check failed"
    node --check guide/guide-enhancements.js
    Assert-True ($LASTEXITCODE -eq 0) "guide enhancement syntax check failed"

    $rootHtml = Get-Content -Raw index.html
    $rootIds = @([regex]::Matches($rootHtml, '\sid="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Assert-True ($rootIds.Count -eq ($rootIds | Sort-Object -Unique).Count) "Duplicate IDs in index.html"
    $rootFragments = @([regex]::Matches($rootHtml, 'href="#([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    foreach ($fragment in $rootFragments) {
        Assert-True ($fragment -in $rootIds) "Broken root fragment: #$fragment"
    }

    $rootReferences = @([regex]::Matches($rootHtml, '(?<![-\w])(?:href|src)="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    foreach ($match in [regex]::Matches($rootHtml, 'srcset="([^"]+)"')) {
        foreach ($candidate in $match.Groups[1].Value -split ',') {
            $rootReferences += (($candidate.Trim() -split '\s+')[0])
        }
    }
    foreach ($reference in ($rootReferences | Sort-Object -Unique)) {
        if ($reference -match '^(?:https?:|#|data:|mailto:|tel:|javascript:)') { continue }
        $localPath = (($reference -split '#')[0] -split '\?')[0]
        Assert-True (Test-Path -LiteralPath $localPath) "Broken root reference: $reference"
    }

    $guideHtml = Get-Content -Raw guide/index.html
    $guideReferences = @([regex]::Matches($guideHtml, '(?<![-\w])(?:href|src)="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    foreach ($reference in ($guideReferences | Sort-Object -Unique)) {
        if ($reference -match '^(?:https?:|#|data:|mailto:|tel:|javascript:)') { continue }
        $localPath = (($reference -split '#')[0] -split '\?')[0]
        Assert-True (Test-Path -LiteralPath (Join-Path guide $localPath)) "Broken guide reference: $reference"
    }

    $archiveHtml = Get-Content -Raw releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0.html
    $archiveUrls = @([regex]::Matches($archiveHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $currentUrls = @([regex]::Matches($guideHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    Assert-True ($archiveUrls.Count -eq 101) "Unexpected external-link count in preserved guide"
    Assert-True ($currentUrls.Count -eq $archiveUrls.Count) "Current guide external-link count changed"
    Assert-True (-not (Compare-Object $archiveUrls $currentUrls)) "Current guide external href set changed"

    $releaseHashes = @{
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_bundle.zip' = '13C7AD20D412A4AC4DF680E56944660FAB3C0CB4373C2A9C8E35961FD4E53073'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_photo_manifest.json' = '3B1195DA986572D247488463683E7F22D49DD8FB072640A8F1A68D30BC327657'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_QA_EVIDENCE.json' = '9415397F7886152BFA834D081395E028E1BE5738341F3F00588FF284DA895C27'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_QA_REPORT.md' = '558D1778989987314E60CD69395D63F6BFF72E08F8B0599EF27554B34CD8DF72'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_RELEASE_MANIFEST.json' = '3B88FB08A12CC2CDEB96933FB1831CC41CCA0439E20D22B5A581C20AA3F4B3C5'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0_SHA256SUMS.txt' = '55CBDE5796EA4A4023A0A718FBE494AE46576C12AD656AC81D6CC23EEA91A945'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0.html' = 'BED30602F55B364BEEDF05A200678F11609F8092C829EF7E084FC11939E11C35'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0.pdf' = '71BCB949B70F9FDDCE36C7384282BF00800C58E417C7E022F5361001C9F14491'
    }
    foreach ($name in $releaseHashes.Keys) {
        $path = Join-Path releases $name
        Assert-True (Test-Path -LiteralPath $path) "Missing archived file: $name"
        $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
        Assert-True ($actual -eq $releaseHashes[$name]) "Archived file changed: $name"
    }

    $visibleRoot = [regex]::Replace($rootHtml, '(?is)<script\b.*?</script>|<style\b.*?</style>', ' ')
    $visibleRoot = [regex]::Replace($visibleRoot, '<[^>]+>', ' ')
    $visibleRoot = [Net.WebUtility]::HtmlDecode($visibleRoot)
    foreach ($term in @('v1.0', '57-page', '57 pages', 'QA', 'PASS', 'release gate', 'checksum', 'provenance', 'photo ID', 'stable photo', 'controlling hash', 'dossier')) {
        Assert-True ($visibleRoot -notmatch [regex]::Escape($term)) "Internal term is visible on the root page: $term"
    }

    Assert-True ((Get-ChildItem assets/images/responsive -Filter *.webp -File).Count -eq 18) "Responsive image set is incomplete"
    Assert-True (([regex]::Matches($rootHtml, 'role="tab"')).Count -eq 14) "Expected fourteen root tabs"
    Assert-True (([regex]::Matches($rootHtml, 'role="tabpanel"')).Count -eq 2) "Expected two root tab panels"
    Assert-True ($rootHtml.Contains('aria-controls="nav-drawer"')) "Root menu is missing aria-controls"
    Assert-True ($guideHtml.Contains('guide-enhancements.js')) "Current guide enhancement is not loaded"

    Write-Output "Static verification passed"
    Write-Output "- archived files unchanged: 8"
    Write-Output "- preserved external guide links: 101"
    Write-Output "- responsive images: 18"
    Write-Output "- root tabs: 14; tab panels: 2"
    Write-Output "- broken local references: 0"
}
finally {
    Pop-Location
}
