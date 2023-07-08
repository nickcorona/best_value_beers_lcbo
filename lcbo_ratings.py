import json
import pandas as pd


def load_config():
    with open("config.json") as config_file:
        config = json.load(config_file)
    return config["beer_dict"]


def load_and_prepare_data(beer_dict):
    # Load the inventory data
    df = pd.read_csv("LCBO_store_inventory.csv")

    # Extract can and Size information
    df[["Quantity", "Size"]] = df["Format"].str.extract(
        r"(?:(\d+)?\s*x\s*)?(\d+ mL.*)", expand=True
    )

    # Clean up the cans column
    df["Quantity"] = df["Quantity"].str.extract(r"(\d+)").fillna(1).astype(float)

    # Clean up the Size column
    df["Size"] = df["Size"].str.extract(r"(\d+)").fillna(df["Quantity"]).astype(int)

    # Calculate total volume
    df["Volume"] = df["Quantity"] * df["Size"]

    # Clean up the Price column and convert it to float
    df["Price"] = df["Price"].str.replace("$", "").str.split("\n").str[0].astype(float)

    # Calculate price per volume
    df["dollar_per_volume"] = df["Price"] / df["Volume"]

    # Extract ratings and convert them to float
    df["Rating"] = df["Rating"].str.split("/5").str[0].fillna(0).astype(float)

    # Apply a minimum rating threshold
    min_rating = 3.5  # Adjust this to a value that you think is a fair minimum
    df = df[df["Rating"] >= min_rating]

    # Define value metric and calculate it
    weight = (
        2  # You can adjust this value to give more or less importance to the rating
    )
    df["value"] = (df["Rating"] ** weight) / df["dollar_per_volume"]

    # Map beer types to categories
    df["Category"] = df["Style"].apply(
        lambda x: next((k for k, v in beer_dict.items() if x in v), "Other")
    )

    return df


def lcbo_ratings():
    """Process and rate the beers"""
    beer_dict = load_config()
    df = load_and_prepare_data(beer_dict)

    # Get the top 2 beers for each category
    df = df.groupby("Category").apply(lambda x: x.nlargest(3, "value"))

    # Create a new multi-index where the second level is a rank within each category
    df.index = pd.MultiIndex.from_tuples(
        [
            (category, rank + 1)
            for category in df.index.get_level_values(0).unique()
            for rank in range(df.loc[category].shape[0])
        ]
    )

    # Filter the DataFrame to include only the necessary columns
    df = df[["Name", "Rating", "Price", "Quantity"]]
    df.to_csv("LCBO_best_value.csv")
    print(df)


if __name__ == "__main__":
    lcbo_ratings()
