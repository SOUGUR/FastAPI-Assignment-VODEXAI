from datetime import datetime, timezone
from bson.objectid import ObjectId
from .database import items_collection, clockin_collection
from fastapi import HTTPException
from typing import Optional


async def get_item(id: str):
    return await items_collection.find_one({"_id": ObjectId(id)})

async def update_item(id: int, updated_fields: dict):
    result = await items_collection.update_one({"_id": id}, {"$set": updated_fields})
    return result.modified_count


async def delete_item(id: int):
    result = await items_collection.delete_one({"_id": id}) 
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

# MongoDB aggregation
async def aggregate_items_by_email():
    return await items_collection.aggregate([
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]).to_list(100)

# CRUD for Clock-in Records
async def add_clockin(clockin_data: dict):
    result = await clockin_collection.insert_one(clockin_data)
    return str(result.inserted_id)

async def get_clockin(id: int):
    return await clockin_collection.find_one({"_id": id})

async def update_clockin(id: int, update_data: dict):
    result = await clockin_collection.update_one({"_id": id}, {"$set": update_data})
    return result

async def delete_clockin(id: int):
    result = await clockin_collection.delete_one({"_id": id})
    return result 

async def filter_clockin(email: Optional[str] = None, location: Optional[str] = None, insert_date: Optional[str] = None):
    query = {}
    
    if email:
        query["email"] = {"$eq": email}  
    if location:
        query["location"] = {"$eq": location}  
    if insert_date:
        try:
            insert_date_obj = datetime.strptime(insert_date, "%Y-%m-%d")
            insert_date_obj = datetime.combine(insert_date_obj, datetime.max.time())
            query["insert_date"] = {"$gt": insert_date_obj}  
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return await clockin_collection.find(query).to_list(100)
