from __future__ import annotations

from pathlib import Path
import argparse

from openpyxl import load_workbook


def _is_empty_value(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _clean_sheet(worksheet) -> None:
    for row_idx in range(worksheet.max_row, 0, -1):
        if all(_is_empty_value(cell.value) for cell in worksheet[row_idx]):
            worksheet.delete_rows(row_idx)

    for col_idx in range(worksheet.max_column, 0, -1):
        column_cells = worksheet.iter_cols(min_col=col_idx, max_col=col_idx, min_row=1, max_row=worksheet.max_row)
        if all(_is_empty_value(cell.value) for cell in next(column_cells)):
            worksheet.delete_cols(col_idx)


def clean_excel_file(input_path: str | Path, output_path: str | Path | None = None) -> Path:
    source = Path(input_path)
    if source.suffix.lower() != ".xlsx":
        raise ValueError("Solo se soportan archivos .xlsx")

    destination = Path(output_path) if output_path else source.with_name(f"{source.stem}_cleaned.xlsx")

    workbook = load_workbook(source)
    for sheet in workbook.worksheets:
        _clean_sheet(sheet)
    workbook.save(destination)

    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Limpia filas y columnas vacías de un archivo Excel (.xlsx).")
    parser.add_argument("input_path", help="Ruta del archivo de entrada")
    parser.add_argument("--output-path", dest="output_path", help="Ruta del archivo limpio de salida")
    args = parser.parse_args()

    result = clean_excel_file(args.input_path, args.output_path)
    print(f"Archivo limpio generado: {result}")


if __name__ == "__main__":
    main()
