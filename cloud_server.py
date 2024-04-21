from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb+srv://mawada1212:k2Tl7AehReFuTfVl@kaha.qbcx70z.mongodb.net/")
db = client["kaha"]
collection = db["kaha_collection"]

class parameters(BaseModel):
    latitude: str
    longitude: str
    panel_number: int
    openingTime: str
    closingTime: str
    InverterType: str
    GeneratorType: str
    generator_max_value: str
    PowerConnection: str

class maxCurrentData(BaseModel):
    value: float
    automatic: bool

class DataInput(BaseModel):
    data: dict

#@app.get("/getCurrent")
#async def get_events():
#    print('Get Charging Current Sent Successfully')
#    return {"message": "3.27 A"}

@app.post("/MaxCurrent")
async def modify_max(data: maxCurrentData):
    result = collection.update_one(
        {"name": "max_charge"},
        {"$set": {
            "change": True,
            "value": data.value,
            "automatic": data.automatic
        }}
    )

    if result.modified_count == 1:
        return {"message": "Max current data updated successfully"}
    else:
        return {"message": "Failed to update max current data"}
    
@app.get("/getMaxCurrent")
async def getMaxCurrent():
    document = str(collection.find_one({"name": "max_charge"}))
    result = collection.update_one(
        {"name": "max_charge"},
        {"$set": {
            "change": False,
        }}
    )
    if document:
        return document
    else:
        return {"message": "No data found"}
    
@app.get("/data")
async def process_data():
    document = collection.find_one({"name": "data"})
    if document:
        values = document.get("values")
        return values
    else:
        return {"message": "No data found"}
    
@app.post("/UpdateData")
async def update_data(data_input: DataInput):
    result = collection.update_one(
        {"name": "data"},
        {"$set": {"values": data_input.data}},
    )

    if result.modified_count == 1:
        return {"message": "Data updated successfully"}
    else:
        return {"message": "Failed to update data"}

@app.post("/parameters")
async def modify_parameters(data: parameters):
    result = collection.update_one(
        {"name": "parameters"},
        {"$set": {
            "latitude": data.latitude,
            "generator_max_value": data.generator_max_value,
            "PowerConnection": data.PowerConnection,
            "longitude": data.longitude,
            "panel_number": data.panel_number,
            "change": True,
            "openingTime": data.openingTime,
            "closingTime": data.closingTime,
            "InverterType": data.InverterType,
            "GeneratorType": data.GeneratorType
        }}
    )

    if result.modified_count == 1:
        return {"message": "parameters updated successfully"}
    else:
        return {"message": "Failed to update parameters"}
    
@app.get("/getParameters")
async def getParameters():
    document = str(collection.find_one({"name": "parameters"}))
    result = collection.update_one(
        {"name": "parameters"},
        {"$set": {
            "change": False
        }}
    )
    if document:
        return document
    else:
        return {"message": "No data found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


