# ================================
# Deploy Angular to GitHub Pages
# ================================

Write-Host "🚀 Starting Angular deploy to GitHub Pages..."

# 1. Go to the Angular project root
Set-Location "avanochi/web-app/front-end"

# 2. Clean previous dist if exists
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "🧹 Cleaned old dist folder"
}

# 3. Build Angular app with correct base-href
ng build --configuration production --base-href "https://avanochi-project.github.io/AVANOCHI/"

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Build failed. Aborting deploy."
    exit 1
}

Write-Host "✅ Build completed successfully"

# 4. Deploy only the browser build to gh-pages
npx ngh --dir="dist/front-end/browser" --branch=gh-pages

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 Deploy successful! Your app is live at:"
    Write-Host "👉 https://avanochi-project.github.io/AVANOCHI/"
} else {
    Write-Error "❌ Deploy failed"
}
