# 📚 Documentación Miroma

## Índice

1. [Arquitectura](#arquitectura)
2. [Sistema 70/30](#sistema-7030)
3. [Planes a Futuro](#planes-a-futuro)
4. [Guía de Desarrollo](#guía-de-desarrollo)
5. [Roadmap](#roadmap)

---

## Arquitectura

### Stack Tecnológico

**Backend:**
- Python 3.x
- Flask (Framework web)
- SQLAlchemy (ORM)
- Flask-Login (Autenticación)
- SQLite (Base de datos)

**Frontend:**
- HTML5
- CSS3 (Variables CSS, Gradientes)
- JavaScript Vanilla (ES6+)
- Diseño responsive

### Estructura del Proyecto

```
MiRoma/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── models/              # Modelos de base de datos
│   │   ├── usuario.py
│   │   ├── pareja.py
│   │   ├── gasto.py
│   │   ├── ahorro.py
│   │   ├── pendiente.py
│   │   └── plan.py
│   ├── routes/              # Rutas/Endpoints
│   │   ├── auth.py
│   │   ├── gastos.py
│   │   ├── ahorros.py
│   │   ├── pendientes.py
│   │   └── planes.py
│   ├── services/            # Lógica de negocio
│   │   └── calculo_70_30.py
│   ├── utils/               # Utilidades
│   │   └── validators.py
│   └── static/              # Archivos estáticos
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── app.js
│       │   └── planes.js
│       └── index.html
├── docs/                    # Documentación
├── instance/                # Base de datos
│   └── miroma.db
├── config.py               # Configuración
├── run.py                  # Punto de entrada
└── requirements.txt        # Dependencias
```

### Modelos de Datos

**Usuario:**
- email, password_hash, apodo, rol (esposa/esposo)
- ingreso_mensual (privado)
- pareja_id (relación)

**Pareja:**
- usuario1_id, usuario2_id
- codigo_vinculacion (6 dígitos)
- fecha_vinculacion

**Gasto:**
- nombre, monto, categoria, fecha
- tipo (compartido/personal)
- pareja_id, usuario_id

**Ahorro:**
- nombre, meta_monto, monto_actual
- fecha_meta, pareja_id

**Pendiente:**
- titulo, descripcion, categoria
- completado, pareja_id

**PlanFuturo:**
- nombre, tipo (viaje/vehiculo/hogar/evento/personalizado)
- fecha_objetivo, pareja_id
- items (ItemPlan)

---

## Sistema 70/30

### Concepto

Sistema automático de distribución de gastos compartidos basado en los ingresos de cada persona.

### Fórmula

```python
ingreso_total = ingreso_usuario1 + ingreso_usuario2
porcentaje_usuario1 = ingreso_usuario1 / ingreso_total
porcentaje_usuario2 = ingreso_usuario2 / ingreso_total

aporte_usuario1 = monto_total * porcentaje_usuario1
aporte_usuario2 = monto_total * porcentaje_usuario2
```

### Ejemplo

**Ingresos:**
- Usuario 1: $2,000,000
- Usuario 2: $1,000,000
- Total: $3,000,000

**Gasto compartido:** $300,000

**Cálculo:**
- Usuario 1: 66.67% → $200,000
- Usuario 2: 33.33% → $100,000

### Semáforo de Gastos

- 🟢 **Verde:** Gastos < 50% del ingreso total
- 🟡 **Amarillo:** Gastos entre 50-70%
- 🔴 **Rojo:** Gastos > 70%

---

## Planes a Futuro

### Tipos de Planes

#### 1. 🏖️ Viaje
**Items predefinidos:**
- Vuelos
- Alojamiento
- Transporte local
- Comidas
- Actividades/Tours
- Extras

#### 2. 🚗 Vehículo
**Items predefinidos:**
- Valor del vehículo
- SOAT
- Tecnomecánica
- Seguro
- Gasolina primer mes
- Mantenimiento
- Imprevistos

#### 3. 🏠 Hogar
**Items predefinidos:**
- Muebles
- Electrodomésticos
- Decoración
- Remodelación
- Herramientas
- Imprevistos

#### 4. 🎉 Evento
**Items predefinidos:**
- Lugar/Venue
- Catering
- Decoración
- Música/Entretenimiento
- Invitaciones
- Fotografía/Video
- Extras

#### 5. 📝 Personalizado
Sin items predefinidos, el usuario crea los suyos.

### Vistas

**Vista Grid:**
- Cards con gradientes coloridos
- Iconos grandes
- Barra de progreso
- Monto total

**Vista Timeline:**
- Línea de tiempo vertical
- Marcadores circulares
- Muestra aportes de cada persona
- Estados visuales (completado/en progreso/pendiente)

### Estados de Items

- ✓ **Pagado** (verde)
- ⏳ **En progreso** (amarillo)
- ○ **Pendiente** (gris)

---

## Guía de Desarrollo

### Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd MiRoma

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Inicializar base de datos
python
>>> from app import db
>>> db.create_all()
>>> exit()

# Ejecutar aplicación
python run.py
```

### Desarrollo

**Ejecutar en modo desarrollo:**
```bash
export FLASK_ENV=development
python run.py
```

**Acceder a la aplicación:**
```
http://localhost:5000
```

### Agregar Nuevas Funcionalidades

#### 1. Crear Modelo
```python
# app/models/nuevo_modelo.py
from app import db

class NuevoModelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... campos
```

#### 2. Crear Ruta
```python
# app/routes/nueva_ruta.py
from flask import Blueprint, jsonify
from flask_login import login_required

bp = Blueprint('nueva_ruta', __name__, url_prefix='/api')

@bp.route('/endpoint', methods=['GET'])
@login_required
def endpoint():
    return jsonify({'mensaje': 'OK'})
```

#### 3. Registrar Blueprint
```python
# app/__init__.py
from app.routes import nueva_ruta
app.register_blueprint(nueva_ruta.bp)
```

### Diseño

**Colores principales:**
- Rosa (Esposa): `#f472b6` → `#ec4899`
- Azul (Esposo): `#60a5fa` → `#3b82f6`
- Verde (Gastos): `#4ade80` → `#22c55e`
- Índigo (Planes): `#818cf8` → `#6366f1`
- Ámbar (Ahorros): `#fbbf24` → `#f59e0b`
- Púrpura (Pendientes): `#c084fc` → `#a855f7`

**Componentes:**
- Cards: `border-radius: 1.5rem`, sombra suave
- Botones: Gradientes, hover con elevación
- Progress bars: Altura 0.5rem, gradientes
- Modales: Fondo con blur

---

## Roadmap

### ✅ Fase 1: MVP (Completado)
- [x] Sistema de autenticación
- [x] Vinculación de parejas
- [x] Gastos compartidos con 70/30
- [x] Gastos personales
- [x] Ahorros
- [x] Pendientes
- [x] Planes a futuro
- [x] Diseño moderno y responsive

### 🚧 Fase 2: Mejoras (En progreso)
- [ ] Notificaciones en tiempo real
- [ ] Gráficos y estadísticas
- [ ] Exportar reportes PDF
- [ ] Modo oscuro
- [ ] PWA (Progressive Web App)

### 📋 Fase 3: Funcionalidades Avanzadas
- [ ] Recordatorios automáticos
- [ ] Integración con bancos
- [ ] Presupuestos mensuales
- [ ] Metas de ahorro automáticas
- [ ] Chat entre pareja
- [ ] Calendario compartido

### 🎯 Fase 4: Escalabilidad
- [ ] API REST completa
- [ ] App móvil nativa (iOS/Android)
- [ ] Multi-idioma
- [ ] Múltiples parejas/familias
- [ ] Roles y permisos avanzados

---

## Preguntas Frecuentes

### ¿Cómo funciona el sistema 70/30?
El sistema calcula automáticamente cuánto debe aportar cada persona según sus ingresos. Si una persona gana el doble, aporta el doble.

### ¿Los ingresos son visibles para la pareja?
No, los ingresos son privados. Solo se muestra el aporte calculado para cada gasto.

### ¿Puedo cambiar el porcentaje de distribución?
Actualmente el sistema es automático basado en ingresos. En futuras versiones se podrá personalizar.

### ¿Cómo se vinculan las parejas?
Una persona genera un código de 6 dígitos y la otra lo ingresa para vincularse.

### ¿Puedo tener gastos personales?
Sí, hay una sección separada para gastos personales que solo tú ves.

### ¿Los planes a futuro calculan aportes individuales?
Sí, cada item del plan muestra cuánto debe aportar cada persona según el sistema 70/30.

---

## Soporte

Para reportar bugs o sugerir mejoras, crear un issue en el repositorio.

## Licencia

[Especificar licencia]
