# GitHub Pages Setup for AVANOCHI

Este documento explica cómo está configurado GitHub Pages para el proyecto AVANOCHI.

## Configuración Actual

### 1. GitHub Actions Workflow
- **Archivo**: `.github/workflows/deploy-gh-pages.yml`
- **Trigger**: Se ejecuta automáticamente cuando se hace push a la rama `main`
- **Proceso**:
  1. Instala dependencias de Node.js
  2. Construye la aplicación Angular con `--base-href="/AVANOCHI/"`
  3. Despliega automáticamente a GitHub Pages

### 2. Scripts de Build
- `npm run build:gh-pages`: Script específico para construir la app para GitHub Pages
- Configura automáticamente el `base-href` correcto para el repositorio

### 3. Configuración de GitHub
Para que funcione correctamente, necesitas:

1. **Habilitar GitHub Pages en tu repositorio**:
   - Ve a Settings > Pages
   - En "Source", selecciona "GitHub Actions"

2. **Permisos del Workflow**:
   - Ve a Settings > Actions > General
   - En "Workflow permissions", selecciona "Read and write permissions"

## URL de la Página

Una vez configurado, tu página estará disponible en:
`https://avanochi-project.github.io/AVANOCHI/`

## Proceso de Despliegue

1. Haz cambios en tu código
2. Haz commit y push a la rama `main`
3. GitHub Actions automáticamente:
   - Construye la aplicación
   - Despliega a GitHub Pages
4. En unos minutos, los cambios estarán visibles en la URL

## Solución de Problemas

### Si no funciona el despliegue:
1. Verifica que GitHub Pages esté habilitado en Settings > Pages
2. Revisa que los permisos de Actions estén configurados correctamente
3. Revisa los logs del workflow en la pestaña "Actions" de GitHub

### Si las rutas no funcionan:
- Asegúrate de que el `base-href` esté configurado correctamente
- Verifica que el nombre del repositorio coincida con el usado en `base-href`

## Comandos Útiles

```bash
# Construir para GitHub Pages localmente
cd avanochi/web-app/avanochi-frontend
npm run build:gh-pages

# Servir localmente (después del build)
npx http-server dist/avanochi-frontend -p 8080
```

## Notas Importantes

- El archivo `.nojekyll` evita que GitHub Pages procese los archivos con Jekyll
- El workflow solo se ejecuta en pushes a `main`, no en otras ramas
- Los cambios pueden tardar unos minutos en aparecer después del despliegue