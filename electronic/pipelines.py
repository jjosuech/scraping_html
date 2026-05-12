import pandas as pd


class RappiPipeline:

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        if spider.name == "rappi":
            self.items.append(item)
        return item

    def close_spider(self, spider):
        if spider.name != "rappi":
            return

        df = pd.DataFrame(self.items)

        # TU LÓGICA ORIGINAL
        df["current_price"] = pd.to_numeric(df["current_price"], errors="coerce")
        df["old_price"] = pd.to_numeric(df["old_price"], errors="coerce")

        df["discount"] = df["discount"].replace("No Discount", None)

        df["store_name"] = df["store_name"].str.strip()
        df["name_product"] = df["name_product"].str.strip()

        df["description"] = df["description"].astype(str).str.strip()

        df = df.drop_duplicates()

        df.to_excel("rappi.xlsx", index=False)



class FalabellaPipeline:

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        if spider.name == "falabella":
            self.items.append(item)
        return item

    def close_spider(self, spider):
        if spider.name != "falabella":
            return

        df = pd.DataFrame(self.items)

        # LIMPIEZA FALABELLA
        df["current_price"] = pd.to_numeric(df["current_price"], errors="coerce")
        df["old_price"] = pd.to_numeric(df["old_price"], errors="coerce")

        df["discount"] = df["discount"].replace("No Discount", None)
        df["discount"] = df["discount"].str.replace('%', '', regex=False)
        df["discount"] = df["discount"].str.replace('-', '', regex=False)

        df["store_name"] = df["store_name"].str.strip()
        df["name_product"] = df["name_product"].str.strip()
        df["brand"] = df["brand"].str.strip()

        df["description"] = df["description"].astype(str).str.strip()

        df = df.drop_duplicates()

        df.to_excel("falabella.xlsx", index=False)