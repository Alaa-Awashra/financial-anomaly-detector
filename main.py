import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File name
FILE_NAME = "apple_income_statement.csv"

# Load the dataset
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"File '{FILE_NAME}' not found.")
    exit()

# Set visual style
sns.set(style="whitegrid")

# Define constants
MIN_DATA_POINTS = 6
MIN_AVG_NET_INCOME = 1_000_000  # in USD

# Check data validity
if len(df) < MIN_DATA_POINTS:
    print("Not enough data points for reliable anomaly detection (min = 6).")
    exit()

if df['Net Income (M USD)'].mean() * 1e6 < MIN_AVG_NET_INCOME:
    print("Net Income is too low for meaningful anomaly detection (avg < $1M).")
    exit()

# Outlier detection functions
def detect_zscore_outliers(series, threshold=1.5):
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    return np.abs(z_scores) > threshold

def detect_iqr_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return (series < lower) | (series > upper)

def detect_percent_change(series, threshold=40.0):
    pct_change = series.pct_change() * 100
    return pct_change.abs() > threshold

# Apply detection
metrics = ['Revenue (M USD)', 'Gross Profit (M USD)', 'Operating Income (M USD)', 'Net Income (M USD)']

for col in metrics:
    df[f'{col} Z-outlier'] = detect_zscore_outliers(df[col], threshold=1.5)
    df[f'{col} IQR-outlier'] = detect_iqr_outliers(df[col])
    df[f'{col} %Change-outlier'] = detect_percent_change(df[col], threshold=40.0)

# Print summary
summary_cols = ['Quarter'] + [col for col in df.columns if 'outlier' in col]
print("Detection Summary:\n")
print(df[summary_cols])

# Save flagged results
df.to_csv("flagged_output.csv", index=False)

# Plot each metric
for metric in metrics:
    plt.figure(figsize=(12, 6))
    plt.plot(df['Quarter'], df[metric], marker='o', label=metric)

    # Z-score outliers
    z_outliers = df[df[f'{metric} Z-outlier']]
    plt.scatter(z_outliers['Quarter'], z_outliers[metric], color='red', s=100, label='Z-score Outlier', zorder=5)

    # IQR outliers
    iqr_outliers = df[df[f'{metric} IQR-outlier']]
    plt.scatter(iqr_outliers['Quarter'], iqr_outliers[metric], color='orange', s=80, marker='x', label='IQR Outlier', zorder=4)

    # % Change outliers
    pct_outliers = df[df[f'{metric} %Change-outlier']]
    plt.scatter(pct_outliers['Quarter'], pct_outliers[metric], color='blue', s=80, marker='^', label='±40% Change', zorder=3)

    plt.title(f"{metric} - Anomaly Detection")
    plt.xlabel("Quarter")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{metric.replace(' ', '_').replace('(', '').replace(')', '')}_anomalies.png")
    plt.show()
