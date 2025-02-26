from typing import List
from pydantic import BaseModel, Field

class PlanType(BaseModel):
    plan: str = Field(..., title="Plan", description="Plan for the task")
    e_number: int = Field(..., title="E Number", description="Variable number for the extracted content")
    tool : str = Field(..., title="Tool", description="Tool to use for the plan")
    tool_params: str = Field(..., title="Tool Parameters", description="Parameters for the tool")

class PlanList(BaseModel):
    plans: List[PlanType] = Field(..., title="Plans", description="List of plans for the task")
    
