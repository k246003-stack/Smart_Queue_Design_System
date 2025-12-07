import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.sklearn

DATA_PATH = "data/bank_queue_dataset.csv" 
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df

def prepare_and_train(df):
    # features and label
    X = df[["Transaction_Type","Priority","Teller_Specialization","Teller_Efficiency","Queue_Length_At_Arrival","Wait_Time"]]
    y = df["Service_Time"]

    categorical = ["Transaction_Type","Priority","Teller_Specialization"]
    numeric = ["Teller_Efficiency","Queue_Length_At_Arrival","Wait_Time"]

    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ], remainder="passthrough")

    pipeline = Pipeline([
        ("pre", preprocessor),
        ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("smart-queue-experiment")
    with mlflow.start_run():
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_val)
        mse = np.mean((preds - y_val)**2)
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(pipeline, "model")
        model_path = os.path.join(MODEL_DIR, "rf_queue_model.pkl")
        joblib.dump(pipeline, model_path)
        print("Saved model to", model_path)
        return pipeline

if __name__ == "__main__":
    df = load_data()
    prepare_and_train(df)
