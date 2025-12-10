from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from app import db
from app.models import GastoCompartido, GastoPersonal, Ahorro, PlanFuturo, Pendiente, Usuario, Pareja

bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@bp.route('/pdf', methods=['GET'])
@login_required
def generar_pdf():
    """Generar PDF con resumen financiero"""
    
    # Crear buffer para el PDF
    buffer = BytesIO()
    
    # Crear documento
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#FF69B4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#4A9EFF'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Título
    elements.append(Paragraph("💜 Miroma - Reporte Financiero", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del usuario
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f"<b>Usuario:</b> {current_user.apodo} ({current_user.rol})", styles['Normal']))
    elements.append(Paragraph(f"<b>Fecha:</b> {fecha_actual}", styles['Normal']))
    elements.append(Paragraph(f"<b>Ingreso Mensual:</b> ${current_user.ingreso_mensual:,.0f}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de pareja
    if current_user.pareja_id:
        pareja = Pareja.query.get(current_user.pareja_id)
        if pareja:
            otro_usuario_id = pareja.usuario2_id if pareja.usuario1_id == current_user.id else pareja.usuario1_id
            otro_usuario = Usuario.query.get(otro_usuario_id)
            if otro_usuario:
                elements.append(Paragraph(f"<b>Pareja:</b> {otro_usuario.apodo}", styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
    
    # Gastos Compartidos
    if current_user.pareja_id:
        elements.append(Paragraph("💰 Gastos Compartidos", heading_style))
        gastos_compartidos = GastoCompartido.query.filter_by(pareja_id=current_user.pareja_id).order_by(GastoCompartido.fecha.desc()).limit(20).all()
        
        if gastos_compartidos:
            data = [['Fecha', 'Nombre', 'Categoría', 'Total', 'Tu Parte']]
            for g in gastos_compartidos:
                pareja = Pareja.query.get(g.pareja_id)
                mi_aporte = g.aporte_usuario1 if pareja.usuario1_id == current_user.id else g.aporte_usuario2
                data.append([
                    g.fecha.strftime('%d/%m/%Y'),
                    g.nombre[:20],
                    g.categoria.capitalize(),
                    f'${g.monto_total:,.0f}',
                    f'${mi_aporte:,.0f}'
                ])
            
            table = Table(data, colWidths=[1*inch, 2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF69B4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            # Total
            total_compartidos = sum(g.aporte_usuario1 if pareja.usuario1_id == current_user.id else g.aporte_usuario2 for g in gastos_compartidos)
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f"<b>Total Gastos Compartidos:</b> ${total_compartidos:,.0f}", styles['Normal']))
        else:
            elements.append(Paragraph("No hay gastos compartidos registrados", styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
    
    # Gastos Personales
    elements.append(Paragraph("🛍️ Gastos Personales", heading_style))
    gastos_personales = GastoPersonal.query.filter_by(usuario_id=current_user.id).order_by(GastoPersonal.fecha.desc()).limit(20).all()
    
    if gastos_personales:
        data = [['Fecha', 'Nombre', 'Categoría', 'Monto']]
        for g in gastos_personales:
            data.append([
                g.fecha.strftime('%d/%m/%Y'),
                g.nombre[:30],
                g.categoria.capitalize(),
                f'${g.monto:,.0f}'
            ])
        
        table = Table(data, colWidths=[1.2*inch, 2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A9EFF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        # Total
        total_personales = sum(g.monto for g in gastos_personales)
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Total Gastos Personales:</b> ${total_personales:,.0f}", styles['Normal']))
    else:
        elements.append(Paragraph("No hay gastos personales registrados", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Ahorros
    elements.append(Paragraph("💵 Ahorros", heading_style))
    ahorros = Ahorro.query.filter_by(pareja_id=current_user.pareja_id).all() if current_user.pareja_id else []
    
    if ahorros:
        data = [['Meta', 'Objetivo', 'Ahorrado', 'Progreso']]
        for a in ahorros:
            progreso = (a.monto_actual / a.meta_monto * 100) if a.meta_monto > 0 else 0
            data.append([
                a.nombre[:25],
                f'${a.meta_monto:,.0f}',
                f'${a.monto_actual:,.0f}',
                f'{progreso:.1f}%'
            ])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00C853')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No hay metas de ahorro registradas", styles['Normal']))
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("_" * 80, styles['Normal']))
    elements.append(Paragraph("Generado por Miroma - App para Parejas 💑", ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)))
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    filename = f"miroma_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@bp.route('/eliminar-todo', methods=['POST'])
@login_required
def eliminar_todo():
    """Eliminar todos los datos financieros del mes/periodo"""
    
    try:
        # Eliminar gastos personales
        GastoPersonal.query.filter_by(usuario_id=current_user.id).delete()
        
        # Eliminar gastos compartidos de la pareja
        if current_user.pareja_id:
            GastoCompartido.query.filter_by(pareja_id=current_user.pareja_id).delete()
            
            # Eliminar ahorros
            Ahorro.query.filter_by(pareja_id=current_user.pareja_id).delete()
            
            # Eliminar planes
            PlanFuturo.query.filter_by(pareja_id=current_user.pareja_id).delete()
            
            # Eliminar pendientes
            Pendiente.query.filter_by(pareja_id=current_user.pareja_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Todos los datos financieros han sido eliminados exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar datos: {str(e)}'}), 500
