#!/usr/bin/env python3
"""
Script para crear iconos para la PWA de Miroma
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    print("✅ PIL instalado")
except ImportError:
    print("❌ PIL no está instalado. Instalando...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'Pillow'])
    from PIL import Image, ImageDraw, ImageFont
    print("✅ PIL instalado exitosamente")

def crear_icono(size, filename):
    """Crear un icono con gradiente y emoji"""
    # Crear imagen con gradiente rosa-morado
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # Gradiente de rosa a morado
    for y in range(size):
        # Interpolación de color
        ratio = y / size
        r = int(255 * (1 - ratio) + 156 * ratio)  # 255 (rosa) -> 156 (morado)
        g = int(105 * (1 - ratio) + 39 * ratio)   # 105 (rosa) -> 39 (morado)
        b = int(180 * (1 - ratio) + 176 * ratio)  # 180 (rosa) -> 176 (morado)
        draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b))
    
    # Agregar círculo blanco en el centro
    circle_size = int(size * 0.7)
    circle_pos = (size - circle_size) // 2
    draw.ellipse(
        [(circle_pos, circle_pos), (circle_pos + circle_size, circle_pos + circle_size)],
        fill='white'
    )
    
    # Agregar texto
    try:
        # Intentar usar una fuente del sistema
        font_size = int(size * 0.3)
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            # Usar fuente por defecto
            font = ImageFont.load_default()
    
    # Texto "M" en el centro
    text = "💜"
    
    # Calcular posición del texto para centrarlo
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        text_width = size // 3
        text_height = size // 3
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    
    # Dibujar texto
    draw.text((text_x, text_y), text, fill='#9C27B0', font=font)
    
    # Guardar imagen
    img.save(f'app/static/{filename}')
    print(f"✅ Creado: app/static/{filename} ({size}x{size})")

if __name__ == '__main__':
    print("🎨 Creando iconos para Miroma PWA...")
    print()
    
    # Crear iconos de diferentes tamaños
    crear_icono(192, 'icon-192.png')
    crear_icono(512, 'icon-512.png')
    
    print()
    print("✅ ¡Iconos creados exitosamente!")
    print()
    print("📱 Ahora puedes:")
    print("1. Ejecutar: python run.py")
    print("2. Abrir en tu celular: http://TU_IP:3000/static/index.html")
    print("3. Instalar como PWA desde el menú del navegador")
    print()
    print("💡 Tip: Para encontrar tu IP local:")
    print("   Mac/Linux: ifconfig | grep 'inet '")
    print("   Windows: ipconfig")
