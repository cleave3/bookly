from fastapi import Depends, FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.dependencies import RoleChecker


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has been stopped")


version = "v1"

app = FastAPI(
    version=version,
    title="Book Service",
    description="A book management portal",
    # lifespan=life_span,
)

app.include_router(book_router, tags=["Books"], prefix=f"/api/{version}/books")
app.include_router(auth_router, tags=["Auth"], prefix=f"/api/{version}/auth")
app.include_router(
    reviews_router,
    tags=["Reviews"],
    prefix=f"/api/{version}/reviews",
    dependencies=[Depends(RoleChecker("user"))],
)
