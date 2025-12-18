from platform import processor
from fastapi import FastAPI
import json
import uvicorn
import platform
from src.get_rocm_data import get_rocm_data
from src.get_cuda_data import get_cuda_data
from src.models import *

app = FastAPI()


@app.get("/stats")
def get_stats() -> SystemInfo:
    cuda_data = get_cuda_data()
    rocm_data = get_rocm_data()
    accelerator_data = cuda_data + rocm_data 

    system_info = SystemInfo(
        processor_name=platform.processor(),
        accelerators=accelerator_data
    )
    return system_info
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)