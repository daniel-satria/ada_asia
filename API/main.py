from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel
from typing import Union
import pickle
import json
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Hello World"}

# Path parameter
@app.get("/items/{item_id}")
def read_item(item_id:int):
    return {"item_id" : "This is response for "+str(item_id)}

# Query Parameter
@app.get("/items/query/{item_id}")
def read_query_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Class as input 
class ModelName(str, Enum):
    alexnet = "alexnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name:ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message":"Deep Learning FTW!"}
    if model_name == "lenet":
        return {"model_name": model_name, "message":"LeCBB all the images"}
    return {"model_name": model_name, "message": "others"}

# Request body
class Item(BaseModel):
    name : str
    description : Union[str, None] = None #default None
    price : float
    tax : Union[float, None] = None #default None

@app.post("/items/")
def create_item(item:Item):
    return item

@app.post("/items/update")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax: 
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Handling error
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/handle/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# For iris classifier
class Ada(BaseModel):
    tcgc_budget : float
    tcgc_type : float
    tcgc_flag_lock : float
    tcm_success : float
    tcm_status_campaign : float
    tcm_channel : float
    feature_tf_id : float
    tcm_inventory_id : float
    tcm_external_entity_id : float




origins = [
    "http://localhost:80",
    "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# loading pipeline preprocess only
pipeline_path = open('model/model_pipeline_ada.pkl', 'rb')
model_ada = pickle.load(pipeline_path)


@app.post("/predict")
def predict_iris(ada:Ada):

    tfgc_status = ""

    if(not(ada)):
        raise HTTPException(status_code=400, 
                            detail = "Please Provide a valid number")
        
    ada_dict = ada.dict()

    data_input = pd.DataFrame([[ada.tcgc_budget,
                                ada.tcgc_type,
                                ada.tcgc_flag_lock,
                                ada.tcm_success,
                                ada.tcm_status_campaign,
                                ada.tcm_channel,
                                ada.feature_tf_id,
                                ada.tcm_inventory_id,
                                ada.tcm_external_entity_id]])
    
    model_result = model_pipeline_ada.transform(data_input)


    if(model_result[0] == 0):
        tfgc_status = "0"

    elif(model_result[0] == -1):
        tfgc_status = "-1"
        
    elif(model_result[0] == 7):
        tfgc_status = "7"

    elif(model_result[0] == 9):
        tfgc_status = "9"

    elif(model_result[0] == 12):
        tfgc_status = "12"
        
    else:
        tfgc_status = "15"
            
    return {
            "tcgc_status": tfgc_status
            }
