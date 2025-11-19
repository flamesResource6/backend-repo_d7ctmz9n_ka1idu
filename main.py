import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Order

app = FastAPI(title="Food Ordering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Food Ordering Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Public endpoints
@app.get("/menu")
def list_menu():
    docs = get_documents("menuitem")
    items = []
    for d in docs:
        item = {
            "id": str(d.get("_id")),
            "name": d.get("name"),
            "description": d.get("description"),
            "price": float(d.get("price", 0)),
            "image": d.get("image"),
            "category": d.get("category", "General"),
            "available": bool(d.get("available", True)),
        }
        items.append(item)
    return {"items": items}

@app.post("/menu", status_code=201)
def create_menu_item(payload: MenuItem):
    item_id = create_document("menuitem", payload)
    return {"id": item_id}

@app.post("/orders", status_code=201)
def create_order(payload: Order):
    # Basic validation: ensure menu items exist
    try:
        item_ids = [ObjectId(i.item_id) for i in payload.items]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item IDs")

    existing = list(db["menuitem"].find({"_id": {"$in": item_ids}}, {"_id": 1}))
    if len(existing) != len(item_ids):
        raise HTTPException(status_code=400, detail="One or more menu items not found")

    order_id = create_document("order", payload)
    return {"id": order_id, "status": "received"}

@app.get("/orders")
def list_orders(limit: Optional[int] = 20):
    docs = get_documents("order", limit=limit)
    # Convert for client
    orders = []
    for d in docs:
        d["_id"] = str(d["_id"]) if "_id" in d else None
        orders.append(d)
    return {"orders": orders}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
