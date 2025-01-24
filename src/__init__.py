from fastapi import Depends, FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.errors import register_all_errors
from src.middleware import register_middleware
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.dependencies import RoleChecker
from .errors import register_all_errors


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has been stopped")


version = "v1"

version_prefix = f"/api/{version}"

app = FastAPI(
    version=version,
    title="Book Service",
    description="A book management portal",
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Cleave Owhiroro",
        "url": "https://github.com/cleave3",
        "email": "owhiroroeghele@gmail.com",
    },
    # terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    # docs_url=f"{version_prefix}/docs",
    # redoc_url=f"{version_prefix}/redoc",
)

register_all_errors(app)

register_middleware(app)

app.include_router(book_router, tags=["Books"], prefix=f"{version_prefix}/books")
app.include_router(auth_router, tags=["Auth"], prefix=f"{version_prefix}/auth")
app.include_router(
    reviews_router,
    tags=["Reviews"],
    prefix=f"{version_prefix}/reviews",
    dependencies=[Depends(RoleChecker("user"))],
)
