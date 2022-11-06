from fastapi import FastAPI
import pymongo
import datetime
import os

MONGODB_URL = os.environ.get("MONGODB_URL")

client = pymongo.MongoClient(MONGODB_URL)

db = client["etikitin"]

app = FastAPI()


@app.get("/get_data/{collection_name}/{_qrcode}")
def read_individual_data(collection_name: str, _qrcode: str):
    collection = db[collection_name]
    info = collection.find_one({"_qrcode": _qrcode})
    name = info["firstname"] + " " + info["lastname"]
    gender = info["gender"]
    scan_status = info["scan_status"]
    scan_date = info["scan_date"]
    scan_time = info["scan_time"]
    print(info)
    return {"name": name, "gender": gender, "scan_status": scan_status, "scan_date": scan_date, "scan_time": scan_time}

@app.get("/data_count/{collection_name}")
def get_data_count(collection_name:str):
    collection = db[collection_name]
    totalDocs = collection.count_documents({})
    oneScanDocs = collection.count_documents({"scan_status": 1})
    twoScanDocs = collection.count_documents({"scan_status": 2})
    
    return {"totalDocs": totalDocs, "oneScanDocs": oneScanDocs, "twoScanDocs": twoScanDocs}

@app.post("/update_in/{collection_name}/{_qrcode}")
def update_record_in(collection_name: str, _qrcode: str):
    collection = db[collection_name]
    tmp = datetime.datetime.utcnow().isoformat(timespec='seconds')

    collection.update_one({"_qrcode": _qrcode}, {"$set": {"scan_status": 1, "scan_date": tmp.split('T')[0],"scan_time": tmp.split('T')[1]}})

    return {"message": "Done"}

@app.post("/update_out/{collection_name}/{_qrcode}")
def update_record_out(collection_name: str, _qrcode: str):
    collection = db[collection_name]
    tmp = datetime.datetime.utcnow().isoformat(timespec='seconds')

    collection.update_one({"_qrcode": _qrcode}, {"$set": {"scan_status": 2, "scan_date": tmp.split('T')[0],"scan_time": tmp.split('T')[1]}})