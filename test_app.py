#!/usr/bin/env python3
"""
Script de prueba para Miroma App
Crea usuarios de ejemplo y datos de prueba
"""
from app import create_app, db
from app.models import Usuario, Pareja, GastoCompartido, Ahorro, PlanFuturo, ItemPlan, Pendiente
from datetime import datetime

def crear_datos_prueba():
    """Crear datos de prueba"""
    app = create_app()
    
    with app.app_context():
        # Limpiar base de datos
        db.drop_all()
        db.create_all()
        
        print("✅ Base de datos inicializada")
        
        # Crear usuarios
        usuario1 = Usuario(
            email='maria@ejemplo.com',
            apodo='María',
            rol='esposa',
            ingreso_mensual=2000000
        )
        usuario1.set_password('password123')
        
        usuario2 = Usuario(
            email='juan@ejemplo.com',
            apodo='Juan',
            rol='esposo',
            ingreso_mensual=1000000
        )
        usuario2.set_password('password123')
        
        db.session.add(usuario1)
        db.session.add(usuario2)
        db.session.commit()
        
        print(f"✅ Usuarios creados:")
        print(f"   - {usuario1.email} / password123")
        print(f"   - {usuario2.email} / password123")
        
        # Crear pareja
        pareja = Pareja(
            codigo_vinculacion=Pareja.generar_codigo(),
            usuario1_id=usuario1.id,
            usuario2_id=usuario2.id,
            activo=True,
            fecha_vinculacion=datetime.utcnow()
        )
        
        db.session.add(pareja)
        db.session.commit()
        
        # Actualizar usuarios con pareja_id
        usuario1.pareja_id = pareja.id
        usuario2.pareja_id = pareja.id
        db.session.commit()
        
        print(f"✅ Pareja vinculada (código: {pareja.codigo_vinculacion})")
        
        # Crear gastos compartidos
        from app.services import CalculadoraAportes
        
        gastos_data = [
            {'nombre': 'Arriendo', 'monto': 1000000, 'categoria': 'hogar'},
            {'nombre': 'Mercado', 'monto': 300000, 'categoria': 'comida'},
            {'nombre': 'Servicios', 'monto': 150000, 'categoria': 'hogar'},
        ]
        
        for gasto_data in gastos_data:
            aportes = CalculadoraAportes.calcular_aportes(
                usuario1.ingreso_mensual,
                usuario2.ingreso_mensual,
                gasto_data['monto']
            )
            
            gasto = GastoCompartido(
                pareja_id=pareja.id,
                nombre=gasto_data['nombre'],
                monto_total=gasto_data['monto'],
                categoria=gasto_data['categoria'],
                creado_por=usuario1.id,
                aporte_usuario1=aportes['aporte_usuario1'],
                aporte_usuario2=aportes['aporte_usuario2']
            )
            db.session.add(gasto)
        
        db.session.commit()
        print(f"✅ {len(gastos_data)} gastos compartidos creados")
        
        # Crear meta de ahorro
        ahorro = Ahorro(
            pareja_id=pareja.id,
            nombre='Luna de Miel en Cartagena',
            meta_monto=5000000,
            monto_actual=2000000
        )
        db.session.add(ahorro)
        db.session.commit()
        
        print("✅ Meta de ahorro creada")
        
        # Crear plan futuro
        plan = PlanFuturo(
            pareja_id=pareja.id,
            nombre='Viaje a Cartagena',
            tipo='viaje'
        )
        db.session.add(plan)
        db.session.flush()
        
        # Agregar items al plan
        items_data = [
            {'nombre': 'Vuelos', 'monto': 800000},
            {'nombre': 'Hotel', 'monto': 600000},
            {'nombre': 'Comidas', 'monto': 400000},
        ]
        
        for item_data in items_data:
            aportes = CalculadoraAportes.calcular_aportes(
                usuario1.ingreso_mensual,
                usuario2.ingreso_mensual,
                item_data['monto']
            )
            
            item = ItemPlan(
                plan_id=plan.id,
                nombre=item_data['nombre'],
                monto_estimado=item_data['monto'],
                estado='pendiente',
                aporte_usuario1=aportes['aporte_usuario1'],
                aporte_usuario2=aportes['aporte_usuario2']
            )
            db.session.add(item)
        
        db.session.commit()
        print(f"✅ Plan futuro creado con {len(items_data)} items")
        
        # Crear pendientes
        pendientes_data = [
            {'titulo': 'Comprar muebles sala', 'categoria': 'hogar'},
            {'titulo': 'Renovar SOAT', 'categoria': 'tramites'},
            {'titulo': 'Planear aniversario', 'categoria': 'eventos'},
        ]
        
        for pend_data in pendientes_data:
            pendiente = Pendiente(
                pareja_id=pareja.id,
                titulo=pend_data['titulo'],
                categoria=pend_data['categoria'],
                creado_por=usuario1.id
            )
            db.session.add(pendiente)
        
        db.session.commit()
        print(f"✅ {len(pendientes_data)} pendientes creados")
        
        print("\n" + "="*50)
        print("🎉 ¡Datos de prueba creados exitosamente!")
        print("="*50)
        print("\n📱 Ahora puedes:")
        print("1. Ejecutar: python run.py")
        print("2. Abrir: http://localhost:5000")
        print("3. Login con:")
        print("   - maria@ejemplo.com / password123")
        print("   - juan@ejemplo.com / password123")
        print("\n💡 Cada usuario verá solo su parte en los gastos compartidos")
        print("   (Sistema 70/30 basado en ingresos)")

if __name__ == '__main__':
    crear_datos_prueba()
