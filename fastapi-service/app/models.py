from pydantic import BaseModel, Field


class Claim(BaseModel):
    claimId: str = Field(..., description="Unique claim identifier")
    customerId: str = Field(..., description="Customer identifier")
    amount: float = Field(..., gt=0, description="Claim amount")
    claimType: str = Field(..., description="Type of claim")
    description: str = Field(..., description="Claim description")
    timestamp: int = Field(..., description="Event timestamp (epoch millis)")


class ManagerAction(BaseModel):
    claimId: str = Field(..., description="Claim identifier")
    action: str = Field(..., description="RELEASE or REJECT")
    managerId: str = Field(..., description="Manager identifier")
