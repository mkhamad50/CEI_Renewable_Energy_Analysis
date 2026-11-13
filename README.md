# Capacity-to-Generation Conversion Efficiency (CEI) Analysis

This repository contains the Python code, dataset, and generated outputs for the research paper: 
**"Assessing Capacity-to-Generation Conversion Efficiency in Renewable Energy Systems: A Comparative Study of Selected Economies"**

## 📌 Overview
This project provides a quantitative framework to evaluate the actual conversion efficiency of installed renewable energy capacity into usable electricity. The code calculates the **Capacity-to-Generation Conversion Efficiency (CEI)**, the **Compound Annual Growth Rate (CAGR) Gap Index**, and the **Marginal Conversion Efficiency** (via linear regression) for solar and wind energy in six selected economies: China, the United States, India, Germany, Brazil, and Morocco. 

The script automatically generates all the statistical tables and high-resolution figures (300 DPI) presented in the manuscript.

## 📊 Data Source
The analysis relies on the **Ember Yearly Electricity Data**, accessed via the World Power Monitor platform. 
* **Original Dataset URL:** [Ember Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/)
* **Accessed via:** [World Power Monitor](https://worldpowermonitor.com/data/ember-annual/)
* **Dataset File:** `ember-annual-generation.csv` (included in this repository, 231,324 rows, covering 1985–2025).

## ⚙️ Prerequisites
Ensure you have Python 3.8 or higher installed. The required libraries are listed in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt