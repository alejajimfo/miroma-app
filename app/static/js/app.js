// Miroma - JavaScript Principal
let currentUser = null;
let authToken = null;
let selectedRole = null;
let usandoSinPareja = false;

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkAuth();
});

// Funciones de navegación
function seleccionarRol(rol) {
    selectedRole = rol;
    document.getElementById('reg-rol').value = rol;
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('login-screen').classList.remove('hidden');
    
    // Actualizar color del logo según rol
    const logoCircle = document.querySelector('#login-screen .logo-circle');
    if (rol === 'esposa') {
        logoCircle.style.background = 'linear-gradient(135deg, #FF69B4 0%, #FF1493 100%)';
        logoCircle.textContent = '💗';
    } else {
        logoCircle.style.background = 'linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%)';
        logoCircle.textContent = '💙';
    }
}

function mostrarLogin() {
    document.getElementById('register-screen').classList.add('hidden');
    document.getElementById('login-screen').classList.remove('hidden');
}

function mostrarRegistro() {
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('register-screen').classList.remove('hidden');
}

function volverABienvenida() {
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('register-screen').classList.add('hidden');
    document.getElementById('welcome-screen').classList.remove('hidden');
    selectedRole = null;
}

function mostrarRecuperarPassword() {
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('recuperar-password-screen').classList.remove('hidden');
}

function setupEventListeners() {
    // Login
    document.getElementById('login-form')?.addEventListener('submit', handleLogin);
    
    // Registro
    document.getElementById('registro-form')?.addEventListener('submit', handleRegistro);
    
    // Logout
    document.getElementById('btn-logout')?.addEventListener('click', handleLogout);
    
    // Vinculación
    document.getElementById('btn-generar-codigo')?.addEventListener('click', generarCodigo);
    document.getElementById('btn-vincular')?.addEventListener('click', vincularPareja);
    
    // Crear gasto compartido
    document.getElementById('form-crear-gasto')?.addEventListener('submit', crearGastoCompartido);
    
    // Recuperar contraseña
    document.getElementById('recuperar-form')?.addEventListener('submit', handleRecuperarPassword);
    document.getElementById('verificar-codigo-form')?.addEventListener('submit', handleVerificarCodigo);
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        // Verificar si la respuesta es JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error('Respuesta no es JSON:', text);
            alert('Error: El servidor no devolvió JSON. Verifica la consola.');
            return;
        }
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.usuario;
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            mostrarPantallaPrincipal();
        } else {
            alert(data.error || 'Error al iniciar sesión');
        }
    } catch (error) {
        console.error('Error completo:', error);
        alert('Error de conexión: ' + error.message);
    }
}


async function handleRegistro(e) {
    e.preventDefault();
    const data = {
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value,
        apodo: document.getElementById('reg-apodo').value,
        rol: document.getElementById('reg-rol').value,
        ingreso_mensual: document.getElementById('reg-ingreso').value
    };
    
    try {
        const response = await fetch('/auth/registro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            currentUser = result.usuario;
            authToken = result.access_token;
            localStorage.setItem('authToken', authToken);
            mostrarPantallaPrincipal();
        } else {
            alert(result.error || 'Error al registrarse');
        }
    } catch (error) {
        alert('Error de conexión');
    }
}

function handleLogout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('authToken');
    location.reload();
}

function checkAuth() {
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        // Recordar si eligió usar sin pareja
        usandoSinPareja = localStorage.getItem('usandoSinPareja') === 'true';
        cargarPerfil();
    }
}

async function cargarPerfil() {
    try {
        const response = await fetch('/auth/perfil', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data.usuario;
            mostrarPantallaPrincipal();
        } else {
            localStorage.removeItem('authToken');
        }
    } catch (error) {
        console.error('Error cargando perfil');
    }
}

function mostrarPantallaPrincipal() {
    // Ocultar todas las pantallas de auth
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('register-screen').classList.add('hidden');
    document.getElementById('main-screen').classList.remove('hidden');
    
    if (currentUser && currentUser.apodo) {
        document.getElementById('bienvenida').textContent = currentUser.apodo;
        
        // Actualizar color del header según el rol
        const userHeader = document.getElementById('user-header');
        if (userHeader && currentUser.rol) {
            if (currentUser.rol === 'esposa') {
                userHeader.style.background = 'linear-gradient(135deg, #FF69B4 0%, #FF1493 100%)';
            } else {
                userHeader.style.background = 'linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%)';
            }
        }
    }
    
    // Cargar estadísticas rápidas del dashboard con un pequeño delay
    setTimeout(() => {
        cargarEstadisticasRapidas();
    }, 100);
    
    if (currentUser && (currentUser.pareja_id || usandoSinPareja)) {
        document.getElementById('vinculacion-section').classList.add('hidden');
        document.getElementById('menu-principal').classList.remove('hidden');
        
        // Mostrar/ocultar secciones según si tiene pareja
        if (currentUser.pareja_id) {
            // Usuario con pareja - mostrar todas las secciones
            document.getElementById('menu-gastos-compartidos').style.display = 'block';
            document.getElementById('menu-ahorros').style.display = 'block';
            document.getElementById('menu-pendientes').style.display = 'block';
            document.getElementById('menu-planes').style.display = 'block';
            cargarSemaforo();
        } else {
            // Usuario sin pareja - solo ocultar "Nuestros gastos", el resto sí puede usarlo
            document.getElementById('menu-gastos-compartidos').style.display = 'none';
            document.getElementById('menu-ahorros').style.display = 'block';
            document.getElementById('menu-pendientes').style.display = 'block';
            document.getElementById('menu-planes').style.display = 'block';
        }
    } else {
        document.getElementById('vinculacion-section').classList.remove('hidden');
        document.getElementById('menu-principal').classList.add('hidden');
        // Asegurar que los datos estén en cero para usuarios sin pareja
        document.getElementById('stat-ahorros-total').textContent = '$0';
        document.getElementById('stat-pendientes-activos').textContent = '0 tareas';
    }
}

