from fastapi import FastAPI, Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="FastAPI AI Blog")
templates = Jinja2Templates(directory="templates")

# Mock Database
posts = [
    {
        "id": 1,
        "author": "Dipen Chimariya",
        "category": "Backend",
        "title": "FastAPI is really fast",
        "content": "Learning to build using FastAPI",
        "date_posted": "24 april, 2026",
    },
    {
        "id": 2,
        "author": "abcd efgh",
        "category": "Random",
        "title": "Dummy data",
        "content": "Real Database is coming soon in DAY 5",
        "date_posted": "24 april, 2026",
    },
]

@app.get("/",include_in_schema=False,name="home")
@app.get("/posts",include_in_schema=False,name="posts")
async def home(request:Request):
    return templates.TemplateResponse(request=request,name="home.html",context={"posts":posts,"title":"home"})

@app.get("/post/api")
async def get_posts():
    return posts


@app.get("/post/{post_id}", name="post_detail")
async def post_detail(request: Request, post_id: int):
    current_post = None
    for post in posts:
        if post.get("id") == post_id:
            current_post = post
            break
            
    if current_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    return templates.TemplateResponse(request=request,name="post.html",context={"post":current_post}
    )




@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    
   
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exception.status_code,
            "message": message,
        },
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
    