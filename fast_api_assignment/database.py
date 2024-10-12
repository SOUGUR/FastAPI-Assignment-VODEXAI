from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb+srv://sourabhgurav23:Iamsourabh#123@cluster0.yab98.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.fastapiassignment

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

items_collection = database.get_collection("items")
counters_collection = database.get_collection("counters")
clockin_collection = database.get_collection("clockin")

