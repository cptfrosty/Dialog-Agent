from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body
from json_models.model import UserRegister, Request

tags_metadata = [
    {
        'name': 'items',
        'description': 'items',
    }
]

app = FastAPI(
    title = 'Mini api',
    descriprion = 'This is my mini app (description)',
    version = '1.0.0',
    openapi_tags = tags_metadata
)

@app.post("/auth/register", response_model=Request, status_code=status.HTTP_201_CREATED)
async def auth_register(user_data: UserRegister):
    req = Request()
    return req

@app.get("/{item_id}")
async def read_item(item_id: int):
    return {"read_iten {item_id}"}