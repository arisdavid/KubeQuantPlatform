import json
import logging
import time
import uuid
from collections import namedtuple

import boto3
from model_orchestrator import ModelOrchestrator

logging.basicConfig(level=logging.INFO)

queue_name = "s3-event-notification-queue"
region_name = "us-east-1"
namespace = "rqmp"
queue_wait_time = 10
max_jobs = 5

SQSStatus = namedtuple("QueueStatus", "messages_available messages_processed")


class KubernetesParameters:

    _image_pull_policy = "Never"
    _restart_policy = "Never"

    def __init__(self, model_name, bucket_name, file_name):
        self.model_name = model_name

        # args = [bucket_name, file_name]
        args = [1000000, 900000, 500000, 0.18, 0.12]

        if model_name == "kmv":
            self.container_name = "credit-models"
            self.container_image = "credit-models:latest"
            self.container_args = args

            self.pod_name = f"cm-{uuid.uuid4()}"
            self.pod_labels = dict(name="credit-models", type="pod")

            self.job_name = f"cm-{uuid.uuid4()}"
            self.job_labels = dict(name="credit-models", type="job")

        else:
            self.container_name = "credit-models"
            self.container_image = "credit-models:latest"
            self.container_args = args

            self.pod_name = f"cm-{uuid.uuid4()}"
            self.pod_labels = dict(name="credit-models", type="pod")

            self.job_name = f"cm-{uuid.uuid4()}"
            self.job_labels = dict(name="credit-models", type="job")

    def make_parameters(self):

        parameters = dict(
            container=dict(
                name=self.container_name,
                image_pull_policy=self._image_pull_policy,
                image=self.container_image,
                args=self.container_args,
            ),
            pod=dict(
                name=self.pod_name,
                restart_policy=self._restart_policy,
                labels=self.pod_labels,
            ),
            job=dict(name=self.job_name, labels=self.job_labels,),
        )

        return parameters

    @property
    def parameters(self):
        return self.parameters


class SQSManager:
    def __init__(self):

        logging.info(
            f"Initialising SQSManager instance with queue_name: {queue_name}, "
        )

        sqs = boto3.resource("sqs", region_name=region_name)
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)
        self.queue_name = queue_name

    def process_message(self):

        self.queue.reload()
        messages_available = int(self.queue.attributes["ApproximateNumberOfMessages"])

        processed_messages = 0

        if messages_available > 0:

            logging.info(f"SQS queue has {messages_available} messages available.")

            messages = self.queue.receive_messages(
                MaxNumberOfMessages=1, WaitTimeSeconds=queue_wait_time,
            )

            for message in messages:

                message_dict = json.loads(message.body)

                if "Records" in message_dict:
                    if "s3" in message_dict["Records"][0]:
                        bucket_name = message_dict["Records"][0]["s3"]["bucket"]["name"]
                        file_name = message_dict["Records"][0]["s3"]["object"]["key"]

                        model = bucket_name.split("-")[-1]

                        param_obj = KubernetesParameters(model, bucket_name, file_name)
                        params = param_obj.make_parameters()

                        # Call Model Manager
                        k8s_object = ModelOrchestrator(
                            namespace,
                            params.get("container"),
                            params.get("pod"),
                            params.get("job"),
                        )

                        # k8s_object.create_namespace()
                        k8s_object.launch_worker()

                        job_status = None
                        logging.info("Waiting for job to complete.")
                        while job_status is None:
                            job_status = k8s_object.get_job_status()

                        logging.info("Job complete.")
                        k8s_object.delete_old_jobs()
                        k8s_object.delete_old_pods()
                        processed_messages += 1

                        self.queue.delete_messages(
                            Entries=[
                                {
                                    "Id": message.message_id,
                                    "ReceiptHandle": message.receipt_handle,
                                }
                            ]
                        )

            return SQSStatus(messages_available, processed_messages)

        else:

            logging.info(f"SQS queue is empty.")
            return SQSStatus(messages_available, 0)


if __name__ == "__main__":

    sqs_queue_manager = SQSManager()

    while True:

        status = sqs_queue_manager.process_message()

        if status.messages_processed is None or status.messages_processed == 0:
            time.sleep(queue_wait_time)
