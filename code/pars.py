import requests as req
import datetime as dt
import openpyxl, os, re


def eating(day):
    if day == 0:
        wkd = dt.datetime.today().weekday()
    else:
        wkd = (dt.date.today() + dt.timedelta(days=1)).weekday()

    if wkd != 6:
        flag = False
        try:
            if day == 0:
                eat = f"https://www.school01.ru/food/{str(dt.date.today())}-sm.xlsx"
            else:
                eat = f"https://www.school01.ru/food/{str(dt.date.today() + dt.timedelta(days=1))}-sm.xlsx"

            file, xls = open("school_food.xlsx", "wb"), req.get(eat)
            file.write(xls.content)
            file.close()

            excel_file = openpyxl.load_workbook('school_food.xlsx')
            employees_sheet = excel_file[excel_file.sheetnames[0]]

            food = {employees_sheet["A4"].value: [], employees_sheet["A12"].value: []}
            food_info = [[employees_sheet["A4"].value, 4, 8], [employees_sheet["A12"].value, 12, 9]]

            flag = True

            if employees_sheet["A22"].value is not None:
                food[employees_sheet["A22"].value] = []
                food_info.append([employees_sheet["A22"].value, 21, 2])

            for j in food_info:
                for i in range(j[2]):
                    if employees_sheet[f"D{j[1] + i}"].value is None:
                        continue

                    gramm = str(int(eval(str(employees_sheet[f"E{j[1] + i}"].value).strip())))
                    kkal = str(eval("".join(str(employees_sheet[f"J{j[1] + i}"].value).split()).replace(",", ".", 1)))

                    food[j[0]].append([employees_sheet[f"D{j[1] + i}"].value, [gramm, kkal]])

            os.remove("school_food.xlsx")

            return [True, food]
        except Exception as e:
            return [False, flag, wkd, repr(e)]
    else:
        return [False, False, wkd]
