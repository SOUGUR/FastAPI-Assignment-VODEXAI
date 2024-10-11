from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, date, timezone
from .database import counters_collection, items_collection
from .models import Item, UpdateItem, ClockIn, UpdateClockIn
from typing import Optional
from .crud import (
    update_item, delete_item, aggregate_items_by_email,
    add_clockin, get_clockin, update_clockin, delete_clockin, filter_clockin
)

app = FastAPI()

async def get_next_id():
    result = await counters_collection.find_one_and_update(
        {"_id": "itemid"},  
        {"$inc": {"seq": 1}},  
        return_document=True,
        upsert=True  
    )
    return result["seq"]

async def get_next_clockin_id():
    result = await counters_collection.find_one_and_update(
        {"_id": "clockinid"},  
        {"$inc": {"seq": 1}}, 
        return_document=True,
        upsert=True
    )
    return result["seq"]



@app.get("/items/filter")
async def filter_items_api(
    email: Optional[str] = Query(None),                
    expiry_date: Optional[str] = Query(None),          
    insert_date: Optional[str] = Query(None),          
    quantity: Optional[int] = Query(None)              
):
    query = {}

    if email:
        query["email"] = email

    if expiry_date:
        try:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
            query["expiry_date"] = {"$gt": expiry_date}  
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid expiry date format. Use YYYY-MM-DD.")

    if insert_date:
        try:
            insert_date = datetime.strptime(insert_date, "%Y-%m-%d")
            query["insert_date"] = {"$eq": insert_date}  
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid insert date format. Use YYYY-MM-DD.")

    if quantity is not None:
        query["quantity"] = {"$gte": quantity}

    items = await items_collection.find(query).to_list(100) 
    return items

@app.get("/items/aggregate")
async def aggregate_items_api():
    return await aggregate_items_by_email()

@app.post("/items/", response_model=Item)
async def create_item(item: Item):  
    item_id = await get_next_id() 
    item_data = item.model_dump()  
    item_data["_id"] = item_id  
    item_data["insert_date"] = datetime.combine(item.insert_date, datetime.min.time())
    if isinstance(item.expiry_date, date):
        item_data["expiry_date"] = datetime.combine(item.expiry_date, datetime.min.time())

    await items_collection.insert_one(item_data)
    return Item(**item_data)


@app.get("/items/{id}", response_model=Item)  
async def get_item(id: int):  
    item = await items_collection.find_one({"_id": id})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{id}")
async def update_item_api(id: int, item: UpdateItem):
    
    updated_fields = item.model_dump(exclude_unset=True) 
    
    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await update_item(id, updated_fields)

    if result == 0:  
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item updated", "updated_fields": updated_fields}


@app.delete("/items/{id}")
async def delete_item_api(id: int):  
    await delete_item(id)  
    return {"message": "Item deleted"}



@app.post("/clock-in")
async def create_clockin(clockin: ClockIn):
    clockin_id = await get_next_clockin_id()
    clockin_data = clockin.model_dump()
    clockin_data["_id"] = clockin_id
    clockin_data["insert_date"] = datetime.now(timezone.utc)

    result = await add_clockin(clockin_data)

    return {"clockin_id": result}

@app.get("/clock-in/{id:int}")
async def read_clockin(id: int):
    clockin = await get_clockin(id)
    if clockin:
        return clockin
    raise HTTPException(status_code=404, detail="Clock-in record not found")

@app.get("/clock-in/filter")
async def filter_clockin_api(
    email: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    insert_date: Optional[str] = Query(None)
):
    clockins = await filter_clockin(email, location, insert_date)
    return clockins

@app.put("/clock-in/{id}", response_model=dict)  
async def update_clockin_api(id: int, clockin: UpdateClockIn):
    update_data = clockin.model_dump(exclude_unset=True)  

    if not update_data: 
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await update_clockin(id, update_data)

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found or same values for the field hence no changes made.")

    return {"message": "Clock-in record updated"}


@app.delete("/clock-in/{id}")
async def delete_clockin_api(id: str):
    await delete_clockin(id)
    return {"message": "Clock-in record deleted"}

