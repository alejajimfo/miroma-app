# ⚡ OPCIÓN MÁS RÁPIDA - APK en 10 Minutos

## 🎯 Método Súper Rápido (Sin Android Studio)

### Paso 1: Desplegar en Railway (5 min)

1. **Sube tu código a GitHub:**
```bash
cd /Users/alejandra/Desktop/MiRoma

# Si no tienes git inicializado
git init
git add .
git commit -m "Miroma app"

# Crea repo en GitHub: https://github.com/new
# Nombre: miroma-app

git remote add origin https://github.com/TU_USUARIO/miroma-app.git
git branch -M main
git push -u origin main
```

2. **Despliega en Railway:**
- Ve a: https://railway.app
- Regístrate con GitHub
- Click "New Project"
- "Deploy from GitHub repo"
- Selecciona "miroma-app"
- Espera 2-3 minutos
- Click "Generate Domain"
- **Copia tu URL** (ej: `miroma-app.up.railway.app`)

### Paso 2: Crear APK con AppsGeyser (5 min)

1. **Ve a:** https://appsgeyser.com

2. **Selecciona:** "Website"

3. **Ingresa tu URL:**
   - URL: `https://TU-URL-RAILWAY.up.railway.app/static/index.html`
   - Ejemplo: `https://miroma-app.up.railway.app/static/index.html`

4. **Personaliza:**
   - Nombre: Miroma
   - Descripción: App para parejas
   - Sube icono (usa `app/static/icon-512.png`)

5. **Descarga APK:**
   - Click "Create"
   - Espera 1-2 minutos
   - Descarga el APK

6. **Instala en tu celular:**
   - Transfiere el APK a tu celular
   - Abre el archivo
   - Permite "Fuentes desconocidas"
   - Instala

✅ **¡Listo en 10 minutos!**

---

## 🔄 Alternativa: Usando ngrok (Temporal)

Si solo quieres probar rápido sin desplegar:

```bash
# Instalar ngrok
brew install ngrok

# Ejecutar servidor
python run.py

# En otra terminal
ngrok http 3000

# Copia la URL HTTPS que aparece
# Ejemplo: https://abc123.ngrok.io

# Usa esa URL en AppsGeyser
# URL: https://abc123.ngrok.io/static/index.html
```

⚠️ **Nota:** La URL de ngrok cambia cada vez que lo reinicias.

---

## 📱 Instalar APK en Android

### Método 1: Desde el celular
1. Descarga el APK en tu celular
2. Abre "Archivos" o "Descargas"
3. Toca el archivo APK
4. Si aparece advertencia:
   - Ve a Configuración → Seguridad
   - Habilita "Fuentes desconocidas" o "Instalar apps desconocidas"
5. Vuelve y toca el APK
6. Instala

### Método 2: Desde la computadora
1. Conecta celular por USB
2. Copia el APK a la carpeta de Descargas
3. En el celular, abre Archivos
4. Busca el APK e instala

---

## 🎨 Mejorar el APK (Opcional)

### Agregar Icono Personalizado

Crea un icono 512x512 con:
- Fondo: Gradiente rosa-morado
- Emoji: 💜 o 💑
- Texto: "Miroma"

Usa: https://www.canva.com (gratis)

### Agregar Splash Screen

En AppsGeyser, en la sección de personalización:
- Sube una imagen de splash (1080x1920)
- Usa el mismo diseño del icono

---

## ⚠️ Limitaciones de AppsGeyser

- ✅ Gratis
- ✅ Rápido
- ✅ Fácil
- ❌ Tiene anuncios (versión gratis)
- ❌ Marca de agua "Created with AppsGeyser"
- ❌ Menos control sobre la app

**Para quitar limitaciones:**
- Paga $9.99/mes en AppsGeyser, O
- Usa Capacitor (ver `CREAR_APK.md`)

---

## 🚀 Siguiente Nivel

Una vez que tengas el APK funcionando, puedes:

1. **Crear APK profesional con Capacitor**
   - Ver: `CREAR_APK.md`
   - Sin anuncios ni marca de agua
   - Control total

2. **Publicar en Play Store**
   - Cuenta de desarrollador: $25 USD
   - Proceso de revisión: 1-3 días
   - Disponible para todos

3. **Crear versión iOS**
   - Necesitas Mac (ya lo tienes ✅)
   - Cuenta de desarrollador Apple: $99 USD/año
   - Publicar en App Store

---

## 📊 Resumen

| Paso | Tiempo | Herramienta |
|------|--------|-------------|
| 1. Subir a GitHub | 2 min | GitHub |
| 2. Desplegar | 3 min | Railway |
| 3. Crear APK | 5 min | AppsGeyser |
| **TOTAL** | **10 min** | ⚡ |

---

## ✅ Checklist Rápido

- [ ] Código en GitHub
- [ ] Desplegado en Railway
- [ ] URL funcionando en navegador
- [ ] APK creado con AppsGeyser
- [ ] APK descargado
- [ ] APK instalado en celular
- [ ] App funcionando

---

**¡Eso es todo! En 10 minutos tienes tu APK funcionando! 🎉**

¿Necesitas ayuda con algún paso? Avísame 😊
