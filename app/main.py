from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user, post, auth, vote
from config import settings


app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
