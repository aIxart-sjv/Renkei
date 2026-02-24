from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.utils.logger import logger

# Import all routers
from app.api.routes import (
    auth_routes,
    student_routes,
    mentor_routes,
    alumni_routes,
    startup_routes,
    achievement_routes,
    recommendation_routes,
    graph_routes,
)

# -----------------------------------
# Create FastAPI app
# -----------------------------------
app = FastAPI(
    title="Renkei API",
    description="AI-powered Innovation, Matching, and Startup Intelligence Platform",
    version="1.0.0",
)


# -----------------------------------
# Enable CORS (for frontend connection)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    ],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Create database tables automatically
# -----------------------------------
@app.on_event("startup")
def startup_event():
    logger.info("Starting Renkei backend...")

    # Create all database tables
    Base.metadata.create_all(bind=engine)

    logger.info("Database tables created successfully.")


# -----------------------------------
# Shutdown event
# -----------------------------------
@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down Renkei backend...")


# -----------------------------------
# Health check endpoint
# -----------------------------------
@app.get("/")
def root():
    return {
        "message": "Renkei API is running",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# -----------------------------------
# Register Routers
# -----------------------------------
app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    student_routes.router,
    prefix="/students",
    tags=["Students"]
)

app.include_router(
    mentor_routes.router,
    prefix="/mentors",
    tags=["Mentors"]
)

app.include_router(
    alumni_routes.router,
    prefix="/alumni",
    tags=["Alumni"]
)

app.include_router(
    startup_routes.router,
    prefix="/startups",
    tags=["Startups"]
)

app.include_router(
    achievement_routes.router,
    prefix="/achievements",
    tags=["Achievements"]
)

app.include_router(
    recommendation_routes.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)

app.include_router(
    graph_routes.router,
    prefix="/graph",
    tags=["Graph Analytics"]
)


# -----------------------------------
# Optional: global exception logging
# -----------------------------------
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response