import pandas as pd
import numpy as np
from config.catalogos import (
    MEDICAMENTOS_VALIDOS,
    INFO_MEDICAMENTOS,
    HOMOLOGACION_MEDICAMENTOS
)

def limpiar_medicamentos(df):
    """
    Rutina de limpieza para la tabla de Medicamentos.
    Normaliza nombres técnicos, limpia unidades y valida dosis inconsistentes.
    """

    # =====================================================
    # 1. NORMALIZACIÓN DE TEXTOS
    # =====================================================

    # Eliminamos espacios en blanco
    # y estandarizamos a MAYÚSCULAS para comparar

    df['nombre_sucio'] = (
        df['nombre']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # =====================================================
    # 2. HOMOLOGACIÓN FLEXIBLE DE MEDICAMENTOS
    # =====================================================

    def homologar_medicamento(nombre):

        nombre = str(nombre).upper().strip()

        for clave, valor in HOMOLOGACION_MEDICAMENTOS.items():

            if clave in nombre:

                return valor

        return "NO_VALIDO"


    # Aplicamos homologación

    df['nombre_homologado'] = (
        df['nombre_sucio']
        .apply(homologar_medicamento)
    )

    # =====================================================
    # 3. FILTRADO DE VALORES ESPERADOS
    # =====================================================

    # Eliminamos basura lógica
    # y medicamentos no reconocidos

    df = df[
        df['nombre_homologado'] != "NO_VALIDO"
    ].copy()

    # =====================================================
    # 4. LIMPIEZA DE DOSIS
    # =====================================================

    if 'dosis_prescrita' in df.columns:

        # Extraemos valores numéricos
        # Ej:
        # "220 MG"
        # "1 GR"
        # "500mg"

        df['dosis_valor'] = pd.to_numeric(

            df['dosis_prescrita']
            .astype(str)
            .str.upper()
            .str.replace(",", ".", regex=False)
            .str.replace(r'[^0-9.]', '', regex=True),

            errors='coerce'
        )

        # Eliminamos dosis inválidas

        df = df[df['dosis_valor'] > 0]

    # =====================================================
    # 5. VALIDACIÓN SEGURIDAD PROA
    # =====================================================

    def validar_seguridad(row):

        nombre_corto = row['nombre_homologado']

        if nombre_corto in INFO_MEDICAMENTOS:

            max_permitida = (
                INFO_MEDICAMENTOS[nombre_corto]['dosis_max_mg_kg']
            )

            # ALERTA por dosis exagerada

            if row['dosis_valor'] > (max_permitida * 100):

                return "ALERTA"

            return "OK"

        return "DESCONOCIDO"

    df['estado_proa'] = df.apply(
        validar_seguridad,
        axis=1
    )

    # =====================================================
    # 6. DUPLICADOS
    # =====================================================

    df = df.drop_duplicates()

    # =====================================================
    # 7. COLUMNAS FINALES
    # =====================================================

    columnas_finales = [
        'nombre_homologado',
        'dosis_valor',
        'estado_proa'
    ]

    return df[columnas_finales]