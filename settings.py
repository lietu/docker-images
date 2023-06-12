from pydantic import BaseSettings


# Any of these can be overridden via environment variables with matching names
class Settings(BaseSettings):
    # GitHub container registry and organization name, used for "registry/org/image" -name generation
    DOCKER_USER = "ghcr.io/ioxiocom"

    LOCAL_REGISTRY = "localhost:5000"

    # List of images that should be built beforehand
    PRIORITY_BUILDS = [
        [
            "ubuntu-base/20.04",
            "ubuntu-base/22.04",
            "nginx-base/alpine-nginx",
        ],
        [
            "python-base/ubuntu20.04-python3.9",
            "python-base/ubuntu22.04-python3.10",
        ],
        [
            "python-base/ubuntu22.04-python3.10-nginx",
        ],
    ]


conf = Settings()
