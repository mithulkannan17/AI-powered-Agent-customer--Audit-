from fastapi import APIRouter
from app.services.agent_metrics_service import AgentMetricsService
from app.services.admin_kpi_service import AdminKPIService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/agent-leaderboard")
async def agent_leaderboard():
    return await AgentMetricsService.compute_leaderboard()

@router.get("/kpis")
async def get_admin_kpis():
    return await AdminKPIService.get_kpis()
