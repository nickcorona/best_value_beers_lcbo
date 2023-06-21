import json
import pandas as pd

# Load the beer categories configuration
with open("config.json") as config_file:
    config = json.load(config_file)

beer_dict = config["beer_dict"]

# Load the inventory data
df = pd.read_csv("D:\\Users\\nickl\\Downloads\\LCBO_store_inventory.csv")

# Extract can and size information
df[["cans", "size"]] = df["Format"].str.split("x", expand=True)

# Clean up the cans column
df["cans"] = df["cans"].str.extract("(\d+)").fillna(1).astype(float)

# Clean up the size column
df["size"] = df["size"].str.extract("(\d+)").fillna(df["cans"]).astype(int)

# Calculate total volume
df["volume"] = df["cans"] * df["size"]

# Clean up the Price column and convert it to float
df["Price"] = df["Price"].str.replace("$", "").str.split("\n").str[0].astype(float)

# Calculate price per volume
df["dollar_per_volume"] = df["Price"] / df["volume"]

# Extract ratings and convert them to float
df["rating"] = df["Rating"].str.split("/5").str[0].fillna(0).astype(float)

# Apply a minimum rating threshold
min_rating = 3.5  # Adjust this to a value that you think is a fair minimum
df = df[df["rating"] >= min_rating]

# Define value metric and calculate it
weight = 2  # You can adjust this value to give more or less importance to the rating
df["value"] = (df["rating"] ** weight) / df["dollar_per_volume"]

# Map beer types to categories
df["Category"] = df["Style"].apply(
    lambda x: next((k for k, v in beer_dict.items() if x in v), "Other")
)

# Select the highest value beer in each category
df = df.sort_values("value", ascending=False).groupby("Category").first()

# Filter the DataFrame to include only the necessary columns
df = df[["Name", "Rating", "Price", "Format"]]

# Print and save the DataFrame
with open("LCBO_store_inventory.txt", "w") as f:
    print(df)
    f.write(df.to_string())
