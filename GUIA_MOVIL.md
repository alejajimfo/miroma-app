# 📱 Guía para Usar Miroma en el Celular

## 🎯 Opciones Disponibles

### Opción 1: PWA (Progressive Web App) ⭐ RECOMENDADA

La app ya está configurada como PWA. Puedes instalarla en tu celular como si fuera una app nativa.

#### ✅ Ventajas
- ✨ No necesitas crear APK
- 🚀 Instalación instantánea
- 📱 Funciona como app nativa
- 🔄 Actualizaciones automáticas
- 💾 Funciona offline (caché)
- 🎨 Icono en pantalla de inicio

#### 📲 Cómo Instalar (Android)

**Paso 1: Hacer la app accesible desde tu celular**

Opción A - Usando tu red local (WiFi):
1. En tu computadora, ejecuta:
   ```bash
   python run.py
   ```
2. Encuentra tu IP local:
   - Mac/Linux: `ifconfig | grep "inet "`
   - Windows: `ipconfig`
   - Busca algo como: `192.168.1.X`
3. En tu celular (conectado a la misma WiFi):
   - Abre Chrome
   - Ve a: `http://TU_IP:3000/static/index.html`
   - Ejemplo: `http://192.168.1.100:3000/static/index.html`

Opción B - Usando ngrok (acceso desde cualquier lugar):
1. Instala ngrok: https://ngrok.com/download
2. Ejecuta:
   ```bash
   ngrok http 3000
   ```
3. Copia la URL que te da (ej: `https://abc123.ngrok.io`)
4. En tu celular, abre esa URL + `/static/index.html`

**Paso 2: Instalar como PWA**
1. Abre la app en Chrome (Android)
2. Toca el menú (⋮) en la esquina superior derecha
3. Selecciona "Agregar a pantalla de inicio" o "Instalar app"
4. Confirma la instalación
5. ¡Listo! Ahora tienes el ícono de Miroma en tu pantalla de inicio

#### 🍎 Cómo Instalar (iPhone/iOS)

1. Abre la app en Safari (debe ser Safari, no Chrome)
2. Toca el botón de compartir (□↑)
3. Desplázate y selecciona "Agregar a pantalla de inicio"
4. Personaliza el nombre si quieres
5. Toca "Agregar"
6. ¡Listo! La app aparece en tu pantalla de inicio

---

### Opción 2: Crear APK con Capacitor 📦

Si prefieres un APK real para distribuir en Google Play o instalar directamente:

#### Requisitos
- Node.js instalado
- Android Studio instalado
- Java JDK instalado

#### Pasos

**1. Instalar Capacitor**
```bash
npm install -g @capacitor/cli @capacitor/core
npm install @capacitor/android
```

**2. Inicializar Capacitor**
```bash
cd /ruta/a/MiRoma
npx cap init
```
- App name: Miroma
- App ID: com.miroma.app
- Web dir: app/static

**3. Agregar plataforma Android**
```bash
npx cap add android
```

**4. Copiar archivos web**
```bash
npx cap copy android
```

**5. Abrir en Android Studio**
```bash
npx cap open android
```

**6. Compilar APK**
- En Android Studio: Build → Build Bundle(s) / APK(s) → Build APK(s)
- El APK estará en: `android/app/build/outputs/apk/debug/app-debug.apk`

**7. Instalar en tu celular**
- Conecta tu celular por USB
- Habilita "Depuración USB" en opciones de desarrollador
- Copia el APK a tu celular
- Instala el APK (permite instalación de fuentes desconocidas)

---

### Opción 3: Usar Directamente desde el Navegador 🌐

La forma más simple si no quieres instalar nada:

#### Usando tu Red Local (WiFi)
1. Tu computadora y celular deben estar en la misma WiFi
2. En tu computadora, ejecuta:
   ```bash
   python run.py
   ```
3. Encuentra tu IP local (ver arriba)
4. En tu celular, abre Chrome/Safari
5. Ve a: `http://TU_IP:3000/static/index.html`
6. Guarda como marcador para acceso rápido

