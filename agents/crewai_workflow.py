"""
CrewAI Multi-Agent Workflow for AgentApply AI
Orchestrates role-based autonomous agents using the CrewAI framework.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.logger import get_logger

logger = get_logger("CrewAIWorkflow")

try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import tool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


# ==============================================================================
# CrewAI Custom Automation Tools
# ==============================================================================
if CREWAI_AVAILABLE:
    @tool("Scrape Enterprise Job Boards")
    def scrape_jobs_tool() -> str:
        """Scrapes Greenhouse, Lever, and RemoteOK API career boards for open developer roles."""
        from agents.agent_scraper_v2 import SafeJobScraperAgent
        scraper = SafeJobScraperAgent()
        count = scraper.run()
        return f"Successfully ingested {count} new jobs into the database."

    @tool("Score and Filter Candidate Qualifications")
    def score_jobs_tool() -> str:
        """Matches candidate resume competencies against scraped job descriptions using heuristic scoring."""
        from agents.job_database import get_jobs_by_status
        from agents.job_matcher import score_job
        from agents.resume_parser import get_parsed_resume
        resume = get_parsed_resume()
        scraped = get_jobs_by_status("scraped")
        eligible_count = 0
        for job in scraped:
            res = score_job(job, resume)
            if res.get("eligible", False):
                eligible_count += 1
        return f"Evaluated {len(scraped)} jobs. Identified {eligible_count} qualified positions meeting threshold."

    @tool("Submit Applications via Playwright Browser")
    def submit_applications_tool() -> str:
        """Automates form filling, resume uploads, and submissions on ATS portals using Playwright."""
        from agents.agent_applier_v3 import PlaywrightJobApplierAgent
        applier = PlaywrightJobApplierAgent()
        applied = applier.run()
        return f"Playwright automation successfully submitted {applied} applications."

    @tool("Audit Applications and Sync Spreadsheet")
    def sync_tracker_tool() -> str:
        """Updates color-coded Excel spreadsheet records and dispatches summary reports."""
        from agents.agent_excel_tracker import ExcelTrackerAgent
        from agents.agent_email_notifier import EmailNotifierAgent
        ExcelTrackerAgent().run()
        EmailNotifierAgent().run()
        return "Application tracking records synchronized to Excel and summary report dispatched."


# ==============================================================================
# Crew Construction & Execution
# ==============================================================================
def build_crew() -> Crew:
    """Builds and returns the configured CrewAI team."""
    if not CREWAI_AVAILABLE:
        raise ImportError("CrewAI is not installed. Install via: pip install -r requirements-crewai.txt")

    # Agent 1: Market Ingestion Specialist
    job_hunter = Agent(
        role="Career Opportunity Scout",
        goal="Discover high-relevance software engineering positions across corporate ATS platforms.",
        backstory="An expert talent scout specialized in querying enterprise career APIs (Greenhouse, Lever, RemoteOK) with zero downtime.",
        tools=[scrape_jobs_tool],
        verbose=True
    )

    # Agent 2: Candidate Qualification Analyst
    qualification_matcher = Agent(
        role="Candidate Qualification Evaluator",
        goal="Filter out misaligned senior roles and rank entry/mid positions matching candidate tech stack.",
        backstory="A seasoned technical recruiter adept at analyzing resume token overlaps and enforcing strict experience level criteria.",
        tools=[score_jobs_tool],
        verbose=True
    )

    # Agent 3: Headless Browser Applier
    application_submitter = Agent(
        role="ATS Form Automation Specialist",
        goal="Accurately fill out job application forms, upload PDF resumes, and handle screening questions.",
        backstory="An automation engineer proficient with Playwright browser controls and anti-detection evasion techniques.",
        tools=[submit_applications_tool],
        verbose=True
    )

    # Agent 4: Audit & Reporting Auditor
    reporting_auditor = Agent(
        role="Application Audit & Delivery Auditor",
        goal="Maintain audit trails in formatted Excel spreadsheets and dispatch HTML performance updates.",
        backstory="A meticulous data coordinator responsible for verifying application proofs and updating stakeholders.",
        tools=[sync_tracker_tool],
        verbose=True
    )

    # Sequential Tasks
    task_scouting = Task(
        description="Scan all registered company career endpoints and fetch recent job openings.",
        expected_output="Summary of newly discovered and indexed job records.",
        agent=job_hunter
    )

    task_matching = Task(
        description="Evaluate scraped jobs against candidate resume skills, penalize senior titles, and tag eligible candidates.",
        expected_output="List of qualified jobs with scores meeting or exceeding minimum thresholds.",
        agent=qualification_matcher
    )

    task_submitting = Task(
        description="Execute browser automation to submit applications for all verified eligible positions.",
        expected_output="Count of confirmed submissions with direct proof links.",
        agent=application_submitter
    )

    task_auditing = Task(
        description="Sync latest submission states into Excel tracker and trigger email delivery notification.",
        expected_output="Confirmation of synchronized spreadsheet and email report delivery.",
        agent=reporting_auditor
    )

    return Crew(
        agents=[job_hunter, qualification_matcher, application_submitter, reporting_auditor],
        tasks=[task_scouting, task_matching, task_submitting, task_auditing],
        process=Process.sequential,
        verbose=True
    )


def run_crewai_cycle():
    """Executes a full multi-agent cycle using CrewAI."""
    logger.info("Initializing CrewAI Multi-Agent Workflow...")
    if not CREWAI_AVAILABLE:
        logger.warning("CrewAI not found in environment. Falling back to native agent pipeline.")
        from agents.orchestrator import run_full_cycle
        return run_full_cycle()

    crew = build_crew()
    result = crew.kickoff()
    logger.info(f"CrewAI execution completed with output: {result}")
    return result


if __name__ == "__main__":
    run_crewai_cycle()
