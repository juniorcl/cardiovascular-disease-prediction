from joblib import load
import numpy as np
import pandas as pd


def getLifeStage(age):
    if age <= 3:
        life_stage = "Infancy"
    
    elif age > 3 and age <= 6:
        life_stage = "Early Childhood"
        
    elif age > 6 and age <= 8:
        life_stage = "Middle Childhood"
        
    elif age >= 9 and age <= 11:
        life_stage = "Late Childhood"
        
    elif age >= 12 and age <= 20:
        life_stage = "Adolescence"
        
    elif age > 20 and age <= 35:
        life_stage = "Early Adulthood"
        
    elif age > 35 and age <= 50:
        life_stage = "Midlife"
        
    elif age > 50 and age <= 80:
        life_stage = "Mature Adulthood"
        
    else:
        life_stage = "Late Adulthood"
        
    return life_stage


def calcIBM(weight, height):
    #BMI = kg/m2
    ibm = np.round(weight / (height**2), 1)
    
    return ibm


def catIBM(ibm):
    if ibm < 18.5:
        status = "Underweight"
    
    elif ibm >= 18.5 and ibm <= 24.9:
        status = "Healthy"
    
    elif ibm >= 25.0 and ibm <= 29.9:
        status = "Overweight"
        
    elif ibm >= 30.0:
        status = "Obese"
        
    return status


class Cardio():
    
    def __init__(self):
        
        self.scaler = load("../parameters/robust_scaler.joblib")
            
    def data_cleaning(self, df1):
        
        new_columns = {"ap_hi": "systolic_blood_pressure", "ap_lo": "diastolic_blood_pressure", "gluc": "glucose",
              "smoke": "smoking", "alco": "alcohol", "active": "physical_activity", "cardio": "disease"}
        df1.rename(columns=new_columns, inplace=True)
    
        df1 = df1[(df1["systolic_blood_pressure"] < 300) & (df1["systolic_blood_pressure"] > 0)]
        df1 = df1[(df1["diastolic_blood_pressure"] < 300) & (df1["diastolic_blood_pressure"] > 0)]
    
        return df1
    
    def feature_engineering(self, df2):
        
        df2["age_year"] = df2["age"].apply(lambda i: np.int(np.round(i / 365)))
        df2["life_stage"] = df2["age_year"].apply(getLifeStage)
        
        df2["IBM"] = df2[["height", "weight"]].apply(lambda i: calcIBM(i["weight"], i["height"]/100), axis=1)
        df2["weight_status"] = df2["IBM"].apply(catIBM)
        
        df2 = df2.drop("age", axis=1)
        
        return df2
    
    def data_preparation(self, df3):
        
        #recaling
        df3[["height", "weight", "systolic_blood_pressure", "diastolic_blood_pressure", "age_year", "IBM"]] = self.scaler.transform(df3[["height", "weight", "systolic_blood_pressure", "diastolic_blood_pressure", "age_year", "IBM"]])
        
        #selected columns
        best_columns = ['height', 'weight', 'systolic_blood_pressure', 'diastolic_blood_pressure', 'age_year', 'IBM']
        
        return df3[best_columns]
    
    def get_prediction(self, model, original_data, test_data):
        
        pred = model.predict(test_data)
        
        original_data["prediction"] = pred
        
        return original_data.to_json(orient="records", date_format="iso") 
