"""
LangGraph State-Machine Workflow for AgentApply AI
Orchestrates cyclic agent graphs with state persistence, conditional edges, and fallback retries.
"""
from __future__ import annotations
import os
import sys
from typing import TypedDict, List, Dict, Any
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.logger import get_logger

logger = get_logger("LangGraphWorkflow")

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False


# ==============================================================================
# LangGraph Shared Pipeline State
# ==============================================================================
class AgentWorkflowState(TypedDict):
    discovered_count: int
    eligible_count: int
    applied_count: int
    failed_count: int
    current_stage: str
    error: str | None


# ==============================================================================
# Graph Node Definitions
# ==============================================================================
def node_scrape_jobs(state: AgentWorkflowState) -> AgentWorkflowState:
    """Stage 1: Parallel Ingestion from Greenhouse / Lever / RemoteOK."""
    logger.info("LangGraph [Node 1]: Ingesting corporate career boards...")
    from agents.agent_scraper_v2 import SafeJobScraperAgent
    count = SafeJobScraperAgent().run()
    state["discovered_count"] = count
    state["current_stage"] = "scraped"
    return state


def node_match_qualifications(state: AgentWorkflowState) -> AgentWorkflowState:
    """Stage 2: Heuristic & Resume Match Scoring with Experience Filtering."""
    logger.info("LangGraph [Node 2]: Evaluating candidate qualifications...")
    from agents.job_database import get_jobs_by_status
    from agents.job_matcher import score_job
    from agents.resume_parser import get_parsed_resume

    resume = get_parsed_resume()
    scraped_jobs = get_jobs_by_status("scraped")
    eligible = 0

    for job in scraped_jobs:
        match_result = score_job(job, resume)
        if match_result.get("eligible", False):
            eligible += 1

    state["eligible_count"] = eligible
    state["current_stage"] = "matched"
    return state


def node_apply_playwright(state: AgentWorkflowState) -> AgentWorkflowState:
    """Stage 3: Headless Playwright Browser Automation for ATS Form Submission."""
    logger.info("LangGraph [Node 3]: Submitting ATS applications via Playwright...")
    from agents.agent_applier_v3 import PlaywrightJobApplierAgent
    applied = PlaywrightJobApplierAgent().run()
    state["applied_count"] = applied
    state["current_stage"] = "applied"
    return state


def node_sync_and_report(state: AgentWorkflowState) -> AgentWorkflowState:
    """Stage 4: Excel Spreadsheet Sync and HTML Email Dispatch."""
    logger.info("LangGraph [Node 4]: Synchronizing Excel audit logs and dispatching summary...")
    from agents.agent_excel_tracker import ExcelTrackerAgent
    from agents.agent_email_notifier import EmailNotifierAgent

    try:
        ExcelTrackerAgent().run()
        EmailNotifierAgent().run()
    except Exception as exc:
        state["error"] = str(exc)

    state["current_stage"] = "completed"
    return state


# ==============================================================================
# Conditional Edge Routing
# ==============================================================================
def should_apply(state: AgentWorkflowState) -> str:
    """
    Conditional Edge Decision:
    If qualified jobs exist, transition to Playwright browser submission.
    Otherwise, bypass browser launch and transition straight to reporting.
    """
    if state.get("eligible_count", 0) > 0:
        logger.info(f"LangGraph Routing: Found {state['eligible_count']} eligible jobs. Routing to 'apply_node'.")
        return "apply_node"
    logger.info("LangGraph Routing: No eligible jobs found. Skipping browser launch, routing to 'report_node'.")
    return "report_node"


# ==============================================================================
# Graph Assembly & Compilation
# ==============================================================================
def build_langgraph_workflow():
    """Builds and compiles the state graph."""
    if not LANGGRAPH_AVAILABLE:
        raise ImportError("LangGraph is not installed. Install via: pip install -r requirements-langgraph.txt")

    workflow = StateGraph(AgentWorkflowState)

    # Register Nodes
    workflow.add_node("scrape_node", node_scrape_jobs)
    workflow.add_node("match_node", node_match_qualifications)
    workflow.add_node("apply_node", node_apply_playwright)
    workflow.add_node("report_node", node_sync_and_report)

    # Define Control Flow Edges
    workflow.set_entry_point("scrape_node")
    workflow.add_edge("scrape_node", "match_node")

    # Conditional Branching
    workflow.add_conditional_edges(
        "match_node",
        should_apply,
        {
            "apply_node": "apply_node",
            "report_node": "report_node"
        }
    )

    workflow.add_edge("apply_node", "report_node")
    workflow.add_edge("report_node", END)

    return workflow.compile()


def run_langgraph_cycle():
    """Executes a full stateful graph cycle using LangGraph."""
    logger.info("Initializing LangGraph State-Machine Workflow...")
    if not LANGGRAPH_AVAILABLE:
        logger.warning("LangGraph not found in environment. Falling back to native agent pipeline.")
        from agents.orchestrator import run_full_cycle
        return run_full_cycle()

    graph = build_langgraph_workflow()
    initial_state: AgentWorkflowState = {
        "discovered_count": 0,
        "eligible_count": 0,
        "applied_count": 0,
        "failed_count": 0,
        "current_stage": "initialized",
        "error": None,
    }

    final_state = graph.invoke(initial_state)
    logger.info(f"LangGraph execution finished: {final_state}")
    return final_state


if __name__ == "__main__":
    run_langgraph_cycle()
