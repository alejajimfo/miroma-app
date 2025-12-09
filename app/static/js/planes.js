// Funciones para el módulo de Planes a Futuro
let planesData = [];

async function cargarPlanes() {
    try {
        const response = await fetch('/planes/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.planes) {
            planesData = data.planes;
            renderPlanesGrid();
        } else {
            document.getElementById('lista-planes').innerHTML = '<p style="color: #999; text-align: center; padding: 2rem;">No hay planes aún. ¡Crea tu primer plan!</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('lista-planes').innerHTML = '<p style="color: #F44336; text-align: center; padding: 2rem;">Error cargando planes</p>';
    }
}

function renderPlanesGrid() {
    const container = document.getElementById('lista-planes');
    
    if (planesData.length === 0) {
        container.innerHTML = '<p style="color: rgba(255,255,255,0.6); text-align: center; padding: 40px;">No hay planes aún. ¡Crea tu primer plan!</p>';
        return;
    }
    
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    ];
    
    const iconos = {
        'viaje': '✈️',
        'vehiculo': '🚗',
        'hogar': '🏠',
        'evento': '🎉',
        'personalizado': '📝'
    };
    
    const html = planesData.map((p, index) => `
        <div class="plan-card" onclick="verDetallePlan(${p.id})">
            <div class="plan-card-image" style="background: ${gradients[index % gradients.length]}">
                <span style="font-size: 4rem;">${iconos[p.tipo] || '🎯'}</span>
            </div>
            <div class="plan-card-content">
                <div class="plan-card-title">${p.nombre}</div>
                <div class="plan-card-subtitle">${p.items ? p.items.length : 0} elementos</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${p.progreso || 0}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-top: 0.5rem;">
                    <span style="color: #6b7280;">${(p.progreso || 0).toFixed(0)}% completado</span>
                    <span style="color: #4f46e5; font-weight: 600;">$${(p.monto_total || 0).toLocaleString()}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function renderPlanesTimeline() {
    const container = document.getElementById('timeline-planes');
    
    if (planesData.length === 0) {
        container.innerHTML = '<p style="color: rgba(255,255,255,0.6); text-align: center; padding: 40px;">No hay planes para mostrar</p>';
        return;
    }
    
    // Ordenar por fecha objetivo o fecha de creación
    const planesSorted = [...planesData].sort((a, b) => {
        const dateA = a.fecha_objetivo ? new Date(a.fecha_objetivo) : new Date(a.fecha_creacion);
        const dateB = b.fecha_objetivo ? new Date(b.fecha_objetivo) : new Date(b.fecha_creacion);
        return dateA - dateB;
    });
    
    const html = `
        <div class="timeline-line"></div>
        ${planesSorted.map((plan, index) => {
            const progreso = plan.progreso || 0;
            const estado = progreso >= 100 ? 'completed' : progreso > 0 ? 'in-progress' : 'pending';
            const fecha = plan.fecha_objetivo ? new Date(plan.fecha_objetivo).toLocaleDateString('es-ES', { year: 'numeric', month: 'long' }) : 'Sin fecha';
            
            return `
                <div class="timeline-item">
                    <div class="timeline-content" onclick="verDetallePlan(${plan.id})">
                        <div class="timeline-date">${fecha}</div>
                        <div class="timeline-title">${plan.nombre}</div>
                        <div class="timeline-amount">$${(plan.monto_total || 0).toLocaleString()}</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progreso}%; background: var(--accent);"></div>
                        </div>
                        <div style="margin-top: 8px; color: rgba(255,255,255,0.6);">
                            ${progreso.toFixed(0)}% completado
                        </div>
                        ${plan.aportes ? `
                            <div class="timeline-contributions">
                                <div class="contribution-item contribution-user1">
                                    <div class="contribution-label">Tu aporte</div>
                                    <div class="contribution-amount">$${(plan.mi_aporte_total || 0).toLocaleString()}</div>
                                </div>
                                <div class="contribution-item contribution-user2">
                                    <div class="contribution-label">Pareja</div>
                                    <div class="contribution-amount">$${(plan.aporte_pareja_total || 0).toLocaleString()}</div>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                    <div class="timeline-marker ${estado}">
                        ${progreso >= 100 ? '✓' : (index + 1)}
                    </div>
                </div>
            `;
        }).join('')}
    `;
    
    container.innerHTML = html;
}

function mostrarVistaPlan(vista) {
    // Actualizar tabs
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
        btn.style.color = '#6b7280';
        btn.style.borderBottom = 'none';
    });
    
    const activeTab = vista === 'grid' ? document.getElementById('tab-grid') : document.getElementById('tab-timeline');
    activeTab.classList.add('active');
    activeTab.style.color = '#4f46e5';
    activeTab.style.borderBottom = '2px solid #4f46e5';
    
    if (vista === 'grid') {
        document.getElementById('planes-grid-view').classList.remove('hidden');
        document.getElementById('planes-timeline-view').classList.add('hidden');
    } else {
        document.getElementById('planes-grid-view').classList.add('hidden');
        document.getElementById('planes-timeline-view').classList.remove('hidden');
    }
}

async function verDetallePlan(planId) {
    try {
        const response = await fetch(`/planes/${planId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.plan) {
            renderDetallePlan(data.plan);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error cargando detalle del plan');
    }
}

function renderDetallePlan(plan) {
    // Ocultar sección de planes y mostrar detalle
    document.getElementById('seccion-planes').classList.add('hidden');
    document.getElementById('seccion-plan-detalle').classList.remove('hidden');
    
    const progreso = plan.progreso || 0;
    const items = plan.items || [];
    
    const iconos = {
        'viaje': '✈️',
        'vehiculo': '🚗',
        'hogar': '🏠',
        'evento': '🎉',
        'personalizado': '📝'
    };
    
    const html = `
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
            <button onclick="volverAPlanes()" class="btn-ghost" style="border-radius: 50%; width: 3rem; height: 3rem; padding: 0;">
                ←
            </button>
            <div style="flex: 1;">
                <h2 style="margin: 0;">${plan.nombre}</h2>
                <p style="color: #6b7280; font-size: 0.875rem;">Desglose detallado</p>
            </div>
        </div>
        
        <div class="plan-detail-header">
            <div style="font-size: 4rem; margin-bottom: 1rem;">${iconos[plan.tipo] || '🎯'}</div>
            <div class="plan-detail-title">${plan.nombre}</div>
            <div class="plan-detail-meta">
                <div class="plan-meta-item">
                    <div class="plan-meta-label">Progreso</div>
                    <div class="plan-meta-value">${progreso.toFixed(0)}%</div>
                </div>
                <div class="plan-meta-item">
                    <div class="plan-meta-label">Total</div>
                    <div class="plan-meta-value">$${(plan.monto_total || 0).toLocaleString()}</div>
                </div>
                <div class="plan-meta-item">
                    <div class="plan-meta-label">Items</div>
                    <div class="plan-meta-value">${items.length}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 style="margin: 0;">Elementos del plan</h3>
                <button onclick="mostrarModal('modal-agregar-item-plan')" class="btn-primary">+ Agregar</button>
            </div>
            
            <div class="items-list">
                ${items.map(item => {
                    const estado = item.estado || 'pendiente';
                    const iconoEstado = estado === 'pagado' ? '✓' : estado === 'en_progreso' ? '⏳' : '○';
                    const claseEstado = estado === 'pagado' ? 'completed' : estado === 'en_progreso' ? 'in-progress' : 'pending';
                    const statusText = estado === 'pagado' ? 'Pagado' : estado === 'en_progreso' ? 'En progreso' : 'Pendiente';
                    const statusColor = estado === 'pagado' ? '#16a34a' : estado === 'en_progreso' ? '#d97706' : '#6b7280';
                    
                    return `
                        <div class="item-card">
                            <div class="item-status ${claseEstado}">${iconoEstado}</div>
                            <div class="item-info">
                                <div class="item-name">${item.nombre}</div>
                                <div style="font-size: 0.875rem; color: ${statusColor}; margin-bottom: 0.5rem;">${statusText}</div>
                                <div class="item-amounts">
                                    <span class="item-amount-total">Estimado: $${(item.monto_estimado || 0).toLocaleString()}</span>
                                </div>
                            </div>
                            <button onclick="cambiarEstadoItem(${plan.id}, ${item.id}, '${estado}')" class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.875rem; ${estado === 'pagado' ? 'background: #00C853;' : ''}">
                                ${estado === 'pagado' ? '✓ Pagado' : 'Marcar pagado'}
                            </button>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
    
    document.getElementById('plan-detalle-content').innerHTML = html;
}

function volverAPlanes() {
    document.getElementById('seccion-plan-detalle').classList.add('hidden');
    document.getElementById('seccion-planes').classList.remove('hidden');
    cargarPlanes(); // Recargar para actualizar cambios
}

async function cambiarEstadoItem(planId, itemId, estadoActual) {
    try {
        // Toggle: si está pagado, volver a pendiente; si no, marcar como pagado
        const nuevoEstado = estadoActual === 'pagado' ? 'pendiente' : 'pagado';
        
        const response = await fetch(`/planes/${planId}/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ estado: nuevoEstado })
        });
        
        if (response.ok) {
            verDetallePlan(planId); // Recargar detalle
        } else {
            alert('Error actualizando item');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error actualizando item');
    }
}


// Crear nuevo plan
async function crearPlan(event) {
    event.preventDefault();
    
    const data = {
        nombre: document.getElementById('plan-nombre').value,
        tipo: document.getElementById('plan-tipo').value
    };
    
    try {
        const response = await fetch('/planes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Plan creado exitosamente');
            cerrarModal('modal-crear-plan');
            document.getElementById('form-crear-plan').reset();
            cargarPlanes();
        } else {
            const error = await response.json();
            alert(error.error || 'Error al crear plan');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear plan');
    }
}
