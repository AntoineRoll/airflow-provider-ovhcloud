from typing import Optional
from airflow.models import BaseOperator
from airflow.exceptions import AirflowException
from ovhcloud.hooks.api import OvhcloudApiHook


class AiTrainingJobOperator(BaseOperator):

    template_fields = (
        "job_name",
        "docker_image",
        "command",
        "resources",
        "volumes",
        "region"
    )

    def __init__(
        self,
        docker_image: str,
        command: list[str],
        resources: dict,
        job_name: str,
        volumes: list[dict],
        region: str,
        labels: dict[str, str] = None,
        environment_variables: list[dict[str, str]] = None,
        ovhcloud_conn_id: str = "ovhcloud_default",
        project_id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.project_id = project_id
        self.conn_id = ovhcloud_conn_id
        self.region = region

        self.docker_image = docker_image
        self.command = command
        self.resources = resources

        self.job_name = job_name
        self.volumes = volumes
        self.labels = labels or {}
        self.environment_variables = environment_variables or []

    def execute(self, context):
        ovh_api_hook = OvhcloudApiHook(ovhcloud_conn_id=self.conn_id)

        if self.project_id is not None:
            ovh_api_hook.cloud_project_id = None
        elif ovh_api_hook.cloud_project_id is None:
            raise AirflowException("Cloud Project ID is not set.")
        
        job_payload = {
            "image": self.docker_image,
            "command": self.command,
            "resources": self.resources,
            "name": self.job_name,
            "volumes": self.volumes,
            "region": self.region,
            "labels": self.labels,
            "envVars": self.environment_variables,
        }

        result = ovh_api_hook.create_ai_training_job(
            job_payload
        )

        if result.status_code != 200:
            raise AirflowException(
                f"Error creating job: {result.json()}"
            )

        job_details = result.json()

        context['ti'].xcom_push("job_id", job_details["id"])