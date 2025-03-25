from fastapi import APIRouter
from database import get_db_connection
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
router = APIRouter()


class UserCreate(BaseModel):
    id: Optional[int] = None # Auto assigned 
    username: str
    image_url: str
    is_admin: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    image_url: Optional[str] = None
# Placeholder Endpoints for Users
@router.post("/users/")
async def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, image_url, is_admin) VALUES (?, ?, ?)",
        (user.username, user.image_url, int(user.is_admin)),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "username": user.username, "image_url": user.image_url, "is_admin": user.is_admin}

@router.get("/users/")
async def get_users(name: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if name: 
        cursor.execute("SELECT * FROM users WHERE username = ?", (name,))
    else:
        cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return [
        {**dict(user), "is_admin": bool(user["is_admin"])}
        for user in users
        ]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    if user:
        return {**dict(user), "is_admin": bool(user["is_admin"])}  
    else:
        return None

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get the existing user data
    cursor.execute("SELECT username, image_url FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        conn.close()
        return {"error": "User not found"}
    # Use existing values if the new ones aren't provided
    updated_username = user.username if user.username is not None else existing_user[0]
    updated_image_url = user.image_url if user.image_url is not None else existing_user[1]
    cursor.execute(
        "UPDATE users SET username = ?, image_url = ? WHERE id = ?",
        (updated_username, updated_image_url, user_id),
    )
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} updated successfully"}

@router.patch("/users/{user_id}/is_admin")
async def patch_user_is_admin(user_id: int, is_admin: bool = Query(...)):
    print(f"Updating user {user_id} to admin: {is_admin}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_admin = ? WHERE id = ?", (int(is_admin), user_id))
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} admin status updated to {is_admin}"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE user_id = ?", (user_id,))

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} and their posts deleted successfully"}