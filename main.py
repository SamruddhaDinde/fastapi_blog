from typing import Annotated

from contextlib import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
#from fastapi.responses import JSONResponse
#we dont need json cause we have default exception handlers
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import models
from database import Base, engine, get_db
#from schemas import PostCreate, PostBase, PostResponse, UserCreate, UserResponse, PostUpdate, UserUpdate


from routers import users, posts
# Base.metadata.create_all(bind=engine)
#this is synchronous we dont need



@asynccontextmanager
async def lifespan(_app: FastAPI):
  #startup
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield
  #shutdown
  await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])


@app.get("/",  include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
  result = await db.execute(select(models.Post).options(selectinload(models.Post.author)))
  posts = result.scalars().all()
  return templates.TemplateResponse(
    request,
    "home.html",
    {"posts":posts, "title": "Home"}

  )
 

@app.get("/posts/{post_id}",include_in_schema=False )
async def post_page(request:Request, post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
#  for post in posts:
#   if post.get("id") == post_id:
#      title = post['title'][:50]
#      return templates.TemplateResponse(request, "post.html ", {"post": post, "title":title})
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
      title = post.title[:50]
      return templates.TemplateResponse(
        request,
        "post.html",
        {"post":post,"title": title}
      )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(request:Request, user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  user = result.scalars().first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.user_id == user_id))
  posts = result.scalars().all()
  return templates.TemplateResponse(
    request,
    "user_posts.html",
    {"posts": posts, "user":user, "title":f"{user.username}'s posts"}
  )




## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
   

    if request.url.path.startswith("/api"):
        # return JSONResponse(
        #     status_code=exception.status_code,
        #     content={"detail": message},
        # )
        return await http_exception_handler(request, exception)
    
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        # return JSONResponse(
        #     status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        #     content={"detail": exception.errors()},
        # )
        return await request_validation_exception_handler(request, exception)
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


"""200 Ok: get , put, patch success
201 Created: successful post for users and posts

204 No content:successful delete
400 Bad request: dupliucate username or email
404 Not found : user/ post not available
422 Unprocessable entity, from pydantic"""
