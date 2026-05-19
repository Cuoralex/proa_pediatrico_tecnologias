import pandas as pd
import random
from ..config.catalogos import MEDICAMENTOS_VALIDOS
from ..utils.generator_base import ensuciar_texto, generar_id_sucio, inyectar_basura_logica

def generar_simulacion_medicamentos(n=40):
    """
    Genera un DataFrame con prescripciones de medicamentos 'sucias'.
    Simula el 'vómito' de datos para el programa PROA Pediátrico.
    """
    datos_sucios = []

    for _ in range(n):
        # Selección estocástica: 15% de probabilidad de insertar basura lógica
        if random.random() < 0.15:
            nombre_med = inyectar_basura_logica()
            dosis = "999999 MG"
        else:
            nombre_med = random.choice(MEDICAMENTOS_VALIDOS)
            # Generamos dosis realistas pero con formato sucio (ej. '220 mg ')
            dosis = f"{random.randint(10, 500)} MG"

        registro = {
            # Inyección de errores: espacios y mezcla de mayúsculas
            "id_medicamento": generar_id_sucio(random.randint(100, 999)),
            "nombre": ensuciar_texto(nombre_med),
            "dosis_prescrita": ensuciar_texto(dosis),
            # Simulación de campo restringido (Booleano con errores)
            "restringido": random.choice([True, False, "SI", "NO", None])
        }
        
        datos_sucios.append(registro)

    # Retornamos el DataFrame tabulado para iniciar la limpieza con Pandas
    return pd.DataFrame(datos_sucios)