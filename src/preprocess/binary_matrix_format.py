import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("groceries_38766.csv", usecols=["Member_number", "itemDescription"])
    pd.crosstab(data["Member_number"], data["itemDescription"]).to_csv("groceries_crosstab.csv")

