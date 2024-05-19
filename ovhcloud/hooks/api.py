from __future__ import annotations

from typing import Any, Tuple

import ovh

from airflow.hooks.base import BaseHook
from functools import cached_property


class OvhcloudApiHook(BaseHook):
    """
    Hook that interacts with OVHcloud API endpoints with the ovh Python SDK.

    """

    conn_name_attr = "ovhcloud_conn_id"
    default_conn_name = "ovhcloud_default"
    conn_type = "ovhcloud"
    hook_name = "OVHcloud"

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField

        return {
            "endpoint": StringField(
                lazy_gettext("Endpoint"), widget=BS3TextFieldWidget()
            ),
            "application_key": StringField(
                lazy_gettext("Application key"), widget=BS3TextFieldWidget()
            ),
            "application_secret": PasswordField(
                lazy_gettext("Application Secret"), widget=BS3PasswordFieldWidget()
            ),
            "consumer_key": PasswordField(
                lazy_gettext("Consumer Key"), widget=BS3PasswordFieldWidget()
            )
        }

    @staticmethod
    def get_ui_field_behaviour() -> dict:
        """Returns custom field behaviour"""

        return {
            "hidden_fields": ["host", "port", "password", "login", "schema", "extra"],
            "relabeling": {},
            "placeholders": {},
        }

    def __init__(
        self,
        ovhcloud_conn_id: str = default_conn_name,
    ) -> None:
        super().__init__()
        self.ovhcloud_conn_id = ovhcloud_conn_id
        self.endpoint = None
        self.application_key = None
        self.application_secret = None
        self.consumer_key = None
        
    @cached_property
    def conn(self) -> ovh.Client:
        """Get the underlying OVH client and cache it

        Returns:
            ovh.Client: The OVH client with credentials from self.ovhcloud_conn_id
        """

        if self.ovhcloud_conn_id:
            conn = self.get_connection(self.ovhcloud_conn_id)
            
            self.endpoint = conn.extra_dejson['endpoint']
            self.application_key = conn.extra_dejson['application_key']
            self.application_secret = conn.extra_dejson['application_secret']
            self.consumer_key = conn.extra_dejson['consumer_key']
            
            ovh_client = ovh.Client(
                self.endpoint,
                self.application_key,
                self.application_secret,
                self.consumer_key
            )            

        return ovh_client

    def get_conn(self) -> ovh.Client:
        """
        Returns an ovh.Client to use for further requests.
        """
        return self.conn


    def test_connection(self) -> Tuple[bool, str]:
        """Test a connection"""
        client = self.get_conn()
        try:
            response = client.get('/me')
            return True, "Connection successfully tested"
        # except ovh.exceptions.APIError as api_error:
        #     return False, 'Requested /me. ' + str(api_error)
        except Exception as exception:
            return False, str(exception)