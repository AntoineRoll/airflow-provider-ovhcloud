__version__ = "0.1.1.dev5"


## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-ovhcloud",  # Required
        "name": "OVHcloud",  # Required
        "description": "OVHcloud Apache Airflow provider integration.",  # Required
        "connection-types": [
            {
                "connection-type": "objectstorage",
                "hook-class-name": "ovhcloud.hooks.object_storage.ObjectStorageHook",
            }
        ],
        # "extra-links": ["sample_provider.operators.sample.SampleOperatorExtraLink"],
        "versions": [__version__],  # Required
    }
