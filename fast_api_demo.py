from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello Johann!"}

@app.post("/")
async def post():
    return {"message": "Hello from the post methd"}

@app.put("/")
async def put():
    return {"message": "Hello from the put"}

@app.get("/users")
async def get_users():
    return {"message": "List users route"}

@app.get("/users/me")
async def get_current_user():
    return {"Message" : "This is the current user"}

@app.get("/users/{user_id}") # The parameter typed by the user
async def get_user(user_id: int):
    return {"user_id": user_id}

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message" : "You are healthy"}
    if food_name.value == "fruits":
        return {"food_name": food_name, "message" : "You like sweet things"}
    
    return {"food_name": food_name, "message": "I like other stuff"}

fake_items = ['item 0', 'item 1', 'item 2', 'item 3', 'item 4', 'item 5']

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 4):
    return {'items_list': fake_items[skip :skip + limit]}

@app.get("/items/{item_id}") # Adding a path parameter
async def get_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id" : item_id}

@app.get("/users/{user_id}/items/{item_id}") # 2 paths parameters
async def get_user_item(user_id: str, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is supposed to be a very long text which is not short at all."})
    return item