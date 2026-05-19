import pandas as pd

from procesamiento.limpieza_pacientes import limpiar_pacientes
from procesamiento.limpieza_medicamentos import limpiar_medicamentos
from procesamiento.limpieza_diagnosticos import limpiar_diagnosticos

def ejecutar_proa_pediatrico():

    print("=== INICIANDO SISTEMA PROA PEDIÁTRICO ===")

    # ==========================================
    # FASE 1: LECTURA DEL EXCEL HOSPITALARIO
    # ==========================================

    print("\n[1] Leyendo archivo hospitalario...")

    ruta_excel = r"D:\Desktop\proa_pediatrico_tecnologias\Reporte de antibióticos 26-10-2023 al 27-10-2023.xlsx"

    try:

        df_original = pd.read_excel(ruta_excel)

        print(f"Archivo cargado correctamente.")
        print(f"Total registros originales: {len(df_original)}")

    except Exception as e:

        print(f"ERROR leyendo Excel: {e}")
        return

    # ==========================================
    # VALIDAR COLUMNAS
    # ==========================================

    columnas_requeridas = [
        "Docidentidad",
        "Usuario",
        "Codigo",
        "Nombre",
        "Dosis",
        "Frecuencia",
        "Tipo",
        "Codigo Diagnostico",
        "Diagnostico",
        "Servicio"
    ]

    columnas_faltantes = [
        col for col in columnas_requeridas
        if col not in df_original.columns
    ]

    if columnas_faltantes:

        print("\nERROR: faltan columnas obligatorias:")
        print(columnas_faltantes)
        return

    # ==========================================
    # FASE 2: FILTRAR SOLO ANTIBIÓTICOS
    # ==========================================

    print("\n[2] Filtrando medicamentos antibióticos...")

    df_original["Tipo"] = (
        df_original["Tipo"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_antibioticos = df_original[
        df_original["Tipo"] == "ANTIBIOTICOS"
    ].copy()

    print(f"Total antibióticos encontrados: {len(df_antibioticos)}")

    # ==========================================
    # FASE 3: CONSTRUIR DATAFRAMES PARA LIMPIEZA
    # ==========================================

    print("\n[3] Preparando estructuras para limpieza...")

    # ---------------- PACIENTES ----------------

    df_pacientes = df_antibioticos[
        [
            "Docidentidad",
            "Usuario",
            "Servicio"
        ]
    ].copy()

    df_pacientes.columns = [
        "documento",
        "nombre",
        "servicio"
    ]

    # Compatibilidad con tu limpiador actual

    if "peso_kg" not in df_pacientes.columns:
        df_pacientes["peso_kg"] = None

    if "fecha_nacimiento" not in df_pacientes.columns:
        df_pacientes["fecha_nacimiento"] = None

    # ---------------- MEDICAMENTOS ----------------

    df_medicamentos = df_antibioticos[
        [
            "Codigo",
            "Nombre",
            "Dosis"
        ]
    ].copy()

    df_medicamentos.columns = [
        "id_medicamento",
        "nombre",
        "dosis_prescrita"
    ]

    # ---------------- DIAGNÓSTICOS ----------------

    df_diagnosticos = df_antibioticos[
        [
            "Codigo Diagnostico",
            "Diagnostico"
        ]
    ].copy()

    df_diagnosticos.columns = [
        "codigo_cie",
        "descripcion"
    ]

    # ==========================================
    # FASE 4: LIMPIEZA Y NORMALIZACIÓN
    # ==========================================

    print("\n[4] Ejecutando limpieza y normalización...")

    df_pacientes = df_antibioticos.rename(columns={

        'Docidentidad': 'documento',
        'Usuario': 'nombre',
        'Servicio': 'servicio'

    })

    df_pacientes_limpio = limpiar_pacientes(
        df_pacientes
    )

    df_meds = df_antibioticos.rename(columns={

        'Nombre': 'nombre',
        'Dosis': 'dosis_prescrita'

    })

    df_meds_limpio = limpiar_medicamentos(
        df_medicamentos
    )

    df_diag = df_antibioticos.rename(columns={

        'Codigo Diagnostico': 'codigo_cie',
        'Diagnostico': 'descripcion'

    })

    df_diag_limpio = limpiar_diagnosticos(
        df_diagnosticos
    )

    # ==========================================
    # FASE 5: ELIMINAR DUPLICADOS
    # ==========================================

    print("\n[5] Eliminando duplicados...")

    columnas_duplicado = [
        "Docidentidad",
        "Nombre"
    ]

    if "Fechaordenado" in df_antibioticos.columns:
        columnas_duplicado.append("Fechaordenado")

    df_antibioticos = df_antibioticos.drop_duplicates(
        subset=columnas_duplicado
    )

    print(f"Registros después de duplicados: {len(df_antibioticos)}")

    # ==========================================
    # FASE 6: INTEGRAR PATOLOGÍA PROA
    # ==========================================

    print("\n[6] Integrando clasificación PROA...")

    df_final = df_antibioticos[
        [
            "Servicio",
            "Docidentidad",
            "Usuario",
            "Nombre",
            "Dosis",
            "Medidadosis",
            "Frecuencia",
            "Unidadfrecuencia",
            "Observacionesorden",
            "Codigo Diagnostico",
            "Diagnostico"
        ]
    ].copy()

    # ==========================================
    # COLUMNAS CLÍNICAS JAVA
    # ==========================================

    df_final["Peso(kg)"] = ""
    df_final["ITU"] = ""
    df_final["ITB"] = ""
    df_final["NAC"] = ""
    df_final["Meningitis"] = ""
    df_final["Dosis Calculada"] = ""
    df_final["Dosis Recetada"] = ""

    # ==========================================
    # COLUMNAS MANUALES PARA RONDA
    # ==========================================

    columnas_manuales = [
        "Tto Empirico",
        "Tto Dirigido",
        "cultivo",
        "Suspender",
        "Cambiar",
        "Escalar",
        "Desescalar",
        "RXN adversa",
        "Por dosis"
    ]

    for col in columnas_manuales:
        df_final[col] = ""

    # ==========================================
    # ORDEN FINAL COLUMNAS
    # ==========================================

    columnas_finales = [

        "Servicio",
        "Docidentidad",
        "Usuario",
        "Nombre",

        "Dosis",
        "Medidadosis",
        "Frecuencia",
        "Unidadfrecuencia",

        "Peso(kg)",
        "ITU",
        "ITB",
        "NAC",
        "Meningitis",
        "Dosis Calculada",
        "Dosis Recetada",

        "Tto Empirico",
        "Tto Dirigido",
        "cultivo",
        "Suspender",
        "Cambiar",
        "Escalar",
        "Desescalar",
        "RXN adversa",
        "Por dosis",

        "Observacionesorden",
        "Codigo Diagnostico",
        "Diagnostico"
    ]

    df_final = df_final[columnas_finales]

    # ==========================================
    # EXPORTAR RESULTADO FINAL
    # ==========================================

    print("\n[7] Exportando Excel final PROA...")

    ruta_salida = r"D:\Documents\3. CESDE - Caso cambio de programa\Tecnica - Proyecto\Semestre 3\Nuevas tecnologías\proa_pediatrico_tecnologias\reporte_PROA_generado.xlsx"

    try:

        df_final.to_excel(
            ruta_salida,
            index=False
        )

        print("\nArchivo exportado exitosamente.")
        print(f"Ruta salida:\n{ruta_salida}")

    except Exception as e:

        print(f"ERROR exportando archivo: {e}")

    # ==========================================
    # RESULTADOS
    # ==========================================

    print("\n[8] RESULTADOS NORMALIZADOS")

    print("\n--- Pacientes Limpios ---")
    print(df_pacientes_limpio.head())

    print("\n--- Medicamentos Limpios ---")
    print(df_meds_limpio.head())

    print("\n--- Diagnósticos Limpios ---")
    print(df_diag_limpio.head())

    print("\n=== PROCESO FINALIZADO ===")


if __name__ == "__main__":
    ejecutar_proa_pediatrico()