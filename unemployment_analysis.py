"""
CodeAlpha Task 2 — Unemployment Analysis with Python
Run:
    python src/unemployment_analysis.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_MAIN = ROOT / "data" / "unemployment_india.csv"
DATA_COVID = ROOT / "data" / "unemployment_rate_upto_11_2020.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

RATE = "Estimated Unemployment Rate (%)"
EMP = "Estimated Employed"

# ---------- Main dataset ----------
df = pd.read_csv(DATA_MAIN)
df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# The supplied file contains 28 blank rows and duplicate records.
before = len(df)
duplicate_rows = int(df.duplicated().sum())
df = df.dropna(subset=["Region", "Date", RATE])
df = df.drop_duplicates().copy()

# ---------- Overall monthly trend ----------
monthly = df.groupby("Date")[RATE].mean().sort_index()
monthly.to_csv(OUT / "monthly_unemployment_rate.csv", header=True)

plt.figure(figsize=(10, 5))
plt.plot(monthly.index, monthly.values, marker="o")
plt.axvline(pd.Timestamp("2020-03-01"), linestyle="--", label="COVID-19 period")
plt.title("Average Unemployment Rate in India")
plt.xlabel("Date")
plt.ylabel("Unemployment rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "monthly_unemployment_trend.png", dpi=180)
plt.close()

# ---------- Rural vs urban ----------
area = df.groupby(["Date", "Area"])[RATE].mean().unstack()
area.to_csv(OUT / "rural_vs_urban.csv")

plt.figure(figsize=(10, 5))
for col in area.columns:
    plt.plot(area.index, area[col], marker="o", label=col)
plt.axvline(pd.Timestamp("2020-03-01"), linestyle="--")
plt.title("Rural vs Urban Unemployment Rate")
plt.xlabel("Date")
plt.ylabel("Unemployment rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "rural_vs_urban.png", dpi=180)
plt.close()

# ---------- State/region averages ----------
region_avg = df.groupby("Region")[RATE].agg(["mean", "min", "max", "count"]).sort_values("mean", ascending=False)
region_avg.to_csv(OUT / "region_summary.csv")

top10 = region_avg.head(10).sort_values("mean")
plt.figure(figsize=(9, 6))
plt.barh(top10.index, top10["mean"])
plt.title("Top 10 Regions by Average Unemployment Rate")
plt.xlabel("Average unemployment rate (%)")
plt.tight_layout()
plt.savefig(OUT / "top_10_regions.png", dpi=180)
plt.close()

# ---------- COVID-19 comparison using the supplemental dataset ----------
covid = pd.read_csv(DATA_COVID)
covid.columns = [c.strip() for c in covid.columns]
covid["Date"] = pd.to_datetime(covid["Date"], dayfirst=True, errors="coerce")

covid_monthly = covid.groupby("Date")[[RATE, EMP]].mean().sort_index()
covid_monthly.to_csv(OUT / "covid_monthly_summary.csv")

pre_covid = covid_monthly.loc[covid_monthly.index <= "2020-02-29"]
covid_shock = covid_monthly.loc[
    (covid_monthly.index >= "2020-03-31") &
    (covid_monthly.index <= "2020-05-31")
]
post_shock = covid_monthly.loc[covid_monthly.index >= "2020-06-30"]

pre_rate = pre_covid[RATE].mean()
shock_rate = covid_shock[RATE].mean()
pre_emp = pre_covid[EMP].mean()
shock_emp = covid_shock[EMP].mean()

summary = f"""DATA QUALITY
Main dataset rows before cleaning: {before}
Blank/missing-key rows removed: {before - len(df)}
Duplicate rows detected in supplied main file: {duplicate_rows}
Rows after cleaning: {len(df)}

COVID-19 ANALYSIS
Average unemployment rate, Jan-Feb 2020: {pre_rate:.2f}%
Average unemployment rate, Mar-May 2020: {shock_rate:.2f}%
Increase in unemployment rate: {shock_rate-pre_rate:.2f} percentage points
Relative increase: {(shock_rate/pre_rate-1)*100:.1f}%

Average estimated employed, Jan-Feb 2020: {pre_emp:,.0f}
Average estimated employed, Mar-May 2020: {shock_emp:,.0f}
Change in estimated employed: {(shock_emp/pre_emp-1)*100:.1f}%

INTERPRETATION
The data show a sharp unemployment shock in April-May 2020, followed by a substantial decline in unemployment from June onward. The pattern is consistent with a major labor-market disruption during the COVID-19 period, followed by partial recovery.
"""
(OUT / "analysis_summary.txt").write_text(summary, encoding="utf-8")

plt.figure(figsize=(10, 5))
plt.plot(covid_monthly.index, covid_monthly[RATE], marker="o")
plt.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-05-31"), alpha=0.15, label="COVID-19 shock period")
plt.title("COVID-19 Period: Average Unemployment Rate")
plt.xlabel("Date")
plt.ylabel("Unemployment rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "covid_unemployment_trend.png", dpi=180)
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(covid_monthly.index, covid_monthly[EMP] / 1e6, marker="o")
plt.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-05-31"), alpha=0.15)
plt.title("Estimated Employment During 2020")
plt.xlabel("Date")
plt.ylabel("Estimated employed (millions)")
plt.tight_layout()
plt.savefig(OUT / "employment_2020.png", dpi=180)
plt.close()

print(summary)
print(f"Outputs saved to: {OUT}")
