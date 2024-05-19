from airflow.models.baseoperator import BaseOperator
from ovhcloud.hooks.object_storage import ObjectStorageHook
from typing import Optional, Union

import logging

class LoadObjectOperator(BaseOperator):

    def __init__(self, 
        *,
        container: Optional[str] = None,
        key: str,
        filename: Optional[str] = None,
        data: Optional[Union[str, bytes]] = None,
        replace: bool = False,
        # encrypt: bool = False,
        # acl_policy: Optional[str] = None,
        encoding: str  = 'utf-8',
        # compression: Optional[str] = None,
        objectstorage_conn_id: str = 'objectstorage_default',
        **kwargs,
        ):

        super().__init__(**kwargs)

        if data is None and filename is None:
            raise ValueError("Either `data` or `filename` parameters must be specified.")
        
        if data is not None and filename is not None:
            raise ValueError("`data` and `filename` parameters can't be specified together.")

        self.objectstorage_conn_id = objectstorage_conn_id

        self.container = container
        self.key = key
        self.replace = replace
        
        self.filename = filename
        self.data = data
        self.encoding = encoding
        

    def execute(self, context):
        from io import BytesIO
        import botocore.exceptions
        
        object_storage_hook = ObjectStorageHook(
            self.objectstorage_conn_id
        )

        client = object_storage_hook.get_conn()

        if not self.replace:
            try:
                response = client.head_object(
                    Bucket=self.container,
                    Key=self.key
                )
                
                raise ValueError(
                    f"The specified Key '{self.key}' in Container '{self.container}' exists"
                    " and replace is set to False."
                )
            
            except botocore.exceptions.ClientError as error:
                if error.response["Error"]["Code"] == "404":
                    logging.info(f"Key: '{self.key}' does not exist in Container: '{self.container}'.")

        if self.filename:
            client.upload_file(
                Filename=self.filename,
                Bucket=self.container,
                key=self.key
            )
            return
        
        if isinstance(self.data, str):
            self.data = self.data.encode(self.encoding)


        data_buffer = BytesIO(self.data)

        client.upload_fileobj(
            Bucket=self.container,
            Key=self.key,
            Fileobj=data_buffer
        )