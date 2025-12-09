# 🚀 Inicio Rápido - Miroma

## Acceso a la Aplicación

La aplicación está corriendo en: **http://localhost:3000**

## Usuarios de Prueba

- **Esposa**: maria@ejemplo.com / password123
- **Esposo**: juan@ejemplo.com / password123

## Funcionalidades Principales

### 1. 📊 Nuestros Gastos
Sistema automático 70/30 que calcula los aportes según el ingreso de cada uno.

### 2. 💰 Gastos Personales
Presupuesto privado de cada usuario.

### 3. 🐷 Ahorros
Metas de ahorro conjuntas con seguimiento de progreso.

### 4. ✓ Pendientes
Lista de tareas compartidas.

### 5. 🚀 Planes a Futuro
Proyectos y sueños con vista de timeline mostrando aportes individuales.

### 6. ⚙️ Configuración (NUEVO)

#### Información de Perfil
- Cambiar apodo
- Ver email (no editable)
- Ver rol (no editable)

#### Información Financiera 🔒
- Actualizar ingreso mensual (privado)
- Solo tú puedes ver tu ingreso
- Se usa para calcular aportes en gastos compartidos

#### Información de Pareja
- Ver estado de vinculación
- Fecha de vinculación
- Información sobre privacidad

#### Cambiar Contraseña
- Requiere contraseña actual
- Nueva contraseña debe tener mínimo 6 caracteres
- Confirmación de nueva contraseña

#### Zona de Peligro
- **Desvincular pareja**: Los datos compartidos se mantienen pero ya no pueden ver la información del otro
- **Eliminar cuenta**: Acción permanente que elimina todos los datos del usuario

## Endpoints de Configuración

### Backend (app/routes/auth.py)

```python
PUT /auth/actualizar-perfil
- Body: { "apodo": "Nuevo Apodo" }
- Actualiza el apodo del usuario

PUT /auth/actualizar-ingreso
- Body: { "ingreso_mensual": 2000000 }
- Actualiza el ingreso mensual (privado)

PUT /auth/cambiar-password
- Body: { "password_actual": "...", "password_nueva": "..." }
- Cambia la contraseña del usuario

POST /auth/desvincular
- Desvincula al usuario de su pareja
- Desactiva la pareja pero mantiene los datos

DELETE /auth/eliminar-cuenta
- Elimina permanentemente la cuenta del usuario
- Elimina gastos personales asociados
- Desvincula de la pareja si está vinculado
```

### Frontend (app/static/js/app.js)

```javascript
cargarConfiguracion()
- Carga los datos del usuario en el formulario
- Llama a cargarInfoPareja()

actualizarPerfil()
- Actualiza el apodo del usuario

actualizarIngreso()
- Actualiza el ingreso mensual

cambiarPassword()
- Cambia la contraseña con validaciones

confirmarDesvinculacion() / desvincularPareja()
- Desvincula de la pareja con confirmación

confirmarEliminarCuenta() / eliminarCuenta()
- Elimina la cuenta con doble confirmación
```

## Flujo de Navegación

1. **Pantalla de Bienvenida**: Selección de rol (Esposa/Esposo)
2. **Login/Registro**: Autenticación
3. **Dashboard**: Menú principal con 6 opciones
4. **Configuración**: Ajustes de cuenta y perfil

## Características de Seguridad

- 🔒 Ingreso mensual es privado (solo el usuario lo ve)
- 🔐 Contraseñas hasheadas con bcrypt
- 🎫 Autenticación con JWT
- ⚠️ Confirmaciones para acciones destructivas
- 🔄 Validaciones en frontend y backend

## Próximos Pasos

Para continuar desarrollando:

1. Agregar modales para crear gastos personales, ahorros y pendientes
2. Implementar edición y eliminación de items
3. Agregar notificaciones/toasts para feedback visual
4. Mejorar estadísticas en el dashboard
5. Agregar gráficos de gastos y ahorros
