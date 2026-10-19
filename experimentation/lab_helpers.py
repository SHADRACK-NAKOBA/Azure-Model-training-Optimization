"""Helpers shared by the lab notebooks (Prince Hands-on Lab).

- get_ml_client():        connect to the workspace from an Azure ML compute instance
- get_sklearn_environment(): pick a scikit-learn environment that exists in YOUR workspace

Why the environment helper exists: Azure regularly retires old "curated" environments
(the original lab used AzureML-sklearn-1.0-ubuntu20.04-py38-cpu, which is being
phased out). Hard-coding one name means the lab breaks the day it is retired.
This helper tries the current curated names first and, if none is available,
creates a small custom environment from environment/conda.yml instead.
"""
from pathlib import Path

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment

HERE = Path(__file__).resolve().parent

# Tried in order. The first one that exists is used.
CURATED_CANDIDATES = [
    ("registry", "sklearn-1.5"),
    ("workspace", "AzureML-sklearn-1.5"),
    ("registry", "sklearn-1.1"),
    ("workspace", "AzureML-sklearn-1.0-ubuntu20.04-py38-cpu"),
]
CUSTOM_ENV_NAME = "prince-sklearn-env"
CUSTOM_ENV_IMAGE = "mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest"


def get_credential():
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    try:
        credential = DefaultAzureCredential()
        # Check the credential can get a token
        credential.get_token("https://management.azure.com/.default")
    except Exception:
        # Fall back to signing in through the browser
        credential = InteractiveBrowserCredential()
    return credential


def get_ml_client(credential=None) -> MLClient:
    credential = credential or get_credential()
    try:
        # On an Azure ML compute instance, the workspace details are already configured
        ml_client = MLClient.from_config(credential=credential)
    except Exception as exc:
        raise RuntimeError(
            "Could not find the workspace configuration. Run this notebook on your Azure ML "
            "compute instance (Notebooks page in the studio), not on your own computer."
        ) from exc
    print(f"Connected to workspace: {ml_client.workspace_name}")
    return ml_client


def get_sklearn_environment(ml_client: MLClient, verbose: bool = True) -> str:
    """Return an environment reference string that works in this workspace."""
    registry_client = None
    for scope, name in CURATED_CANDIDATES:
        try:
            if scope == "registry":
                if registry_client is None:
                    registry_client = MLClient(credential=ml_client._credential, registry_name="azureml")
                registry_client.environments.get(name, label="latest")
                ref = f"azureml://registries/azureml/environments/{name}/labels/latest"
            else:
                ml_client.environments.get(name, label="latest")
                ref = f"{name}@latest"
            if verbose:
                print(f"Using curated environment: {ref}")
            return ref
        except Exception:
            continue

    # Nothing curated found: create (or reuse) a custom environment.
    if verbose:
        print("No curated scikit-learn environment found - creating a custom one "
              "(the first job will take ~10 extra minutes to build it).")
    env = ml_client.environments.create_or_update(
        Environment(
            name=CUSTOM_ENV_NAME,
            description="scikit-learn + MLflow environment for the Prince MLOps lab",
            image=CUSTOM_ENV_IMAGE,
            conda_file=str(HERE / "environment" / "conda.yml"),
        )
    )
    ref = f"{env.name}:{env.version}"
    if verbose:
        print(f"Using custom environment: {ref}")
    return ref
