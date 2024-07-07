"""
A script that scrapes USD and EUR values from the xls files in 
the BCV website (Banco Central de Venezuela) and saves them to a file.

Authors:
    Camilo Perez <camilop15.cp@gmail.com>

Usage: 
    python excel_scrap.py

Requirements:
    pip install xlrd
"""

import os
from datetime import datetime

import xlrd

from .config import XLS_DIR, XLS_FILE, RENAME_FILES_ENABLED


def rename_files(directory: str):
    """
    Renames the files in the directory.

    Args:
        directory (str): The directory to rename the files in.
    """
    file_list = os.listdir(directory)
    file_list.sort(reverse=True)
    for old_name in file_list:
        if "_" in old_name:
            new_name = old_name.split("_")[2]
            new_name = new_name[2:4] + new_name[1] + ".xls"
            os.rename(directory + old_name, directory + new_name)
            print(f"Renamed '{old_name}' to '{new_name}'")


def get_sheet_date(column):
    """
    Gets the sheet date from a column.

    Args:
        column (list): The column to get the sheet date from.

    Returns:
        str: The sheet date.
    """
    for cell in column:
        content = str(cell).replace("'", "").split(":")
        if content[1].lstrip().rstrip() == "Fecha Valor":
            sheet_date = content[2].replace(" ", "")
            sheet_date = str(datetime.strptime(sheet_date, "%d/%m/%Y")).split(
                " ", maxsplit=1
            )[0]
            return sheet_date
    return None


def get_currency_value(row):
    """
    Gets the currency value from a row.

    Args:
        row (list): The row to get the currency value from.

    Returns:
        str: The currency value.
    """
    value_list = str(row[-1]).split(":")[1].split(".")
    value_list[1] = value_list[1].ljust(8, "0")
    value = ",".join(value_list)
    return value


def process_sheet(sheet: xlrd.sheet.Sheet):
    """
    Processes a sheet and returns the results.

    Args:
        sheet (xlrd.sheet.Sheet): The sheet to process.

    Returns:
        str: The results of the processing.
    """
    sheet_rows = sheet.nrows

    column = sheet.col(3)
    sheet_date = get_sheet_date(column)

    for index in range(sheet_rows):
        row = sheet.row(index)
        currency = str(row[1]).split(":")[1].replace("'", "")

        if currency == "EUR":
            eur_value = get_currency_value(row)
        if currency == "USD":
            usd_value = get_currency_value(row)

    if sheet_date is not None:
        return f"{sheet_date} EUR {eur_value} USD {usd_value}"
    return None


def process_file(file_name: str):
    """
    Processes a single file and returns the results.

    Args:
        file_name (str): The name of the file to process.

    Returns:
        list[str]: The results of the processing.
    """
    workbook = xlrd.open_workbook_xls(file_name)
    number_of_sheets = workbook.nsheets

    data: list[str] = []
    for index in range(number_of_sheets):
        sheet = workbook.sheet_by_index(index)
        result = process_sheet(sheet)
        if result is not None:
            data.append(result)
    return data


def process_directory(directory: str, output_file: str):
    """
    Processes all files in a directory and writes the results to an output file.

    Args:
        directory (str): The directory to process.
        output_file (str): The output file to write the results to.
    """
    file_list = os.listdir(directory)
    file_list.sort(reverse=True)

    data: list[str] = []
    for source_name in file_list:
        data.extend(process_file(directory + source_name))
    data.sort()

    with open(output_file, "w", encoding="utf-8") as file:
        for line in data:
            file.write(f"{line}\n")


def main():
    """
    Main function.
    """
    if RENAME_FILES_ENABLED:
        rename_files(XLS_DIR)
    process_directory(XLS_DIR, XLS_FILE)


if __name__ == "__main__":
    main()
