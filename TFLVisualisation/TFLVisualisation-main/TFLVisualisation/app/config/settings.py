from functools import lru_cache
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Pydantic settings for the application.
    Add all the environment variables that you want to use in the application.
    """

    environment: str = "DEV"
    debug: bool = True

    @model_validator(mode="after")
    def post_validator(self) -> Any:
        """
        Post validation method. This method is called after the validation of the settings. If the environment is PROD,
        set debug to False.

        :return: AppSettings
        """
        if self.environment == "PROD":
            self.debug = False
        return self


@lru_cache()
def __settings() -> AppSettings:
    """
    Load the settings from the environment variables. Cache the settings to avoid loading them multiple times.
    :return:
    """
    return AppSettings()


settings: AppSettings = __settings()
