__version__ = "0.1.0"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-ovhcloud",  # Required
        "name": "OVHcloud",  # Required
        "description": "OVHcloud Apache Airflow provider integration..",  # Required
        # "connection-types": [
        #     {
        #         "connection-type": "sample",
        #         "hook-class-name": "sample_provider.hooks.sample.SampleHook"
        #     }
        # ],
        # "extra-links": ["sample_provider.operators.sample.SampleOperatorExtraLink"],
        "versions": [__version__],  # Required
    }
