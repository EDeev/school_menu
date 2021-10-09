from bs4 import BeautifulSoup
import requests as req
import datetime as dt
import openpyxl, os


def eating(day):
    if day == 0:
        wkd = dt.datetime.today().weekday()
    else:
        wkd = (dt.date.today() + dt.timedelta(days=1)).weekday()

    if wkd != 6:
        try:
            resp = req.get('http://school09.ru/vse-stati/main/food1').text
            soup = BeautifulSoup(resp, "html.parser").find_all("ul", "easyfolderlisting")[0]

            food = [[str(_)[15:32], str(_)[190:200], str(_)[130:172]] for _ in soup if _ != "\n"]
            if day == 0:
                eat = [_[2] for _ in food if _[0] == 'A Microsoft Excel' and _[1] == str(dt.date.today())][0]
            else:
                eat = [_[2] for _ in food if _[0] == 'A Microsoft Excel' and _[1] == str(dt.date.today() + dt.timedelta(days=1))][0]

            file, xls = open("school_food.xlsx", "wb"), req.get(eat)
            file.write(xls.content)
            file.close()

            excel_file = openpyxl.load_workbook('school_food.xlsx')
            employees_sheet = excel_file['Лист1']

            food = {employees_sheet["A4"].value: [], employees_sheet["A12"].value: [], employees_sheet["A21"].value: []}

            for j in [[employees_sheet["A4"].value, 4, 7], [employees_sheet["A12"].value, 12, 8],
                      [employees_sheet["A21"].value, 21, 2]]:
                for i in range(j[2]):
                    if employees_sheet[f"D{j[1] + i}"].value is None:
                        break
                    food[j[0]].append([employees_sheet[f"D{j[1] + i}"].value,
                                       [employees_sheet[f"E{j[1] + i}"].value, employees_sheet[f"J{j[1] + i}"].value]])

            os.remove("school_food.xlsx")

            return food
        except Exception:
            return False
    else:
        return False
