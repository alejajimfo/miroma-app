#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación Miroma
"""
from app import create_app, db
from app.models import Usuario, Pareja, GastoCompartido, GastoPersonal, Ahorro, PlanFuturo, Pendiente

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Contexto para Flask shell"""
    return {
        'db': db,
        'Usuario': Usuario,
        'Pareja': Pareja,
        'GastoCompartido': GastoCompartido,
        'GastoPersonal': GastoPersonal,
        'Ahorro': Ahorro,
        'PlanFuturo': PlanFuturo,
        'Pendiente': Pendiente,
    }

@app.route('/')
def index():
    """Ruta principal - redirige directamente a la app"""
    from flask import redirect
    return redirect('/static/index.html')

@app.route('/api/docs')
def api_docs():
    """Documentación de la API"""
    return '''
    <html>
        <head>
            <title>Miroma API - Documentación</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #F7E7CE;
                    padding: 20px;
                    max-width: 1200px;
                    margin: 0 auto;
                }
                h1, h2 { color: #4CAF50; }
                .endpoint {
                    background: white;
                    padding: 20px;
                    margin: 10px 0;
                    border-radius: 10px;
                    border-left: 4px solid #4CAF50;
                }
                .method {
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 5px;
                    color: white;
                    font-weight: bold;
                    margin-right: 10px;
                }
                .get { background-color: #4CAF50; }
                .post { background-color: #2196F3; }
                .put { background-color: #FF9800; }
                .delete { background-color: #F44336; }
            </style>
        </head>
        <body>
            <h1>📚 Miroma API - Documentación</h1>
            
            <h2>🔐 Autenticación</h2>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/auth/registro</strong>
                <p>Registrar nuevo usuario</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/auth/login</strong>
                <p>Iniciar sesión</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/auth/generar-codigo</strong>
                <p>Generar código de vinculación</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/auth/vincular</strong>
                <p>Vincular con pareja usando código</p>
            </div>
            
            <h2>💰 Gastos</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/gastos/compartidos</strong>
                <p>Listar gastos compartidos</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/gastos/compartidos</strong>
                <p>Crear gasto compartido</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/gastos/personales</strong>
                <p>Listar gastos personales</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/gastos/personales</strong>
                <p>Crear gasto personal</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/gastos/semaforo</strong>
                <p>Obtener estado del semáforo financiero</p>
            </div>
            
            <h2>💵 Ahorros</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/ahorros/</strong>
                <p>Listar metas de ahorro</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/ahorros/</strong>
                <p>Crear meta de ahorro</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/ahorros/{id}/aportar</strong>
                <p>Agregar aporte a meta</p>
            </div>
            
            <h2>🎯 Planes</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/planes/</strong>
                <p>Listar planes futuros</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/planes/</strong>
                <p>Crear plan futuro</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/planes/{id}/items</strong>
                <p>Agregar item a plan</p>
            </div>
            
            <h2>📋 Pendientes</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/pendientes/</strong>
                <p>Listar pendientes</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/pendientes/</strong>
                <p>Crear pendiente</p>
            </div>
            <div class="endpoint">
                <span class="method put">PUT</span>
                <strong>/pendientes/{id}/completar</strong>
                <p>Marcar como completado</p>
            </div>
            
            <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">← Volver al inicio</a>
        </body>
    </html>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
