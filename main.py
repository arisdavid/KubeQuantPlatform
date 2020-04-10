import argparse
import uuid

from model_manager import ModelManager

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    namespace = "rqmp"

    container_params = dict(
        name="credit-models",
        image_pull_policy="Never",
        image="credit-models:latest",
        args=["1000000", "900000", "500000", "0.18", "0.12"],
    )

    pod_params = dict(
        name=f"cm-{uuid.uuid4()}",
        restart_policy="Never",
        labels=dict(name="credit-models", type="pod"),
    )

    job_params = dict(
        name=f"cm-{uuid.uuid4()}", labels=dict(name="credit-models", type="job")
    )
    k8_object = ModelManager(namespace, container_params, pod_params, job_params)

    # Delete old jobs and pods
    k8_object.delete_old_jobs()
    k8_object.delete_old_pods()

    k8_object.create_namespace()
    k8_object.launch_worker()
