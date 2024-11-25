import re
import os
from gtts import gTTS
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceNotFoundError
from constants import AZURE_CONTAINER_NAME_AUDIO_SUMMARY, AZURE_STORAGE_CONNECTION_STRING, AUDIO_PATH


def download_blob(storage_connection_string, container_name, blob_name):
    """
    Downloads the content of a blob from Azure Storage.

    Parameters:
    - storage_connection_string (str): The connection string for the Azure Storage account.
    - container_name (str): The name of the container where the blob is located.
    - blob_name (str): The name of the blob to download.

    Returns:
    - bytes: The content of the downloaded blob.
    """
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(
            storage_connection_string
        )

        # Create ContainerClient
        container_client = blob_service_client.get_container_client(container_name)

        # Create BlobClient
        blob_client = container_client.get_blob_client(blob_name)

        # Download blob content
        blob_data = blob_client.download_blob()
        return blob_data.readall()
    except ResourceNotFoundError as e:
        return None
    except Exception as e:
        return None


def generate_and_upload_audio(text, file_name, app):
    """
    Generates audio from text using gtts, uploads the file to Azure Blob Storage.

    Parameters:
        text (str): The text to convert to audio.
        file_name (str): The name of the audio file to generate and upload.
        app: The Flask application instance for logging purposes.

    Returns:
        None
    """
    try:
        file_path = f"{AUDIO_PATH}/{file_name}"
        
        gtts = gTTS(text)
        gtts.save(file_path)
        app.logger.info("Audio file generated")
        
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME_AUDIO_SUMMARY)
        content_settings = ContentSettings(content_type="audio/mpeg")
        
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=file_name, data=data, content_settings=content_settings)
            
        os.remove(file_path)
        app.logger.info("Audio file uploaded")
    except Exception as e:
        app.logger.info(f"Error in Generating Audio File: {str(e)}")


def remove_special_characters(text):
    """
    Remove special characters from the given text.
    """
    return re.sub(r'[#*-]', '', text)
