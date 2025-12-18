from pydantic import BaseModel


class PCIEInfo(BaseModel):
    """Topology information for accelerators."""
    other_gpu_id: int
    p2p_accessible: bool
    link_type: str


class AcceleratorInfo(BaseModel):
    """Accelerator information."""
    gpu_id: int
    model_name: str
    memory_capacity: int
    memory_used: int | None = None
    average_power: float | None = None
    topology: list[PCIEInfo] | None = None

class SystemInfo(BaseModel):
    processor_name: str
    accelerators: list[AcceleratorInfo]
    software_details: str | None = None 
    driver_versions: dict | None = None

