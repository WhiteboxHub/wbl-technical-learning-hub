from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ContainerStatus = Literal["docked", "in_transit", "customs_hold", "delivered"]


class ContainerCreate(BaseModel):
    container_code: str = Field(..., min_length=4, max_length=20, examples=["MSCU1234567"])
    cargo: str = Field(..., min_length=1, max_length=120, examples=["Microchips & Servers"])
    origin_port: str = Field(..., min_length=2, max_length=80, examples=["Shenzhen"])
    destination_port: str = Field(..., min_length=2, max_length=80, examples=["Rotterdam"])
    weight_kg: int = Field(..., gt=0, le=30480, examples=[18500])
    status: ContainerStatus = "docked"


class ContainerUpdate(BaseModel):
    cargo: str | None = Field(default=None, min_length=1, max_length=120)
    destination_port: str | None = Field(default=None, min_length=2, max_length=80)
    weight_kg: int | None = Field(default=None, gt=0, le=30480)
    status: ContainerStatus | None = None


class ContainerRecord(ContainerCreate):
    id: int
    created_at: str

