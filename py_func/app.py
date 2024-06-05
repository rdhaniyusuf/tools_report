import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import pytz
import pyautogui
import time as tsleep

import win32com.client as win32

def format_id_time():
    dt =datetime.utcnow()
    id_tz = pytz.timezone("Asia/Jakarta")
    dt_id = dt.replace(tzinfo=pytz.utc).astimezone(id_tz)
    formated_date = dt_id.strftime("%d %B %Y")
    hour = dt_id.hour
    if 7<= hour <10:
        period_day = "Pagi"
    elif 10<= hour <16:
        period_day = "Siang"
    elif 15<= hour <24:
        period_day = "Sore"
    
    return [formated_date, period_day]

time = format_id_time()

FILE_NAME = "Monitoring Tiket ITSM "+ time[0] +  " " + time[1]+".xlsx"


def save_to_excel(xlApp):

    # Modifikasi ini
    # Save the DataFrame to an Excel file with the FILE_NAME in the name
    # output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=FILE_NAME)
    output_file_path = "output/" + FILE_NAME
    wb = xlApp.ActiveWorkbook
    # print(output_file_path)
    # wb.Close()

    ws = wb.ActiveSheet
    ws.Range("A2").Select()
    ws.PivotTables("Aplikasi").PivotSelect("", win32.constants.xlDataAndLabel, True)
    if output_file_path:
        wb.SaveAs(output_file_path, FileFormat=51, CreateBackup=False)
        print("Saving Done")

    # xlApp.Selection.Copy()
    # tsleep.sleep(3)
    # pyautogui.hotkey('alt', 'tab', 'tab', 'tab')
    # tsleep.sleep(3)
    # pyautogui.hotkey('ctrl', 'v')

def do_rename_sort(ws):
    ws.Activate()
    pt = ws.PivotTables("Aplikasi")
    pt.CompactLayoutRowHeader = "Aplikasi"

    try:
        ws.Range("A5").Select()
        ws.PivotTables("Aplikasi").PivotFields("Service Family").AutoSort(2, "Count of Ticket Created On")

        # Sort "Status" in descending order
        ws.Range("A6").Select()
        ws.PivotTables("Aplikasi").PivotFields("Status").AutoSort(2, "Status")

        # Sort "Task Assign To" in descending order based on "Count of Ticket Created On"
        ws.Range("A8").Select()
        ws.PivotTables("Aplikasi").PivotFields("Task Assign To").AutoSort(2, "Count of Ticket Created On")


    except Exception as e:
        print(f"Error in AutoSort: {e}")

def insert_pivot_field(pt, ws_report):
    field_rows= {
        "Service Family" : "Service Family",
        "Status":"Status",
        "Task Assign To": "Task Assign To",
        "Ticket Created On" :"Ticket Created On"
    }

    # pivot Row
    for field_name, field in field_rows.items():
        pt.PivotFields(field).Orientation = 1 # As Row
        pt.PivotFields(field).Position = list(field_rows.values()).index(field)+1
    
    # Pivot Column
    ticket_create_on_pivot_column = pt.PivotFields("Ticket Created On")
    ticket_create_on_pivot_column.Orientation = 2 # Column
    ticket_create_on_pivot_column.Position = 1

    # Need Group
    
    #Pivot Values
    ticket_create_on_pivot_values = pt.PivotFields("Ticket Created On")
    ticket_create_on_pivot_values.Orientation = 4 # Values
    ticket_create_on_pivot_values.Function = -4112
    
    group_report = ws_report.Range("B3")
    group_report.Group(Start=True, End=True, Periods=[False, False, False,True, False, False, True])
    ws_report.Rows("3:3").EntireRow.Hidden = True

    pt_field_year = pt.PivotFields("Years (Ticket Created On)")
    pt_field_year.Subtotals = [False] * 12
    
    do_rename_sort(ws_report)

def do_pivot(wb,ws_data, ws_report):
    start_range = "A$1"
    last_col = ws_data.Cells(1, ws_report.Columns.Count).End(win32.constants.xlToLeft).Column
    end_range = f"{ws_data.Cells(1, last_col).Address}"

    pt_cache = wb.PivotCaches().Create(1, ws_data.Range(start_range, end_range).CurrentRegion)
    pt = pt_cache.CreatePivotTable(ws_report.Range("A2"), "Aplikasi")

    pt.ColumnGrand = True
    pt.RowGrand = True
    pt.SubtotalLocation(2)
    pt.RowAxisLayout(0)

    pt.TableStyle2 = "PivotStyleMedium9"

    insert_pivot_field(pt, ws_report)


def do_border_pivot(xlApp):
    wb = xlApp.ActiveWorkbook
    ws = wb.ActiveSheet
    ws.PivotTables("Aplikasi").PivotSelect("", win32.constants.xlDataAndLabel, True)
    selection = xlApp.Selection
    selection.Borders(win32.constants.xlDiagonalDown).LineStyle = win32.constants.xlNone
    selection.Borders(win32.constants.xlDiagonalUp).LineStyle = win32.constants.xlNone


    for border_type in [win32.constants.xlEdgeLeft, win32.constants.xlEdgeTop,
                    win32.constants.xlEdgeBottom, win32.constants.xlEdgeRight,
                    win32.constants.xlInsideVertical, win32.constants.xlInsideHorizontal]:
        b = selection.Borders(border_type)
        b.LineStyle = win32.constants.xlContinuous
        b.ColorIndex = 0
        b.TintAndShade = 0
        b.Weight = win32.constants.xlThin
    
    selection.Copy()


def process_excel_file(input_file_path):
    xlApp = win32.Dispatch('Excel.Application')
    xlApp.Visible = True

    wb = xlApp.Workbooks.Open(input_file_path)
    ws_input = wb.Worksheets("Data")
    ws_rekap = wb.Worksheets.Add()
    ws_rekap.Name = "Rekap"

    # do Pivot
    do_pivot(wb, ws_input, ws_rekap)
    
    #do bordering
    do_border_pivot(xlApp)
    
    save_to_excel(xlApp)

def on_submit():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        process_excel_file(file_path)

# if __name__ == '__main__':
#     on_submit()