
import openpyxl

def read_excel_data(wk:openpyxl.Workbook, sheet_name, header_row)->list[dict]:
    # 取得したオブジェクトから、指定した行をヘッダーとして取得
    sheet = wk[sheet_name]
    headers = [cell.value for cell in sheet[header_row]]

    # ヘッダー行以降の行データから、ヘッダーにある列名と行データをもとにセルデータを取得する
    row_data_list:list[dict] = []
    for row in sheet.iter_rows(min_row=header_row + 1, values_only=True):
        row_data:dict[str:any] = {}
        for header, value in zip(headers, row):
            row_data[header] = value
        row_data_list.append(row_data)

    # 取得したセルデータはリストで保持する
    return row_data_list