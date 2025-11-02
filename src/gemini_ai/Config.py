import os
import sys

"""
Holds all necessary configuration settings for the GitStory CLI.
"""


class Config:
    # Static variable for the API key environment variable name
    API_KEY_ENV_VAR = "GITSTORY_LLM_API_KEY"
    DEFAULT_MODEL = "Z.ai GLM-4.5"

    # defines the structure of a Config object
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    # loads configuration settings from env variables
    @classmethod
    def load():
        api_key = os.getenv(Config.API_KEY_ENV_VAR)

        if not api_key:
            print(f"ERROR: The environment variable {api_key} is not set.")
            print("Please set your LLM API key to proceed.")
            # exits since app cannot function without the key
            sys.exit(1)

        model = os.getenv(Config.DEFAULT_MODEL)

        # Return a new Config object with the loaded values
        return Config(api_key=api_key, model=model)
