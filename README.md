# NLP Text Clustering

An unsupervised NLP project for grouping similar application error messages and identifying recurring failure patterns using **TF-IDF** and **K-Means clustering**.

## Overview

Large collections of application logs can be difficult to inspect manually because the same underlying issue may appear in many slightly different messages. This project builds a lightweight text-clustering pipeline that converts raw error messages into numerical representations, groups similar messages, and helps summarize the dominant themes inside each cluster.

The workflow includes:

1. Cleaning and normalizing raw error-message text
2. Converting text into TF-IDF feature vectors
3. Exploring cluster counts with the elbow method and silhouette score
4. Clustering error messages with K-Means
5. Extracting the most important terms for each cluster
6. Assigning readable cluster labels
7. Comparing cluster distributions across error locations

## Project Context

This project was developed as a **personal implementation of an NLP clustering task introduced during my n11 internship**.

The dataset used for this project contains **internal company data**, so I am not able to share the original CSV/Excel file publicly. For confidentiality reasons, this repository includes only my implementation and does **not** contain any proprietary company data.

## Tech Stack

- Python
- Pandas
- scikit-learn
- TF-IDF
- K-Means Clustering
- Matplotlib
- openpyxl

## Methodology

### 1. Text preprocessing

Error messages are converted to lowercase and cleaned using regular expressions so that the clustering model focuses on meaningful alphanumeric content.

### 2. TF-IDF vectorization

`TfidfVectorizer` converts the cleaned messages into sparse numerical vectors. Common terms that appear in too many documents are reduced through `max_df`, while extremely rare terms are filtered with `min_df`.

### 3. Choosing the number of clusters

The project includes exploratory code for:

- **Elbow method** using K-Means inertia
- **Silhouette score** for comparing candidate cluster counts

The current implementation uses **6 clusters**.

### 4. Cluster interpretation

After fitting K-Means, the most heavily weighted terms in each centroid are inspected to understand the theme of each group. The current implementation maps clusters to categories such as:

- Client connection and timeout errors
- Invalid state / deletion errors
- Session and login-limit errors
- Code-execution related errors
- Network I/O and stream errors
- Report cache and instance failures

### 5. Location-based analysis

A pivot table compares how frequently each error category appears across different error locations, making it easier to identify where specific failure types are concentrated.

## Expected Input

The current script expects an Excel dataset containing at least:

- `ERROR MESSAGE` — the raw text to be clustered
- `LOCATION` — the source/location associated with the error

The dataset itself is intentionally **not included** in this repository.

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/berkayclsknn/nlp-text-clustering.git
cd nlp-text-clustering

pip install pandas scikit-learn matplotlib openpyxl
```

### Configure the dataset

In `NLP_clustering.py`, update `FILE_PATH` and the Excel sheet name to point to your own dataset.

Example:

```python
FILE_PATH = "path/to/your/error_logs.xlsx"
df = pd.read_excel(FILE_PATH, sheet_name="Sheet1", engine="openpyxl")
```

Make sure your file contains compatible `ERROR MESSAGE` and `LOCATION` columns, or update the column names in the script.

### Run

```bash
python NLP_clustering.py
```

The script prints:

- Top terms for each cluster
- Cluster/category counts
- Error-location vs. cluster distributions
- Example error messages from each cluster

Optional sections in the script can also export cluster assignments back to CSV or Excel.

## What I Learned

This project gave me practical experience with:

- Applying unsupervised learning to noisy real-world text
- Converting natural-language data into machine-learning features
- Evaluating clustering quality
- Interpreting unsupervised model outputs
- Turning clusters into understandable operational categories
- Using NLP techniques for log and error analysis

## Possible Improvements

- Remove hard-coded dataset configuration and replace it with command-line arguments
- Add a reusable preprocessing pipeline
- Automatically select the number of clusters
- Compare K-Means with DBSCAN or hierarchical clustering
- Add dimensionality reduction such as PCA or UMAP for visualization
- Add a small dashboard for interactive cluster exploration
- Add unit tests and a sample synthetic dataset

## Author

**Berkay Caliskan**  
Computer Science — University of Ottawa

[LinkedIn](https://www.linkedin.com/) · [GitHub](https://github.com/berkayclsknn)
