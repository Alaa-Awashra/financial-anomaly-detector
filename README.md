# Financial Anomaly Detector

This project is a Python-based audit assistant developed to detect anomalies in corporate income statements. It implements multiple statistical techniques to identify unusual financial patterns that may indicate errors, fraud, or accounting inconsistencies.

## Description

The tool applies the following anomaly detection methods:

- Z-Score based outlier detection
- Interquartile Range (IQR) method
- Quarter-over-quarter percentage change threshold (±40%)

It is designed to support accounting research, auditing education, and basic forensic financial analysis.

## Datasets

Three corporate cases are included:

1. **Apple Inc.** – Used as a baseline with expected normal behavior
2. **Wirecard AG (converted to USD)** – Real-world example with known financial fraud
3. **Synthetic Company** – Artificially injected anomalies for testing algorithm sensitivity

## Features

- Highlights abnormal changes in revenue, gross profit, operating income, and net income
- Plots anomaly detection results using matplotlib and seaborn
- Supports datasets with low variance or short histories
- Designed for transparency, reproducibility, and academic extension

## Requirements

Make sure the following Python packages are installed:

```bash
pip install pandas matplotlib seaborn numpy
