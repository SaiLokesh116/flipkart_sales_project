# Flipkart Sales Project

## 📌 Overview
This project analyzes Flipkart sales data to generate meaningful insights such as:
- Monthly sales trends
- Product-wise performance
- Regional sales distribution
- Summary reports (CSV, PNG, PDF)
The pipeline handles raw data ingestion, cleaning, transformation, and report generation.

## 📂 Project Structure

flipkart_sales_project/
│
├── data/
│ ├── raw/ # Raw input files (CSV, JSON, XLSX, etc.)
│ └── processed/ # Intermediate cleaned data
│
├── reports/ # Generated reports (CSV, PNG, PDF)
│
├── src/ # Source code
│ ├── generate_data.py # Script to generate sample datasets
│ └── pipeline.py # Main data pipeline
│
└── README.md # Project documentation

#requirements

pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
tabulate>=0.9.0
reportlab>=3.6.0
openpyxl>=3.1.0


#Quick Start

Setup Guide – ELMS Application
1. Clone the Repository
git clone https://github.com/SaiLokesh116/flipkart_sales_project.git
cd flipkart_sales_project

2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux

3. Install Dependencies
pip install -r requirements.txt

4. Running the Application

Execute the pipeline to process raw sales data and generate reports:

python src/pipeline.py --raw-dir data/raw --out-dir reports


Input data is read from data/raw/ (CSV, JSON, Excel supported).

Cleaned and transformed reports are generated inside the reports/ folder (CSV summaries, visualizations, and PDF).

5. Testing the Application

To validate that the pipeline works end-to-end:

Ensure raw datasets are available in data/raw/.

Run the pipeline (as above).

Verify that the following outputs are created in reports/:

monthly_sales.csv, regional_sales.csv, product_sales.csv

monthly_trend.png, regional_sales.png, product_sales.png

summary_report.pdf

If all outputs are generated successfully, the ELMS application setup is correct. ✅
