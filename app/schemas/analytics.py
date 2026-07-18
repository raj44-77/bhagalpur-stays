"""Analytics schemas"""
from pydantic import BaseModel
from typing import List, Optional


class KPIResponse(BaseModel):
    total_hotels: int = 0
    active_users: int = 0
    total_bookings: int = 0
    total_revenue: float = 0
    avg_rating: float = 0
    occupancy_rate: float = 0


class ChartData(BaseModel):
    label: str
    value: float


class DashboardResponse(BaseModel):
    kpis: KPIResponse
    weekly_bookings: List[ChartData] = []
    recent_bookings: List[dict] = []
    pending_approvals: int = 0