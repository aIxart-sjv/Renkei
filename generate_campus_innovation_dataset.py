"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║       Campus Innovation & Engagement Intelligence Hub                          ║
║       Master Dataset Generator — 10,000 Unique Student Records                 ║
║                                                                                ║
║  Features:                                                                     ║
║  ✅ GPU-Accelerated (NVIDIA RAPIDS cupy/cudf) with CPU fallback                ║
║  ✅ Zero Duplicate Records (Cryptographic Signature Check)                     ║
║  ✅ Noise-Minimized via Strict Conditional Logic & Digital Trace Data           ║
║  ✅ Meaningful Modular Semantic Text (NLP-Ready, no Lorem Ipsum)               ║
║  ✅ Correlated Features (No random fluff — every column earns its place)       ║
║  ✅ All Features: Predictive ML + NLP Matching + Graph SNA + Dashboards        ║
╚══════════════════════════════════════════════════════════════════════════════════╝

INSTALLATION:
  pip install faker numpy pandas
  (For GPU acceleration): pip install cupy-cuda12x cudf-cu12
"""

import csv
import random
import hashlib
import time
from faker import Faker

# ── GPU / CPU AUTO-DETECTION ────────────────────────────────────────────────────
try:
    import cupy as cp
    import cudf
    GPU_AVAILABLE = True
    print("✅ GPU (RAPIDS/cupy) detected — running in GPU-accelerated mode.")
except ImportError:
    import numpy as cp   # Drop-in numpy replacement when GPU unavailable
    GPU_AVAILABLE = False
    print("⚠️  GPU libraries not found — falling back to CPU (numpy) mode.")
    print("    Install: pip install cupy-cuda12x cudf-cu12 for GPU support.\n")

import numpy as np

# ── CONFIGURATION ───────────────────────────────────────────────────────────────
TARGET_STUDENTS  = 10_000     # Exact number of unique students we want
GENERATE_BATCH   = 13_000     # Overshoot buffer — duplicates will be dropped
RANDOM_SEED      = 2026

# Seed ALL random engines for full reproducibility
fake = Faker('en_US')
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
if GPU_AVAILABLE:
    cp.random.seed(RANDOM_SEED)

# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — CONTROLLED VOCABULARIES
#  Purpose: Prevents NLP sparsity and buzzword noise.
#  Every text field is built from these real-world, domain-specific word banks.
# ══════════════════════════════════════════════════════════════════════════════════

TECH_SKILLS = [
    "Python", "Machine Learning", "React.js", "Django",
    "Data Analysis", "Node.js", "Blockchain", "UI/UX Design",
    "Computer Vision", "Natural Language Processing", "IoT", "Cloud Computing",
    "Cybersecurity", "AR/VR Development", "Android Development", "iOS Development",
    "DevOps", "Embedded Systems", "Data Engineering", "Business Analytics"
]

INDUSTRIES = [
    "HealthTech", "EdTech", "AgriTech", "FinTech",
    "CleanEnergy", "LogisticsTech", "LegalTech", "HRTech",
    "RetailTech", "SpaceTech", "BioTech", "CivicTech"
]

# Structured Problem Spaces — forces NLP to find real semantic overlaps
PROBLEM_SPACES = [
    "inefficient supply chain visibility",
    "lack of affordable mental health access",
    "high student dropout rates in rural areas",
    "fragmented agricultural market data",
    "manual compliance reporting in hospitals",
    "poor financial literacy among youth",
    "inadequate early flood warning systems",
    "carbon-intensive logistics operations",
    "inaccessible legal aid for low-income families",
    "untapped renewable energy in tier-2 cities"
]

# Structured Solutions — pairs semantically with problem spaces above
SOLUTION_APPROACHES = [
    "an AI-driven predictive analytics dashboard",
    "a blockchain-backed traceability ledger",
    "a peer-to-peer micro-mentorship application",
    "an IoT sensor network with real-time alerts",
    "a no-code automation workflow engine",
    "a federated machine learning recommendation system",
    "a mobile-first community engagement platform",
    "a computer-vision quality inspection tool",
    "a conversational AI patient triage assistant",
    "a gamified financial literacy learning app"
]

TARGET_AUDIENCES = [
    "rural farmers", "first-generation college students",
    "government health workers", "early-stage startup founders",
    "logistics managers in emerging markets", "small business owners",
    "environmental compliance officers", "low-income urban households",
    "school teachers in tier-3 districts", "senior citizens"
]

COMPETITION_TYPES = [
    "National Hackathon", "Campus Ideathon", "Smart India Hackathon (SIH)",
    "Inter-College Innovation Challenge", "State-Level Startup Pitch",
    "IEEE Paper Presentation", "Product Design Sprint", "Data Science Olympiad",
    "Social Entrepreneurship Challenge", "Climate Action Hackathon"
]

STARTUP_ACHIEVEMENTS = [
    "Accepted into IIT Incubation Centre",
    "Won Best DeepTech Prototype at National Hackathon",
    "Secured Letter of Intent from Industry Partner",
    "Onboarded 500+ Beta Users",
    "Filed Provisional Patent",
    "Featured in YourStory Startup Edition",
    "Completed DST-NIDHI PRAYAS Grant",
    "Selected for Atal Incubation Mission",
    "Awarded BIRAC BIG Grant",
    "Reached ₹5 Lakh Monthly Recurring Revenue"
]

INVESTOR_TYPES = [
    "University Seed Fund",
    "Government TIDE 2.0 Grant",
    "Angel Syndicate (₹25L round)",
    "Tier-1 VC Partner (₹1Cr seed)",
    "Family Office Investment",
    "SIDBI Startup Mitra Fund",
    "Corporate Innovation Arm"
]

# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — HELPER FUNCTIONS (Noise-Reduction Utilities)
# ══════════════════════════════════════════════════════════════════════════════════

def pick_skills(all_skills, count_range=(1, 4)):
    """Picks a random subset of skills. Used for skills_possessed and skills_seeking."""
    k = random.randint(*count_range)
    return " | ".join(random.sample(all_skills, k=min(k, len(all_skills))))


def pick_seeking_skills(possessed_skills_str, all_skills):
    """
    🛡️ NOISE REDUCTION: A student should seek skills they DON'T already possess.
    This prevents the model from matching a student with someone who has identical skills.
    """
    possessed_set = set(possessed_skills_str.split(" | "))
    remaining    = [s for s in all_skills if s not in possessed_set]
    if not remaining:
        return "General Mentorship"
    k = random.randint(1, min(3, len(remaining)))
    return " | ".join(random.sample(remaining, k=k))


def calculate_portfolio_scale(competitions_participated, competitions_won, innovation_credits):
    """
    Weighted portfolio score (1–10).
    Formula: Participation (minor weight) + Wins (heavy weight) + Credits (moderate)
    🛡️ NOISE REDUCTION: Wins carry 3x more weight than mere participation.
    """
    raw = 1.0 + (competitions_participated * 0.15) + (competitions_won * 1.2) + (innovation_credits * 0.08)
    return round(min(10.0, raw), 1)


def build_semantic_pitch(industry):
    """
    Modular Semantic Construction — avoids buzzword soup.
    Creates a logically coherent sentence: We solve [PROBLEM] for [AUDIENCE] by building [SOLUTION].
    """
    problem  = random.choice(PROBLEM_SPACES)
    solution = random.choice(SOLUTION_APPROACHES)
    audience = random.choice(TARGET_AUDIENCES)
    return f"We solve {problem} for {audience} by building {solution} in the {industry} sector."


def get_investor_details(startup_achievement_scale):
    """
    🛡️ NOISE REDUCTION: Investor tier is tied to startup quality.
    Low-scale startups don't attract Tier-1 VCs — this prevents impossible pairings.
    """
    if startup_achievement_scale >= 8.5:
        return random.choice(["Tier-1 VC Partner (₹1Cr seed)", "Corporate Innovation Arm", "Angel Syndicate (₹25L round)"])
    elif startup_achievement_scale >= 6.5:
        return random.choice(["Government TIDE 2.0 Grant", "SIDBI Startup Mitra Fund", "University Seed Fund"])
    else:
        return "Bootstrapped"


def make_signature(row_dict):
    """
    🛡️ DEDUPLICATION ENGINE: Creates a SHA-256 fingerprint of every student's core traits.
    If two students have identical fingerprints, the second is DISCARDED and regenerated.
    This guarantees 100% unique records — the most important data quality constraint.
    """
    core = (
        f"{row_dict['vle_engagement_score']}"
        f"_{row_dict['entrepreneurial_grit_index']}"
        f"_{row_dict['competitions_participated']}"
        f"_{row_dict['competitions_won']}"
        f"_{row_dict['skills_possessed']}"
        f"_{row_dict['has_startup']}"
        f"_{row_dict['tech_readiness_level_trl']}"
        f"_{row_dict['mentorship_hours']}"
    )
    return hashlib.sha256(core.encode()).hexdigest()


# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — SINGLE STUDENT GENERATOR (All Business Logic Lives Here)
# ══════════════════════════════════════════════════════════════════════════════════

def generate_one_student():
    """
    Generates a single, fully correlated, noise-free student record.
    Every feature is causally linked to upstream features — no random orphan data.

    FEATURE PIPELINE:
      Base Behavior ──► Startup Probability ──► Startup Details ──► Success Label
    """

    # ── 1. BASE BEHAVIORAL METRICS (Digital Trace Data — cannot be self-faked) ──
    vle_engagement_score      = random.randint(10, 500)
    entrepreneurial_grit_index = round(random.uniform(1.0, 7.0), 1)
    innovation_credits_completed = random.randint(0, 12)

    # ── 2. COMPETITION LOGIC ──────────────────────────────────────────────────────
    # 🛡️ KEY CONDITION: competitions_won can NEVER exceed competitions_participated
    competitions_participated = random.randint(0, 12)
    if competitions_participated > 0:
        competitions_won = random.randint(0, competitions_participated)
        competition_history = " | ".join(
            random.sample(COMPETITION_TYPES, k=min(competitions_participated, len(COMPETITION_TYPES)))
        )
    else:
        competitions_won     = 0
        competition_history  = "None"

    # ── 3. PORTFOLIO ACHIEVEMENT SCALE (Derived — not independently random) ──────
    portfolio_achievement_scale = calculate_portfolio_scale(
        competitions_participated, competitions_won, innovation_credits_completed
    )

    # ── 4. PEER-TO-PEER MATCHING FEATURES ────────────────────────────────────────
    skills_possessed = pick_skills(TECH_SKILLS, count_range=(1, 4))
    # 🛡️ CONDITION: Skills sought must differ from skills possessed
    skills_seeking   = pick_seeking_skills(skills_possessed, TECH_SKILLS)

    # ── 5. STARTUP PROBABILITY ENGINE ────────────────────────────────────────────
    # Probability is CAUSALLY DRIVEN by measurable behavioral data
    startup_prob = 0.04  # Baseline: 4% of all students start ventures
    if vle_engagement_score > 300:          startup_prob += 0.18
    if entrepreneurial_grit_index > 5.0:    startup_prob += 0.22
    if competitions_won >= 2:               startup_prob += 0.16
    if innovation_credits_completed > 6:    startup_prob += 0.12

    has_startup = 1 if random.random() < startup_prob else 0

    # ── 6. STARTUP FEATURES (ONLY generated if has_startup == 1) ─────────────────
    # 🛡️ CONDITION: All startup columns default to zero/None for non-founders
    # This prevents the model from training on meaningless zeros in startup columns
    # for students who never founded anything.

    startup_industry            = "None"
    semantic_pitch_statement    = "None"
    tech_readiness_level_trl    = 0
    mentorship_hours            = 0
    founder_idea_fit_score      = 0.0
    market_readiness_score      = 0.0
    team_size                   = 0
    patents_filed               = 0
    technology_transfers_completed = 0
    revenue_generated_usd       = 0
    seed_funding_received       = 0
    startup_achievement         = "None"
    startup_achievement_scale   = 0.0
    investor_details            = "None"
    success_prediction_label    = 0

    if has_startup == 1:

        # 6a. Startup Identity
        startup_industry         = random.choice(INDUSTRIES)
        semantic_pitch_statement = build_semantic_pitch(startup_industry)

        # 6b. Core Startup Metrics
        trl            = random.randint(1, 9)
        mentor_hours   = random.randint(5, 100)
        team_size_val  = random.randint(1, 8)
        market_score   = round(random.uniform(0.3, 1.0), 2)

        # 6c. Founder-Idea Fit: Derived from grit + competitions (not random)
        base_fit = 0.35 + (entrepreneurial_grit_index * 0.05) + (competitions_won * 0.04)
        fit_val  = round(min(1.0, base_fit + random.uniform(0.0, 0.15)), 2)

        # 6d. IP & Commercialization Chain
        # 🛡️ CONDITION: Patents only possible if TRL > 6 (prototype stage reached)
        patents_val = random.randint(1, 3) if trl > 6 else 0

        # 🛡️ CONDITION: Tech transfers only if patents exist AND TRL >= 7
        if patents_val > 0 and trl >= 7:
            tech_transfers = random.randint(0, patents_val)
        else:
            tech_transfers = 0

        # 🛡️ CONDITION: Revenue only if market-ready (TRL ≥ 8) and transfers happened
        if trl >= 8 and tech_transfers > 0:
            revenue_val = tech_transfers * random.randint(8_000, 50_000)
        else:
            revenue_val = 0

        # 6e. Funding Logic
        # 🛡️ CONDITION: Seed funding tied to sufficient mentorship + TRL
        seed_funding = 1 if (mentor_hours > 40 and trl > 4) else 0

        # 6f. Startup Achievement (scale 1–10, higher for more developed startups)
        startup_ach_text  = random.choice(STARTUP_ACHIEVEMENTS)
        # Scale anchored to TRL and funding status — not random
        ach_scale_base    = 3.0 + (trl * 0.5) + (seed_funding * 1.5) + (patents_val * 0.5)
        ach_scale_val     = round(min(10.0, ach_scale_base + random.uniform(0.0, 1.0)), 1)

        # 6g. Investor Details (tier linked to achievement scale)
        investor_detail_val = get_investor_details(ach_scale_val)

        # 6h. SUCCESS PREDICTION LABEL — The Target Variable for Scikit-learn
        # 🛡️ STRICT CORRELATION: Model is trained on REAL causal logic
        # High TRL + sustained mentorship + founder fit = success
        success_chance = 0.0
        if trl >= 7:          success_chance += 0.45
        if mentor_hours > 50: success_chance += 0.28
        if fit_val > 0.75:    success_chance += 0.18
        if seed_funding == 1: success_chance += 0.10
        success_lbl = 1 if random.random() < success_chance else 0

        # ── Assign to the outer scope variables ──
        tech_readiness_level_trl       = trl
        mentorship_hours               = mentor_hours
        founder_idea_fit_score         = fit_val
        market_readiness_score         = market_score
        team_size                      = team_size_val
        patents_filed                  = patents_val
        technology_transfers_completed = tech_transfers
        revenue_generated_usd          = revenue_val
        seed_funding_received          = seed_funding
        startup_achievement            = startup_ach_text
        startup_achievement_scale      = ach_scale_val
        investor_details               = investor_detail_val
        success_prediction_label       = success_lbl

    # ── 7. ASSEMBLE THE FULL STUDENT RECORD ──────────────────────────────────────
    return {
        # ── Identifiers ─────────────────────────────────────────────────────────
        "student_id":                      "PLACEHOLDER",   # Assigned after dedup

        # ── Predictive ML Features (Scikit-learn / XGBoost) ─────────────────────
        "vle_engagement_score":            vle_engagement_score,
        "entrepreneurial_grit_index":      entrepreneurial_grit_index,
        "innovation_credits_completed":    innovation_credits_completed,
        "competitions_participated":       competitions_participated,
        "competitions_won":                competitions_won,
        "portfolio_achievement_scale":     portfolio_achievement_scale,

        # ── NLP Peer-Matching Features (spaCy / Content-Based Filtering) ────────
        "skills_possessed":                skills_possessed,
        "skills_seeking":                  skills_seeking,
        "competition_history":             competition_history,

        # ── Startup Core Features ────────────────────────────────────────────────
        "has_startup":                     has_startup,
        "startup_industry":                startup_industry,

        # ── NLP Investor-Matchmaking Feature (LLM / Cosine Similarity) ──────────
        "semantic_pitch_statement":        semantic_pitch_statement,

        # ── Advanced Startup Predictors (for Scikit-learn) ───────────────────────
        "tech_readiness_level_trl":        tech_readiness_level_trl,
        "mentorship_hours":                mentorship_hours,
        "founder_idea_fit_score":          founder_idea_fit_score,
        "market_readiness_score":          market_readiness_score,
        "team_size":                       team_size,

        # ── NIRF/ARIIA Institutional Compliance Features (Dashboard) ────────────
        "patents_filed":                   patents_filed,
        "technology_transfers_completed":  technology_transfers_completed,
        "revenue_generated_usd":           revenue_generated_usd,
        "seed_funding_received":           seed_funding_received,

        # ── Startup Achievement Features ─────────────────────────────────────────
        "startup_achievement":             startup_achievement,
        "startup_achievement_scale":       startup_achievement_scale,
        "investor_details":                investor_details,

        # ── Target Variable (ML Label) ────────────────────────────────────────────
        "success_prediction_label":        success_prediction_label,
    }


# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — GPU-VECTORIZED BATCH GENERATOR
#  When GPU is available, numerical features are computed in massive parallel batches.
#  Text fields are generated on CPU (GPU struggles with string manipulation).
# ══════════════════════════════════════════════════════════════════════════════════

def generate_gpu_batch_numerics(batch_size):
    """
    Generates all NUMERICAL features for an entire batch simultaneously on the GPU.
    Returns a dictionary of numpy/cupy arrays — one value per student.

    This replaces the slow Python for-loop with vectorized GPU operations,
    making the generation of 13,000 rows as fast as generating 1 row.
    """
    N = batch_size

    # ── Base behavioral signals ───────────────────────────────────────────────
    vle   = cp.random.randint(10, 501,  size=N)
    grit  = cp.round(cp.random.uniform(1.0, 7.0, size=N), 1)
    icred = cp.random.randint(0, 13,    size=N)

    # ── Competition logic ─────────────────────────────────────────────────────
    comp_part = cp.random.randint(0, 13, size=N)
    # 🛡️ CONDITION: won <= participated (vectorized clamp)
    comp_won  = cp.array([
        random.randint(0, int(p)) if p > 0 else 0
        for p in comp_part.tolist()
    ])

    # Portfolio scale (vectorized formula)
    portfolio = cp.round(
        cp.clip(1.0 + (comp_part * 0.15) + (comp_won * 1.2) + (icred * 0.08), 1.0, 10.0), 1
    )

    # ── Startup probability (vectorized conditional accumulation) ─────────────
    prob = cp.full(N, 0.04)
    prob = cp.where(vle  > 300, prob + 0.18, prob)
    prob = cp.where(grit > 5.0, prob + 0.22, prob)
    prob = cp.where(comp_won >= 2, prob + 0.16, prob)
    prob = cp.where(icred > 6,    prob + 0.12, prob)
    has_startup = (cp.random.uniform(0, 1, size=N) < prob).astype(cp.int32)

    # ── Startup numerics (only meaningful for has_startup==1) ────────────────
    trl_raw   = cp.random.randint(1, 10, size=N)
    trl       = cp.where(has_startup == 1, trl_raw, 0)
    ment_raw  = cp.random.randint(5, 101, size=N)
    ment      = cp.where(has_startup == 1, ment_raw, 0)
    team_raw  = cp.random.randint(1, 9,   size=N)
    team      = cp.where(has_startup == 1, team_raw, 0)
    mkt_raw   = cp.round(cp.random.uniform(0.3, 1.0, size=N), 2)
    mkt       = cp.where(has_startup == 1, mkt_raw, 0.0)

    # Founder fit: causally linked to grit and wins
    base_fit  = cp.clip(0.35 + (grit * 0.05) + (comp_won * 0.04), 0.0, 1.0)
    fit_noise = cp.random.uniform(0.0, 0.15, size=N)
    fit       = cp.round(cp.clip(base_fit + fit_noise, 0.0, 1.0), 2)
    fit       = cp.where(has_startup == 1, fit, 0.0)

    # 🛡️ CONDITION: patents only if trl > 6
    pat_raw   = cp.array([random.randint(1, 3) for _ in range(N)])
    patents   = cp.where((has_startup == 1) & (trl > 6), pat_raw, 0)

    # 🛡️ CONDITION: tech transfers only if patents > 0 AND trl >= 7
    xfer_raw  = cp.array([random.randint(0, max(1, int(p))) for p in patents.tolist()])
    transfers = cp.where((patents > 0) & (trl >= 7), xfer_raw, 0)

    # 🛡️ CONDITION: revenue only if trl >= 8 AND transfers happened
    rev_mult  = cp.array([random.randint(8_000, 50_000) for _ in range(N)])
    revenue   = cp.where((trl >= 8) & (transfers > 0), transfers * rev_mult, 0)

    # 🛡️ CONDITION: seed funding requires adequate mentorship AND decent TRL
    seed      = cp.where((ment > 40) & (trl > 4), 1, 0).astype(cp.int32)
    seed      = cp.where(has_startup == 1, seed, 0)

    # Achievement scale — anchored to TRL and funding
    ach_base  = cp.clip(3.0 + (trl * 0.5) + (seed * 1.5) + (patents * 0.5), 1.0, 9.0)
    ach_noise = cp.random.uniform(0.0, 1.0, size=N)
    ach_scale = cp.round(cp.clip(ach_base + ach_noise, 1.0, 10.0), 1)
    ach_scale = cp.where(has_startup == 1, ach_scale, 0.0)

    # SUCCESS LABEL — strict causal correlation for Scikit-learn training
    s_chance  = cp.zeros(N)
    s_chance  = cp.where((has_startup == 1) & (trl  >= 7),  s_chance + 0.45, s_chance)
    s_chance  = cp.where((has_startup == 1) & (ment  > 50), s_chance + 0.28, s_chance)
    s_chance  = cp.where((has_startup == 1) & (fit   > 0.75), s_chance + 0.18, s_chance)
    s_chance  = cp.where((has_startup == 1) & (seed  == 1), s_chance + 0.10, s_chance)
    success   = (cp.random.uniform(0, 1, size=N) < s_chance).astype(cp.int32)
    success   = cp.where(has_startup == 1, success, 0)

    # Convert back to numpy for easy row-by-row text augmentation
    def to_list(arr):
        return arr.get().tolist() if GPU_AVAILABLE else arr.tolist()

    return {
        "vle":        to_list(vle),
        "grit":       to_list(grit),
        "icred":      to_list(icred),
        "comp_part":  to_list(comp_part),
        "comp_won":   to_list(comp_won),
        "portfolio":  to_list(portfolio),
        "has_startup":to_list(has_startup),
        "trl":        to_list(trl),
        "ment":       to_list(ment),
        "team":       to_list(team),
        "mkt":        to_list(mkt),
        "fit":        to_list(fit),
        "patents":    to_list(patents),
        "transfers":  to_list(transfers),
        "revenue":    to_list(revenue),
        "seed":       to_list(seed),
        "ach_scale":  to_list(ach_scale),
        "success":    to_list(success),
    }


# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — MAIN GENERATION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════════

def generate_master_dataset():
    """
    Main orchestrator.  Runs the GPU batch numeric generation, augments with
    semantic text fields on CPU, deduplicates via SHA-256 signatures, and
    writes exactly TARGET_STUDENTS unique records to CSV.
    """
    print("=" * 70)
    print("  Campus Innovation & Engagement Hub — Master Dataset Generator")
    print(f"  Target: {TARGET_STUDENTS:,} unique student records")
    print(f"  Mode: {'GPU (RAPIDS)' if GPU_AVAILABLE else 'CPU (numpy)'}")
    print("=" * 70)

    start_time   = time.time()
    seen_sigs    = set()      # SHA-256 fingerprints of already-written rows
    unique_count = 0
    total_attempted = 0

    output_path = "C:\\Users\\Sanjay\\OneDrive\\Documents\\Hackathon\\Renkei\\campus_innovation_10k_dataset.csv"

    FIELDNAMES = [
        "student_id",
        # ML Predictive Features
        "vle_engagement_score", "entrepreneurial_grit_index",
        "innovation_credits_completed", "competitions_participated",
        "competitions_won", "portfolio_achievement_scale",
        # NLP Peer-Matching Features
        "skills_possessed", "skills_seeking", "competition_history",
        # Startup Core
        "has_startup", "startup_industry",
        # NLP Investor-Matchmaking
        "semantic_pitch_statement",
        # Startup Predictors
        "tech_readiness_level_trl", "mentorship_hours",
        "founder_idea_fit_score", "market_readiness_score", "team_size",
        # NIRF/ARIIA Compliance
        "patents_filed", "technology_transfers_completed",
        "revenue_generated_usd", "seed_funding_received",
        # Achievement Features
        "startup_achievement", "startup_achievement_scale", "investor_details",
        # Target Variable
        "success_prediction_label",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()

        while unique_count < TARGET_STUDENTS:
            # ── Generate a GPU batch of numerics ─────────────────────────────
            batch = generate_gpu_batch_numerics(GENERATE_BATCH)
            total_attempted += GENERATE_BATCH

            for i in range(GENERATE_BATCH):
                if unique_count >= TARGET_STUDENTS:
                    break

                hs  = batch["has_startup"][i]
                trl = batch["trl"][i]
                ach = batch["ach_scale"][i]
                cp_part = batch["comp_part"][i]

                # ── Augment with CPU text fields ──────────────────────────────
                industry    = random.choice(INDUSTRIES) if hs == 1 else "None"
                pitch       = build_semantic_pitch(industry) if hs == 1 else "None"
                ach_text    = random.choice(STARTUP_ACHIEVEMENTS) if hs == 1 else "None"
                inv_details = get_investor_details(ach) if hs == 1 else "None"

                skills_pos  = pick_skills(TECH_SKILLS, count_range=(1, 4))
                skills_seek = pick_seeking_skills(skills_pos, TECH_SKILLS)

                if cp_part > 0:
                    comp_hist = " | ".join(
                        random.sample(COMPETITION_TYPES, k=min(int(cp_part), len(COMPETITION_TYPES)))
                    )
                else:
                    comp_hist = "None"

                # ── Build row dict ────────────────────────────────────────────
                row = {
                    "student_id":                      "PLACEHOLDER",
                    "vle_engagement_score":            batch["vle"][i],
                    "entrepreneurial_grit_index":      batch["grit"][i],
                    "innovation_credits_completed":    batch["icred"][i],
                    "competitions_participated":       int(cp_part),
                    "competitions_won":                batch["comp_won"][i],
                    "portfolio_achievement_scale":     batch["portfolio"][i],
                    "skills_possessed":                skills_pos,
                    "skills_seeking":                  skills_seek,
                    "competition_history":             comp_hist,
                    "has_startup":                     hs,
                    "startup_industry":                industry,
                    "semantic_pitch_statement":        pitch,
                    "tech_readiness_level_trl":        trl,
                    "mentorship_hours":                batch["ment"][i],
                    "founder_idea_fit_score":          batch["fit"][i],
                    "market_readiness_score":          batch["mkt"][i],
                    "team_size":                       batch["team"][i],
                    "patents_filed":                   batch["patents"][i],
                    "technology_transfers_completed":  batch["transfers"][i],
                    "revenue_generated_usd":           batch["revenue"][i],
                    "seed_funding_received":           batch["seed"][i],
                    "startup_achievement":             ach_text,
                    "startup_achievement_scale":       ach,
                    "investor_details":                inv_details,
                    "success_prediction_label":        batch["success"][i],
                }

                # ── Deduplication check ───────────────────────────────────────
                sig = make_signature(row)
                if sig in seen_sigs:
                    continue   # Duplicate detected — discard silently

                # ── Unique record confirmed — write it ────────────────────────
                seen_sigs.add(sig)
                unique_count += 1
                row["student_id"] = f"STU{unique_count:05d}"
                writer.writerow(row)

                # Progress logging every 2000 records
                if unique_count % 2_000 == 0:
                    elapsed = time.time() - start_time
                    dup_rate = ((total_attempted - unique_count) / total_attempted) * 100
                    print(f"  ✅ {unique_count:,} / {TARGET_STUDENTS:,} unique records "
                          f"| Elapsed: {elapsed:.1f}s | Dup-discard rate: {dup_rate:.1f}%")

    elapsed     = time.time() - start_time
    dup_rate    = ((total_attempted - unique_count) / total_attempted) * 100

    print("\n" + "=" * 70)
    print(f"  🎉  SUCCESS — Dataset generation complete!")
    print(f"  📁  Output file : {output_path}")
    print(f"  👤  Records     : {unique_count:,} (100% unique, zero duplicates)")
    print(f"  🗑️   Discarded   : {total_attempted - unique_count:,} duplicate rows ({dup_rate:.1f}%)")
    print(f"  ⏱️   Time elapsed: {elapsed:.2f} seconds")
    print(f"  📊  Features    : 25 columns (ML + NLP + NIRF + Achievement)")
    print("=" * 70)
    print("\n  📌  Feature Coverage Summary:")
    print("    ├── Predictive ML (Scikit-learn/XGBoost) : vle, grit, trl,")
    print("    │   mentorship_hours, fit_score, success_label, etc.")
    print("    ├── NLP Matching (spaCy/LLMs)            : semantic_pitch_statement,")
    print("    │   skills_possessed, skills_seeking")
    print("    ├── Graph SNA (Neo4j edges)               : via student_id as node keys")
    print("    ├── NIRF/ARIIA Compliance (Dashboards)   : patents_filed,")
    print("    │   tech_transfers, revenue, seed_funding")
    print("    └── Portfolio Generator (React frontend) : portfolio_achievement_scale,")
    print("        startup_achievement, investor_details")
    print("\n  ✅  Ready for Phase 3: Django models.py ingestion + ML training!")


# ══════════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — NOISE SUMMARY (What we actively prevented)
# ══════════════════════════════════════════════════════════════════════════════════
NOISE_SUMMARY = """
╔══════════════════════════════════════════════════════════════════════╗
║                NOISE REDUCTION TECHNIQUES APPLIED                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  1. Self-Reporting Bias      → Replaced with VLE digital trace     ║
║     (students lying on forms)  data (vle_engagement_score)         ║
║                                                                    ║
║  2. Buzzword Text Noise      → Modular Semantic Construction       ║
║     (Lorem Ipsum / jargon)     (Problem + Audience + Solution)     ║
║                                                                    ║
║  3. Logical Inconsistencies  → Conditional gates enforced:         ║
║     (wins > participated,       • wins ≤ participated              ║
║      patents w/o prototype,     • patents only if TRL > 6          ║
║      revenue w/o market fit)    • revenue only if TRL ≥ 8          ║
║                                                                    ║
║  4. Orphan Startup Data      → Startup columns hard-zero'd         ║
║     (null/0 for non-founders)   for non-founders to avoid          ║
║                                 model confusion                    ║
║                                                                    ║
║  5. Random Success Labels    → Causally linked: TRL + Mentorship   ║
║     (flipping coins)            + Founder Fit → Success            ║
║                                                                    ║
║  6. Duplicate Rows           → SHA-256 signature deduplication     ║
║     (model overfitting)         on core behavioral traits          ║
║                                                                    ║
║  7. Investor-Startup Mismatch→ Tier linked to achievement scale    ║
║     (VC funding for day-1)     (Bootstrapped → VC only via scale) ║
╚══════════════════════════════════════════════════════════════════════╝
"""

# ── ENTRY POINT ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(NOISE_SUMMARY)
    generate_master_dataset()