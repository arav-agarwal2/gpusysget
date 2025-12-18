from src.models import AcceleratorInfo
from typing import List

from pyrsmi import rocml

def get_rocm_data() -> List[AcceleratorInfo]:
    """Get ROCM accelerator information and link topology."""

    accelerators = []

    try:
        rocml.smi_initialize()
    except Exception as e:
        return accelerators 

    try:
        device_count = rocml.smi_get_device_count()
        
        for i in range(device_count):
            name = rocml.smi_get_device_name(i)
            dev_id = rocml.smi_get_device_id(i)
            memory_total = rocml.smi_get_device_memory_total(i)
            memory_used = rocml.smi_get_device_memory_used(i)
            gpu_power = rocml.smi_get_device_average_power(i)
            
            topology_info = []
            for j in range(device_count):
                if i != j:
                    # Untested as I don't have access to multiple GPUs.
                    p2p = rocml.smi_is_device_p2p_accessible(i, j)
                    link_type, _ = rocml.smi_get_device_link_type(i,j)
                    pcie_info = PCIEInfo(
                        other_gpu_id=j,
                        p2p_accessible=p2p,
                        link_type=str(link_type) # Untested conversion. May fail.
                    )
                    topology_info.append(pcie_info)
            
            accelerator_info = AcceleratorInfo(
                gpu_id=dev_id,
                model_name=name,
                memory_capacity=memory_total,
                memory_used=memory_used,
                average_power=gpu_power,
                topology=topology_info
            )

            accelerators.append(accelerator_info)
        
    except Exception as e:
        # Not using logging as this is an MVP - would be better to use logging library instead.
        print(f"Error retrieving ROCM data: {e}")
    finally:
        rocml.smi_shutdown()
    
    return accelerators
