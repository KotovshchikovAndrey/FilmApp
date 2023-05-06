import pandas as pd
import json

ids = set()

file_path = "Путь"
df = pd.read_csv(file_path, low_memory=False)

length = len(df.get("id"))
conuter = 0
for index in range(length):
    id = df.get("id")[index]
    if id in ids:
        continue

    production_company = df.get("production_companies")[index]
    if production_company:
        try:
            json.loads(production_company.replace("'", '"'))
        except:
            conuter += 1
            print(f"ошибка на строке с id={id}", production_company)

    ids.add(id)

print(conuter)