async function generarCodigo() {
    try {
        const response = await fetch('/auth/generar-codigo', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('codigo-generado').innerHTML = 
                `<strong>Tu código: ${data.codigo}</strong><br>Compártelo con tu pareja`;
            currentUser.pareja_id = data.pareja_id;
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error generando código');
    }
}

async function vincularPareja() {
    const codigo = document.getElementById('input-codigo').value;
    
    try {
        const response = await fetch('/auth/vincular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ codigo })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('¡Vinculación exitosa!');
            currentUser.pareja_id = data.pareja.id;
            mostrarPantallaPrincipal();
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error vinculando');
    }
}

function mostrarSeccion(seccion) {
    // Ocultar todas las secciones
    document.querySelectorAll('[id^="seccion-"]').forEach(el => el.classList.add('hidden'));
    document.getElementById('menu-principal').classList.add('hidden');
    
    if (seccion === 'menu') {
        document.getElementById('menu-principal').classList.remove('hidden');
        // Recargar estadísticas cuando vuelve al menú principal
        setTimeout(() => {
            cargarEstadisticasRapidas();
        }, 100);
    } else {
        document.getElementById(`seccion-${seccion}`).classList.remove('hidden');
        
        // Actualizar colores de botones según rol
        actualizarColoresBotones();
        
        // Cargar datos según la sección
        if (seccion === 'gastos-compartidos') cargarGastosCompartidos();
        if (seccion === 'gastos-personales') cargarGastosPersonales();
        if (seccion === 'ahorros') cargarAhorros();
        if (seccion === 'pendientes') cargarPendientes();
        if (seccion === 'planes') cargarPlanes();
        if (seccion === 'configuracion') cargarConfiguracion();
    }
}

async function cargarSemaforo() {
    try {
        const response = await fetch('/gastos/semaforo', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        

        
        if (response.ok) {
            const totalGastos = data.total_gastos || 0;
            const ingresoMensual = currentUser?.ingreso_mensual || 0;
            const porcentajeGastado = ingresoMensual > 0 ? (totalGastos / ingresoMensual * 100) : 0;
            
            // Actualizar elementos del semáforo
            document.getElementById('semaforo-gastado').textContent = `$${totalGastos.toLocaleString()}`;
            document.getElementById('semaforo-presupuesto').textContent = `$${ingresoMensual.toLocaleString()}`;
            
            // Actualizar barra de progreso
            const fillElement = document.getElementById('semaforo-fill');
            fillElement.style.width = `${Math.min(porcentajeGastado, 100)}%`;
            
            // Actualizar estado y colores
            const estadoElement = document.getElementById('semaforo-estado');
            
            if (porcentajeGastado <= 50) {
                // Verde - Buen estado
                estadoElement.textContent = 'En buen estado';
                estadoElement.className = 'badge badge-green';
                fillElement.style.background = 'linear-gradient(90deg, #00C853, #4CAF50)';
            } else if (porcentajeGastado <= 80) {
                // Amarillo - Precaución
                estadoElement.textContent = 'Precaución';
                estadoElement.className = 'badge badge-yellow';
                fillElement.style.background = 'linear-gradient(90deg, #FF9800, #FFB300)';
            } else {
                // Rojo - Alerta
                estadoElement.textContent = 'Alerta';
                estadoElement.className = 'badge badge-red';
                fillElement.style.background = 'linear-gradient(90deg, #F44336, #E57373)';
            }
            
            // Actualizar resumen personal
            document.getElementById('resumen-aporte').textContent = `$${totalGastos.toLocaleString()}`;
            document.getElementById('resumen-porcentaje').textContent = `${porcentajeGastado.toFixed(0)}%`;
            
        } else {
            // Error o sin datos
            document.getElementById('semaforo-estado').textContent = 'Sin datos';
            document.getElementById('semaforo-estado').className = 'badge badge-gray';
            document.getElementById('semaforo-gastado').textContent = '$0';
            document.getElementById('semaforo-presupuesto').textContent = '$0';
            document.getElementById('resumen-aporte').textContent = '$0';
            document.getElementById('resumen-porcentaje').textContent = '0%';
            document.getElementById('semaforo-fill').style.width = '0%';
        }
    } catch (error) {
        console.error('Error cargando semáforo:', error);
        // Mostrar estado de error
        document.getElementById('semaforo-estado').textContent = 'Error';
        document.getElementById('semaforo-estado').className = 'badge badge-gray';
        document.getElementById('semaforo-gastado').textContent = '$0';
        document.getElementById('semaforo-presupuesto').textContent = '$0';
        document.getElementById('resumen-aporte').textContent = '$0';
        document.getElementById('resumen-porcentaje').textContent = '0%';
        document.getElementById('semaforo-fill').style.width = '0%';
    }
}

async function cargarGastosCompartidos() {
    try {
        const response = await fetch('/gastos/compartidos', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        // Verificar si tiene pareja antes de procesar
        if (!currentUser || !currentUser.pareja_id) {
            document.getElementById('lista-gastos-compartidos').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Vincula con tu pareja para compartir gastos</p>';
            return;
        }
        
        if (response.ok && data.gastos && data.gastos.length > 0) {
            const html = data.gastos.map(g => `
                <div class="lista-item" style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <strong>${g.nombre}</strong><br>
                        <small>${g.categoria} - ${new Date(g.fecha).toLocaleDateString()}</small><br>
                        Total: $${g.monto_total ? g.monto_total.toLocaleString() : '0'}<br>
                        <strong style="color: var(--shared)">Tu parte: $${g.mi_aporte ? g.mi_aporte.toLocaleString() : '0'}</strong>
                    </div>
                    <button onclick="eliminarGastoCompartido(${g.id})" class="btn-icon" style="color: #F44336; background: none; border: none; font-size: 1.5rem; cursor: pointer;" title="Eliminar">
                        🗑️
                    </button>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-compartidos').innerHTML = html;
        } else {
            document.getElementById('lista-gastos-compartidos').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay gastos compartidos aún</p>';
        }
    } catch (error) {
        console.error('Error cargando gastos:', error);
        document.getElementById('lista-gastos-compartidos').innerHTML = '<p>Error cargando gastos</p>';
    }
}

function mostrarModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function cerrarModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

async function crearGastoCompartido(e) {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('gasto-nombre').value,
        monto_total: document.getElementById('gasto-monto').value,
        categoria: document.getElementById('gasto-categoria').value
    };
    
    try {
        const response = await fetch('/gastos/compartidos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('✅ Gasto creado exitosamente');
            cerrarModal('modal-crear-gasto');
            cargarGastosCompartidos();
            cargarSemaforo();
            e.target.reset();
        } else {
            alert('❌ Error: ' + (result.error || 'No se pudo crear el gasto'));
        }
    } catch (error) {
        console.error('Error creando gasto:', error);
        alert('❌ Error de conexión al crear gasto');
    }
}

async function cargarGastosPersonales() {
    try {
        const response = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.gastos && data.gastos.length > 0) {
            const html = data.gastos.map(g => `
                <div class="lista-item" style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <strong>${g.nombre}</strong><br>
                        <small>${g.categoria} - ${new Date(g.fecha).toLocaleDateString()}</small><br>
                        <strong>$${g.monto ? g.monto.toLocaleString() : '0'}</strong>
                    </div>
                    <button onclick="eliminarGastoPersonal(${g.id})" class="btn-icon" style="color: #F44336; background: none; border: none; font-size: 1.5rem; cursor: pointer;" title="Eliminar">
                        🗑️
                    </button>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-personales').innerHTML = html;
        } else {
            document.getElementById('lista-gastos-personales').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay gastos personales aún</p>';
        }
        
        // Actualizar presupuesto personal
        await cargarPresupuestoPersonal();
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('lista-gastos-personales').innerHTML = '<p>Error cargando gastos</p>';
    }
}

async function cargarPresupuestoPersonal() {
    try {
        const response = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        let totalGastosPersonales = 0;
        const fechaActual = new Date();
        const mesActual = fechaActual.getMonth();
        const añoActual = fechaActual.getFullYear();
        
        if (response.ok && data.gastos) {
            // Sumar gastos personales del mes actual
            data.gastos.forEach(gasto => {
                const fechaGasto = new Date(gasto.fecha);
                if (fechaGasto.getMonth() === mesActual && fechaGasto.getFullYear() === añoActual) {
                    totalGastosPersonales += gasto.monto || 0;
                }
            });
        }
        
        // Calcular presupuesto personal (30% del ingreso mensual)
        const ingresoMensual = currentUser?.ingreso_mensual || 0;
        const presupuestoPersonal = ingresoMensual * 0.3; // 30% para gastos personales
        const disponible = presupuestoPersonal - totalGastosPersonales;
        const porcentajeUsado = presupuestoPersonal > 0 ? (totalGastosPersonales / presupuestoPersonal * 100) : 0;
        
        // Actualizar UI
        document.getElementById('presupuesto-gastado').textContent = `${totalGastosPersonales.toLocaleString()}`;
        document.getElementById('presupuesto-total').textContent = `${presupuestoPersonal.toLocaleString()}`;
        document.getElementById('presupuesto-disponible').textContent = `${disponible.toLocaleString()}`;
        
        // Actualizar barra de progreso
        const fillElement = document.getElementById('presupuesto-personal-fill');
        if (fillElement) {
            fillElement.style.width = `${Math.min(porcentajeUsado, 100)}%`;
            
            // Cambiar color según el porcentaje usado
            if (porcentajeUsado <= 50) {
                fillElement.style.background = 'linear-gradient(90deg, #4CAF50, #00C853)';
            } else if (porcentajeUsado <= 80) {
                fillElement.style.background = 'linear-gradient(90deg, #FF9800, #FFB300)';
            } else {
                fillElement.style.background = 'linear-gradient(90deg, #F44336, #E57373)';
            }
        }
        
    } catch (error) {
        console.error('Error cargando presupuesto personal:', error);
        document.getElementById('presupuesto-gastado').textContent = '$0';
        document.getElementById('presupuesto-total').textContent = '$0';
        document.getElementById('presupuesto-disponible').textContent = '$0';
    }
}

async function cargarAhorros() {
    try {
        // Los ahorros pueden ser individuales o compartidos
        if (!currentUser) {
            document.getElementById('lista-ahorros').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Error cargando usuario</p>';
            document.getElementById('total-ahorrado').textContent = '$0';
            return;
        }
        
        const response = await fetch('/ahorros/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();

        
        if (response.ok && data.ahorros && data.ahorros.length > 0) {
            const html = data.ahorros.map(a => `
                <div class="card">
                    <h4>${a.nombre}</h4>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${a.progreso || 0}%"></div>
                    </div>
                    <p>${(a.progreso || 0).toFixed(0)}% - $${(a.monto_actual || 0).toLocaleString()} de $${(a.meta_monto || 0).toLocaleString()}</p>
                </div>
            `).join('');
            
            document.getElementById('lista-ahorros').innerHTML = html;
            
            // Calcular total ahorrado
            const totalAhorrado = data.ahorros.reduce((sum, ahorro) => sum + (ahorro.monto_actual || 0), 0);
            document.getElementById('total-ahorrado').textContent = `${totalAhorrado.toLocaleString()}`;
        } else if (response.status === 400 && !currentUser.pareja_id) {
            // Usuario sin pareja - mostrar mensaje apropiado
            document.getElementById('total-ahorrado').textContent = '$0';
            document.getElementById('lista-ahorros').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay metas de ahorro aún<br><small>💡 Vincula con tu pareja para compartir metas</small></p>';
        } else {
            document.getElementById('total-ahorrado').textContent = '$0';
            document.getElementById('lista-ahorros').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay metas de ahorro aún</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('total-ahorrado').textContent = '$0';
        document.getElementById('lista-ahorros').innerHTML = '<p>Error cargando ahorros</p>';
    }
}

async function cargarPendientes() {
    try {
        // Los pendientes pueden ser individuales o compartidos
        if (!currentUser) {
            document.getElementById('lista-pendientes-activos').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Error cargando usuario</p>';
            document.getElementById('lista-pendientes-completados').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Error cargando usuario</p>';
            // Actualizar contadores
            document.getElementById('count-pendientes').textContent = '0';
            document.getElementById('count-completadas').textContent = '0';
            return;
        }
        
        const response = await fetch('/pendientes/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();

        
        if (response.ok && data.pendientes && data.pendientes.length > 0) {
            // Separar pendientes activos y completados
            const activos = data.pendientes.filter(p => !p.completado);
            const completados = data.pendientes.filter(p => p.completado);
            
            // Actualizar contadores
            document.getElementById('count-pendientes').textContent = activos.length.toString();
            document.getElementById('count-completadas').textContent = completados.length.toString();
            
            // Renderizar pendientes activos
            const htmlActivos = activos.map(p => `
                <div class="checkbox-item">
                    <input type="checkbox" onchange="togglePendiente(${p.id})">
                    <span>${p.titulo} - ${p.categoria}</span>
                </div>
            `).join('');
            
            // Renderizar pendientes completados
            const htmlCompletados = completados.map(p => `
                <div class="checkbox-item completado">
                    <input type="checkbox" checked onchange="togglePendiente(${p.id})">
                    <span>${p.titulo} - ${p.categoria}</span>
                </div>
            `).join('');
            
            document.getElementById('lista-pendientes-activos').innerHTML = htmlActivos || '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes activos</p>';
            document.getElementById('lista-pendientes-completados').innerHTML = htmlCompletados || '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes completados</p>';
        } else if (response.status === 400 && !currentUser.pareja_id) {
            // Usuario sin pareja - mostrar mensaje apropiado
            document.getElementById('count-pendientes').textContent = '0';
            document.getElementById('count-completadas').textContent = '0';
            document.getElementById('lista-pendientes-activos').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes activos<br><small>💡 Vincula con tu pareja para compartir tareas</small></p>';
            document.getElementById('lista-pendientes-completados').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes completados</p>';
        } else {
            // Sin datos
            document.getElementById('count-pendientes').textContent = '0';
            document.getElementById('count-completadas').textContent = '0';
            document.getElementById('lista-pendientes-activos').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes activos</p>';
            document.getElementById('lista-pendientes-completados').innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes completados</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('count-pendientes').textContent = '0';
        document.getElementById('count-completadas').textContent = '0';
        document.getElementById('lista-pendientes-activos').innerHTML = '<p>Error cargando pendientes</p>';
        document.getElementById('lista-pendientes-completados').innerHTML = '<p>Error cargando pendientes</p>';
    }
}

async function togglePendiente(id) {
    try {
        await fetch(`/pendientes/${id}/completar`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        cargarPendientes();
        // También actualizar las estadísticas rápidas
        cargarPendientesActivos();
    } catch (error) {
        console.error('Error');
    }
}



// Funciones de Configuración
function cargarConfiguracion() {
    if (!currentUser) return;
    
    // Cargar datos del usuario
    document.getElementById('config-apodo').value = currentUser.apodo || '';
    document.getElementById('config-email').value = currentUser.email || '';
    document.getElementById('config-rol').value = currentUser.rol === 'esposa' ? 'Esposa' : 'Esposo';
    document.getElementById('config-ingreso').value = currentUser.ingreso_mensual || '';
    
    // Cargar foto de perfil
    const previewFoto = document.getElementById('preview-foto-perfil');
    if (currentUser.foto_perfil) {
        previewFoto.innerHTML = `<img src="${currentUser.foto_perfil}" style="width: 100%; height: 100%; object-fit: cover;">`;
    } else {
        previewFoto.innerHTML = currentUser.rol === 'esposa' ? '💗' : '💙';
        previewFoto.style.background = currentUser.rol === 'esposa' 
            ? 'linear-gradient(135deg, #FF69B4 0%, #FF1493 100%)'
            : 'linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%)';
    }
    
    // Cargar información de pareja
    cargarInfoPareja();
}

// Previsualizar foto de perfil
function previsualizarFoto(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewFoto = document.getElementById('preview-foto-perfil');
            previewFoto.innerHTML = `<img src="${e.target.result}" style="width: 100%; height: 100%; object-fit: cover;">`;
            previewFoto.style.background = 'transparent';
            
            // Subir foto
            subirFotoPerfil(file);
        };
        reader.readAsDataURL(file);
    }
}

// Subir foto de perfil
async function subirFotoPerfil(file) {
    const formData = new FormData();
    formData.append('foto', file);
    
    try {
        const response = await fetch('/auth/subir-foto', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser.foto_perfil = data.foto_url;
            alert('Foto actualizada exitosamente');
            
            // Actualizar avatar en header
            const userAvatar = document.querySelector('.user-avatar');
            if (userAvatar) {
                userAvatar.innerHTML = `<img src="${data.foto_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
            }
        } else {
            const error = await response.json();
            alert(error.error || 'Error al subir foto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al subir foto');
    }
}

// Actualizar color de botones volver según rol
function actualizarColoresBotones() {
    if (!currentUser) return;
    
    const botonesVolver = document.querySelectorAll('.btn-back');
    botonesVolver.forEach(btn => {
        btn.classList.remove('esposa', 'esposo');
        btn.classList.add(currentUser.rol);
    });
}

async function cargarInfoPareja() {
    if (!currentUser || !currentUser.pareja_id) {
        document.getElementById('info-pareja').innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <p style="color: #999; margin-bottom: 2rem;">No estás vinculado con una pareja aún.</p>
                
                <div style="background: #f0f8ff; padding: 1.5rem; border-radius: 1rem; margin-bottom: 2rem;">
                    <h4 style="color: #4A9EFF; margin-bottom: 1rem;">💑 ¿Quieres vincular con tu pareja?</h4>
                    <p style="color: #666; font-size: 0.875rem; margin-bottom: 1.5rem;">
                        Al vincularte podrán compartir gastos, ahorros, planes y pendientes. Tu ingreso seguirá siendo privado.
                    </p>
                    
                    <div style="display: grid; gap: 1rem;">
                        <button onclick="mostrarVinculacionEnConfig()" class="btn" style="background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%); color: white; font-weight: 600;">
                            💕 Vincular con mi pareja
                        </button>
                    </div>
                </div>
                
                <p style="color: #999; font-size: 0.875rem;">
                    También puedes seguir usando Miroma de forma individual
                </p>
            </div>
        `;
        return;
    }
    
    try {
        const response = await fetch('/auth/perfil', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            const fechaVinculacion = data.pareja?.fecha_vinculacion 
                ? new Date(data.pareja.fecha_vinculacion).toLocaleDateString('es-ES')
                : 'Desconocida';
            
            document.getElementById('info-pareja').innerHTML = `
                <div style="background: #f9f9f9; padding: 1.5rem; border-radius: 1rem;">
                    <p style="margin-bottom: 0.5rem;"><strong>Estado:</strong> Vinculado 💑</p>
                    <p style="margin-bottom: 0.5rem;"><strong>Fecha de vinculación:</strong> ${fechaVinculacion}</p>
                    <p style="color: #666; font-size: 0.875rem; margin-top: 1rem;">
                        Tu pareja puede ver los gastos compartidos, ahorros, pendientes y planes que crean juntos.
                        Tu ingreso mensual es privado y solo tú puedes verlo.
                    </p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error cargando info de pareja:', error);
    }
}

async function actualizarPerfil() {
    const apodo = document.getElementById('config-apodo').value.trim();
    
    if (!apodo) {
        alert('El apodo no puede estar vacío');
        return;
    }
    
    try {
        const response = await fetch('/auth/actualizar-perfil', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ apodo })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser.apodo = apodo;
            document.getElementById('bienvenida').textContent = apodo;
            alert('Perfil actualizado exitosamente');
        } else {
            const error = await response.json();
            alert(error.error || 'Error al actualizar perfil');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar perfil');
    }
}

async function actualizarIngreso() {
    const ingreso = parseFloat(document.getElementById('config-ingreso').value);
    
    if (!ingreso || ingreso < 0) {
        alert('Ingresa un monto válido');
        return;
    }
    
    try {
        const response = await fetch('/auth/actualizar-ingreso', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ ingreso_mensual: ingreso })
        });
        
        if (response.ok) {
            currentUser.ingreso_mensual = ingreso;
            alert('Ingreso actualizado exitosamente');
        } else {
            const error = await response.json();
            alert(error.error || 'Error al actualizar ingreso');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar ingreso');
    }
}

async function cambiarPassword() {
    const passwordActual = document.getElementById('config-password-actual').value;
    const passwordNueva = document.getElementById('config-password-nueva').value;
    const passwordConfirmar = document.getElementById('config-password-confirmar').value;
    
    if (!passwordActual || !passwordNueva || !passwordConfirmar) {
        alert('Completa todos los campos');
        return;
    }
    
    if (passwordNueva !== passwordConfirmar) {
        alert('Las contraseñas nuevas no coinciden');
        return;
    }
    
    if (passwordNueva.length < 6) {
        alert('La contraseña debe tener al menos 6 caracteres');
        return;
    }
    
    try {
        const response = await fetch('/auth/cambiar-password', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                password_actual: passwordActual,
                password_nueva: passwordNueva
            })
        });
        
        if (response.ok) {
            alert('Contraseña cambiada exitosamente');
            document.getElementById('config-password-actual').value = '';
            document.getElementById('config-password-nueva').value = '';
            document.getElementById('config-password-confirmar').value = '';
        } else {
            const error = await response.json();
            alert(error.error || 'Error al cambiar contraseña');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cambiar contraseña');
    }
}

function confirmarDesvinculacion() {
    if (confirm('¿Estás seguro de que quieres desvincular tu cuenta de tu pareja?\n\nLos datos compartidos se mantendrán pero ya no podrán ver la información del otro.')) {
        desvincularPareja();
    }
}

async function desvincularPareja() {
    try {
        const response = await fetch('/auth/desvincular', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            alert('Cuenta desvinculada exitosamente');
            currentUser.pareja_id = null;
            mostrarPantallaPrincipal();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al desvincular');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al desvincular');
    }
}

function confirmarEliminarCuenta() {
    if (confirm('⚠️ ADVERTENCIA ⚠️\n\n¿Estás COMPLETAMENTE seguro de que quieres eliminar tu cuenta?\n\nEsta acción es PERMANENTE y NO se puede deshacer.\nSe eliminarán TODOS tus datos.\n\nEscribe "ELIMINAR" en el siguiente cuadro para confirmar.')) {
        const confirmacion = prompt('Escribe "ELIMINAR" para confirmar:');
        if (confirmacion === 'ELIMINAR') {
            eliminarCuenta();
        } else {
            alert('Eliminación cancelada');
        }
    }
}

async function eliminarCuenta() {
    try {
        const response = await fetch('/auth/eliminar-cuenta', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            alert('Cuenta eliminada exitosamente');
            handleLogout();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al eliminar cuenta');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar cuenta');
    }
}


// Funciones para Ahorros
async function crearAhorro(event) {
    event.preventDefault();
    
    const data = {
        nombre: document.getElementById('ahorro-nombre').value,
        meta_monto: document.getElementById('ahorro-meta').value,
        fecha_objetivo: document.getElementById('ahorro-fecha').value || null
    };
    
    try {
        const response = await fetch('/ahorros/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Meta de ahorro creada exitosamente');
            cerrarModal('modal-crear-ahorro');
            document.getElementById('form-crear-ahorro').reset();
            cargarAhorros();
            // Actualizar estadísticas rápidas
            cargarEstadisticasRapidas();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al crear meta');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear meta');
    }
}

function mostrarModalAporte(ahorroId) {
    document.getElementById('aporte-ahorro-id').value = ahorroId;
    mostrarModal('modal-agregar-aporte');
}

async function agregarAporte(event) {
    event.preventDefault();
    
    const ahorroId = document.getElementById('aporte-ahorro-id').value;
    const data = {
        monto: document.getElementById('aporte-monto').value,
        notas: document.getElementById('aporte-notas').value
    };
    
    try {
        const response = await fetch(`/ahorros/${ahorroId}/aportar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Aporte agregado exitosamente');
            cerrarModal('modal-agregar-aporte');
            document.getElementById('form-agregar-aporte').reset();
            cargarAhorros();
            // Actualizar estadísticas rápidas
            cargarEstadisticasRapidas();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al agregar aporte');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al agregar aporte');
    }
}

// Funciones para Pendientes
async function crearPendiente(event) {
    event.preventDefault();
    
    const data = {
        titulo: document.getElementById('pendiente-titulo').value,
        categoria: document.getElementById('pendiente-categoria').value,
        recordatorio: document.getElementById('pendiente-fecha').value || null,
        notas: document.getElementById('pendiente-notas').value
    };
    
    try {
        const response = await fetch('/pendientes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Pendiente creado exitosamente');
            cerrarModal('modal-crear-pendiente');
            document.getElementById('form-crear-pendiente').reset();
            cargarPendientes();
            // Actualizar estadísticas rápidas
            cargarEstadisticasRapidas();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al crear pendiente');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear pendiente');
    }
}

// Funciones para Gastos Personales
async function crearGastoPersonal(event) {
    event.preventDefault();
    
    const data = {
        nombre: document.getElementById('gasto-personal-nombre').value,
        monto: document.getElementById('gasto-personal-monto').value,
        categoria: document.getElementById('gasto-personal-categoria').value
    };
    
    try {
        const response = await fetch('/gastos/personales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Gasto personal creado exitosamente');
            cerrarModal('modal-crear-gasto-personal');
            document.getElementById('form-crear-gasto-personal').reset();
            cargarGastosPersonales();
            // Actualizar estadísticas rápidas
            cargarEstadisticasRapidas();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al crear gasto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear gasto');
    }
}

// ============================================
// RECUPERACIÓN DE CONTRASEÑA
// ============================================

let emailRecuperacion = '';

async function handleRecuperarPassword(e) {
    e.preventDefault();
    
    const email = document.getElementById('recuperar-email').value;
    emailRecuperacion = email;
    
    try {
        const response = await fetch('/auth/recuperar-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar mensaje según si se envió email o no
            if (data.email_enviado) {
                alert('📧 Código enviado a tu correo electrónico\nRevisa tu bandeja de entrada (y spam)');
            } else if (data.codigo) {
                console.log('🔑 Código de recuperación:', data.codigo);
                alert(`🔑 Código de recuperación: ${data.codigo}\n\n⚠️ Email no configurado - El código aparece aquí\n(En producción se enviará por email)`);
            } else {
                alert('Código generado. Revisa tu email.');
            }
            
            // Ir a pantalla de verificación
            document.getElementById('recuperar-password-screen').classList.add('hidden');
            document.getElementById('verificar-codigo-screen').classList.remove('hidden');
        } else {
            alert(data.error || 'Error al generar código');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

async function handleVerificarCodigo(e) {
    e.preventDefault();
    
    const codigo = document.getElementById('codigo-verificacion').value;
    const passwordNueva = document.getElementById('nueva-password').value;
    
    try {
        const response = await fetch('/auth/restablecer-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: emailRecuperacion,
                codigo: codigo,
                password_nueva: passwordNueva
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Contraseña restablecida exitosamente');
            
            // Limpiar formularios
            document.getElementById('verificar-codigo-form').reset();
            document.getElementById('recuperar-form').reset();
            
            // Volver al login
            document.getElementById('verificar-codigo-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            
            emailRecuperacion = '';
        } else {
            alert(data.error || 'Error al restablecer contraseña');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

async function reenviarCodigo() {
    if (!emailRecuperacion) {
        alert('Error: No hay email registrado');
        return;
    }
    
    try {
        const response = await fetch('/auth/recuperar-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: emailRecuperacion })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.email_enviado) {
                alert('📧 Nuevo código enviado a tu correo');
            } else if (data.codigo) {
                console.log('🔑 Nuevo código:', data.codigo);
                alert(`🔑 Nuevo código: ${data.codigo}\n\n⚠️ Email no configurado`);
            } else {
                alert('Código reenviado exitosamente');
            }
        } else {
            alert(data.error || 'Error al reenviar código');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}
// ============================================
// FUNCIONES DE ELIMINAR GASTOS
// ============================================

async function eliminarGastoCompartido(gastoId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este gasto compartido?')) {
        return;
    }
    
    try {
        const response = await fetch(`/gastos/compartidos/${gastoId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Gasto eliminado exitosamente');
            cargarGastosCompartidos();
            cargarSemaforo();
        } else {
            alert(data.error || 'Error al eliminar gasto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar gasto');
    }
}

async function eliminarGastoPersonal(gastoId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este gasto personal?')) {
        return;
    }
    
    try {
        const response = await fetch(`/gastos/personales/${gastoId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Gasto eliminado exitosamente');
            cargarGastosPersonales();
            cargarSemaforo();
            // Actualizar estadísticas rápidas
            cargarEstadisticasRapidas();
        } else {
            alert(data.error || 'Error al eliminar gasto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar gasto');
    }
}
// ============================================
// REPORTES Y GESTIÓN DE DATOS
// ============================================

async function descargarReportePDF() {
    try {
        const response = await fetch('/reportes/pdf', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            // Crear blob del PDF
            const blob = await response.blob();
            
            // Crear URL temporal
            const url = window.URL.createObjectURL(blob);
            
            // Crear enlace de descarga
            const a = document.createElement('a');
            a.href = url;
            a.download = `miroma_reporte_${new Date().toISOString().slice(0,10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            
            // Limpiar
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            alert('📄 Reporte PDF descargado exitosamente');
        } else {
            const error = await response.json();
            alert('❌ Error al generar reporte: ' + (error.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión al generar reporte');
    }
}

function confirmarLimpiarDatos() {
    const confirmacion = confirm(
        '⚠️ ¿ESTÁS SEGURO?\n\n' +
        'Esta acción eliminará TODOS los datos financieros:\n' +
        '• Gastos compartidos\n' +
        '• Gastos personales\n' +
        '• Ahorros\n' +
        '• Planes futuros\n' +
        '• Pendientes\n\n' +
        '💡 Recomendación: Descarga el reporte PDF antes de continuar.\n\n' +
        'Esta acción NO se puede deshacer.'
    );
    
    if (confirmacion) {
        const segundaConfirmacion = confirm(
            '🚨 ÚLTIMA CONFIRMACIÓN\n\n' +
            'Escribirás "ELIMINAR" para confirmar que quieres borrar todos los datos financieros.\n\n' +
            '¿Continuar?'
        );
        
        if (segundaConfirmacion) {
            const texto = prompt('Escribe "ELIMINAR" para confirmar:');
            if (texto === 'ELIMINAR') {
                limpiarTodosLosDatos();
            } else {
                alert('❌ Cancelado. Los datos no fueron eliminados.');
            }
        }
    }
}

async function limpiarTodosLosDatos() {
    try {
        const response = await fetch('/reportes/eliminar-todo', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Todos los datos financieros han sido eliminados exitosamente\n\n🎉 ¡Puedes empezar un nuevo periodo!');
            
            // Recargar todas las secciones para mostrar datos limpios
            cargarGastosCompartidos();
            cargarGastosPersonales();
            cargarAhorros();
            cargarPlanes();
            cargarPendientes();
            cargarSemaforo();
            
            // Actualizar estadísticas del dashboard
            cargarEstadisticasRapidas();
            
            // Volver al menú principal
            mostrarSeccion('menu');
        } else {
            alert('❌ Error al eliminar datos: ' + (data.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión al eliminar datos');
    }
}
// ============================================
// ESTADÍSTICAS RÁPIDAS DEL DASHBOARD
// ============================================

async function cargarEstadisticasRapidas() {
    try {
        // Verificar que tenemos los datos necesarios
        if (!currentUser || !authToken) {
            console.log('Usuario o token no disponible, reintentando...');
            setTimeout(cargarEstadisticasRapidas, 500);
            return;
        }
        
        // Inicializar con valores por defecto
        document.getElementById('stat-gastos-mes').textContent = '$0';
        document.getElementById('stat-ahorros-total').textContent = '$0';
        document.getElementById('stat-pendientes-activos').textContent = '0 tareas';
        document.getElementById('disponible-ingreso').textContent = '$0';
        document.getElementById('disponible-restante').textContent = '$0';
        
        // Cargar disponible según sueldo
        await cargarDisponibleMensual();
        
        // Cargar gastos del mes actual
        await cargarGastosDelMes();
        
        // Cargar ahorros acumulados
        await cargarAhorrosAcumulados();
        
        // Cargar pendientes activos
        await cargarPendientesActivos();
        
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
        // Asegurar valores por defecto en caso de error
        document.getElementById('stat-gastos-mes').textContent = '$0';
        document.getElementById('stat-ahorros-total').textContent = '$0';
        document.getElementById('stat-pendientes-activos').textContent = '0 tareas';
        document.getElementById('disponible-ingreso').textContent = '$0';
        document.getElementById('disponible-restante').textContent = '$0';
    }
}

async function cargarGastosDelMes() {
    try {
        // Obtener gastos compartidos
        const responseCompartidos = await fetch('/gastos/compartidos', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        // Obtener gastos personales
        const responsePersonales = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        let totalGastos = 0;
        const fechaActual = new Date();
        const mesActual = fechaActual.getMonth();
        const añoActual = fechaActual.getFullYear();
        
        // Sumar gastos compartidos del mes actual
        if (responseCompartidos.ok) {
            const dataCompartidos = await responseCompartidos.json();
            if (dataCompartidos.gastos) {
                dataCompartidos.gastos.forEach(gasto => {
                    const fechaGasto = new Date(gasto.fecha);
                    if (fechaGasto.getMonth() === mesActual && fechaGasto.getFullYear() === añoActual) {
                        totalGastos += gasto.mi_aporte || 0;
                    }
                });
            }
        }
        
        // Sumar gastos personales del mes actual
        if (responsePersonales.ok) {
            const dataPersonales = await responsePersonales.json();
            if (dataPersonales.gastos) {
                dataPersonales.gastos.forEach(gasto => {
                    const fechaGasto = new Date(gasto.fecha);
                    if (fechaGasto.getMonth() === mesActual && fechaGasto.getFullYear() === añoActual) {
                        totalGastos += gasto.monto || 0;
                    }
                });
            }
        }
        
        // Actualizar UI
        document.getElementById('stat-gastos-mes').textContent = `$${totalGastos.toLocaleString()}`;
        
    } catch (error) {
        console.error('Error cargando gastos del mes:', error);
        document.getElementById('stat-gastos-mes').textContent = '$0';
    }
}

async function cargarAhorrosAcumulados() {
    try {
        // Cargar ahorros (individuales o compartidos)
        if (!currentUser) {
            document.getElementById('stat-ahorros-total').textContent = '$0';
            return;
        }
        
        const response = await fetch('/ahorros/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        let totalAhorros = 0;
        
        if (response.ok) {
            const data = await response.json();
            if (data.ahorros && data.ahorros.length > 0) {
                totalAhorros = data.ahorros.reduce((sum, ahorro) => sum + (ahorro.monto_actual || 0), 0);
            }
        }
        
        // Actualizar UI
        document.getElementById('stat-ahorros-total').textContent = `$${totalAhorros.toLocaleString()}`;
        
    } catch (error) {
        console.error('Error cargando ahorros:', error);
        document.getElementById('stat-ahorros-total').textContent = '$0';
    }
}

async function cargarPendientesActivos() {
    try {
        // Cargar pendientes (individuales o compartidos)
        if (!currentUser) {
            document.getElementById('stat-pendientes-activos').textContent = '0 tareas';
            return;
        }
        
        const response = await fetch('/pendientes/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        let pendientesActivos = 0;
        
        if (response.ok) {
            const data = await response.json();
            if (data.pendientes && data.pendientes.length > 0) {
                pendientesActivos = data.pendientes.filter(p => !p.completado).length;
            }
        }
        
        // Actualizar UI
        const texto = pendientesActivos === 1 ? '1 tarea' : `${pendientesActivos} tareas`;
        document.getElementById('stat-pendientes-activos').textContent = texto;
        
    } catch (error) {
        console.error('Error cargando pendientes:', error);
        document.getElementById('stat-pendientes-activos').textContent = '0 tareas';
    }
}
async function cargarDisponibleMensual() {
    try {
        // Mostrar ingreso mensual
        const ingresoMensual = currentUser?.ingreso_mensual || 0;
        document.getElementById('disponible-ingreso').textContent = `$${ingresoMensual.toLocaleString()}`;
        
        // Calcular gastos del mes actual
        let totalGastosMes = 0;
        
        // Obtener gastos compartidos
        const responseCompartidos = await fetch('/gastos/compartidos', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        // Obtener gastos personales
        const responsePersonales = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const fechaActual = new Date();
        const mesActual = fechaActual.getMonth();
        const añoActual = fechaActual.getFullYear();
        
        // Sumar gastos compartidos del mes actual
        if (responseCompartidos.ok) {
            const dataCompartidos = await responseCompartidos.json();
            if (dataCompartidos.gastos) {
                dataCompartidos.gastos.forEach(gasto => {
                    const fechaGasto = new Date(gasto.fecha);
                    if (fechaGasto.getMonth() === mesActual && fechaGasto.getFullYear() === añoActual) {
                        totalGastosMes += gasto.mi_aporte || 0;
                    }
                });
            }
        }
        
        // Sumar gastos personales del mes actual
        if (responsePersonales.ok) {
            const dataPersonales = await responsePersonales.json();
            if (dataPersonales.gastos) {
                dataPersonales.gastos.forEach(gasto => {
                    const fechaGasto = new Date(gasto.fecha);
                    if (fechaGasto.getMonth() === mesActual && fechaGasto.getFullYear() === añoActual) {
                        totalGastosMes += gasto.monto || 0;
                    }
                });
            }
        }
        
        // Calcular disponible
        const disponible = ingresoMensual - totalGastosMes;
        
        // Actualizar UI con color según el disponible
        const elementoDisponible = document.getElementById('disponible-restante');
        elementoDisponible.textContent = `$${disponible.toLocaleString()}`;
        
        // Cambiar color según el disponible
        const cardDisponible = elementoDisponible.closest('.card');
        if (disponible < 0) {
            // Rojo si está en números rojos
            cardDisponible.style.background = 'linear-gradient(135deg, #F44336 0%, #D32F2F 100%)';
        } else if (disponible < ingresoMensual * 0.2) {
            // Naranja si queda menos del 20%
            cardDisponible.style.background = 'linear-gradient(135deg, #FF9800 0%, #F57C00 100%)';
        } else {
            // Verde si está bien
            cardDisponible.style.background = 'linear-gradient(135deg, #4CAF50 0%, #00C853 100%)';
        }
        
    } catch (error) {
        console.error('Error cargando disponible mensual:', error);
        document.getElementById('disponible-ingreso').textContent = '$0';
        document.getElementById('disponible-restante').textContent = '$0';
    }
}
// ============================================
// USO SIN PAREJA
// ============================================

function usarSinPareja() {
    // Marcar que está usando sin pareja
    usandoSinPareja = true;
    localStorage.setItem('usandoSinPareja', 'true');
    
    // Ocultar sección de vinculación y mostrar menú principal
    document.getElementById('vinculacion-section').classList.add('hidden');
    document.getElementById('menu-principal').classList.remove('hidden');
    
    // Solo ocultar "Nuestros gastos", el resto sí puede usarlo individualmente
    document.getElementById('menu-gastos-compartidos').style.display = 'none';
    document.getElementById('menu-ahorros').style.display = 'block';
    document.getElementById('menu-pendientes').style.display = 'block';
    document.getElementById('menu-planes').style.display = 'block';
    
    // Cargar estadísticas para usuario individual
    cargarEstadisticasRapidas();
    
    alert('✅ ¡Perfecto! Puedes usar Miroma de forma individual.\n\n💡 Si más tarde quieres vincular con tu pareja, ve a Configuración.');
}
function mostrarVinculacionEnConfig() {
    // Mostrar modal de vinculación
    const modalHTML = `
        <div id="modal-vinculacion" class="modal active">
            <div class="modal-content">
                <h3 style="text-align: center; margin-bottom: 2rem; color: #FF69B4;">💑 Vincular con tu Pareja</h3>
                
                <div class="grid" style="gap: 2rem;">
                    <div>
                        <h4 style="font-size: 1rem; margin-bottom: 1rem;">Generar Código</h4>
                        <p style="color: #666; font-size: 0.875rem; margin-bottom: 1rem;">
                            Genera un código para que tu pareja se vincule contigo
                        </p>
                        <button onclick="generarCodigoEnModal()" class="btn btn-primary" style="margin-bottom: 1rem;">
                            Generar Código
                        </button>
                        <p id="codigo-generado-modal" style="text-align: center; font-size: 1.5rem; font-weight: 700; color: #FF69B4;"></p>
                    </div>
                    
                    <div>
                        <h4 style="font-size: 1rem; margin-bottom: 1rem;">Ingresar Código</h4>
                        <p style="color: #666; font-size: 0.875rem; margin-bottom: 1rem;">
                            Ingresa el código que te dio tu pareja
                        </p>
                        <input type="text" id="input-codigo-modal" placeholder="Código de 6 dígitos" maxlength="6" style="margin-bottom: 1rem;">
                        <button onclick="vincularEnModal()" class="btn btn-secondary">
                            Vincular
                        </button>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <button onclick="cerrarModalVinculacion()" class="btn btn-ghost">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

async function generarCodigoEnModal() {
    try {
        const response = await fetch('/auth/generar-codigo', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('codigo-generado-modal').textContent = data.codigo;
            alert('✅ Código generado exitosamente\\n\\n📱 Comparte este código con tu pareja para que se vincule contigo');
        } else {
            alert('❌ Error: ' + (data.error || 'No se pudo generar el código'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión');
    }
}

async function vincularEnModal() {
    const codigo = document.getElementById('input-codigo-modal').value.trim();
    
    if (!codigo) {
        alert('❌ Por favor ingresa el código');
        return;
    }
    
    try {
        const response = await fetch('/auth/vincular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ codigo })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ ¡Vinculación exitosa!\\n\\n💑 Ahora pueden compartir gastos, ahorros, planes y pendientes');
            
            // Actualizar usuario actual
            currentUser.pareja_id = data.pareja.id;
            
            // Limpiar preferencia de usar sin pareja
            usandoSinPareja = false;
            localStorage.removeItem('usandoSinPareja');
            
            // Mostrar secciones compartidas
            document.getElementById('menu-gastos-compartidos').style.display = 'block';
            document.getElementById('menu-ahorros').style.display = 'block';
            document.getElementById('menu-pendientes').style.display = 'block';
            document.getElementById('menu-planes').style.display = 'block';
            
            // Cerrar modal y recargar info
            cerrarModalVinculacion();
            cargarInfoPareja();
        } else {
            alert('❌ Error: ' + (data.error || 'Código inválido'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión');
    }
}

function cerrarModalVinculacion() {
    const modal = document.getElementById('modal-vinculacion');
    if (modal) {
        modal.remove();
    }
}