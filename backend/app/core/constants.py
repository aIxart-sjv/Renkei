"""
Renkei System Constants

Central definition of roles, entity types, connection types,
ML defaults, and graph parameters.
"""


# =========================
# USER ROLES
# =========================

ROLE_ADMIN = "admin"
ROLE_STUDENT = "student"
ROLE_MENTOR = "mentor"
ROLE_ALUMNI = "alumni"

ALL_ROLES = [
    ROLE_ADMIN,
    ROLE_STUDENT,
    ROLE_MENTOR,
    ROLE_ALUMNI
]


# =========================
# ENTITY TYPES (Graph Nodes)
# =========================

ENTITY_STUDENT = "student"
ENTITY_MENTOR = "mentor"
ENTITY_ALUMNI = "alumni"
ENTITY_STARTUP = "startup"

ALL_ENTITY_TYPES = [
    ENTITY_STUDENT,
    ENTITY_MENTOR,
    ENTITY_ALUMNI,
    ENTITY_STARTUP
]


# =========================
# CONNECTION TYPES (Graph Edges)
# =========================

CONNECTION_MENTORSHIP = "mentorship"
CONNECTION_COLLABORATION = "collaboration"
CONNECTION_STARTUP_MEMBER = "startup_member"
CONNECTION_STARTUP_FOUNDER = "startup_founder"
CONNECTION_PEER = "peer"
CONNECTION_ADVISOR = "advisor"

ALL_CONNECTION_TYPES = [
    CONNECTION_MENTORSHIP,
    CONNECTION_COLLABORATION,
    CONNECTION_STARTUP_MEMBER,
    CONNECTION_STARTUP_FOUNDER,
    CONNECTION_PEER,
    CONNECTION_ADVISOR
]


# =========================
# ACHIEVEMENT TYPES
# =========================

ACHIEVEMENT_HACKATHON = "hackathon"
ACHIEVEMENT_PROJECT = "project"
ACHIEVEMENT_CERTIFICATION = "certification"
ACHIEVEMENT_INTERNSHIP = "internship"
ACHIEVEMENT_RESEARCH = "research"
ACHIEVEMENT_STARTUP = "startup"

ALL_ACHIEVEMENT_TYPES = [
    ACHIEVEMENT_HACKATHON,
    ACHIEVEMENT_PROJECT,
    ACHIEVEMENT_CERTIFICATION,
    ACHIEVEMENT_INTERNSHIP,
    ACHIEVEMENT_RESEARCH,
    ACHIEVEMENT_STARTUP
]


# =========================
# STARTUP STAGES
# =========================

STARTUP_IDEA = "idea"
STARTUP_PROTOTYPE = "prototype"
STARTUP_MVP = "mvp"
STARTUP_EARLY = "early"
STARTUP_GROWTH = "growth"
STARTUP_SCALE = "scale"

ALL_STARTUP_STAGES = [
    STARTUP_IDEA,
    STARTUP_PROTOTYPE,
    STARTUP_MVP,
    STARTUP_EARLY,
    STARTUP_GROWTH,
    STARTUP_SCALE
]


# =========================
# ML DEFAULT SETTINGS
# =========================

EMBEDDING_DIMENSION = 384

DEFAULT_RECOMMENDATION_LIMIT = 10

SIMILARITY_THRESHOLD = 0.65

INNOVATION_SCORE_MAX = 100.0


# =========================
# GRAPH SETTINGS
# =========================

DEFAULT_EDGE_WEIGHT = 1.0

COLLABORATION_WEIGHT = 1.5

MENTORSHIP_WEIGHT = 2.0

FOUNDER_WEIGHT = 2.5


# =========================
# TOKEN TYPES
# =========================

TOKEN_TYPE_ACCESS = "access"

TOKEN_TYPE_REFRESH = "refresh"


# =========================
# CACHE KEYS
# =========================

CACHE_GRAPH = "graph_cache"

CACHE_EMBEDDINGS = "embedding_cache"


# =========================
# SYSTEM LIMITS
# =========================

MAX_SKILLS_PER_ENTITY = 100

MAX_CONNECTIONS_PER_ENTITY = 10000

MAX_ACHIEVEMENTS_PER_STUDENT = 1000