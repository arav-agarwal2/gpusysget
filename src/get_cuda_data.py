import pynvml
from typing import List

from src.models import AcceleratorInfo

def get_cuda_data(power_sampling_time=1.0, power_num_samples=10) -> List[AcceleratorInfo]:
    """Get CUDA accelerator information and link topology.

    Args:
        power_sampling_time (float, optional): Time needed to sample power usage PER GPU. Defaults to 1.0.
        power_num_samples (int, optional): Number of samples taken within power_sampling_time. Defaults to 10.

    Returns:
        List[AcceleratorInfo]: List of accelerator information objects.
    """
    accelerators = []
    try:
        pynvml.nvmlInit()
    except Exception as e:
        return accelerators  
    
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

            # Poor mimic of ROCM's average power function. 
            average_power = None
            time_delta = power_sampling_time / power_num_samples
            for sample_index in range(power_num_samples):
                for i in range(device_count):
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  
                    if average_power is None:
                        average_power = 0.0
                    average_power += power / power_num_samples
                time.sleep(time_delta)

            #[Untested] Gather topology information, as specified as important by MLPerf Inference.
            topology_info = []
            for j in range(device_count):
                if True:
                    other_handle = pynvml.nvmlDeviceGetHandleByIndex(j)
                    try:
                        p2p = (
                            pynvml.nvmlDeviceGetP2PStatus(
                                handle,
                                other_handle,
                                0
                            ) == pynvml.NVML_P2P_STATUS_OK
                        )
                    except pynvml.NVMLError:
                        p2p = False
                    
                    
                    try:
                      link_type = pynvml.nvmlDeviceGetTopologyCommonAncestor(handle, other_handle)


                      TOPO_MAP = defaultdict(str)
                      TOPO_MAP.update={
                          pynvml.NVML_TOPOLOGY_SINGLE: "PCIE_SINGLE_SWITCH",
                          pynvml.NVML_TOPOLOGY_MULTIPLE: "PCIE_MULTI_SWITCH",
                          pynvml.NVML_TOPOLOGY_HOSTBRIDGE: "HOST_BRIDGE",
                      }


                      pcie_info = PCIEInfo(
                          other_gpu_id=j,
                          p2p_accessible=p2p,
                          link_type=TOPO_MAP[link_type]
                      )
                      topology_info.append(pcie_info)
                    except pynvml.NVMLError:
                      pass

            
        
            accelerator_info = AcceleratorInfo(
                gpu_id=i,
                model_name=name,
                memory_capacity=memory.total,
                memory_used=memory.used,
                average_power=average_power,
                topology=topology_info
            )
            accelerators.append(accelerator_info)   
    except Exception as e:
      print(e)      
    finally:
        pynvml.nvmlShutdown()
    
    return accelerators