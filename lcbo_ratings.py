import json

import matplotlib.pyplot as plt
import pandas as pd
import spacy
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

with open("config.json") as config_file:
    config = json.load(config_file)

beer_dict = config["beer_dict"]

df = pd.read_csv("D:\\Users\\nickl\\Downloads\\LCBO_store_inventory.csv")

# split Format on 'x' if it exists, rename start as cans and end as number
df[["cans", "size"]] = df["Format"].str.split("x", expand=True)
df.head()
# if number is null, then replace with cans
df["size"] = df["size"].fillna(df["cans"])
df["cans"] = df["cans"].astype(str)

# if can in cans then replace whole value with 1
df["cans"] = df["cans"].apply(lambda x: "1" if "mL" in x else x)
df["cans"] = df["cans"].str.replace(" ", "")
df["cans"] = df["cans"].fillna(1)
df["cans"] = df["cans"].astype(float)

# extract integers from cans column
df["size"] = df["size"].str.extract(r"(\d+)")

# drop na on size
df = df.dropna(subset=["size"])
df["size"] = df["size"].astype(int)
df["volume"] = df["cans"] * df["size"]


# remove $ from price
df["Price"] = df["Price"].str.replace("$", "")

# grab before \n if \n exists
df["Price"] = df["Price"].str.split("\n").str[0]

# convert price to float
df["Price"] = df["Price"].astype(float)


# volume per dollar
df["volume_per_dollar"] = df["volume"] / df["Price"]

# pull number before /5 and convert to float
df["rating"] = df["Rating"].str.split("/5").str[0].fillna(0).astype(float)

# rating per volume per dollar
df["rating_per_volume_per_dollar"] = df["rating"] / df["volume_per_dollar"]

df = df.sort_values(by=["rating_per_volume_per_dollar"], ascending=False)

# replace nan with None in Style
df["Style"] = df["Style"].fillna("None")


# Function to map specific beer type to a general category
def map_to_category(beer_type):
    for category, types in beer_dict.items():
        if beer_type in types:
            return category
    return "Other"  # for beer types not covered in the dictionary


# Apply the function to the 'beer_style' column
df["Category"] = df["Style"].apply(map_to_category)

# select highest rating per volume per dollar for each cluster
df = (
    df.sort_values(by=["rating_per_volume_per_dollar"], ascending=False)
    .groupby("Category")
    .head(1)
)

# filter on name, inventory, rating, price
df = df[
    ["Name", "Producer", "Category", "Rating", "Price"]
].dropna()

# reset and drop index
df = df.reset_index(drop=True)

# write dataframe as seen to txt
with open("LCBO_store_inventory.txt", "w") as f:
    f.write(df.to_string())
