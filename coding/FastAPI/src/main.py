from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import Depends, FastAPI

from pydantic import BaseModel, Field

from operations.router import router as operation_router
from auth.base_config import auth_backend
from auth.base_config import _fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate
from auth.models import User


app = FastAPI(
    title="Trading App"
)

# toy data
users = [
    {"id": 1, "role": "admin", "name": "Vlad"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Alice"},
    {"id": 4, "role": "investor", "name": "Bob", "degree": [
        {"id": 1, "created_at": datetime.now(), "name": "newbiew"},
    ]},
    {"id": 5, "role": 100, "name": "Error User"},
]


trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]

# data models for data validation
class Trade(BaseModel):
    """
    PyData data model for trades.
    """
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float = Field(ge=0)


class DegreeName(Enum):
    newbiew = 'newbiew'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    name: DegreeName


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None


# routers (simple definition via @)
@app.get("/users/{user_id}", response_model=List[User])
def get_users(user_id: int):
    return [
        user for user in users if user["id"] == user_id
    ]


@app.get("/trades/")
def get_trades(limit: int = 10, offset: int = 0):
    return trades[offset:][:limit]


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user["id"] == user_id, users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


@app.post("/trades")
def add_trades(trades_data: List[Trade]):
    trades.extend(trades_data)
    return {"status": 200, "data": trades}

# more flexibe definition via app.include_router

# authentication
app.include_router(
    _fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# registration
app.include_router(
    _fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# for registered users
current_user = _fastapi_users.current_user()
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


# operation routers
app.include_router(operation_router)
