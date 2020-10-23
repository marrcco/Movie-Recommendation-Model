import pandas as pd

df = pd.read_csv("imdb_top_800_movies.csv", encoding='ISO-8859-1')

print(df.head())
print(df.dtypes)
print(df.info())

# Cleaning title, directors, writers and stars columns
df["Title"] = df["Title"].apply(lambda x: x.split("(")[0])
df["Director"] = df["Director"].apply(lambda x: x.split(":")[1])
df["Writers"] = df["Writers"].apply(lambda x: x.split(":")[1].split("|")[0].split("(")[0])
df["Stars"] = df["Stars"].apply(lambda x: x.split(":")[1].split("|")[0])

# Converting duration of movie to minutes
df["duration"] = df["Movie_Duration"].apply(pd.Timedelta)
df["hour"] = df["duration"].apply(lambda x: str(x).split("days")[1].split(":")[0])
df["hour"] = pd.to_numeric(df["hour"]) * 60
df["minutes"] = df["duration"].apply(lambda x: str(x).split("days")[1].split(":")[1])
df["minutes"] = pd.to_numeric(df["minutes"])
df["Movie_Duration"] = df["hour"] + df["minutes"]
df.drop(columns=["duration","hour","minutes"],inplace=True)

# Extracting number of ratings from Rating column
df["Num_of_ratings"] = df["Rating"].apply(lambda x: x.split("\r")[1].replace(",",""))
df["Num_of_ratings"] = pd.to_numeric(df["Num_of_ratings"])

df["Rating"] = df["Rating"].apply(lambda x: x.split("\r")[0].split("/")[0])
df["Rating"] = pd.to_numeric(df["Rating"])
print(df.dtypes)


# Converting rows to lower case
to_convert = ["Title","Director","Writers","Stars","Keywords"]
def convert_to_lower(columns):
    for i in columns:
        df[i] = df[i].apply(lambda x: x.lower())

convert_to_lower(to_convert)

# Getting rid of special characters
spec_chars = ["!",'"',"#","ç","","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–",",","[","]",
              "à","á","â","ã","ó", "+","Ù","Û",
              "ä", "©", "í", "ì","ç","\r"]


for char in spec_chars:
    df["Stars"] = df["Stars"].str.replace(char, "")
    df["Keywords"] = df["Keywords"].str.replace(char, "")
    df["Writers"] = df["Writers"].str.replace(char, "")
    df["Title"] = df["Title"].str.replace(char, "")
    df["Director"] = df["Director"].str.replace(char, "")

# Checking for NaN rows
print(df.isnull().values.any())
print(df.isnull().sum().sum())
df.drop(columns="Description",inplace=True)

# Saving dataframe to new CSV
#df.to_csv("imdb_top_800_cleaned.csv", index=False,header=True)