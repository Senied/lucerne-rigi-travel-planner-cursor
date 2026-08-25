$ErrorActionPreference = "Stop"

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

function Get-VisibleText {
    param([string]$Html)
    $text = [regex]::Replace($Html, '(?is)<script\b.*?</script>|<style\b.*?</style>', ' ')
    $text = [regex]::Replace($text, '<[^>]+>', ' ')
    return [Net.WebUtility]::HtmlDecode($text)
}

function Assert-UniqueIdsAndFragments {
    param([string]$Html, [string]$Label)
    $ids = @([regex]::Matches($Html, '\sid="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Assert-True ($ids.Count -eq ($ids | Sort-Object -Unique).Count) "Duplicate IDs in $Label"
    foreach ($fragment in @([regex]::Matches($Html, 'href="#([^"]+)"') | ForEach-Object { $_.Groups[1].Value })) {
        Assert-True ($fragment -in $ids) "Broken fragment in ${Label}: #$fragment"
    }
}

$siteRoot = Split-Path -Parent $PSScriptRoot
Push-Location $siteRoot
try {
    node --check app.js
    Assert-True ($LASTEXITCODE -eq 0) "app.js syntax check failed"
    python -m py_compile scripts/build-traveler-guide.py
    Assert-True ($LASTEXITCODE -eq 0) "Guide builder syntax check failed"

    $rootHtml = Get-Content -Raw index.html
    $guideHtml = Get-Content -Raw guide/index.html
    Assert-UniqueIdsAndFragments $rootHtml 'index.html'
    Assert-UniqueIdsAndFragments $guideHtml 'guide/index.html'

    $rootReferences = @([regex]::Matches($rootHtml, '(?<![-\w])(?:href|src)="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    foreach ($match in [regex]::Matches($rootHtml, 'srcset="([^"]+)"')) {
        foreach ($candidate in $match.Groups[1].Value -split ',') { $rootReferences += (($candidate.Trim() -split '\s+')[0]) }
    }
    foreach ($reference in ($rootReferences | Sort-Object -Unique)) {
        if ($reference -match '^(?:https?:|#|data:|mailto:|tel:)') { continue }
        $localPath = (($reference -split '#')[0] -split '\?')[0]
        Assert-True (Test-Path -LiteralPath $localPath) "Broken root reference: $reference"
    }

    $guideReferences = @([regex]::Matches($guideHtml, '(?<![-\w])(?:href|src)="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    foreach ($reference in ($guideReferences | Sort-Object -Unique)) {
        if ($reference -match '^(?:https?:|#|data:|mailto:|tel:)') { continue }
        $localPath = (($reference -split '#')[0] -split '\?')[0]
        Assert-True (Test-Path -LiteralPath (Join-Path guide $localPath)) "Broken guide reference: $reference"
    }

    $sourceHtml = Get-Content -Raw releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.html
    $sourceUrls = @([regex]::Matches($sourceHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $guideUrls = @([regex]::Matches($guideHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    Assert-True ($guideUrls.Count -eq 206) "Unexpected external-link count in current guide"
    Assert-True (-not (Compare-Object $sourceUrls $guideUrls)) "Current guide external destinations differ from the expanded source"

    Assert-True (([regex]::Matches($guideHtml, 'class="section module-section"')).Count -eq 7) "Expected seven complete day plans"
    Assert-True (([regex]::Matches($guideHtml, 'class="excursion-card ')).Count -eq 41) "Expected forty-one additional excursions"
    Assert-True ((Get-ChildItem guide/assets/photos -Filter *.webp -File).Count -eq 60) "Responsive guide photographs are incomplete"
    Assert-True ((Get-ChildItem guide/assets/photos -Filter *-print.jpg -File).Count -eq 30) "Printable guide photographs are incomplete"
    Assert-True (Test-Path guide/Lucerne_Central_Switzerland_Travel_Guide_2026.pdf) "Current printable guide is missing"
    Assert-True (Test-Path releases/Lucerne_Central_Switzerland_Travel_Guide_2026_v1_2.html) "Current archived HTML is missing"
    Assert-True (Test-Path releases/Lucerne_Central_Switzerland_Travel_Guide_2026_v1_2.pdf) "Current archived PDF is missing"

    $banned = @('v1.0','v1.1','v1.2',' QA ','release gate','controlling source','discovery lineage','photo ID','photo atlas','rights record','checksum','manifest','provenance','dossier')
    foreach ($pair in @(@('root page',(Get-VisibleText $rootHtml)),@('current guide',(Get-VisibleText $guideHtml)))) {
        foreach ($term in $banned) { Assert-True ($pair[1] -notmatch [regex]::Escape($term)) "Internal term is visible in $($pair[0]): $term" }
    }

    Assert-True (([regex]::Matches($rootHtml, 'role="tab"')).Count -eq 14) "Expected fourteen root tabs"
    Assert-True (([regex]::Matches($rootHtml, 'role="tabpanel"')).Count -eq 2) "Expected two root tab panels"
    Assert-True ($rootHtml.Contains('aria-controls="nav-drawer"')) "Root menu is missing aria-controls"
    Assert-True (Test-Path -LiteralPath .nojekyll) ".nojekyll is missing"

    Write-Output "Static verification passed"
    Write-Output "- complete day plans: 7"
    Write-Output "- additional excursions: 41"
    Write-Output "- external destinations: 206"
    Write-Output "- responsive photo files: 60"
    Write-Output "- printable photo files: 30"
    Write-Output "- broken local references: 0"
}
finally {
    Pop-Location
}
