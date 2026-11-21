from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header, data = contacts_list[0], contacts_list[1:]

def fix_name(record):
    parts = " ".join(record[:3]).split(" ")
    parts = [p for p in parts if p]
    record[:3] = [
        parts[0] if len(parts) > 0 else "",
        parts[1] if len(parts) > 1 else "",
        parts[2] if len(parts) > 2 else "",
    ]
    return record

PHONE_PATTERN = re.compile(
    r"(\+7|8)\s*$?(\d{3})$?[\s\-]*"            # код страны +7/8 и код города
    r"(\d{3})[\s\-]*"                            # 999
    r"(\d{2})[\s\-]*"                            # 99
    r"(\d{2})"                                   # 99
    r"(?:\s*$?(?:доб\.?|ext\.?)\s*(\d+)$?)?"   # необязательный добавочный
)

def fix_phone(phone):
    m = PHONE_PATTERN.search(phone)
    if not m:
        return phone
    result = f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
    if m.group(6):
        result += f" доб.{m.group(6)}"
    return result

processed = [fix_name(r) for r in data]
for r in processed:
    r[5] = fix_phone(r[5])

merged = {}
for r in processed:
    key = tuple(r[:2])
    if key in merged:
        for i in range(2, 7):
            if not merged[key][i] and r[i]:
                merged[key][i] = r[i]
    else:
        merged[key] = r

contacts_list = [header] + list(merged.values())
pprint(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(contacts_list)
