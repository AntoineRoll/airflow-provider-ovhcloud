from typing import Optional
from airflow.models import BaseOperator
from ovhcloud.hooks.api import OvhcloudApiHook


class AiTrainingJobOperator(BaseOperator):
    def __init__(
        self,
        ovhcloud_conn_id: str = "ovhcloud_default",
        project_id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.project_id = project_id
        self.conn_id = ovhcloud_conn_id

    def execute(self, context):
        ovh_api_hook = OvhcloudApiHook(ovhcloud_conn_id=self.conn_id)

        if self.project_id is not None:
            ovh_api_hook.project_id = None
