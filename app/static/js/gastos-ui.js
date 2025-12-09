// UI Functions for Gastos - Miroma

// Cargar gastos compartidos con nuevo diseño
async function cargarGastosCompartidosUI() {
    try {
        const response = await fetch('/gastos/compartidos', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.gastos) {
            const iconos = {
                'hogar': '🏠', 'comida': '🍽️', 'transporte': '🚗',
                'salud': '💊', 'entretenimiento': '🎮', 'otros': '📦'
            };
            
            const colores = {
                'hogar': 'background: linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%);',
                'comida': 'background: linear-gradient(135deg, #FF9800 0%, #FFB300 100%);',
                'transporte': 'background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);',
                'salud': 'background: linear-gradient(135deg, #F44336 0%, #E57373 100%);',
                'entretenimiento': 'background: linear-gradient(135deg, #00C853 0%, #00E676 100%);',
                'otros': 'background: linear-gradient(135deg, #78909C 0%, #90A4AE 100%);'
            };
            
            const html = data.gastos.map(g => `
                <div class="expense-item">
                    <div class="expense-icon" style="${colores[g.categoria] || colores.otros}">
                        ${iconos[g.categoria] || iconos.otros}
                    </div>
                    <div class="expense-info">
                        <div class="expense-name">${g.nombre}</div>
                        <div class="expense-meta">${g.categoria.charAt(0).toUpperCase() + g.categoria.slice(1)} • ${new Date(g.fecha).toLocaleDateString('es-ES')}</div>
                    </div>
                    <div class="expense-amount">
                        <div class="expense-total">Total<br>$${(g.monto_total || 0).toLocaleString()}</div>
                        <div style="color: #00C853; font-weight: 600; font-size: 0.875rem; margin-top: 0.25rem;">Tu parte<br>$${(g.mi_aporte || 0).toLocaleString()}</div>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-compartidos').innerHTML = html || '<p style="text-align: center; color: #999; padding: 2rem;">No hay gastos registrados</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Cargar gastos personales con nuevo diseño
async function cargarGastosPersonalesUI() {
    try {
        const response = await fetch('/gastos/personales', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.gastos) {
            const iconos = {
                'hogar': '🏠', 'comida': '☕', 'transporte': '🚗',
                'salud': '💊', 'entretenimiento': '🎮', 'ropa': '👕', 'otros': '📦'
            };
            
            const colores = {
                'hogar': 'background: linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%);',
                'comida': 'background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);',
                'transporte': 'background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);',
                'salud': 'background: linear-gradient(135deg, #F44336 0%, #E57373 100%);',
                'entretenimiento': 'background: linear-gradient(135deg, #00C853 0%, #00E676 100%);',
                'ropa': 'background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);',
                'otros': 'background: linear-gradient(135deg, #78909C 0%, #90A4AE 100%);'
            };
            
            const html = data.gastos.map(g => `
                <div class="expense-item">
                    <div class="expense-icon" style="${colores[g.categoria] || colores.otros}">
                        ${iconos[g.categoria] || iconos.otros}
                    </div>
                    <div class="expense-info">
                        <div class="expense-name">${g.nombre}</div>
                        <div class="expense-meta">${new Date(g.fecha).toLocaleDateString('es-ES')}</div>
                    </div>
                    <div class="expense-amount">
                        <div class="expense-total">$${(g.monto || 0).toLocaleString()}</div>
                        <div class="expense-category">${g.categoria.charAt(0).toUpperCase() + g.categoria.slice(1)}</div>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('lista-gastos-personales').innerHTML = html || '<p style="text-align: center; color: #999; padding: 2rem;">No hay gastos registrados</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Cargar ahorros con nuevo diseño
async function cargarAhorrosUI() {
    try {
        const response = await fetch('/ahorros/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.ahorros) {
            const html = data.ahorros.map(a => {
                const progreso = a.progreso || 0;
                const ahorrado = a.monto_actual || 0;
                const falta = (a.meta_monto || 0) - ahorrado;
                
                return `
                    <div class="savings-card">
                        <div class="savings-header">
                            <div class="savings-icon" style="background: linear-gradient(135deg, #FF9800 0%, #FFB300 100%);">
                                ${a.nombre.includes('Viaje') ? '✈️' : a.nombre.includes('Carro') || a.nombre.includes('Auto') ? '🚗' : '🎯'}
                            </div>
                            <div style="flex: 1;">
                                <div class="savings-title">${a.nombre}</div>
                                <div class="savings-meta">Meta: $${(a.meta_monto || 0).toLocaleString()}</div>
                            </div>
                            <div class="badge badge-${progreso >= 100 ? 'green' : progreso >= 50 ? 'yellow' : 'red'}" style="margin-left: auto;">
                                🎯
                            </div>
                        </div>
                        
                        <div class="savings-progress">
                            <div class="progress-bar-large">
                                <div class="progress-fill-large" style="width: ${progreso}%; background: linear-gradient(90deg, #FF9800 0%, #FFB300 100%);"></div>
                            </div>
                            <div style="text-align: center; margin-top: 0.5rem; font-weight: 600; color: #FF9800;">
                                Progreso ${progreso.toFixed(0)}%
                            </div>
                        </div>
                        
                        <div class="savings-amounts">
                            <div class="savings-amount-item" style="background: #E8F5E9; padding: 1rem; border-radius: 0.75rem; flex: 1;">
                                <div class="savings-amount-label">Ahorrado</div>
                                <div class="savings-amount-value" style="color: #00C853;">$${ahorrado.toLocaleString()}</div>
                            </div>
                            <div class="savings-amount-item" style="background: #FFF3E0; padding: 1rem; border-radius: 0.75rem; flex: 1; margin-left: 1rem;">
                                <div class="savings-amount-label">Falta</div>
                                <div class="savings-amount-value" style="color: #FF9800;">$${falta.toLocaleString()}</div>
                            </div>
                        </div>
                        
                        <button onclick="mostrarModalAporte(${a.id})" class="btn" style="margin-top: 1rem; background: white; border: 2px solid #FF9800; color: #FF9800; padding: 0.75rem;">
                            + Agregar aporte
                        </button>
                    </div>
                `;
            }).join('');
            
            document.getElementById('lista-ahorros').innerHTML = html || '<p style="text-align: center; color: #999; padding: 2rem;">No hay metas de ahorro</p>';
            
            // Calcular total ahorrado
            const totalAhorrado = data.ahorros.reduce((sum, a) => sum + (a.monto_actual || 0), 0);
            const totalEl = document.getElementById('total-ahorrado');
            if (totalEl) {
                totalEl.textContent = `$${totalAhorrado.toLocaleString()}`;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Cargar pendientes con nuevo diseño
async function cargarPendientesUI() {
    try {
        const response = await fetch('/pendientes/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const data = await response.json();
        
        if (response.ok && data.pendientes) {
            const iconos = {
                'hogar': '🏠', 'tramites': '📄', 'eventos': '🎉',
                'familia': '👨‍👩‍👧', 'salud': '💊', 'otros': '📌'
            };
            
            const colores = {
                'hogar': 'background: linear-gradient(135deg, #4A9EFF 0%, #2196F3 100%);',
                'tramites': 'background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);',
                'eventos': 'background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);',
                'familia': 'background: linear-gradient(135deg, #00C853 0%, #00E676 100%);',
                'salud': 'background: linear-gradient(135deg, #F44336 0%, #E57373 100%);',
                'otros': 'background: linear-gradient(135deg, #78909C 0%, #90A4AE 100%);'
            };
            
            const activos = data.pendientes.filter(p => !p.completado);
            const completados = data.pendientes.filter(p => p.completado);
            
            // Actualizar contadores
            document.getElementById('count-pendientes').textContent = activos.length;
            document.getElementById('count-completadas').textContent = completados.length;
            
            // Renderizar activos
            const htmlActivos = activos.map(p => `
                <div class="todo-item" onclick="togglePendiente(${p.id})">
                    <input type="checkbox" class="todo-checkbox" ${p.completado ? 'checked' : ''}>
                    <div class="todo-icon" style="${colores[p.categoria] || colores.otros}">
                        ${iconos[p.categoria] || iconos.otros}
                    </div>
                    <div class="todo-info">
                        <div class="todo-name">${p.titulo}</div>
                        <div class="todo-meta">${p.categoria.charAt(0).toUpperCase() + p.categoria.slice(1)} • ${p.recordatorio ? new Date(p.recordatorio).toLocaleDateString('es-ES') : 'Sin fecha'}</div>
                    </div>
                </div>
            `).join('');
            
            // Renderizar completados
            const htmlCompletados = completados.map(p => `
                <div class="todo-item completed" onclick="togglePendiente(${p.id})">
                    <input type="checkbox" class="todo-checkbox" checked>
                    <div class="todo-icon" style="${colores[p.categoria] || colores.otros}; opacity: 0.5;">
                        ${iconos[p.categoria] || iconos.otros}
                    </div>
                    <div class="todo-info">
                        <div class="todo-name">${p.titulo}</div>
                        <div class="todo-meta">${p.categoria.charAt(0).toUpperCase() + p.categoria.slice(1)}</div>
                    </div>
                    <div style="color: #00C853; font-size: 1.5rem;">✓</div>
                </div>
            `).join('');
            
            document.getElementById('lista-pendientes-activos').innerHTML = htmlActivos || '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes activos</p>';
            document.getElementById('lista-pendientes-completados').innerHTML = htmlCompletados || '<p style="text-align: center; color: #999; padding: 2rem;">No hay pendientes completados</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
