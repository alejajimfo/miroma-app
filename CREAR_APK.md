# 📦 Crear APK de Miroma - Guía Completa

## 🎯 Estrategia: Desplegar + APK

Como no estarán en la misma red, necesitas:
1. **Desplegar la app en internet** (gratis)
2. **Crear APK** que apunte a esa URL

---

## Paso 1: Desplegar en Railway (5 minutos, GRATIS)

### 1.1 Crear cuenta en Railway
1. Ve a: https://railway.app
2. Regístrate con GitHub
3. Es gratis (500 horas/mes)

### 1.2 Subir código a GitHub
```bash
cd /Users/alejandra/Desktop/MiRoma

# Inicializar git (si no lo has hecho)
git init
git add .
git commit -m "Initial commit - Miroma app"

# Crear repositorio en GitHub
# Ve a: https://github.com/new
# Nombre: miroma-app

# Conectar y subir
git remote add origin https://github.com/TU_USUARIO/miroma-app.git
git branch -M main
git push -u origin main
```

### 1.3 Desplegar en Railway
1. En Railway, click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Elige tu repositorio "miroma-app"
4. Railway detecta automáticamente que es Flask
5. Click en "Deploy"
6. Espera 2-3 minutos

### 1.4 Obtener URL
1. En Railway, ve a tu proyecto
2. Click en "Settings"
3. Click en "Generate Domain"
4. Copia la URL (ej: `miroma-app.up.railway.app`)

✅ **¡Listo!** Tu app ya está en internet 24/7

---

## Paso 2: Crear APK con Capacitor

### 2.1 Instalar Node.js
Si no lo tienes:
```bash
brew install node
```

### 2.2 Instalar Capacitor
```bash
cd /Users/alejandra/Desktop/MiRoma

npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
```

### 2.3 Inicializar Capacitor
```bash
npx cap init
```

Responde:
- **App name:** Miroma
- **App ID:** com.miroma.app
- **Web asset directory:** app/static

### 2.4 Configurar URL de producción

Edita `capacitor.config.json`:
```json
{
  "appId": "com.miroma.app",
  "appName": "Miroma",
  "webDir": "app/static",
  "server": {
    "url": "https://TU-URL-DE-RAILWAY.up.railway.app",
    "cleartext": true
  }
}
```

Reemplaza `TU-URL-DE-RAILWAY` con tu URL real.

### 2.5 Agregar plataforma Android
```bash
npx cap add android
```

### 2.6 Instalar Android Studio
1. Descarga: https://developer.android.com/studio
2. Instala Android Studio
3. Abre Android Studio
4. Instala SDK de Android (sigue el wizard)

### 2.7 Abrir proyecto en Android Studio
```bash
npx cap open android
```

### 2.8 Compilar APK

En Android Studio:
1. Espera a que termine de sincronizar (barra de progreso abajo)
2. Ve a: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
3. Espera 2-5 minutos
4. Click en "locate" cuando termine

El APK estará en:
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### 2.9 Instalar en tu celular

**Opción A: USB**
1. Conecta tu celular por USB
2. Habilita "Depuración USB" en opciones de desarrollador
3. En Android Studio: Run → Run 'app'

**Opción B: Archivo APK**
1. Copia `app-debug.apk` a tu celular
2. Abre el archivo en tu celular
3. Permite "Instalar desde fuentes desconocidas"
4. Instala

✅ **¡Listo!** Ya tienes Miroma instalada

---

## Alternativa Más Rápida: APK Builder Online

Si no quieres instalar Android Studio:

### Opción 1: AppsGeyser (Gratis, Fácil)
1. Ve a: https://appsgeyser.com
2. Selecciona "Website"
3. Ingresa tu URL de Railway
4. Personaliza nombre e icono
5. Descarga APK

### Opción 2: Appy Pie (Gratis con marca de agua)
1. Ve a: https://www.appypie.com
2. Crea app desde URL
3. Descarga APK

---

