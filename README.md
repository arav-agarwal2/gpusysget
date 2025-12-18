# A Simple POC of a GPU-System Monitor


## Part 1: Metrics Collected

While these are definitely NOT an exhaustive list of GPU metrics for ML Perf Inference benchmarking, this POC collects the following metrics:

- GPU Model Name
    - Important for correctness to ensure we know what GPU we are benchmarking on.
    - This is mandatory for ML Perf Inference submissions.
    - There should be no issues in collecting this metric if ran alongside a Docker container.
- GPU ID
    - Important for correctness so we can identify which PCIe index the GPU is located at.
    - This is optional in the context of ML Perf Inference submissions.
    - This should be easy to collect even when ran alongside a Docker container.
- GPU Memory Utilization and Capacity
    - This is important to understand the performance of the ML Perf Inference submission. I'm collecting both the utilization and capacity to make sure there are no additional workloads running on the GPU during benchmarking.
    - Utilization is optional, but capacity is mandatory for ML Perf Inference submissions.
    - This would be slightly incorrect if ran alongside a Docker container, as there could be far less memory allocated to the container than the full GPU capacity if used in a k8s system with system resource limits.
- GPU Average Power Usage
    - This is important to understand the performance of the submission, as generally higher power usage indicates higher performance.
    - This is optional for ML Perf Inference submissions.
    - This should still be fine when ran alongside a Docker container.
- GPU PCIe Link Type
    - This is important to understand the performance of the submission, as generally higher PCIe link types (e.g. Gen4 vs Gen3) indicate higher performance.
    - This is required for ML Perf Inference submissions, as specified in the ML Perf inference specification. If I had more time, I'd implement getting the bandwidths as well.
    - This should still be fine when ran alongside a Docker container.
- GPU PCIe P2P Accessiblility
    - This is important to understand the performance of the submission, as generally having P2P access between GPUs indicates higher performance for multi-GPU workloads.
    - This is probably optional for ML Perf Inference submissions, but should be recorded for auditability.
    - This should still be fine when ran alongside a Docker container.
- Processor Name
    - This is important to understand the performance of the submission, as generally better processors indicate better overall system performance.
    - This should be mandatory for ML Perf Inference submissions.
    - This should be fine when ran alongside a Docker container.

## Part 2: Running the POC

To install dependencies, run:

```bash
uv sync
```

Otherwise, feel free to install the dependencies manually:

```bash
pip install -r requirements.txt
```

Afterwards, to run the POC, simply run:

```bash
fastapi dev --port 8001
```

(Note: This is obviously not production-ready. When deploying in production, please run using uvicorn)

Then, to see the collected metrics, navigate to:

```
http://localhost:8001/stats
```

## Part 3: Client-Server Interaction

In general, we'd want to collect this data twice; once before and once after the run.

This is for two reasons:
1. We need to ensure the system doesn't change during the run. For all metrics except memory utilization and power usage, these should be identical.
2. For memory utilization and power usage, we need to see the difference to make sure that again nothing has changed during the run. If memory utilization or power usage is higher, there may be other loads on the GPU during the run which may affect performance.