from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# BASE RECOMMENDATION ITEM
# =========================

class RecommendationBase(BaseModel):
    """
    Core recommendation fields
    """

    entity_id: int

    entity_type: str = Field(
        ...,
        description="student, mentor, alumni, startup"
    )

    score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Recommendation score"
    )


# =========================
# EXTENDED RECOMMENDATION ITEM
# =========================

class RecommendationItem(RecommendationBase):
    """
    Recommendation with optional metadata
    """

    name: Optional[str] = None

    title: Optional[str] = None

    industry: Optional[str] = None

    innovation_score: Optional[float] = None

    similarity_score: Optional[float] = None

    graph_score: Optional[float] = None


# =========================
# STUDENT RECOMMENDATIONS RESPONSE
# =========================

class StudentRecommendationResponse(BaseModel):

    student_id: int

    recommendations: List[RecommendationItem]


# =========================
# MENTOR RECOMMENDATIONS RESPONSE
# =========================

class MentorRecommendationResponse(BaseModel):

    mentor_id: int

    recommendations: List[RecommendationItem]


# =========================
# STARTUP RECOMMENDATIONS RESPONSE
# =========================

class StartupRecommendationResponse(BaseModel):

    startup_id: int

    recommendations: List[RecommendationItem]


# =========================
# GENERIC RECOMMENDATION RESPONSE
# =========================

class RecommendationResponse(BaseModel):

    source_id: int

    source_type: str

    recommendations: List[RecommendationItem]


# =========================
# FULL ECOSYSTEM RECOMMENDATIONS
# =========================

class FullRecommendationResponse(BaseModel):
    """
    Returns recommendations across all entity types
    """

    students: List[RecommendationItem]

    mentors: List[RecommendationItem]

    startups: List[RecommendationItem]

    alumni: List[RecommendationItem]


# =========================
# SIMPLE RECOMMENDATION LIST
# =========================

class RecommendationListItem(BaseModel):

    entity_id: int

    entity_type: str

    score: float


class RecommendationListResponse(BaseModel):

    recommendations: List[RecommendationListItem]