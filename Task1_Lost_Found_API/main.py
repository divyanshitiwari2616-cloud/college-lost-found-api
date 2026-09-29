from fastapi import FastAPI, HTTPException
from schemas import ItemCreate, ItemUpdate, Item
from db import Database


app = FastAPI(
    title="Lost and Found API",
    description="FastAPI CRUD application for managing lost and found items",
    version="1.0.0"
)

db = Database("items.db")

@app.get("/")
def home():
    return {"message": "Lost and Found API is running successfully"}


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):

    new_item = db.create_item(item)

    if new_item is None:
        raise HTTPException(status_code=500,detail="Unable to create item")

    return new_item


@app.get("/items", response_model=list[Item])
def get_items():

    return db.get_items()


# =========================================================
# GET ITEM BY ID
# GET /items/{item_id}
# =========================================================

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):

    item = db.get_item(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# =========================================================
# UPDATE ITEM
# PUT /items/{item_id}
# =========================================================

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):

    updated_item = db.update_item(item_id, item)

    if updated_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return updated_item


# =========================================================
# DELETE ITEM
# DELETE /items/{item_id}
# =========================================================

@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    deleted = db.delete_item(item_id)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "message": "Item deleted successfully"
    }


# =========================================================
# GET ITEMS BY STATUS
# GET /items/status/{status}
# =========================================================

@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(status: str):

    return db.get_items_by_status(status)


# =========================================================
# GET ITEMS BY CATEGORY
# GET /items/category/{category}
# =========================================================

@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(category: str):

    return db.get_items_by_category(category)