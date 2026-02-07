from fastapi import FastAPI
from app.api.works import router as works_router
from app.api.users import router as users_router

app = FastAPI(
    title="AO3 API",
    description="Obtain public fanwork data from Archive of Our Own ",
    version="1.0.0",
)

app.include_router(works_router, prefix="/works", tags=["works"])
app.include_router(users_router, prefix="/users", tags=["users"])
