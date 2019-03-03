import pandas as pd
from boardgamegeek import BGGClient
from tqdm import tqdm

def get_id(url):
    try:
        return url.split("/")[4]
    except:
        return ""



df = pd.read_csv("games_input.csv", dtype=str)
df["BGG_ID"] = df["BGG_URL"].apply(get_id)


bgg = BGGClient(requests_per_minute=720)
newdf = pd.DataFrame(columns=df.columns)
for i, row in tqdm(df.iterrows(), total=df.shape[0], ascii=True):
    # print(row.TITLE)
    newdf.loc[i,:] = row
    if not row.BGG_ID:
        continue
    try:
        game = bgg.game(game_id=row.BGG_ID)
    except:
        game = None
    
    if game:

        newdf.loc[i, "TITLE"] = game.name
        newdf.loc[i, "MINPLAYERS"] = game.min_players
        newdf.loc[i, "MAXPLAYERS"] = game.max_players
        newdf.loc[i, "THUMBNAIL"] = game.thumbnail
        newdf.loc[i, "IMAGE"] = game.image
        newdf.loc[i, "DESCRIPTION"] = game.description.replace("\n", "")
        newdf.loc[i, "YEAR"] = game.year
        if game.expansion:
            newdf.loc[i, "TYPE"] = "Expansion"
            newdf.loc[i, "BASEGAME"] = " AND ".join([thing.name for thing in game.expands])
        else:
            newdf.loc[i, "TYPE"] = "Game"

newdf = newdf.sort_values("TITLE")

lockerdf = newdf[newdf["LOCATION"] == "Main Games Locker R2"]
storagedf = newdf[newdf["LOCATION"] != "Main Games Locker R2"]

lockerdf.to_csv("lockergames.csv", index=False)
storagedf.to_csv("storagegames.csv", index=False)