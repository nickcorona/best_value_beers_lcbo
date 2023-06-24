import json

import pandas as pd


def lcbo_ratings():
    """Process and rate the beers"""
    # Load the beer categories configuration
    with open("config.json") as config_file:
        config = json.load(config_file)

    beer_dict = config["beer_dict"]

    # Load the inventory data
    df = pd.read_csv("D:\\Users\\nickl\\Downloads\\LCBO_store_inventory.csv")

    # Extract can and Size information
    df[["cans", "Size"]] = df["Format"].str.split("x", expand=True)

    # Clean up the cans column
    df["cans"] = df["cans"].str.extract(r"(\d+)").fillna(1).astype(float)

    # Clean up the Size column
    df["Size"] = df["Size"].str.extract(r"(\d+)").fillna(df["cans"]).astype(int)

    # Calculate total volume
    df["volume"] = df["cans"] * df["Size"]

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
    weight = (
        2  # You can adjust this value to give more or less importance to the rating
    )
    df["value"] = (df["rating"] ** weight) / df["dollar_per_volume"]

    # Map beer types to categories
    df["Category"] = df["Style"].apply(
        lambda x: next((k for k, v in beer_dict.items() if x in v), "Other")
    )

    # Get the top 2 beers for each category
    df = df.groupby("Category").apply(lambda x: x.nlargest(2, "value"))

    # Create a new multi-index where the second level is a rank within each category
    df.index = pd.MultiIndex.from_tuples(
        [
            (category, rank + 1)
            for category in df.index.get_level_values(0).unique()
            for rank in range(2)
        ]
    )

    # Filter the DataFrame to include only the necessary columns
    df = df[["Name", "Price", "Format"]]
    df.to_csv("LCBO_best_value.csv")


if __name__ == "__main__":
    lcbo_ratings()
