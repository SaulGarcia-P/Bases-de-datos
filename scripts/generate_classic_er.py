import os
from graphviz import Graph

def generar_diagrama_formal_ds3():
    # Motor 'dot' para diseño jerárquico y estructurado
    dot = Graph('EER_Health_Formal', engine='dot', format='png')
    
    # Configuración de diseño formal (estilo académico)
    dot.attr(rankdir='TB', splines='false', nodesep='0.6', ranksep='0.8')
    dot.attr('node', fontname='Helvetica', fontsize='11', color='black', fillcolor='white', style='filled', penwidth='1.2')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='black', dir='none', penwidth='1.0')

    # ================= ENTIDADES (Rectángulos) =================
    dot.attr('node', shape='box')
    dot.node('PATIENTS', 'Pacientes\n(PATIENTS)')
    dot.node('HOSPITALS', 'Hospitales\n(HOSPITALS)')
    dot.node('ICUS', 'Unidades UCI\n(ICUS)')
    dot.node('ENCOUNTERS', 'Encuentros Médicos\n(ENCOUNTERS)')

    # ================= RELACIONES (Rombos) =================
    dot.attr('node', shape='diamond')
    dot.node('r_pat', 'registra')
    dot.node('r_hos', 'recibe')
    dot.node('r_icu', 'asigna')

    # ================= ATRIBUTOS (Óvalos) =================
    dot.attr('node', shape='ellipse')
    
    # Atributos de Pacientes
    dot.node('p_id', '< <U>patient_id</U> >')
    dot.node('p_age', 'age')
    dot.node('p_gen', 'gender')
    dot.node('p_eth', 'ethnicity')
    dot.node('p_hgt', 'height')
    
    # Atributos de Hospitales
    dot.node('h_id', '< <U>hospital_id</U> >')
    
    # Atributos de ICUs
    dot.node('i_id', '< <U>icu_id</U> >')
    dot.node('i_type', 'icu_type')
    dot.node('i_stype', 'icu_stay_type')
    
    # Atributos de Encuentros Médicos (Omitimos las +70 variables por limpieza visual)
    dot.node('e_id', '< <U>encounter_id</U> >')
    dot.node('e_bmi', 'bmi')
    dot.node('e_wt', 'weight')
    dot.node('e_death', 'hospital_death')

    # ================= CONEXIONES Y LÍNEAS =================
    
    # 1. Unir Entidades con sus Atributos
    dot.edges([
        ('PATIENTS', 'p_id'), ('PATIENTS', 'p_age'), ('PATIENTS', 'p_gen'), 
        ('PATIENTS', 'p_eth'), ('PATIENTS', 'p_hgt'),
        ('HOSPITALS', 'h_id'),
        ('ICUS', 'i_id'), ('ICUS', 'i_type'), ('ICUS', 'i_stype'),
        ('ENCOUNTERS', 'e_id'), ('ENCOUNTERS', 'e_bmi'), 
        ('ENCOUNTERS', 'e_wt'), ('ENCOUNTERS', 'e_death')
    ])

    # 2. Unir Entidades con Relaciones (Con Cardinalidades)
    
    # Un paciente puede tener muchos encuentros médicos (1:N)
    dot.edge('PATIENTS', 'r_pat', label='(1,1)')
    dot.edge('r_pat', 'ENCOUNTERS', label='(0,N)')

    # Un hospital recibe muchos encuentros médicos (1:N)
    dot.edge('HOSPITALS', 'r_hos', label='(1,1)')
    dot.edge('r_hos', 'ENCOUNTERS', label='(0,N)')

    # Una UCI es asignada a muchos encuentros médicos (1:N)
    dot.edge('ICUS', 'r_icu', label='(1,1)')
    dot.edge('r_icu', 'ENCOUNTERS', label='(0,N)')

    # ================= GUARDAR ARCHIVO =================
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'docs', 'diagramas_er', 'modelo_salud_formal')
    
    dot.render(output_path, cleanup=True)
    print(f"Diagrama formal generado en: {output_path}.png")

if __name__ == '__main__':
    generar_diagrama_formal_ds3()