import os
from dotenv import load_dotenv, find_dotenv

# Loading .env file
load_dotenv(find_dotenv(), override=True)

# Environment variables
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")
AZURE_CONTAINER_NAME_AUDIO_SUMMARY = os.environ.get("AZURE_CONTAINER_NAME_AUDIO_SUMMARY")
SECURITY_KEY = os.environ.get("SECURITY_KEY")
AUDIO_PATH = os.environ.get("AUDIO_PATH")

# OpenAI Error:
OPENAI_ERROR = "We apologize for the inconvenience. Our server is currently experiencing technical difficulties, which are likely temporary. Please try your request again in a little while."

# Safety configurations
safety_config = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]