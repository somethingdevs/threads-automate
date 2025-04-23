from fastapi import FastAPI
from threads_routes import router as threads_router

app = FastAPI()
app.include_router(threads_router)
