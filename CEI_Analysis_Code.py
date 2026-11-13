# ==============================================================================
# Title: Assessing Capacity-to-Generation Conversion Efficiency (CEI)
# Description: This script calculates the CEI, CAGR Gap Index, and Marginal 
#              Efficiency for solar and wind energy in six selected economies.
# Data Source: Ember Annual Generation Dataset (via World Power Monitor)
# ==============================================================================

# 1. Import Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# Set high-resolution plotting for academic publications
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# ==============================================================================
# 2. Data Loading and Preprocessing
# ==============================================================================
# Load the dataset (Ensure 'ember-annual-generation.csv' is in the working directory)
file_name = 'ember-annual-generation.csv'
ember = pd.read_csv(file_name)

# Extract Generation (TWh) for Solar and Wind
gen = ember[
    (ember['metric'] == 'generation') &
    (ember['fuel'].isin(['solar', 'wind'])) &
    (ember['unit'] == 'TWh')
][['country', 'year', 'fuel', 'value']].copy()
gen.columns = ['Country', 'Year', 'Source', 'Generation_TWh']
gen['Source'] = gen['Source'].str.capitalize()

# Extract Installed Capacity (GW) for Solar and Wind
cap = ember[
    (ember['metric'] == 'installed_capacity') &
    (ember['fuel'].isin(['solar', 'wind'])) &
    (ember['unit'] == 'GW')
][['country', 'year', 'fuel', 'value']].copy()
cap.columns = ['Country', 'Year', 'Source', 'Capacity_GW']
cap['Source'] = cap['Source'].str.capitalize()

# Merge datasets
merged = pd.merge(gen, cap, on=['Country', 'Year', 'Source'], how='inner')

# ==============================================================================
# 3. Metric Calculations
# ==============================================================================
# Metric 1: Capacity-to-Generation Conversion Efficiency (CEI)
# CEI = Generation (TWh) / (Capacity (GW) * 8.76)
# 8.76 is the theoretical maximum TWh from 1 GW running 100% for a year.
merged['CEI'] = merged['Generation_TWh'] / (merged['Capacity_GW'] * 8.76)

# Filter out physically impossible values (CEI > 1) and zeros
merged = merged[(merged['CEI'] > 0) & (merged['CEI'] <= 1)].copy()

# Define Target Countries
target_countries = ['China', 'United States', 'India', 'Germany', 'Brazil', 'Morocco']
available = merged['Country'].unique()
actual_names = {}

for tc in target_countries:
    matches = [a for a in available if tc.lower() in a.lower() or a.lower() in tc.lower()]
    if matches:
        actual_names[tc] = matches[0]

# ==============================================================================
# 4. Visualizations (Figures 1, 2, and 3)
# ==============================================================================

# Figure 1: Solar CEI Trend
solar_data = merged[merged['Source'] == 'Solar']
fig, ax = plt.subplots(figsize=(10, 6))
for tc, actual in actual_names.items():
    data = solar_data[solar_data['Country'] == actual].sort_values('Year')
    if len(data) > 2:
        ax.plot(data['Year'], data['CEI'], marker='o', label=tc, linewidth=2, markersize=6)

