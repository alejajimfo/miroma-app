from flask import Blueprint, render_template_string, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db
from app.models import Usuario, Pareja, GastoCompartido, GastoPersonal, Ahorro, PlanFuturo, Pendiente
from sqlalchemy import text

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/db')
@login_required
def ver_base_datos():
    """Ver todos los datos de la base de datos"""
    
    try:
        # Obtener todos los datos
        usuarios = Usuario.query.all()
        parejas = Pareja.query.all()
        gastos_compartidos = GastoCompartido.query.all()
        gastos_personales = GastoPersonal.query.all()
        ahorros = Ahorro.query.all()
        planes = PlanFuturo.query.all()
        pendientes = Pendiente.query.all()
        
        # Template HTML para mostrar los datos
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Base de Datos - Miroma</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f0f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .table-section { margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #9C27B0; text-align: center; }
                h2 { color: #FF69B4; border-bottom: 2px solid #FF69B4; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f8f9fa; font-weight: bold; }
                tr:hover { background-color: #f5f5f5; }
                .count { color: #666; font-size: 0.9em; }
                .btn { background: #FF69B4; color: white; padding: 10px 20px; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px 5px; cursor: pointer; }
                .btn:hover { background: #E91E63; }
                .btn.green { background: #4CAF50; }
                .btn.green:hover { background: #45a049; }
                .btn.blue { background: #2196F3; }
                .btn.blue:hover { background: #1976D2; }
                .btn.gray { background: #666; }
                .btn.gray:hover { background: #555; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
                .stat-card { background: linear-gradient(135deg, #FF69B4, #9C27B0); color: white; padding: 15px; border-radius: 10px; text-align: center; }
                .stat-number { font-size: 2em; font-weight: bold; }
                .stat-label { font-size: 0.9em; opacity: 0.9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Base de Datos - Miroma</h1>
                
                <div style="text-align: center; margin-bottom: 20px;">
                    <a href="/admin/db" class="btn">Actualizar</a>
                    <a href="/admin/edit" class="btn green">Editor Visual</a>
                    <a href="/admin/sql" class="btn blue">Consultas SQL</a>
                    <a href="/" class="btn gray">Volver a la App</a>
                    <button onclick="toggleAutoRefresh()" class="btn green" id="autoRefreshBtn">Auto-actualizar: OFF</button>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{{ usuarios|length }}</div>
                        <div class="stat-label">Usuarios</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ parejas|length }}</div>
                        <div class="stat-label">Parejas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ gastos_compartidos|length }}</div>
                        <div class="stat-label">Gastos Compartidos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ gastos_personales|length }}</div>
                        <div class="stat-label">Gastos Personales</div>
                    </div>
                </div>
                
                <!-- Usuarios -->
                <div class="table-section">
                    <h2>Usuarios <span class="count">({{ usuarios|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Email</th>
                            <th>Apodo</th>
                            <th>Rol</th>
                            <th>Ingreso Mensual</th>
                            <th>Pareja ID</th>
                            <th>Fecha Registro</th>
                        </tr>
                        {% for usuario in usuarios %}
                        <tr>
                            <td>{{ usuario.id }}</td>
                            <td>{{ usuario.email }}</td>
                            <td>{{ usuario.apodo }}</td>
                            <td>{{ usuario.rol }}</td>
                            <td>${{ "{:,}".format(usuario.ingreso_mensual) if usuario.ingreso_mensual else 'No definido' }}</td>
                            <td>{{ usuario.pareja_id or 'Sin pareja' }}</td>
                            <td>{{ usuario.fecha_registro.strftime('%Y-%m-%d %H:%M') if usuario.fecha_registro else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Parejas -->
                <div class="table-section">
                    <h2>Parejas <span class="count">({{ parejas|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Código Vinculación</th>
                            <th>Usuario 1 ID</th>
                            <th>Usuario 2 ID</th>
                            <th>Fecha Vinculación</th>
                            <th>Activo</th>
                        </tr>
                        {% for pareja in parejas %}
                        <tr>
                            <td>{{ pareja.id }}</td>
                            <td>{{ pareja.codigo_vinculacion }}</td>
                            <td>{{ pareja.usuario1_id }}</td>
                            <td>{{ pareja.usuario2_id }}</td>
                            <td>{{ pareja.fecha_vinculacion.strftime('%Y-%m-%d %H:%M') if pareja.fecha_vinculacion else 'N/A' }}</td>
                            <td>{{ 'Sí' if pareja.activo else 'No' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Gastos Compartidos -->
                <div class="table-section">
                    <h2>Gastos Compartidos <span class="count">({{ gastos_compartidos|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Monto Total</th>
                            <th>Categoría</th>
                            <th>Pareja ID</th>
                            <th>Creado Por</th>
                            <th>Fecha</th>
                        </tr>
                        {% for gasto in gastos_compartidos %}
                        <tr>
                            <td>{{ gasto.id }}</td>
                            <td>{{ gasto.nombre }}</td>
                            <td>${{ "{:,}".format(gasto.monto_total) if gasto.monto_total else '0' }}</td>
                            <td>{{ gasto.categoria }}</td>
                            <td>{{ gasto.pareja_id }}</td>
                            <td>{{ gasto.creado_por }}</td>
                            <td>{{ gasto.fecha.strftime('%Y-%m-%d') if gasto.fecha else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Gastos Personales -->
                <div class="table-section">
                    <h2>Gastos Personales <span class="count">({{ gastos_personales|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Monto</th>
                            <th>Categoría</th>
                            <th>Usuario ID</th>
                            <th>Fecha</th>
                        </tr>
                        {% for gasto in gastos_personales %}
                        <tr>
                            <td>{{ gasto.id }}</td>
                            <td>{{ gasto.nombre }}</td>
                            <td>${{ "{:,}".format(gasto.monto) if gasto.monto else '0' }}</td>
                            <td>{{ gasto.categoria }}</td>
                            <td>{{ gasto.usuario_id }}</td>
                            <td>{{ gasto.fecha.strftime('%Y-%m-%d') if gasto.fecha else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Ahorros -->
                <div class="table-section">
                    <h2>Ahorros <span class="count">({{ ahorros|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Meta Monto</th>
                            <th>Monto Actual</th>
                            <th>Progreso</th>
                            <th>Pareja ID</th>
                            <th>Fecha Objetivo</th>
                        </tr>
                        {% for ahorro in ahorros %}
                        <tr>
                            <td>{{ ahorro.id }}</td>
                            <td>{{ ahorro.nombre }}</td>
                            <td>${{ "{:,}".format(ahorro.meta_monto) if ahorro.meta_monto else '0' }}</td>
                            <td>${{ "{:,}".format(ahorro.monto_actual) if ahorro.monto_actual else '0' }}</td>
                            <td>{{ "%.1f"|format(ahorro.progreso) if ahorro.progreso else '0' }}%</td>
                            <td>{{ ahorro.pareja_id }}</td>
                            <td>{{ ahorro.fecha_objetivo.strftime('%Y-%m-%d') if ahorro.fecha_objetivo else 'Sin fecha' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Planes Futuros -->
                <div class="table-section">
                    <h2>Planes Futuros <span class="count">({{ planes|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Tipo</th>
                            <th>Pareja ID</th>
                            <th>Fecha Creación</th>
                        </tr>
                        {% for plan in planes %}
                        <tr>
                            <td>{{ plan.id }}</td>
                            <td>{{ plan.nombre }}</td>
                            <td>{{ plan.tipo }}</td>
                            <td>{{ plan.pareja_id }}</td>
                            <td>{{ plan.fecha_creacion.strftime('%Y-%m-%d') if plan.fecha_creacion else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <!-- Pendientes -->
                <div class="table-section">
                    <h2>Pendientes <span class="count">({{ pendientes|length }} registros)</span></h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Título</th>
                            <th>Categoría</th>
                            <th>Completado</th>
                            <th>Pareja ID</th>
                            <th>Fecha Creación</th>
                            <th>Recordatorio</th>
                        </tr>
                        {% for pendiente in pendientes %}
                        <tr>
                            <td>{{ pendiente.id }}</td>
                            <td>{{ pendiente.titulo }}</td>
                            <td>{{ pendiente.categoria }}</td>
                            <td>{{ 'Sí' if pendiente.completado else 'No' }}</td>
                            <td>{{ pendiente.pareja_id }}</td>
                            <td>{{ pendiente.fecha_creacion.strftime('%Y-%m-%d') if pendiente.fecha_creacion else 'N/A' }}</td>
                            <td>{{ pendiente.recordatorio.strftime('%Y-%m-%d') if pendiente.recordatorio else 'Sin recordatorio' }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
                <script>
                    let autoRefreshInterval = null;
                    let autoRefreshEnabled = false;
                    
                    function toggleAutoRefresh() {
                        const btn = document.getElementById('autoRefreshBtn');
                        
                        if (autoRefreshEnabled) {
                            clearInterval(autoRefreshInterval);
                            autoRefreshEnabled = false;
                            btn.textContent = 'Auto-actualizar: OFF';
                            btn.className = 'btn green';
                        } else {
                            autoRefreshInterval = setInterval(() => {
                                location.reload();
                            }, 10000);
                            autoRefreshEnabled = true;
                            btn.textContent = 'Auto-actualizar: ON (10s)';
                            btn.className = 'btn';
                        }
                    }
                    
                    document.addEventListener('DOMContentLoaded', function() {
                        const now = new Date().toLocaleTimeString();
                        document.title = `Base de Datos - Actualizado: ${now}`;
                    });
                </script>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(template, 
                                    usuarios=usuarios,
                                    parejas=parejas, 
                                    gastos_compartidos=gastos_compartidos,
                                    gastos_personales=gastos_personales,
                                    ahorros=ahorros,
                                    planes=planes,
                                    pendientes=pendientes)
                                    
    except Exception as e:
        return f"Error al cargar la base de datos: {str(e)}", 500

@bp.route('/sql', methods=['GET', 'POST'])
@login_required 
def ejecutar_sql():
    """Ejecutar consultas SQL personalizadas"""
    
    resultado = None
    error = None
    
    if request.method == 'POST':
        sql_query = request.form.get('sql', '').strip()
        
        if sql_query:
            try:
                result = db.session.execute(text(sql_query))
                
                if sql_query.upper().startswith('SELECT'):
                    rows = result.fetchall()
                    columns = result.keys() if rows else []
                    resultado = {'columns': columns, 'rows': rows}
                else:
                    db.session.commit()
                    resultado = {'message': f'Consulta ejecutada exitosamente. Filas afectadas: {result.rowcount}'}
                    
            except Exception as e:
                error = str(e)
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Consultas SQL - Miroma</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f0f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            h1 { color: #9C27B0; text-align: center; }
            textarea { width: 100%; height: 200px; font-family: monospace; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
            .btn { background: #FF69B4; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; text-decoration: none; display: inline-block; }
            .btn:hover { background: #E91E63; }
            .btn.green { background: #4CAF50; }
            .btn.green:hover { background: #45a049; }
            .btn.blue { background: #2196F3; }
            .btn.blue:hover { background: #1976D2; }
            .btn.gray { background: #666; }
            .btn.gray:hover { background: #555; }
            .btn.red { background: #f44336; }
            .btn.red:hover { background: #da190b; }
            .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
            .error { background: #ffebee; color: #c62828; border: 1px solid #ef5350; }
            .success { background: #e8f5e9; color: #2e7d32; border: 1px solid #4caf50; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; font-weight: bold; }
            tr:hover { background-color: #f5f5f5; }
            .guide { background: #e3f2fd; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .guide h3 { color: #1976d2; margin-top: 0; }
            .guide code { background: white; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
            .quick-actions { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px; margin-bottom: 20px; }
            .quick-btn { padding: 8px 12px; border: none; border-radius: 5px; cursor: pointer; font-size: 0.9em; }
            .example { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 4px solid #2196F3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Consultas SQL</h1>
            
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="/admin/db" class="btn gray">Ver Tablas</a>
                <a href="/admin/edit" class="btn green">Editor Visual</a>
                <a href="/" class="btn gray">Volver a App</a>
            </div>
            
            <div class="guide">
                <h3>Guía de SQL Básico</h3>
                
                <h4>1. Ver datos (SELECT)</h4>
                <div class="example">
                    <code>SELECT * FROM usuarios;</code> - Ver todos los usuarios<br>
                    <code>SELECT email, apodo FROM usuarios;</code> - Ver solo email y apodo<br>
                    <code>SELECT * FROM usuarios WHERE rol = 'esposa';</code> - Solo esposas
                </div>
                
                <h4>2. Modificar datos (UPDATE)</h4>
                <div class="example">
                    <code>UPDATE usuario SET apodo = 'Nuevo Nombre' WHERE id = 1;</code><br>
                    <code>UPDATE usuario SET ingreso_mensual = 2000000 WHERE email = 'user@email.com';</code>
                </div>
                
                <h4>3. Eliminar datos (DELETE)</h4>
                <div class="example">
                    <code>DELETE FROM gasto_personal WHERE id = 1;</code> - Eliminar un gasto<br>
                    <code>DELETE FROM gastos_personales WHERE usuario_id = 1;</code> - Eliminar todos los gastos de un usuario
                </div>
                
                <h4>4. Contar registros</h4>
                <div class="example">
                    <code>SELECT COUNT(*) FROM usuario;</code> - Contar usuarios<br>
                    <code>SELECT COUNT(*) FROM gasto_personal WHERE usuario_id = 1;</code> - Contar gastos de un usuario
                </div>
                
                <h4>5. Consultas de parejas</h4>
                <div class="example">
                    <code>SELECT u1.apodo as usuario1, u2.apodo as usuario2, p.codigo_vinculacion FROM usuario u1 JOIN usuario u2 ON u1.pareja_id = u2.pareja_id JOIN pareja p ON u1.pareja_id = p.id WHERE u1.id < u2.id;</code> - Ver parejas vinculadas<br>
                    <code>SELECT * FROM usuario WHERE pareja_id IS NULL;</code> - Ver usuarios sin pareja<br>
                    <code>SELECT * FROM usuario WHERE pareja_id IS NOT NULL;</code> - Ver usuarios con pareja
                </div>
            </div>
            
            <div class="quick-actions">
                <button class="quick-btn blue" onclick="setQuery('SELECT * FROM usuarios;')">Ver todos los usuarios</button>
                <button class="quick-btn blue" onclick="setQuery('SELECT * FROM gastos_compartidos ORDER BY fecha DESC LIMIT 10;')">Últimos 10 gastos compartidos</button>
                <button class="quick-btn blue" onclick="setQuery('SELECT * FROM gastos_personales ORDER BY fecha DESC LIMIT 10;')">Últimos 10 gastos personales</button>
                <button class="quick-btn blue" onclick="setQuery('SELECT u.apodo, u.email, u.rol, u.ingreso_mensual FROM usuarios u;')">Info básica usuarios</button>
                <button class="quick-btn green" onclick="setQuery('SELECT COUNT(*) as total_usuarios FROM usuarios;')">Contar usuarios</button>
                <button class="quick-btn green" onclick="setQuery('SELECT COUNT(*) as total_gastos FROM gastos_personales;')">Contar gastos personales</button>
                <button class="quick-btn blue" onclick="setQuery('SELECT * FROM usuarios WHERE pareja_id IS NULL;')">Usuarios sin pareja</button>
                <button class="quick-btn blue" onclick="setQuery('SELECT u1.apodo as usuario1, u2.apodo as usuario2, p.codigo_vinculacion FROM usuarios u1 JOIN usuarios u2 ON u1.pareja_id = u2.pareja_id JOIN parejas p ON u1.pareja_id = p.id WHERE u1.id < u2.id;')">Ver parejas vinculadas</button>
                <button class="quick-btn green" onclick="setQuery('SELECT * FROM usuarios ORDER BY fecha_registro DESC LIMIT 5;')">Últimos usuarios creados</button>
            </div>
            
            <form method="POST">
                <label for="sqlQuery"><strong>Escribe tu consulta SQL:</strong></label>
                <textarea name="sql" id="sqlQuery" placeholder="Ejemplo: SELECT * FROM usuarios;">{{ request.form.get('sql', 'SELECT * FROM usuarios;') }}</textarea><br>
                <button type="submit" class="btn">Ejecutar Consulta</button>
                <button type="button" class="btn gray" onclick="document.getElementById('sqlQuery').value = '';">Limpiar</button>
            </form>
            
            {% if error %}
            <div class="result error">
                <h3>Error:</h3>
                <p>{{ error }}</p>
            </div>
            {% endif %}
            
            {% if resultado %}
                {% if resultado.message %}
                <div class="result success">
                    <h3>Éxito:</h3>
                    <p>{{ resultado.message }}</p>
                </div>
                {% else %}
                <div class="result">
                    <h3>Resultados ({{ resultado.rows|length }} filas):</h3>
                    {% if resultado.rows %}
                    <table>
                        <tr>
                            {% for column in resultado.columns %}
                            <th>{{ column }}</th>
                            {% endfor %}
                        </tr>
                        {% for row in resultado.rows %}
                        <tr>
                            {% for value in row %}
                            <td>{{ value if value is not none else 'NULL' }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </table>
                    {% else %}
                    <p>No se encontraron resultados.</p>
                    {% endif %}
                </div>
                {% endif %}
            {% endif %}
        </div>
        
        <script>
            function setQuery(query) {
                document.getElementById('sqlQuery').value = query;
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(template, resultado=resultado, error=error)

@bp.route('/edit')
@login_required
def editor_visual():
    """Editor visual para modificar datos fácilmente"""
    
    usuarios = Usuario.query.all()
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Editor Visual - Miroma</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f0f5; }
            .container { max-width: 1400px; margin: 0 auto; }
            h1 { color: #9C27B0; text-align: center; }
            .section { background: white; margin-bottom: 20px; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { background: #FF69B4; color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; text-decoration: none; display: inline-block; font-size: 0.9em; }
            .btn:hover { background: #E91E63; }
            .btn.danger { background: #f44336; }
            .btn.danger:hover { background: #da190b; }
            .btn.success { background: #4CAF50; }
            .btn.success:hover { background: #45a049; }
            .btn.warning { background: #FF9800; }
            .btn.warning:hover { background: #F57C00; }
            .btn.gray { background: #666; }
            .btn.gray:hover { background: #555; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 12px 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; font-weight: bold; }
            tr:hover { background-color: #f5f5f5; }
            .actions { display: flex; gap: 5px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }
            .stat-card { background: linear-gradient(135deg, #FF69B4, #9C27B0); color: white; padding: 15px; border-radius: 10px; text-align: center; }
            .stat-number { font-size: 1.5em; font-weight: bold; }
            .stat-label { font-size: 0.9em; opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Editor Visual de Base de Datos</h1>
            
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="/admin/db" class="btn gray">Ver Tablas</a>
                <a href="/admin/sql" class="btn gray">Consultas SQL</a>
                <a href="/" class="btn gray">Volver a App</a>
                <button onclick="location.reload()" class="btn success">Actualizar</button>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ usuarios|length }}</div>
                    <div class="stat-label">Usuarios</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Gestión de Usuarios</h2>
                
                <div style="margin-bottom: 15px;">
                    <button onclick="mostrarModalCrearUsuario()" class="btn success">Crear Usuario</button>
                    <button onclick="mostrarModalVincular()" class="btn success">Vincular Pareja</button>
                    <button onclick="limpiarTodosGastos()" class="btn danger">Limpiar Todos los Gastos</button>
                    <button onclick="resetearPasswords()" class="btn warning">Resetear Passwords a "123456"</button>
                    <button onclick="limpiarBaseDatos()" class="btn danger">Limpiar TODA la Base de Datos</button>
                </div>
                
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Email</th>
                        <th>Apodo</th>
                        <th>Rol</th>
                        <th>Ingreso</th>
                        <th>Pareja</th>
                        <th>Acciones</th>
                    </tr>
                    {% for usuario in usuarios %}
                    <tr>
                        <td>{{ usuario.id }}</td>
                        <td>{{ usuario.email }}</td>
                        <td>
                            <input type="text" value="{{ usuario.apodo }}" id="apodo-{{ usuario.id }}" style="width: 100px;">
                        </td>
                        <td>{{ usuario.rol }}</td>
                        <td>
                            <input type="number" value="{{ usuario.ingreso_mensual or 0 }}" id="ingreso-{{ usuario.id }}" style="width: 100px;">
                        </td>
                        <td>{{ usuario.pareja_id or 'Sin pareja' }}</td>
                        <td class="actions">
                            <button onclick="actualizarUsuario({{ usuario.id }})" class="btn success">Guardar</button>
                            <button onclick="cambiarPassword({{ usuario.id }})" class="btn warning">Cambiar Password</button>
                            {% if usuario.pareja_id %}
                            <button onclick="desvincularUsuario({{ usuario.id }})" class="btn warning">Desvincular</button>
                            {% endif %}
                            <button onclick="eliminarUsuario({{ usuario.id }})" class="btn danger">Eliminar</button>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
        
        <script>
            async function actualizarUsuario(userId) {
                const apodo = document.getElementById(`apodo-${userId}`).value;
                const ingreso = document.getElementById(`ingreso-${userId}`).value;
                
                try {
                    const response = await fetch(`/admin/usuario/${userId}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({apodo, ingreso_mensual: parseFloat(ingreso)})
                    });
                    
                    if (response.ok) {
                        alert('Usuario actualizado exitosamente');
                    } else {
                        alert('Error al actualizar usuario');
                    }
                } catch (error) {
                    alert('Error de conexión');
                }
            }
            
            async function eliminarUsuario(userId) {
                if (confirm('¿Estás seguro de eliminar este usuario? Esta acción no se puede deshacer.')) {
                    try {
                        const response = await fetch(`/admin/usuario/${userId}`, {method: 'DELETE'});
                        if (response.ok) {
                            alert('Usuario eliminado');
                            location.reload();
                        } else {
                            alert('Error al eliminar usuario');
                        }
                    } catch (error) {
                        alert('Error de conexión');
                    }
                }
            }
            
            async function cambiarPassword(userId) {
                const newPassword = prompt('Nueva contraseña para el usuario:');
                if (newPassword) {
                    try {
                        const response = await fetch(`/admin/usuario/${userId}/password`, {
                            method: 'PUT',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({password: newPassword})
                        });
                        
                        if (response.ok) {
                            alert('Contraseña cambiada exitosamente');
                        } else {
                            alert('Error al cambiar contraseña');
                        }
                    } catch (error) {
                        alert('Error de conexión');
                    }
                }
            }
            
            async function limpiarBaseDatos() {
                if (confirm('¿ELIMINAR TODOS LOS DATOS? Esta acción es IRREVERSIBLE.')) {
                    if (confirm('ÚLTIMA CONFIRMACIÓN: Se eliminarán TODOS los usuarios, gastos, ahorros, etc.')) {
                        try {
                            const response = await fetch('/admin/limpiar-todo', {method: 'POST'});
                            if (response.ok) {
                                alert('Base de datos limpiada');
                                location.reload();
                            }
                        } catch (error) {
                            alert('Error');
                        }
                    }
                }
            }
            
            async function limpiarTodosGastos() {
                if (confirm('¿Eliminar TODOS los gastos (compartidos y personales)?')) {
                    try {
                        const response = await fetch('/admin/limpiar-gastos', {method: 'POST'});
                        if (response.ok) {
                            alert('Todos los gastos eliminados');
                            location.reload();
                        }
                    } catch (error) {
                        alert('Error');
                    }
                }
            }
            
            async function resetearPasswords() {
                if (confirm('¿Cambiar TODAS las contraseñas a "123456"?')) {
                    try {
                        const response = await fetch('/admin/resetear-passwords', {method: 'POST'});
                        if (response.ok) {
                            alert('Todas las contraseñas cambiadas a "123456"');
                        }
                    } catch (error) {
                        alert('Error');
                    }
                }
            }
            
            function mostrarModalVincular() {
                document.getElementById('modal-vincular').style.display = 'block';
            }
            
            function cerrarModalVincular() {
                document.getElementById('modal-vincular').style.display = 'none';
            }
            
            function mostrarModalCrearUsuario() {
                document.getElementById('modal-crear-usuario').style.display = 'block';
            }
            
            function cerrarModalCrearUsuario() {
                document.getElementById('modal-crear-usuario').style.display = 'none';
                // Limpiar formulario
                document.getElementById('nuevo-email').value = '';
                document.getElementById('nuevo-apodo').value = '';
                document.getElementById('nuevo-password').value = '';
                document.getElementById('nuevo-rol').value = 'esposa';
                document.getElementById('nuevo-ingreso').value = '';
            }
            
            async function vincularPareja() {
                const usuario1Id = document.getElementById('usuario1').value;
                const usuario2Id = document.getElementById('usuario2').value;
                
                if (!usuario1Id || !usuario2Id) {
                    alert('Selecciona ambos usuarios');
                    return;
                }
                
                if (usuario1Id === usuario2Id) {
                    alert('No puedes vincular un usuario consigo mismo');
                    return;
                }
                
                try {
                    const response = await fetch('/admin/vincular-pareja', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({usuario1_id: parseInt(usuario1Id), usuario2_id: parseInt(usuario2Id)})
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        alert('Pareja vinculada exitosamente');
                        cerrarModalVincular();
                        location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    alert('Error de conexión');
                }
            }
            
            async function desvincularUsuario(userId) {
                if (confirm('¿Desvincular este usuario de su pareja?')) {
                    try {
                        const response = await fetch(`/admin/desvincular-usuario/${userId}`, {method: 'POST'});
                        const data = await response.json();
                        
                        if (response.ok) {
                            alert('Usuario desvinculado exitosamente');
                            location.reload();
                        } else {
                            alert('Error: ' + data.error);
                        }
                    } catch (error) {
                        alert('Error de conexión');
                    }
                }
            }
            
            async function crearUsuario() {
                const email = document.getElementById('nuevo-email').value.trim();
                const apodo = document.getElementById('nuevo-apodo').value.trim();
                const password = document.getElementById('nuevo-password').value;
                const rol = document.getElementById('nuevo-rol').value;
                const ingreso = document.getElementById('nuevo-ingreso').value;
                
                // Validaciones
                if (!email || !apodo || !password) {
                    alert('Por favor completa todos los campos obligatorios (Email, Apodo, Contraseña)');
                    return;
                }
                
                if (password.length < 6) {
                    alert('La contraseña debe tener al menos 6 caracteres');
                    return;
                }
                
                // Validar formato de email
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(email)) {
                    alert('Por favor ingresa un email válido');
                    return;
                }
                
                try {
                    const response = await fetch('/admin/crear-usuario', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            email: email,
                            apodo: apodo,
                            password: password,
                            rol: rol,
                            ingreso_mensual: ingreso ? parseFloat(ingreso) : null
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        alert('Usuario creado exitosamente');
                        cerrarModalCrearUsuario();
                        location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    alert('Error de conexión');
                }
            }
        </script>
        
        <!-- Modal para Vincular Pareja -->
        <div id="modal-vincular" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
            <div style="background-color: white; margin: 5% auto; padding: 20px; border-radius: 10px; width: 80%; max-width: 600px;">
                <h2>Vincular Pareja</h2>
                <p>Selecciona dos usuarios para vincular como pareja:</p>
                
                <div style="margin-bottom: 15px;">
                    <label>Usuario 1:</label>
                    <select id="usuario1" style="width: 100%; padding: 8px; margin-top: 5px;">
                        <option value="">Seleccionar usuario...</option>
                        {% for usuario in usuarios %}
                        <option value="{{ usuario.id }}">{{ usuario.apodo }} ({{ usuario.email }}) - {{ usuario.rol }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Usuario 2:</label>
                    <select id="usuario2" style="width: 100%; padding: 8px; margin-top: 5px;">
                        <option value="">Seleccionar usuario...</option>
                        {% for usuario in usuarios %}
                        <option value="{{ usuario.id }}">{{ usuario.apodo }} ({{ usuario.email }}) - {{ usuario.rol }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <button onclick="vincularPareja()" class="btn success">Vincular Pareja</button>
                    <button onclick="cerrarModalVincular()" class="btn gray">Cancelar</button>
                </div>
            </div>
        </div>
        
        <!-- Modal para Crear Usuario -->
        <div id="modal-crear-usuario" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
            <div style="background-color: white; margin: 5% auto; padding: 20px; border-radius: 10px; width: 80%; max-width: 600px;">
                <h2>Crear Nuevo Usuario</h2>
                <p>Completa los datos del nuevo usuario:</p>
                
                <div style="margin-bottom: 15px;">
                    <label>Email:</label>
                    <input type="email" id="nuevo-email" style="width: 100%; padding: 8px; margin-top: 5px;" placeholder="usuario@email.com" required>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Apodo:</label>
                    <input type="text" id="nuevo-apodo" style="width: 100%; padding: 8px; margin-top: 5px;" placeholder="Nombre del usuario" required>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Contraseña:</label>
                    <input type="password" id="nuevo-password" style="width: 100%; padding: 8px; margin-top: 5px;" placeholder="Contraseña" required>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Rol:</label>
                    <select id="nuevo-rol" style="width: 100%; padding: 8px; margin-top: 5px;">
                        <option value="esposa">Esposa</option>
                        <option value="esposo">Esposo</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Ingreso Mensual (opcional):</label>
                    <input type="number" id="nuevo-ingreso" style="width: 100%; padding: 8px; margin-top: 5px;" placeholder="2000000" min="0" step="100000">
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <button onclick="crearUsuario()" class="btn success">Crear Usuario</button>
                    <button onclick="cerrarModalCrearUsuario()" class="btn gray">Cancelar</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, usuarios=usuarios)

# Rutas de API para el editor
@bp.route('/usuario/<int:user_id>', methods=['PUT'])
@login_required
def actualizar_usuario(user_id):
    try:
        data = request.get_json()
        usuario = Usuario.query.get_or_404(user_id)
        
        if 'apodo' in data:
            usuario.apodo = data['apodo']
        if 'ingreso_mensual' in data:
            usuario.ingreso_mensual = data['ingreso_mensual']
            
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/usuario/<int:user_id>', methods=['DELETE'])
@login_required
def eliminar_usuario(user_id):
    try:
        usuario = Usuario.query.get_or_404(user_id)
        
        # Eliminar gastos personales
        GastoPersonal.query.filter_by(usuario_id=user_id).delete()
        
        # Si tiene pareja, eliminar datos compartidos
        if usuario.pareja_id:
            GastoCompartido.query.filter_by(pareja_id=usuario.pareja_id).delete()
            Ahorro.query.filter_by(pareja_id=usuario.pareja_id).delete()
            PlanFuturo.query.filter_by(pareja_id=usuario.pareja_id).delete()
            Pendiente.query.filter_by(pareja_id=usuario.pareja_id).delete()
            
            # Eliminar pareja si no hay otros usuarios
            otros_usuarios = Usuario.query.filter_by(pareja_id=usuario.pareja_id).filter(Usuario.id != user_id).count()
            if otros_usuarios == 0:
                Pareja.query.filter_by(id=usuario.pareja_id).delete()
        
        # Eliminar usuario
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/usuario/<int:user_id>/password', methods=['PUT'])
@login_required
def cambiar_password_usuario(user_id):
    try:
        data = request.get_json()
        usuario = Usuario.query.get_or_404(user_id)
        
        usuario.password_hash = generate_password_hash(data['password'])
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/limpiar-todo', methods=['POST'])
@login_required
def limpiar_todo():
    try:
        GastoCompartido.query.delete()
        GastoPersonal.query.delete()
        Ahorro.query.delete()
        PlanFuturo.query.delete()
        Pendiente.query.delete()
        Usuario.query.delete()
        Pareja.query.delete()
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/limpiar-gastos', methods=['POST'])
@login_required
def limpiar_gastos():
    try:
        GastoCompartido.query.delete()
        GastoPersonal.query.delete()
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/resetear-passwords', methods=['POST'])
@login_required
def resetear_passwords():
    try:
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            usuario.password_hash = generate_password_hash('123456')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/vincular-pareja', methods=['POST'])
@login_required
def vincular_pareja():
    try:
        data = request.get_json()
        usuario1_id = data.get('usuario1_id')
        usuario2_id = data.get('usuario2_id')
        
        # Validar que los usuarios existan
        usuario1 = Usuario.query.get_or_404(usuario1_id)
        usuario2 = Usuario.query.get_or_404(usuario2_id)
        
        # Verificar que no estén ya vinculados
        if usuario1.pareja_id or usuario2.pareja_id:
            return jsonify({'error': 'Uno o ambos usuarios ya están vinculados a una pareja'}), 400
        
        # Crear nueva pareja usando el método estático para generar código
        nueva_pareja = Pareja(
            codigo_vinculacion=Pareja.generar_codigo(),
            usuario1_id=usuario1_id,
            usuario2_id=usuario2_id,
            fecha_vinculacion=datetime.utcnow(),
            activo=True
        )
        
        db.session.add(nueva_pareja)
        db.session.flush()  # Para obtener el ID de la pareja
        
        # Vincular usuarios a la pareja
        usuario1.pareja_id = nueva_pareja.id
        usuario2.pareja_id = nueva_pareja.id
        
        db.session.commit()
        
        return jsonify({'success': True, 'pareja_id': nueva_pareja.id, 'codigo': nueva_pareja.codigo_vinculacion})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/desvincular-usuario/<int:user_id>', methods=['POST'])
@login_required
def desvincular_usuario(user_id):
    try:
        usuario = Usuario.query.get_or_404(user_id)
        
        if not usuario.pareja_id:
            return jsonify({'error': 'El usuario no está vinculado a ninguna pareja'}), 400
        
        pareja_id = usuario.pareja_id
        
        # Buscar si hay otro usuario vinculado a la misma pareja
        otros_usuarios = Usuario.query.filter_by(pareja_id=pareja_id).filter(Usuario.id != user_id).all()
        
        # Desvincular el usuario
        usuario.pareja_id = None
        
        # Si no hay otros usuarios vinculados a esta pareja, eliminar la pareja
        if not otros_usuarios:
            pareja = Pareja.query.get(pareja_id)
            if pareja:
                # Eliminar datos compartidos de la pareja
                GastoCompartido.query.filter_by(pareja_id=pareja_id).delete()
                Ahorro.query.filter_by(pareja_id=pareja_id).delete()
                PlanFuturo.query.filter_by(pareja_id=pareja_id).delete()
                Pendiente.query.filter_by(pareja_id=pareja_id).delete()
                
                db.session.delete(pareja)
        else:
            # Si hay otros usuarios, solo desvincular este usuario pero mantener la pareja
            for otro_usuario in otros_usuarios:
                otro_usuario.pareja_id = None
            
            # Eliminar la pareja y sus datos compartidos
            pareja = Pareja.query.get(pareja_id)
            if pareja:
                GastoCompartido.query.filter_by(pareja_id=pareja_id).delete()
                Ahorro.query.filter_by(pareja_id=pareja_id).delete()
                PlanFuturo.query.filter_by(pareja_id=pareja_id).delete()
                Pendiente.query.filter_by(pareja_id=pareja_id).delete()
                
                db.session.delete(pareja)
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/crear-usuario', methods=['POST'])
@login_required
def crear_usuario():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        email = data.get('email', '').strip()
        apodo = data.get('apodo', '').strip()
        password = data.get('password', '')
        rol = data.get('rol', 'esposa')
        ingreso_mensual = data.get('ingreso_mensual')
        
        if not email or not apodo or not password:
            return jsonify({'error': 'Email, apodo y contraseña son obligatorios'}), 400
        
        # Verificar que el email no exista
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({'error': 'Ya existe un usuario con este email'}), 400
        
        # Validar rol
        if rol not in ['esposa', 'esposo']:
            return jsonify({'error': 'Rol debe ser "esposa" o "esposo"'}), 400
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            email=email,
            apodo=apodo,
            rol=rol,
            password_hash=generate_password_hash(password),
            ingreso_mensual=ingreso_mensual if ingreso_mensual else None
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'usuario_id': nuevo_usuario.id,
            'message': f'Usuario {apodo} creado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500