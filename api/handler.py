import pandas as pd
from joblib import load
from cardio.Cardio import Cardio
from flask import Flask, request, Response

model = load("../models/model_cardio.joblib")
    
# loading
app = Flask(__name__)

@app.route("/cardio/predict", methods=['POST'])
def cardio_predict():
    test_json = request.get_json()
   
    if test_json: # there is data
        
        if isinstance(test_json, dict): # unique example
            test_raw = pd.DataFrame(test_json, index=[0])
            
        else: # multiple example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        pipeline = Cardio()
        
        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        
        # feature engineering
        df2 = pipeline.feature_engineering(df1)
        
        # data preparation
        df3 = pipeline.data_preparation(df2)
        
        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return df_response
        
    else:
        return Response("{}", status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
