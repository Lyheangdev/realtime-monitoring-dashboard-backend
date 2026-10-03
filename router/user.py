from fastapi import APIRouter

from ..lib.api_enum import ApiTagEnum

router = APIRouter(prefix="/users", tags=[ApiTagEnum.SYSTEM_USER], responses= {404: {"Description" : "Resource not found."}})

# Create user
@router.post("/")
async def create_user():
    pass

# Get a user
@router.get("/${user_id}")
async def get_user(user_id: int):
    pass

# Get all users
@router.get('/')
async def get_users():
    pass

# Update user
@router.put('/${user_id}')
async def update_user(user_id: int):
    pass

# Delete a user
@router.delete('/${user_id}')
async def delete_user(user_id: int):
    pass

# Delete all users
@router.delete('/')
async def delete_users():
    pass