from pydantic import BaseSettings


# Any of these can be overridden via environment variables with matching names
class Settings(BaseSettings):
    # User or organization name, used for "user/image" -name generation
    DOCKER_USER = "ghcr.io/lietu"

    # List of images that should be built beforehand
    PRIORITY_BUILDS = [
        [
            "ubuntu-base/22.04",
            "nginx-base/alpine-nginx",
        ],
        [
            "python-base/ubuntu22.04-python3.10",
            "python-base/ubuntu22.04-python3.11",
        ],
        [
            "python-base/ubuntu22.04-python3.10-nginx",
        ],
    ]


conf = Settings()
