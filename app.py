import pandas as pd
import joblib
from fastapi import FastAPI

# Global parameters
PORTS_LIST = ['c', 'q', 's', None]
SEX_LIST = ['male', 'female']

# Load model
MODEL = joblib.load('model.joblib')

# FAST API
app = FastAPI()

# Request Example
#?pclass=3&age=17&sibsp=1&parch=2&fare=45.2&embarked=S&sex=male

@app.get("/predict/")
async def make_prediction(pclass: int,
                          age: int,
                          sibsp: int,
                          parch: int,
                          fare: float,
                          sex: str,
                          embarked: str | None = None,
                          ):
    
    response = {"parameters": f"pclass={pclass}, age={age}, sibsp={sibsp}, parch={parch}, fare={fare}, embarked={embarked}, sex={sex}"}
    
    if isinstance(embarked, str) : embarked = embarked.lower() # To handle the None type
    sex = sex.lower()

    if embarked in PORTS_LIST and sex in SEX_LIST:

        # Parameters mapping
        map_ohe = lambda char, arr : [int(el == char) for el in arr]
        embarked_c, embarked_q, embarked_s, _ = map_ohe(embarked, PORTS_LIST)
        sex_female = 0 if sex == 'male' else 1

        # Creating new observation
        new_obs = {'pclass': pclass,
                    'age': age,
                    'sibsp': sibsp,
                    'parch': parch,
                    'fare': fare,
                    'embarked_c': embarked_c,
                    'embarked_q': embarked_q,
                    'embarked_s': embarked_s,
                    'sex_female': sex_female}
        
        new_obs_df = pd.DataFrame([new_obs])
        
        # Try to predict
        try:
            response["survived"] = str(MODEL.predict(new_obs_df)[0])
            response["probabilities"] = str(MODEL.predict_proba(new_obs_df))
            response["status"] = "success"
            response["observation"] = new_obs
            
        except:
            response["status"] = "failure"
            response["error"] = "model couldn't predict"


    else:
        response["status"] = "failure"
        response["error"] = "wrong parameters"

    
    return response