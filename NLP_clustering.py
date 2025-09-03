import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

FILE_PATH = "/Users/berkay.caliskan/Desktop/MSTR_ERROR_LOGS_EDIT.xlsx"

df = pd.read_excel(FILE_PATH, sheet_name="Edited Error Logs info deleted", engine="openpyxl")

def clean_text(s):
    s = str(s).lower()
    # remove everything except letters, digits, and spaces
    return re.sub(r"[^a-z0-9\s]", " ", s)

df["msg_clean"] = df["ERROR MESSAGE"].apply(clean_text)

vectorizer = TfidfVectorizer(
    stop_words="english",  # built-in English stopwords
    max_df=0.8,
    min_df=2
)
X = vectorizer.fit_transform(df["msg_clean"])

"""
#Elbow method

inertia = []
K_values = range(2, 16)
for k in K_values:
    km = KMeans(n_clusters=k, random_state=42).fit(X)
    inertia.append(km.inertia_)

plt.figure()
plt.plot(K_values, inertia, marker="o")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method for K-Means")
plt.tight_layout()
plt.show()


#Calculating Silhouette score

for k in (4, 6):
    labels = KMeans(n_clusters=k, random_state=42).fit_predict(X)
    print(k, silhouette_score(X, labels))

"""

k = 6

model = KMeans(n_clusters=k, random_state=42)
df["cluster"] = model.fit_predict(X)

terms = vectorizer.get_feature_names_out()
order_centroids = model.cluster_centers_.argsort()[:, ::-1]

print("Top terms per cluster:")
for i in range(k):
    top10 = [terms[idx] for idx in order_centroids[i, :10]]
    print(f"Cluster {i}: {', '.join(top10)}")


'''
output_csv = "clustered_errors.csv"
df[["ERROR MESSAGE", "cluster"]].to_csv(output_csv, index=False, sep=';')
print(f"\nCluster assignments saved to '{output_csv}'.")
'''

cluster_names = {
    0: "Client Connection & Timeout Errors",
    1: "Invalid State / Deletion Errors",
    2: "Session & Login Limit Errors",
    3: "Code Execution (C++ Source) Errors",
    4: "Network I/O & Stream Errors",
    5: "Report Cache & Instance Failures"
}
df["cluster_name"] = df["cluster"].map(cluster_names)

print(df["cluster_name"].value_counts())

pivot = df.pivot_table(
    index="LOCATION",
    columns="cluster_name",
    values="ERROR MESSAGE",
    aggfunc="count",
    fill_value=0
)
print(pivot)

for i in range(model.n_clusters):
    print(f"\n--- Cluster {i} samples ---")
    print(df[df["cluster"]==i]["ERROR MESSAGE"].sample(5).tolist())

'''

OUTPUT_PATH  = "/Users/berkay.caliskan/Desktop/MSTR_ERROR_LOGS_EDIT.xlsx"
NEW_SHEET   = "WithClusters"

with pd.ExcelWriter(
        OUTPUT_PATH,
        engine="openpyxl",
        mode="a",                    
        if_sheet_exists="replace"   
    ) as writer:
    df.to_excel(writer, index=False, sheet_name=NEW_SHEET)

print(f"Written merged data (with clusters) to the new sheet '{NEW_SHEET}'.")

'''
