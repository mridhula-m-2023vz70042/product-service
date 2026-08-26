from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI(title="Product Service")

# Database Connection (Creates database product_db and collection products automatically)
client = MongoClient("mongodb://localhost:27017/")
db = client["product_db"]
products_collection = db["products"]

class ProductCreate(BaseModel):
    name: str
    price: float

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    res = products_collection.insert_one(product.model_dump())
    return {"id": str(res.inserted_id), **product.model_dump()}

@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])
    return product

