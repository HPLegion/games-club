import pandas as pd

df = pd.read_csv("games_input.csv", dtype=str, na_values=str)

def get_id(url):
    try:
        return url.split("/")[4]
    except:
        return ""

df["BGG_ID"] = df["BGG_URL"].apply(get_id)

for i, row in df.iterrows():
    print(row.BGG_ID)