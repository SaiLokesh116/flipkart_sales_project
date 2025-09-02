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

Clone the repository:

git clone https://github.com/SaiLokesh116/flipkart_sales_project.git
cd flipkart_sales_project


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the pipeline:

python src/pipeline.py --raw-dir data/raw --out-dir reports


Reports (CSV, PNG, PDF) will be generated in the reports/ folder. ✅
