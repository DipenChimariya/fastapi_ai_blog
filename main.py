from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app=FastAPI(title="fastapi ai blog")
templates=Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Dipen Chimariya",
        "title": "FastAPI is really fast",
        "content": "Learning to build using FastAPI",
        "date_posted": "24 april, 2026",
    },
    {
        "id": 2,
        "author": "abcd efgh",
        "title": "Dummy data",
        "content": "Real Database is coming soon in DAY 5",
        "date_posted": "24 april, 2026",
    },
]

@app.get("/",include_in_schema=False)
@app.get("/posts",include_in_schema=False)
def home(request:Request):
    return templates.TemplateResponse(request=request,name="home.html",context={"posts":posts,"title":"home"})

@app.get("/post/api")
def get_posts():
    return posts