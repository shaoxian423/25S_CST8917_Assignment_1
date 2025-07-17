import logging
import os
   
from PIL import Image   
from io import BytesIO
from azure.storage.blob import BlobServiceClient

def main(input_data: dict) -> dict:
       try:
           blob_name = input_data["blob_name"]
           file_name = blob_name.split("/")[-1]  

           conn_str = os.environ["AzureWebJobsStorage"]
           blob_service = BlobServiceClient.from_connection_string(conn_str)
           blob_client = blob_service.get_blob_client(container="images-input", blob=file_name)

           stream = blob_client.download_blob().readall()
           image = Image.open(BytesIO(stream))

           logging.info(f"Image format detected by Pillow: {image.format}")
           logging.info(f"Image info: {image.info}")
           metadata = {
               "FileName": file_name,
               "FileSizeKB": round(len(stream) / 1024, 2),
               "Width": image.width,
               "Height": image.height,
               "Format": image.format
           }

           logging.info(f"Extracted metadata for {blob_name}: {metadata}")
           return metadata
       except Exception as e:
           logging.error(f"Error extracting metadata for {blob_name}: {str(e)}")
           raise