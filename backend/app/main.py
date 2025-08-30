from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import des routers
from app.routers import organisation, logements, souscriptions

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Boaz Housing API",
    description="API pour la gestion des logements et souscriptions Boaz Housing",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(organisation.router, prefix="/api")
app.include_router(logements.router, prefix="/api")
app.include_router(souscriptions.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Boaz Housing API v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)