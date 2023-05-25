import json
import re

import pandas as pd

ids = set()

# Файл, где будет сохранен валидный датасет
writebale_file_path = r"ValidDataset.csv"

file_path = r"C:\Users\Andrey\Downloads\DataSet.csv"
df = pd.read_csv(file_path, low_memory=False)

# Удаляем ненужное
df = df.drop(
    columns=[
        "belongs_to_collection",
        "homepage",
        "popularity",
        "revenue",
        "spoken_languages",
        "status",
        "title",
        "video",
        "vote_average",
        "vote_count",
    ]
)

# Меняем местами столбцы. Так надо :)
df = df.reindex(
    columns=[
        "id",
        "original_title",
        "overview",
        "budget",
        "adult",
        "original_language",
        "imdb_id",
        "poster_path",
        "release_date",
        "runtime",
        "tagline",
        "genres",
        "production_companies",
        "production_countries",
    ]
)

length = len(df.get("id"))
counter = 0
for index in range(length):
    id = df.get("id")[index]
    if id in ids:
        continue

    # нужные нам поля
    title = df.get("original_title")[index]
    description = df.get("overview")[index]
    budget = df.get("budget")[index]
    is_adult = df.get("adult")[index]
    language = df.get("original_language")[index]
    imdb_id = df.get("imdb_id")[index]
    poster_path = df.get("poster_path")[index]
    release_date = df.get("release_date")[index]
    time = df.get("runtime")[index]
    tagline = df.get("tagline")[index]
    genres = df.get("genres")[index].replace("'", '"')

    production_company = df.get("production_companies")[index]
    production_countries = df.get("production_countries")[index].replace("'", '"')

    # Замена строки номер {index}
    df.loc[index, "genres"] = genres
    try:
        j = json.loads(production_countries)
        df.loc[index, "production_countries"] = json.dumps(j)
    except:
        counter += 1
        print(f"ошибка на строке {index}", production_countries)

    if production_company != "[]":
        production_company = production_company.replace("'", '"')
        names = re.findall(r"\"name\": \"([^\t,]+)\", \"id\"", production_company)
        edited_names = [name.replace('"', "'") for name in names]
        for i in range(len(names)):
            production_company = production_company.replace(names[i], edited_names[i])
        production_company = production_company.replace("\\xa0", "")
        try:
            y = json.loads(production_company)
            df.loc[index, "production_companies"] = json.dumps(y)
        except Exception as exc:
            print(exc)
            counter += 1
            print(f"ошибка на строке с id={id}", production_company)

    ids.add(id)

df = df.drop(columns=["id"])

# Сохраняем все это барахло
df.to_csv(writebale_file_path, index=False, lineterminator="")
print(counter)
