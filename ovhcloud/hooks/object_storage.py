from __future__ import annotations

import json
from typing import Any, Tuple

import boto3.session

from airflow.hooks.base import BaseHook

import boto3


class ObjectStorageHook(BaseHook):
    """
    Object Storage hook for OVHcloud Public Cloud.

    :param objectstorage_conn_id: ...
    :type objectstorage_conn_id: str
    """

    conn_name_attr = "objectstorage_conn_id"
    default_conn_name = "objectstorage_default"
    conn_type = "objectstorage"
    hook_name = "OVHcloud ObjectStorage"

    def __init__(self, objectstorage_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.objectstorage_conn_id = objectstorage_conn_id

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import (
            BS3PasswordFieldWidget,
            BS3TextFieldWidget,
        )
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField

        return {
            "endpoint_url": StringField(
                lazy_gettext("Endpoint URL"), widget=BS3TextFieldWidget()
            ),
            "region_name": StringField(
                lazy_gettext("Region name"), widget=BS3TextFieldWidget()
            ),
            "access_key": StringField(
                lazy_gettext("Access Key"), widget=BS3TextFieldWidget()
            ),
            "secret_key": PasswordField(
                lazy_gettext("Secret Key"), widget=BS3PasswordFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> dict:
        """Returns custom field behaviour"""

        return {
            "hidden_fields": ["host", "port", "password", "login", "schema", "extra"],
            "relabeling": {},
            "placeholders": {},
        }

    def get_conn(self) -> boto3.session.Session.client:
        """
        Returns boto3 S3 client
        """

        if self.objectstorage_conn_id:
            conn = self.get_connection(self.objectstorage_conn_id)

            self.endpoint_url = conn.extra_dejson['endpoint_url']
            self.region_name = conn.extra_dejson['region_name']
            self.access_key = conn.extra_dejson['access_key']
            self.secret_key = conn.extra_dejson['secret_key']

        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

        return client

    def test_connection(self) -> tuple[bool, str]:
        """Test Object Storage connectivity from UI."""
        try:
            s3_client = self.get_conn()
            response = s3_client.list_buckets()
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                return False, json.dumps(response["ResponseMetadata"])
        except Exception as e:
            return False, str(e)

        return True, "Connection successfully tested."
    
