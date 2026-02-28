from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

# Optional later
# from app.db.init_db import init_db


# Create FastAPI instance
app = FastAPI(
    title="Renkei API",
    description="AI-Powered Innovation Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS configuration (frontend communication)
origins = [
    "http://localhost:5173",  # Vite frontend
    "http://localhost:3000",  # optional React default
    "*",  # allow all for development (restrict in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API router
app.include_router(api_router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Renkei API is running",
        "status": "success",
        "version": "1.0.0",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    print("Renkei API starting...")

    # Later enable this
    # init_db()

    print("Renkei API started successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Renkei API shutting down...")