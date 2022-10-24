import pandas as pd
from typing import Optional
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import pre.cle as pc

import predict.prediction as pp

# from preprocessing import cleaning as pc


app = FastAPI()

class Property_type(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    OTHERS = "OTHERS"


class Building_state(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    TO_RENOVATE = "TO RENOVATE"
    JUST_RENOVATED = "JUST RENOVATED"
    TO_REBUILD = "TO REBUILD"

class Data(BaseModel):
    area: int
    property_type: Property_type
    rooms_number: int
    zip_code: int
    land_area: Optional[int] = None
    garden: Optional[bool] = None
    garden_area: Optional[int] = None
    equipped_kitchen: Optional[bool] = None
    full_address: Optional[str] = None
    swimming_pool: Optional[bool] = None
    furnished: Optional[bool] = None
    open_fire: Optional[bool] = None
    terrace: Optional[bool] = None
    terrace_area: Optional[int]= None
    facades_number: Optional[int]= None
    building_state: Building_state



@app.get("/")
async def root():
    return {"message": "Alive!"}

@app.post("/predict/")
async def post_data(data: Data = Body(embed=True)):
    if data.area  == 0:
        raise HTTPException(status_code = 422, detail = "Must provide Area of the property")      
    if data.zip_code  == 0:
        raise HTTPException(status_code = 422, detail = "Must provide the zip-code of the property") 
    if data.rooms_number  == 0:
        raise HTTPException(status_code = 422, detail = "Must provide number of rooms")
    
    df = pd.DataFrame.from_dict([data.dict()])
    df = pc.preprocessing(df)
    pred = pp.prediction(df)
    print(pred)
    prediction_dict = {"Prediction" : pred[0]}
    print(data.dict())
    return prediction_dict