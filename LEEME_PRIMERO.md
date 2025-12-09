# 📱 USAR MIROMA EN EL CELULAR - 3 PASOS

## 🎯 Lo Más Fácil y Rápido

### 1️⃣ Encuentra tu IP
En tu Mac, abre Terminal y ejecuta:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```
Anota el número que aparece (ej: `192.168.1.100`)

### 2️⃣ Abre en tu Celular
- Conecta tu celular a la **misma WiFi**
- Abre **Chrome** (Android) o **Safari** (iPhone)
- Ve a: `http://TU_IP:3000/static/index.html`
- Ejemplo: `http://192.168.1.100:3000/static/index.html`

### 3️⃣ Instala como App
**Android:**
- Menú (⋮) → "Agregar a pantalla de inicio"

**iPhone:**
- Compartir (□↑) → "Agregar a pantalla de inicio"

---

## 🌐 Alternativa: Acceso desde Cualquier Lugar

Si no estás en la misma WiFi o quieres acceso permanente:

### Opción A: ngrok (Temporal)
```bash
# Instalar
brew install ngrok

# Ejecutar
ngrok http 3000

# Copiar la URL que aparece (ej: https://abc123.ngrok.io)
# Abrir en celular: https://abc123.ngrok.io/static/index.html
```

### Opción B: Railway (Permanente, Gratis)
1. Ve a: https://railway.app
2. Conecta tu GitHub
3. Despliega Miroma
4. Obtienes URL permanente

---

## ✅ ¡Eso es Todo!

Ahora tienes Miroma en tu celular como una app nativa 💜

**Archivos importantes:**
- `INSTRUCCIONES_CELULAR.md` - Guía detallada
- `GUIA_MOVIL.md` - Todas las opciones disponibles
- `crear_iconos.py` - Script para regenerar iconos

**¿Problemas?**
- Verifica que ambos estén en la misma WiFi
- Asegúrate que el servidor esté corriendo
- Usa la IP correcta (no 127.0.0.1)
