import pandas as pd
import numpy as np
from config.catalogos import DIAGNOSTICOS_CIE10


def limpiar_diagnosticos(df):
    """
    Rutina de limpieza para la tabla de Diagnósticos.
    Aplica normalización, filtrado por catálogo y gestión de duplicados.
    """

    # =====================================================
    # 1. NORMALIZACIÓN DE TEXTOS
    # =====================================================

    # Convertimos a string
    # eliminamos espacios
    # estandarizamos formato

    df['codigo_cie'] = (
        df['codigo_cie']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df['descripcion'] = (
        df['descripcion']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # =====================================================
    # 2. VALIDACIÓN CONTRA CATÁLOGO CIE10
    # =====================================================

    # Validamos si el código existe
    # en el catálogo institucional

    df['es_valido'] = (
        df['codigo_cie']
        .isin(DIAGNOSTICOS_CIE10.keys())
    )

    # =====================================================
    # 3. HOMOLOGACIÓN DE DESCRIPCIÓN OFICIAL
    # =====================================================

    # Si el código existe,
    # usamos descripción oficial.
    # Si no existe,
    # conservamos la descripción original.

    df['descripcion_oficial'] = (
        df['codigo_cie']
        .map(
            lambda x:
            DIAGNOSTICOS_CIE10.get(x, {}).get(
                'descripcion',
                np.nan
            )
        )
    )

    df['descripcion_oficial'] = (
        df['descripcion_oficial']
        .fillna(df['descripcion'])
    )

    # ==========================================
    # PATOLOGÍA PROA
    # ==========================================

    df['patologia_proa'] = (
        df['codigo_cie']
        .map(
            lambda x:
            DIAGNOSTICOS_CIE10.get(x, {}).get(
                'patologia',
                ''
            )
        )
    )

    # =====================================================
    # 4. LIMPIEZA DE IDs
    # =====================================================

    if 'id_diagnostico' in df.columns:

        df['id_diagnostico'] = pd.to_numeric(
            df['id_diagnostico'],
            errors='coerce'
        )

        df = df[df['id_diagnostico'] > 0]

    # =====================================================
    # 5. GESTIÓN DE NULOS
    # =====================================================

    # Eliminamos únicamente
    # códigos completamente vacíos

    df['codigo_cie'] = (
        df['codigo_cie']
        .replace(['', 'NONE', 'NAN'], np.nan)
    )

    df = df.dropna(subset=['codigo_cie'])

    # =====================================================
    # 6. ESTADO DE VALIDACIÓN
    # =====================================================

    # Creamos estado clínico
    # sin eliminar información real

    df['estado_cie10'] = np.where(
        df['es_valido'] == True,
        'VALIDO',
        'NO_VALIDADO'
    )

    # =====================================================
    # 7. DUPLICADOS
    # =====================================================

    # Eliminamos SOLO registros idénticos.
    # Ya NO eliminamos por codigo_cie únicamente.

    df = df.drop_duplicates()

    # =====================================================
    # 8. COLUMNAS FINALES
    # =====================================================

    columnas_finales = [
        'codigo_cie',
        'descripcion_oficial',
        'patologia_proa',
        'estado_cie10'
    ]

    return df[columnas_finales]