import pandas as pd

class Transformation:

    def __init__(self, path):
        self.df = pd.read_json(path)

    def clean(self):
        # convertir precios a float
        self.df["current_price"] = pd.to_numeric(self.df["current_price"], errors="coerce")
        self.df["old_price"] = pd.to_numeric(self.df["old_price"], errors="coerce")

        # normalizar discount
        self.df["discount"] = self.df["discount"].replace("No Discount", None)

        # limpiar strings
        self.df["store_name"] = self.df["store_name"].str.strip()
        self.df["name_product"] = self.df["name_product"].str.strip()

        # quitar duplicados
        self.df = self.df.drop_duplicates()

    def to_excel(self):
        self.df.to_excel("rappi.xlsx", index=False)


if __name__ == "__main__":
    t = Transformation("rappi.json")
    t.clean()
    t.to_excel()