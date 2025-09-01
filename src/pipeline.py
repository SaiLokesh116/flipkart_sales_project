import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# ----------------------------
# Data Loading
# ----------------------------
def load_and_merge_datasets(raw_dir: str) -> pd.DataFrame:
    """Load CSV, JSON, and Excel files from raw_dir and merge into a single DataFrame."""
    import os
    import pandas as pd

    frames = []
    required = {"order_id", "date", "region", "product", "quantity", "unit_price", "discount"}

    for file in os.listdir(raw_dir):
        path = os.path.join(raw_dir, file)
        try:
            if file.endswith(".csv"):
                df = pd.read_csv(path)
            elif file.endswith(".json"):
                try:
                    df = pd.read_json(path, lines=True)  # JSONL
                except Exception:
                    df = pd.read_json(path)  # Normal JSON
            elif file.endswith(".xlsx"):
                df = pd.read_excel(path)
            else:
                print(f"[PIPELINE] Skipping unsupported file {file}")
                continue
        except Exception as e:
            print(f"[PIPELINE] Could not read {file}: {e}")
            continue

        # ✅ Skip invalid datasets
        if not required.issubset(df.columns):
            missing = required - set(df.columns)
            print(f"[PIPELINE] Skipping {file} (missing {missing})")
            continue

        print(f"[PIPELINE] Loaded {file} -> {df.shape}")
        frames.append(df)

    if not frames:
        raise ValueError(f"No valid datasets found in {raw_dir}")

    return pd.concat(frames, ignore_index=True)


# ----------------------------
# Data Cleaning
# ----------------------------
def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform sales data."""
    df = df.copy()

    # Ensure correct dtypes
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)

    # Derived column: revenue
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])

    return df


# ----------------------------
# EDA & Reports
# ----------------------------
def analyze_sales(df: pd.DataFrame, out_dir: str):
    """Perform EDA and save reports & plots."""
    os.makedirs(out_dir, exist_ok=True)

    # 1. Monthly sales
    monthly = df.groupby(df["date"].dt.to_period("M")).agg({"revenue": "sum"}).reset_index()
    monthly["date"] = monthly["date"].astype(str)
    monthly.to_csv(os.path.join(out_dir, "monthly_sales.csv"), index=False)

    # 2. Regional sales
    regional = df.groupby("region").agg({"revenue": "sum"}).reset_index()
    regional.to_csv(os.path.join(out_dir, "regional_sales.csv"), index=False)

    # 3. Product sales
    product = df.groupby("product").agg({"revenue": "sum"}).reset_index()
    product.to_csv(os.path.join(out_dir, "product_sales.csv"), index=False)

    # ----------------------------
    # Plots
    # ----------------------------
    plt.figure(figsize=(8, 4))
    sns.lineplot(x="date", y="revenue", data=monthly, marker="o")
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "monthly_trend.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    sns.barplot(x="region", y="revenue", data=regional)
    plt.title("Regional Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "regional_sales.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    sns.barplot(x="product", y="revenue", data=product)
    plt.title("Product Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "product_sales.png"))
    plt.close()

    # ----------------------------
    # PDF Report
    # ----------------------------
    pdf_path = os.path.join(out_dir, "summary_report.pdf")
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    flow = []

    flow.append(Paragraph("Flipkart Sales Report", styles["Title"]))
    flow.append(Spacer(1, 12))

    # Add tables
    for name, table_df in [("Monthly Sales", monthly), ("Regional Sales", regional), ("Product Sales", product)]:
        flow.append(Paragraph(name, styles["Heading2"]))
        flow.append(Spacer(1, 6))
        data = [table_df.columns.tolist()] + table_df.values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        flow.append(table)
        flow.append(Spacer(1, 12))

    doc.build(flow)
    print(f"[PIPELINE] PDF report saved to {pdf_path}")


# ----------------------------
# Runner
# ----------------------------
def run_pipeline(raw_dir: str, out_dir: str):
    print(f"[PIPELINE] Loading raw data from {os.path.abspath(raw_dir)} ...")
    df = load_and_merge_datasets(raw_dir)
    print(f"[PIPELINE] Rows loaded: {len(df)}")

    print("[PIPELINE] Cleaning & transforming ...")
    df = clean_and_transform(df)

    print("[PIPELINE] Running analysis & reports ...")
    analyze_sales(df, out_dir)

    print("[PIPELINE] Done.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=str, default="data/raw", help="Path to raw data")
    parser.add_argument("--out-dir", type=str, default="reports", help="Path to output reports")
    args = parser.parse_args()

    run_pipeline(args.raw_dir, args.out_dir)


if __name__ == "__main__":
    main()
