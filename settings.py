from pydantic import BaseSettings


# Any of these can be overridden via environment variables with matching names
class Settings(BaseSettings):
    # User or organization name, used for "user/image" -name generation
    DOCKER_USER = "digitallivinginternational"  # Hopefully we'll get a shorter one


conf = Settings()
