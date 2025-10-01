# Script para construir y preparar la aplicacion para GitHub Pages
# Ejecutar desde la raiz del proyecto AVANOCHI

Write-Host "Iniciando build para GitHub Pages..." -ForegroundColor Green

# Navegar al directorio del frontend
Set-Location "avanochi\web-app\avanochi-frontend"

# Verificar que existe package.json
if (-not (Test-Path "package.json")) {
    Write-Host "Error: No se encuentra package.json en el directorio actual" -ForegroundColor Red
    exit 1
}

# Instalar dependencias si no existen
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    npm install
}

# Construir la aplicacion para GitHub Pages
Write-Host "Construyendo aplicacion..." -ForegroundColor Yellow
npm run build:gh-pages

# Verificar que el build fue exitoso
if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completado exitosamente!" -ForegroundColor Green
    Write-Host "Los archivos estan en: dist/avanochi-frontend/" -ForegroundColor Cyan
    Write-Host "Despues del push a main, estara disponible en: https://avanochi-project.github.io/AVANOCHI/" -ForegroundColor Cyan
} else {
    Write-Host "Error en el build" -ForegroundColor Red
    exit 1
}

# Volver al directorio raiz
Set-Location "..\..\..\"

Write-Host "Proceso completado!" -ForegroundColor Green