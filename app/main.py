from fastapi import FastAPI
from app.api.works import router as works_router

app = FastAPI(
    title="AO3 API",
    description="FastAPI wrapper around AO3 Work module",
    version="1.0.0",
)

app.include_router(works_router, prefix="/works", tags=["works"])
