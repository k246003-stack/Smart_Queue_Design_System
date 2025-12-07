# **Smart Queue Design System**

A complete end-to-end queue optimization and teller assignment system that uses synthetic data generation, machine learning prediction, and smart scheduling logic to improve service flow in environments such as banks, hospitals, or customer service centers.

This project includes:

Synthetic queue dataset generation

ML model training (Random Forest)

Teller assignment scheduler

REST API (FastAPI)

Web dashboard (Flask UI)

# **Project Overview** 

The Smart Queue System predicts customer service times using machine learning and then assigns customers to the most suitable teller based on:

1. Teller specialization

2. Teller efficiency

3. Estimated wait time

4. Current workload

It improves queue management by balancing teller load and reducing customer waiting time.



### **1. Generate Synthetic Queue Data**
Use data_generator.py to create a dataset of simulated bank customers and their queue behaviors.

### **🤖 2. Train the Machine Learning Model**

model_trainer.py trains a RandomForestRegressor that predicts expected service time.

### **3. Teller Assignment Scheduler**

The scheduling logic (in scheduler.py) chooses the best teller based on:

1. ✔ Specialization match
2. ✔ Teller availability
3. ✔ Efficiency
4. ✔ Customer arrival time
5. ✔ Predicted service time

The scheduler outputs:

1. Assigned teller

2. Start & end time

3. Effective service duration


### ** 4. FastAPI Backend** 

main.py provides a REST endpoint:

#### POST /predict-and-assign

Predicts the service time and assigns the best teller.


### **5. Flask Web Dashboard**

A simple frontend for interacting with the backend API.

The dashboard lets users:

Enter customer details

Send request to backend

View predicted service time

See assigned teller & timestamps



## ** Technologies Used**

Python

FastAPI & Flask

RandomForest (scikit-learn)

MLflow

NumPy, Pandas

Joblib

Uvicorn

Time-based scheduling


## ** Future Improvements**

Real-time dashboard with WebSockets

Database integration (PostgreSQL / MongoDB)

Reinforcement-learning based teller allocation

Mobile UI

Live queue simulation engine

