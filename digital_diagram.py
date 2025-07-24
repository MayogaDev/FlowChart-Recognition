from graphviz import Digraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY

def generar_explicacion(lineas):
    explicacion = []
    acciones = {
        'ADELANTE': 'Avanzará',
        'IZQUIERDA': 'Girará a la izquierda',
        'DERECHA': 'Girará a la derecha'
    }
    
    for linea in lineas[1:-1]:  # Excluye INICIO y FIN
        partes = linea.split()
        comando = partes[0]
        repeticion = partes[1] if len(partes) > 1 else '1'
        
        if comando in acciones:
            accion = acciones[comando]
            if int(repeticion) > 1:
                explicacion.append(f"- {accion} {repeticion} veces")
            else:
                explicacion.append(f"- {accion} {repeticion} vez")
    
    # Convertimos a texto con saltos de línea
    texto_explicacion = "Secuencia de movimientos del robot:\n\n" + "\n".join(explicacion) + "\n\nEl robot ha llegado a su destino."
    return texto_explicacion.split('\n')  # Devolvemos como lista de líneas

def crear_pdf(diagrama_path, explicacion, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    styles = getSampleStyleSheet()

    # Creamos un estilo personalizado para mantener saltos de línea
    estilo_explicacion = ParagraphStyle(
        name='Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )

    story = []
    
    # Título
    story.append(Paragraph("Diagrama de Flujo del Robot", styles['Title']))
    story.append(Spacer(1, 0.25 * inch))
    
    # Diagrama
    img = Image(diagrama_path, width=4*inch, height=6*inch)
    story.append(img)
    story.append(Spacer(1, 0.5 * inch))
    
    # Explicación
    story.append(Paragraph("Explicación:", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))

    # Añadimos cada línea como párrafo separado
    for linea in explicacion:
        if linea.strip():  # Solo añadimos líneas con contenido
            story.append(Paragraph(linea, estilo_explicacion))
        else:
            story.append(Spacer(1, 0.2 * inch))
    
    doc.build(story)

def generar_diagrama(archivo_txt, archivo_salida):
    with open(archivo_txt, 'r') as f:
        lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
    
    dot = Digraph()
    dot.attr(rankdir='TB')  # Diagrama vertical
    dot.attr('graph', bgcolor='white', ranksep='0.8')
    dot.attr('node', fontname='Arial', fontsize='12', shape='box',
            style='filled', fillcolor='#F5F5F5', color="#000000")
    
    # Estilo especial para INICIO/FIN
    dot.node('INICIO', 'INICIO', shape='ellipse', style='filled',
            fillcolor='#E0E0E0', color="#000000", penwidth='2')
    dot.node('FIN', 'FIN', shape='ellipse', style='filled',
            fillcolor='#E0E0E0', color="#000000", penwidth='2')
    
    previous_node = 'INICIO'
    node_counter = 0
    
    for linea in lineas[1:-1]:  # Excluye INICIO y FIN
        node_counter += 1
        partes = linea.split()
        comando = partes[0]
        node_id = f'nodo_{node_counter}'
        
        if len(partes) > 1:  # Comando con repetición
            repeticion = partes[1]
            label = f"{comando}"
            dot.node(node_id, label, shape='box', style='filled',
                   fillcolor='#FAFAFA', color="#000000")
            
            # Conexión principal
            dot.edge(previous_node, node_id)
            
            # Auto-conexión (bucle)
            dot.edge(node_id, node_id, label=f" x{repeticion}",
                    fontsize='10', color="#000000", arrowhead='vee',
                    constraint='false')
            
            previous_node = node_id
        else:
            dot.node(node_id, comando)
            dot.edge(previous_node, node_id)
            previous_node = node_id
    
    # Conexión al FIN
    dot.edge(previous_node, 'FIN')
    
    # Ajustes finales
    dot.attr('edge', color="#000000", arrowhead='vee', penwidth='1.5')
    diagrama_path = f"{archivo_salida}.png"
    dot.render(archivo_salida, view=True, cleanup=True, format='png')
    
    # Generar explicación
    lineas_explicacion  = generar_explicacion(lineas)
    
    # Crear PDF
    crear_pdf(diagrama_path, lineas_explicacion, f"{archivo_salida}.pdf")
    print(f"PDF generado: {archivo_salida}.pdf")

if __name__ == "__main__":
    generar_diagrama('resultado_diagrama.txt', 'RobotFlowchart')