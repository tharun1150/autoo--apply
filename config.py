"""
Configuration for the Job Auto-Apply Bot
Fill in your credentials and preferences below.
"""
import os
from pathlib import Path

# ============================================================
# RESUME
# ============================================================
BASE_DIR = Path(__file__).parent
RESUME_PATH = os.getenv("RESUME_PATH", str(BASE_DIR / "resume.pdf"))

# ============================================================
# JOB SEARCH SETTINGS
# ============================================================
SEARCH_QUERIES = [
    "Software Engineer",
    "Python Developer",
    "Full Stack Developer",
    "Backend Developer",
    "Software Developer",
    "Data Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
]

LOCATIONS = [
    "United States",
    "Remote",
]

# Filter settings
EXPERIENCE_LEVEL = ["Entry level", "Associate", "Mid-Senior level"]
JOB_TYPE = ["Full-time", "Contract"]
REMOTE_FILTER = ["Remote", "Hybrid"]

# How many jobs to apply per platform per run
DAILY_TARGET = 50
LINKEDIN_TARGET = 20
INDEED_TARGET = 15
DICE_TARGET = 15

# ============================================================
# LINKEDIN CREDENTIALS
# ============================================================
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "YOUR_LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "YOUR_LINKEDIN_PASSWORD")

# ============================================================
# INDEED CREDENTIALS  (Indeed uses email-based login)
# ============================================================
INDEED_EMAIL = os.getenv("INDEED_EMAIL", "YOUR_INDEED_EMAIL")
INDEED_PASSWORD = os.getenv("INDEED_PASSWORD", "YOUR_INDEED_PASSWORD")

# ============================================================
# DICE CREDENTIALS
# ============================================================
DICE_EMAIL = os.getenv("DICE_EMAIL", "YOUR_DICE_EMAIL")
DICE_PASSWORD = os.getenv("DICE_PASSWORD", "YOUR_DICE_PASSWORD")

# ============================================================
# PERSONAL INFO FOR FORM FILLING
# ============================================================
PERSONAL_INFO = {
    "first_name": os.getenv("FIRST_NAME", "YourFirstName"),
    "last_name": os.getenv("LAST_NAME", "YourLastName"),
    "email": os.getenv("PERSONAL_EMAIL", ""),
    "phone": os.getenv("PERSONAL_PHONE", ""),
    "city": os.getenv("CITY", "YourCity"),
    "state": os.getenv("STATE", "YourState"),
    "zip": os.getenv("ZIP_CODE", "00000"),
    "country": os.getenv("COUNTRY", "United States"),
    "linkedin_url": os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/tharunchwdry"),
    "github_url": os.getenv("GITHUB_URL", "https://github.com/tharun1150"),
    "portfolio_url": os.getenv("PORTFOLIO_URL", "https://allatharun.onrender.com/"),
    "years_of_experience": os.getenv("YEARS_EXPERIENCE", "1"),
    "work_authorization": os.getenv("WORK_AUTHORIZATION", "Yes"),
    "sponsorship_needed": os.getenv("SPONSORSHIP_NEEDED", "No"),
    "salary_expectation": os.getenv("SALARY_EXPECTATION", "90000"),
    "available_start": os.getenv("AVAILABLE_START", "Immediately"),
    "education": os.getenv("EDUCATION_LEVEL", "Master's"),
    "willing_to_relocate": os.getenv("WILLING_TO_RELOCATE", "Yes"),
}

# ============================================================
# BROWSER SETTINGS
# ============================================================
HEADLESS = False  # Set True to run browser in background (less detectable if False)
SLOW_MO = 1.5    # Seconds between actions (human-like delay)
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10

# ============================================================
# APPLICATION TRACKING
# ============================================================
TRACKER_DB = os.path.join(os.path.dirname(__file__), "applied_jobs.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "bot.log")

# ============================================================
# ANTI-DETECTION
# ============================================================
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
RANDOM_DELAY_MIN = 1.0
RANDOM_DELAY_MAX = 3.5
