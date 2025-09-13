import motor.motor_asyncio
from bson import ObjectId

MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)


db = client.news_aggregator

class PyObjectId(ObjectId):
    @classmethod
    def __get_validator__(cls):
        yield cls.validate 
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("INvalide ObjectId")
        return ObjectId
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        