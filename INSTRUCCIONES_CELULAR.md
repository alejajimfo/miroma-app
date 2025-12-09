# 📱 Cómo Usar Miroma en tu Celular - Guía Rápida

## ✅ Todo Está Listo

Ya configuré Miroma como una **PWA (Progressive Web App)**. Esto significa que puedes instalarla en tu celular como si fuera una app de la Play Store, pero sin necesidad de crear un APK.

## 🚀 Pasos Rápidos (5 minutos)

### Paso 1: Encuentra tu IP Local

En tu computadora (Mac), abre Terminal y ejecuta:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Busca algo como: `inet 192.168.1.100` (ese es tu IP)

### Paso 2: Inicia el Servidor

```bash
cd /Users/alejandra/Desktop/MiRoma
python run.py
```

El servidor debe estar corriendo en el puerto 3000.

### Paso 3: Abre en tu Celular

1. **Conecta tu celular a la misma WiFi** que tu computadora
2. Abre **Chrome** en tu celular (Android) o **Safari** (iPhone)
3. Ve a: `http://TU_IP:3000/static/index.html`
   - Ejemplo: `http://192.168.1.100:3000/static/index.html`

### Paso 4: Instala como App

**En Android (Chrome):**
1. Toca el menú (⋮) arriba a la derecha
2. Selecciona "Agregar a pantalla de inicio" o "Instalar app"
3. Confirma
4. ¡Listo! Ahora tienes el ícono de Miroma 💜

**En iPhone (Safari):**
1. Toca el botón de compartir (□↑)
2. Selecciona "Agregar a pantalla de inicio"
3. Toca "Agregar"
4. ¡Listo! 💜

---

## 🌐 Alternativa: Usar ngrok (Acceso desde Cualquier Lugar)

Si quieres acceder desde cualquier lugar (no solo tu WiFi):

### 1. Instala ngrok
```bash
brew install ngrok
```

O descarga desde: https://ngrok.com/download

### 2. Ejecuta ngrok
```bash
ngrok http 3000
```

### 3. Copia la URL
Verás algo como:
```
Forwarding: https://abc123.ngrok.io -> http://localhost:3000
```

### 4. Abre en tu Celular
Ve a: `https://abc123.ngrok.io/static/index.html`

⚠️ **Nota:** La URL de ngrok cambia cada vez que lo reinicias (versión gratuita).

---

## ✨ Características de la PWA

✅ **Funciona offline** - Caché de archivos principales
✅ **Icono en pantalla de inicio** - Como una app nativa
✅ **Pantalla completa** - Sin barra de navegador
✅ **Actualizaciones automáticas** - Siempre la última versión
✅ **Notificaciones** (próximamente)

---

## 🎨 Iconos Creados

Ya creé los iconos automáticamente:
- ✅ `app/static/icon-192.png` (192x192)
- ✅ `app/static/icon-512.png` (512x512)

Tienen un diseño con gradiente rosa-morado y el emoji 💜

---

## 🔧 Solución de Problemas

### "No puedo conectarme desde mi celular"

**Verifica:**
1. ✅ Ambos dispositivos en la misma WiFi
2. ✅ El servidor está corriendo (`python run.py`)
3. ✅ Usas la IP correcta (no 127.0.0.1)
4. ✅ El puerto 3000 no está bloqueado

**Prueba:**
```bash
# En tu Mac, verifica que el servidor esté escuchando
lsof -i :3000
```

### "No aparece la opción de instalar"

**Soluciones:**
1. ✅ Usa Chrome en Android o Safari en iOS
2. ✅ Asegúrate de estar en HTTPS (usa ngrok)
3. ✅ Recarga la página (Ctrl+R o Cmd+R)
4. ✅ Limpia caché del navegador

### "Los iconos no se ven"

**Verifica:**
```bash
ls -la app/static/icon-*.png
```

Si no existen, ejecuta:
```bash
python crear_iconos.py
```

---

## 📊 Comparación: PWA vs APK

| Característica | PWA | APK |
|---------------|-----|-----|
| Instalación | ⚡ Instantánea | ⏱️ Lenta |
| Tamaño | 📦 ~2MB | 📦 ~20MB |
| Actualizaciones | 🔄 Automáticas | ❌ Manuales |
| Desarrollo | ✅ Ya está listo | ⏱️ 2-3 horas |
| Play Store | ❌ No necesario | ✅ Opcional |
| Funciona offline | ✅ Sí | ✅ Sí |

**Recomendación:** Usa PWA para uso personal. Es más rápido y fácil.

---

## 🎯 Próximos Pasos (Opcional)

Si quieres que la app esté disponible 24/7 sin tener tu computadora prendida:

### Opción 1: Railway (Gratis, Fácil)
1. Ve a: https://railway.app
2. Conecta tu GitHub
3. Despliega con un click
4. Obtienes una URL permanente

### Opción 2: PythonAnywhere (Gratis)
1. Ve a: https://www.pythonanywhere.com
2. Crea cuenta gratuita
3. Sube tu código
4. URL: `tuusuario.pythonanywhere.com`

---

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:
1. Verifica los logs del servidor
2. Abre la consola del navegador (F12 en Chrome)
3. Revisa que todos los archivos se carguen

---

## ✅ Checklist Final

- [ ] Servidor corriendo (`python run.py`)
- [ ] IP local identificada
- [ ] Celular en la misma WiFi
- [ ] App abierta en el navegador del celular
- [ ] PWA instalada en pantalla de inicio
- [ ] ¡Disfrutando de Miroma! 💜

---

**¡Listo! Ahora puedes usar Miroma desde tu celular como una app nativa! 🎉📱**