#### Usando ngrok (Internet)
1. Instala ngrok: https://ngrok.com/download
2. Ejecuta:
   ```bash
   ngrok http 3000
   ```
3. Copia la URL pública (ej: `https://abc123.ngrok.io`)
4. Abre esa URL en tu celular + `/static/index.html`
5. ⚠️ La URL cambia cada vez que reinicias ngrok

---

## 🎨 Iconos para PWA

Para que la PWA se vea profesional, necesitas crear iconos:

### Crear Iconos Rápidamente

**Opción 1: Usar un generador online**
1. Ve a: https://www.pwabuilder.com/imageGenerator
2. Sube una imagen (logo de Miroma)
3. Descarga los iconos generados
4. Guárdalos en `app/static/` como:
   - `icon-192.png` (192x192)
   - `icon-512.png` (512x512)

**Opción 2: Crear manualmente**
Crea dos imágenes PNG:
- 192x192 píxeles → `app/static/icon-192.png`
- 512x512 píxeles → `app/static/icon-512.png`

Sugerencia de diseño:
- Fondo: Rosa/Morado degradado
- Emoji: 💑 o 💜
- Texto: "Miroma" (opcional)

---

## 🔧 Configuración del Servidor para Producción

Si quieres que la app esté disponible 24/7:

### Opción 1: Desplegar en Heroku (Gratis)
```bash
# Instalar Heroku CLI
# Crear Procfile
echo "web: python run.py" > Procfile

# Crear runtime.txt
echo "python-3.11.0" > runtime.txt

# Desplegar
heroku create miroma-app
git push heroku main
```

### Opción 2: Desplegar en Railway (Gratis)
1. Ve a: https://railway.app
2. Conecta tu repositorio GitHub
3. Railway detecta automáticamente Flask
4. Despliega con un click

### Opción 3: Desplegar en PythonAnywhere (Gratis)
1. Ve a: https://www.pythonanywhere.com
2. Crea cuenta gratuita
3. Sube tu código
4. Configura la web app
5. Tu app estará en: `tuusuario.pythonanywhere.com`

---

## 📊 Comparación de Opciones

| Opción | Dificultad | Tiempo | Offline | Icono | Actualizaciones |
|--------|-----------|--------|---------|-------|-----------------|
| PWA | ⭐ Fácil | 5 min | ✅ Sí | ✅ Sí | 🔄 Auto |
| APK | ⭐⭐⭐ Difícil | 2 horas | ✅ Sí | ✅ Sí | ❌ Manual |
| Navegador | ⭐ Muy fácil | 1 min | ❌ No | ❌ No | 🔄 Auto |

---

## 🎯 Recomendación Final

**Para uso personal/pareja:**
1. ✅ Usa **PWA** (Opción 1)
2. Despliega en **Railway** o **PythonAnywhere** para acceso 24/7
3. Instala en ambos celulares
4. ¡Disfruta! 🎉

**Para distribuir públicamente:**
1. Crea **APK con Capacitor** (Opción 2)
2. Publica en Google Play Store
3. Crea versión iOS con Capacitor también

---

## 🆘 Solución de Problemas

### "No puedo acceder desde mi celular"
- ✅ Verifica que estén en la misma WiFi
- ✅ Desactiva el firewall temporalmente
- ✅ Usa la IP correcta (no 127.0.0.1)

### "La app no se instala como PWA"
- ✅ Usa HTTPS (ngrok lo proporciona)
- ✅ Verifica que manifest.json esté accesible
- ✅ Usa Chrome en Android o Safari en iOS

### "Los iconos no aparecen"
- ✅ Crea los archivos icon-192.png y icon-512.png
- ✅ Colócalos en app/static/
- ✅ Limpia caché del navegador

---

## 📞 Contacto y Soporte

Si tienes problemas:
1. Revisa los logs del servidor
2. Abre la consola del navegador (F12)
3. Verifica que todos los archivos se carguen correctamente

---

**¡Disfruta de Miroma en tu celular! 💜📱**
