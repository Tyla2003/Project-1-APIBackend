from fastapi import APIRouter
from database import get_db_connection
from pydantic import BaseModel
from typing import Optional

class PostUpdate(BaseModel):
    title: str
    post_text: str

class PostCreate(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    post_text: str

router = APIRouter()

@router.post("/posts/")
async def create_post(post: PostCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (user_id, title, post_text, likes) VALUES (?, ?, ?, ?)",
        (post.user_id, post.title, post.post_text, 0),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return {
        "id": post_id,
        "user_id": post.user_id,
        "title": post.title,
        "post_text": post.post_text,
        "likes":0
    }

@router.get("/posts/")
async def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return [dict(post) for post in posts]

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post:
        return dict(post)
    else:
        return {"error": "Post not found"}

@router.get("/posts/user/{user_id}")
async def get_posts_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE user_id = ?", (user_id,))
    posts = cursor.fetchall()
    conn.close()
    
    return [dict(post) for post in posts]

@router.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE posts SET title = ?, post_text = ? WHERE id = ?",
        (post.title, post.post_text, post_id),
    )
    conn.commit()
    conn.close()
    return {"message": f"Post {post_id} updated successfully"}

@router.patch("/posts/{post_id}/title")
async def patch_post_title(post_id: int, title: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE posts SET title = ? WHERE id = ?",
        (title, post_id)
    )
    conn.commit()
    conn.close()
    return {"message": f"Post {post_id} title updated successfully"}

@router.patch("/posts/{post_id}/post_text")
async def patch_post_text(post_id: int, post_text: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE posts SET post_text = ? WHERE id = ?",
        (post_text, post_id),
    )
    conn.commit()
    conn.close()
    return {"message": f"Post {post_id} text updated successfully"}

@router.patch("/posts/{post_id}/increment_likes")
async def increment_post_likes(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return {"message": f"Likes incremented for post {post_id}"}

@router.patch("/posts/{post_id}/decrement_likes")
async def decrement_post_likes(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE posts SET likes = likes - 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return {"message": f"Likes decremented for post {post_id}"}

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return {"message": f"Post {post_id} deleted successfully"}