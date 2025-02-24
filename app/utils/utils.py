import os
from typing import Dict, Any

class FromEnv:
    """
    A class to handle environment variable configurations.
    """

    @staticmethod
    def get_models() -> Dict[str, str]:
        """
        Returns a dictionary of models that start with REASONING_MODEL_
        """
        model_dict = {}
        for key, value in os.environ.items():
            if key.startswith("REASONING_MODEL_"):
                model_dict[key.replace("REASONING_MODEL_", "")] = value
        return model_dict

    @staticmethod
    def get_chat_api() -> Dict[str, str]:
        """
        Returns a dictionary of chat API configuration.
        """
        chat_api_dict = {
            "CHAT_API_KEY": os.getenv("CHAT_API_KEY", "ollama"),
            "CHAT_API_URL": os.getenv("CHAT_API_URL", "http://localhost:11434/v1/"),
        }
        return chat_api_dict

    # Add more methods here as needed

