from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__, template_folder="templates")

API_URL = "http://localhost:8000/predict-and-assign"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/assign", methods=["POST"])
def assign():
    payload = {
        "Customer_ID": request.form["customer_id"],
        "Arrival_Time": request.form["arrival_time"],
        "Transaction_Type": request.form["transaction_type"],
        "Priority": request.form["priority"],
        "Teller_Specialization": request.form["teller_specialization"],
        "Teller_Efficiency": float(request.form["teller_efficiency"]),
        "Queue_Length_At_Arrival": int(request.form["queue_length"]),
        "Wait_Time": int(request.form["wait_time"])
    }
    r = requests.post(API_URL, json=payload)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)

