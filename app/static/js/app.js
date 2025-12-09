// Miroma - JavaScript Principal
let currentUser = null;
let authToken = null;
let selectedRole = null;

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
        console.error('Error:', error);
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
    
    if (currentUser && currentUser.pareja_id) {
        document.getElementById('vinculacion-section').classList.add('hidden');
        document.getElementById('menu-principal').classList.remove('hidden');
        cargarSemaforo();
    } else {
        document.getElementById('vinculacion-section').classList.remove('hidden');
        document.getElementById('menu-principal').classList.add('hidden');
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
        
        if (response.ok && data.semaforo) {
            const semaforo = data.semaforo;
            const html = `
                <div class="semaforo ${semaforo.estado}">
                    ${semaforo.mensaje}<br>
                    Gastos: $${data.total_gastos ? data.total_gastos.toLocaleString() : '0'}
                </div>
            `;
            const container = document.getElementById('semaforo-container');
            if (container) {
                container.innerHTML = html;
            }
        }
    } catch (error) {
        console.error('Error cargando semáforo:', error);
    }
}

async function cargarGastosCompartidos() {
    try {
        const response = await fetch('/gastos/compartidos', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.gastos) {
            const html = data.gastos.map(g => `
                <div class="lista-item">
                    <div>
                        <strong>${g.nombre}</strong><br>
                        <small>${g.categoria} - ${new Date(g.fecha).toLocaleDateString()}</small><br>
                        Total: $${g.monto_total ? g.monto_total.toLocaleString() : '0'}<br>
                        <strong style="color: var(--shared)">Tu parte: $${g.mi_aporte ? g.mi_aporte.toLocaleString() : '0'}</strong>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-compartidos').innerHTML = html || '<p>No hay gastos</p>';
        } else {
            document.getElementById('lista-gastos-compartidos').innerHTML = '<p>No hay gastos</p>';
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
            alert('Gasto creado exitosamente');
            cerrarModal('modal-crear-gasto');
            cargarGastosCompartidos();
            cargarSemaforo();
            e.target.reset();
        } else {
            alert(result.error);
        }
    } catch (error) {
        alert('Error creando gasto');
    }
}

async function cargarGastosPersonales() {
    try {
        const response = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.gastos) {
            const html = data.gastos.map(g => `
                <div class="lista-item">
                    <div>
                        <strong>${g.nombre}</strong><br>
                        <small>${g.categoria} - ${new Date(g.fecha).toLocaleDateString()}</small><br>
                        <strong>$${g.monto ? g.monto.toLocaleString() : '0'}</strong>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-personales').innerHTML = html || '<p>No hay gastos</p>';
        } else {
            document.getElementById('lista-gastos-personales').innerHTML = '<p>No hay gastos</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('lista-gastos-personales').innerHTML = '<p>Error cargando gastos</p>';
    }
}

async function cargarAhorros() {
    try {
        const response = await fetch('/ahorros/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.ahorros) {
            const html = data.ahorros.map(a => `
                <div class="card">
                    <h4>${a.nombre}</h4>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${a.progreso || 0}%"></div>
                    </div>
                    <p>${(a.progreso || 0).toFixed(0)}% - $${(a.monto_actual || 0).toLocaleString()} de $${(a.meta_monto || 0).toLocaleString()}</p>
                </div>
            `).join('');
            
            document.getElementById('lista-ahorros').innerHTML = html || '<p>No hay metas</p>';
        } else {
            document.getElementById('lista-ahorros').innerHTML = '<p>No hay metas</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('lista-ahorros').innerHTML = '<p>Error cargando ahorros</p>';
    }
}

async function cargarPendientes() {
    try {
        const response = await fetch('/pendientes/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.pendientes) {
            const html = data.pendientes.map(p => `
                <div class="checkbox-item ${p.completado ? 'completado' : ''}">
                    <input type="checkbox" ${p.completado ? 'checked' : ''} 
                           onchange="togglePendiente(${p.id})">
                    <span>${p.titulo} - ${p.categoria}</span>
                </div>
            `).join('');
            
            document.getElementById('lista-pendientes').innerHTML = html || '<p>No hay pendientes</p>';
        } else {
            document.getElementById('lista-pendientes').innerHTML = '<p>No hay pendientes</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('lista-pendientes').innerHTML = '<p>Error cargando pendientes</p>';
    }
}

async function togglePendiente(id) {
    try {
        await fetch(`/pendientes/${id}/completar`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        cargarPendientes();
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
            <p style="color: #999;">No estás vinculado con una pareja aún.</p>
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
        } else {
            const error = await response.json();
            alert(error.error || 'Error al crear gasto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear gasto');
    }
}
