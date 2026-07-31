# CodeAlpha — Unemployment Analysis with Python

## Internship Task 2

This project analyzes unemployment in India using the supplied datasets. The analysis covers:

- Data cleaning and quality checks
- Monthly unemployment trends
- Rural vs urban differences
- Regional/state-level patterns
- The COVID-19 labor-market shock
- Changes in estimated employment during 2020

### Datasets

Two supplied CSV files are included:

1. `data/unemployment_india.csv` — the main dataset covering May 2019 to June 2020 and including Rural/Urban observations.
2. `data/unemployment_rate_upto_11_2020.csv` — a supplemental 2020 dataset used to extend the COVID-period trend through October 2020.

### Data cleaning

The main dataset contains 28 blank rows and duplicate records. Rows missing the region, date, or unemployment-rate value were removed, and duplicate rows were dropped.

After cleaning, **740 usable observations** remained.

### Key findings

- The overall average unemployment rate in the main dataset rose from **9.96% in February 2020** to **23.64% in April 2020** and **24.88% in May 2020**.
- The supplemental 2020 dataset shows an average unemployment rate of about **9.23% in January-February 2020** versus **18.75% in March-May 2020**, an increase of about **9.52 percentage points**.
- Average estimated employment in the supplemental dataset fell by about **21.6%** between the January-February baseline and March-May 2020.
- Urban unemployment was generally higher than rural unemployment in the main dataset, with a particularly strong urban increase during April-May 2020.
- Tripura, Haryana, Jharkhand, Bihar, and Himachal Pradesh were among the regions with the highest average unemployment rates in the supplied main dataset.

### COVID-19 interpretation

The strongest unemployment spike occurs in April-May 2020, which aligns with the period of severe labor-market disruption associated with COVID-19. The rate falls substantially from June 2020 onward, suggesting partial recovery. These results describe patterns in the supplied data; they should not by themselves be interpreted as a causal estimate of the pandemic's effect.

### Repository structure

```text
CodeAlpha_Unemployment_Analysis/
├── data/
│   ├── unemployment_india.csv
│   └── unemployment_rate_upto_11_2020.csv
├── outputs/
│   ├── analysis_summary.txt
│   ├── monthly_unemployment_rate.csv
│   ├── monthly_unemployment_trend.png
│   ├── rural_vs_urban.csv
│   ├── rural_vs_urban.png
│   ├── region_summary.csv
│   ├── top_10_regions.png
│   ├── covid_monthly_summary.csv
│   ├── covid_unemployment_trend.png
│   └── employment_2020.png
├── src/
│   └── unemployment_analysis.py
├── requirements.txt
└── README.md
```

### Run locally

```bash
pip install -r requirements.txt
python src/unemployment_analysis.py
```

### Skills demonstrated

Python, pandas, data cleaning, exploratory data analysis, time-series aggregation, groupby analysis, data visualization, economic interpretation, and reproducible analysis.
