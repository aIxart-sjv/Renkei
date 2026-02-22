"""
Application-wide constants for Renkei
"""


# -----------------------------------
# User Roles
# -----------------------------------
ROLE_STUDENT = "student"
ROLE_MENTOR = "mentor"
ROLE_ALUMNI = "alumni"
ROLE_ADMIN = "admin"
ROLE_INVESTOR = "investor"

VALID_ROLES = [
    ROLE_STUDENT,
    ROLE_MENTOR,
    ROLE_ALUMNI,
    ROLE_ADMIN,
    ROLE_INVESTOR,
]


# -----------------------------------
# Account Status
# -----------------------------------
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_SUSPENDED = "suspended"

VALID_STATUSES = [
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_SUSPENDED,
]


# -----------------------------------
# Startup Stages
# -----------------------------------
STARTUP_IDEATION = "Ideation"
STARTUP_PROTOTYPE = "Prototype"
STARTUP_MVP = "MVP"
STARTUP_EARLY_REVENUE = "Early Revenue"
STARTUP_GROWTH = "Growth"
STARTUP_SCALING = "Scaling"

VALID_STARTUP_STAGES = [
    STARTUP_IDEATION,
    STARTUP_PROTOTYPE,
    STARTUP_MVP,
    STARTUP_EARLY_REVENUE,
    STARTUP_GROWTH,
    STARTUP_SCALING,
]


# -----------------------------------
# Achievement Categories
# -----------------------------------
ACHIEVEMENT_HACKATHON = "Hackathon"
ACHIEVEMENT_PROJECT = "Project"
ACHIEVEMENT_CERTIFICATION = "Certification"
ACHIEVEMENT_STARTUP = "Startup"

VALID_ACHIEVEMENT_CATEGORIES = [
    ACHIEVEMENT_HACKATHON,
    ACHIEVEMENT_PROJECT,
    ACHIEVEMENT_CERTIFICATION,
    ACHIEVEMENT_STARTUP,
]


# -----------------------------------
# Achievement Outcomes
# -----------------------------------
OUTCOME_WON = "Won"
OUTCOME_RUNNER_UP = "Runner-up"
OUTCOME_PARTICIPATED = "Participated"
OUTCOME_LOST = "Lost"

VALID_OUTCOMES = [
    OUTCOME_WON,
    OUTCOME_RUNNER_UP,
    OUTCOME_PARTICIPATED,
    OUTCOME_LOST,
]


# -----------------------------------
# Default Limits
# -----------------------------------
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

DEFAULT_RECOMMENDATION_LIMIT = 10


# -----------------------------------
# Graph Weights (for innovation score)
# -----------------------------------
DEGREE_WEIGHT = 0.4
BETWEENNESS_WEIGHT = 0.4
CLOSENESS_WEIGHT = 0.2