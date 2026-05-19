import pandas as pd
import numpy as np


def limpiar_pacientes(df):
    """
    Rutina de limpieza para la tabla de Pacientes.
    Normaliza nombres, documentos, fechas de nacimiento y valida el peso (kg).
    """

    # =====================================================
    # 1. NORMALIZACIÓN DE TEXTOS
    # =====================================================

    # Convertimos nombres a string,
    # eliminamos espacios
    # y estandarizamos formato

    df['nombre'] = (
        df['nombre']
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # =====================================================
    # 2. LIMPIEZA DE DOCUMENTO
    # =====================================================

    # Garantizamos que el documento
    # sea completamente numérico

    df['documento'] = pd.to_numeric(

        df['documento']
        .astype(str)
        .str.replace(r'[^0-9]', '', regex=True),

        errors='coerce'
    )

    # =====================================================
    # 3. FECHA DE NACIMIENTO
    # =====================================================

    # En Excel hospitalario real
    # esta columna puede NO existir

    if 'fecha_nacimiento' in df.columns:

        df['fecha_nacimiento'] = pd.to_datetime(
            df['fecha_nacimiento'],
            errors='coerce'
        )

    else:

        # Creamos columna vacía
        # para mantener compatibilidad

        df['fecha_nacimiento'] = pd.NaT

    # =====================================================
    # 4. VALIDACIÓN DE PESO
    # =====================================================

    # En el hospital real
    # puede no venir el peso

    if 'peso_kg' in df.columns:

        df['peso_kg'] = pd.to_numeric(
            df['peso_kg'],
            errors='coerce'
        )

        # Validación rango pediátrico lógico

        df = df[
            (df['peso_kg'] > 0) &
            (df['peso_kg'] < 100)
        ]

    else:

        # Creamos columna vacía
        # para mantener compatibilidad

        df['peso_kg'] = np.nan

    # =====================================================
    # 5. SERVICIO HOSPITALARIO
    # =====================================================

    # Nueva columna importante
    # del Excel real

    if 'servicio' in df.columns:

        df['servicio'] = (
            df['servicio']
            .astype(str)
            .str.strip()
            .str.upper()
        )

    else:

        df['servicio'] = ""

    # =====================================================
    # 6. GESTIÓN DE NULOS
    # =====================================================

    # Campos obligatorios mínimos

    df = df.dropna(
        subset=[
            'documento',
            'nombre'
        ]
    )

    # =====================================================
    # 7. DUPLICADOS
    # =====================================================

    # Conservamos un paciente único
    # por documento

    df = df.drop_duplicates(
        subset=['documento']
    )

    # =====================================================
    # 8. COLUMNAS FINALES
    # =====================================================

    columnas_finales = [
        'documento',
        'nombre',
        'servicio',
        'fecha_nacimiento',
        'peso_kg'
    ]

    return df[columnas_finales]