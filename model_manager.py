import logging

from kubernetes import client, config

config.load_kube_config()

logging.basicConfig(level=logging.INFO)


class ModelManager:
    _api_version = "batch/v1"

    def __init__(self, namespace, container_params, pod_params, job_params):

        # Initialize K8s API instances for batch process
        self.core_api = client.CoreV1Api()
        self.batch_api = client.BatchV1Api()

        self.namespace = namespace

        # Parameters
        self.container_params = container_params
        self.pod_params = pod_params
        self.job_params = job_params

    def create_namespace(self):

        namespaces = self.core_api.list_namespace()
        all_namespaces = []
        for ns in namespaces.items:
            all_namespaces.append(ns.metadata.name)

        if self.namespace in all_namespaces:
            logging.info(f"Namespace {self.namespace} already exists. Reusing.")
        else:
            namespace_metadata = client.V1ObjectMeta(name=self.namespace)
            self.core_api.create_namespace(
                client.V1Namespace(metadata=namespace_metadata)
            )
            logging.info(f"Created namespace {self.namespace}.")

    def create_container(self):
        container = client.V1Container(
            name=self.container_params["name"],
            image_pull_policy=self.container_params["image_pull_policy"],
        )

        # TODO: programmtically call the right model
        container.command = ["python3", "-u", "/main.py"]
        container.args = [str(args) for args in self.container_params["args"]]

        container.image = self.container_params["image"]

        logging.info(f"Created container with image {self.container_params['image']}")

        return container

    def create_pod_template(self):
        pod_metadata = client.V1ObjectMeta(
            name=self.pod_params["name"], labels=self.pod_params["labels"],
        )
        pod_template = client.V1PodTemplateSpec(metadata=pod_metadata)
        pod_template.spec = client.V1PodSpec(
            containers=[self.create_container()], restart_policy="Never"
        )
        logging.info(f"Created pod template with name {self.pod_params['name']}.")

        return pod_template

    def create_job(self):
        job_metadata = client.V1ObjectMeta(
            name=f"{self.job_params['name']}", labels=self.job_params["labels"],
        )

        job = client.V1Job(
            spec=client.V1JobSpec(backoff_limit=0, template=self.create_pod_template()),
            metadata=job_metadata,
            kind="Job",
            api_version=self._api_version,
        )

        logging.info(f"Created job with name {self.job_params['name']}.")

        return job

    def launch_worker(self):

        self.batch_api.create_namespaced_job(self.namespace, self.create_job())
        logging.info(f"Launched pod.")

    def get_job_status(self):

        jobs = self.batch_api.list_namespaced_job(namespace=self.namespace)
        return jobs.items[0].status.succeeded

    def delete_old_jobs(self):

        """ Delete old jobs """
        jobs = self.batch_api.list_namespaced_job(namespace=self.namespace)

        for job in jobs.items:
            if job.status.succeeded:
                self.batch_api.delete_namespaced_job(
                    namespace=self.namespace, name=job.metadata.name,
                )
                logging.info(f"Deleted job {job.metadata.name}")

    def delete_old_pods(self):

        """ Delete pods that succeeded previously """
        pods = self.core_api.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=f"name={self.pod_params['labels']['name']}",
        )

        for pod in pods.items:
            if pod.status.phase == "Succeeded":
                self.core_api.delete_namespaced_pod(
                    name=pod.metadata.name, namespace=self.namespace
                )
                logging.info(f"Deleted pod {pod.metadata.name}")
