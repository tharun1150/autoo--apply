# ==============================================================================
# AgentApply AI - DevOps Automation Makefile
# ==============================================================================

.PHONY: help up-crewai down-crewai logs-crewai up-langgraph down-langgraph logs-langgraph clean

help:
	@echo "Available commands:"
	@echo "  make up-crewai          Start stack with CrewAI multi-agent engine"
	@echo "  make up-crewai-n8n      Start stack with CrewAI + n8n automation"
	@echo "  make down-crewai        Stop CrewAI stack"
	@echo "  make logs-crewai        Stream logs from CrewAI containers"
	@echo ""
	@echo "  make up-langgraph       Start stack with LangGraph state machine engine"
	@echo "  make up-langgraph-n8n   Start stack with LangGraph + n8n automation"
	@echo "  make down-langgraph     Stop LangGraph stack"
	@echo "  make logs-langgraph     Stream logs from LangGraph containers"
	@echo ""
	@echo "  make clean              Remove stopped containers and dangling images"

# ------------------------------------------------------------------------------
# CrewAI Multi-Agent Stack
# ------------------------------------------------------------------------------
up-crewai:
	docker compose -f docker-compose.crewai.yml up --build -d

up-crewai-n8n:
	docker compose -f docker-compose.crewai.yml --profile with-n8n up --build -d

down-crewai:
	docker compose -f docker-compose.crewai.yml down

logs-crewai:
	docker compose -f docker-compose.crewai.yml logs -f

# ------------------------------------------------------------------------------
# LangGraph Multi-Agent Stack
# ------------------------------------------------------------------------------
up-langgraph:
	docker compose -f docker-compose.langgraph.yml up --build -d

up-langgraph-n8n:
	docker compose -f docker-compose.langgraph.yml --profile with-n8n up --build -d

down-langgraph:
	docker compose -f docker-compose.langgraph.yml down

logs-langgraph:
	docker compose -f docker-compose.langgraph.yml logs -f

# ------------------------------------------------------------------------------
# Maintenance
# ------------------------------------------------------------------------------
clean:
	docker system prune -f
