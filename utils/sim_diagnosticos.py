import pandas as pd
import random
from ..config.catalogos import DIAGNOSTICOS_CIE10
from ..utils.generator_base import ensuciar_texto, inyectar_basura_logica, formato_fecha_erroneo

def generar_simulacion_diagnosticos(n=50):
    """
    Genera una lista de diccionarios con datos de diagnósticos 'sucios'.
    Basado en los códigos CIE-10 del Informe.pdf[cite: 1].
    """
    datos_sucios = []
    codigos_oficiales = list(DIAGNOSTICOS_CIE10.keys())

    for _ in range(n):
        # Seleccionamos un código real o inyectamos basura lógica el 10% de las veces
        if random.random() < 0.1:
            codigo = inyectar_basura_logica()
            descripcion = "Descripción inválida"
        else:
            codigo = random.choice(codigos_oficiales)
            descripcion = DIAGNOSTICOS_CIE10[codigo]

        # Aplicamos procesos estocásticos para ensuciar los datos
        registro = {
            "codigo_cie": ensuciar_texto(codigo), # Ej: "  r398  "
            "descripcion": ensuciar_texto(descripcion), # Ej: "fIebRe No eSpEcIfIcAdA"
            "fecha_registro": formato_fecha_erroneo("2026-05-09"), # Formatos incorrectos
            "id_prescripcion": random.randint(-10, 1000) # Incluye IDs negativos
        }
        
        datos_sucios.append(registro)
    
    # Retornamos un DataFrame de Pandas para cumplir con el requerimiento
    return pd.DataFrame(datos_sucios)