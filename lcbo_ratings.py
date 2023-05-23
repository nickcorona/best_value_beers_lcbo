# BEGIN: 5j3z8r9s2v7t
import pandas as pd
import spacy
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("C:\\Users\\nickl\\AppData\\Local\\Temp\\MicrosoftEdgeDownloads\\09626e46-951c-497f-b6a9-2fbae07b87f6\\LCBO_store_inventory.csv")

# split Format on 'x' if it exists, rename start as cans and end as number
df[['cans', 'size']] = df['Format'].str.split('x', expand=True)
df.head()
# if number is null, then replace with cans
df['size'] = df['size'].fillna(df['cans'])
df['cans'] = df['cans'].astype(str)

# if can in cans then replace whole value with 1
df['cans'] = df['cans'].apply(lambda x: '1' if 'mL' in x else x)
df['cans'] = df['cans'].str.replace(' ', '')
df['cans'] = df['cans'].fillna(1)
df['cans'] = df['cans'].astype(float)

# extract integers from cans column
df['size'] = df['size'].str.extract('(\d+)')

# drop na on size
df = df.dropna(subset=['size'])
df['size'] = df['size'].astype(int)
df['volume'] = df['cans'] * df['size']


# remove $ from price
df['Price'] = df['Price'].str.replace('$', '')

# grab before \n if \n exists
df['Price'] = df['Price'].str.split('\n').str[0]

# convert price to float
df['Price'] = df['Price'].astype(float)


# volume per dollar
df['volume_per_dollar'] = df['volume'] / df['Price']

# pull number before /5 and convert to float
df['rating'] = df['Rating'].str.split('/5').str[0].fillna(0)

# rating per volume per dollar
df['rating_per_volume_per_dollar'] = df['rating'].astype(float) / df['volume_per_dollar']

df = df.sort_values(by=['rating_per_volume_per_dollar'], ascending=False)

# replace nan with None in Style
df['Style'] = df['Style'].fillna('None')

# This is the English model by SpaCy. You need to download it first with: python -m spacy download en_core_web_md
nlp = spacy.load('en_core_web_md')

# Vectorize the beer styles
df['vector'] = df['Style'].apply(lambda x: nlp(x).vector)

# Transform list of vectors into feature matrix
X = df['vector'].to_list()

# Use DBSCAN to identify clusters based on cosine similarity
db = DBSCAN(metric='cosine', eps=0.2, min_samples=2).fit(X)

# Create a new column in dataframe with cluster labels
df['cluster'] = db.labels_

# Print out the dataframe
print(df)

# select highest rating per volume per dollar for each cluster
df = df.sort_values(by=['rating_per_volume_per_dollar'], ascending=False).groupby('cluster').head(1)

# filter on name, inventory, rating, price
df = df[['Name', 'Producer', 'Style', 'Rating', 'ABV', 'Price', 'Stock', 'Format']].dropna()

# print all columns
pd.set_option('display.max_columns', None)
print(df)
