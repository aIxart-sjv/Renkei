from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.routes import (
    student_routes,
    mentor_routes,
    startup_routes,
    recommendation_routes,
    graph_routes,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Renkei API",
    description="AI-Powered Campus Intelligence & Innovation Platform",
    version="1.0.0",
)

# CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Renkei API 🚀"}

# Include routers
app.include_router(student_routes.router, prefix="/students", tags=["Students"])
app.include_router(mentor_routes.router, prefix="/mentors", tags=["Mentors"])
app.include_router(startup_routes.router, prefix="/startups", tags=["Startups"])
app.include_router(recommendation_routes.router, prefix="/recommend", tags=["Recommendations"])
app.include_router(graph_routes.router, prefix="/graph", tags=["Graph Analytics"])