# US Housing Affordability Analysis and Prediction

## Overview
This project analyzes the relationship between **essential living costs** and **housing affordability** in the United States.  
Households are increasingly challenged by rising expenses, making affordability a sensitive issue to address.  

Using open-source datasets from **Kaggle**, this project investigates:

**How do essential living expenses impact the ability of U.S. households to afford housing?**

---

## Objectives
1. Explore cost-of-living data and correlate it with household incomes across U.S. counties.  
2. Analyze housing costs and measure the affordability burden for households.  
3. Apply predictive modeling to forecast affordability trends and housing-related stress.  

---

## Repository Structure
```
.
├─ README.md                # project documentation
├─ requirements.txt         # dependencies
├─ data-analysis.py         # main exploratory data analysis
├─ extra-analysis.py        # prediction analysis based on data
├─ pipeline.py              # end-to-end workflow (analysis + prediction)
├─ pipeline.sh              # shell wrapper for pipeline
├─ test.py                  # basic checks
├─ tests.sh                 # additional shell-based checks
│
├─ analysis-report.pdf      # main technical report
├─ data-report.pdf          # dataset documentation
├─ project-plan.md          # planning document
├─ presentation-video.md    # script for presentation
├─ slides.pdf               # project presentation
```
---   
## Key Metrics and Formulas

### Essential Cost of Living to Income Ratio (ECLIR)

$$
\mathrm{ECLIR}(s) = \frac{\text{Essential Living Expenses}_s}{\text{Median Household Income}_s} \times 100
$$

This ratio measures the percentage of a household's income spent on essential living costs in state/county \(s\).

### Housing Cost Burden (HCB)

$$
\mathrm{HCB}(s) = \frac{\text{Median Housing Expenses}_s}{\text{Median Household Income}_s} \times 100
$$

Housing is considered affordable if HCB ≤ 30%. Higher values indicate households are housing-burdened.

### Price-to-Income Ratio (PIR)

$$
\mathrm{PIR}(s) = \frac{\text{Median House Price}_s}{\text{Median Annual Household Income}_s}
$$

The PIR indicates how many years of income are needed to purchase a median-priced home in state/county \(s\).  

---  

## Methods
- **Data Cleaning & Preprocessing** of Kaggle datasets  
- **Exploratory Data Analysis (EDA)** with visualization  
- **Predictive Modeling** of affordability metrics  
- **Correlation Analysis** between living expenses and household income  

---

## Tools & Technologies
- Python (pandas, scikit-learn, matplotlib, seaborn)  
- Jupyter Notebook / VS Code  
- Shell scripting (pipeline automation)  

---

## Quickstart

Clone this repository:
```bash
git clone https://github.com/xhensilahoxha/US-Housing-Affordability-Analysis-and-Prediction.git
cd US-Housing-Affordability-Analysis-and-Prediction
```

Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows PowerShell

pip install -r requirements.txt
```

Run the full pipeline:
```bash
python pipeline.py
```

Or use the shell wrapper:
```bash
bash pipeline.sh
```

---

## Data Sources
The datasets used in this project were retrieved from **Kaggle** and adapted for analysis:
- [US Cost of Living Dataset](https://www.kaggle.com/datasets/asaniczka/us-cost-of-living-dataset-3171-counties)  
- [US House Listings Dataset](https://www.kaggle.com/datasets/febinphilips/us-house-listings-2023)  

---

## Outputs
- `analysis-report.pdf` — technical analysis and results  
- `data-report.pdf` — dataset documentation  
- `slides.pdf` — project presentation  

---

## Testing
Run lightweight checks:
```bash
python test.py
bash tests.sh
```

---

## License
This project is released under the [MIT License](LICENSE).

---

## Acknowledgements
This work was carried out as part of the **Methods of Advanced Data Engineering (MADE)** module at **FAU Erlangen-Nürnberg**.
