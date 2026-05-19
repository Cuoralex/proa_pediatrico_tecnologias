# PROA Pediátrico - ETL Clínico Hospitalario

Sistema ETL desarrollado en Python para procesamiento, limpieza, normalización y validación de antibióticos hospitalarios pediátricos orientados al programa PROA (Programa de Optimización de Antimicrobianos).

El proyecto permite:

- Leer reportes hospitalarios reales en Excel
- Filtrar antibióticos institucionales
- Limpiar datos clínicos
- Homologar medicamentos
- Validar diagnósticos CIE10
- Integrar clasificación PROA
- Generar archivo Excel final listo para ronda médica y backend Java

---

# Tecnologías utilizadas

- Python 3.12
- Pandas
- NumPy
- OpenPyXL
- Excel Hospitalario
- Backend Java (consumo posterior)

---

# Estructura del proyecto

```text
proa_pediatrico_tecnologias/
│
├── config/
│   ├── __init__.py
│   └── catalogos.py
│
├── procesamiento/
│   ├── __init__.py
│   ├── limpieza_pacientes.py
│   ├── limpieza_medicamentos.py
│   └── limpieza_diagnosticos.py
│
├── utils/
│
├── main.py
├── requirements.txt
├── README.md
│
├── Reporte de antibióticos 26-10-2023 al 27-10-2023.xlsx
├── reporte PROA - Octubre-2.xlsx
└── reporte_PROA_generado.xlsx
```

---

# Archivos de entrada

## Excel hospitalario origen

Ubicación:

```text
proa_pediatrico_tecnologias/
└── Reporte de antibióticos 26-10-2023 al 27-10-2023.xlsx
```

Contiene:

- medicamentos
- dosis
- frecuencias
- diagnósticos
- servicios
- pacientes

---

# Archivo generado automáticamente

```text
reporte_PROA_generado.xlsx
```

Este archivo:

- queda listo para ronda médica
- se completa manualmente clínicamente
- posteriormente es consumido por el backend Java

---

# Instalación

## 1. Instalar dependencias

Abrir terminal en la raíz del proyecto:

```bash
pip install pandas numpy openpyxl
```

---

# Ejecución del proyecto

Desde PowerShell:

```powershell
C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe main.py
```

---

# Flujo del sistema

```text
Excel hospitalario
        ↓
Python ETL PROA
        ↓
reporte_PROA_generado.xlsx
        ↓
Ronda médica
        ↓
Backend Java
        ↓
Cálculos clínicos
```

---

# Funcionalidades implementadas

## Limpieza de pacientes

- normalización de nombres
- validación documentos
- limpieza de servicio
- control de duplicados

---

## Limpieza de medicamentos

- homologación institucional
- validación antibióticos
- limpieza de dosis
- clasificación PROA
- validación de seguridad

---

## Limpieza diagnósticos

- normalización CIE10
- validación institucional
- clasificación PROA:
  - ITU
  - ITB
  - NAC
  - MENINGITIS

---

# Columnas finales exportadas

```text
Servicio
Docidentidad
Usuario
Nombre
Dosis
Medidadosis
Frecuencia
Unidadfrecuencia
Tto Empirico
Tto Dirigido
cultivo
Suspender
Cambiar
Escalar
Desescalar
RXN adversa
Por dosis
Observacionesorden
Codigo Diagnostico
Diagnostico
```

---

# Desarrolladores

## Integrantes del equipo

- Judy A. Cuartas O.
- Orlan S. Baena V.

---

# Estado actual del proyecto

| Componente | Estado |
|---|---|
| Lectura Excel | ✅ |
| Limpieza ETL | ✅ |
| Homologación medicamentos | ✅ |
| Validación CIE10 | ✅ |
| Clasificación PROA | ✅ |
| Exportación Excel | ✅ |
| Compatibilidad Java | ✅ |
| Pipeline end-to-end | ✅ |

---

# Observaciones clínicas

El sistema actualmente:

- NO reemplaza criterio médico
- NO prescribe tratamiento
- sirve como apoyo clínico PROA
- requiere validación médica final

---

# Requisitos

```text
pandas
numpy
openpyxl
```