ax.set_title('Solar Capacity-to-Generation Conversion Efficiency (CEI)\nSelected Economies, 2000–2025', fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('CEI (Actual Generation / Theoretical Maximum)')
ax.legend(loc='best', frameon=True)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Fig1_Solar_CEI_Trend.png', dpi=300)
plt.show()

# Figure 2: Wind CEI Trend
wind_data = merged[merged['Source'] == 'Wind']
fig, ax = plt.subplots(figsize=(10, 6))
for tc, actual in actual_names.items():
    data = wind_data[wind_data['Country'] == actual].sort_values('Year')
    if len(data) > 2:
        ax.plot(data['Year'], data['CEI'], marker='s', label=tc, linewidth=2, markersize=6)

ax.set_title('Wind Capacity-to-Generation Conversion Efficiency (CEI)\nSelected Economies, 2000–2025', fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('CEI (Actual Generation / Theoretical Maximum)')
ax.legend(loc='best', frameon=True)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Fig2_Wind_CEI_Trend.png', dpi=300)
plt.show()

# ==============================================================================
# 5. Table Generation (Tables 1, 2, and 3)
# ==============================================================================

# --- Table 1: CEI for 2025 ---
latest_year = merged['Year'].max()
latest = merged[merged['Year'] == latest_year]
pivot = latest.pivot_table(index='Country', columns='Source', values='CEI', aggfunc='first')
selected_actual = [v for v in actual_names.values() if v in pivot.index]
cei_table = pivot.loc[selected_actual].round(3)
cei_table.to_csv('Table1_CEI_2025.csv')
print(f"\n=== Table 1: CEI for {latest_year} ===\n", cei_table)

# --- Table 2: CAGR Gap Analysis ---
gap_results = []
for tc, actual in actual_names.items():
    for source in ['Solar', 'Wind']:
        data = merged[(merged['Country'] == actual) & (merged['Source'] == source)].sort_values('Year')
        d2015 = data[data['Year'] == 2015]
        dlatest = data[data['Year'] == latest_year]

        if len(d2015) > 0 and len(dlatest) > 0:
            cap0, cap1 = d2015['Capacity_GW'].values[0], dlatest['Capacity_GW'].values[0]
            gen0, gen1 = d2015['Generation_TWh'].values[0], dlatest['Generation_TWh'].values[0]

            if cap0 > 0.001 and gen0 > 0.001:
                years = latest_year - 2015
                cap_cagr = (cap1 / cap0) ** (1 / years) - 1
                gen_cagr = (gen1 / gen0) ** (1 / years) - 1
                gap = (cap_cagr - gen_cagr) * 100

                gap_results.append({
                    'Country': tc, 'Source': source,
                    'Capacity_CAGR_%': round(cap_cagr * 100, 2),
                    'Generation_CAGR_%': round(gen_cagr * 100, 2),
                    'Gap_Index_%': round(gap, 2)
                })
gap_df = pd.DataFrame(gap_results)
gap_df.to_csv('Table2_Gap_Index_CAGR.csv', index=False)
print("\n=== Table 2: CAGR and Gap Index ===\n", gap_df.to_string(index=False))

# --- Table 3: Linear Regression & Marginal Efficiency ---
regression_results = []
for tc, actual in actual_names.items():
    for source in ['Solar', 'Wind']:
        data = merged[(merged['Country'] == actual) & (merged['Source'] == source)].sort_values('Year')
        if len(data) >= 5:
            X = data['Capacity_GW'].values.reshape(-1, 1)
            y = data['Generation_TWh'].values
            model = LinearRegression().fit(X, y)
            beta1 = model.coef_[0]
            r2 = model.score(X, y)
            marginal_efficiency = (beta1 / 8.76) * 100

            regression_results.append({
                'Country': tc, 'Source': source,
                'Beta1 (TWh/GW)': round(beta1, 4),
                'R2': round(r2, 4),
                'Marginal_Efficiency_%': round(marginal_efficiency, 2)
            })
reg_df = pd.DataFrame(regression_results)
reg_df.to_csv('Table3_Linear_Regression.csv', index=False)
print("\n=== Table 3: Linear Regression ===\n", reg_df.to_string(index=False))

# --- Figure 3: Gap Heatmap ---
if len(gap_df) > 0:
    gap_pivot = gap_df.pivot(index='Country', columns='Source', values='Gap_Index_%')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(gap_pivot, annot=True, fmt='.1f', cmap='RdBu_r', center=0, linewidths=0.5, ax=ax)
    ax.set_title('Gap Index (CAGR Difference) 2015–2025', fontweight='bold')
    plt.tight_layout()
    plt.savefig('Fig3_Gap_Heatmap.png', dpi=300)
    plt.show()

print("\n? Execution complete. All tables and figures have been saved.")