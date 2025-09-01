import os, random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sample_data(raw_dir="data/raw", seed=7):
    random.seed(seed)
    np.random.seed(seed)

    os.makedirs(raw_dir, exist_ok=True)

    regions = ["North", "South", "East", "West"]
    products = ["Laptop", "Phone", "Headphones", "Camera", "Smartwatch", "Tablet"]
    payment_methods = ["UPI", "Card", "COD", "Wallet"]

    start = datetime(2025, 1, 1)
    rows = []
    oid = 100000

    for day in range(180):  # ~6 months
        d = start + timedelta(days=day)
        for _ in range(np.random.poisson(40)):  # avg 40 orders/day
            product = random.choice(products)
            qty = max(1, int(np.random.exponential(1.2)))
            base_price = {
                "Laptop": 60000, "Phone": 30000, "Headphones": 3000,
                "Camera": 45000, "Smartwatch": 8000, "Tablet": 20000
            }[product]
            unit_price = float(np.random.normal(base_price, base_price*0.08))
            discount = float(max(0, min(0.35, np.random.beta(2,8))))
            region = random.choice(regions)
            pm = random.choice(payment_methods)
            rows.append({
                "order_id": oid,
                "date": d.strftime("%Y-%m-%d"),
                "region": region,
                "product": product,
                "quantity": qty,
                "unit_price": round(unit_price,2),
                "discount": round(discount,2),
                "payment_method": pm
            })
            oid += 1

    df = pd.DataFrame(rows)

    # introduce missing values
    mask = np.random.rand(len(df)) < 0.01
    df.loc[mask, "discount"] = np.nan
    mask = np.random.rand(len(df)) < 0.005
    df.loc[mask, "region"] = None

    # duplicate some rows
    dup_idx = np.random.choice(df.index, size=100, replace=False)
    df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

    # Save in multiple formats
    df.sample(frac=0.5, random_state=1).to_csv(os.path.join(raw_dir, "sales_part_a.csv"), index=False)
    df.sample(frac=0.3, random_state=2).to_json(os.path.join(raw_dir, "sales_part_b.json"), orient="records", lines=True)
    df.sample(frac=0.4, random_state=3).to_excel(os.path.join(raw_dir, "sales_part_c.xlsx"), index=False)

    print(f"✅ Synthetic data generated in {raw_dir}")

if __name__ == "__main__":
    generate_sample_data()
