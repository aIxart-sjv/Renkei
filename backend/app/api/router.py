from fastapi import APIRouter

# Import endpoint routers
from app.api.endpoints import auth
from app.api.endpoints import users
from app.api.endpoints import students
from app.api.endpoints import mentors
from app.api.endpoints import alumni
from app.api.endpoints import startups
from app.api.endpoints import achievements
from app.api.endpoints import connections
from app.api.endpoints import recommendations
from app.api.endpoints import graph
from app.api.endpoints import ml


# Main API router
api_router = APIRouter()


# Auth routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)


# User routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)


# Student routes
api_router.include_router(
    students.router,
    prefix="/students",
    tags=["Students"]
)


# Mentor routes
api_router.include_router(
    mentors.router,
    prefix="/mentors",
    tags=["Mentors"]
)


# Alumni routes
api_router.include_router(
    alumni.router,
    prefix="/alumni",
    tags=["Alumni"]
)


# Startup routes
api_router.include_router(
    startups.router,
    prefix="/startups",
    tags=["Startups"]
)


# Achievement routes
api_router.include_router(
    achievements.router,
    prefix="/achievements",
    tags=["Achievements"]
)


# Connection routes
api_router.include_router(
    connections.router,
    prefix="/connections",
    tags=["Connections"]
)


# Recommendation routes (ML powered)
api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)


# Graph intelligence routes
api_router.include_router(
    graph.router,
    prefix="/graph",
    tags=["Graph Intelligence"]
)


# ML system routes
api_router.include_router(
    ml.router,
    prefix="/ml",
    tags=["Machine Learning"]
)