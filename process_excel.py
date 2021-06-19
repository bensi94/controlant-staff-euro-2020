import json
import os
import re

from benedict import benedict
from openpyxl import load_workbook

data = benedict()


def get_cells(current_sheet, cells):
    return [current_sheet[cell].value.strip() for cell in cells]


def get_winner(current_sheet):
    qualifiers = [
        current_sheet["G58"].value.strip(),
        current_sheet["L58"].value.strip(),
    ]
    score_1, score_2 = current_sheet["I58"].value, current_sheet["J58"].value

    if score_1 == score_2:
        penalty_1, penalty_2 = current_sheet["M58"].value, current_sheet["N58"].value

        return qualifiers if penalty_1 > penalty_2 else reversed(qualifiers)

    return qualifiers if score_1 > score_2 else reversed(qualifiers)


FIRST_PLACE_IN_GROUP_CELLS = ("R7", "R12", "R17", "R22", "R27", "R32")
SECOND_PLACE_IN_GROUP_CELLS = ("R8", "R13", "R18", "R23", "R28", "R33")
QUARTER_FINAL_QUALIFIERS_CELLS = ("G52", "G53", "G54", "G55", "L52", "L53", "L54", "L55")
SEMI_FINALS_QUALIFIERS_CELLS = ("G56", "G57", "L56", "L57")
FINALS_QUALIFIERS_CELLS = ("G58", "L58")

for file in os.listdir("sheets"):
    if file.startswith("."):
        continue

    print(f'Processing sheet: "{file}"')
    participant = re.search(r"Euro 2020 -(.*)\.", file, re.IGNORECASE).group(1).strip()

    workbook = load_workbook(filename=f"sheets/{file}", read_only=True, data_only=True)
    sheet = workbook["Matches"]
    data[participant, "First place in group"] = get_cells(sheet, FIRST_PLACE_IN_GROUP_CELLS)
    data[participant, "Second place in group"] = get_cells(sheet, SECOND_PLACE_IN_GROUP_CELLS)
    data[participant, "Quarter final qualifiers"] = get_cells(sheet, QUARTER_FINAL_QUALIFIERS_CELLS)
    data[participant, "Semi finals qualifiers"] = get_cells(sheet, SEMI_FINALS_QUALIFIERS_CELLS)
    data[participant, "Finals qualifiers"] = get_cells(sheet, FINALS_QUALIFIERS_CELLS)
    data[participant, "1st place"], data[participant, "2nd place"] = get_winner(sheet)

with open("data.json", "w") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