## 🎨 Personalizar Icono y Splash Screen

### Crear Iconos para Android

Necesitas iconos en diferentes tamaños. Usa:
https://icon.kitchen

O crea manualmente:
- `android/app/src/main/res/mipmap-mdpi/ic_launcher.png` (48x48)
- `android/app/src/main/res/mipmap-hdpi/ic_launcher.png` (72x72)
- `android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` (96x96)
- `android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` (144x144)
- `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` (192x192)

### Crear Splash Screen

Edita `android/app/src/main/res/values/styles.xml`:
```xml
<style name="AppTheme.NoActionBarLaunch" parent="AppTheme.NoActionBar">
    <item name="android:background">@drawable/splash</item>
</style>
```

Crea `android/app/src/main/res/drawable/splash.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/splash_background"/>
    <item>
        <bitmap
            android:gravity="center"
            android:src="@mipmap/ic_launcher"/>
    </item>
</layer-list>
```

---

## 📱 Firmar APK para Producción

Para publicar en Play Store o distribuir oficialmente:

### 1. Generar Keystore
```bash
keytool -genkey -v -keystore miroma-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias miroma
```

### 2. Configurar en Android Studio
Edita `android/app/build.gradle`:
```gradle
android {
    ...
    signingConfigs {
        release {
            storeFile file('../../miroma-release-key.jks')
            storePassword 'TU_PASSWORD'
            keyAlias 'miroma'
            keyPassword 'TU_PASSWORD'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            ...
        }
    }
}
```

### 3. Compilar Release
```bash
cd android
./gradlew assembleRelease
```

APK firmado en:
```
android/app/build/outputs/apk/release/app-release.apk
```

---

## 🚀 Publicar en Google Play Store

### Requisitos
- Cuenta de desarrollador ($25 USD una sola vez)
- APK firmado
- Iconos y screenshots
- Descripción de la app

### Pasos
1. Ve a: https://play.google.com/console
2. Crea cuenta de desarrollador
3. Crea nueva aplicación
4. Sube APK firmado
5. Completa información
6. Envía para revisión (1-3 días)

---

## 🔧 Solución de Problemas

### "Gradle sync failed"
```bash
cd android
./gradlew clean
./gradlew build
```

### "SDK not found"
En Android Studio:
- Tools → SDK Manager
- Instala Android SDK 33 o superior

### "APK no instala"
- Habilita "Fuentes desconocidas" en Configuración
- Verifica que sea para tu arquitectura (ARM/x86)

### "App no conecta al servidor"
- Verifica que la URL en `capacitor.config.json` sea correcta
- Asegúrate que Railway esté corriendo
- Prueba la URL en el navegador del celular primero

---

## 📊 Comparación de Opciones

| Método | Tiempo | Dificultad | Personalización | Costo |
|--------|--------|------------|-----------------|-------|
| Railway + Capacitor | 30 min | ⭐⭐⭐ | ✅ Total | Gratis |
| AppsGeyser | 5 min | ⭐ | ❌ Limitada | Gratis |
| Appy Pie | 10 min | ⭐ | ⭐ Media | Gratis* |

*Con marca de agua

---

## ✅ Checklist

- [ ] Código subido a GitHub
- [ ] App desplegada en Railway
- [ ] URL de Railway funcionando
- [ ] Node.js instalado
- [ ] Capacitor instalado
- [ ] Android Studio instalado
- [ ] Proyecto Android creado
- [ ] APK compilado
- [ ] APK instalado en celular
- [ ] App funcionando correctamente

---

## 🎯 Resumen Rápido

**Lo más fácil:**
1. Desplegar en Railway (5 min)
2. Usar AppsGeyser para crear APK (5 min)
3. Instalar en celular

**Lo más profesional:**
1. Desplegar en Railway
2. Crear APK con Capacitor
3. Firmar APK
4. Publicar en Play Store

---

**¿Necesitas ayuda?** Avísame en qué paso estás y te ayudo 😊
