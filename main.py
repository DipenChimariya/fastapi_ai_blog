from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="FastAPI AI Blog")
templates = Jinja2Templates(directory="templates")



class PostBase(BaseModel):
    """Common fields for all Post models"""
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    author: str = Field(default="Anonymous")
    category: str = Field(default="General")

class PostCreate(PostBase):
    """Schema for creating a post (data sent by user)"""
    pass

class Post(PostBase):
    """The full Post schema (as stored in our 'database')"""
    id: int
    date_posted: str  




posts: List[Post] = [
    Post(
        id=1,
        author="Dipen Chimariya",
        category="Backend",
        title="FastAPI is really fast",
        content="Learning to build using FastAPI",
        date_posted="24 April, 2026",
    ),
    Post(
        id=2,
        author="abcd efgh",
        category="Random",
        title="Dummy data",
        content="Real Database is coming soon in DAY 5",
        date_posted="24 April, 2026",
    ),
]



@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={"posts": posts, "title": "Home"}
    )

@app.get("/post/api", response_model=List[Post])
async def get_posts_api():
    """API endpoint returns raw JSON data validated by Pydantic"""
    return posts

@app.get("/post/{post_id}", name="post_detail")
async def post_detail(request: Request, post_id: int):
    
    current_post = next((p for p in posts if p.id == post_id), None)
            
    if current_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": current_post}
    )



@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = exception.detail if exception.detail else "An error occurred."

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"status_code": exception.status_code, "message": message},
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )
    
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": 422,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )