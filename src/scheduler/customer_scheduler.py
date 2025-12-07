from datetime import datetime, timedelta, time

class Teller:
    def __init__(self, teller_id, specialization, efficiency):
        self.teller_id = teller_id
        self.specialization = specialization
        self.efficiency = efficiency
        
        # FIX: Proper date + time (today at 09:00)
        today = datetime.now().date()
        self.available_at = datetime.combine(today, time(9, 0))

def assign_customer(customer, tellers):
    best = None
    best_score = None

    for t in tellers:

        # penalty for mismatch specialization
        spec_penalty = 0 if (
            t.specialization == "General" or
            (customer["Transaction_Type"] == "New Account" and t.specialization == "Accounts") or
            (customer["Transaction_Type"] == "Loan Inquiry" and t.specialization == "Loans")
        ) else 2

        available_at = t.available_at

        # Calculate waiting minutes
        wait_if_assigned = max(0, (available_at - customer["Arrival_Time"]).total_seconds() / 60)

        # SAFE SCORE CALCULATION (timestamp now valid)
        score = available_at.timestamp() + spec_penalty * 60 + wait_if_assigned * 10 - t.efficiency * 5

        if best is None or score < best_score:
            best = t
            best_score = score

    # service duration adjusted by efficiency
    service_duration = max(1, int(round(customer["Predicted_Service_Time"] / best.efficiency)))

    start_time = max(best.available_at, customer["Arrival_Time"])
    end_time = start_time + timedelta(minutes=service_duration)

    best.available_at = end_time

    return {
        "Assigned_Teller": best.teller_id,
        "Start_Time": start_time,
        "Service_Duration": service_duration,
        "End_Time": end_time
    }
