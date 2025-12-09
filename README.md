# 💑 Miroma - App para Parejas

Aplicación web moderna para parejas que organiza finanzas, pendientes, planes y metas futuras con privacidad total y sistema automático 70/30.

## ✨ Características

- **Sistema 70/30 automático:** Divide gastos según ingresos sin revelar cuánto gana cada uno
- **Gastos compartidos:** Con cálculo automático de aportes individuales
- **Gastos personales:** 100% privados
- **Metas de ahorro:** Con barra de progreso visual
- **Planes a futuro:** Con desglose automático (viajes, vehículos, hogar, eventos)
- **Pendientes:** Checklist organizado por categorías
- **Semáforo financiero:** Verde/Amarillo/Rojo según presupuesto
- **Diseño moderno:** Interfaz limpia con gradientes y animaciones suaves
- **Responsive:** Funciona en móvil, tablet y desktop

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd MiRoma

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear base de datos con datos de prueba
python test_app.py

# 5. Ejecutar aplicación
python run.py
```

Abrir navegador en: **http://localhost:8080**

## 👥 Usuarios de Prueba

```
Usuario 1 (Esposa):
Email: maria@ejemplo.com
Password: password123
Ingreso: $2,000,000 (privado)

Usuario 2 (Esposo):
Email: juan@ejemplo.com
Password: password123
Ingreso: $1,000,000 (privado)
```

## 💰 Sistema 70/30

El sistema calcula automáticamente cuánto debe aportar cada persona según sus ingresos, **manteniendo total privacidad**.

### Ejemplo:
- María gana $2,000,000/mes (privado)
- Juan gana $1,000,000/mes (privado)
- Gasto compartido: Mercado $300,000

**Sistema calcula:**
- María aporta: 66.67% = $200,000
- Juan aporta: 33.33% = $100,000

**Lo que ve cada uno:**
- María ve: "Tu parte: $200,000"
- Juan ve: "Tu parte: $100,000"

**Ninguno ve el ingreso del otro.**

## 📁 Estructura del Proyecto

```
MiRoma/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Endpoints API
│   ├── services/        # Lógica de negocio (70/30)
│   ├── utils/           # Validadores
│   └── static/          # Frontend (HTML/CSS/JS)
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── app.js
│       │   └── planes.js
│       └── index.html
├── docs/                # Documentación
├── instance/            # Base de datos
├── config.py            # Configuración
├── run.py              # Punto de entrada
└── requirements.txt    # Dependencias
```

## 🎨 Diseño

### Colores Principales
- **Rosa (Esposa):** `#f472b6` → `#ec4899`
- **Azul (Esposo):** `#60a5fa` → `#3b82f6`
- **Verde (Gastos):** `#4ade80` → `#22c55e`
- **Índigo (Planes):** `#818cf8` → `#6366f1`
- **Ámbar (Ahorros):** `#fbbf24` → `#f59e0b`
- **Púrpura (Pendientes):** `#c084fc` → `#a855f7`

### Características de Diseño
- Cards con bordes redondeados (24px)
- Gradientes suaves en fondos y botones
- Sombras sutiles para profundidad
- Animaciones de hover suaves
- Diseño responsive mobile-first

## 🛠️ Tecnologías

**Backend:**
- Python 3.8+
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-Login (Autenticación)
- Flask-JWT-Extended
- bcrypt (Encriptación)

**Frontend:**
- HTML5 / CSS3
- JavaScript ES6+
- Variables CSS
- Fetch API

**Base de Datos:**
- SQLite (desarrollo)
- PostgreSQL (producción)

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Autenticación JWT
- ✅ Ingresos privados
- ✅ Validación de permisos
- ✅ Protección SQL injection
- ✅ CORS configurado

## 📡 API REST

Base URL: `http://localhost:8080`

### Autenticación
```
POST /auth/registro          # Registrar usuario
POST /auth/login             # Iniciar sesión
POST /auth/generar-codigo    # Generar código de vinculación
POST /auth/vincular          # Vincular con pareja
GET  /auth/perfil            # Obtener perfil
```

### Gastos
```
GET  /gastos/compartidos     # Listar gastos compartidos
POST /gastos/compartidos     # Crear gasto compartido
GET  /gastos/personales      # Listar gastos personales
POST /gastos/personales      # Crear gasto personal
GET  /gastos/semaforo        # Estado del semáforo
```

### Ahorros
```
GET  /ahorros/               # Listar metas
POST /ahorros/               # Crear meta
POST /ahorros/{id}/aportar   # Agregar aporte
```

### Planes a Futuro
```
GET  /planes/                # Listar planes
POST /planes/                # Crear plan
GET  /planes/{id}            # Detalle de plan
POST /planes/{id}/items      # Agregar item
PUT  /planes/{id}/items/{item_id}  # Actualizar item
```

### Pendientes
```
GET  /pendientes/            # Listar pendientes
POST /pendientes/            # Crear pendiente
PUT  /pendientes/{id}/completar  # Marcar completado
```

## ⚙️ Configuración

Crear archivo `.env`:

```env
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=otra-clave-secreta
DATABASE_URL=sqlite:///instance/miroma.db
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
Cambiar puerto en `run.py`:
```python
app.run(host='0.0.0.0', port=8081, debug=True)
```

### Resetear base de datos
```bash
rm instance/miroma.db
python test_app.py
```

## 📚 Documentación

Ver `docs/README.md` para documentación completa:
- Arquitectura del sistema
- Sistema 70/30 detallado
- Planes a futuro
- Guía de desarrollo
- Roadmap

## 🗺️ Roadmap

### ✅ Fase 1: MVP (Completado)
- Sistema de autenticación
- Vinculación de parejas
- Gastos compartidos con 70/30
- Gastos personales
- Ahorros
- Pendientes
- Planes a futuro
- Diseño moderno

### 🚧 Fase 2: Mejoras
- [ ] Notificaciones en tiempo real
- [ ] Gráficos y estadísticas
- [ ] Exportar reportes PDF
- [ ] Modo oscuro
- [ ] PWA

### 📋 Fase 3: Avanzado
- [ ] Integración con bancos
- [ ] Presupuestos mensuales
- [ ] Chat entre pareja
- [ ] Calendario compartido

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License

## 👨‍💻 Autor

Desarrollado con ❤️ para parejas que quieren organizar su vida juntos.

---

**¿Preguntas?** Abre un issue en el repositorio.
