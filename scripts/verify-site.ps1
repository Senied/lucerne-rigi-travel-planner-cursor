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

    $currentReleaseHtmlPath = 'releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.html'
    $currentReleasePdfPath = 'releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.pdf'
    $currentReleaseZipPath = 'releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_bundle.zip'
    $currentReleaseHtml = Get-Content -Raw $currentReleaseHtmlPath
    $currentUrls = @([regex]::Matches($currentReleaseHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $guideUrls = @([regex]::Matches($guideHtml, 'href="(https?://[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    Assert-True ($currentUrls.Count -eq 206) "Unexpected external-link count in canonical v1.1 guide"
    Assert-True (-not (Compare-Object $currentUrls $guideUrls)) "Compatibility guide external href set differs from canonical v1.1"

    $photoIds = @([regex]::Matches($currentReleaseHtml, 'data-photo-id="(P\d{3})"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $captionPhotoIds = @([regex]::Matches($currentReleaseHtml, 'class="photo-id">(P\d{3})<') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $expectedPhotoIds = @(1..30 | ForEach-Object { 'P{0:d3}' -f $_ })
    Assert-True (-not (Compare-Object $expectedPhotoIds $photoIds)) "Canonical v1.1 photo element IDs are incomplete"
    Assert-True (-not (Compare-Object $expectedPhotoIds $captionPhotoIds)) "Canonical v1.1 photo caption IDs are incomplete"
    Assert-True (([regex]::Matches($currentReleaseHtml, 'id="module-l[1-7]"')).Count -eq 7) "Canonical v1.1 module set is incomplete"

    $releaseHashes = @{
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_bundle.zip' = '1DB5A454924308A853AD9ED92C157DF1226EE0802BA2F7CCF2A8028795A6DDEC'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_photo_manifest.json' = '78C801DB79F6E57F7C92A6899E7626644FAAF22EB4C023FA7AEDA1CD501E5DA2'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_QA_EVIDENCE.json' = '8405029A8D20222EDA3417B324FDEE35F732B4CC450CA88FF0872508F2ADB212'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_QA_REPORT.md' = '01932C5DFD21B7020A940625F25E01031A61B1CFB894BB1616E0682765120B3D'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_RELEASE_MANIFEST.json' = '372AF734515B8C64BC0C6E239B2694A9F5578F9976D94D6DC5D31C07CD19141C'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_SHA256SUMS.txt' = '932AE635CDEA8F0DFE9CECF174A4B06C727591BEA6DE3E815A364482D2D5537D'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.html' = '386237DAC7728432F8F9812B312D658742BB5F8D48D355EEB5817756781ECBF0'
        'Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.pdf' = '266BF8615237A352CE7DF1AC20ACA99773884D0A6205A1055B51933B72A580EE'
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

    $currentHtmlHash = (Get-FileHash -LiteralPath $currentReleaseHtmlPath -Algorithm SHA256).Hash
    $currentPdfHash = (Get-FileHash -LiteralPath $currentReleasePdfPath -Algorithm SHA256).Hash
    Assert-True ((Get-FileHash -LiteralPath guide/index.html -Algorithm SHA256).Hash -eq $currentHtmlHash) "guide/index.html is not the exact canonical v1.1 HTML"
    Assert-True ((Get-FileHash -LiteralPath guide/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.pdf -Algorithm SHA256).Hash -eq $currentPdfHash) "Canonical guide PDF mirror differs from v1.1"
    Assert-True ((Get-FileHash -LiteralPath guide/Lucerne_Central_Switzerland_Travel_Guide_2026.pdf -Algorithm SHA256).Hash -eq $currentPdfHash) "Legacy PDF route does not resolve to v1.1"

    foreach ($requiredRootReference in @($currentReleaseHtmlPath, $currentReleasePdfPath, $currentReleaseZipPath)) {
        Assert-True ($requiredRootReference -in $rootReferences) "Root page is missing direct current-release link: $requiredRootReference"
    }
    Assert-True (Test-Path -LiteralPath .nojekyll) ".nojekyll is missing"
    Assert-True (-not $guideHtml.Contains('guide-enhancements')) "Compatibility guide still contains an enhancement rewrite"
    Assert-True (-not (Test-Path -LiteralPath guide/guide-enhancements.css)) "Obsolete guide enhancement stylesheet remains"
    Assert-True (-not (Test-Path -LiteralPath guide/guide-enhancements.js)) "Obsolete guide enhancement script remains"

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
    Write-Output "Static verification passed"
    Write-Output "- canonical release files hash-verified: 16"
    Write-Output "- canonical v1.1 external links: 206"
    Write-Output "- visible canonical photo IDs: 30"
    Write-Output "- current modules: 7"
    Write-Output "- responsive images: 18"
    Write-Output "- root tabs: 14; tab panels: 2"
    Write-Output "- broken local references: 0"
}
finally {
    Pop-Location
}
