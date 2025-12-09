from decimal import Decimal, ROUND_HALF_UP

class CalculadoraAportes:
    """Servicio para calcular aportes según el sistema 70/30"""
    
    @staticmethod
    def calcular_aportes(ingreso_usuario1, ingreso_usuario2, monto_total):
        """
        Calcula los aportes de cada usuario según sus ingresos.
        
        Args:
            ingreso_usuario1: Ingreso mensual del usuario 1
            ingreso_usuario2: Ingreso mensual del usuario 2
            monto_total: Monto total del gasto
            
        Returns:
            dict: {'aporte_usuario1': float, 'aporte_usuario2': float}
        """
        # Convertir a Decimal para precisión
        ing1 = Decimal(str(ingreso_usuario1))
        ing2 = Decimal(str(ingreso_usuario2))
        monto = Decimal(str(monto_total))
        
        total_ingresos = ing1 + ing2
        
        # Si no hay ingresos, dividir 50/50
        if total_ingresos == 0:
            mitad = (monto / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return {
                'aporte_usuario1': float(mitad),
                'aporte_usuario2': float(mitad)
            }
        
        # Calcular porcentajes
        porcentaje_usuario1 = ing1 / total_ingresos
        porcentaje_usuario2 = ing2 / total_ingresos
        
        # Calcular aportes
        aporte1 = (monto * porcentaje_usuario1).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        aporte2 = (monto * porcentaje_usuario2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Ajustar para que sumen exactamente el monto total
        diferencia = monto - (aporte1 + aporte2)
        if diferencia != 0:
            aporte1 += diferencia
        
        return {
            'aporte_usuario1': float(aporte1),
            'aporte_usuario2': float(aporte2)
        }
    
    @staticmethod
    def calcular_semaforo_financiero(gastos_mes, ingreso_usuario):
        """
        Calcula el estado del semáforo financiero.
        
        Args:
            gastos_mes: Total de gastos del mes
            ingreso_usuario: Ingreso mensual del usuario
            
        Returns:
            dict: {'estado': str, 'porcentaje': float, 'mensaje': str}
        """
        if ingreso_usuario == 0:
            return {
                'estado': 'rojo',
                'porcentaje': 100,
                'mensaje': 'Configura tu ingreso mensual'
            }
        
        porcentaje_gastado = (gastos_mes / ingreso_usuario) * 100
        
        if porcentaje_gastado < 70:
            return {
                'estado': 'verde',
                'porcentaje': round(porcentaje_gastado, 2),
                'mensaje': '¡Van muy bien este mes! 💚'
            }
        elif porcentaje_gastado < 90:
            return {
                'estado': 'amarillo',
                'porcentaje': round(porcentaje_gastado, 2),
                'mensaje': 'Cuidado, cerca del límite 🟡'
            }
        else:
            return {
                'estado': 'rojo',
                'porcentaje': round(porcentaje_gastado, 2),
                'mensaje': 'Presupuesto excedido 🔴'
            }
