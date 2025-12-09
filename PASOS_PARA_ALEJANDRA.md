# 📱 Pasos para Alejandra - Crear APK de Miroma

## 🎯 Tu Situación
- ✅ Tienes la app funcionando en tu Mac
- ✅ Necesitas APK porque no estarán en la misma red
- ✅ Quieres la forma más rápida

## ⚡ OPCIÓN 1: Súper Rápida (10 min) - RECOMENDADA

### 1. Sube a GitHub (2 min)
```bash
cd /Users/alejandra/Desktop/MiRoma

git init
git add .
git commit -m "Miroma app lista"

# Ve a: https://github.com/new
# Crea repo llamado: miroma-app

git remote add origin https://github.com/TU_USUARIO/miroma-app.git
git branch -M main
git push -u origin main
```

### 2. Despliega en Render (3 min) - Railway está caído
1. Ve a: https://render.com
2. Regístrate con tu GitHub
3. Click "New +" → "Web Service"
4. Conecta tu repo "miroma-app"
5. Configuración:
   - Name: miroma-app
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
6. Click "Create Web Service"
7. Espera 3-5 minutos
8. **COPIA TU URL** (algo como: `miroma-app.onrender.com`)

### 3. Crea APK (5 min)
1. Ve a: https://appsgeyser.com
2. Click "Create App Now"
3. Selecciona "Website"
4. Pega tu URL + `/static/index.html`
   - Ejemplo: `https://miroma-app.up.railway.app/static/index.html`
5. Nombre: Miroma
6. Sube icono: `/Users/alejandra/Desktop/MiRoma/app/static/icon-512.png`
7. Click "Create"
8. Descarga el APK

### 4. Instala en tu Celular
1. Transfiere el APK a tu celular (email, WhatsApp, etc.)
2. Abre el archivo en tu celular
3. Permite "Instalar desde fuentes desconocidas"
4. Instala
5. ¡Listo! 🎉

---

## 🔧 OPCIÓN 2: Profesional (30 min)

Si quieres un APK sin anuncios ni marca de agua:

### 1. Instala herramientas
```bash
# Instalar Node.js
brew install node

# Instalar Capacitor
cd /Users/alejandra/Desktop/MiRoma
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
```

### 2. Configura Capacitor
```bash
npx cap init
```
- App name: Miroma
- App ID: com.miroma.app
- Web dir: app/static

### 3. Edita capacitor.config.json
Reemplaza con tu URL de Railway:
```json
{
  "appId": "com.miroma.app",
  "appName": "Miroma",
  "webDir": "app/static",
  "server": {
    "url": "https://TU-URL-RAILWAY.up.railway.app",
    "cleartext": true
  }
}
```

### 4. Instala Android Studio
1. Descarga: https://developer.android.com/studio
2. Instala (sigue el wizard)
3. Abre Android Studio
4. Instala Android SDK cuando te lo pida

### 5. Crea proyecto Android
```bash
npx cap add android
npx cap open android
```

### 6. Compila APK
En Android Studio:
1. Espera a que termine de sincronizar
2. Build → Build Bundle(s) / APK(s) → Build APK(s)
3. Espera 2-5 minutos
4. Click "locate" cuando termine

APK en: `android/app/build/outputs/apk/debug/app-debug.apk`

### 7. Instala
Copia el APK a tu celular e instala.

---

## 🆘 Si Algo Sale Mal

### "No puedo subir a GitHub"
```bash
# Verifica que tengas git
git --version

# Si no lo tienes
brew install git

# Configura git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### "Railway no despliega"
- Verifica que `requirements.txt` esté completo
- Verifica que `Procfile` exista
- Mira los logs en Railway para ver el error

### "APK no instala"
- Habilita "Fuentes desconocidas" en Configuración → Seguridad
- Verifica que el APK no esté corrupto (descárgalo de nuevo)

### "App no carga"
- Verifica que la URL de Railway funcione en el navegador
- Asegúrate de agregar `/static/index.html` al final
- Limpia caché del navegador

---

## 📊 ¿Cuál Opción Elegir?

### Elige OPCIÓN 1 si:
- ✅ Quieres algo rápido
- ✅ No te importan los anuncios
- ✅ Es solo para uso personal

### Elige OPCIÓN 2 si:
- ✅ Quieres algo profesional
- ✅ Sin anuncios ni marca de agua
- ✅ Planeas publicar en Play Store
- ✅ Tienes 30 minutos

---

## 🎯 Mi Recomendación

**Empieza con OPCIÓN 1:**
1. Es rápida (10 min)
2. Puedes probar que todo funcione
3. Si te gusta, luego haces OPCIÓN 2

**Luego, si quieres mejorar:**
1. Haz OPCIÓN 2 para APK profesional
2. Publica en Play Store
3. Comparte con más personas

---

## ✅ Archivos que Necesitas

Ya están listos en tu proyecto:
- ✅ `Procfile` - Para Railway
- ✅ `runtime.txt` - Versión de Python
- ✅ `railway.json` - Configuración Railway
- ✅ `requirements.txt` - Dependencias
- ✅ `app/static/manifest.json` - PWA config
- ✅ `app/static/icon-512.png` - Icono

---

## 📞 Siguiente Paso

**Ahora mismo, haz esto:**

1. Abre Terminal
2. Ejecuta:
```bash
cd /Users/alejandra/Desktop/MiRoma
git init
git add .
git commit -m "Miroma lista para desplegar"
```

3. Ve a: https://github.com/new
4. Crea repo "miroma-app"
5. Ejecuta:
```bash
git remote add origin https://github.com/TU_USUARIO/miroma-app.git
git branch -M main
git push -u origin main
```

6. Ve a: https://railway.app
7. Despliega tu repo

**¡Y listo! En 10 minutos tendrás tu APK! 🚀**

---

¿Necesitas ayuda con algún paso? ¡Avísame! 😊
