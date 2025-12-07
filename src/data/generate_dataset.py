import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import argparse

def generate_queue_data(num_customers=5000, seed=42, save_path="data/bank_queue_dataset.csv"):
    random.seed(seed)
    np.random.seed(seed)

    transaction_types = {
        "Deposit": (3, 6, 0.40),
        "Withdrawal": (2, 5, 0.30),
        "New Account": (20, 35, 0.08),
        "Loan Inquiry": (10, 25, 0.10),
        "Utility Payment": (4, 8, 0.12)
    }

    priorities = ["Regular", "VIP", "Senior"]
    tellers = [
        {"Teller_ID": "T01", "Specialization": "General", "Efficiency": 0.95},
        {"Teller_ID": "T02", "Specialization": "Accounts", "Efficiency": 0.85},
        {"Teller_ID": "T03", "Specialization": "General", "Efficiency": 0.90},
        {"Teller_ID": "T04", "Specialization": "Loans", "Efficiency": 0.80},
        {"Teller_ID": "T05", "Specialization": "General", "Efficiency": 0.92},
    ]

    trx_names = list(transaction_types.keys())
    trx_probs = [transaction_types[t][2] for t in trx_names]

    data = []
    start_time = datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time())
    teller_available_at = {t["Teller_ID"]: start_time for t in tellers}
    last_arrival = start_time

    for i in range(num_customers):
        customer_id = f"C{i+1:05d}"
        gap = np.random.poisson(3)
        if np.random.rand() < 0.15:
            gap = max(1, np.random.randint(0,3))
        arrival_time = last_arrival + timedelta(minutes=int(gap))
        last_arrival = arrival_time

        trx_type = np.random.choice(trx_names, p=trx_probs)
        low, high, _ = transaction_types[trx_type]
        service_time = max(1, int(np.round(np.random.normal((low+high)/2, (high-low)/4))))
        service_time = min(max(service_time, low), high)

        priority = np.random.choice(priorities, p=[0.85, 0.05, 0.10])

        preferred_tellers = [t for t in tellers if (t["Specialization"] == "General" or (trx_type == "New Account" and t["Specialization"]=="Accounts") or (trx_type=="Loan Inquiry" and t["Specialization"]=="Loans"))]
        teller = random.choice(preferred_tellers) if preferred_tellers and np.random.rand() < 0.80 else random.choice(tellers)

        adjusted_service_time = max(1, int(np.round(service_time * (1.0 / teller["Efficiency"]))))
        teller_free_time = teller_available_at[teller["Teller_ID"]]
        service_start_time = max(arrival_time, teller_free_time)
        wait_time = int((service_start_time - arrival_time).total_seconds() // 60)
        queue_length = sum(1 for t_id, free_time in teller_available_at.items() if free_time > arrival_time)
        teller_available_at[teller["Teller_ID"]] = service_start_time + timedelta(minutes=adjusted_service_time)

        data.append({
            "Customer_ID": customer_id,
            "Arrival_Time": arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Transaction_Type": trx_type,
            "Priority": priority,
            "Teller_ID": teller["Teller_ID"],
            "Teller_Specialization": teller["Specialization"],
            "Teller_Efficiency": round(teller["Efficiency"], 2),
            "Service_Time": adjusted_service_time,
            "Wait_Time": wait_time,
            "Queue_Length_At_Arrival": queue_length
        })

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Saved {len(df)} rows to {save_path}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5000)
    parser.add_argument("--out", type=str, default="data/bank_queue_dataset.csv")
    args = parser.parse_args()
    generate_queue_data(num_customers=args.n, save_path=args.out)
